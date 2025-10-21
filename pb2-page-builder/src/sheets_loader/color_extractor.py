"""
@CODE:SHEETS-001 | SPEC: SPEC-SHEETS-001.md

ColorExtractor - 이미지로부터 지배 색상 추출 (K-means 기반)

레퍼런스: reference/dana/scripts/load_from_sheets.py의 extract_dominant_color_improved()
"""

from typing import Optional, TYPE_CHECKING
from pathlib import Path
import tempfile
from PIL import Image
import numpy as np

if TYPE_CHECKING:
    from src.sheets_loader.loader import SheetsLoader


class ColorExtractor:
    """이미지로부터 지배 색상을 추출하는 K-means 기반 색상 추출기"""

    # 색상 추출 설정
    CROP_PERCENT = 0.3  # 중앙 30% 크롭
    BRIGHTNESS_THRESHOLD = 240  # 밝기 임계값 (배경 필터링)
    KMEANS_CLUSTERS = 3  # K-means 클러스터 개수
    KMEANS_ITERATIONS = 10  # 최대 반복 횟수

    def __init__(self, sheets_loader: Optional["SheetsLoader"] = None) -> None:
        """
        초기화

        Args:
            sheets_loader: SheetsLoader 인스턴스 (Google Drive API 사용)
        """
        self.sheets_loader = sheets_loader

    def extract_color_from_url(self, image_url: str) -> Optional[str]:
        """
        이미지 URL로부터 지배 색상 HEX 코드 추출

        Args:
            image_url: 이미지 URL (Google Drive 등)

        Returns:
            HEX 색상 코드 (예: "#A1B2C3") 또는 None

        Raises:
            Exception: 이미지 다운로드/처리 실패 시
        """
        if not image_url:
            return None

        if not self.sheets_loader:
            print("⚠️  SheetsLoader가 없어서 색상 추출을 건너뜁니다.")
            return None

        try:
            # 임시 파일에 이미지 다운로드 (Google Drive API 사용)
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                tmp_path = Path(tmp_file.name)

            # SheetsLoader의 Drive API로 다운로드
            self.sheets_loader.download_image(image_url, tmp_path)

            # 색상 추출
            hex_color = self.extract_color_from_file(tmp_path)

            # 임시 파일 삭제
            tmp_path.unlink()

            return hex_color

        except Exception as e:
            print(f"⚠️  색상 추출 실패 ({image_url}): {e}")
            return None

    def extract_color_from_file(self, image_path: Path) -> str:
        """
        이미지 파일로부터 지배 색상 HEX 코드 추출 (K-means 알고리즘)

        알고리즘:
        1. 이미지 로드 및 RGB 변환
        2. 중앙 30% 크롭 (제품에 집중)
        3. 밝기 필터 (< 240) - 배경 제거
        4. K-means 클러스터링 (3개 클러스터)
        5. 가장 큰 클러스터의 중심 색상 반환

        Args:
            image_path: 이미지 파일 경로

        Returns:
            HEX 색상 코드 (예: "#A1B2C3")

        Raises:
            FileNotFoundError: 이미지 파일이 없을 경우
            Exception: 이미지 처리 실패 시
        """
        # 1. 이미지 로드
        img = Image.open(image_path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # 2. 중앙 크롭 (30%)
        width, height = img.size
        crop_width = int(width * self.CROP_PERCENT)
        crop_height = int(height * self.CROP_PERCENT)
        left = (width - crop_width) // 2
        top = (height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height
        img_cropped = img.crop((left, top, right, bottom))

        # 3. NumPy 배열 변환
        img_array = np.array(img_cropped)
        pixels = img_array.reshape(-1, 3)

        # 4. 밝기 필터 (배경 제거)
        brightness = np.mean(pixels, axis=1)
        dark_pixels = pixels[brightness < self.BRIGHTNESS_THRESHOLD]

        if len(dark_pixels) == 0:
            # 어두운 픽셀이 없으면 전체 픽셀 사용
            dark_pixels = pixels

        # 5. K-means 클러스터링
        n_clusters = min(self.KMEANS_CLUSTERS, len(dark_pixels))
        np.random.seed(42)  # 재현성을 위한 시드 고정

        # 초기 중심점 선택 (랜덤)
        centroids = dark_pixels[
            np.random.choice(len(dark_pixels), n_clusters, replace=False)
        ]

        # K-means 반복
        for _ in range(self.KMEANS_ITERATIONS):
            # 각 픽셀을 가장 가까운 중심점에 할당
            distances = np.sqrt(
                ((dark_pixels[:, np.newaxis] - centroids) ** 2).sum(axis=2)
            )
            labels = np.argmin(distances, axis=1)

            # 중심점 업데이트
            new_centroids = np.array(
                [
                    (
                        dark_pixels[labels == i].mean(axis=0)
                        if np.any(labels == i)
                        else centroids[i]
                    )
                    for i in range(n_clusters)
                ]
            )

            # 수렴 확인
            if np.allclose(centroids, new_centroids):
                break

            centroids = new_centroids

        # 6. 가장 큰 클러스터 찾기
        cluster_sizes = [np.sum(labels == i) for i in range(n_clusters)]
        dominant_cluster = np.argmax(cluster_sizes)
        dominant_color = centroids[dominant_cluster]

        # 7. HEX 코드 변환
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(dominant_color[0]),
            int(dominant_color[1]),
            int(dominant_color[2]),
        )

        return hex_color
