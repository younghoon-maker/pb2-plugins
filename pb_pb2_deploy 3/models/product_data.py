"""
@CODE:SHEETS-001 | SPEC: SPEC-SHEETS-001.md | TEST: tests/test_product_data.py

Pydantic 데이터 모델
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class ColorVariant(BaseModel):
    """색상 변형 정보"""

    color_image: HttpUrl = Field(..., description="색상 대표 이미지")
    color_name: str = Field(..., min_length=1, description="색상명")
    color_hex: Optional[str] = Field(
        None, pattern=r"^#?[0-9A-Fa-f]{6}$", description="HEX 코드"
    )

    @field_validator("color_hex")
    @classmethod
    def ensure_hex_prefix(cls, v: Optional[str]) -> Optional[str]:
        """HEX 코드에 # 접두사 추가"""
        if v and not v.startswith("#"):
            return f"#{v}"
        return v


class DetailPoint(BaseModel):
    """디테일 포인트 정보"""

    detail_image: HttpUrl = Field(..., description="디테일 이미지")
    detail_text: str = Field(..., min_length=1, description="디테일 설명")


class FabricInfo(BaseModel):
    """소재 정보"""

    fabric_image: Optional[HttpUrl] = Field(None, description="소재 이미지")
    fabric_composition: str = Field(..., min_length=1, description="소재 구성")
    fabric_care: str = Field(..., min_length=1, description="세탁 방법")


class CheckpointInfo(BaseModel):
    """체크포인트 정보"""

    checkpoint_image: HttpUrl = Field(..., description="체크포인트 이미지")
    checkpoint_text: str = Field(..., min_length=1, description="체크포인트 설명")


class ModelInfo(BaseModel):
    """모델 정보"""

    model_image: Optional[HttpUrl] = Field(None, description="모델 이미지")
    model_size: str = Field(..., min_length=1, description="모델 착용 사이즈")
    model_measurements: str = Field(..., min_length=1, description="모델 신체 정보")


class TopSize(BaseModel):
    """상의 사이즈"""

    size_name: str = Field(..., min_length=1, description="사이즈명 (S, M, L 등)")
    chest: float = Field(..., gt=0, description="가슴 둘레 (cm)")
    shoulder: float = Field(..., gt=0, description="어깨 너비 (cm)")
    sleeve: float = Field(..., gt=0, description="소매 길이 (cm)")
    length: float = Field(..., gt=0, description="총장 (cm)")


class BottomSize(BaseModel):
    """하의 사이즈"""

    size_name: str = Field(..., min_length=1, description="사이즈명 (S, M, L 등)")
    waist: float = Field(..., gt=0, description="허리 둘레 (cm)")
    hip: float = Field(..., gt=0, description="엉덩이 둘레 (cm)")
    thigh: float = Field(..., gt=0, description="허벅지 둘레 (cm)")
    rise: float = Field(..., gt=0, description="밑위 (cm)")
    hem: float = Field(..., gt=0, description="밑단 둘레 (cm)")


class SizeInfo(BaseModel):
    """사이즈 정보"""

    top: Optional[List[TopSize]] = Field(None, description="상의 사이즈")
    bottom: Optional[List[BottomSize]] = Field(None, description="하의 사이즈")

    @model_validator(mode="after")
    def at_least_one_size(self) -> "SizeInfo":
        """top 또는 bottom 중 하나는 필수"""
        if not self.top and not self.bottom:
            raise ValueError("top 또는 bottom 중 하나는 필수입니다")
        return self


class ProductData(BaseModel):
    """상품 전체 데이터 모델"""

    # 기본 정보
    product_code: str = Field(..., min_length=1, description="상품코드 (내부 식별용)")
    product_name: str = Field(..., min_length=1, description="상품명")
    main_image: HttpUrl = Field(..., description="메인 이미지 URL")

    # 색상 정보
    colors: List[ColorVariant] = Field(
        ..., min_length=1, max_length=6, description="색상 변형"
    )

    # 갤러리
    gallery_by_color: Dict[str, List[HttpUrl]] = Field(
        ..., description="컬러별 갤러리 이미지"
    )

    # 디테일 포인트
    detail_points: List[DetailPoint] = Field(
        ..., min_length=1, max_length=3, description="제품 특징"
    )

    # 소재 정보
    fabric_info: FabricInfo = Field(..., description="소재 정보")

    # 체크포인트 (선택)
    checkpoint: Optional[CheckpointInfo] = Field(None, description="체크포인트 정보")

    # 모델 정보 (선택)
    model_info: List[ModelInfo] = Field(
        default_factory=list, max_length=2, description="모델 정보"
    )

    # 사이즈 정보
    size_info: SizeInfo = Field(..., description="사이즈 정보")
