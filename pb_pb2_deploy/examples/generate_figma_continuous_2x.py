"""
Figma 템플릿 기반 HTML 페이지 생성 (연속 배치 + 폰트 2배)

피드백 반영:
1. 모든 섹션의 배경색 제거 (흰색 배경)
2. Pretendard Light 폰트 사용 및 섹션별 글씨 색깔 적용
3. 갤러리 섹션에 컬러칩 추가 (42x42px, Color Selector 참조)

실행 방법:
  python examples/generate_figma_continuous_2x.py

환경변수 설정 (선택):
  export GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
  export GOOGLE_SHEET_ID=your-sheet-id
"""

import os
import sys
import base64
import tempfile
from pathlib import Path
from typing import Optional

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.sheets_loader.loader import SheetsLoader
from src.sheets_loader.product_builder import ProductDataBuilder


def image_to_base64(sheets_loader: SheetsLoader, image_url: str) -> Optional[str]:
    """
    이미지를 Google Drive에서 다운로드하고 Base64로 변환

    Args:
        sheets_loader: SheetsLoader 인스턴스 (Google Drive API 사용)
        image_url: 이미지 URL (Google Drive)

    Returns:
        Base64 data URL (예: "data:image/jpeg;base64,...")
    """
    if not image_url:
        return None

    try:
        # 임시 파일에 이미지 다운로드
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        # Google Drive API로 다운로드
        sheets_loader.download_image(image_url, tmp_path)

        # Base64 인코딩
        with open(tmp_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')

        # 임시 파일 삭제
        tmp_path.unlink()

        # MIME type 감지 (확장자 기반)
        suffix = tmp_path.suffix.lower()
        mime_type = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }.get(suffix, 'image/jpeg')

        return f"data:{mime_type};base64,{base64_data}"

    except Exception as e:
        print(f"⚠️  이미지 변환 실패 ({image_url}): {e}")
        return None


def generate_html(product, sheets_loader):
    """ProductData와 figma_continuous_2x 템플릿을 사용하여 HTML 생성"""

    print("🖼️  이미지 다운로드 및 Base64 변환 중...")

    # 1. 메인 이미지 (Product Hero 섹션)
    main_image_base64 = None
    if product.main_image:
        print(f"  - 메인 이미지: {str(product.main_image)[:50]}...")
        main_image_base64 = image_to_base64(sheets_loader, str(product.main_image))

    # 2. 컬러 이미지 (Color Variants 섹션)
    color_images_base64 = []
    for i, color in enumerate(product.colors, 1):
        print(f"  - 컬러 {i} 이미지 ({color.color_name}): {str(color.color_image)[:50]}...")
        base64_img = image_to_base64(sheets_loader, str(color.color_image))
        color_images_base64.append({
            'name': color.color_name,
            'hex': color.color_hex or '#cccccc',
            'image': base64_img
        })

    # 3. 갤러리 이미지 (Lifestyle Gallery 섹션) - 컬러칩 정보 포함
    gallery_images_base64 = {}
    for color_name, images in product.gallery_by_color.items():
        print(f"  - 갤러리 ({color_name}): {len(images)}장")

        # Color Selector에서 해당 컬러의 HEX 값 찾기
        color_hex = '#cccccc'  # 기본값
        for color in product.colors:
            if color.color_name == color_name:
                color_hex = color.color_hex or '#cccccc'
                break

        base64_list = []
        for img_url in images:
            base64_img = image_to_base64(sheets_loader, str(img_url))
            if base64_img:
                base64_list.append(base64_img)
        if base64_list:
            gallery_images_base64[color_name] = {
                'hex': color_hex,
                'images': base64_list
            }

    # 4. 디테일 포인트 이미지 (Material Detail 섹션)
    detail_images_base64 = []
    for i, point in enumerate(product.detail_points, 1):
        print(f"  - 디테일 포인트 {i}: {str(point.detail_image)[:50]}...")
        base64_img = image_to_base64(sheets_loader, str(point.detail_image))
        detail_images_base64.append({
            'image': base64_img,
            'text': point.detail_text
        })

    # 5. 체크포인트 이미지 (Care Instructions 섹션)
    checkpoint_image_base64 = None
    if product.checkpoint:
        print(f"  - 체크포인트: {str(product.checkpoint.checkpoint_image)[:50]}...")
        checkpoint_image_base64 = image_to_base64(sheets_loader, str(product.checkpoint.checkpoint_image))

    print("✅ 이미지 변환 완료!")
    print()

    # HTML 생성
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product.product_name} - {product.product_code}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600&display=swap">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-weight: 300;
            background-color: #f5f5f5;
            padding: 20px;
        }}

        .info {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .info h1 {{
            margin: 0 0 10px 0;
            color: #333;
        }}

        .info p {{
            margin: 5px 0;
            color: #666;
        }}

        .canvas-wrapper {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow-x: auto;
        }}

        .canvas {{
            margin: 0 auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
            background: white;
        }}

        .section {{
            position: relative;
            overflow: hidden;
        }}

        .section img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
    </style>
