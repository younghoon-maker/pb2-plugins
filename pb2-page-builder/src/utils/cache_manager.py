# @CODE:FIGMA-001:INFRA
# SPEC: .moai/specs/SPEC-FIGMA-001/spec.md
# TEST: tests/test_cache_manager.py

"""캐시 관리자

TTL 기반 로컬 캐시 저장/로드를 제공합니다.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, cast


class CacheManager:
    """TTL 기반 캐시 관리자

    Figma 메타데이터를 로컬에 캐싱하여 오프라인 모드를 지원합니다.
    """

    CACHE_DIR = Path(".cache/figma")

    def __init__(self, ttl: int = 3600) -> None:
        """CacheManager 초기화

        Args:
            ttl: 캐시 만료 시간 (초), 기본값 1시간 (3600초)
        """
        self.ttl = ttl
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def save(self, node_id: str, data: Dict[str, Any]) -> None:
        """캐시 저장

        Args:
            node_id: Figma 노드 ID (예: "1:95")
            data: 저장할 데이터 (dict)
        """
        cache_file = self._get_cache_path(node_id)
        cache_data = {"timestamp": datetime.now().isoformat(), "data": data}

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)

    def load(self, node_id: str) -> Optional[Dict[str, Any]]:
        """캐시 로드

        Args:
            node_id: Figma 노드 ID

        Returns:
            Optional[Dict]: TTL 이내 캐시 데이터, 없으면 None
        """
        cache_file = self._get_cache_path(node_id)

        if not cache_file.exists():
            return None

        # TTL 확인
        if not self.is_valid(node_id):
            return None

        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = cast(Dict[str, Any], json.load(f))

        return cast(Dict[str, Any], cache_data["data"])

    def is_valid(self, node_id: str) -> bool:
        """캐시 유효성 확인 (TTL)

        Args:
            node_id: Figma 노드 ID

        Returns:
            bool: TTL 이내이면 True
        """
        cache_file = self._get_cache_path(node_id)

        if not cache_file.exists():
            return False

        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = cast(Dict[str, Any], json.load(f))

        timestamp = datetime.fromisoformat(str(cache_data["timestamp"]))
        return datetime.now() - timestamp < timedelta(seconds=self.ttl)

    def _get_cache_path(self, node_id: str) -> Path:
        """캐시 파일 경로 생성

        Args:
            node_id: Figma 노드 ID (예: "1:95")

        Returns:
            Path: 캐시 파일 경로 (예: ".cache/figma/1-95.json")
        """
        filename = node_id.replace(":", "-") + ".json"
        return self.CACHE_DIR / filename
