#!/usr/bin/env python3
"""
AI 기반 색상 HEX 코드 자동 추출
이미지 분석을 통한 정확한 색상 HEX 코드 추출 (DANA&PETA 페이지 빌더용)
"""

import logging
from pathlib import Path
from typing import Optional, Dict
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


class ColorExtractor:
    """AI 기반 색상 HEX 코드 추출기"""

    def __init__(self):
        """ColorExtractor 초기화"""
        pass

    def extract_color_hex(
        self,
        image_path: str,
        color_name: str,
        product_type: str = "의류"
    ) -> Optional[str]:
        """
        이미지에서 색상 HEX 코드 추출

        k-means clustering 알고리즘 사용:
        1. 이미지 중앙 영역(50%)만 사용하여 배경 제거
        2. k-means로 5개 주요 색상 클러스터 추출
        3. 밝은색(흰색/회색 배경) 필터링 (brightness < 230)
        4. 가장 많이 나타나는 유효한 색상 선택

        Args:
            image_path: 색상 이미지 경로
            color_name: 색상 이름 (예: "베이지", "레드")
            product_type: 제품 타입 (예: "의류", "니트")

        Returns:
            HEX 코드 (예: "#936d4a") 또는 None
        """
        try:
            image_path = Path(image_path)
            if not image_path.exists():
                logger.error(f"❌ 이미지 파일을 찾을 수 없습니다: {image_path}")
                return None

            logger.info(f"🎨 색상 분석 중: {color_name} (파일: {image_path.name})")

            # 1. 이미지 로드 및 RGB 변환
            img = Image.open(image_path)
            img = img.convert('RGB')

            # 2. NumPy 배열로 변환
            img_array = np.array(img)

            # 3. 이미지 중앙 영역만 사용 (제품 부분, 배경 제거)
            # 중앙 50% 영역 추출
            h, w, _ = img_array.shape
            center_h_start = h // 4
            center_h_end = 3 * h // 4
            center_w_start = w // 4
            center_w_end = 3 * w // 4

            center_region = img_array[center_h_start:center_h_end, center_w_start:center_w_end]

            # 4. 픽셀들을 1D 배열로 변환 (각 행이 하나의 픽셀 RGB)
            pixels = center_region.reshape(-1, 3)

            # 5. k-means clustering으로 주요 색상 추출 (5개 클러스터)
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            kmeans.fit(pixels)

            # 6. 각 클러스터의 크기 계산
            labels = kmeans.labels_
            counts = np.bincount(labels)

            # 7. 배경색(흰색/회색) 제외하고 가장 많은 색상 선택
            centers = kmeans.cluster_centers_.astype(int)
            valid_colors = []

            for i, (color, count) in enumerate(zip(centers, counts)):
                # 너무 밝은 색상(흰색 배경) 제외
                brightness = np.mean(color)
                if brightness < 230:  # 흰색 배경 필터링 기준
                    valid_colors.append((color, count))

            if not valid_colors:
                # 모든 색상이 필터링된 경우, 가장 많은 색상 사용
                dominant_color = centers[np.argmax(counts)]
                logger.warning(f"⚠️  모든 색상이 밝아서 필터링 없이 선택: {color_name}")
            else:
                # 유효한 색상 중 가장 많은 것 선택
                valid_colors.sort(key=lambda x: x[1], reverse=True)
                dominant_color = valid_colors[0][0]

            # 8. RGB를 HEX로 변환
            hex_code = '#{:02x}{:02x}{:02x}'.format(
                int(dominant_color[0]),
                int(dominant_color[1]),
                int(dominant_color[2])
            )

            logger.info(f"✅ 색상 추출 완료: {color_name} → {hex_code}")
            return hex_code

        except ImportError as e:
            logger.error(f"❌ 필요한 라이브러리가 설치되지 않았습니다: {e}")
            logger.error("   pip install scikit-learn numpy Pillow")
            return None
        except Exception as e:
            logger.error(f"❌ 색상 추출 실패 ({color_name}): {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    def extract_colors_batch(
        self,
        color_images: Dict[str, str],
        product_type: str = "의류"
    ) -> Dict[str, Optional[str]]:
        """
        여러 색상 이미지를 일괄 처리

        Args:
            color_images: {color_name: image_path} 딕셔너리
            product_type: 제품 타입

        Returns:
            {color_name: hex_code} 딕셔너리
        """
        results = {}

        for color_name, image_path in color_images.items():
            hex_code = self.extract_color_hex(image_path, color_name, product_type)
            results[color_name] = hex_code

        return results


def main():
    """테스트용 메인 함수"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 ai_color_extractor_dana.py <image_path> <color_name>")
        print("Example: python3 ai_color_extractor_dana.py output/assets/images/DN25SPT008_color_1.jpg '베이지'")
        sys.exit(1)

    image_path = sys.argv[1]
    color_name = sys.argv[2]

    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 색상 추출
    extractor = ColorExtractor()
    hex_code = extractor.extract_color_hex(image_path, color_name, "니트")

    if hex_code:
        print(f"\n✅ 결과: {color_name} → {hex_code}")
    else:
        print(f"\n❌ 실패: HEX 코드를 추출하지 못했습니다")
        sys.exit(1)


if __name__ == "__main__":
    main()
