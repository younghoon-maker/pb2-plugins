# @CODE:HTML-001:UI | SPEC: .moai/specs/SPEC-HTML-001/spec.md
# TEST: tests/test_template_engine.py

"""Jinja2 템플릿 엔진 래퍼

템플릿 로딩 및 렌더링을 추상화합니다.
"""

from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, Template

from src.models.design_spec import Section


class TemplateEngine:
    """Jinja2 템플릿 엔진 래퍼

    템플릿 관리 및 렌더링을 담당합니다.
    """

    def __init__(self, template_dir: str = "templates") -> None:
        """템플릿 엔진 초기화.

        Args:
            template_dir: 템플릿 디렉토리 경로
        """
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,  # XSS 방지
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """템플릿 렌더링.

        Args:
            template_name: 템플릿 파일명 (예: "base.html.jinja2")
            context: 템플릿 컨텍스트 (변수 딕셔너리)

        Returns:
            str: 렌더링된 HTML

        Raises:
            TemplateNotFoundError: 템플릿 파일 없음
            TemplateSyntaxError: 템플릿 문법 오류
        """
        template = self._load_template(template_name)
        return template.render(**context)

    def render_section(self, section_name: str, section: Section) -> str:
        """섹션별 템플릿 렌더링.

        Args:
            section_name: 섹션명 (예: "product_hero")
            section: Section 객체

        Returns:
            str: 렌더링된 섹션 HTML
        """
        template_path = f"sections/{section_name}.html.jinja2"
        context = {"section": section}
        return self.render(template_path, context)

    def get_base_template(self) -> str:
        """기본 HTML 골격 템플릿 로드.

        Returns:
            str: base.html.jinja2 경로
        """
        return "base.html.jinja2"

    def _load_template(self, template_name: str) -> Template:
        """Jinja2 템플릿 로드 (내부 메서드).

        Args:
            template_name: 템플릿 파일명

        Returns:
            jinja2.Template: 로드된 템플릿 객체
        """
        return self.env.get_template(template_name)
