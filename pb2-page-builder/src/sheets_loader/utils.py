"""
@CODE:SHEETS-001 | SPEC: SPEC-SHEETS-001.md | TEST: tests/test_utils.py

유틸리티 함수
"""

from typing import Optional


def is_empty_value(value: Optional[str]) -> bool:
    """
    빈 값 여부 확인

    Args:
        value: 검사할 값

    Returns:
        빈 값이면 True, 그렇지 않으면 False

    Examples:
        >>> is_empty_value("-")
        True
        >>> is_empty_value("Valid Text")
        False
    """
    if value is None:
        return True

    # 공백 제거 후 검사
    trimmed = value.strip()

    if not trimmed:
        return True

    # 대소문자 구분 없이 빈 값 패턴 검사
    upper_value = trimmed.upper()

    # 대시
    if upper_value == "-":
        return True

    # N/A 변형
    if upper_value in ("N/A", "#N/A"):
        return True

    # REF 에러
    if upper_value == "#REF!":
        return True

    return False
