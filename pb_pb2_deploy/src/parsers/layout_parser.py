# @CODE:FIGMA-001:DOMAIN
# SPEC: .moai/specs/SPEC-FIGMA-001/spec.md
# TEST: tests/test_layout_parser.py

"""Figma 레이아웃 파서

Figma JSON 데이터를 파싱하여 DesignSpec 모델로 변환합니다.
"""

from typing import Any, Dict

from src.models.design_spec import DesignSpec, Section


def parse_layout(figma_data: Dict[str, Any]) -> DesignSpec:
    """Figma JSON 데이터를 DesignSpec으로 파싱

    Args:
        figma_data: Figma JSON 데이터 (node_id, canvas, sections 포함)

    Returns:
        DesignSpec: 파싱된 디자인 스펙

    Raises:
        ValidationError: 섹션이 10개가 아니거나 필수 필드 누락 시

    Example:
        >>> figma_data = {"canvas": {"width": 1080, "height": 25520}, "sections": [...]}
        >>> spec = parse_layout(figma_data)
        >>> spec.width
        1080
    """
    canvas = figma_data["canvas"]
    sections_data = figma_data["sections"]

    sections = [_parse_section(section) for section in sections_data]

    return DesignSpec(
        width=canvas["width"],
        height=canvas["height"],
        sections=sections,
        font_family="Pretendard"
    )


def _parse_section(section_data: Dict[str, Any]) -> Section:
    """단일 섹션 데이터 파싱

    Args:
        section_data: 섹션 JSON 데이터

    Returns:
        Section: 파싱된 섹션 모델
    """
    return Section(
        id=section_data["id"],
        name=section_data["name"],
        figma_group=section_data["figma_group"],
        x=section_data["x"],
        y=section_data["y"],
        width=section_data["width"],
        height=section_data["height"],
        styles=section_data.get("styles", {})
    )
