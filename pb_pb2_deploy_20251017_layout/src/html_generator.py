# @CODE:HTML-001:DOMAIN | SPEC: .moai/specs/SPEC-HTML-001/spec.md
# TEST: tests/test_html_generator.py

"""HTML 생성기

DesignSpec을 HTML/CSS로 변환하는 오케스트레이션을 담당합니다.
"""

import logging
import os
from typing import List

from src.layout_renderer import LayoutRenderer
from src.models.design_spec import DesignSpec
from src.models.exceptions import ValidationError
from src.template_engine import TemplateEngine

logger = logging.getLogger(__name__)


class HTMLGenerator:
    """HTML 생성기

    DesignSpec → HTML 변환 오케스트레이션을 담당합니다.
    """

    # 필수 섹션 이름 (10개)
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

    # 섹션명 → 템플릿 파일명 매핑
    SECTION_TEMPLATE_MAP = {
        "Product Hero": "product_hero",
        "Color Variants": "color_variants",
        "Lifestyle Gallery": "lifestyle_gallery",
        "Material Detail": "material_detail",
        "Color Selector": "color_selector",
        "Product Info": "product_info",
        "Care Instructions": "care_instructions",
        "Model Info": "model_info",
        "Size Guide": "size_guide",
        "Size Chart": "size_chart",
    }

    def __init__(
        self,
        template_engine: TemplateEngine,
        layout_renderer: LayoutRenderer,
        output_dir: str = "output",
    ) -> None:
        """HTML 생성기 초기화.

        Args:
            template_engine: Jinja2 템플릿 엔진
            layout_renderer: CSS 레이아웃 렌더러
            output_dir: 출력 디렉토리 경로
        """
        self.template_engine = template_engine
        self.layout_renderer = layout_renderer
        self.output_dir = output_dir

    def generate(self, design_spec: DesignSpec) -> str:
        """DesignSpec을 HTML로 변환합니다.

        Args:
            design_spec: Figma 디자인 스펙 객체

        Returns:
            str: 생성된 HTML 파일 경로 (예: "output/original.html")

        Raises:
            ValidationError: DesignSpec 검증 실패 시
        """
        logger.info("Starting HTML generation...")

        # 1. DesignSpec 검증
        self.validate_spec(design_spec)
        logger.info("DesignSpec validation passed")

        # 2. CSS 생성
        css = self._generate_css(design_spec)
        logger.info("CSS generation completed")

        # 3. 섹션 렌더링 (10개)
        sections_html_list = self._render_sections(design_spec)
        sections_html = "\n".join(sections_html_list)
        logger.info(f"Rendered {len(sections_html_list)} sections")

        # 4. 기본 HTML 템플릿 렌더링
        html_content = self.template_engine.render(
            self.template_engine.get_base_template(),
            {
                "canvas_width": design_spec.width,
                "canvas_height": design_spec.height,
                "sections_html": sections_html,
                "css": css,
            },
        )
        logger.info("Base HTML template rendered")

        # 5. HTML 파일 저장
        output_path = self._save_html(html_content)
        logger.info(f"HTML saved to: {output_path}")

        return output_path

    def validate_spec(self, design_spec: DesignSpec) -> bool:
        """DesignSpec 유효성 검증.

        Args:
            design_spec: 검증할 디자인 스펙

        Returns:
            bool: 검증 성공 여부

        Raises:
            ValidationError: 필수 섹션 누락, 캔버스 크기 불일치 등
        """
        # 1. 섹션 개수 검증 (정확히 10개)
        if len(design_spec.sections) != 10:
            raise ValidationError(
                f"DesignSpec must contain exactly 10 sections, got {len(design_spec.sections)}"
            )

        # 2. 캔버스 크기 검증
        if design_spec.width != 1082:
            raise ValidationError(
                f"Invalid canvas width: {design_spec.width}px (expected: 1082px)"
            )

        if design_spec.height != 25520:
            raise ValidationError(
                f"Invalid canvas height: {design_spec.height}px (expected: 25520px)"
            )

        # 3. 필수 섹션 존재 여부 검증
        section_names = {section.name for section in design_spec.sections}
        for required in self.REQUIRED_SECTIONS:
            if required not in section_names:
                raise ValidationError(f"Missing required section: {required}")

        return True

    def _render_sections(self, design_spec: DesignSpec) -> List[str]:
        """10개 섹션을 순차적으로 렌더링.

        Args:
            design_spec: 디자인 스펙

        Returns:
            List[str]: 렌더링된 섹션 HTML 목록 (10개)
        """
        rendered_sections = []
        for i, section in enumerate(design_spec.sections, start=1):
            logger.info(f"Rendering section {i}/10: {section.name}")

            # 섹션 템플릿명 결정
            template_name = self.SECTION_TEMPLATE_MAP.get(
                section.name, section.name.lower().replace(" ", "_")
            )

            # 섹션 렌더링
            section_html = self.template_engine.render_section(template_name, section)
            rendered_sections.append(section_html)

        return rendered_sections

    def _generate_css(self, design_spec: DesignSpec) -> str:
        """레이아웃 CSS 생성.

        Args:
            design_spec: 디자인 스펙

        Returns:
            str: CSS 코드 (절대 포지셔닝 기반)
        """
        return self.layout_renderer.render_css(design_spec)

    def _save_html(self, html: str, filename: str = "original.html") -> str:
        """HTML 파일 저장.

        Args:
            html: HTML 코드
            filename: 파일명

        Returns:
            str: 저장된 파일 경로
        """
        # 출력 디렉토리 생성 (없으면)
        os.makedirs(self.output_dir, exist_ok=True)

        # HTML 파일 저장
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        # 파일 크기 검증 (경고)
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        if file_size_mb > 30:
            logger.warning(f"HTML file size exceeds 30MB: {file_size_mb:.2f}MB")

        return output_path