</head>
<body>
    <div class="info">
        <h1>📦 {product.product_name}</h1>
        <p><strong>제품 코드:</strong> {product.product_code}</p>
        <p><strong>컬러:</strong> {len(product.colors)}개</p>
        <p><strong>갤러리:</strong> {sum(len(data['images']) for data in gallery_images_base64.values())}장</p>
        <p><strong>디테일 포인트:</strong> {len(product.detail_points)}개</p>
    </div>

    <div class="canvas-wrapper">
        <div class="canvas" style="width: 1082px; height: auto; min-height: 24018px;">
"""

    # Section 1: Product Hero (메인 이미지)
    if main_image_base64:
        html += f"""
            <div class="section section--product-hero" style="position: relative; width: 1033px; height: 1849px; margin: 0 auto;">
                <img src="{main_image_base64}" alt="{product.product_name}" style="position: absolute; top: 0; left: 0; width: 100%; height: 1382px; object-fit: cover;">
                <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 70px; background: white; display: flex; align-items: center; justify-content: center; font-size: 48px; font-weight: 600; color: #222;">
                    {product.product_name}
                </div>
            </div>
"""

    # Section 2: Color Variants (컬러 이미지)
    if color_images_base64:
        html += """
            <div class="section section--color-variants" style="position: relative; width: 1082px; margin: 20px auto 0;">
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
"""
        for color_data in color_images_base64:
            html += f"""
                    <div style="display: flex; flex-direction: column; gap: 15px;">
                        <img src="{color_data['image']}" alt="{color_data['name']}" style="width: 100%; height: 470px; object-fit: cover;">
                        <div style="text-align: center; font-size: 36px; font-weight: 300; color: #222;">{color_data['name']}</div>
                    </div>
"""
        html += """
                </div>
            </div>
"""

    # Section 3: Lifestyle Gallery (갤러리) - 컬러칩 추가
    if gallery_images_base64:
        html += """
            <div class="section section--lifestyle-gallery" style="position: relative; width: 1042px; margin: 20px auto 0;">
"""
        for color_name, color_data in gallery_images_base64.items():
            # 컬러 헤더 (컬러칩 + 컬러명)
            html += f"""
                <div style="display: flex; align-items: center; gap: 10px; height: 67px; margin-bottom: 20px;">
                    <div style="width: 42px; height: 42px; background: {color_data['hex']}; border: 2px solid #ddd;"></div>
                    <span style="font-size: 40px; font-weight: 400;">{color_name}</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 104px;">
"""
            # 갤러리 이미지들
            for img_base64 in color_data['images']:
                html += f"""
                    <img src="{img_base64}" alt="{color_name}" style="width: 100%; height: 1394px; object-fit: cover;">
"""
            html += """
                </div>
"""
        html += """
            </div>
"""

    # Section 4: Material Detail (디테일 포인트)
    if detail_images_base64:
        html += """
            <div class="section section--material-detail" style="position: relative; width: 1042px; margin: 20px auto 0;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                    <span style="font-size: 40px; font-weight: 400;">Detail</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 161px;">
