"""
통합 테스트: Google Sheets → ProductData 변환

실행 방법:
  python examples/load_sample.py

환경변수 설정 (선택):
  export GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
  export GOOGLE_SHEET_ID=your-sheet-id
"""

import os
import sys
import json
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.sheets_loader.loader import SheetsLoader
from src.sheets_loader.product_builder import ProductDataBuilder


def main():
    # 1. 환경변수 또는 기본값 설정
    service_account_file = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        str(project_root / "service-account.json")  # 기본 경로
    )
    sheet_id = os.getenv(
        "GOOGLE_SHEET_ID",
        "YOUR_SHEET_ID_HERE"  # 여기에 실제 Sheet ID 입력
    )

    # 2. 설정 검증
    if not Path(service_account_file).exists():
        print(f"❌ Service Account 파일을 찾을 수 없습니다: {service_account_file}")
        print("\n설정 방법:")
        print("  1. Google Cloud Console에서 Service Account JSON 다운로드")
        print("  2. 프로젝트 루트에 service-account.json으로 저장")
        print("  또는 환경변수 설정:")
        print("  export GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json")
        sys.exit(1)

    if sheet_id == "YOUR_SHEET_ID_HERE":
        print("❌ Sheet ID를 설정해주세요")
        print("\n설정 방법:")
        print("  1. 코드 수정: examples/load_sample.py의 sheet_id 변수")
        print("  2. 환경변수: export GOOGLE_SHEET_ID=your-sheet-id")
        sys.exit(1)

    print("=" * 60)
    print("📋 Google Sheets 데이터 로드 테스트")
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

    # 4. 단일 행 로드 테스트 (2번 행)
    print("\n" + "-" * 60)
    print("TEST 1: 단일 행 로드 (2번 행)")
    print("-" * 60)

    try:
        row = loader.load_row(sheet_id, 2)
        print(f"✅ 로드 성공: {len(row)}개 컬럼")

        # 처음 10개 컬럼 샘플 출력
        print("\n📊 처음 10개 컬럼 샘플:")
        for i, value in enumerate(row[:10]):
            print(f"  [{i}] {value[:50] if value else '(empty)'}{'...' if value and len(value) > 50 else ''}")

        if len(row) != 292:
            print(f"\n⚠️  경고: 예상 292개 컬럼, 실제 {len(row)}개 컬럼")
    except Exception as e:
        print(f"❌ 로드 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 5. ProductData 변환 테스트
    print("\n" + "-" * 60)
    print("TEST 2: ProductData 변환 (색상 추출 활성화)")
    print("-" * 60)

    try:
        builder = ProductDataBuilder(
            enable_color_extraction=True, sheets_loader=loader
        )
        product = builder.build_product_data(row)
        print("✅ 변환 성공")

        # 기본 정보 출력
        print(f"\n📦 상품 정보:")
        print(f"  코드: {product.product_code}")
        print(f"  이름: {product.product_name}")
        # HttpUrl을 문자열로 변환
        main_img_str = str(product.main_image) if product.main_image else 'None'
        print(f"  메인 이미지: {main_img_str[:50]}..." if len(main_img_str) > 50 else f"  메인 이미지: {main_img_str}")
        print(f"  색상 개수: {len(product.colors)}")
        print(f"  갤러리 색상 수: {len(product.gallery_by_color)}")
        print(f"  디테일 포인트: {len(product.detail_points)}")
        print(f"  모델 정보: {len(product.model_info)}")

        # 색상 정보
        if product.colors:
            print(f"\n🎨 색상 목록:")
            for i, color in enumerate(product.colors, 1):
                print(f"  {i}. {color.color_name} ({color.color_hex})")

        # 사이즈 정보
        if product.size_info.top:
            print(f"\n👕 상의 사이즈: {len(product.size_info.top)}개")
            for size in product.size_info.top:
                print(f"  - {size.size_name}: 어깨 {size.shoulder}cm, 가슴 {size.chest}cm, 소매 {size.sleeve}cm, 총장 {size.length}cm")

        if product.size_info.bottom:
            print(f"\n👖 하의 사이즈: {len(product.size_info.bottom)}개")
            for size in product.size_info.bottom:
                print(f"  - {size.size_name}: 허리 {size.waist}cm, 힙 {size.hip}cm, 허벅지 {size.thigh}cm")

        # JSON 출력 (선택)
        print("\n" + "-" * 60)
        print("📄 JSON 출력 (전체 데이터)")
        print("-" * 60)
        # mode='json'으로 HttpUrl을 문자열로 자동 변환
        print(json.dumps(product.model_dump(mode='json'), indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ 변환 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 6. 하이퍼링크 추출 테스트 (선택)
    print("\n" + "-" * 60)
    print("TEST 3: 하이퍼링크 추출 (선택)")
    print("-" * 60)

    try:
        hyperlinks = loader.extract_hyperlinks(sheet_id, 2)
        print(f"✅ 추출 성공: {len(hyperlinks)}개 컬럼")

        # 하이퍼링크가 있는 컬럼만 출력
        hyperlink_count = sum(1 for h in hyperlinks if h)
        print(f"📎 하이퍼링크 발견: {hyperlink_count}개")

        if hyperlink_count > 0:
            print("\n처음 5개 하이퍼링크:")
            count = 0
            for i, link in enumerate(hyperlinks):
                if link:
                    print(f"  [{i}] {link}")
                    count += 1
                    if count >= 5:
                        break
    except Exception as e:
        print(f"⚠️  하이퍼링크 추출 실패: {e}")
        print("   (선택 기능이므로 계속 진행)")

    # 7. 최종 결과
    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료")
    print("=" * 60)
    print("\n다음 단계:")
    print("  1. 데이터 검증: 위 출력 내용이 예상과 일치하는지 확인")
    print("  2. 추가 행 테스트: 다른 행 번호로 테스트")
    print("  3. 문제 발견 시: 이슈 리포트 또는 코드 수정")
    print("  4. 정상 동작 확인 후: /alfred:3-sync 실행")


if __name__ == "__main__":
    main()
