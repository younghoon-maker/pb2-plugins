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


def show_stats(output_dir: Path, cache_dir: Path):
    """output 폴더 및 캐시 통계 표시"""
    output_exists = output_dir.exists()
    cache_exists = cache_dir.exists()

    if not output_exists and not cache_exists:
        print(f"❌ Output 및 캐시 폴더가 존재하지 않습니다.")
        return

    print("\n" + "=" * 60)
    print("📊 스토리지 통계")
    print("=" * 60)

    total_size = 0

    # Output 폴더 통계
    if output_exists:
        output_size = get_dir_size(output_dir)
        total_size += output_size
        folders = get_dated_folders(output_dir)
        html_files = list(output_dir.glob('*.html'))

        print(f"\n📁 Output 폴더: {output_dir}")
        print(f"💾 크기: {format_size(output_size)}")
        print(f"📅 날짜별 폴더: {len(folders)}개")
        print(f"📄 루트 HTML 파일: {len(html_files)}개")

        if folders:
            print("\n📅 날짜별 폴더 상세:")
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

    # Cache 폴더 통계
    if cache_exists:
        cache_size = get_dir_size(cache_dir)
        total_size += cache_size
        cache_files = list(cache_dir.glob('*.json'))

        print(f"\n📦 캐시 폴더: {cache_dir}")
        print(f"💾 크기: {format_size(cache_size)}")
        print(f"📄 캐시 파일: {len(cache_files)}개")

        if cache_files and len(cache_files) <= 10:
            print("\n📄 캐시 파일:")
            for file_path in cache_files:
                size = file_path.stat().st_size
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                age_days = (datetime.now() - mtime).days
                print(f"   {file_path.name} - {format_size(size):>10} ({age_days}일 전)")
        elif cache_files:
            print(f"\n   (총 {len(cache_files)}개 파일 - 목록 생략)")

    print(f"\n💾 전체 크기: {format_size(total_size)}")
    print("\n" + "=" * 60 + "\n")


