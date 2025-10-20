"""
Flask Local Server for DANA&PETA Page Builder
Serves editable HTML and handles file exports to output/날짜/익스포트
"""

import base64
import json
import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from config import DATE_FORMAT, EDITABLE_FOLDER, OUTPUT_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Export folder name
EXPORT_FOLDER = "익스포트"


def get_today_export_dir():
    """Get today's export directory"""
    today = datetime.now().strftime(DATE_FORMAT)
    export_dir = OUTPUT_DIR / today / EXPORT_FOLDER
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir


def get_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
    """Generate unique filename by adding numbers if file exists"""
    file_path = directory / f"{base_name}{extension}"

    if not file_path.exists():
        return file_path

    counter = 1
    while True:
        file_path = directory / f"{base_name}_{counter}{extension}"
        if not file_path.exists():
            return file_path
        counter += 1


@app.route('/save-html', methods=['POST'])
def save_html():
    """Save HTML file to output/날짜/익스포트"""
    try:
        data = request.get_json()
        product_code = data.get('productCode')
        html_content = data.get('htmlContent')

        if not product_code or not html_content:
            return jsonify({'error': 'Missing productCode or htmlContent'}), 400

        # Get export directory
        export_dir = get_today_export_dir()

        # Generate unique filename
        base_name = f"{product_code}_exported_dana"
        file_path = get_unique_filename(export_dir, base_name, ".html")

        # Save HTML file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"✅ HTML saved: {file_path}")

        return jsonify({
            'success': True,
            'path': str(file_path.relative_to(OUTPUT_DIR.parent)),
            'filename': file_path.name
        })

    except Exception as e:
        logger.error(f"❌ HTML save error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/save-jpg', methods=['POST'])
def save_jpg():
    """Save JPG file to output/날짜/익스포트"""
    try:
        data = request.get_json()
        product_code = data.get('productCode')
        image_data = data.get('imageData')

        if not product_code or not image_data:
            return jsonify({'error': 'Missing productCode or imageData'}), 400

        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        # Decode base64 image
        image_bytes = base64.b64decode(image_data)

        # Get export directory
        export_dir = get_today_export_dir()

        # Generate unique filename
        base_name = f"{product_code}_dana"
        file_path = get_unique_filename(export_dir, base_name, ".jpg")

        # Save JPG file
        with open(file_path, 'wb') as f:
            f.write(image_bytes)

        logger.info(f"✅ JPG saved: {file_path}")

        return jsonify({
            'success': True,
            'path': str(file_path.relative_to(OUTPUT_DIR.parent)),
            'filename': file_path.name
        })

    except Exception as e:
        logger.error(f"❌ JPG save error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/editable/<product_code>')
def serve_editable(product_code):
    """Serve editable HTML file"""
    try:
        today = datetime.now().strftime(DATE_FORMAT)
        editable_dir = OUTPUT_DIR / today / EDITABLE_FOLDER

        file_path = editable_dir / f"{product_code}_editable.html"

        if not file_path.exists():
            return f"❌ File not found: {file_path}", 404

        return send_file(file_path, mimetype='text/html')

    except Exception as e:
        logger.error(f"❌ Serve error: {e}")
        return f"❌ Error: {e}", 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


@app.route('/')
def index():
    """Show available editable files"""
    try:
        today = datetime.now().strftime(DATE_FORMAT)
        editable_dir = OUTPUT_DIR / today / EDITABLE_FOLDER

        if not editable_dir.exists():
            return f"""
            <h1>DANA&PETA 에디터블 서버</h1>
            <p>❌ 에디터블 파일이 없습니다.</p>
            <p>먼저 <code>python3 scripts/generate_pages_dana.py</code>를 실행하세요.</p>
            """

        # Find all editable HTML files
        editable_files = list(editable_dir.glob("*_editable.html"))

        if not editable_files:
            return f"""
            <h1>DANA&PETA 에디터블 서버</h1>
            <p>❌ 에디터블 파일이 없습니다.</p>
            <p>먼저 <code>python3 scripts/generate_pages_dana.py</code>를 실행하세요.</p>
            """

        # Generate HTML list
        html = """
        <html>
        <head>
            <title>DANA&PETA 에디터블 서버</title>
            <style>
                body {
                    font-family: 'Pretendard', sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    border-bottom: 2px solid #333;
                    padding-bottom: 10px;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    border-left: 4px solid #007bff;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                    font-weight: 600;
                }
                a:hover {
                    text-decoration: underline;
                }
                .info {
                    color: #666;
                    font-size: 14px;
                    margin-top: 20px;
                    padding: 15px;
                    background: #e7f3ff;
                    border-radius: 8px;
                }
            </style>
        </head>
        <body>
            <h1>🖼️ DANA&PETA 에디터블 서버</h1>
            <p>사용 가능한 에디터블 파일:</p>
            <ul>
        """

        for file in editable_files:
            product_code = file.stem.replace("_editable", "")
            html += f"""
                <li>
                    <a href="/editable/{product_code}" target="_blank">
                        {product_code}
                    </a>
                </li>
            """

        html += """
            </ul>
            <div class="info">
                <strong>💡 사용 방법:</strong><br>
                1. 위 링크를 클릭하여 에디터블 HTML 열기<br>
                2. 우측 컨트롤 패널에서 이미지 편집<br>
                3. "HTML 다운로드" 또는 "JPG 다운로드" 클릭<br>
                4. 파일이 <code>output/날짜/익스포트</code> 폴더에 자동 저장됨
            </div>
        </body>
        </html>
        """

        return html

    except Exception as e:
        logger.error(f"❌ Index error: {e}")
        return f"❌ Error: {e}", 500


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 DANA&PETA 에디터블 서버 시작")
    logger.info("=" * 60)
    logger.info(f"📂 Output Directory: {OUTPUT_DIR}")
    logger.info(f"🌐 Server URL: http://localhost:5001")
    logger.info("=" * 60)

    # Run Flask server
    app.run(host='0.0.0.0', port=5001, debug=True)
