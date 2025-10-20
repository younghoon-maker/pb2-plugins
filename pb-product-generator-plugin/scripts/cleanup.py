#!/usr/bin/env python3
"""
PB Product Generator - Output Cleanup Script
자동으로 오래된 output 파일들을 정리합니다.
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Tuple


def get_dir_size(path: Path) -> int:
    """디렉토리 크기 계산 (bytes)"""
    total = 0
    for entry in path.rglob('*'):
        if entry.is_file():
            total += entry.stat().st_size
    return total


def format_size(bytes_size: int) -> str:
    """바이트를 읽기 쉬운 형식으로 변환"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def get_dated_folders(output_dir: Path) -> List[Tuple[Path, datetime]]:
    """날짜별 폴더 목록 가져오기 (YYYYMMDD 형식)"""
    folders = []
    for item in output_dir.iterdir():
        if item.is_dir() and item.name.isdigit() and len(item.name) == 8:
            try:
                date = datetime.strptime(item.name, "%Y%m%d")
                folders.append((item, date))
            except ValueError:
                continue
    return sorted(folders, key=lambda x: x[1])


def get_old_html_files(output_dir: Path, days: int) -> List[Tuple[Path, datetime]]:
    """루트의 오래된 HTML 파일 목록"""
    cutoff = datetime.now() - timedelta(days=days)
    old_files = []

    for item in output_dir.iterdir():
        if item.is_file() and item.suffix in ['.html', '.htm']:
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff:
                old_files.append((item, mtime))

    return sorted(old_files, key=lambda x: x[1])


def cleanup_by_age(output_dir: Path, days: int, dry_run: bool = False) -> Tuple[int, int]:
    """오래된 파일/폴더 삭제"""
    cutoff = datetime.now() - timedelta(days=days)
    deleted_count = 0
    freed_bytes = 0

    print(f"\n🗑️  오래된 파일 정리 (기준: {days}일 이전)\n")
    print(f"   기준 날짜: {cutoff.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 날짜별 폴더 삭제
    folders = get_dated_folders(output_dir)
    for folder, date in folders:
        if date < cutoff:
            size = get_dir_size(folder)
            if dry_run:
                print(f"   [DRY RUN] 삭제 예정: {folder.name}/ ({format_size(size)})")
            else:
                print(f"   삭제 중: {folder.name}/ ({format_size(size)})")
                shutil.rmtree(folder)
            deleted_count += 1
            freed_bytes += size

    # 루트의 오래된 HTML 파일 삭제
    old_files = get_old_html_files(output_dir, days)
    for file_path, mtime in old_files:
        size = file_path.stat().st_size
        if dry_run:
            print(f"   [DRY RUN] 삭제 예정: {file_path.name} ({format_size(size)})")
        else:
            print(f"   삭제 중: {file_path.name} ({format_size(size)})")
            file_path.unlink()
        deleted_count += 1
        freed_bytes += size

    return deleted_count, freed_bytes


def cleanup_by_size(output_dir: Path, max_size_mb: int, dry_run: bool = False) -> Tuple[int, int]:
    """크기 제한 기반 정리 (오래된 것부터 삭제)"""
    max_bytes = max_size_mb * 1024 * 1024
    current_size = get_dir_size(output_dir)

    if current_size <= max_bytes:
        print(f"\n✅ 현재 크기 {format_size(current_size)} ≤ 최대 크기 {format_size(max_bytes)}")
        print("   정리 불필요\n")
        return 0, 0

    print(f"\n🗑️  크기 기반 정리 (최대: {format_size(max_bytes)})\n")
    print(f"   현재 크기: {format_size(current_size)}")
    print(f"   초과 크기: {format_size(current_size - max_bytes)}\n")

    deleted_count = 0
    freed_bytes = 0

    # 오래된 날짜 폴더부터 삭제
    folders = get_dated_folders(output_dir)
    for folder, date in folders:
        if current_size - freed_bytes <= max_bytes:
            break

        size = get_dir_size(folder)
        if dry_run:
            print(f"   [DRY RUN] 삭제 예정: {folder.name}/ ({format_size(size)})")
        else:
            print(f"   삭제 중: {folder.name}/ ({format_size(size)})")
            shutil.rmtree(folder)
        deleted_count += 1
        freed_bytes += size

    # 아직 초과하면 루트의 오래된 HTML도 삭제
    if current_size - freed_bytes > max_bytes:
        old_files = get_old_html_files(output_dir, days=0)  # 모든 파일
        for file_path, mtime in old_files:
            if current_size - freed_bytes <= max_bytes:
                break

            size = file_path.stat().st_size
            if dry_run:
                print(f"   [DRY RUN] 삭제 예정: {file_path.name} ({format_size(size)})")
            else:
                print(f"   삭제 중: {file_path.name} ({format_size(size)})")
                file_path.unlink()
            deleted_count += 1
            freed_bytes += size

    return deleted_count, freed_bytes


def show_stats(output_dir: Path):
    """output 폴더 통계 표시"""
    if not output_dir.exists():
        print(f"❌ Output 폴더가 존재하지 않습니다: {output_dir}")
        return

    total_size = get_dir_size(output_dir)
    folders = get_dated_folders(output_dir)
    html_files = list(output_dir.glob('*.html'))

    print("\n" + "=" * 60)
    print("📊 Output 폴더 통계")
    print("=" * 60)
    print(f"\n📁 위치: {output_dir}")
    print(f"💾 전체 크기: {format_size(total_size)}")
    print(f"📅 날짜별 폴더: {len(folders)}개")
    print(f"📄 루트 HTML 파일: {len(html_files)}개\n")

    if folders:
        print("📅 날짜별 폴더 상세:")
        for folder, date in folders:
            size = get_dir_size(folder)
            age_days = (datetime.now() - date).days
            print(f"   {folder.name}/ - {format_size(size):>10} ({age_days}일 전)")

    if html_files:
        print("\n📄 루트 HTML 파일:")
        for file_path in html_files:
            size = file_path.stat().st_size
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            age_days = (datetime.now() - mtime).days
            print(f"   {file_path.name} - {format_size(size):>10} ({age_days}일 전)")

    print("\n" + "=" * 60 + "\n")


def cleanup_all(output_dir: Path, dry_run: bool = False) -> Tuple[int, int]:
    """전체 삭제 (output 폴더 전체)"""
    if not output_dir.exists():
        print(f"❌ Output 폴더가 존재하지 않습니다: {output_dir}")
        return 0, 0

    size = get_dir_size(output_dir)
    count = sum(1 for _ in output_dir.rglob('*') if _.is_file())

    if dry_run:
        print(f"\n[DRY RUN] 전체 삭제 예정: {count}개 파일, {format_size(size)}\n")
        return count, size

    print(f"\n⚠️  경고: output 폴더 전체를 삭제합니다!")
    print(f"   파일 수: {count}개")
    print(f"   크기: {format_size(size)}\n")

    response = input("정말 삭제하시겠습니까? (yes/no): ")
    if response.lower() != 'yes':
        print("\n취소되었습니다.\n")
        return 0, 0

    shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True)
    print(f"\n✅ 삭제 완료: {count}개 파일, {format_size(size)} 확보\n")

    return count, size


