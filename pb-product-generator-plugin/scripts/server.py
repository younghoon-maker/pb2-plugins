"""
Flask 로컬 서버 - Editable HTML 제공 및 Export 처리 (V4 - 날짜별 폴더 지원)

Port 5001에서 실행:
- /: 에디터블 파일 목록 (최신 날짜 폴더)
- /editable/<product_code>: 에디터블 HTML 제공 (최신 날짜 폴더)
- /save-html: HTML 저장 (POST) → export 폴더
- /save-jpg: JPG 저장 (POST) → export 폴더

폴더 구조:
  output/
  ├── {YYYYMMDD}/
  │   ├── editable/    # 에디터블 HTML (배치 생성 스크립트가 생성)
  │   └── export/      # 익스포트 결과물 (서버가 저장)

실행 방법:
  python scripts/server.py
"""

import os
import sys
import base64
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS

# 프로젝트 루트
project_root = Path(__file__).parent.parent.resolve()

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)  # CORS 활성화 (브라우저 보안)

# 출력 디렉토리 (현재 작업 디렉토리 기준)
OUTPUT_DIR = Path(os.getcwd()) / "output"


def get_latest_date_folder() -> Path:
    """
    최신 날짜 폴더 반환 (YYYYMMDD 형식)

    Returns:
        최신 날짜 폴더 Path (없으면 오늘 날짜 폴더 생성)
    """
    # 숫자로만 구성된 디렉토리 찾기 (YYYYMMDD)
    date_folders = [
        d for d in OUTPUT_DIR.iterdir()
        if d.is_dir() and d.name.isdigit() and len(d.name) == 8
    ]

    if not date_folders:
        # 폴더가 없으면 오늘 날짜로 생성
        today = datetime.now().strftime("%Y%m%d")
        date_folder = OUTPUT_DIR / today
        date_folder.mkdir(exist_ok=True, parents=True)
        return date_folder

    # 최신 날짜 폴더 반환 (숫자로 정렬)
    return max(date_folders, key=lambda d: d.name)


def get_editable_folder() -> Path:
    """에디터블 폴더 경로 (최신 날짜)"""
    latest = get_latest_date_folder()
    editable_dir = latest / "editable"
    editable_dir.mkdir(exist_ok=True, parents=True)
    return editable_dir


def get_export_folder() -> Path:
    """익스포트 폴더 경로 (현재 날짜)"""
    today = datetime.now().strftime("%Y%m%d")
    export_dir = OUTPUT_DIR / today / "export"
    export_dir.mkdir(exist_ok=True, parents=True)
    return export_dir


def get_unique_filename(directory: Path, base_name: str, extension: str) -> Path:
    """
    중복 파일명 처리 (자동 suffix 추가)

    Args:
        directory: 저장 디렉토리
        base_name: 기본 파일명
        extension: 확장자 (.html, .jpg)

    Returns:
        고유한 파일 경로
    """
    file_path = directory / f"{base_name}{extension}"

    if not file_path.exists():
        return file_path

    counter = 1
    while True:
        file_path = directory / f"{base_name}_{counter}{extension}"
        if not file_path.exists():
            return file_path
        counter += 1


