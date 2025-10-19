# @CODE:HTML-001:DOMAIN | SPEC: .moai/specs/SPEC-HTML-001/spec.md
# TEST: tests/test_layout_renderer.py

"""CSS 레이아웃 렌더러

픽셀 정확도 검증 및 CSS absolute positioning 생성을 담당합니다.
"""

import re
from typing import Any, Dict, Optional

from src.models.design_spec import DesignSpec, Section


class LayoutRenderer:
    """CSS 레이아웃 렌더러

    Figma 디자인을 픽셀 퍼펙트 CSS로 변환합니다.
    """

    def __init__(self, pixel_tolerance: int = 2) -> None:
        """레이아웃 렌더러 초기화.

        Args:
            pixel_tolerance: 픽셀 오차 허용 범위 (기본: 2px)
        """
        self.pixel_tolerance = pixel_tolerance

    def render_section_css(self, section: Section) -> str:
        """섹션별 CSS 스타일 생성.

        Args:
            section: Section 객체

        Returns:
            str: CSS 코드 (position: absolute 기반)
        """
        # 섹션명을 CSS 클래스명으로 변환 (소문자, 공백/특수문자 제거)
        class_name = self._normalize_class_name(section.name)

        return f""".section--{class_name} {{
    position: absolute;
    left: {section.x}px;
    top: {section.y}px;
    width: {section.width}px;
    height: {section.height}px;
}}"""

    def _normalize_class_name(self, name: str) -> str:
        """섹션명을 CSS 클래스명으로 정규화.

        Args:
            name: 섹션명 (예: "Product Hero", "Product Info & Details")

        Returns:
            str: 정규화된 클래스명 (예: "product-hero", "product-info-details")
        """
        # 소문자 변환 후 공백/특수문자를 하이픈으로 변환
        normalized = name.lower()
        # 특수문자 제거 (알파벳, 숫자, 공백만 유지)
        normalized = re.sub(r"[^a-z0-9\s]", "", normalized)
        # 연속된 공백을 하이픈으로 변환
        normalized = re.sub(r"\s+", "-", normalized.strip())
        return normalized

    def validate_layout(
        self, section: Section, expected_x: int, expected_y: int
    ) -> Optional[Dict[str, Any]]:
        """레이아웃 정확도 검증 (±2px).

        Args:
            section: 검증할 Section 객체
            expected_x: 기대하는 X 좌표
            expected_y: 기대하는 Y 좌표

        Returns:
            Optional[Dict[str, Any]]: 오차 발견 시 오차 리포트, 없으면 None
        """
        expected = {"x": expected_x, "y": expected_y}
        actual = {"x": section.x, "y": section.y}

        diff_x = abs(expected["x"] - actual["x"])
        diff_y = abs(expected["y"] - actual["y"])
        max_diff = max(diff_x, diff_y)

        if max_diff > self.pixel_tolerance:
            return {
                "section": section.name,
                "expected": expected,
                "actual": actual,
                "diff": max_diff,
                "exceeds_tolerance": True,
            }
        return None

    def render_css(self, design_spec: DesignSpec) -> str:
        """전체 CSS 생성.

        Args:
            design_spec: 디자인 스펙

        Returns:
            str: CSS 코드 (변수 + 섹션별 스타일)
        """
        # CSS 변수 생성
        css_vars = f""":root {{
    --canvas-width: {design_spec.width}px;
    --canvas-height: {design_spec.height}px;
    --font-family: '{design_spec.font_family}', sans-serif;
}}"""

        # 섹션별 스타일 생성
        section_styles = "\n\n".join(
            self.render_section_css(section) for section in design_spec.sections
        )

        return f"{css_vars}\n\n{section_styles}"