def main():
    parser = argparse.ArgumentParser(
        description="PB Product Generator Output Cleanup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s --stats                    # 통계만 표시
  %(prog)s --days 7                   # 7일 이상 오래된 파일 삭제
  %(prog)s --days 7 --dry-run         # 삭제 예정 목록만 표시
  %(prog)s --max-size 500             # 500MB로 크기 제한
  %(prog)s --all                      # 전체 삭제 (확인 필요)
  %(prog)s --all --dry-run            # 전체 삭제 시뮬레이션
        """
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Output 디렉토리 경로 (기본: output/)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='통계만 표시하고 종료'
    )
    parser.add_argument(
        '--days',
        type=int,
        help='N일 이상 오래된 파일 삭제'
    )
    parser.add_argument(
        '--max-size',
        type=int,
        help='최대 크기 (MB) - 초과 시 오래된 것부터 삭제'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='전체 삭제 (확인 필요)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 삭제하지 않고 시뮬레이션만 실행'
    )

    args = parser.parse_args()
    output_dir = Path(args.output_dir)

    print("\n" + "🚀 PB Product Generator - Output Cleanup")
    print("=" * 60)

    # 통계 표시
    if args.stats:
        show_stats(output_dir)
        return

    # 전체 삭제
    if args.all:
        count, size = cleanup_all(output_dir, dry_run=args.dry_run)
        return

    # 날짜 기반 정리
    if args.days:
        count, size = cleanup_by_age(output_dir, args.days, dry_run=args.dry_run)
        if count > 0:
            print(f"\n✅ 정리 완료: {count}개 항목, {format_size(size)} 확보\n")
        else:
            print(f"\n✅ 정리할 파일이 없습니다.\n")
        return

    # 크기 기반 정리
    if args.max_size:
        count, size = cleanup_by_size(output_dir, args.max_size, dry_run=args.dry_run)
        if count > 0:
            print(f"\n✅ 정리 완료: {count}개 항목, {format_size(size)} 확보\n")
        return

    # 옵션 없으면 도움말 표시
    parser.print_help()
    print("\n💡 통계를 보려면: python3 cleanup.py --stats\n")


if __name__ == "__main__":
    main()
