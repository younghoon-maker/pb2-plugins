# @CODE:FIGMA-001 | SPEC: .moai/specs/SPEC-FIGMA-001/spec.md | TEST: tests/test_design_spec.py
# @CODE:HTML-001 | SPEC: .moai/specs/SPEC-HTML-001/spec.md | TEST: tests/test_html_generator.py

"""Figma Parser 및 HTML Generator 커스텀 예외 클래스"""


class FigmaParserError(Exception):
    """Figma Parser 기본 예외"""
    pass


class FigmaAPIError(FigmaParserError):
    """Figma MCP API 호출 실패"""
    pass


class ValidationError(FigmaParserError):
    """디자인 스펙 검증 실패"""
    pass


class CacheError(FigmaParserError):
    """캐시 로드/저장 실패"""
    pass


# HTML Generator 예외 (SPEC-HTML-001)
class HTMLGeneratorError(Exception):
    """HTML Generator 기본 예외"""
    pass


class TemplateError(HTMLGeneratorError):
    """Jinja2 템플릿 렌더링 실패"""
    pass


class LayoutError(HTMLGeneratorError):
    """레이아웃 오차 초과 (경고)"""
    pass


class FileSizeError(HTMLGeneratorError):
    """HTML 파일 크기 초과 (경고)"""
    pass
