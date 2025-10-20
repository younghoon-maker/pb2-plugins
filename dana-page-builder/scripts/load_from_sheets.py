"""
DANA&PETA Product Data Loader
Loads 96-column product data from Google Sheets and downloads images
"""

import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PIL import Image

# Import configuration
from config import (
    ASSETS_DIR,
    COLOR_EXTRACTION_BRIGHTNESS_THRESHOLD,
    COLOR_EXTRACTION_CROP_PERCENT,
    COLOR_EXTRACTION_KMEANS_CLUSTERS,
    COLOR_EXTRACTION_KMEANS_ITERATIONS,
    LOG_DATE_FORMAT,
    LOG_FILE,
    LOG_FORMAT,
    PRODUCTS_DATA_PATH,
    REQUIRED_FIELDS,
    SCOPES,
    SERVICE_ACCOUNT_FILE,
    SHEET_ID,
    SHEET_NAME,
    SHEET_RANGE,
    TEMPLATE_COLUMNS,
    VERSION,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DanaDataLoader:
    """Load DANA&PETA product data from Google Sheets"""

    def __init__(self):
        """Initialize the data loader"""
        self.sheets_service = None
        self.drive_service = None
        self.products = []
        self.image_cache = set()

        # Create output directories
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        PRODUCTS_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Load existing images to cache
        if ASSETS_DIR.exists():
            self.image_cache = {
                f.name for f in ASSETS_DIR.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']
            }
            logger.info(f"📦 Loaded {len(self.image_cache)} existing images into cache")

    def authenticate(self) -> None:
        """Authenticate with Google APIs"""
        try:
            if not SERVICE_ACCOUNT_FILE.exists():
                raise FileNotFoundError(f"❌ Service Account file not found: {SERVICE_ACCOUNT_FILE}")

            credentials = service_account.Credentials.from_service_account_file(
                str(SERVICE_ACCOUNT_FILE),
                scopes=SCOPES
            )

            self.sheets_service = build('sheets', 'v4', credentials=credentials)
            self.drive_service = build('drive', 'v3', credentials=credentials)

            logger.info("✅ Google API authentication successful")

        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")
            raise

    def extract_dominant_color_improved(self, image_path: str) -> str:
        """
        V13: Extract dominant color using improved K-means algorithm
        - Center crop (30%) to focus on product
        - Brightness filter (< 240) to remove background
        - K-means clustering (3 clusters) to group colors
        - Select most dominant cluster

        Args:
            image_path: Path to image file

        Returns:
            HEX color code (e.g., "#d7c4ab")
        """
        try:
            # Load image
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Center crop to focus on product (remove background)
            width, height = img.size
            crop_percent = COLOR_EXTRACTION_CROP_PERCENT
            crop_width = int(width * crop_percent)
            crop_height = int(height * crop_percent)
            left = (width - crop_width) // 2
            top = (height - crop_height) // 2
            right = left + crop_width
            bottom = top + crop_height
            img_cropped = img.crop((left, top, right, bottom))

            # Convert to numpy array
            img_array = np.array(img_cropped)
            pixels = img_array.reshape(-1, 3)

            # Filter out bright pixels (background)
            brightness = np.mean(pixels, axis=1)
            dark_pixels = pixels[brightness < COLOR_EXTRACTION_BRIGHTNESS_THRESHOLD]

            if len(dark_pixels) < 10:
                logger.warning(f"⚠️  Not enough dark pixels in {image_path}, using all pixels")
                dark_pixels = pixels

            # K-means clustering
            n_clusters = min(COLOR_EXTRACTION_KMEANS_CLUSTERS, len(dark_pixels))

            # Simple K-means implementation
            np.random.seed(42)
            centroids = dark_pixels[np.random.choice(len(dark_pixels), n_clusters, replace=False)]

            for _ in range(COLOR_EXTRACTION_KMEANS_ITERATIONS):
                # Assign pixels to nearest centroid
                distances = np.sqrt(((dark_pixels[:, np.newaxis] - centroids) ** 2).sum(axis=2))
                labels = np.argmin(distances, axis=1)

                # Update centroids
                new_centroids = np.array([
                    dark_pixels[labels == i].mean(axis=0) if np.any(labels == i) else centroids[i]
                    for i in range(n_clusters)
                ])

                if np.allclose(centroids, new_centroids):
                    break

                centroids = new_centroids

            # Find most dominant cluster (most pixels)
            cluster_sizes = [np.sum(labels == i) for i in range(n_clusters)]
            dominant_cluster = np.argmax(cluster_sizes)
            dominant_color = centroids[dominant_cluster]

            # Convert to HEX
            hex_color = "#{:02x}{:02x}{:02x}".format(
                int(dominant_color[0]),
                int(dominant_color[1]),
                int(dominant_color[2])
            )

            logger.info(f"✅ Extracted dominant color from {Path(image_path).name}: {hex_color}")
            return hex_color

        except Exception as e:
            logger.error(f"❌ Color extraction failed for {image_path}: {e}")
            return "#cccccc"  # Default gray

    def extract_drive_file_id(self, url: str) -> Optional[str]:
        """Extract Google Drive file ID from URL"""
        if not url or url.strip() == "":
            return None

        patterns = [
            r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
            r'id=([a-zA-Z0-9_-]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def download_image(self, drive_url: str, output_filename: str) -> Optional[str]:
        """
        Download image from Google Drive

        Args:
            drive_url: Google Drive URL
            output_filename: Output filename

        Returns:
            Relative path to downloaded image or None
        """
        if not drive_url or drive_url.strip() == "":
            return None

        # Check cache
        if output_filename in self.image_cache:
            logger.info(f"♻️  Using cached image: {output_filename}")
            return f"../assets/images/{output_filename}"

        try:
            file_id = self.extract_drive_file_id(drive_url)
            if not file_id:
                logger.warning(f"⚠️  Invalid Drive URL: {drive_url}")
                return None

            # Download file
            request = self.drive_service.files().get_media(fileId=file_id)
            file_path = ASSETS_DIR / output_filename

            with open(file_path, 'wb') as f:
                downloader = request.execute()
                f.write(downloader if isinstance(downloader, bytes) else downloader.encode())

            self.image_cache.add(output_filename)
            logger.info(f"✅ Downloaded image: {output_filename}")

            return f"../assets/images/{output_filename}"

        except Exception as e:
            logger.error(f"❌ Failed to download {drive_url}: {e}")
            return None

    def load_products_from_sheets(self) -> None:
        """Load product data from unified template (템플릿 tab)"""
        try:
            logger.info(f"🚀 Loading DANA&PETA product data from unified template")
            logger.info(f"📊 Sheet range: {SHEET_NAME}!{SHEET_RANGE}")

            # Extract hyperlinks for all image columns
            logger.info(f"📊 Extracting hyperlinks from template...")
            rows = self.extract_hyperlinks_from_range(SHEET_NAME, SHEET_RANGE)

            if not rows:
                logger.warning("⚠️  No data found in sheet")
                return

            logger.info(f"📥 Processing {len(rows)} product rows...")

            for idx, row in enumerate(rows):
                try:
                    # Pad row to 302 columns if needed
                    while len(row) < 302:
                        row.append("")

                    product_code = row[TEMPLATE_COLUMNS["productCode"]].strip()
                    if not product_code:
                        logger.warning(f"⚠️  Row {idx + 2}: No product code, skipping")
                        continue

                    logger.info(f"📦 Processing product: {product_code}")

                    # Build product data from unified template
                    product = self.build_product_data(row, product_code)

                    if product:
                        self.products.append(product)
                        logger.info(f"✅ Loaded product: {product_code}")

                except Exception as e:
                    logger.error(f"❌ Error processing row {idx + 2}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    continue

            logger.info(f"✅ Successfully loaded {len(self.products)} products")

        except Exception as e:
            logger.error(f"❌ Failed to load products from sheets: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def is_empty_value(self, value: str) -> bool:
        """
        Check if a value should be considered empty and skipped
        Skip: '-', 'N/A', '#N/A', '#REF!', empty strings, whitespace
        """
        if not value:
            return True
        value = value.strip()
        return value in ['-', 'N/A', '#N/A', '#REF!', ''] or not value

    def build_product_data(self, row: List[str], product_code: str) -> Optional[Dict]:
        """Build product data structure from unified template (302 columns)"""
        try:
            # Basic info
            product = {
                "productCode": product_code,
                "title": row[TEMPLATE_COLUMNS["title"]].strip(),
                "mdComment": row[TEMPLATE_COLUMNS["mdComment"]].strip(),
                "sellingPoints": [
                    row[TEMPLATE_COLUMNS["sellingPoint1"]].strip(),
                    row[TEMPLATE_COLUMNS["sellingPoint2"]].strip(),
                    row[TEMPLATE_COLUMNS["sellingPoint3"]].strip()
                ],
                "images": {},
                "colors": [],
                "detailPoints": [],
                "gallery": [],
                "galleryByColor": {},
                "productShots": [],
                "fabricInfo": {},
                "productInfo": {},
                "sizeInfo": {"topSizes": [], "bottomSizes": []},
                "sizeImage": None
            }

            # Download main image
            main_image_url = row[TEMPLATE_COLUMNS["mainImage"]].strip()
            if main_image_url and not self.is_empty_value(main_image_url):
                main_image_path = self.download_image(
                    main_image_url,
                    f"{product_code}_main.jpg"
                )
                product["images"]["main_single"] = main_image_path

            # Process colors (4 colors with names and HEX codes)
            colors_data = []
            for i in range(1, 5):
                color_name = row[TEMPLATE_COLUMNS[f"color{i}Name"]].strip()
                color_hex = row[TEMPLATE_COLUMNS[f"color{i}Hex"]].strip()

                if color_name and not self.is_empty_value(color_name):
                    # Use provided HEX or extract from first gallery image
                    if color_hex and not self.is_empty_value(color_hex):
                        # Ensure HEX format
                        if not color_hex.startswith('#'):
                            color_hex = f"#{color_hex}"
                    else:
                        color_hex = "#cccccc"  # Default gray

                    colors_data.append({
                        "name": color_name,
                        "hex": color_hex
                    })

            product["colors"] = colors_data

            # Download detail point images (4 points)
            detail_points = []
            for i in range(1, 5):
                detail_image_url = row[TEMPLATE_COLUMNS[f"detailPoint{i}Image"]].strip()
                detail_text = row[TEMPLATE_COLUMNS[f"detailPoint{i}Text"]].strip()

                if detail_image_url and not self.is_empty_value(detail_image_url):
                    image_path = self.download_image(
                        detail_image_url,
                        f"{product_code}_detail_point_{i}.jpg"
                    )
                    if image_path:
                        detail_points.append({
                            "image": image_path,
                            "text": detail_text if not self.is_empty_value(detail_text) else ""
                        })

            product["detailPoints"] = detail_points

            # Download gallery images by color (8 colors × 12 images = 96 total)
            gallery_by_color = {}
            for color_num in range(1, 9):
                color_images = []
                for img_num in range(1, 13):
                    gallery_url = row[TEMPLATE_COLUMNS[f"color{color_num}Gallery{img_num}"]].strip()
                    if gallery_url and not self.is_empty_value(gallery_url):
                        image_path = self.download_image(
                            gallery_url,
                            f"{product_code}_gallery_color{color_num}_{img_num}.jpg"
                        )
                        if image_path:
                            color_images.append(image_path)

                if color_images:
                    gallery_by_color[f"color{color_num}"] = color_images

            product["galleryByColor"] = gallery_by_color

            # Download product shots by color (8 shots)
            product_shots = []
            for i in range(1, 9):
                shot_url = row[TEMPLATE_COLUMNS[f"color{i}ProductShot"]].strip()
                if shot_url and not self.is_empty_value(shot_url):
                    image_path = self.download_image(
                        shot_url,
                        f"{product_code}_shot_color{i}.jpg"
                    )
                    if image_path:
                        product_shots.append(image_path)

            product["productShots"] = product_shots

            # Fabric info
            fabric_image_url = row[TEMPLATE_COLUMNS["fabricImage"]].strip()
            if fabric_image_url and not self.is_empty_value(fabric_image_url):
                fabric_image_path = self.download_image(
                    fabric_image_url,
                    f"{product_code}_fabric.jpg"
                )

                fabric_composition = row[TEMPLATE_COLUMNS["fabricComposition"]].strip()
                fabric_desc = row[TEMPLATE_COLUMNS["fabricDesc"]].strip()

                product["fabricInfo"] = {
                    "image": fabric_image_path,
                    "composition": fabric_composition if not self.is_empty_value(fabric_composition) else "",
                    "description": fabric_desc if not self.is_empty_value(fabric_desc) else "",
                    "properties": {
                        "transparency": row[TEMPLATE_COLUMNS["fabricTransparency"]].strip(),
                        "stretch": row[TEMPLATE_COLUMNS["fabricStretch"]].strip(),
                        "lining": row[TEMPLATE_COLUMNS["fabricLining"]].strip(),
                        "thickness": row[TEMPLATE_COLUMNS["fabricThickness"]].strip(),
                        "season": row[TEMPLATE_COLUMNS["fabricSeason"]].strip()
                    }
                }

            # Size image (column 135 / EF)
            size_image_value = row[TEMPLATE_COLUMNS["sizeImage"]].strip()
            if size_image_value and not self.is_empty_value(size_image_value):
                product["sizeImage"] = size_image_value

            # Product info (6 fields: 제품명, 컬러명, 사이즈, 패브릭, 세탁법, 생산지)
            product["productInfo"] = {
                "productName": row[TEMPLATE_COLUMNS["productName"]].strip(),
                "colorName": row[TEMPLATE_COLUMNS["colorName"]].strip(),
                "sizeName": row[TEMPLATE_COLUMNS["sizeName"]].strip(),
                "fabric": row[TEMPLATE_COLUMNS["fabric"]].strip(),
                "washingInfo": row[TEMPLATE_COLUMNS["washingInfo"]].strip(),
                "origin": row[TEMPLATE_COLUMNS["origin"]].strip()
            }

            # Top sizes (10 sizes, 8 fields each)
            top_sizes = []
            for i in range(1, 11):
                size_name = row[TEMPLATE_COLUMNS[f"topSize{i}Name"]].strip()
                if size_name and not self.is_empty_value(size_name):
                    size_data = {
                        "name": size_name,
                        "shoulder": row[TEMPLATE_COLUMNS[f"topSize{i}Shoulder"]].strip(),
                        "chest": row[TEMPLATE_COLUMNS[f"topSize{i}Chest"]].strip(),
                        "hem": row[TEMPLATE_COLUMNS[f"topSize{i}Hem"]].strip(),
                        "sleeveLength": row[TEMPLATE_COLUMNS[f"topSize{i}SleeveLength"]].strip(),
                        "sleeveOpening": row[TEMPLATE_COLUMNS[f"topSize{i}SleeveOpening"]].strip(),
                        "totalLength": row[TEMPLATE_COLUMNS[f"topSize{i}TotalLength"]].strip(),
                        "optional": row[TEMPLATE_COLUMNS[f"topSize{i}Optional"]].strip()
                    }
                    top_sizes.append(size_data)

            product["sizeInfo"]["topSizes"] = top_sizes

            # Bottom sizes (10 sizes, 8 fields each)
            bottom_sizes = []
            for i in range(1, 11):
                size_name = row[TEMPLATE_COLUMNS[f"bottomSize{i}Name"]].strip()
                if size_name and not self.is_empty_value(size_name):
                    size_data = {
                        "name": size_name,
                        "waist": row[TEMPLATE_COLUMNS[f"bottomSize{i}Waist"]].strip(),
                        "hip": row[TEMPLATE_COLUMNS[f"bottomSize{i}Hip"]].strip(),
                        "thigh": row[TEMPLATE_COLUMNS[f"bottomSize{i}Thigh"]].strip(),
                        "hem": row[TEMPLATE_COLUMNS[f"bottomSize{i}Hem"]].strip(),
                        "rise": row[TEMPLATE_COLUMNS[f"bottomSize{i}Rise"]].strip(),
                        "totalLength": row[TEMPLATE_COLUMNS[f"bottomSize{i}TotalLength"]].strip(),
                        "optional": row[TEMPLATE_COLUMNS[f"bottomSize{i}Optional"]].strip()
                    }
                    bottom_sizes.append(size_data)

            product["sizeInfo"]["bottomSizes"] = bottom_sizes

            return product

        except Exception as e:
            logger.error(f"❌ Failed to build product data for {product_code}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    def extract_hyperlinks_from_range(self, sheet_name: str, range_spec: str) -> List[List[str]]:
        """
        Extract hyperlinks from Google Sheets cells

        Args:
            sheet_name: Name of the sheet
            range_spec: Range specification (e.g., "A2:KP100")

        Returns:
            List of rows with hyperlinks extracted
        """
        try:
            result = self.sheets_service.spreadsheets().get(
                spreadsheetId=SHEET_ID,
                ranges=[f"{sheet_name}!{range_spec}"],
                includeGridData=True
            ).execute()

            sheets = result.get('sheets', [])
            if not sheets:
                return []

            data = sheets[0].get('data', [])
            if not data:
                return []

            rows_data = data[0].get('rowData', [])
            extracted_rows = []

            for row in rows_data:
                values = row.get('values', [])
                row_values = []

                for cell in values:
                    # Check for hyperlink first
                    hyperlink = cell.get('hyperlink')
                    if hyperlink:
                        row_values.append(hyperlink)
                    else:
                        # Fall back to formatted value
                        formatted_value = cell.get('formattedValue', '')
                        row_values.append(formatted_value)

                extracted_rows.append(row_values)

            logger.info(f"✅ Extracted {len(extracted_rows)} rows with hyperlinks from {sheet_name}")
            return extracted_rows

        except Exception as e:
            logger.error(f"❌ Failed to extract hyperlinks: {e}")
            return []

    def save_products_json(self) -> None:
        """Save products data to JSON file"""
        try:
            data = {
                "products": self.products,
                "metadata": {
                    "totalCount": len(self.products),
                    "lastUpdated": datetime.now().isoformat(),
                    "version": VERSION,
                    "brand": "DANA&PETA"
                }
            }

            with open(PRODUCTS_DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"✅ Products data saved: {PRODUCTS_DATA_PATH}")
            logger.info(f"📊 Total products: {len(self.products)}")

        except Exception as e:
            logger.error(f"❌ Failed to save products JSON: {e}")
            raise

    def run(self) -> None:
        """Run the complete data loading process using unified template system"""
        try:
            logger.info("=" * 60)
            logger.info("DANA&PETA Product Data Loader - Unified Template System")
            logger.info("=" * 60)

            # Step 1: Authenticate
            logger.info("\n📝 Step 1: Authenticating with Google APIs...")
            self.authenticate()

            # Step 2: Load products from unified template
            logger.info("\n📝 Step 2: Loading products from unified template (템플릿 tab)...")
            logger.info("🔄 Using Unified Template System (302 columns)")
            self.load_products_from_sheets()

            # Step 3: Save JSON
            logger.info("\n📝 Step 3: Saving products data...")
            self.save_products_json()

            logger.info("\n" + "=" * 60)
            logger.info("✅ Data loading completed successfully!")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"\n❌ Data loading failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise


def main():
    """Main entry point"""
    loader = DanaDataLoader()
    loader.run()


if __name__ == "__main__":
    main()
