# @CODE:FIGMA-001:DATA | SPEC: .moai/specs/SPEC-FIGMA-001/spec.md | TEST: tests/test_design_spec.py

"""Figma 디자인 스펙 데이터 모델

Pydantic 기반 데이터 검증 및 직렬화를 제공합니다.
"""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Section(BaseModel):
    """Figma 섹션 정보

    단일 섹션의 레이아웃 및 스타일 정보를 포함합니다.
    """

    id: str = Field(..., description="Figma 노드 ID (예: 1:159)")
    name: str = Field(..., description="섹션명 (예: Product Hero)")
    figma_group: str = Field(..., description="Figma Group ID (예: Group 10)")
    x: int = Field(..., ge=0, description="X 좌표 (px)")
    y: int = Field(..., ge=0, description="Y 좌표 (px)")
    width: int = Field(..., gt=0, description="너비 (px)")
    height: int = Field(..., gt=0, description="높이 (px)")
    styles: Dict[str, Any] = Field(
        default_factory=dict,
        description="폰트 스타일 등 (font-family, font-weight, font-size, line-height)",
    )


class DesignSpec(BaseModel):
    """디자인 스펙 최상위 모델

    Figma 디자인의 전체 레이아웃 정보를 포함합니다.
    """

    width: int = Field(1080, description="캔버스 너비 (px)")
    height: int = Field(25520, description="캔버스 높이 (px)")
    sections: List[Section] = Field(
        ..., min_length=10, max_length=10, description="10개 섹션"
    )
    font_family: str = Field("Pretendard", description="기본 폰트")

    def to_json(self) -> str:
        """JSON 문자열로 직렬화

        Returns:
            str: JSON 형식의 문자열
        """
        return self.model_dump_json(indent=2)