"""
        for detail in detail_images_base64:
            html += f"""
                    <div style="display: flex; flex-direction: column; gap: 29px;">
                        <img src="{detail['image']}" alt="디테일" style="width: 100%; height: 788px; object-fit: cover;">
                        <div style="text-align: center; font-size: 36px; font-weight: 300; color: #222;">{detail['text']}</div>
                    </div>
"""
        html += """
                </div>
            </div>
"""

    # Section 5: Color Selector
    if product.colors:
        html += """
            <div class="section section--color-selector" style="position: relative; width: 1044px; margin: 20px auto 0;">
                <div style="font-size: 36px; font-weight: 400; margin-bottom: 20px;">Color</div>
                <div style="display: flex; gap: 60px; align-items: center;">
"""
        for color in product.colors:
            html += f"""
                    <div style="display: flex; gap: 10px; align-items: center;">
                        <div style="width: 26px; height: 26px; background: {color.color_hex or '#cccccc'}; border: 2px solid #ddd;"></div>
                        <span style="font-size: 24px; font-weight: 300;">{color.color_name}</span>
                    </div>
"""
        html += """
                </div>
            </div>
"""

    # Section 6: Product Info (Fabric + Care)
    html += f"""
            <div class="section section--product-info" style="position: relative; width: 1044px; margin: 20px auto 0;">
                <div style="font-size: 40px; font-weight: 400; margin-bottom: 46px;">Fabric</div>
                <div style="font-size: 26px; font-weight: 300; color: #222; margin-bottom: 20px;">{product.fabric_info.fabric_composition or 'N/A'}</div>

                <div style="display: flex; gap: 120px; align-items: flex-start; margin-top: 46px;">
                    <div style="font-size: 40px; font-weight: 400; width: 100px;">Care</div>
                    <div style="font-size: 26px; font-weight: 300; color: #666; line-height: 1.6; flex: 1;">
                        {product.fabric_info.fabric_care or 'N/A'}
                    </div>
                </div>
            </div>
"""

    # Section 7: Care Instructions (체크포인트)
    if product.checkpoint and checkpoint_image_base64:
        html += f"""
            <div class="section section--care-instructions" style="position: relative; width: 1044px; margin: 20px auto 0;">
                <div style="display: flex; gap: 120px; align-items: flex-start;">
                    <div style="font-size: 36px; font-weight: 400; line-height: 1.2; width: 100px;">Check<br/>Point</div>
                    <div style="display: flex; gap: 13px; align-items: center;">
                        <img src="{checkpoint_image_base64}" alt="주의사항" style="width: 294px; height: 294px; object-fit: cover;">
                        <div style="font-size: 26px; font-weight: 300; color: #666; line-height: 1.6; flex: 1;">
                            {product.checkpoint.checkpoint_text}
                        </div>
                    </div>
                </div>
            </div>
"""

    # Section 8: Model Info
    if product.model_info:
        html += """
            <div class="section section--model-info" style="position: relative; width: 1044px; margin: 20px auto 0;">
                <div style="font-size: 36px; font-weight: 400; margin-bottom: 20px;">Model</div>
                <div style="display: flex; gap: 42px;">
"""
        for model in product.model_info:
            html += f"""
                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <div style="background: #ddd; width: 264px; height: 322px; display: flex; align-items: center; justify-content: center; color: #666;">
                            모델 이미지
                        </div>
                        <div style="text-align: center; font-size: 26px; font-weight: 300; color: #666;">{model.model_measurements} / {model.model_size}</div>
                    </div>
"""
        html += """
                </div>
            </div>
"""

    # Section 9: Size Chart
    if product.size_info.top or product.size_info.bottom:
        html += """
            <div class="section section--size-chart" style="position: relative; width: 1044px; margin: 20px auto 0;">
                <div style="font-size: 36px; font-weight: 400; margin-bottom: 20px;">Size Information <span style="font-size: 26px; font-weight: 300; color: #666;">(cm)</span></div>
