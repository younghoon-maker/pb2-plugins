# @CODE:FIGMA-001:INFRA | SPEC: SPEC-FIGMA-001.md | TEST: tests/test_figma_client.py
"""
FigmaClient: Figma MCP API 래퍼 클래스

Phase 2 구현 범위:
- Mock 모드: fixture 기반 데이터 로드
- 캐시 fallback: API 실패 시 캐시 사용
- 에러 핸들링: FileNotFoundError, NotImplementedError

Phase 5 구현 예정:
- 실제 Figma MCP API 연동
- retry 3회 + exponential backoff (1s, 2s, 4s)
- 타임아웃 10초
"""

import json
from pathlib import Path
from typing import Any, Dict, cast


class FigmaClient:
    """
    @CODE:FIGMA-001:INFRA

    Figma MCP API 클라이언트 (Mock 모드 지원)

    Attributes:
        mock_mode: Mock 데이터 사용 여부
        use_cache: 캐시 fallback 사용 여부
        timeout: API 타임아웃 (초)
        fixture_dir: Mock fixture 디렉토리
        cache_dir: 캐시 디렉토리
    """

    def __init__(
        self,
        mock_mode: bool = True,
        use_cache: bool = True,
        timeout: int = 10
    ):
        """
        FigmaClient 초기화

        Args:
            mock_mode: True면 fixture 사용, False면 실제 API 호출
            use_cache: API 실패 시 캐시 사용 여부
            timeout: API 호출 타임아웃 (초, Phase 5에서 활성화)
        """
        self.mock_mode = mock_mode
        self.use_cache = use_cache
        self.timeout = timeout
        self.fixture_dir = Path("tests/fixtures")
        self.cache_dir = Path("tests/fixtures/.cache")

    def get_metadata(self, node_id: str) -> Dict[str, Any]:
        """
        @CODE:FIGMA-001:INFRA - 메타데이터 추출 메인 메서드

        Figma 노드의 메타데이터를 추출합니다.
        Mock 모드에서는 fixture를, 실제 모드에서는 MCP API를 호출합니다.

        Args:
            node_id: Figma 노드 ID (예: "1-95")

        Returns:
            Dict: 노드 트리 메타데이터
                - node_id: str
                - canvas: {width: int, height: int}
                - sections: List[Section] (10개)

        Raises:
            FileNotFoundError: Mock 모드에서 fixture 파일 없을 때
            NotImplementedError: 실제 API 호출 시 (Phase 5에서 구현)
        """
        if self.mock_mode:
            return self._load_mock_data(node_id)

        # 실제 API 호출 시도
        try:
            return self._call_mcp_api(node_id)
        except NotImplementedError:
            # API 구현 안 됨 → 캐시 사용 시도
            if self.use_cache:
                try:
                    return self._load_cache(node_id)
                except Exception as cache_err:
                    # 캐시도 실패 → NotImplementedError 재발생
                    raise NotImplementedError(
                        "Real Figma MCP API not implemented yet (Phase 5). "
                        "Cache also unavailable."
                    ) from cache_err
            raise

    def _load_mock_data(self, node_id: str) -> Dict[str, Any]:
        """
        @CODE:FIGMA-001:INFRA - Mock 데이터 로더

        Fixture 파일에서 Mock 데이터를 로드합니다.

        Args:
            node_id: Figma 노드 ID (예: "1-95")

        Returns:
            Dict: Mock 메타데이터 (tests/fixtures/{node_id}.json)

        Raises:
            FileNotFoundError: Fixture 파일이 없을 때
        """
        fixture_path = self.fixture_dir / f"{node_id}.json"

        if not fixture_path.exists():
            raise FileNotFoundError(
                f"Fixture not found: {fixture_path}. "
                f"Available fixtures: {list(self.fixture_dir.glob('*.json'))}"
            )

        with open(fixture_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return cast(Dict[str, Any], data)

    def _call_mcp_api(self, node_id: str) -> Dict[str, Any]:
        """
        @CODE:FIGMA-001:INFRA - 실제 MCP API 호출 (Phase 5 구현 예정)

        실제 Figma MCP API를 호출합니다.

        Phase 5에서 구현 예정:
        - MCP SDK 연동 (figma-mcp 패키지)
        - retry 3회 + exponential backoff (1s, 2s, 4s)
        - 타임아웃 10초
        - 응답 검증 및 정규화

        Args:
            node_id: Figma 노드 ID

        Raises:
            NotImplementedError: Phase 5에서 구현 예정
        """
        raise NotImplementedError(
            f"Real Figma MCP API not implemented yet (Phase 5). "
            f"Use mock_mode=True or ensure cache exists for node_id={node_id}"
        )

    def _load_cache(self, node_id: str) -> Dict[str, Any]:
        """
        @CODE:FIGMA-001:INFRA - 캐시 데이터 로더

        캐시 디렉토리에서 데이터를 로드합니다.
        API 실패 시 fallback으로 사용됩니다.

        Args:
            node_id: Figma 노드 ID

        Returns:
            Dict: 캐시된 메타데이터 (tests/fixtures/.cache/{node_id}.json)

        Raises:
            FileNotFoundError: 캐시 파일이 없을 때
        """
        cache_path = self.cache_dir / f"{node_id}.json"

        if not cache_path.exists():
            raise FileNotFoundError(
                f"Cache not found: {cache_path}. "
                f"Run with mock_mode=True first to generate cache."
            )

        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return cast(Dict[str, Any], data)