def cleanup_cache(cache_dir: Path, days: int = 0, dry_run: bool = False) -> Tuple[int, int]:
    """캐시 파일 정리 (.cache/figma)

    Args:
        cache_dir: 캐시 디렉토리 경로
        days: N일 이상 오래된 파일 삭제 (0이면 전체)
        dry_run: 시뮬레이션 모드

    Returns:
        Tuple[int, int]: (삭제된 파일 수, 확보된 바이트)
    """
    if not cache_dir.exists():
        print(f"ℹ️  캐시 디렉토리가 존재하지 않습니다: {cache_dir}")
        return 0, 0

    deleted_count = 0
    freed_bytes = 0

    print(f"\n🗑️  캐시 정리 ({cache_dir})\n")

    if days > 0:
        cutoff = datetime.now() - timedelta(days=days)
        print(f"   기준 날짜: {cutoff.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # JSON 캐시 파일 정리
    cache_files = list(cache_dir.glob('*.json'))

    for file_path in cache_files:
        # 날짜 기준이 있으면 체크
        if days > 0:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime >= cutoff:
                continue

        size = file_path.stat().st_size
        if dry_run:
            print(f"   [DRY RUN] 삭제 예정: {file_path.name} ({format_size(size)})")
        else:
            print(f"   삭제 중: {file_path.name} ({format_size(size)})")
            file_path.unlink()
        deleted_count += 1
        freed_bytes += size

    return deleted_count, freed_bytes


def cleanup_all(output_dir: Path, cache_dir: Path, dry_run: bool = False) -> Tuple[int, int]:
    """전체 삭제 (output 폴더 + 캐시 전체)"""
    total_count = 0
    total_size = 0

    # Output 폴더
    if output_dir.exists():
        output_size = get_dir_size(output_dir)
        output_count = sum(1 for _ in output_dir.rglob('*') if _.is_file())
        total_count += output_count
        total_size += output_size

    # Cache 폴더
    if cache_dir.exists():
        cache_size = get_dir_size(cache_dir)
        cache_count = sum(1 for _ in cache_dir.rglob('*') if _.is_file())
        total_count += cache_count
        total_size += cache_size

    if total_count == 0:
        print(f"ℹ️  삭제할 파일이 없습니다.\n")
        return 0, 0

    if dry_run:
        print(f"\n[DRY RUN] 전체 삭제 예정: {total_count}개 파일, {format_size(total_size)}\n")
        if output_dir.exists():
            print(f"   Output: {output_count}개 파일, {format_size(output_size)}")
        if cache_dir.exists():
            print(f"   Cache: {cache_count}개 파일, {format_size(cache_size)}")
        print()
        return total_count, total_size

    print(f"\n⚠️  경고: output 및 캐시 폴더 전체를 삭제합니다!")
    print(f"   총 파일 수: {total_count}개")
    print(f"   총 크기: {format_size(total_size)}\n")
    if output_dir.exists():
        print(f"   Output: {output_count}개 파일, {format_size(output_size)}")
    if cache_dir.exists():
        print(f"   Cache: {cache_count}개 파일, {format_size(cache_size)}")
    print()

    response = input("정말 삭제하시겠습니까? (yes/no): ")
    if response.lower() != 'yes':
        print("\n취소되었습니다.\n")
        return 0, 0

    deleted_count = 0
    deleted_size = 0

    # Output 삭제
    if output_dir.exists():
        shutil.rmtree(output_dir)
        output_dir.mkdir(exist_ok=True)
        deleted_count += output_count
        deleted_size += output_size
        print(f"✅ Output 삭제 완료: {output_count}개 파일")

    # Cache 삭제
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        cache_dir.mkdir(exist_ok=True)
        deleted_count += cache_count
        deleted_size += cache_size
        print(f"✅ Cache 삭제 완료: {cache_count}개 파일")

    print(f"\n✅ 전체 삭제 완료: {deleted_count}개 파일, {format_size(deleted_size)} 확보\n")

    return deleted_count, deleted_size


def main():
    parser = argparse.ArgumentParser(
        description="PB Product Generator Output & Cache Cleanup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s --stats                    # 통계만 표시
  %(prog)s --days 7                   # 7일 이상 오래된 파일 삭제
  %(prog)s --days 7 --dry-run         # 삭제 예정 목록만 표시
  %(prog)s --max-size 500             # 500MB로 크기 제한
  %(prog)s --cache --days 7           # 캐시만 정리 (7일 이상)
  %(prog)s --cache                    # 캐시 전체 정리
  %(prog)s --all                      # 전체 삭제 (output + cache)
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
        '--cache-dir',
        type=str,
        default='.cache/figma',
        help='캐시 디렉토리 경로 (기본: .cache/figma/)'
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
        '--cache',
        action='store_true',
        help='캐시 파일만 정리 (--days와 함께 사용 가능)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='전체 삭제 (output + cache, 확인 필요)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 삭제하지 않고 시뮬레이션만 실행'
    )

    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    cache_dir = Path(args.cache_dir)

    print("\n" + "🚀 PB Product Generator - Storage Cleanup")
    print("=" * 60)

    # 통계 표시
    if args.stats:
        show_stats(output_dir, cache_dir)
        return

    # 전체 삭제
    if args.all:
        count, size = cleanup_all(output_dir, cache_dir, dry_run=args.dry_run)
        return

    # 캐시만 정리
    if args.cache:
        count, size = cleanup_cache(cache_dir, days=args.days or 0, dry_run=args.dry_run)
        if count > 0:
            print(f"\n✅ 캐시 정리 완료: {count}개 파일, {format_size(size)} 확보\n")
        else:
            print(f"\n✅ 정리할 캐시 파일이 없습니다.\n")
        return

    # 날짜 기반 정리 (output만)
    if args.days:
        count, size = cleanup_by_age(output_dir, args.days, dry_run=args.dry_run)
        if count > 0:
            print(f"\n✅ 정리 완료: {count}개 항목, {format_size(size)} 확보\n")
        else:
            print(f"\n✅ 정리할 파일이 없습니다.\n")
        return

    # 크기 기반 정리 (output만)
    if args.max_size:
        count, size = cleanup_by_size(output_dir, args.max_size, dry_run=args.dry_run)
        if count > 0:
            print(f"\n✅ 정리 완료: {count}개 항목, {format_size(size)} 확보\n")
        return

    # 옵션 없으면 도움말 표시
    parser.print_help()
    print("\n💡 통계를 보려면: python3 cleanup.py --stats\n")
    print("💡 캐시 정리: python3 cleanup.py --cache --days 7\n")


if __name__ == "__main__":
    main()
