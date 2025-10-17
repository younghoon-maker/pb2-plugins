# @CODE:FIGMA-001:DOMAIN | SPEC: .moai/specs/SPEC-FIGMA-001/spec.md
# TEST: tests/test_design_validator.py

"""디자인 스펙 검증기

필수 섹션, 레이아웃 정확도, 캔버스 크기를 검증합니다.
"""

from typing import List

from src.models.design_spec import DesignSpec
from src.models.exceptions import ValidationError


class DesignValidator:
    """디자인 스펙 검증기

    10개 필수 섹션, ±2px 레이아웃 정확도, 1080px 캔버스 너비를 검증합니다.
    """

    # 필수 섹션 10개 (tests/fixtures/1-95.json 기준)
    REQUIRED_SECTIONS = [
        "Product Hero",
        "Color Variants",
        "Lifestyle Gallery",
        "Material Detail",
        "Color Selector",
        "Product Info",
        "Care Instructions",
        "Model Info",
        "Size Guide",
        "Size Chart",
    ]

    TOLERANCE = 2  # ±2px
    EXPECTED_WIDTH = 1082  # 1082px (실제 Figma 디자인 기준)

    # 기준 좌표 (실제 Figma 디자인 기준 - 2025-10-15 업데이트)
    REFERENCE_COORDS = {
        "Product Hero": (24, 180),
        "Color Variants": (0, 1996),
        "Lifestyle Gallery": (24, 3633),
        "Material Detail": (19, 18857),
        "Color Selector": (36, 21829),
        "Product Info": (20, 22027),
        "Care Instructions": (36, 23260),
        "Model Info": (37, 23737),
        "Size Guide": (53, 24307),
        "Size Chart": (53, 24581),
    }

    def validate_sections(self, spec: DesignSpec) -> bool:
        """필수 섹션 10개가 모두 존재하는지 확인

        Args:
            spec: 검증할 DesignSpec 객체

        Returns:
            bool: 모든 섹션 존재 시 True

        Raises:
            ValidationError: 필수 섹션 누락 시
        """
        section_names = {s.name for s in spec.sections}

        for required in self.REQUIRED_SECTIONS:
            if required not in section_names:
                raise ValidationError(f"Missing required section: {required}")

        return True

    def validate_layout_accuracy(self, spec: DesignSpec) -> List[str]:
        """레이아웃 오차 검증 (±2px 기준)

        Args:
            spec: 검증할 DesignSpec 객체

        Returns:
            List[str]: 오차 초과 에러 메시지 목록
        """
        errors = []

        for section in spec.sections:
            if section.name in self.REFERENCE_COORDS:
                ref_x, ref_y = self.REFERENCE_COORDS[section.name]

                # X 좌표 오차
                x_diff = section.x - ref_x
                if abs(x_diff) > self.TOLERANCE:
                    errors.append(
                        f"Section '{section.name}' X position error: "
                        f"{'+' if x_diff > 0 else ''}{x_diff}px (expected {ref_x}, got {section.x})"
                    )

                # Y 좌표 오차
                y_diff = section.y - ref_y
                if abs(y_diff) > self.TOLERANCE:
                    errors.append(
                        f"Section '{section.name}' Y position error: "
                        f"{'+' if y_diff > 0 else ''}{y_diff}px (expected {ref_y}, got {section.y})"
                    )

        return errors

    def validate_canvas_width(self, spec: DesignSpec) -> bool:
        """캔버스 너비 검증 (1080px)

        Args:
            spec: 검증할 DesignSpec 객체

        Returns:
            bool: 1080px이면 True

        Raises:
            ValidationError: 너비가 1080px이 아닐 시
        """
        if spec.width != self.EXPECTED_WIDTH:
            raise ValidationError(
                f"Canvas width must be {self.EXPECTED_WIDTH}px, got {spec.width}px"
            )

        return True
