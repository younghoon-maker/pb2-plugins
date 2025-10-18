"""
여러 제품의 Figma 템플릿 기반 Editable HTML V4 일괄 생성

V4 개선사항:
1. JPG 익스포트 좌표계 수정 (CENTER → TOP-LEFT)
2. localStorage 버전 체크 (디폴트 값 보장)
3. 날짜별 폴더 구조 (Dana&Peta 스타일)

폴더 구조:
  output/
  ├── {YYYYMMDD}/
  │   ├── editable/
  │   │   ├── VD25FPT003_editable_v4.html
  │   │   └── ...
  │   └── export/  (서버가 자동 생성)

실행 방법:
  # 특정 행 범위 지정 (예: 2번 행부터 5번 행까지)
  python scripts/generate_batch.py --start 2 --end 5

  # 모든 행 자동 탐색 (제품 코드가 있는 행만)
  python scripts/generate_batch.py --all

  # 특정 행들만 지정 (쉼표로 구분)
  python scripts/generate_batch.py --rows 2,5,10

환경변수 설정 (선택):
  export GOOGLE_SERVICE_ACCOUNT_FILE=/path/to/service-account.json
  export GOOGLE_SHEET_ID=your-sheet-id
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.sheets_loader.loader import SheetsLoader
from src.sheets_loader.product_builder import ProductDataBuilder

# generate_editable_html 함수 임포트
import importlib.util
spec = importlib.util.spec_from_file_location(
    "generate_editable_html",
    project_root / "scripts" / "generate_editable_html.py"
)
generate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_module)
generate_editable_html = generate_module.generate_editable_html


def get_today_folder(output_dir: Path) -> Tuple[Path, Path]:
    """
    오늘 날짜 폴더 생성 및 반환

    Returns:
        (editable_dir, export_dir) 튜플
    """
    today = datetime.now().strftime("%Y%m%d")
    date_dir = output_dir / today

    editable_dir = date_dir / "editable"
    export_dir = date_dir / "export"

    # 폴더 생성
    editable_dir.mkdir(exist_ok=True, parents=True)
    export_dir.mkdir(exist_ok=True, parents=True)

    return editable_dir, export_dir


def get_all_product_rows(loader: SheetsLoader, sheet_id: str) -> List[int]:
    """
    시트에서 제품 코드가 있는 모든 행 번호 찾기

    Args:
        loader: SheetsLoader 인스턴스
        sheet_id: Google Sheets ID

    Returns:
        제품 코드가 있는 행 번호 리스트 (2부터 시작)
    """
    print("📊 시트 전체 스캔 중...")

    # 전체 시트 데이터 로드 (A열만 - 제품 코드)
    try:
        range_name = "A:A"  # A열 전체
        values = loader.service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_name
        ).execute()

        rows_data = values.get('values', [])
        product_rows = []

        for idx, row in enumerate(rows_data[1:], start=2):  # 헤더 제외, 2번 행부터
            if row and row[0] and str(row[0]).strip():  # 제품 코드가 있으면
                product_rows.append(idx)

        print(f"✅ 총 {len(product_rows)}개 제품 발견")
        return product_rows

    except Exception as e:
        print(f"❌ 시트 스캔 실패: {e}")
        return []


def generate_product_editable_html(
    loader: SheetsLoader,
    builder: ProductDataBuilder,
    sheet_id: str,
    row_number: int,
    editable_dir: Path
) -> Optional[Dict]:
    """
    단일 제품 Editable HTML V4 생성

    Returns:
        성공 시 제품 정보 딕셔너리, 실패 시 None
    """
    try:
        # 데이터 로드
        row = loader.load_row(sheet_id, row_number)

        # ProductData 변환
        product = builder.build_product_data(row)

        # Editable HTML V4 생성
        html_content = generate_editable_html(product, loader)

        # 파일 저장
        output_file = editable_dir / f"{product.product_code}_editable_v4.html"
        output_file.write_text(html_content, encoding="utf-8")

        return {
            'row': row_number,
            'code': product.product_code,
            'name': product.product_name,
            'file': output_file,
            'size': len(html_content) / 1024 / 1024,  # MB
            'colors': len(product.colors),
            'gallery': sum(
                len(data['images'])
                for data in product.gallery_by_color.values()
                if isinstance(data, dict) and 'images' in data
            ),
        }

    except Exception as e:
        print(f"  ⚠️  Row {row_number} 처리 실패: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="여러 제품의 Editable HTML V4 페이지 일괄 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 2-5번 행 생성
  python scripts/generate_batch.py --start 2 --end 5

  # 모든 제품 생성
  python scripts/generate_batch.py --all

  # 특정 행만 생성
  python scripts/generate_batch.py --rows 2,5,10

폴더 구조:
  output/{YYYYMMDD}/editable/    # 오늘 날짜 폴더에 생성
  output/{YYYYMMDD}/export/      # 서버가 자동 생성 (익스포트용)
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--start', type=int, help='시작 행 번호')
    group.add_argument('--all', action='store_true', help='모든 제품 생성')
    group.add_argument('--rows', type=str, help='특정 행 번호 (쉼표로 구분, 예: 2,5,10)')

    parser.add_argument('--end', type=int, help='종료 행 번호 (--start와 함께 사용)')

    args = parser.parse_args()

    # 환경변수 또는 기본값
    service_account_file = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        str(project_root / "service-account.json")
    )
    sheet_id = os.getenv(
        "GOOGLE_SHEET_ID",
        "1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk"
    )

    # 설정 검증
    if not Path(service_account_file).exists():
        print(f"❌ Service Account 파일을 찾을 수 없습니다: {service_account_file}")
        sys.exit(1)

    print("=" * 60)
    print("🎨 Figma Editable HTML V4 일괄 생성")
    print("=" * 60)
    print(f"Service Account: {service_account_file}")
    print(f"Sheet ID: {sheet_id}")
    print()

    # SheetsLoader 초기화
    try:
        loader = SheetsLoader(Path(service_account_file))
        print("✅ SheetsLoader 초기화 완료")
    except Exception as e:
        print(f"❌ SheetsLoader 초기화 실패: {e}")
        sys.exit(1)

    # ProductDataBuilder 초기화
    builder = ProductDataBuilder(
        enable_color_extraction=False,  # 시트에 이미 HEX 값 존재
        sheets_loader=loader
    )

    # 오늘 날짜 폴더 생성 (현재 작업 디렉토리 기준)
    output_dir = Path(os.getcwd()) / "output"
    editable_dir, export_dir = get_today_folder(output_dir)

    today = datetime.now().strftime("%Y%m%d")
    print(f"📁 출력 폴더: output/{today}/editable/")
    print(f"📁 익스포트 폴더: output/{today}/export/")
    print()

    # 처리할 행 번호 결정
    row_numbers = []

    if args.all:
        row_numbers = get_all_product_rows(loader, sheet_id)
        if not row_numbers:
            print("❌ 제품을 찾을 수 없습니다")
            sys.exit(1)
    elif args.rows:
        row_numbers = [int(r.strip()) for r in args.rows.split(',')]
    elif args.start:
        if args.end:
            row_numbers = list(range(args.start, args.end + 1))
        else:
            row_numbers = [args.start]

    print()
    print(f"📋 처리 대상: {len(row_numbers)}개 행")
    print(f"   행 번호: {row_numbers}")
    print()

    # 일괄 생성
    results = {
        'success': [],
        'failed': []
    }

    for idx, row_num in enumerate(row_numbers, 1):
        print(f"[{idx}/{len(row_numbers)}] Row {row_num} 처리 중...")

        result = generate_product_editable_html(
            loader, builder, sheet_id, row_num, editable_dir
        )

        if result:
            results['success'].append(result)
            print(f"  ✅ {result['code']} - {result['name']}")
            print(f"     파일: {result['file'].name} ({result['size']:.1f} MB)")
        else:
            results['failed'].append(row_num)

    # 최종 요약
    print()
    print("=" * 60)
    print("📊 생성 완료 요약")
    print("=" * 60)
    print(f"✅ 성공: {len(results['success'])}개")
    print(f"❌ 실패: {len(results['failed'])}개")
    print()

    if results['success']:
        print("✅ 생성된 파일:")
        total_size = 0
        for r in results['success']:
            total_size += r['size']
            print(f"   - {r['file'].name}")
            print(f"     {r['colors']}색, 갤러리 {r['gallery']}장, {r['size']:.1f} MB")
        print(f"\n   💾 전체 용량: {total_size:.1f} MB")

    if results['failed']:
        print()
        print("❌ 실패한 행:")
        for row_num in results['failed']:
            print(f"   - Row {row_num}")

    print()
    print(f"📁 출력 폴더: {editable_dir}")
    print(f"📁 익스포트 폴더: {export_dir}")
    print()
    print("💡 다음 단계:")
    print("   1. Flask 서버 시작: python scripts/server.py")
    print("   2. 브라우저에서 열기: http://localhost:5001/")
    print("   3. 파일 선택 → 편집 → Export JPG")
    print()


if __name__ == "__main__":
    main()
