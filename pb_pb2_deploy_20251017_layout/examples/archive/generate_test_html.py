"""
HTML 테스트 페이지 생성

실행 방법:
  python examples/generate_test_html.py

환경변수 설정 (선택):
  export GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
  export GOOGLE_SHEET_ID=your-sheet-id
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.sheets_loader.loader import SheetsLoader
from src.sheets_loader.product_builder import ProductDataBuilder


def generate_html(product):
    """ProductData를 HTML로 변환"""
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product.product_name} - 상품 상세</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            padding: 20px 0;
            background: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .color-swatch {{
            display: inline-block;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 3px solid #ddd;
            margin-right: 15px;
            vertical-align: middle;
        }}
        .color-item {{
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .gallery-img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .detail-point {{
            margin: 20px 0;
            padding: 20px;
            background: #e9ecef;
            border-radius: 8px;
        }}
        .detail-img {{
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 8px;
        }}
        .section-title {{
            font-size: 24px;
            font-weight: bold;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #dee2e6;
        }}
        .badge {{
            font-size: 14px;
            padding: 8px 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 헤더 -->
        <div class="text-center mb-5">
            <h1 class="display-4">{product.product_name}</h1>
            <p class="lead text-muted">제품 코드: <span class="badge bg-primary">{product.product_code}</span></p>
        </div>

        <!-- 메인 이미지 -->
        <div class="row mb-5">
            <div class="col-12">
                <h2 class="section-title">메인 이미지</h2>
                <img src="{product.main_image}" alt="{product.product_name}" class="img-fluid rounded">
            </div>
        </div>

        <!-- 색상 정보 -->
        <div class="mb-5">
            <h2 class="section-title">색상 옵션 ({len(product.colors)}개)</h2>
            <div class="row">
"""

    # 색상 목록
    for i, color in enumerate(product.colors, 1):
        html += f"""
                <div class="col-md-6 col-lg-3">
                    <div class="color-item">
                        <div class="d-flex align-items-center mb-2">
                            <div class="color-swatch" style="background-color: {color.color_hex or '#cccccc'};"></div>
                            <div>
                                <strong>{color.color_name}</strong><br>
                                <small class="text-muted">{color.color_hex or 'N/A'}</small>
                            </div>
                        </div>
                        <img src="{color.color_image}" alt="{color.color_name}" class="img-fluid rounded">
                    </div>
                </div>
"""

    html += """
            </div>
        </div>
"""

    # 갤러리
    if product.gallery_by_color:
        html += """
        <div class="mb-5">
            <h2 class="section-title">갤러리</h2>
"""
        for color_name, images in product.gallery_by_color.items():
            html += f"""
            <h3 class="h5 mt-4 mb-3">{color_name} ({len(images)}장)</h3>
            <div class="row">
"""
            for img_url in images:
                html += f"""
                <div class="col-md-4 col-lg-3">
                    <img src="{img_url}" alt="{color_name}" class="gallery-img">
                </div>
"""
            html += """
            </div>
"""
        html += """
        </div>
"""

    # 디테일 포인트
    if product.detail_points:
        html += f"""
        <div class="mb-5">
            <h2 class="section-title">디테일 포인트 ({len(product.detail_points)}개)</h2>
"""
        for i, point in enumerate(product.detail_points, 1):
            html += f"""
            <div class="detail-point">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <img src="{point.detail_image}" alt="디테일 {i}" class="detail-img">
                    </div>
                    <div class="col-md-6">
                        <h3 class="h5">POINT {i}</h3>
                        <p class="lead">{point.detail_text}</p>
                    </div>
                </div>
            </div>
"""
        html += """
        </div>
"""

    # 소재 정보
    html += f"""
        <div class="mb-5">
            <h2 class="section-title">소재 정보</h2>
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">소재 구성</h5>
                    <p class="card-text">{product.fabric_info.fabric_composition or 'N/A'}</p>

                    <h5 class="card-title mt-4">세탁 방법</h5>
                    <p class="card-text">{product.fabric_info.fabric_care or 'N/A'}</p>
                </div>
            </div>
        </div>
"""

    # 모델 정보
    if product.model_info:
        html += f"""
        <div class="mb-5">
            <h2 class="section-title">모델 정보</h2>
            <div class="row">
"""
        for i, model in enumerate(product.model_info, 1):
            html += f"""
                <div class="col-md-6">
                    <div class="alert alert-info">
                        <strong>모델 {i}</strong><br>
                        사이즈: {model.model_size}<br>
                        신장: {model.model_measurements}
                    </div>
                </div>
"""
        html += """
            </div>
        </div>
"""

    # 사이즈 정보
    if product.size_info.top or product.size_info.bottom:
        html += """
        <div class="mb-5">
            <h2 class="section-title">사이즈 정보</h2>
"""

        # 상의 사이즈
        if product.size_info.top:
            html += """
            <h3 class="h5 mb-3">상의</h3>
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th>사이즈</th>
                            <th>어깨</th>
                            <th>가슴</th>
                            <th>소매</th>
                            <th>총장</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for size in product.size_info.top:
                html += f"""
                        <tr>
                            <td><strong>{size.size_name}</strong></td>
                            <td>{size.shoulder}cm</td>
                            <td>{size.chest}cm</td>
                            <td>{size.sleeve}cm</td>
                            <td>{size.length}cm</td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
            </div>