@app.route('/')
def index():
    """에디터블 파일 목록 표시 (최신 날짜 폴더)"""
    try:
        # 최신 날짜 폴더 가져오기
        editable_folder = get_editable_folder()
        latest_date = editable_folder.parent.name

        # editable 폴더에서 *_editable_v4.html 파일 찾기
        editable_files = list(editable_folder.glob("*_editable*.html"))

        if not editable_files:
            return """
            <html>
            <head>
                <title>Editable HTML Files</title>
                <style>
                    body { font-family: 'Pretendard', sans-serif; padding: 40px; background: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
                    h1 { color: #333; }
                    .warning { background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎨 Editable HTML Files</h1>
                    <div class="warning">
                        ⚠️ 에디터블 파일이 없습니다.
                        <p>다음 명령으로 생성하세요:</p>
                        <code>python examples/generate_figma_editable_v4_batch.py --all</code>
                    </div>
                </div>
            </body>
            </html>
            """

        # 파일 목록 HTML 생성
        file_list = ""
        for file_path in sorted(editable_files):
            # product_code 추출 (예: VD25FPT003_editable_v4.html → VD25FPT003_v4)
            stem = file_path.stem  # 확장자 제거
            # _editable 또는 _editable_v4 제거
            if "_editable_v4" in stem:
                product_code = stem.replace("_editable", "")
            elif "_editable" in stem:
                product_code = stem.replace("_editable", "")
            else:
                product_code = stem

            file_list += f'''
            <li style="margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 4px;">
                <a href="/editable/{product_code}"
                   style="font-size: 18px; color: #007bff; text-decoration: none; font-weight: 600;">
                    {product_code}
                </a>
                <div style="font-size: 14px; color: #666; margin-top: 5px;">
                    {file_path.name} ({file_path.stat().st_size / 1024 / 1024:.1f} MB)
                </div>
            </li>
            '''

        return f"""
        <html>
        <head>
            <title>Editable HTML Files</title>
            <style>
                body {{ font-family: 'Pretendard', sans-serif; padding: 40px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 15px; }}
                ul {{ list-style: none; padding: 0; }}
                .info {{ background: #e7f3ff; padding: 15px; border-left: 4px solid #007bff; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎨 Editable HTML Files (V4)</h1>
                <div class="info">
                    📅 날짜: <code>{latest_date}</code><br>
                    📁 에디터블 폴더: <code>{editable_folder}</code><br>
                    💾 익스포트 폴더: <code>{get_export_folder()}</code>
                </div>
                <ul style="margin-top: 30px;">
                    {file_list}
                </ul>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        return f"<h1>❌ Error</h1><p>{str(e)}</p>", 500


@app.route('/editable/<product_code>')
def serve_editable(product_code):
    """에디터블 HTML 파일 제공 (최신 날짜 폴더)"""
    try:
        editable_folder = get_editable_folder()

        # 파일명 패턴 매칭 (예: VD25FPT003_v4 → VD25FPT003_editable_v4.html)
        possible_files = []

        # product_code가 _v4로 끝나는 경우 (예: VD25FPT003_v4)
        if product_code.endswith("_v4"):
            base_code = product_code[:-3]  # _v4 제거
            possible_files = [
                editable_folder / f"{base_code}_editable_v4.html",  # VD25FPT003_editable_v4.html
                editable_folder / f"{product_code}_editable.html",  # VD25FPT003_v4_editable.html
                editable_folder / f"{product_code}.html",           # VD25FPT003_v4.html
            ]
        else:
            # product_code가 _v4로 끝나지 않는 경우 (예: VD25FPT003)
            possible_files = [
                editable_folder / f"{product_code}_editable_v4.html",
                editable_folder / f"{product_code}_editable.html",
                editable_folder / f"{product_code}.html",
            ]

        # 첫 번째로 존재하는 파일 찾기
        file_path = None
        for path in possible_files:
            if path.exists():
                file_path = path
                break

        if not file_path:
            return f"""<h1>❌ File not found</h1>
                      <p>Product Code: {product_code}</p>
                      <p>Searched in: {editable_folder}</p>
                      <p>Tried patterns:</p>
                      <ul>{''.join(f'<li>{p.name}</li>' for p in possible_files)}</ul>
                      """, 404

        return send_file(file_path, mimetype='text/html')

    except Exception as e:
        return f"<h1>❌ Error</h1><p>{str(e)}</p>", 500


@app.route('/save-html', methods=['POST'])
def save_html():
    """HTML 파일 저장 (현재 날짜 export 폴더)"""
    try:
        data = request.get_json()
        product_code = data.get('productCode')
        html_content = data.get('htmlContent')

        if not product_code or not html_content:
            return jsonify({"error": "Missing productCode or htmlContent"}), 400

        # 현재 날짜 export 폴더
        export_dir = get_export_folder()

        # 고유한 파일명 생성
        file_path = get_unique_filename(
            export_dir,
            f"{product_code}_exported",
            ".html"
        )

        # 파일 저장
        file_path.write_text(html_content, encoding='utf-8')

        print(f"✅ HTML saved: {file_path}")
        return jsonify({
            "success": True,
            "path": str(file_path),
            "filename": file_path.name
        })

    except Exception as e:
        print(f"❌ Save HTML error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/save-jpg', methods=['POST'])
def save_jpg():
    """JPG 파일 저장 (현재 날짜 export 폴더)"""
    try:
        data = request.get_json()
        product_code = data.get('productCode')
        image_data = data.get('imageData')

        print(f"\n📥 JPG 저장 요청 받음:")
        print(f"   Product Code: {product_code}")
        print(f"   ImageData 타입: {type(image_data)}")
        print(f"   ImageData 길이: {len(image_data) if image_data else 0}")
        if image_data:
            print(f"   ImageData 시작: {image_data[:100]}")

        if not product_code or not image_data:
            return jsonify({"error": "Missing productCode or imageData"}), 400

        # Base64 디코딩
        # data:image/jpeg;base64,... 형식에서 base64 부분만 추출
        base64_part = image_data
        if image_data.startswith('data:image'):
            header, base64_part = image_data.split(',', 1)
            print(f"   Base64 헤더: {header}")
            print(f"   Base64 데이터 길이: {len(base64_part)} chars")

            # V4.2 FIX: 너무 짧은 데이터 검증 강화 (1KB 미만은 비정상)
            if len(base64_part) < 1000:
                print(f"   ❌ 에러: Base64 데이터가 너무 짧습니다! ({len(base64_part)} chars, 예상: 100KB+)")
                print(f"   전체 데이터: {repr(base64_part[:200])}")

                error_message = (
                    f"❌ 생성된 이미지가 비정상적으로 작습니다\n\n"
                    f"📊 Base64 길이: {len(base64_part)} chars (예상: 100KB+)\n"
                    f"💡 Canvas가 비어있을 가능성이 높습니다.\n\n"
                    f"해결 방법:\n"
                    f"1. 브라우저 콘솔에서 메모리 에러 확인\n"
                    f"2. 이미지 갯수를 줄여주세요\n"
                    f"3. 이미지 해상도를 낮춰주세요\n"
                    f"4. 브라우저를 재시작해주세요 (메모리 정리)"
                )
                return jsonify({"error": error_message}), 400
        else:
            base64_part = image_data

        image_bytes = base64.b64decode(base64_part)
        print(f"   디코딩된 바이트 길이: {len(image_bytes)} bytes ({len(image_bytes) / 1024:.1f} KB)")

        # 현재 날짜 export 폴더
        export_dir = get_export_folder()

        # 고유한 파일명 생성
        file_path = get_unique_filename(
            export_dir,
            product_code,
            ".jpg"
        )

        # 파일 저장
        file_path.write_bytes(image_bytes)

        print(f"✅ JPG saved: {file_path}")
        return jsonify({
            "success": True,
            "path": str(file_path),
            "filename": file_path.name
        })

    except Exception as e:
        print(f"❌ Save JPG error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # 최신 날짜 폴더 정보
    latest_date_folder = get_latest_date_folder()
    latest_date = latest_date_folder.name
    editable_folder = get_editable_folder()
    export_folder = get_export_folder()

    print("=" * 60)
    print("🚀 Editable HTML Server V4 (날짜별 폴더 지원)")
    print("=" * 60)
    print(f"📅 현재 날짜: {latest_date}")
    print(f"📁 에디터블 폴더: {editable_folder}")
    print(f"💾 익스포트 폴더: {export_folder}")
    print(f"🌐 Server URL: http://localhost:5001")
    print("=" * 60)
    print()

    # Port 5001에서 실행 (5000은 macOS AirPlay가 사용)
    app.run(host='0.0.0.0', port=5001, debug=False)
