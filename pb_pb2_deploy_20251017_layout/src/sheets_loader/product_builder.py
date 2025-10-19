"""
@CODE:SHEETS-001 | SPEC: SPEC-SHEETS-001.md | TEST: tests/test_product_builder.py

ProductDataBuilder - 292개 컬럼 → ProductData 변환
"""

from typing import List, Dict, Optional, TYPE_CHECKING
from src.models.product_data import (
    ProductData,
    ColorVariant,
    DetailPoint,
    FabricInfo,
    CheckpointInfo,
    ModelInfo,
    TopSize,
    BottomSize,
    SizeInfo,
)
from src.sheets_loader import column_mapping as cm
from src.sheets_loader.utils import is_empty_value
from src.sheets_loader.color_extractor import ColorExtractor

if TYPE_CHECKING:
    from src.sheets_loader.loader import SheetsLoader


class ProductDataBuilder:
    """Google Sheets 292개 컬럼을 ProductData 모델로 변환"""

    def __init__(
        self,
        enable_color_extraction: bool = False,
        sheets_loader: Optional["SheetsLoader"] = None,
    ) -> None:
        """
        초기화

        Args:
            enable_color_extraction: 색상 자동 추출 활성화 여부 (기본: False)
                True로 설정 시 HEX 코드가 없는 색상 이미지에서 자동으로 색상 추출
            sheets_loader: SheetsLoader 인스턴스 (Google Drive API 사용)
        """
        self.color_extractor = (
            ColorExtractor(sheets_loader) if enable_color_extraction else None
        )

    def build_product_data(self, row: List[str], text_formatting: Optional[List[Optional[List[dict]]]] = None) -> ProductData:
        """
        292개 컬럼 행 데이터를 ProductData로 변환

        Args:
            row: Google Sheets 행 데이터 (292개 컬럼)
            text_formatting: 셀별 textFormatRuns 리스트 (선택, loader.extract_text_formatting 결과)

        Returns:
            ProductData 인스턴스

        Raises:
            ValidationError: Pydantic 검증 실패 시
        """
        # 기본 정보
        product_code = self._get_value(row, cm.COL_PRODUCT_CODE)
        product_name = self._get_value(row, cm.COL_PRODUCT_NAME)
        product_description = self._get_value(row, cm.COL_PRODUCT_DESCRIPTION)

        # 볼드 서식 적용 (product_description에만)
        if product_description and text_formatting and cm.COL_PRODUCT_DESCRIPTION < len(text_formatting):
            format_runs = text_formatting[cm.COL_PRODUCT_DESCRIPTION]
            if format_runs:
                product_description = self._apply_text_formatting(product_description, format_runs)
        main_image = self._get_value(row, cm.COL_MAIN_IMAGE)

        # 색상 정보 (1-6개 동적 파싱)
        colors = self._parse_colors(row)

        # 갤러리 (Color 1-8)
        gallery_by_color = self._parse_gallery(row, colors)

        # 디테일 포인트 (1-3개)
        detail_points = self._parse_detail_points(row)

        # 소재 정보
        fabric_info = self._parse_fabric_info(row)

        # 체크포인트 (선택)
        checkpoint = self._parse_checkpoint(row)

        # 모델 정보 (0-2개)
        model_info = self._parse_model_info(row)

        # 사이즈 정보
        size_info = self._parse_size_info(row)

        return ProductData(
            product_code=product_code,
            product_name=product_name,
            product_description=product_description,
            main_image=main_image,
            colors=colors,
            gallery_by_color=gallery_by_color,
            detail_points=detail_points,
            fabric_info=fabric_info,
            checkpoint=checkpoint,
            model_info=model_info,
            size_info=size_info,
        )

    def _get_value(self, row: List[str], index: int) -> Optional[str]:
        """컬럼 값 가져오기 (빈 값 필터링)"""
        if index >= len(row):
            return None
        value = row[index]
        return None if is_empty_value(value) else value

    def _parse_colors(self, row: List[str]) -> List[ColorVariant]:
        """
        색상 정보 파싱 (1-6개)

        HEX 코드가 없으면 color_extractor를 사용하여 이미지에서 자동 추출
        """
        colors = []
        for i in range(1, 7):
            color_image = self._get_value(row, cm.get_color_image_index(i))
            color_name = self._get_value(row, cm.get_color_name_index(i))

            if color_image and color_name:
                color_hex = self._get_value(row, cm.get_color_hex_index(i))

                # HEX 코드가 없고 색상 추출기가 활성화되어 있으면 자동 추출
                if not color_hex and self.color_extractor:
                    try:
                        print(f"🎨 색상 추출 중: {color_name} ({color_image[:50]}...)")
                        color_hex = self.color_extractor.extract_color_from_url(
                            color_image
                        )
                        if color_hex:
                            print(f"✅ 색상 추출 완료: {color_name} = {color_hex}")
                    except Exception as e:
                        print(f"⚠️  색상 추출 실패: {color_name} - {e}")
                        color_hex = None

                colors.append(
                    ColorVariant(
                        color_image=color_image,
                        color_name=color_name,
                        color_hex=color_hex,
                    )
                )
        return colors

    def _parse_gallery(
        self, row: List[str], colors: List[ColorVariant]
    ) -> Dict[str, List[str]]:
        """갤러리 이미지 파싱 (Color 1-8 × 12개)"""
        gallery: Dict[str, List[str]] = {}

        for color_num in range(1, 9):
            images = []
            for idx in cm.get_gallery_indices(color_num):
                img = self._get_value(row, idx)
                if img:
                    images.append(img)

            # 이미지가 있는 경우에만 추가
            if images:
                # Color 1-6은 colors 리스트에서 이름 가져오기
                if color_num <= len(colors):
                    color_name = colors[color_num - 1].color_name
                else:
                    color_name = f"Color{color_num}"

                gallery[color_name] = images

        return gallery

    def _parse_detail_points(self, row: List[str]) -> List[DetailPoint]:
        """디테일 포인트 파싱 (1-3개)"""
        points = []
        for i in range(1, cm.COL_DETAIL_POINT_COUNT + 1):
            img_idx, text_idx = cm.get_detail_point_indices(i)
            img = self._get_value(row, img_idx)
            text = self._get_value(row, text_idx)

            if img and text:
                points.append(DetailPoint(detail_image=img, detail_text=text))

        return points

    def _parse_fabric_info(self, row: List[str]) -> FabricInfo:
        """소재 정보 파싱"""
        image = self._get_value(row, cm.COL_FABRIC_IMAGE)
        composition = self._get_value(row, cm.COL_FABRIC_COMPOSITION)
        care = self._get_value(row, cm.COL_FABRIC_CARE)

        return FabricInfo(fabric_image=image, fabric_composition=composition, fabric_care=care)

    def _parse_checkpoint(self, row: List[str]) -> Optional[CheckpointInfo]:
        """체크포인트 파싱 (선택) - 이미지 없이 텍스트만 사용"""
        text = self._get_value(row, cm.COL_CHECKPOINT_TEXT)

        if text:
            # 체크포인트 이미지는 삭제되었으므로 더미 URL 사용
            # CheckpointInfo는 checkpoint_image가 필수이므로 None 처리 불가
            # 빈 문자열 또는 더미 URL 필요
            return CheckpointInfo(
                checkpoint_image="https://placeholder.com/checkpoint",
                checkpoint_text=text
            )
        return None

    def _parse_model_info(self, row: List[str]) -> List[ModelInfo]:
        """모델 정보 파싱 (0-2개)"""
        models = []

        # 모델 1
        image1 = self._get_value(row, cm.COL_MODEL1_IMAGE)
        height1 = self._get_value(row, cm.COL_MODEL1_HEIGHT)
        size1 = self._get_value(row, cm.COL_MODEL1_SIZE)
        if height1 and size1:
            models.append(ModelInfo(model_image=image1, model_size=size1, model_measurements=height1))

        # 모델 2
        image2 = self._get_value(row, cm.COL_MODEL2_IMAGE)
        height2 = self._get_value(row, cm.COL_MODEL2_HEIGHT)
        size2 = self._get_value(row, cm.COL_MODEL2_SIZE)
        if height2 and size2:
            models.append(ModelInfo(model_image=image2, model_size=size2, model_measurements=height2))

        return models

    def _parse_size_info(self, row: List[str]) -> SizeInfo:
        """사이즈 정보 파싱 (상의/하의)"""
        top_sizes = self._parse_top_sizes(row)
        bottom_sizes = self._parse_bottom_sizes(row)

        return SizeInfo(top=top_sizes if top_sizes else None, bottom=bottom_sizes if bottom_sizes else None)

    def _parse_top_sizes(self, row: List[str]) -> List[TopSize]:
        """상의 사이즈 파싱 (1-10개)"""
        sizes = []
        for i in range(1, cm.COL_TOP_SIZE_COUNT + 1):
            indices = cm.get_top_size_indices(i)

            size_name = self._get_value(row, indices["size_name"])
            shoulder = self._get_value(row, indices["shoulder"])
            chest = self._get_value(row, indices["chest"])
            sleeve = self._get_value(row, indices["sleeve"])
            length = self._get_value(row, indices["length"])

            # 필수 필드가 모두 있는 경우만 추가
            if all([size_name, shoulder, chest, sleeve, length]):
                sizes.append(
                    TopSize(
                        size_name=size_name,
                        shoulder=float(shoulder),
                        chest=float(chest),
                        sleeve=float(sleeve),
                        length=float(length),
                    )
                )

        return sizes

    def _parse_bottom_sizes(self, row: List[str]) -> List[BottomSize]:
        """하의 사이즈 파싱 (1-10개)"""
        sizes = []
        for i in range(1, cm.COL_BOTTOM_SIZE_COUNT + 1):
            indices = cm.get_bottom_size_indices(i)

            size_name = self._get_value(row, indices["size_name"])
            waist = self._get_value(row, indices["waist"])
            hip = self._get_value(row, indices["hip"])
            thigh = self._get_value(row, indices["thigh"])
            hem = self._get_value(row, indices["hem"])
            rise = self._get_value(row, indices["rise"])

            # 필수 필드가 모두 있는 경우만 추가
            if all([size_name, waist, hip, thigh, hem, rise]):
                sizes.append(
                    BottomSize(
                        size_name=size_name,
                        waist=float(waist),
                        hip=float(hip),
                        thigh=float(thigh),
                        hem=float(hem),
                        rise=float(rise),
                    )
                )

        return sizes

    def _apply_text_formatting(self, text: str, format_runs: List[dict]) -> str:
        """
        textFormatRuns를 바탕으로 텍스트에 HTML 서식 적용

        Args:
            text: 원본 텍스트
            format_runs: Google Sheets textFormatRuns 리스트
                각 run: {'startIndex': int, 'format': {'bold': bool, 'italic': bool, ...}}

        Returns:
            HTML 태그가 적용된 텍스트

        Example:
            text = "Hello World"
            format_runs = [
                {'startIndex': 0, 'format': {'bold': False}},
                {'startIndex': 6, 'format': {'bold': True}}
            ]
            → "Hello <b>World</b>"
        """
        if not format_runs:
            return text

        # 결과 텍스트 조립
        result = []

        for i, run in enumerate(format_runs):
            start_index = run.get('startIndex', 0)
            format_info = run.get('format', {})
            is_bold = format_info.get('bold', False)

            # 다음 run의 시작 인덱스 (없으면 텍스트 끝)
            next_index = format_runs[i + 1].get('startIndex', len(text)) if i + 1 < len(format_runs) else len(text)

            # 현재 구간 텍스트
            segment = text[start_index:next_index]

            # 볼드 적용
            if is_bold:
                result.append(f"<b>{segment}</b>")
            else:
                result.append(segment)

        return ''.join(result)
