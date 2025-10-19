# @CODE:FIGMA-001:DOMAIN | SPEC: .moai/specs/SPEC-FIGMA-001/spec.md

"""Figma JSON 파서 모듈

Figma JSON 데이터를 DesignSpec 모델로 변환합니다.
"""

from src.parsers.layout_parser import parse_layout

__all__ = ["parse_layout"]
