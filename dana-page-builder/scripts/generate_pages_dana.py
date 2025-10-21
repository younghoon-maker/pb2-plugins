"""
DANA&PETA HTML Page Generator
Generates product detail pages with DANA&PETA brand template
"""

import base64
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from config import (
    ASSETS_DIR,
    BRAND_LOGO_TEXT,
    BRAND_NAME,
    DATE_FORMAT,
    EDITABLE_FILE_PATTERN,
    EDITABLE_FOLDER,
    LOG_DATE_FORMAT,
    LOG_FILE,
    LOG_FORMAT,
    ORIGINAL_FILE_PATTERN,
    ORIGINAL_FOLDER,
    OUTPUT_DIR,
    PRODUCTS_DATA_PATH,
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


class DanaPageGenerator:
    """Generate DANA&PETA product detail pages"""

    def __init__(self):
        """Initialize the page generator"""
        self.products = []
        self.date_folder = datetime.now().strftime(DATE_FORMAT)
        self.output_original = OUTPUT_DIR / self.date_folder / ORIGINAL_FOLDER
        self.output_editable = OUTPUT_DIR / self.date_folder / EDITABLE_FOLDER

        # Create output directories
        self.output_original.mkdir(parents=True, exist_ok=True)
        self.output_editable.mkdir(parents=True, exist_ok=True)

    def load_products_data(self) -> None:
        """Load products from JSON file"""
        try:
            if not PRODUCTS_DATA_PATH.exists():
                raise FileNotFoundError(f"❌ Products data not found: {PRODUCTS_DATA_PATH}")

            with open(PRODUCTS_DATA_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.products = data.get('products', [])
            logger.info(f"✅ Loaded {len(self.products)} products from {PRODUCTS_DATA_PATH}")

        except Exception as e:
            logger.error(f"❌ Failed to load products data: {e}")
            raise

    def image_to_base64(self, image_path: str) -> Optional[str]:
        """Convert image to base64 data URL"""
        try:
            if not image_path or image_path.strip() == "":
                return None

            # Resolve relative path
            if image_path.startswith("../"):
                full_path = OUTPUT_DIR / image_path.replace("../", "")
            else:
                full_path = Path(image_path)

            if not full_path.exists():
                logger.warning(f"⚠️  Image not found: {full_path}")
                return None

            with open(full_path, 'rb') as f:
                image_data = f.read()
                base64_data = base64.b64encode(image_data).decode('utf-8')

            # Detect image format
            suffix = full_path.suffix.lower()
            mime_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }.get(suffix, 'image/jpeg')

            return f"data:{mime_type};base64,{base64_data}"

        except Exception as e:
            logger.error(f"❌ Failed to convert image to base64: {e}")
            return None

    def create_placeholder_image(self) -> str:
        """Create a placeholder SVG image as base64 data URL"""
        svg_content = '''<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
            <rect width="800" height="600" fill="#E0E0E0"/>
            <text x="400" y="280" font-family="Arial, sans-serif" font-size="24" fill="#757575" text-anchor="middle">이미지 없음</text>
            <text x="400" y="320" font-family="Arial, sans-serif" font-size="16" fill="#999999" text-anchor="middle">클릭하여 이미지 업로드</text>
        </svg>'''
        svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{svg_base64}"

    def generate_html(self, product: Dict, editable: bool = False) -> str:
        """Generate HTML for a product"""

        # Contenteditable class and attribute (must be at top since used throughout)
        editable_class = ' editable' if editable else ''
        contenteditable_attr = ' contenteditable="true"' if editable else ''

        # Convert images to base64
        main_image_base64 = self.image_to_base64(product["images"].get("main_single"))

        # Load DANA&PETA logo from reference/logo folder
        # Load white logo for hero section
        logo_white_path = Path(__file__).parent.parent / "reference" / "logo" / "dana&peta_logo.png"
        logo_white_base64 = self.image_to_base64(str(logo_white_path))

        # Load black logo for gallery logo groups (avoids filter: invert(1) issues with html2canvas)
        logo_black_path = Path(__file__).parent.parent / "reference" / "logo" / "dana&peta_logo_black.png"
        logo_black_base64 = self.image_to_base64(str(logo_black_path))

        # Build colors section HTML (horizontal swatches with color picker)
        colors_html = ""
        colors = product.get("colors", [])

        # Color swatches container
        colors_html += '<div class="color-swatches-container">'

        for idx, color in enumerate(colors):
            hex_color = color.get("hex", "#cccccc")
            color_name = color.get("name", "")

            # Calculate text color for contrast
            # Remove # and convert to RGB
            hex_val = hex_color.lstrip('#')
            r = int(hex_val[0:2], 16) if len(hex_val) >= 2 else 0
            g = int(hex_val[2:4], 16) if len(hex_val) >= 4 else 0
            b = int(hex_val[4:6], 16) if len(hex_val) >= 6 else 0
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            text_color = "#333" if brightness >= 128 else "#fff"

            contenteditable_color_name = f' contenteditable="true"' if editable else ''

            colors_html += f'''
            <div class="color-swatch-item" data-color-index="{idx}">
                <div class="color-swatch-wrapper">
                    <div class="color-swatch" style="background-color: {hex_color};">'''

            # Add color picker only in editable mode
            if editable:
                colors_html += f'''
                        <input type="color" value="{hex_color}"
                               class="hex-picker"
                               data-color-index="{idx}"
                               title="색상 변경 (스포이드 도구)">'''

            colors_html += f'''
                    </div>
                </div>
                <div class="color-name-swatch"{contenteditable_color_name}>{color_name}</div>
            </div>
            '''

        colors_html += '</div>'

        # Build selling points HTML
        selling_points_html = ""
        for idx, point in enumerate(product.get("sellingPoints", [])):
            if point:
                contenteditable_point = f' contenteditable="true"' if editable else ''
                selling_points_html += f'''
                <div class="selling-point">
                    <span class="point-number">0{idx + 1}</span>
                    <span class="point-text{editable_class}"{contenteditable_point}>{point}</span>
                </div>
                '''

        # Build detail points HTML (left-right layout)
        detail_points_html = ""
        for idx, point in enumerate(product.get("detailPoints", [])):
            # Render if text exists OR image exists
            has_text = point.get('text', '').strip()
            has_image = point.get('image')

            if not has_text and not has_image:
                continue

            # Use placeholder if no image
            point_image_base64 = self.image_to_base64(point.get("image"))
            if not point_image_base64:
                point_image_base64 = self.create_placeholder_image()

            frame_class = ' image-frame' if editable else ''
            data_id_attr = f' data-id="detailPoint{idx + 1}"' if editable else ''
            img_class = ' editable-image' if editable else ''

            detail_points_html += f'''
            <div class="detail-point-item">
                <div class="detail-point-image-wrapper{frame_class}"{data_id_attr}>
                    <img src="{point_image_base64}" alt="Detail point {idx + 1}" class="detail-point-image{img_class}">
                </div>
                <div class="detail-point-text-box">
                    <div class="detail-point-number">0{idx + 1}</div>
                    <div class="detail-point-text{editable_class}"{contenteditable_attr}>{point.get('text', '')}</div>
                </div>
            </div>
            '''

        # Build gallery HTML (organized by color with logo insertions)
        gallery_html = ""
        gallery_by_color = product.get("galleryByColor", {})
        colors = product.get("colors", [])

        if gallery_by_color and colors:
            # Use galleryByColor structure (color1, color2, etc.)
            # Pattern repeats for each color: 1-3 normal, 4-5 logo group 1, 6 normal, 7-8 logo group 2, 9+ normal
            for color_idx, color in enumerate(colors):
                color_key = f"color{color_idx + 1}"
                color_images = gallery_by_color.get(color_key, [])

                if color_images:
                    # Add color header
                    gallery_html += f'''
                <div class="gallery-color-header{editable_class}"{contenteditable_attr}>{color.get('name', '')}</div>
                '''

                    # Add images for this color with logo insertions
                    gallery_img_count = 0  # Track gallery image index for data-id
                    for img_idx, image_path in enumerate(color_images):
                        # Insert logo group 1 with images 4 and 5 after image 3 (img_idx == 2)
                        if img_idx == 2:
                            # Get images 4 and 5 from current color's images
                            image_4_path = color_images[3] if len(color_images) > 3 else None
                            image_5_path = color_images[4] if len(color_images) > 4 else None

                            image_4_base64 = self.image_to_base64(image_4_path) if image_4_path else None
                            image_5_base64 = self.image_to_base64(image_5_path) if image_5_path else None

                            # Add current image (3rd)
                            gallery_img_count += 1
                            gallery_image_base64 = self.image_to_base64(image_path)
                            frame_class = ' image-frame' if editable else ''
                            data_id_attr = f' data-id="gallery_color{color_idx+1}_{gallery_img_count}"' if editable else ''
                            img_class = ' editable-image' if editable else ''

                            gallery_html += f'''
                        <div class="gallery-image-wrapper{frame_class}"{data_id_attr}>
                            <img src="{gallery_image_base64}" alt="{color.get('name', '')} Gallery {gallery_img_count}" class="gallery-image{img_class}">
                        </div>
                        '''

                            # Add logo group with images 4 and 5
                            if image_4_base64 and image_5_base64:
                                frame_class = ' image-frame' if editable else ''
                                img_class = ' editable-image' if editable else ''
                                data_id_4 = f' data-id="logoGroup_color{color_idx+1}_1_1"' if editable else ''
                                data_id_5 = f' data-id="logoGroup_color{color_idx+1}_1_2"' if editable else ''

                                gallery_html += f'''
                        <div class="gallery-logo-group-1">
                            <div class="logo-group-image-frame{frame_class}"{data_id_4}>
                                <img src="{image_4_base64}" alt="Gallery 4" class="gallery-image-4{img_class}">
                            </div>
                            <div class="logo-group-image-frame{frame_class}"{data_id_5}>
                                <img src="{image_5_base64}" alt="Gallery 5" class="gallery-image-5{img_class}">
                            </div>
                            <img src="{logo_black_base64}" alt="DANA&PETA" class="gallery-logo-right">
                            <img src="{logo_black_base64}" alt="DANA&PETA" class="gallery-logo-left">
                        </div>
                        '''
                            continue

                        # Skip images 4 and 5 (img_idx 3, 4 - already in logo group 1)
                        if img_idx in [3, 4]:
                            continue

                        # Skip images 7 and 8 (img_idx 6, 7 - already in logo group 2)
                        if img_idx in [6, 7]:
                            continue

                        # Add normal image
                        gallery_img_count += 1
                        gallery_image_base64 = self.image_to_base64(image_path)
                        frame_class = ' image-frame' if editable else ''
                        data_id_attr = f' data-id="gallery_color{color_idx+1}_{gallery_img_count}"' if editable else ''
                        img_class = ' editable-image' if editable else ''

                        gallery_html += f'''
                        <div class="gallery-image-wrapper{frame_class}"{data_id_attr}>
                            <img src="{gallery_image_base64}" alt="{color.get('name', '')} Gallery {gallery_img_count}" class="gallery-image{img_class}">
                        </div>
                        '''

                        # Insert logo group 2 with images 7 and 8 after 6th image (img_idx == 5)
                        if img_idx == 5:
                            # Get images 7 and 8 from current color's images
                            image_7_path = color_images[6] if len(color_images) > 6 else None
                            image_8_path = color_images[7] if len(color_images) > 7 else None

                            image_7_base64 = self.image_to_base64(image_7_path) if image_7_path else None
                            image_8_base64 = self.image_to_base64(image_8_path) if image_8_path else None

                            # Add logo group with images 7 and 8
                            if image_7_base64 and image_8_base64:
                                frame_class = ' image-frame' if editable else ''
                                img_class = ' editable-image' if editable else ''
                                data_id_7 = f' data-id="logoGroup_color{color_idx+1}_2_1"' if editable else ''
                                data_id_8 = f' data-id="logoGroup_color{color_idx+1}_2_2"' if editable else ''

                                gallery_html += f'''
                        <div class="gallery-logo-group-2">
                            <div class="logo-group-image-frame{frame_class}"{data_id_7}>
                                <img src="{image_7_base64}" alt="Gallery 7" class="gallery-image-7{img_class}">
                            </div>
                            <div class="logo-group-image-frame{frame_class}"{data_id_8}>
                                <img src="{image_8_base64}" alt="Gallery 8" class="gallery-image-8{img_class}">
                            </div>
                            <img src="{logo_black_base64}" alt="DANA&PETA" class="gallery-logo-horizontal">
                        </div>
                        '''
        else:
            # Fallback: check for old gallery array
            gallery_images = product.get("gallery", [])
            for idx, image_path in enumerate(gallery_images):
                gallery_image_base64 = self.image_to_base64(image_path)
                gallery_html += f'''
                <img src="{gallery_image_base64}" alt="Gallery {idx + 1}" class="gallery-image">
                '''

        # Build product shots HTML (with color labels)
        product_shots_html = ""
        product_shots = product.get("productShots", [])
        colors = product.get("colors", [])

        if product_shots and colors:
            # Divide product shots among colors
            shots_per_color = len(product_shots) // len(colors)
            remainder = len(product_shots) % len(colors)

            start_idx = 0
            shot_count = 0
            for color_idx, color in enumerate(colors):
                # Calculate how many shots for this color
                num_shots = shots_per_color + (1 if color_idx < remainder else 0)
                end_idx = start_idx + num_shots

                # Add shots for this color with label
                for idx in range(start_idx, end_idx):
                    if idx < len(product_shots):
                        shot_count += 1
                        shot_base64 = self.image_to_base64(product_shots[idx])
                        frame_class = ' image-frame' if editable else ''
                        data_id_attr = f' data-id="productShot{shot_count}"' if editable else ''
                        img_class = ' editable-image' if editable else ''

                        product_shots_html += f'''
                        <div class="product-shot-wrapper">
                            <div class="product-shot-image-frame{frame_class}"{data_id_attr}>
                                <img src="{shot_base64}" alt="{color.get('name', '')} Product shot {shot_count}" class="product-shot-image{img_class}">
                            </div>
                            <div class="product-shot-color-label{editable_class}"{contenteditable_attr}>{color.get('name', '')}</div>
                        </div>
                        '''

                start_idx = end_idx
        else:
            # Fallback: no color labels
            for idx, shot_path in enumerate(product_shots):
                shot_base64 = self.image_to_base64(shot_path)
                frame_class = ' image-frame' if editable else ''
                data_id_attr = f' data-id="productShot{idx + 1}"' if editable else ''
                img_class = ' editable-image' if editable else ''

                product_shots_html += f'''
                <div class="product-shot-wrapper">
                    <div class="product-shot-image-frame{frame_class}"{data_id_attr}>
                        <img src="{shot_base64}" alt="Product shot {idx + 1}" class="product-shot-image{img_class}">
                    </div>
                </div>
                '''

        # Build fabric info HTML
        fabric_info = product.get("fabricInfo", {})
        fabric_image_path = fabric_info.get("image")
        fabric_image_base64 = self.image_to_base64(fabric_image_path) if fabric_image_path else None
        fabric_properties = fabric_info.get("properties", {})

        # Build fabric properties 4-column grid (Figma node 53-101)
        # Grid structure: 5 rows × 4 columns
        # Each row: [Property Label] [Option 1] [Option 2] [Option 3]
        # Row 1: 비침 | 없음 | 약간 비침 | 비침
        # Row 2: 신축성 | 없음 | 약간 있음 | 좋음
        # Row 3: 안감 | 없음 | 안감 있음 | 기모안감
        # Row 4: 두께감 | 얇음 | 적당함 | 두꺼움
        # Row 5: 계절감 | 봄/가을 | 여름 | 겨울

        # Get fabric property values
        transparency_value = fabric_properties.get('transparency', '')
        stretch_value = fabric_properties.get('stretch', '')
        lining_value = fabric_properties.get('lining', '')
        thickness_value = fabric_properties.get('thickness', '')
        season_value = fabric_properties.get('season', '')

        # Define property rows (property name + options)
        property_rows = [
            {
                'label': '비침',
                'options': ['없음', '약간 비침', '비침'],
                'value': transparency_value
            },
            {
                'label': '신축성',
                'options': ['없음', '약간 있음', '좋음'],
                'value': stretch_value
            },
            {
                'label': '안감',
                'options': ['없음', '안감 있음', '기모안감'],
                'value': lining_value
            },
            {
                'label': '두께감',
                'options': ['얇음', '적당함', '두꺼움'],
                'value': thickness_value
            },
            {
                'label': '계절감',
                'options': ['봄/가을', '여름', '겨울'],
                'value': season_value
            }
        ]

        # Build unified 4-column grid HTML
        fabric_properties_html = '<div class="fabric-properties-grid">'

        for row in property_rows:
            # First column: property label (header-style)
            fabric_properties_html += f'<div class="fabric-prop-header">{row["label"]}</div>'

            # Remaining columns: options (max 3 options per property)
            for i in range(3):
                if i < len(row['options']):
                    option = row['options'][i]
                    selected_class = ' selected' if option == row['value'] or option in row['value'] else ''
                    fabric_properties_html += f'<div class="fabric-prop-cell{selected_class}{editable_class}"{contenteditable_attr}>{option}</div>'
                else:
                    fabric_properties_html += '<div class="fabric-prop-cell fabric-prop-cell-empty"></div>'

        fabric_properties_html += '</div>'

        # Build product info HTML (Figma node 1-91: horizontal layout with image + 2-column table)
        product_info_data = product.get("productInfo", {})

        # Load all size images for editable mode
        size_images_data = {}
        default_size_image = product.get("sizeImage", "상의")

        if editable:
            # Load all size images from size_images folder
            size_images_dir = Path(__file__).parent.parent / "size_images"
            if size_images_dir.exists():
                for size_image_file in size_images_dir.glob("*.png"):
                    image_name = size_image_file.stem  # filename without extension
                    image_base64 = self.image_to_base64(str(size_image_file))
                    if image_base64:
                        size_images_data[image_name] = image_base64

        # Get size image (same as used in size table section)
        product_info_image_html = ""
        size_image_value = product.get("sizeImage", "")
        if size_image_value and size_image_value.strip():
            size_image_filename = f"{size_image_value.strip()}.png"
            size_image_path = Path(__file__).parent.parent / "size_images" / size_image_filename
            if size_image_path.exists():
                product_info_image_base64 = self.image_to_base64(str(size_image_path))
                if product_info_image_base64:
                    img_id = ' id="product-info-image"' if editable else ''
                    product_info_image_html = f'<img{img_id} src="{product_info_image_base64}" alt="Product info illustration" class="product-info-image">'

        # Build 2-column table rows
        product_info_rows = ""

        # 1. 제품명 (Product Name)
        product_name = product_info_data.get("productName", product.get("title", ""))
        if product_name:
            product_info_rows += f'''
            <tr>
                <td class="product-info-label{editable_class}"{contenteditable_attr}>제품명</td>
                <td class="product-info-value{editable_class}"{contenteditable_attr}>{product_name}</td>
            </tr>'''

        # 2. 컬러명 (Color Names)
        color_name = product_info_data.get("colorName", "")
        if not color_name:
            colors = product.get("colors", [])
            if colors:
                color_name = ", ".join([c.get("name", "") for c in colors if c.get("name")])
        if color_name:
            product_info_rows += f'''
            <tr>
                <td class="product-info-label{editable_class}"{contenteditable_attr}>컬러</td>
                <td class="product-info-value{editable_class}"{contenteditable_attr}>{color_name}</td>
            </tr>'''

        # 3. 사이즈 (Sizes)
        size_name = product_info_data.get("sizeName", "")
        if not size_name:
            size_info = product.get("sizeInfo", {})
            all_sizes = []
            all_sizes.extend(size_info.get("topSizes", []))
            all_sizes.extend(size_info.get("bottomSizes", []))
            if all_sizes:
                size_name = ", ".join([s.get("name", "") for s in all_sizes if s.get("name")])
        if size_name:
            product_info_rows += f'''
            <tr>
                <td class="product-info-label{editable_class}"{contenteditable_attr}>사이즈</td>
                <td class="product-info-value{editable_class}"{contenteditable_attr}>{size_name}</td>
            </tr>'''

        # 4. 패브릭 (Fabric Composition)
        fabric = product_info_data.get("fabric", "")
        if not fabric:
            fabric_info_dict = product.get("fabricInfo", {})
            fabric = fabric_info_dict.get("composition", "")
        if fabric:
            product_info_rows += f'''
            <tr>
                <td class="product-info-label{editable_class}"{contenteditable_attr}>소재</td>
                <td class="product-info-value{editable_class}"{contenteditable_attr}>{fabric}</td>
            </tr>'''

        # 5. 세탁법 (Washing Info)
        washing_info = product_info_data.get("washingInfo", "")
        if washing_info:
            product_info_rows += f'''
            <tr>
                <td class="product-info-label{editable_class}"{contenteditable_attr}>세탁방법</td>
                <td class="product-info-value{editable_class}"{contenteditable_attr}>{washing_info}</td>
            </tr>'''

        # 6. 생산지 (Origin)
        origin = product_info_data.get("origin", "")
        if origin:
            product_info_rows += f'''
            <tr>
                <td class="product-info-label{editable_class}"{contenteditable_attr}>생산지</td>
                <td class="product-info-value{editable_class}"{contenteditable_attr}>{origin}</td>
            </tr>'''

        # Assemble horizontal layout HTML
        product_info_html = f'''
        <div class="product-info-horizontal">
            <div class="product-info-image-container">
                {product_info_image_html}
            </div>
            <table class="product-info-table">
                {product_info_rows}
            </table>
        </div>
        '''

        # Build size table HTML with size image
        size_info = product.get("sizeInfo", {})
        size_table_html = ""

        # Get size image based on sizeImage field value
        size_image_html = ""
        size_image_value = product.get("sizeImage", "")
        if size_image_value and size_image_value.strip():
            # Map size image value to PNG filename
            size_image_filename = f"{size_image_value.strip()}.png"
            size_image_path = Path(__file__).parent.parent / "size_images" / size_image_filename

            if size_image_path.exists():
                size_image_base64 = self.image_to_base64(str(size_image_path))
                if size_image_base64:
                    size_image_html = f'''
                    <div style="max-width: 800px; margin: 40px auto; text-align: center;">
                        <img src="{size_image_base64}" alt="Size illustration" style="width: 100%; height: auto;">
                    </div>
                    '''
            else:
                logger.warning(f"⚠️  Size image not found: {size_image_path}")

        # Check for topSizes or bottomSizes (unified template format)
        top_sizes = size_info.get("topSizes", [])
        bottom_sizes = size_info.get("bottomSizes", [])

        if top_sizes or bottom_sizes:
            # Combine sizes for display
            all_sizes = []
            if top_sizes:
                all_sizes.extend(top_sizes)
            if bottom_sizes:
                all_sizes.extend(bottom_sizes)

            sizes = all_sizes
        else:
            # Fallback: check for old "sizes" array
            sizes = size_info.get("sizes", [])

        if sizes:
            # Determine which columns to display based on available data
            has_shoulder = any(s.get("shoulder") for s in sizes)
            has_chest = any(s.get("chest") for s in sizes)
            has_waist = any(s.get("waist") for s in sizes)
            has_hip = any(s.get("hip") for s in sizes)
            has_thigh = any(s.get("thigh") for s in sizes)
            has_hem = any(s.get("hem") for s in sizes)
            has_rise = any(s.get("rise") for s in sizes)
            has_sleeve_opening = any(s.get("sleeveOpening") for s in sizes)
            has_sleeve_length = any(s.get("sleeveLength") for s in sizes)
            has_total_length = any(s.get("totalLength") for s in sizes)

            # Build header row
            header_row = f"<th{contenteditable_attr}>호칭</th>"
            if has_shoulder:
                header_row += f"<th{contenteditable_attr}>어깨</th>"
            if has_chest:
                header_row += f"<th{contenteditable_attr}>가슴</th>"
            if has_waist:
                header_row += f"<th{contenteditable_attr}>허리</th>"
            if has_hip:
                header_row += f"<th{contenteditable_attr}>엉덩이</th>"
            if has_thigh:
                header_row += f"<th{contenteditable_attr}>허벅지</th>"
            if has_hem:
                header_row += f"<th{contenteditable_attr}>밑단</th>"
            if has_rise:
                header_row += f"<th{contenteditable_attr}>밑위</th>"
            if has_sleeve_opening:
                header_row += f"<th{contenteditable_attr}>소매통</th>"
            if has_sleeve_length:
                header_row += f"<th{contenteditable_attr}>소매기장</th>"
            if has_total_length:
                header_row += f"<th{contenteditable_attr}>총장</th>"

            # Build data rows
            data_rows = ""
            for size in sizes:
                row = f"<td{contenteditable_attr}><strong>{size.get('name', '')}</strong></td>"
                if has_shoulder:
                    row += f"<td{contenteditable_attr}>{size.get('shoulder', '')}</td>"
                if has_chest:
                    row += f"<td{contenteditable_attr}>{size.get('chest', '')}</td>"
                if has_waist:
                    row += f"<td{contenteditable_attr}>{size.get('waist', '')}</td>"
                if has_hip:
                    row += f"<td{contenteditable_attr}>{size.get('hip', '')}</td>"
                if has_thigh:
                    row += f"<td{contenteditable_attr}>{size.get('thigh', '')}</td>"
                if has_hem:
                    row += f"<td{contenteditable_attr}>{size.get('hem', '')}</td>"
                if has_rise:
                    row += f"<td{contenteditable_attr}>{size.get('rise', '')}</td>"
                if has_sleeve_opening:
                    row += f"<td{contenteditable_attr}>{size.get('sleeveOpening', '')}</td>"
                if has_sleeve_length:
                    row += f"<td{contenteditable_attr}>{size.get('sleeveLength', '')}</td>"
                if has_total_length:
                    row += f"<td{contenteditable_attr}>{size.get('totalLength', '')}</td>"
                data_rows += f"<tr>{row}</tr>"

            size_table_html = f'''
            <table class="size-table">
                <thead>
                    <tr>{header_row}</tr>
                </thead>
                <tbody>
                    {data_rows}
                </tbody>
            </table>
            '''

            # Add size comments if available
            comments = size_info.get("comments", {})
            if comments:
                size_comments_html = ""
                if comments.get("size55"):
                    size_comments_html += f'<div class="size-comment"><strong>55 사이즈:</strong> {comments["size55"]}</div>'
                if comments.get("size66"):
                    size_comments_html += f'<div class="size-comment"><strong>66 사이즈:</strong> {comments["size66"]}</div>'
                if comments.get("size77"):
                    size_comments_html += f'<div class="size-comment"><strong>77 사이즈:</strong> {comments["size77"]}</div>'

                if size_comments_html:
                    size_table_html += f'''
                    <div class="size-comments" style="max-width: 800px; margin: 30px auto; font-size: 14px; color: #666;">
                        {size_comments_html}
                    </div>
                    '''

        # Legacy format: separate top and bottom tables
        elif "top" in size_info or "bottom" in size_info:
            if "top" in size_info:
                top = size_info["top"]
                size_table_html += f'''
                <table class="size-table">
                    <thead>
                        <tr>
                            <th{contenteditable_attr}>호칭</th>
                            <th{contenteditable_attr}>어깨</th>
                            <th{contenteditable_attr}>가슴</th>
                            <th{contenteditable_attr}>밑단</th>
                            <th{contenteditable_attr}>소매기장</th>
                            <th{contenteditable_attr}>소매단</th>
                            <th{contenteditable_attr}>총장</th>
                            <th{contenteditable_attr}>암홀</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td{contenteditable_attr}>{top.get('size', '')}</td>
                            <td{contenteditable_attr}>{top.get('shoulder', '')}</td>
                            <td{contenteditable_attr}>{top.get('chest', '')}</td>
                            <td{contenteditable_attr}>{top.get('hem', '')}</td>
                            <td{contenteditable_attr}>{top.get('sleeveLength', '')}</td>
                            <td{contenteditable_attr}>{top.get('sleeveOpening', '')}</td>
                            <td{contenteditable_attr}>{top.get('totalLength', '')}</td>
                            <td{contenteditable_attr}>{top.get('armhole', '')}</td>
                        </tr>
                    </tbody>
                </table>
                '''

            if "bottom" in size_info:
                bottom = size_info["bottom"]
                size_table_html += f'''
                <table class="size-table">
                    <thead>
                        <tr>
                            <th{contenteditable_attr}>호칭</th>
                            <th{contenteditable_attr}>허리</th>
                            <th{contenteditable_attr}>엉덩이</th>
                            <th{contenteditable_attr}>밑위</th>
                            <th{contenteditable_attr}>허벅지</th>
                            <th{contenteditable_attr}>밑단</th>
                            <th{contenteditable_attr}>안기장</th>
                            <th{contenteditable_attr}>총장</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td{contenteditable_attr}>{bottom.get('size', '')}</td>
                            <td{contenteditable_attr}>{bottom.get('waist', '')}</td>
                            <td{contenteditable_attr}>{bottom.get('hip', '')}</td>
                            <td{contenteditable_attr}>{bottom.get('rise', '')}</td>
                            <td{contenteditable_attr}>{bottom.get('thigh', '')}</td>
                            <td{contenteditable_attr}>{bottom.get('hem', '')}</td>
                            <td{contenteditable_attr}>{bottom.get('inseam', '')}</td>
                            <td{contenteditable_attr}>{bottom.get('outseam', '')}</td>
                        </tr>
                    </tbody>
                </table>
                '''

        # Note: Size table add button and form moved to control panel

        # Build notices HTML
        notices = product.get("notices", {})
        shot_notices = notices.get("shotNotice", [])
        shot_notice_html = "<br>".join([n for n in shot_notices if n])

        # Editable mode scripts
        editable_scripts = ""
        if editable:
            # Generate detail points entries dynamically
            detail_points = product.get("detailPoints", [])
            detail_points_entries = ""
            for idx in range(len(detail_points)):
                point_num = idx + 1
                detail_points_entries += f'''
                    {{id: "detailPoint{point_num}", label: "디테일 포인트 {point_num}", type: "detail"}},'''

            # Generate product shot entries dynamically based on actual product shots
            product_shots = product.get("productShots", [])
            product_shot_entries = ""
            for idx in range(len(product_shots)):
                shot_num = idx + 1
                product_shot_entries += f'''
                    {{id: "productShot{shot_num}", label: "제품 샷 {shot_num}", type: "shot"}},'''

            # Generate gallery entries dynamically for all colors
            gallery_by_color = product.get("galleryByColor", {})
            colors = product.get("colors", [])
            gallery_entries = ""

            if gallery_by_color and colors:
                for color_idx, color in enumerate(colors):
                    color_key = f"color{color_idx + 1}"
                    color_images = gallery_by_color.get(color_key, [])
                    color_name = color.get('name', f'컬러{color_idx + 1}')

                    if color_images:
                        # Count and add gallery images for this color
                        gallery_img_count = 0
                        for img_idx, _ in enumerate(color_images):
                            # Images 4,5 (idx 3,4) are in logoGroup1
                            # Images 7,8 (idx 6,7) are in logoGroup2
                            if img_idx in [3, 4, 6, 7]:
                                continue  # Skip, will be added as logoGroup

                            gallery_img_count += 1
                            gallery_entries += f'''
                    {{id: "gallery_color{color_idx+1}_{gallery_img_count}", label: "{color_name} - 갤러리 {gallery_img_count}", type: "gallery"}},'''

                        # Add logo group images if they exist
                        if len(color_images) > 3:  # Has image 4 (logoGroup1_1)
                            gallery_entries += f'''
                    {{id: "logoGroup_color{color_idx+1}_1_1", label: "{color_name} - 로고 그룹 1-1 (이미지 4)", type: "gallery"}},'''
                        if len(color_images) > 4:  # Has image 5 (logoGroup1_2)
                            gallery_entries += f'''
                    {{id: "logoGroup_color{color_idx+1}_1_2", label: "{color_name} - 로고 그룹 1-2 (이미지 5)", type: "gallery"}},'''
                        if len(color_images) > 6:  # Has image 7 (logoGroup2_1)
                            gallery_entries += f'''
                    {{id: "logoGroup_color{color_idx+1}_2_1", label: "{color_name} - 로고 그룹 2-1 (이미지 7)", type: "gallery"}},'''
                        if len(color_images) > 7:  # Has image 8 (logoGroup2_2)
                            gallery_entries += f'''
                    {{id: "logoGroup_color{color_idx+1}_2_2", label: "{color_name} - 로고 그룹 2-2 (이미지 8)", type: "gallery"}},'''

            # Prepare size images data for JavaScript
            size_images_json = json.dumps(size_images_data) if size_images_data else "{}"

            editable_scripts = f'''
<script>
                // Image list for editing
                const imageList = [
                    {{id: "hero", label: "히어로 이미지 (메인 배경)", type: "hero"}},{detail_points_entries}{gallery_entries}{product_shot_entries}
                    {{id: "fabric", label: "패브릭 배경 이미지", type: "fabric"}}
                ];

                // Size images data for product info
                const sizeImagesData = {size_images_json};
                let currentSizeImage = "{default_size_image}";

                // Crop settings storage
                const cropSettings = {{
                    productCode: '{product["productCode"]}',
                    images: {{}}
                }};

                // Initialize crop settings for all images
                imageList.forEach(img => {{
                    cropSettings.images[img.id] = {{ x: 100, y: 100, scale: 100 }};
                }});

                // Current selected image
                let currentImageId = imageList.length > 0 ? imageList[0].id : null;

                // Page zoom level (30-100%, default 60%)
                let pageZoom = 60;

                // Drag state
                let isDragging = false;
                let startX, startY, startObjX, startObjY;

                // Upload button elements
                let uploadBtn;
                let fileInput;

                // Initialize
                function init() {{
                    // Populate image dropdown
                    const select = document.getElementById('image-select');
                    imageList.forEach(img => {{
                        const option = document.createElement('option');
                        option.value = img.id;
                        option.textContent = img.label;
                        select.appendChild(option);
                    }});

                    // Populate size image dropdown
                    const sizeImageSelect = document.getElementById('size-image-select');
                    if (sizeImageSelect && Object.keys(sizeImagesData).length > 0) {{
                        Object.keys(sizeImagesData).sort().forEach(imageName => {{
                            const option = document.createElement('option');
                            option.value = imageName;
                            option.textContent = imageName;
                            if (imageName === currentSizeImage) {{
                                option.selected = true;
                            }}
                            sizeImageSelect.appendChild(option);
                        }});
                    }}

                    // Load settings from localStorage
                    loadSettings();

                    // Apply initial settings
                    applyAllCropSettings();
                    applyPageZoom();  // Apply page zoom after loading settings

                    // Setup event listeners
                    setupEventListeners();

                    // Populate size illustration options
                    populateSizeIllustrationOptions();

                    // Select first image
                    if (currentImageId) {{
                        selectImage(currentImageId);
                    }}
                }}

                // Setup all event listeners
                function setupEventListeners() {{
                    // Dropdown change
                    document.getElementById('image-select').addEventListener('change', (e) => {{
                        selectImage(e.target.value);
                    }});

                    // Size image dropdown change
                    const sizeImageSelect = document.getElementById('size-image-select');
                    if (sizeImageSelect) {{
                        sizeImageSelect.addEventListener('change', (e) => {{
                            changeSizeImage(e.target.value);
                        }});
                    }}

                    // Page zoom slider
                    document.getElementById('page-zoom').addEventListener('input', (e) => {{
                        pageZoom = parseInt(e.target.value);
                        document.getElementById('page-zoom-value').textContent = pageZoom + '%';
                        applyPageZoom();
                        autoSave();
                    }});

                    // Image position/scale sliders
                    document.getElementById('position-x').addEventListener('input', (e) => {{
                        const value = parseInt(e.target.value);
                        cropSettings.images[currentImageId].x = value;
                        document.getElementById('x-value').textContent = value + '%';
                        applyCurrentCrop();
                        autoSave();
                    }});

                    document.getElementById('position-y').addEventListener('input', (e) => {{
                        const value = parseInt(e.target.value);
                        cropSettings.images[currentImageId].y = value;
                        document.getElementById('y-value').textContent = value + '%';
                        applyCurrentCrop();
                        autoSave();
                    }});

                    document.getElementById('scale').addEventListener('input', (e) => {{
                        const value = parseInt(e.target.value);
                        cropSettings.images[currentImageId].scale = value;
                        document.getElementById('scale-value').textContent = value + '%';
                        applyCurrentCrop();
                        autoSave();
                    }});

                    // Image frame interactions
                    document.querySelectorAll('.image-frame').forEach(frame => {{
                        const id = frame.getAttribute('data-id');
                        if (!id) return;

                        // Click to select
                        frame.addEventListener('click', (e) => {{
                            if (!isDragging) {{
                                selectImage(id);
                                document.getElementById('image-select').value = id;
                            }}
                        }});

                        // Drag to move
                        frame.addEventListener('mousedown', (e) => {{
                            e.preventDefault();
                            if (!cropSettings.images[id]) return;

                            selectImage(id);
                            document.getElementById('image-select').value = id;

                            isDragging = true;
                            startX = e.clientX;
                            startY = e.clientY;
                            startObjX = cropSettings.images[id].x;
                            startObjY = cropSettings.images[id].y;
                            frame.classList.add('dragging');
                        }});

                        // Wheel to zoom
                        frame.addEventListener('wheel', (e) => {{
                            e.preventDefault();
                            if (!cropSettings.images[id]) return;

                            selectImage(id);
                            document.getElementById('image-select').value = id;

                            const delta = e.deltaY > 0 ? -5 : 5;
                            const newScale = Math.max(100, Math.min(500,
                                cropSettings.images[id].scale + delta
                            ));

                            cropSettings.images[id].scale = newScale;
                            applyCurrentCrop();
                            updateSliders();
                            autoSave();
                        }}, {{ passive: false }});
                    }});

                    // Global mouse move/up for drag
                    document.addEventListener('mousemove', (e) => {{
                        if (!isDragging) return;

                        const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
                        if (!frame || !cropSettings.images[currentImageId]) return;

                        const dx = (e.clientX - startX) / frame.offsetWidth * 100;
                        const dy = (e.clientY - startY) / frame.offsetHeight * 100;

                        const scale = cropSettings.images[currentImageId].scale / 100;
                        const maxRange = (scale - 1) * 50;
                        const minX = -maxRange;
                        const maxX = 100 + maxRange;
                        const minY = -maxRange;
                        const maxY = 100 + maxRange;

                        const newX = Math.max(minX, Math.min(maxX, startObjX + dx));
                        const newY = Math.max(minY, Math.min(maxY, startObjY + dy));

                        cropSettings.images[currentImageId].x = newX;
                        cropSettings.images[currentImageId].y = newY;

                        applyCurrentCrop();
                        updateSliders();
                    }});

                    document.addEventListener('mouseup', () => {{
                        if (isDragging) {{
                            isDragging = false;
                            document.querySelectorAll('.image-frame').forEach(f => {{
                                f.classList.remove('dragging');
                            }});
                            autoSave();
                        }}
                    }});

                    // Keyboard shortcuts
                    document.addEventListener('keydown', (e) => {{
                        if (!currentImageId || !cropSettings.images[currentImageId]) return;

                        const step = e.shiftKey ? 10 : 1;
                        let changed = false;

                        const scale = cropSettings.images[currentImageId].scale / 100;
                        const maxRange = (scale - 1) * 50;
                        const minX = -maxRange;
                        const maxX = 100 + maxRange;
                        const minY = -maxRange;
                        const maxY = 100 + maxRange;

                        switch(e.key) {{
                            case 'ArrowLeft':
                                e.preventDefault();
                                cropSettings.images[currentImageId].x = Math.max(minX,
                                    cropSettings.images[currentImageId].x - step
                                );
                                changed = true;
                                break;
                            case 'ArrowRight':
                                e.preventDefault();
                                cropSettings.images[currentImageId].x = Math.min(maxX,
                                    cropSettings.images[currentImageId].x + step
                                );
                                changed = true;
                                break;
                            case 'ArrowUp':
                                e.preventDefault();
                                cropSettings.images[currentImageId].y = Math.max(minY,
                                    cropSettings.images[currentImageId].y - step
                                );
                                changed = true;
                                break;
                            case 'ArrowDown':
                                e.preventDefault();
                                cropSettings.images[currentImageId].y = Math.min(maxY,
                                    cropSettings.images[currentImageId].y + step
                                );
                                changed = true;
                                break;
                            case '+':
                            case '=':
                                e.preventDefault();
                                cropSettings.images[currentImageId].scale = Math.min(500,
                                    cropSettings.images[currentImageId].scale + 5
                                );
                                changed = true;
                                break;
                            case '-':
                            case '_':
                                e.preventDefault();
                                cropSettings.images[currentImageId].scale = Math.max(100,
                                    cropSettings.images[currentImageId].scale - 5
                                );
                                changed = true;
                                break;
                        }}

                        if (changed) {{
                            applyCurrentCrop();
                            updateSliders();
                            autoSave();
                        }}
                    }});

                    // Upload button handler
                    uploadBtn = document.getElementById('upload-trigger-btn');
                    fileInput = document.getElementById('file-input-global');

                    uploadBtn.addEventListener('click', () => {{
                        if (!currentImageId) {{
                            alert('⚠️ 먼저 교체할 이미지를 선택해주세요.');
                            return;
                        }}
                        fileInput.click();
                    }});

                    fileInput.addEventListener('change', (e) => {{
                        const file = e.target.files[0];
                        if (!file || !currentImageId) return;

                        console.log('📤 Uploading image for:', currentImageId);

                        const reader = new FileReader();
                        reader.onload = (event) => {{
                            const base64 = event.target.result;

                            const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
                            if (frame) {{
                                const img = frame.querySelector('.editable-image');
                                if (img) {{
                                    img.src = base64;
                                    console.log('✅ Image replaced:', currentImageId);
                                    autoSave();
                                }}
                            }}

                            e.target.value = '';
                        }};
                        reader.readAsDataURL(file);
                    }});

                    // Color picker handlers
                    document.querySelectorAll('.hex-picker').forEach(picker => {{
                        const updateColor = (e) => {{
                            const newHex = e.target.value;
                            const colorIndex = parseInt(e.target.getAttribute('data-color-index'));

                            const swatch = e.target.closest('.color-swatch');
                            if (swatch) {{
                                swatch.style.backgroundColor = newHex;
                            }}

                            console.log(`Color ${{colorIndex}} updated to ${{newHex}}`);
                        }};

                        picker.addEventListener('change', updateColor);
                        picker.addEventListener('input', updateColor);
                    }});

                    // Note: Size table form event handlers moved to inline onclick
                }}

                // Select image
                function selectImage(imageId) {{
                    currentImageId = imageId;

                    document.querySelectorAll('.image-frame').forEach(frame => {{
                        frame.classList.remove('selected');
                    }});

                    const selectedFrame = document.querySelector(`[data-id="${{imageId}}"]`);
                    if (selectedFrame) {{
                        selectedFrame.classList.add('selected');
                        selectedFrame.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    }}

                    updateSliders();
                }}

                // Load settings from localStorage
                function loadSettings() {{
                    const saved = localStorage.getItem('cropSettings_{product["productCode"]}_dana');
                    if (saved) {{
                        try {{
                            const settings = JSON.parse(saved);

                            // Load page zoom if available
                            if (settings.pageZoom && typeof settings.pageZoom === 'number' &&
                                settings.pageZoom >= 30 && settings.pageZoom <= 100) {{
                                pageZoom = settings.pageZoom;
                                const zoomSlider = document.getElementById('page-zoom');
                                const zoomValue = document.getElementById('page-zoom-value');
                                if (zoomSlider) zoomSlider.value = pageZoom;
                                if (zoomValue) zoomValue.textContent = pageZoom + '%';
                            }}

                            // Load size image selection if available
                            if (settings.sizeImage && typeof settings.sizeImage === 'string' &&
                                sizeImagesData[settings.sizeImage]) {{
                                currentSizeImage = settings.sizeImage;
                                const sizeImageSelect = document.getElementById('size-image-select');
                                if (sizeImageSelect) sizeImageSelect.value = currentSizeImage;

                                // Apply the saved size image
                                const productInfoImage = document.getElementById('product-info-image');
                                if (productInfoImage) {{
                                    productInfoImage.src = sizeImagesData[currentSizeImage];
                                }}
                            }}

                            // Validate and load only valid settings for existing images
                            if (settings.images && typeof settings.images === 'object') {{
                                imageList.forEach(img => {{
                                    // Skip loading settings for hero, shot, fabric, and first gallery images
                                    // These images always use default values (x:100, y:100, scale:100)
                                    const isFirstGalleryImage = img.type === 'gallery' && img.id.endsWith('_1');
                                    if (img.type === 'hero' || img.type === 'shot' || img.type === 'fabric' || isFirstGalleryImage) {{
                                        return;  // Keep default values
                                    }}

                                    const savedImgSettings = settings.images[img.id];
                                    if (savedImgSettings &&
                                        typeof savedImgSettings.x === 'number' &&
                                        typeof savedImgSettings.y === 'number' &&
                                        typeof savedImgSettings.scale === 'number' &&
                                        savedImgSettings.scale >= 100 && savedImgSettings.scale <= 500) {{
                                        // Valid saved settings found, use them
                                        cropSettings.images[img.id] = {{
                                            x: savedImgSettings.x,
                                            y: savedImgSettings.y,
                                            scale: savedImgSettings.scale
                                        }};
                                    }}
                                    // If invalid or missing, keep the default (100, 100, 100)
                                }});
                            }}
                        }} catch (e) {{
                            console.warn('Failed to load crop settings from localStorage:', e);
                            // Keep default settings on error
                        }}
                    }}
                }}

                function computeTransform(frame, settings) {{
                    if (!frame || !settings) {{
                        return {{ translateX: 0, translateY: 0, scale: 1 }};
                    }}

                    const rect = frame.getBoundingClientRect();
                    const frameWidth = frame.offsetWidth || rect.width || 0;
                    const frameHeight = frame.offsetHeight || rect.height || 0;

                    const scale = (typeof settings.scale === 'number' ? settings.scale : 100) / 100;
                    const offsetXPercent = (typeof settings.x === 'number' ? settings.x : 100) - 100;
                    const offsetYPercent = (typeof settings.y === 'number' ? settings.y : 100) - 100;

                    const translateX = frameWidth * (offsetXPercent / 100);
                    const translateY = frameHeight * (offsetYPercent / 100);

                    return {{ translateX, translateY, scale }};
                }}

                function applyTransform(frame, img, settings) {{
                    const {{ translateX, translateY, scale }} = computeTransform(frame, settings);
                    img.style.transform = `translate(${{translateX}}px, ${{translateY}}px) scale(${{scale}})`;
                }}

                const imageCache = new Map();

                async function loadImage(src) {{
                    if (!src) {{
                        throw new Error('Invalid image source');
                    }}

                    if (imageCache.has(src)) {{
                        const cached = imageCache.get(src);
                        if (cached instanceof Promise) {{
                            return await cached;
                        }}
                        return cached;
                    }}

                    const loader = new Promise((resolve, reject) => {{
                        const tempImg = new Image();
                        tempImg.onload = () => resolve(tempImg);
                        tempImg.onerror = (err) => reject(err);
                        tempImg.src = src;
                    }});

                    imageCache.set(src, loader);
                    try {{
                        const loaded = await loader;
                        imageCache.set(src, loaded);
                        return loaded;
                    }} catch (error) {{
                        imageCache.delete(src);
                        throw error;
                    }}
                }}

                async function generateFlattenedImageData(frame, img, settings) {{
                    const frameRect = frame.getBoundingClientRect();
                    const frameWidth = Math.max(1, Math.round(frame.offsetWidth || frameRect.width || 0));
                    const frameHeight = Math.max(1, Math.round(frame.offsetHeight || frameRect.height || 0));

                    if (frameWidth === 0 || frameHeight === 0) {{
                        throw new Error('Frame has zero size');
                    }}

                    const imageSource = img.currentSrc || img.src;
                    const baseImage = await loadImage(imageSource);
                    const naturalWidth = baseImage.naturalWidth || baseImage.width;
                    const naturalHeight = baseImage.naturalHeight || baseImage.height;

                    if (!naturalWidth || !naturalHeight) {{
                        throw new Error('Unable to determine image dimensions');
                    }}

                    const baseScale = Math.max(frameWidth / naturalWidth, frameHeight / naturalHeight);
                    const userScale = (typeof settings.scale === 'number' ? settings.scale : 100) / 100;
                    const totalScale = baseScale * userScale;

                    const displayWidth = naturalWidth * totalScale;
                    const displayHeight = naturalHeight * totalScale;

                    const offsetXPercent = (typeof settings.x === 'number' ? settings.x : 100) - 100;
                    const offsetYPercent = (typeof settings.y === 'number' ? settings.y : 100) - 100;

                    const translateX = frameWidth * (offsetXPercent / 100);
                    const translateY = frameHeight * (offsetYPercent / 100);

                    const drawX = (frameWidth - displayWidth) / 2 + translateX;
                    const drawY = (frameHeight - displayHeight) / 2 + translateY;

                    const canvas = document.createElement('canvas');
                    canvas.width = frameWidth;
                    canvas.height = frameHeight;

                    const ctx = canvas.getContext('2d', {{ willReadFrequently: true }});
                    if (!ctx) {{
                        throw new Error('Failed to acquire canvas context');
                    }}

                    ctx.clearRect(0, 0, frameWidth, frameHeight);
                    ctx.drawImage(baseImage, drawX, drawY, displayWidth, displayHeight);

                    return canvas.toDataURL('image/png');
                }}

                async function createFlattenedImageMap() {{
                    const flattenedMap = {{}};
                    const cacheKeyMap = new Map();

                    for (const frame of document.querySelectorAll('.image-frame')) {{
                        const id = frame.getAttribute('data-id');
                        if (!id) continue;
                        const img = frame.querySelector('.editable-image');
                        if (!img) continue;

                        const settings = cropSettings.images[id] || {{ x: 100, y: 100, scale: 100 }};
                        const frameWidth = Math.round(frame.offsetWidth);
                        const frameHeight = Math.round(frame.offsetHeight);
                        const cacheKey = `${{img.currentSrc || img.src}}|${{settings.x}}|${{settings.y}}|${{settings.scale}}|${{frameWidth}}|${{frameHeight}}`;

                        try {{
                            if (cacheKey && cacheKeyMap.has(cacheKey)) {{
                                flattenedMap[id] = cacheKeyMap.get(cacheKey);
                                continue;
                            }}

                            const flattenedData = await generateFlattenedImageData(frame, img, settings);
                            flattenedMap[id] = flattenedData;
                            if (cacheKey) {{
                                cacheKeyMap.set(cacheKey, flattenedData);
                            }}
                        }} catch (error) {{
                            console.warn('Flatten image failed', id, error);
                        }}
                    }}

                    return flattenedMap;
                }}

                // Apply crop settings to all images
                function applyAllCropSettings() {{
                    document.querySelectorAll('.image-frame').forEach(frame => {{
                        const id = frame.getAttribute('data-id');
                        const img = frame.querySelector('.editable-image');
                        const settings = cropSettings.images[id];

                        if (settings && img) {{
                            applyTransform(frame, img, settings);
                        }}
                    }});
                }}

                // Apply page zoom to container
                function applyPageZoom() {{
                    const container = document.querySelector('.container');
                    if (container) {{
                        const scale = pageZoom / 100;
                        container.style.transform = `scale(${{scale}})`;

                        // Adjust container height to account for scale transform
                        // This prevents excessive whitespace below scaled content
                        const naturalHeight = container.scrollHeight;
                        container.style.height = `${{naturalHeight * scale}}px`;
                    }}
                }}

                // Apply crop to current image
                function applyCurrentCrop() {{
                    const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
                    if (!frame) return;

                    const img = frame.querySelector('.editable-image');
                    const settings = cropSettings.images[currentImageId];
                    if (img && settings) {{
                        applyTransform(frame, img, settings);
                    }}
                }}

                // Update sliders from current image settings
                function updateSliders() {{
                    const settings = cropSettings.images[currentImageId];
                    if (settings) {{
                        document.getElementById('position-x').value = settings.x;
                        document.getElementById('position-y').value = settings.y;
                        document.getElementById('scale').value = settings.scale;
                        document.getElementById('x-value').textContent = settings.x + '%';
                        document.getElementById('y-value').textContent = settings.y + '%';
                        document.getElementById('scale-value').textContent = settings.scale + '%';
                    }}
                }}

                // Change size image in product info
                function changeSizeImage(imageName) {{
                    if (!sizeImagesData[imageName]) {{
                        console.error('Size image not found:', imageName);
                        return;
                    }}

                    const productInfoImage = document.getElementById('product-info-image');
                    if (productInfoImage) {{
                        productInfoImage.src = sizeImagesData[imageName];
                        currentSizeImage = imageName;
                        autoSave();
                    }}
                }}

                // Populate size illustration dropdown
                function populateSizeIllustrationOptions() {{
                    const sizeIllustrationSelect = document.getElementById('size-illustration');
                    if (!sizeIllustrationSelect) return;

                    // Add size images to dropdown
                    if (sizeImagesData && Object.keys(sizeImagesData).length > 0) {{
                        Object.keys(sizeImagesData).sort().forEach(imageName => {{
                            const option = document.createElement('option');
                            option.value = imageName;
                            option.textContent = imageName;
                            sizeIllustrationSelect.appendChild(option);
                        }});
                    }}
                }}

                // Toggle size table form
                function toggleSizeTableForm() {{
                    const form = document.getElementById('size-table-form');
                    if (form) {{
                        form.style.display = form.style.display === 'none' ? 'block' : 'none';
                    }}
                }}

                // Create new size table
                function createNewSizeTable() {{
                    const tableType = document.getElementById('table-type').value;
                    const rowCount = parseInt(document.getElementById('row-count').value);
                    const illustration = document.getElementById('size-illustration').value;

                    // Validate inputs
                    if (rowCount < 1 || rowCount > 10) {{
                        alert('⚠️ 행 수는 1-10 사이여야 합니다.');
                        return;
                    }}

                    // Create illustration HTML if selected
                    let illustrationHTML = '';
                    if (illustration && sizeImagesData[illustration]) {{
                        illustrationHTML = `
                        <div style="max-width: 300px; margin: 40px auto; text-align: left;">
                            <img src="${{sizeImagesData[illustration]}}" alt="Size illustration" style="width: 100%; height: auto;">
                        </div>
                        `;
                    }}

                    // Define table headers based on type
                    let headerHTML = '';
                    if (tableType === 'top') {{
                        headerHTML = `
                        <tr>
                            <th contenteditable="true">호칭</th>
                            <th contenteditable="true">어깨</th>
                            <th contenteditable="true">가슴</th>
                            <th contenteditable="true">밑단</th>
                            <th contenteditable="true">소매기장</th>
                            <th contenteditable="true">소매단</th>
                            <th contenteditable="true">총장</th>
                            <th contenteditable="true">암홀</th>
                        </tr>
                        `;
                    }} else {{ // bottom
                        headerHTML = `
                        <tr>
                            <th contenteditable="true">호칭</th>
                            <th contenteditable="true">허리</th>
                            <th contenteditable="true">엉덩이</th>
                            <th contenteditable="true">밑위</th>
                            <th contenteditable="true">허벅지</th>
                            <th contenteditable="true">밑단</th>
                            <th contenteditable="true">안기장</th>
                            <th contenteditable="true">총장</th>
                        </tr>
                        `;
                    }}

                    // Create table rows (all empty cells)
                    let rowsHTML = '';
                    const colCount = tableType === 'top' ? 8 : 8; // Both have 8 columns
                    for (let i = 0; i < rowCount; i++) {{
                        rowsHTML += '<tr>';
                        for (let j = 0; j < colCount; j++) {{
                            rowsHTML += '<td contenteditable="true" class="editable"></td>';
                        }}
                        rowsHTML += '</tr>';
                    }}

                    // Create full table HTML
                    const tableHTML = illustrationHTML + `
                    <table class="size-table">
                        <thead>
                            ${{headerHTML}}
                        </thead>
                        <tbody>
                            ${{rowsHTML}}
                        </tbody>
                    </table>
                    `;

                    // Find the size tables container and append new table
                    const container = document.getElementById('size-tables-container');
                    const newTableDiv = document.createElement('div');
                    newTableDiv.innerHTML = tableHTML;
                    container.appendChild(newTableDiv);

                    // Close form
                    toggleSizeTableForm();

                    // Reset form
                    document.getElementById('row-count').value = 1;
                    document.getElementById('size-illustration').value = '';

                    alert('✅ 사이즈표가 추가되었습니다.');
                }}

                // Auto-save to localStorage
                function autoSave() {{
                    // Save crop settings, page zoom, and size image selection
                    cropSettings.pageZoom = pageZoom;
                    cropSettings.sizeImage = currentSizeImage;
                    localStorage.setItem('cropSettings_{product["productCode"]}_dana', JSON.stringify(cropSettings));
                }}

                // Reset current image
                function resetCurrentImage() {{
                    cropSettings.images[currentImageId] = {{ x: 100, y: 100, scale: 100 }};
                    updateSliders();
                    applyCurrentCrop();
                    autoSave();
                    alert('✅ 현재 이미지가 리셋되었습니다.');
                }}

                // Reset all images
                function resetAllImages() {{
                    if (!confirm('⚠️ 모든 이미지 설정을 리셋하시겠습니까?')) return;

                    imageList.forEach(img => {{
                        cropSettings.images[img.id] = {{ x: 100, y: 100, scale: 100 }};
                    }});
                    updateSliders();
                    applyAllCropSettings();
                    autoSave();
                    alert('✅ 모든 이미지가 리셋되었습니다.');
                }}

                // Export HTML
                async function exportHTML() {{
                    applyAllCropSettings();
                    const flattenedImageMap = await createFlattenedImageMap();
                    const transformMap = {{}};
                    document.querySelectorAll('.image-frame').forEach(frame => {{
                        const id = frame.getAttribute('data-id');
                        const img = frame.querySelector('.editable-image');
                        if (!id || !img) return;
                        const computedStyle = window.getComputedStyle(img);
                        const transform = computedStyle.transform;
                        const origin = computedStyle.transformOrigin;
                        transformMap[id] = {{
                            transform: transform && transform !== 'none' ? transform : '',
                            origin: origin && origin !== 'none' ? origin : ''
                        }};
                    }});
                    const clone = document.documentElement.cloneNode(true);

                    // Remove control panel
                    const controlPanel = clone.querySelector('.control-panel');
                    if (controlPanel) controlPanel.remove();

                    // Remove scripts
                    const scripts = clone.querySelectorAll('script');
                    scripts.forEach(s => s.remove());

                    // Apply inline styles to all images and remove frame styling
                    clone.querySelectorAll('.image-frame').forEach(frame => {{
                        const id = frame.getAttribute('data-id');
                        const img = frame.querySelector('.editable-image');
                        const transformInfo = id ? transformMap[id] : null;
                        const flattenedSrc = id ? flattenedImageMap[id] : null;
                        if (img) {{
                            if (flattenedSrc) {{
                                img.setAttribute('src', flattenedSrc);
                                img.style.transform = 'none';
                                img.style.transformOrigin = 'center center';
                                img.style.objectFit = 'cover';
                            }} else if (transformInfo && transformInfo.transform) {{
                                img.style.transform = transformInfo.transform;
                                if (transformInfo.origin) {{
                                    img.style.transformOrigin = transformInfo.origin;
                                }} else {{
                                    img.style.removeProperty('transform-origin');
                                }}
                            }} else {{
                                img.style.removeProperty('transform');
                                img.style.removeProperty('transform-origin');
                            }}
                        }}
                        frame.style.cursor = 'default';
                        frame.classList.remove('selected');
                        frame.style.border = 'none';
                        frame.style.outline = 'none';
                    }});

                    // Remove contenteditable
                    clone.querySelectorAll('[contenteditable]').forEach(el => {{
                        el.removeAttribute('contenteditable');
                    }});

                    // Remove hex pickers
                    clone.querySelectorAll('.hex-picker').forEach(picker => picker.remove());

                    // Remove inline styles from body (especially min-height)
                    const body = clone.querySelector('body');
                    if (body) {{
                        body.removeAttribute('style');
                    }}

                    const htmlContent = '<!DOCTYPE html>\\n' + clone.outerHTML;

                    try {{
                        // Send to server
                        const response = await fetch('http://localhost:5001/save-html', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{
                                productCode: '{product["productCode"]}',
                                htmlContent: htmlContent
                            }})
                        }});

                        if (response.ok) {{
                            const result = await response.json();
                            alert(`✅ HTML 저장 완료\\n경로: ${{result.path}}`);
                        }} else {{
                            const error = await response.json();
                            alert(`❌ 서버 저장 실패: ${{error.error}}`);
                        }}
                    }} catch (error) {{
                        console.error('Export error:', error);
                        alert('❌ 서버 연결 실패. 서버가 실행 중인지 확인하세요.\\n(python3 scripts/server.py)');
                    }}
                }}

                // Export as JPG
                async function exportAsJPG() {{
                    applyAllCropSettings();
                    const flattenedImageMap = await createFlattenedImageMap();
                    const imageTransformStates = [];
                    const replacedImageStates = [];

                    document.querySelectorAll('.image-frame').forEach(frame => {{
                        const id = frame.getAttribute('data-id');
                        const img = frame.querySelector('.editable-image');
                        if (!img) return;

                        const flattenedSrc = id ? flattenedImageMap[id] : null;

                        if (flattenedSrc) {{
                            replacedImageStates.push({{
                                img,
                                src: img.src,
                                transform: img.style.transform,
                                origin: img.style.transformOrigin,
                                objectFit: img.style.objectFit
                            }});
                            img.src = flattenedSrc;
                            img.style.transform = 'none';
                            img.style.transformOrigin = 'center center';
                            img.style.objectFit = 'cover';
                        }} else {{
                            const computed = window.getComputedStyle(img);
                            imageTransformStates.push({{
                                img,
                                transform: img.style.transform,
                                origin: img.style.transformOrigin
                            }});
                            const computedTransform = computed.transform;
                            if (computedTransform && computedTransform !== 'none') {{
                                img.style.transform = computedTransform;
                            }}
                            const computedOrigin = computed.transformOrigin;
                            if (computedOrigin && computedOrigin !== 'none') {{
                                img.style.transformOrigin = computedOrigin;
                            }}
                        }}
                    }});

                    await Promise.all(replacedImageStates.map(state => {{
                        if (state.img.decode) {{
                            return state.img.decode().catch(() => undefined);
                        }}
                        return Promise.resolve();
                    }}));

                    const controlPanel = document.querySelector('.control-panel');
                    const container = document.querySelector('.container');
                    const body = document.body;

                    if (!container) {{
                        alert('❌ 컨테이너를 찾을 수 없습니다.');
                        return;
                    }}

                    // Save original styles
                    const originalTransform = container.style.transform;
                    const originalHeight = container.style.height;
                    const originalMinHeight = body.style.minHeight;

                    // Save original selection state
                    const selectedFrames = document.querySelectorAll('.image-frame.selected');
                    const originalSelectedIds = Array.from(selectedFrames).map(f => f.getAttribute('data-id'));

                    // Hide control panel
                    if (controlPanel) {{
                        controlPanel.style.display = 'none';
                    }}

                    // Declare base64Image outside try block so catch can access it
                    let base64Image;

                    try {{
                        // Reset container transform and height for capture
                        container.style.transform = 'none';
                        container.style.height = 'auto';
                        body.style.minHeight = 'auto';

                        // Remove all selection styles before capture
                        document.querySelectorAll('.image-frame').forEach(frame => {{
                            frame.classList.remove('selected');
                            frame.style.border = 'none';
                            frame.style.outline = 'none';
                            frame.style.boxShadow = 'none';
                        }});

                        // Wait for layout and styles to settle
                        await new Promise(resolve => setTimeout(resolve, 150));

                        // Capture entire container as canvas
                        const canvas = await html2canvas(container, {{
                            scale: 2,  // High resolution
                            useCORS: true,
                            backgroundColor: '#ffffff',
                            logging: false,
                            allowTaint: true,
                            windowWidth: container.scrollWidth,
                            windowHeight: container.scrollHeight,
                            width: container.scrollWidth,
                            height: container.scrollHeight
                        }});

                        // Convert canvas to base64
                        base64Image = canvas.toDataURL('image/jpeg', 0.95);

                        // Send to server
                        const response = await fetch('http://localhost:5001/save-jpg', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{
                                productCode: '{product["productCode"]}',
                                imageData: base64Image
                            }})
                        }});

                        if (response.ok) {{
                            const result = await response.json();
                            alert(`✅ JPG 저장 완료\\n경로: ${{result.path}}`);
                        }} else {{
                            // 서버 저장 실패 시 fallback으로 진행
                            throw new Error('Server save failed');
                        }}

                    }} catch (error) {{
                        console.error('Export error:', error);

                        // Fallback: Download directly in browser when server is not running
                        if (base64Image) {{
                            try {{
                                const link = document.createElement('a');
                                const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
                                link.download = `{product["productCode"]}_${{timestamp}}.jpg`;
                                link.href = base64Image;
                                link.click();

                                alert('✅ JPG 다운로드 완료\\n위치: 다운로드 폴더\\n(서버 미실행 시 브라우저 다운로드)');
                            }} catch (downloadError) {{
                                console.error('Download error:', downloadError);
                                alert('❌ 다운로드 실패: ' + downloadError.message);
                            }}
                        }} else {{
                            alert('❌ 이미지 생성 실패. 페이지를 새로고침 후 다시 시도하세요.');
                        }}
                    }} finally {{
                        imageTransformStates.forEach(state => {{
                            state.img.style.transform = state.transform;
                            state.img.style.transformOrigin = state.origin || '';
                        }});
                        replacedImageStates.forEach(state => {{
                            state.img.src = state.src;
                            state.img.style.transform = state.transform || '';
                            state.img.style.transformOrigin = state.origin || '';
                            if (state.objectFit) {{
                                state.img.style.objectFit = state.objectFit;
                            }} else {{
                                state.img.style.removeProperty('object-fit');
                            }}
                        }});

                        // Restore original styles
                        container.style.transform = originalTransform;
                        container.style.height = originalHeight;
                        body.style.minHeight = originalMinHeight;

                        // Restore selection state
                        originalSelectedIds.forEach(id => {{
                            const frame = document.querySelector(`[data-id="${{id}}"]`);
                            if (frame) {{
                                frame.classList.add('selected');
                                frame.style.border = '';
                                frame.style.outline = '';
                                frame.style.boxShadow = '';
                            }}
                        }});

                        // Restore control panel
                        if (controlPanel) {{
                            controlPanel.style.display = 'block';
                        }}
                    }}
                }}

                // Initialize on page load
                window.addEventListener('DOMContentLoaded', init);
            </script>'''

        # Control panel HTML (only for editable mode)
        control_panel_html = ""
        if editable:
            control_panel_html = '''
            <div class="control-panel" style="position: fixed; top: 20px; right: 20px; background: white; padding: 20px; border: 2px solid #333; z-index: 9999; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 300px; max-height: 90vh; overflow-y: auto;">
                <h3 style="margin: 0 0 20px 0; font-size: 18px; font-weight: bold; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px;">이미지 편집 도구</h3>

                <!-- Page Zoom Control -->
                <div style="margin-bottom: 20px; padding: 15px; background: #e7f3ff; border-radius: 6px; border: 1px solid #b3d9ff;">
                    <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">🖥️ 페이지 줌</h4>
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                            화면 표시: <span id="page-zoom-value" style="font-weight: bold; color: #0066cc;">60%</span>
                        </label>
                        <input type="range" id="page-zoom" min="30" max="100" value="60" step="5" style="width: 100%;">
                        <p style="margin: 8px 0 0 0; font-size: 11px; color: #666; line-height: 1.4;">
                            💡 실제 크기는 유지되며, 화면 표시만 조절됩니다.
                        </p>
                    </div>
                </div>

                <!-- Size Image Selector (Product Info) -->
                <div style="margin-bottom: 20px; padding: 15px; background: #e8f5e9; border-radius: 6px; border: 1px solid #81c784;">
                    <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">📐 사이즈 이미지 선택</h4>
                    <label style="display: block; margin-bottom: 5px; font-size: 12px;">프로덕트 인포 이미지:</label>
                    <select id="size-image-select" style="width: 100%; padding: 8px; font-size: 13px; border: 1px solid #66bb6a; border-radius: 4px; cursor: pointer;">
                        <!-- Options populated by JavaScript -->
                    </select>
                    <p style="margin: 8px 0 0 0; font-size: 11px; color: #2e7d32; line-height: 1.4;">
                        💡 사이즈 이미지를 변경하면 프로덕트 인포에 표시됩니다.
                    </p>
                </div>

                <!-- Image Selector -->
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; font-size: 13px; font-weight: 600;">📷 이미지 선택</label>
                    <select id="image-select" style="width: 100%; padding: 8px; font-size: 13px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer;">
                        <!-- Options populated by JavaScript -->
                    </select>
                </div>

                <!-- Position Controls -->
                <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 6px;">
                    <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">🎯 위치 조절</h4>

                    <div style="margin-bottom: 12px;">
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                            좌우 (X): <span id="x-value" style="font-weight: bold; color: #007bff;">100%</span>
                        </label>
                        <input type="range" id="position-x" min="0" max="200" value="100" step="1" style="width: 100%;">
                    </div>

                    <div style="margin-bottom: 0;">
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                            상하 (Y): <span id="y-value" style="font-weight: bold; color: #007bff;">100%</span>
                        </label>
                        <input type="range" id="position-y" min="0" max="200" value="100" step="1" style="width: 100%;">
                    </div>
                </div>

                <!-- Scale Control -->
                <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 6px;">
                    <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">🔍 확대/축소</h4>
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                            크기: <span id="scale-value" style="font-weight: bold; color: #28a745;">100%</span>
                        </label>
                        <input type="range" id="scale" min="100" max="500" value="100" step="1" style="width: 100%;">
                    </div>
                </div>

                <!-- Image Replacement -->
                <div style="margin-bottom: 20px; padding: 15px; background: #fff3cd; border-radius: 6px;">
                    <h4 style="margin: 0 0 8px 0; font-size: 14px; font-weight: 600;">📤 이미지 교체</h4>
                    <p style="margin: 0 0 10px 0; font-size: 11px; color: #666; line-height: 1.4;">선택된 이미지를 새 파일로 교체합니다.</p>
                    <button id="upload-trigger-btn" style="width: 100%; padding: 10px; background: #ffc107; border: none; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 600; color: #000;">
                        📤 이미지 파일 선택
                    </button>
                    <input type="file" id="file-input-global" accept="image/*" style="display: none;">
                </div>

                <!-- Reset Buttons -->
                <div style="margin-bottom: 20px; padding: 15px; background: #f8d7da; border-radius: 6px;">
                    <h4 style="margin: 0 0 10px 0; font-size: 14px; font-weight: 600;">🔄 리셋</h4>
                    <button onclick="resetCurrentImage()" style="width: 100%; padding: 8px; margin-bottom: 8px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                        현재 이미지 리셋
                    </button>
                    <button onclick="resetAllImages()" style="width: 100%; padding: 8px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                        모든 이미지 리셋
                    </button>
                </div>

                <!-- Keyboard Shortcuts Guide -->
                <div style="padding: 12px; background: #e7f3ff; border-radius: 6px; font-size: 11px; line-height: 1.6; color: #004085;">
                    <strong style="display: block; margin-bottom: 6px;">⌨️ 키보드 단축키</strong>
                    <div>• 화살표: 이미지 이동</div>
                    <div>• +/-: 확대/축소</div>
                    <div>• Shift: 10배 빠르게</div>
                    <div>• 마우스 휠: 확대/축소</div>
                    <div>• 드래그: 이미지 이동</div>
                </div>

                <!-- Size Table Add Section -->
                <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 6px; border: 1px solid #ffc107;">
                    <button id="add-size-table-btn" onclick="toggleSizeTableForm()" style="width: 100%; padding: 12px; background: #ffc107; color: #000; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; margin-bottom: 0;">
                        📊 사이즈표 추가
                    </button>

                    <!-- Size Table Form (Initially Hidden) -->
                    <div id="size-table-form" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #ffc107;">
                        <div style="margin-bottom: 12px;">
                            <label for="table-type" style="display: block; margin-bottom: 5px; font-size: 12px; font-weight: 600;">타입 선택:</label>
                            <select id="table-type" style="width: 100%; padding: 8px; font-size: 13px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer;">
                                <option value="top">상의</option>
                                <option value="bottom">하의</option>
                            </select>
                        </div>

                        <div style="margin-bottom: 12px;">
                            <label for="row-count" style="display: block; margin-bottom: 5px; font-size: 12px; font-weight: 600;">행 수 (1-10):</label>
                            <input type="number" id="row-count" min="1" max="10" value="1" style="width: 100%; padding: 8px; font-size: 13px; border: 1px solid #ccc; border-radius: 4px;">
                        </div>

                        <div style="margin-bottom: 12px;">
                            <label for="size-illustration" style="display: block; margin-bottom: 5px; font-size: 12px; font-weight: 600;">도식화 이미지:</label>
                            <select id="size-illustration" style="width: 100%; padding: 8px; font-size: 13px; border: 1px solid #ccc; border-radius: 4px; cursor: pointer;">
                                <option value="">이미지 없음</option>
                            </select>
                        </div>

                        <div style="display: flex; gap: 8px;">
                            <button id="create-table-btn" onclick="createNewSizeTable()" style="flex: 1; padding: 10px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 600;">
                                생성
                            </button>
                            <button id="cancel-table-btn" onclick="toggleSizeTableForm()" style="flex: 1; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 600;">
                                취소
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Export Buttons -->
                <div style="margin-top: 20px; display: flex; gap: 10px; flex-direction: column;">
                    <button onclick="exportHTML()" style="width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                        ✅ HTML 다운로드
                    </button>
                    <button onclick="exportAsJPG()" style="width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                        🖼️ JPG 다운로드
                    </button>
                </div>
            </div>
            '''

        # Contenteditable class
        editable_class = ' editable' if editable else ''
        contenteditable_attr = ' contenteditable="true"' if editable else ''

        # Complete HTML template
        html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product['title']} - {BRAND_NAME}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;700&family=EB+Garamond:wght@400;700&family=Pretendard:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Pretendard', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #ffffff;
            color: #000000;
            line-height: 1.6;
        }}

        .container {{
            width: 1200px;
            margin: 0 auto;
            transform-origin: top center;  /* Scale from top center for page zoom */
            transition: transform 0.2s ease;  /* Smooth zoom transition */
        }}

        /* Section 1: Hero Section with Background Image */
        .hero-section {{
            position: relative;
            height: 1565px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 60px 0;
            overflow: hidden;
        }}

        .hero-image-frame {{
            position: absolute !important;  /* Override .image-frame's position: relative */
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
        }}

        .hero-bg-image {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: unset;
            object-position: unset;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        .hero-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.2);
            z-index: 1;
            pointer-events: none;  /* Allow mouse events to pass through to hero image */
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            color: #FEFEFE;
            width: 100%;
        }}

        .brand-logo {{
            width: 775px;
            height: 98px;
            margin-bottom: 134px;
        }}

        .hero-subtitle {{
            font-family: 'Pretendard', sans-serif;
            font-size: 43px;
            font-weight: 500;
            color: #FEFEFE;
            letter-spacing: 0px;
            margin-bottom: 300px;
        }}

        .hero-footer {{
            position: absolute;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            font-family: 'Cormorant Garamond', serif;
            font-size: 40px;
            font-weight: 400;
            color: #FEFEFE;
            letter-spacing: 0px;
        }}

        /* Section 2: Product Info Section */
        .product-info-intro-section {{
            background-color: #E8E4E0;
            padding: 80px 0;
        }}

        .product-title-main {{
            font-family: 'Pretendard', sans-serif;
            font-size: 70px;
            font-weight: 600;
            color: #000000;
            text-align: center;
            margin-bottom: 40px;
        }}

        .divider-line {{
            width: 975.5px;
            height: 1px;
            background-color: #000000;
            margin: 0 auto 50px;
        }}

        .selling-points {{
            max-width: 900px;
            margin: 0 auto 50px;
        }}

        .selling-point {{
            font-family: 'Pretendard', sans-serif;
            font-size: 45px;
            font-weight: 400;
            color: #000000;
            margin-bottom: 20px;
        }}

        .md-comment {{
            font-family: 'Pretendard', sans-serif;
            font-size: 35px;
            font-weight: 400;
            color: #000000;
            text-align: center;
            margin: 50px 0;
        }}

        /* Section 3: Color Section */
        .color-section {{
            background-color: #E8E4E0;
            padding: 60px 0;
        }}

        .color-section-title {{
            font-family: 'Cormorant Garamond', serif;
            font-size: 70px;
            font-weight: 700;
            color: #000000;
            text-align: center;
            margin-bottom: 80px;
        }}

        .color-swatches-container {{
            display: flex;
            justify-content: center;
            align-items: flex-start;
            gap: 40px;
            flex-wrap: wrap;
            max-width: 800px;
            margin: 0 auto;
        }}

        .color-swatch-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }}

        .color-swatch-wrapper {{
            width: 279.24px;
            height: 279.24px;
            background-color: #d9d9d9;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .color-swatch {{
            position: relative;
            width: 200px;
            height: 200px;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .color-swatch:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        .hex-picker {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 40px;
            height: 40px;
            opacity: 0;
            cursor: pointer;
        }}

        .hex-picker:hover {{
            opacity: 0.5;
        }}

        .color-swatch:hover .hex-picker {{
            opacity: 0.3;
        }}

        .color-name-swatch {{
            font-family: 'Pretendard', sans-serif;
            font-size: 47px;
            font-weight: 600;
            color: #000000;
            text-align: center;
        }}

        /* Section 4: Detail Points */
        .detail-points-section {{
            background-color: #D9D3CE;
            padding: 80px 0;
        }}

        .detail-point-badge {{
            display: inline-block;
            width: 575px;
            height: 175px;
            background-color: #c9c0b8;
            border-radius: 50%;
            font-family: 'Cormorant Garamond', serif;
            font-size: 70px;
            font-weight: 700;
            color: #000000;
            margin-bottom: 60px;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .detail-point-item {{
            display: flex;
            align-items: stretch;
            margin-bottom: 30px;
            margin-left: 62px;
            margin-right: 88px;
            background-color: #FFFFFF;
            overflow: hidden;
            height: 600px;
        }}

        .detail-point-image-wrapper {{
            width: 500px;
            height: 600px;
            flex-shrink: 0;
            position: relative;
            overflow: hidden;
        }}

        .detail-point-image {{
            width: 100%;
            height: 100%;
            object-fit: unset;
            object-position: unset;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        .detail-point-text-box {{
            width: 550px;
            height: 600px;
            padding: 60px 80px;
            background-color: #F8F5F2;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            flex-shrink: 0;
        }}

        .detail-point-number {{
            font-family: 'Pretendard', sans-serif;
            font-size: 60px;
            font-weight: 600;
            color: #000000;
            margin-bottom: 20px;
            letter-spacing: 3px;
        }}

        .detail-point-text {{
            font-family: 'Pretendard', sans-serif;
            font-size: 40px;
            font-weight: 400;
            color: #000000;
            text-align: center;
            line-height: 1.6;
            letter-spacing: 2px;
        }}

        .detail-point-text.editable {{
            min-height: 80px;
            cursor: text;
            outline: none;
        }}

        .detail-point-text.editable:empty:before {{
            content: '텍스트를 입력하세요';
            color: #999;
            font-size: 32px;
        }}

        /* Section 5: Gallery */
        .gallery-section {{
            background-color: #E8E4E0;
            padding: 40px 0;
        }}

        .gallery-color-header {{
            font-family: 'Pretendard', sans-serif;
            font-size: 56px;
            font-weight: 700;
            color: #000000;
            text-align: center;
            margin: 60px 0 30px 0;
            padding: 15px 0;
            background-color: #E8E4E0;
        }}

        .gallery-color-header:first-of-type {{
            margin-top: 20px;
        }}

        .gallery-image-wrapper {{
            width: 100%;
            margin-bottom: 10px;
            position: relative;
            overflow: hidden;
        }}

        .gallery-image {{
            width: 100%;
            height: auto;
            display: block;
        }}

        /* Gallery logo group 1: 이미지 4, 5와 로고 병렬 배치 */
        .gallery-logo-group-1 {{
            position: relative;
            width: 100%;
            height: 989px;
            margin-bottom: 10px;
            overflow: visible;
        }}

        /* Logo group image frames - maintain absolute positioning */
        .logo-group-image-frame {{
            position: absolute;
            overflow: hidden;
        }}

        /* 4번 이미지 (오른쪽) */
        .logo-group-image-frame[data-id$="_1_1"] {{
            right: 71px;
            top: 0;
            width: 480px;
            height: 830px;
        }}

        .gallery-image-4 {{
            width: 100%;
            height: 100%;
            object-fit: unset;
            object-position: unset;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        /* 5번 이미지 (왼쪽, 약간 아래) */
        .logo-group-image-frame[data-id$="_1_2"] {{
            right: 650px;
            top: 159px;
            width: 550px;
            height: 830px;
        }}

        .gallery-image-5 {{
            width: 100%;
            height: 100%;
            object-fit: unset;
            object-position: unset;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        /* 로고 1 (90도 회전, 오른쪽) */
        .gallery-logo-right {{
            position: absolute;
            left: calc(50% + 564.5px);
            top: 127.5px;
            width: 296px;
            height: 41px;
            transform: translateX(-50%) rotate(90deg);
            transform-origin: center;
        }}

        /* 로고 2 (270도 회전, 왼쪽 하단) */
        .gallery-logo-left {{
            position: absolute;
            left: calc(50% - 0.5px);
            top: 820.5px;
            width: 296px;
            height: 41px;
            transform: translateX(-50%) rotate(270deg);
            transform-origin: center;
        }}

        /* Gallery logo group 2: 이미지 7, 8과 로고 배치 */
        .gallery-logo-group-2 {{
            position: relative;
            width: 100%;
            height: 943px;
            margin-bottom: 10px;
            overflow: visible;
        }}

        /* 7번 이미지 (왼쪽) */
        .logo-group-image-frame[data-id$="_2_1"] {{
            right: 630px;
            top: 0;
            width: 520px;
            height: 830px;
        }}

        .gallery-image-7 {{
            width: 100%;
            height: 100%;
            object-fit: unset;
            object-position: unset;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        /* 8번 이미지 (오른쪽) */
        .logo-group-image-frame[data-id$="_2_2"] {{
            right: 50px;
            top: 0;
            width: 520px;
            height: 830px;
        }}

        .gallery-image-8 {{
            width: 100%;
            height: 100%;
            object-fit: unset;
            object-position: unset;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        /* 로고 (중앙 하단) */
        .gallery-logo-horizontal {{
            position: absolute;
            left: 50%;
            top: 881px;
            width: 454px;
            height: 62px;
            transform: translateX(-50%);
        }}

        /* Section 6: Product Shots */
        .product-shots-section {{
            background-color: #E8E4E0;
            padding: 60px 0;
        }}

        .product-shot-wrapper {{
            position: relative;
            width: 994.5px;
            margin: 0 auto 10px auto;
        }}

        .product-shot-image-frame {{
            width: 994.5px;
            position: relative;
            overflow: hidden;
        }}

        .product-shot-image {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .product-shot-color-label {{
            position: absolute;
            top: 20px;
            right: 20px;
            background-color: transparent;
            color: #000000;
            font-family: 'Pretendard', sans-serif;
            font-size: 45px;
            font-weight: 700;
            padding: 10px 20px;
            border-radius: 4px;
        }}

        .shot-notice {{
            text-align: center;
            font-family: 'Pretendard', sans-serif;
            font-size: 12px;
            color: #999999;
            line-height: 1.8;
            margin-top: 30px;
        }}

        /* Section 7: Fabric & Product Info (통합) */
        .fabric-product-info-section {{
            background-color: #FFFFFF;
            padding: 60px 0 20px 0;
        }}

        .section-title {{
            font-family: 'Cormorant Garamond', serif;
            font-size: 70px;
            font-weight: 700;
            color: #000000;
            text-align: center;
            margin-bottom: 60px;
        }}

        /* Fabric image container with background */
        .fabric-image-container {{
            position: relative;
            width: 100%;
            height: 600px;
            display: flex;
            align-items: flex-start;
            justify-content: flex-start;
            padding: 0;
            margin-bottom: 0;
            overflow: hidden;
        }}

        .fabric-image-frame {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
        }}

        .fabric-bg-image {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: unset;
            object-position: unset;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        /* Fabric overlay text */
        .fabric-overlay-text {{
            position: absolute;
            left: calc(50% - 555px);
            bottom: 40px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 1;
        }}

        /* Large "FABRIC" label */
        .fabric-label {{
            font-family: 'EB Garamond', serif;
            font-size: 80px;
            font-weight: 700;
            color: #FFFFFF;
            text-transform: uppercase;
        }}

        /* Fabric name overlay */
        .fabric-name-overlay {{
            font-family: 'Pretendard', sans-serif;
            font-size: 20px;
            font-weight: 600;
            color: #FFFFFF;
        }}

        /* Fabric composition overlay */
        .fabric-composition {{
            font-family: 'Pretendard', sans-serif;
            font-size: 28px;
            font-weight: 500;
            color: #FFFFFF;
        }}

        /* Navy description box */
        .fabric-description-box {{
            background-color: #031a13;
            padding: 40px 60px;
            margin-bottom: 40px;
        }}

        /* White description text */
        .fabric-desc-text {{
            font-family: 'Pretendard', sans-serif;
            font-size: 50px;
            font-weight: 400;
            color: #FFFFFF;
            text-align: center;
            line-height: 1.8;
            margin: 0;
        }}

        /* Fabric Properties 4-Column Grid (Figma node 53-101) */
        /* Grid structure: 5 rows × 4 columns */
        /* Each row: [Property Label] [Option 1] [Option 2] [Option 3] */
        .fabric-properties-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0;
            max-width: 1000px;
            margin: 40px auto;
            border-top: 3px solid #000000;
            border-bottom: 3px solid #000000;
        }}

        .fabric-prop-header {{
            height: 97px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #FFFFFF;
            border-bottom: 1px solid #000000;
            font-family: 'Pretendard', sans-serif;
            font-size: 35px;
            font-weight: 600;
            color: #000000;
        }}

        /* Only property label column (first in each row) gets right border */
        .fabric-prop-header {{
            border-right: 1px solid #000000;
        }}

        .fabric-prop-cell {{
            height: 97px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #FFFFFF;
            border-bottom: 1px solid #000000;
            font-family: 'Pretendard', sans-serif;
            font-size: 35px;
            font-weight: 600;
            color: #000000;
        }}

        .fabric-prop-cell.selected {{
            background-color: #d9d9d9;
        }}

        .fabric-prop-cell-empty {{
            background-color: #FFFFFF;
        }}

        .fabric-properties-grid > div:nth-last-child(-n+4) {{
            border-bottom: none;
        }}

        /* Product Info Horizontal Layout (Figma node 1-91) */
        .product-info-horizontal {{
            display: flex;
            gap: 60px;
            max-width: 1000px;
            margin: 60px auto;
            align-items: flex-start;
        }}

        .product-info-image-container {{
            width: 300px;
            flex-shrink: 0;
        }}

        .product-info-image {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .product-info-table {{
            flex: 1;
            border-collapse: collapse;
        }}

        .product-info-table tr {{
            border-bottom: 1px solid #E0E0E0;
        }}

        .product-info-table tr:last-child {{
            border-bottom: none;
        }}

        .product-info-label {{
            font-family: 'Pretendard', sans-serif;
            font-size: 40px;
            font-weight: 600;
            color: #000000;
            line-height: 70px;
            padding: 10px 20px 10px 0;
            vertical-align: top;
            width: 200px;
        }}

        .product-info-value {{
            font-family: 'Pretendard', sans-serif;
            font-size: 40px;
            font-weight: 500;
            color: #000000;
            line-height: 70px;
            padding: 10px 0;
            vertical-align: top;
        }}

        /* Size Table */
        .size-table {{
            width: 100%;
            max-width: 900px;
            margin: 40px auto;
            border-collapse: collapse;
            background: #FFFFFF;
        }}

        .size-table th,
        .size-table td {{
            padding: 15px;
            text-align: center;
            font-family: 'Pretendard', sans-serif;
            font-size: 30px;
            border: 1px solid #E0E0E0;
        }}

        .size-table th {{
            background-color: #e4e4e4;
            color: #000000;
            font-weight: 600;
        }}

        .size-table td {{
            font-weight: 400;
        }}

        /* Editable mode styles */
        .editable {{
            outline: 2px dashed transparent;
            transition: outline 0.2s;
        }}

        .editable:hover {{
            outline-color: #007bff;
        }}

        .editable:focus {{
            outline-color: #0056b3;
            background-color: #f0f8ff;
        }}

        /* Image frame for crop controls */
        .image-frame {{
            position: relative;
            overflow: hidden;
            cursor: grab;
            border: 3px solid transparent;
            transition: border-color 0.3s, box-shadow 0.3s;
        }}

        .image-frame:hover {{
            border-color: #007bff;
            box-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
        }}

        .image-frame.selected {{
            border-color: #28a745;
            box-shadow: 0 0 15px rgba(40, 167, 69, 0.5);
        }}

        .image-frame.dragging {{
            cursor: grabbing;
            border-color: #ffc107;
        }}

        /* Editable image with transform support */
        .editable-image {{
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.1s ease-out;
            transform-origin: center center;
        }}

        /* Override image-frame styles for logo group images */
        .logo-group-image-frame.image-frame {{
            position: absolute !important;
            cursor: grab;
        }}

        .logo-group-image-frame.image-frame:hover {{
            border-color: #007bff;
            box-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .colors-grid,
            .detail-points-grid,
            .gallery-grid,
            .product-shots-grid {{
                grid-template-columns: 1fr;
            }}

            .product-title {{
                font-size: 22px;
            }}

            .section-title {{
                font-size: 20px;
            }}
        }}

        /* Add Size Table Button */
        .add-size-table-btn {{
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
        }}

        .add-size-table-btn:hover {{
            background-color: #45a049;
            transform: translateY(-2px);
        }}

        .add-size-table-btn:active {{
            transform: translateY(0);
        }}

        /* Modal */
        .modal {{
            display: none;
            position: absolute;
            z-index: 10000;
            left: 50%;
            transform: translateX(-50%);
            top: 100%;
            margin-top: 20px;
            width: auto;
            background-color: rgba(0,0,0,0.5);
            padding: 20px;
            border-radius: 12px;
        }}

        .modal-content {{
            background-color: #fefefe;
            margin: 0;
            padding: 30px;
            border: 1px solid #888;
            border-radius: 12px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}

        .modal-content h2 {{
            margin-top: 0;
            margin-bottom: 20px;
            font-family: 'Pretendard', sans-serif;
            font-size: 24px;
            color: #333;
        }}

        .close {{
            color: #aaa;
            float: right;
            font-size: 32px;
            font-weight: bold;
            line-height: 20px;
            cursor: pointer;
        }}

        .close:hover,
        .close:focus {{
            color: #000;
        }}

        .modal-form {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .form-group {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .form-group label {{
            font-family: 'Pretendard', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: #333;
        }}

        .form-control {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-family: 'Pretendard', sans-serif;
            font-size: 14px;
            transition: border-color 0.3s;
        }}

        .form-control:focus {{
            outline: none;
            border-color: #4CAF50;
        }}

        .btn-primary {{
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}

        .btn-primary:hover {{
            background-color: #45a049;
        }}

        .btn-secondary {{
            background-color: #757575;
            color: white;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}

        .btn-secondary:hover {{
            background-color: #616161;
        }}
    </style>
</head>
<body>
    {control_panel_html}

    <div class="container">
        <!-- Section 1: Hero Section with Background Image -->
        <section class="hero-section">
            <div class="hero-image-frame image-frame" data-id="hero">
                <img src="{main_image_base64}" alt="Hero background" class="hero-bg-image editable-image">
            </div>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <img src="{logo_white_base64}" alt="DANA&PETA" class="brand-logo">
                <div class="hero-subtitle{editable_class}"{contenteditable_attr}>- 퀸잇이 제안하는 트렌디 패션 -</div>
            </div>
            <div class="hero-footer{editable_class}"{contenteditable_attr}>queenit made</div>
        </section>

        <!-- Section 2: Product Info Introduction -->
        <section class="product-info-intro-section">
            <h1 class="product-title-main{editable_class}"{contenteditable_attr}>{product['title']}</h1>
            <div class="divider-line"></div>
            <div class="selling-points">
                {selling_points_html}
            </div>
            <div class="divider-line"></div>
            <div class="md-comment{editable_class}"{contenteditable_attr}>{product.get('mdComment', '')}</div>
        </section>

        <!-- Section 3: Color Section -->
        <section class="color-section">
            <h2 class="color-section-title{editable_class}"{contenteditable_attr}>COLOR</h2>
            {colors_html}
        </section>

        <!-- Section 4: Detail Points -->
        <section class="detail-points-section">
            <div style="display: flex; justify-content: center;">
                <div class="detail-point-badge{editable_class}"{contenteditable_attr}>DETAIL POINT</div>
            </div>
            {detail_points_html}
        </section>

        <!-- Section 5: Gallery -->
        <section class="gallery-section">
            {gallery_html}
        </section>

        <!-- Section 6: Product Shots -->
        <section class="product-shots-section">
            {product_shots_html}
            <div class="shot-notice{editable_class}"{contenteditable_attr}>{shot_notice_html}</div>
        </section>

        <!-- Section 7: FABRIC INFO + PRODUCT INFO (통합) -->
        <section class="fabric-product-info-section">
            <h2 class="section-title{editable_class}"{contenteditable_attr}>FABRIC INFO</h2>

            <!-- Fabric image with text overlay -->
            <div class="fabric-image-container">
                <div class="fabric-image-frame image-frame" data-id="fabric">
                    <img src="{fabric_image_base64}" alt="Fabric" class="fabric-bg-image editable-image">
                </div>
                <div class="fabric-overlay-text">
                    <div class="fabric-label{editable_class}"{contenteditable_attr}>FABRIC</div>
                    <div class="fabric-composition{editable_class}"{contenteditable_attr}>{fabric_info.get('composition', '')}</div>
                    <div class="fabric-name-overlay{editable_class}"{contenteditable_attr}>{fabric_info.get('name', '')}</div>
                </div>
            </div>

            <!-- Navy box with description -->
            <div class="fabric-description-box">
                <p class="fabric-desc-text{editable_class}"{contenteditable_attr}>{fabric_info.get('description', '')}</p>
            </div>

            {fabric_properties_html}

            <h2 class="section-title{editable_class}"{contenteditable_attr} style="margin-top: 100px;">PRODUCT INFO</h2>
            {product_info_html}
            <div id="size-tables-container">
                {size_table_html}
            </div>
        </section>
    </div>
{editable_scripts}
</body>
</html>'''

        return html

    def generate_pages(self, product_code: Optional[str] = None) -> None:
        """Generate HTML pages for products"""
        try:
            products_to_generate = self.products

            if product_code:
                products_to_generate = [
                    p for p in self.products if p['productCode'] == product_code
                ]
                if not products_to_generate:
                    logger.warning(f"⚠️  Product not found: {product_code}")
                    return

            logger.info(f"📝 Generating HTML pages for {len(products_to_generate)} products...")

            for product in products_to_generate:
                try:
                    code = product['productCode']
                    logger.info(f"🔨 Generating pages for {code}...")

                    # Generate original HTML
                    original_html = self.generate_html(product, editable=False)
                    original_file = self.output_original / ORIGINAL_FILE_PATTERN.format(
                        productCode=code
                    )
                    with open(original_file, 'w', encoding='utf-8') as f:
                        f.write(original_html)
                    logger.info(f"✅ Generated original: {original_file}")

                    # Generate editable HTML
                    editable_html = self.generate_html(product, editable=True)
                    editable_file = self.output_editable / EDITABLE_FILE_PATTERN.format(
                        productCode=code
                    )
                    with open(editable_file, 'w', encoding='utf-8') as f:
                        f.write(editable_html)
                    logger.info(f"✅ Generated editable: {editable_file}")

                except Exception as e:
                    logger.error(f"❌ Failed to generate pages for {code}: {e}")
                    continue

            logger.info(f"✅ Successfully generated {len(products_to_generate)} products")

        except Exception as e:
            logger.error(f"❌ Page generation failed: {e}")
            raise

    def run(self, product_code: Optional[str] = None) -> None:
        """Run the page generation process"""
        try:
            logger.info("=" * 60)
            logger.info("DANA&PETA HTML Page Generator")
            logger.info("=" * 60)

            # Load products data
            logger.info("\n📝 Step 1: Loading products data...")
            self.load_products_data()

            # Generate pages
            logger.info("\n📝 Step 2: Generating HTML pages...")
            self.generate_pages(product_code)

            logger.info("\n" + "=" * 60)
            logger.info("✅ Page generation completed successfully!")
            logger.info(f"📂 Output folders:")
            logger.info(f"   - Original: {self.output_original}")
            logger.info(f"   - Editable: {self.output_editable}")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"\n❌ Page generation failed: {e}")
            raise


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate DANA&PETA product pages')
    parser.add_argument('--product', help='Generate specific product only (by product code)')

    args = parser.parse_args()

    generator = DanaPageGenerator()
    generator.run(product_code=args.product)


if __name__ == "__main__":
    main()