"""

        # 상의 사이즈 테이블
        if product.size_info.top:
            html += """
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <thead style="background: #f0f0f0;">
                        <tr>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">사이즈</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">어깨</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">가슴</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">소매</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">총장</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for size in product.size_info.top:
                html += f"""
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.size_name}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.shoulder}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.chest}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.sleeve}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.length}</td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
"""

        # 하의 사이즈 테이블
        if product.size_info.bottom:
            html += """
                <table style="width: 100%; border-collapse: collapse;">
                    <thead style="background: #f0f0f0;">
                        <tr>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">사이즈</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">허리</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">힙</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">허벅지</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">밑단</th>
                            <th style="padding: 10px; border: 1px solid #ddd; font-size: 24px; font-weight: 400;">밑위</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for size in product.size_info.bottom:
                html += f"""
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.size_name}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.waist}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.hip}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.thigh}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.hem}</td>
                            <td style="padding: 10px; border: 1px solid #ddd; text-align: center; font-size: 22px; font-weight: 300;">{size.rise}</td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
"""
        html += """
            </div>
"""

    # Footer
    html += """
        </div>
    </div>

    <div class="info" style="margin-top: 20px;">
        <p style="text-align: center; color: #999;">
            이 페이지는 Google Sheets 데이터로부터 자동 생성되었습니다.<br>
            © 2025 pb_pb2_new_page Project
        </p>
    </div>
</body>
</html>
"""

    return html


def main():
    # 1. 환경변수 또는 기본값 설정
    service_account_file = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        str(project_root / "service-account.json")
    )
    sheet_id = os.getenv(
        "GOOGLE_SHEET_ID",
        "1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk"
    )

    # 2. 설정 검증
    if not Path(service_account_file).exists():
        print(f"❌ Service Account 파일을 찾을 수 없습니다: {service_account_file}")
        sys.exit(1)

    print("=" * 60)
    print("🎨 Figma Continuous 2x 템플릿 기반 HTML 페이지 생성")
    print("=" * 60)
    print(f"Service Account: {service_account_file}")
    print(f"Sheet ID: {sheet_id}")
    print()

    # 3. SheetsLoader 초기화
    try:
        loader = SheetsLoader(Path(service_account_file))
        print("✅ SheetsLoader 초기화 완료")
    except Exception as e:
        print(f"❌ SheetsLoader 초기화 실패: {e}")
        sys.exit(1)

    # 4. 데이터 로드 (2번 행)
    print("\n📊 데이터 로딩 중...")
    try:
        row = loader.load_row(sheet_id, 2)
        print(f"✅ 데이터 로드 완료: {len(row)}개 컬럼")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        sys.exit(1)

    # 5. ProductData 변환 (색상 추출 활성화)
    print("\n🔄 ProductData 변환 중...")
    try:
        builder = ProductDataBuilder(
            enable_color_extraction=True,
            sheets_loader=loader
        )
        product = builder.build_product_data(row)
        print(f"✅ 변환 완료: {product.product_code}")
        print(f"  - 컬러: {len(product.colors)}개")
        print(f"  - 갤러리: {sum(len(imgs) for imgs in product.gallery_by_color.values())}장")
        print(f"  - 디테일 포인트: {len(product.detail_points)}개")
    except Exception as e:
        print(f"❌ 변환 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 6. HTML 생성
    print("\n🎨 HTML 생성 중...")
    try:
        html_content = generate_html(product, loader)

        # output 폴더 생성
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)

        # HTML 파일 저장
        output_file = output_dir / f"{product.product_code}_figma.html"
        output_file.write_text(html_content, encoding="utf-8")

        print(f"\n✅ HTML 생성 완료: {output_file}")
        print()
        print("=" * 60)
        print("🎉 Figma Continuous 2x 템플릿 기반 HTML 생성 완료!")
        print("=" * 60)
        print()
        print("브라우저에서 확인:")
        print(f"  open {output_file}")
        print()

    except Exception as e:
        print(f"❌ HTML 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
