"""
DANA&PETA Index Page Generator
Creates an index page with links to all product pages
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from config import (
    BRAND_NAME,
    DATE_FORMAT,
    LOG_DATE_FORMAT,
    LOG_FILE,
    LOG_FORMAT,
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


class IndexPageGenerator:
    """Generate index page for DANA&PETA products"""

    def __init__(self):
        """Initialize the index page generator"""
        self.products = []
        self.date_folder = datetime.now().strftime(DATE_FORMAT)
        self.original_folder = OUTPUT_DIR / self.date_folder / ORIGINAL_FOLDER
        self.index_file = OUTPUT_DIR / "index.html"

    def load_products_data(self) -> None:
        """Load products from JSON file"""
        try:
            if not PRODUCTS_DATA_PATH.exists():
                raise FileNotFoundError(f"❌ Products data not found: {PRODUCTS_DATA_PATH}")

            with open(PRODUCTS_DATA_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.products = data.get('products', [])
            logger.info(f"✅ Loaded {len(self.products)} products")

        except Exception as e:
            logger.error(f"❌ Failed to load products data: {e}")
            raise

    def generate_index_html(self) -> str:
        """Generate index page HTML"""

        # Build product cards HTML
        product_cards_html = ""
        for product in self.products:
            code = product['productCode']
            title = product['title']
            page_path = f"{self.date_folder}/{ORIGINAL_FOLDER}/{code}.html"

            product_cards_html += f'''
            <div class="product-card">
                <a href="{page_path}" class="product-link">
                    <div class="product-info">
                        <div class="product-code">{code}</div>
                        <div class="product-title">{title}</div>
                    </div>
                </a>
            </div>
            '''

        # Complete HTML
        html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{BRAND_NAME} - Product Index</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: #f8f8f8;
            color: #333;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            margin-bottom: 50px;
        }}

        .brand-name {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }}

        .subtitle {{
            font-size: 14px;
            color: #999;
            margin-bottom: 30px;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 20px;
        }}

        .stat-item {{
            font-size: 14px;
        }}

        .stat-label {{
            color: #999;
            margin-right: 5px;
        }}

        .stat-value {{
            font-weight: bold;
            color: #333;
        }}

        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }}

        .product-card {{
            background: #fff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .product-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }}

        .product-link {{
            display: block;
            text-decoration: none;
            color: inherit;
        }}

        .product-info {{
            padding: 30px 20px;
        }}

        .product-code {{
            font-size: 12px;
            color: #999;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }}

        .product-title {{
            font-size: 16px;
            font-weight: bold;
            line-height: 1.4;
            color: #333;
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            background: #fff;
            border-radius: 12px;
            margin-top: 40px;
        }}

        .footer-text {{
            font-size: 12px;
            color: #999;
            line-height: 1.8;
        }}

        @media (max-width: 768px) {{
            .products-grid {{
                grid-template-columns: 1fr;
            }}

            .brand-name {{
                font-size: 24px;
            }}

            .stats {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="brand-name">{BRAND_NAME}</div>
            <div class="subtitle">Product Detail Pages</div>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-label">Total Products:</span>
                    <span class="stat-value">{len(self.products)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Generated:</span>
                    <span class="stat-value">{self.date_folder}</span>
                </div>
            </div>
        </div>

        <div class="products-grid">
            {product_cards_html}
        </div>

        <div class="footer">
            <div class="footer-text">
                {BRAND_NAME} Product Pages<br>
                Generated by DANA&PETA Page Builder v1.0.0<br>
                © 2025 All Rights Reserved
            </div>
        </div>
    </div>
</body>
</html>'''

        return html

    def generate(self) -> None:
        """Generate index page"""
        try:
            logger.info("🚀 Generating index page...")

            # Check if original folder exists
            if not self.original_folder.exists():
                logger.warning(f"⚠️  Original folder not found: {self.original_folder}")
                logger.warning("   Please run generate_pages_dana.py first")
                return

            # Generate HTML
            html = self.generate_index_html()

            # Save to file
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write(html)

            logger.info(f"✅ Index page generated: {self.index_file}")
            logger.info(f"📊 Total products: {len(self.products)}")

        except Exception as e:
            logger.error(f"❌ Index generation failed: {e}")
            raise

    def run(self) -> None:
        """Run the index generation process"""
        try:
            logger.info("=" * 60)
            logger.info("DANA&PETA Index Page Generator")
            logger.info("=" * 60)

            # Load products
            logger.info("\n📝 Step 1: Loading products data...")
            self.load_products_data()

            # Generate index
            logger.info("\n📝 Step 2: Generating index page...")
            self.generate()

            logger.info("\n" + "=" * 60)
            logger.info("✅ Index generation completed!")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"\n❌ Index generation failed: {e}")
            raise


def main():
    """Main entry point"""
    generator = IndexPageGenerator()
    generator.run()


if __name__ == "__main__":
    main()