"""

        # 하의 사이즈
        if product.size_info.bottom:
            html += """
            <h3 class="h5 mb-3 mt-4">하의</h3>
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th>사이즈</th>
                            <th>허리</th>
                            <th>힙</th>
                            <th>허벅지</th>
                            <th>밑단</th>
                            <th>밑위</th>
                        </tr>
                    </thead>
                    <tbody>
"""
            for size in product.size_info.bottom:
                html += f"""
                        <tr>
                            <td><strong>{size.size_name}</strong></td>
                            <td>{size.waist}cm</td>
                            <td>{size.hip}cm</td>
                            <td>{size.thigh}cm</td>
                            <td>{size.hem}cm</td>
                            <td>{size.rise}cm</td>
                        </tr>
"""
            html += """
                    </tbody>
                </table>
            </div>
"""

        html += """
        </div>
"""

    # 체크포인트
    if product.checkpoint:
        html += f"""
        <div class="mb-5">
            <h2 class="section-title">주의사항</h2>
            <div class="alert alert-warning">
                <div class="row align-items-center">
                    <div class="col-md-3">
                        <img src="{product.checkpoint.checkpoint_image}" alt="주의사항" class="img-fluid rounded">
                    </div>
                    <div class="col-md-9">
                        <p class="mb-0">{product.checkpoint.checkpoint_text}</p>
                    </div>
                </div>
            </div>
        </div>
"""

    # 푸터
    html += """
        <div class="text-center mt-5 pt-4 border-top">
            <p class="text-muted">
                <small>이 페이지는 Google Sheets 데이터로부터 자동 생성되었습니다.</small><br>
                <small>© 2025 pb_pb2_new_page Project</small>
            </p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
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
    print("📄 HTML 테스트 페이지 생성")
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
    print("\n데이터 로딩 중...")
    try:
        row = loader.load_row(sheet_id, 2)
        print(f"✅ 데이터 로드 완료: {len(row)}개 컬럼")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        sys.exit(1)

    # 5. ProductData 변환 (색상 추출 활성화)
    print("\nProductData 변환 중...")
    try:
        builder = ProductDataBuilder(
            enable_color_extraction=True,
            sheets_loader=loader
        )
        product = builder.build_product_data(row)
        print(f"✅ 변환 완료: {product.product_code}")
    except Exception as e:
        print(f"❌ 변환 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 6. HTML 생성
    print("\nHTML 생성 중...")
    try:
        html_content = generate_html(product)

        # output 폴더 생성
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)

        # HTML 파일 저장
        output_file = output_dir / f"{product.product_code}_test.html"
        output_file.write_text(html_content, encoding="utf-8")

        print(f"✅ HTML 생성 완료: {output_file}")
        print()
        print("=" * 60)
        print("🎉 테스트 페이지 생성 완료!")
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
