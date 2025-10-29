"""
Figma 템플릿 기반 HTML 페이지 생성 (Editable 버전 V4)

V4 수정사항 (V3 문제 해결):
1. ✅ V3 성공 사항 유지: .info 제거, .selected 제거, 컬러 칩 표시
2. 🔧 이미지 왜곡 수정: inline object-fit 제거 함수 삭제 (원본 유지)
3. 🎨 진짜 스포이드 도구 구현: Canvas 기반 색상 추출 + 컬러 칩 업데이트

실행 방법:
  python examples/generate_figma_editable_v4.py
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from googleapiclient.errors import HttpError

# 프로젝트 루트를 sys.path에 추가 (모듈 임포트용)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 현재 작업 디렉토리 (파일 경로용)
cwd = Path.cwd()

# .env 파일 로드 (CWD 기준)
env_file = cwd / ".env"
if env_file.exists():
    load_dotenv(env_file)

from src.sheets_loader.loader import SheetsLoader
from src.sheets_loader.product_builder import ProductDataBuilder


def build_image_list(product):
    """ProductData에서 모든 이미지 리스트 생성"""
    image_list = []

    # 메인 이미지
    if product.main_image:
        image_list.append({
            "id": "mainImage",
            "label": "메인 이미지",
            "type": "main"
        })

    # 색상 이미지 (color_hex 포함)
    for i, color in enumerate(product.colors):
        image_list.append({
            "id": f"color{i+1}",
            "label": f"컬러 {color.color_name}",
            "type": "color",
            "color_name": color.color_name,
            "color_hex": color.color_hex
        })

    # 갤러리 이미지
    for color_name, images in product.gallery_by_color.items():
        if isinstance(images, list):
            for j, img_url in enumerate(images):
                image_list.append({
                    "id": f"gallery_{color_name}_{j+1}",
                    "label": f"{color_name} - 갤러리 {j+1}",
                    "type": "gallery"
                })

    # 디테일 포인트 이미지
    for i, point in enumerate(product.detail_points):
        image_list.append({
            "id": f"detail{i+1}",
            "label": f"디테일 포인트 {i+1}",
            "type": "detail"
        })

    # 소재 이미지
    if product.fabric_info and product.fabric_info.fabric_image:
        image_list.append({
            "id": "fabricImage",
            "label": "소재 이미지",
            "type": "fabric"
        })

    # 체크포인트 이미지
    if product.checkpoint and product.checkpoint.checkpoint_image:
        image_list.append({
            "id": "checkpointImage",
            "label": "체크포인트 이미지",
            "type": "checkpoint"
        })

    # 모델 이미지
    for i, model in enumerate(product.model_info):
        if model.model_image:
            image_list.append({
                "id": f"model{i+1}",
                "label": f"모델 {i+1}",
                "type": "model"
            })

    return image_list


def remove_info_sections(soup):
    """
    .info 클래스를 가진 div 제거 (제품 정보 박스, 푸터 등)
    """
    info_divs = soup.find_all('div', class_='info')
    removed_count = 0
    for div in info_divs:
        div.decompose()
        removed_count += 1

    if removed_count > 0:
        print(f"   ✅ {removed_count}개 .info 섹션 제거 완료")
    return soup


def add_color_selector_styles(soup):
    """
    Color Selector와 Lifestyle Gallery 섹션의 컬러 칩에 클릭 가능 표시 추가
    """
    total_chips = 0

    # 1. Color Selector 섹션 (26x26px 컬러칩)
    color_selector = soup.find('div', class_='section--color-selector')
    if color_selector:
        color_chips = color_selector.find_all('div', style=lambda s: s and '26px' in s)
        for chip in color_chips:
            style = chip.get('style', '')
            if 'cursor' not in style:
                chip['style'] = style + ' cursor: pointer; transition: transform 0.2s ease;'
            chip['class'] = chip.get('class', []) + ['color-chip-clickable', 'color-chip-selector']
        total_chips += len(color_chips)
        print(f"   ✅ Color Selector: {len(color_chips)}개 컬러 칩 발견")
    else:
        print("   ⚠️ Color Selector 섹션을 찾을 수 없습니다")

    # 2. Lifestyle Gallery 섹션 (42x42px 컬러칩)
    lifestyle_gallery = soup.find('div', class_='section--lifestyle-gallery')
    if lifestyle_gallery:
        gallery_chips = lifestyle_gallery.find_all('div', style=lambda s: s and '42px' in s and 'background' in s)
        for chip in gallery_chips:
            style = chip.get('style', '')
            if 'cursor' not in style:
                chip['style'] = style + ' cursor: pointer; transition: transform 0.2s ease;'
            chip['class'] = chip.get('class', []) + ['color-chip-clickable', 'color-chip-gallery']
        total_chips += len(gallery_chips)
        print(f"   ✅ Lifestyle Gallery: {len(gallery_chips)}개 컬러 칩 발견")
    else:
        print("   ⚠️ Lifestyle Gallery 섹션을 찾을 수 없습니다")

    print(f"   ✅ 총 {total_chips}개 컬러 칩에 클릭 표시 추가 완료")
    return soup


def add_gallery_section_indexes(soup, product):
    """
    V4.2: 모든 Lifestyle Gallery 섹션에 data-gallery-index와 data-gallery-color 속성 추가
    """
    gallery_sections = soup.find_all('div', class_='section--lifestyle-gallery')

    if not gallery_sections:
        print("   ⚠️ Lifestyle Gallery 섹션을 찾을 수 없습니다")
        return soup

    # product.colors에서 색상 이름 추출
    color_names = [color.color_name for color in product.colors] if product.colors else []

    for idx, section in enumerate(gallery_sections):
        section['data-gallery-index'] = str(idx)

        # 색상 이름 추가 (범위 내에 있으면)
        if idx < len(color_names):
            section['data-gallery-color'] = color_names[idx]
        else:
            section['data-gallery-color'] = f"색상{idx + 1}"

    print(f"   ✅ {len(gallery_sections)}개 갤러리 섹션에 인덱스 부여 완료")
    return soup


def wrap_images_with_frames_sequential(soup, image_list):
    """
    BeautifulSoup으로 이미지를 image-frame으로 감싸기

    순차적 매칭: HTML의 이미지 순서와 image_list 순서가 일치한다고 가정
    """
    all_imgs = soup.find_all('img')

    print(f"   총 {len(all_imgs)}개 이미지 발견")
    print(f"   이미지 리스트: {len(image_list)}개")

    # 순차적으로 매칭
    for idx, img in enumerate(all_imgs):
        # 이미 image-frame으로 감싸진 경우 스킵
        if img.parent and img.parent.get('class') and 'image-frame' in img.parent.get('class', []):
            continue

        # image_list 범위 내에서 ID 할당
        if idx < len(image_list):
            image_id = image_list[idx]["id"]
        else:
            # 범위 초과 시 임시 ID
            image_id = f"unknown_{idx}"

        # div.image-frame으로 감싸기
        frame = soup.new_tag('div', **{
            'class': 'image-frame',
            'data-id': image_id,
            'style': img.get('style', '')  # 원본 스타일 유지
        })

        # img 스타일 제거 (frame으로 이동)
        img['style'] = ''
        img['class'] = img.get('class', []) + ['editable-image']

        # img를 frame으로 감싸기
        img.wrap(frame)

    print(f"   ✅ {len(all_imgs)}개 이미지를 image-frame으로 감쌌습니다")


def generate_editable_html(product, loader: SheetsLoader) -> str:
    """
    Editable HTML 생성 (이미지 편집 가능)

    Args:
        product: ProductData 인스턴스
        loader: SheetsLoader 인스턴스 (이미지 다운로드용)

    Returns:
        HTML 문자열 (base64 이미지 포함, editable 기능 탑재)
    """
    # 기존 generate_html 함수를 import하여 사용
    from scripts.generate_final_html import generate_html as generate_base_html

    print("📝 기본 HTML 생성 중...")
    base_html = generate_base_html(product, loader)

    print("✏️ Editable 기능 추가 중...")

    # BeautifulSoup으로 파싱
    soup = BeautifulSoup(base_html, 'html.parser')

    # V4 수정 1: .info 섹션 제거 (V3에서 유지)
    print("   🗑️ .info 섹션 제거 중...")
    soup = remove_info_sections(soup)

    # V4 수정 2: inline object-fit 제거 함수 **삭제** (이미지 왜곡 방지)
    print("   ✅ inline object-fit 유지 (이미지 왜곡 방지)")

    # V4 수정 3: Color Selector 컬러 칩에 클릭 표시 (V3에서 유지)
    print("   🎨 컬러 칩 클릭 표시 추가 중...")
    soup = add_color_selector_styles(soup)

    # V4.2: 갤러리 섹션에 인덱스 부여
    print("   📋 갤러리 섹션 인덱스 부여 중...")
    soup = add_gallery_section_indexes(soup, product)

    # imageList 동적 생성
    print("   🎯 이미지 리스트 생성 중...")
    image_list = build_image_list(product)
    print(f"   총 {len(image_list)}개 이미지 발견")

    # 이미지를 image-frame으로 감싸기 (순차적 매칭)
    print("   🖼️  이미지 frame 래핑 중...")
    wrap_images_with_frames_sequential(soup, image_list)

    # html2canvas 스크립트 추가 (head에)
    head = soup.find('head')
    if head:
        html2canvas_script = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js')
        head.append(html2canvas_script)

    # CSS 추가 (V4: object-fit 수정)
    style_tag = soup.find('style')
    if style_tag:
        additional_css = '''
        /* Editable image frame */
        .image-frame {
            position: relative;
            overflow: hidden;
            cursor: move;
        }

        .image-frame.selected {
            border: 3px solid #4CAF50;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
        }

        /* V4: 고정 뷰포트 + 전체 원본 이미지 (position absolute로 변경) */
        .editable-image {
            width: auto !important;
            height: auto !important;
            max-width: none;
            max-height: none;
            position: absolute;
            top: 0;
            left: 0;
            transform-origin: top left;
            transition: none;
        }

        /* V4: Eyedropper mode cursor */
        body.eyedropper-active {
            cursor: crosshair !important;
        }

        body.eyedropper-active * {
            cursor: crosshair !important;
        }

        /* Color chip clickable styles */
        .color-chip-clickable:hover {
            transform: scale(1.1);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }

        /* Control Panel */
        .control-panel {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 20px;
            border: 2px solid #333;
            z-index: 9999;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            width: 320px;
            max-height: 90vh;
            overflow-y: auto;
        }

        /* Container transform */
        .container {
            transform-origin: top center;
            transition: transform 0.2s ease;
        }

        /* Color picker display */
        .color-display {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }

        .color-swatch {
            width: 40px;
            height: 40px;
            border-radius: 4px;
            border: 2px solid #ccc;
        }

        /* Thumbnail grid styles */
        .thumbnail-item {
            cursor: pointer;
            border: 2px solid transparent;
            border-radius: 4px;
            overflow: hidden;
            transition: all 0.2s ease;
            position: relative;
            background: #fff;
        }

        .thumbnail-item:hover {
            border-color: #007bff;
            transform: scale(1.05);
            box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
        }

        .thumbnail-item.selected {
            border-color: #28a745;
            box-shadow: 0 0 8px rgba(40, 167, 69, 0.5);
        }

        .thumbnail-item img {
            width: 100%;
            height: 80px;
            object-fit: cover;
            display: block;
        }

        .thumbnail-item .thumbnail-label {
            padding: 4px;
            font-size: 9px;
            text-align: center;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* V4.3: Text element selection and resize handles */
        .text-selected {
            outline: 2px dashed #ff9800 !important;
            outline-offset: 2px;
            overflow: visible !important;
        }

        .resize-handle {
            position: absolute;
            background: #ff9800;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            z-index: 10000;
            pointer-events: auto;
        }

        .resize-handle-top {
            width: 40px;
            height: 8px;
            top: -4px;
            left: 50%;
            transform: translateX(-50%);
            cursor: ns-resize;
        }

        .resize-handle-right {
            width: 8px;
            height: 40px;
            right: -4px;
            top: 50%;
            transform: translateY(-50%);
            cursor: ew-resize;
        }

        .resize-handle-bottom {
            width: 40px;
            height: 8px;
            bottom: -4px;
            left: 50%;
            transform: translateX(-50%);
            cursor: ns-resize;
        }

        .resize-handle-left {
            width: 8px;
            height: 40px;
            left: -4px;
            top: 50%;
            transform: translateY(-50%);
            cursor: ew-resize;
        }

        .resize-handle:hover {
            background: #f57c00;
        }
        '''
        style_tag.string = style_tag.string + additional_css

    # Control panel HTML 생성 (V4: 스포이드 도구 개선)
    control_panel_html = f'''
    <div class="control-panel">
        <h3 style="margin: 0 0 20px 0; font-size: 18px; font-weight: bold; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px;">
            이미지 편집 도구
        </h3>

        <!-- V4: Real Eyedropper Tool -->
        <div style="margin-bottom: 20px; padding: 15px; background: #f0f8ff; border-radius: 6px; border-left: 4px solid #0066cc;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #003d82;">🎨 스포이드 도구</h4>
            <button id="eyedropper-btn" onclick="activateEyedropper()" style="width: 100%; padding: 10px; background: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 600; margin-bottom: 10px;">
                🔍 스포이드 활성화
            </button>
            <div id="eyedropper-status" style="font-size: 12px; color: #666; line-height: 1.5;">
                💡 버튼 클릭 → 이미지 클릭 → 색상 추출
            </div>
            <div id="eyedropper-result" class="color-display" style="display: none; margin-top: 10px;">
                <div id="extracted-swatch" class="color-swatch"></div>
                <div style="flex: 1;">
                    <div id="extracted-hex" style="font-weight: bold; font-size: 13px; font-family: 'Courier New', monospace;"></div>
                    <div style="font-size: 11px; color: #666;">추출된 색상</div>
                </div>
            </div>
        </div>

        <!-- Page Zoom -->
        <div style="margin-bottom: 20px; padding: 15px; background: #e7f3ff; border-radius: 6px;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">🖥️ 페이지 줌</h4>
            <div>
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    화면 표시: <span id="page-zoom-value" style="font-weight: bold; color: #0066cc;">60%</span>
                </label>
                <input type="range" id="page-zoom" min="30" max="100" value="60" step="5" style="width: 100%;">
            </div>
        </div>

        <!-- Image Selector -->
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 8px; font-size: 13px; font-weight: 600;">📷 이미지 선택</label>
            <select id="image-select" style="width: 100%; padding: 8px; font-size: 13px; border: 1px solid #ccc; border-radius: 4px;">
                <!-- Options populated by JavaScript -->
            </select>
        </div>

        <!-- Image Replace Section -->
        <div style="margin-bottom: 20px; padding: 15px; background: #fff8dc; border-radius: 6px; border-left: 4px solid #ffa500;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #cc6600;">🖼️ 이미지 교체</h4>

            <!-- Option 1: Internal Image Selection (Thumbnail Grid) -->
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 8px; font-size: 12px; font-weight: 600;">
                    내부 이미지 선택 (썸네일 클릭)
                </label>

                <!-- Thumbnail Grid Container -->
                <div id="thumbnail-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; max-height: 300px; overflow-y: auto; padding: 8px; background: #f9f9f9; border-radius: 4px; margin-bottom: 10px;">
                    <!-- Thumbnails populated by JavaScript -->
                </div>

                <button onclick="replaceFromInternal()" style="width: 100%; padding: 8px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                    ✅ 적용
                </button>
            </div>

            <!-- Option 2: File Upload -->
            <div style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px; font-weight: 600;">
                    파일 업로드
                </label>
                <input type="file" id="replace-image-file" accept="image/*" style="width: 100%; padding: 6px; font-size: 11px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 8px;">
                <button onclick="replaceFromFile()" style="width: 100%; padding: 8px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                    📤 업로드 및 적용
                </button>
            </div>

            <!-- Crop Settings Option -->
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #ddd;">
                <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; cursor: pointer; margin-bottom: 8px;">
                    <input type="checkbox" id="keep-crop-settings" checked style="cursor: pointer;">
                    <span>크롭 설정 유지</span>
                </label>
                <div style="font-size: 10px; color: #666; margin-top: 8px; line-height: 1.5; background: #f0f8ff; padding: 8px; border-radius: 4px;">
                    💡 <strong>전체 원본 이미지가 이미 로드되어 있습니다!</strong><br>
                    확대/이동 슬라이더로 숨겨진 영역까지 자유롭게 탐색할 수 있습니다.
                </div>
            </div>
        </div>

        <!-- Image Add Section (NEW) -->
        <div style="margin-bottom: 20px; padding: 15px; background: #e8f5e9; border-radius: 6px; border-left: 4px solid #4caf50;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #2e7d32;">➕ 이미지 추가 (갤러리)</h4>

            <!-- Color Selection -->
            <div style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px; font-weight: 600;">
                    컬러 선택
                </label>
                <select id="add-image-color-select" style="width: 100%; padding: 6px; font-size: 12px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 8px;">
                    <option value="">-- 컬러 선택 --</option>
                </select>
            </div>

            <!-- File Upload -->
            <div style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px; font-weight: 600;">
                    이미지 파일
                </label>
                <input type="file" id="add-image-file" accept="image/*" style="width: 100%; padding: 6px; font-size: 11px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 8px;">
            </div>

            <button onclick="addImageToGallery()" style="width: 100%; padding: 10px; background: #4caf50; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                ✅ 갤러리에 추가
            </button>

            <div style="font-size: 10px; color: #2e7d32; margin-top: 8px; line-height: 1.5;">
                💡 선택한 컬러의 라이프스타일 갤러리에 이미지 컨테이너가 추가됩니다.
            </div>
        </div>

        <!-- Image Delete Section -->
        <div style="margin-bottom: 20px; padding: 15px; background: #ffe6e6; border-radius: 6px; border-left: 4px solid #dc3545;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #c82333;">🗑️ 이미지 삭제</h4>
            <div style="font-size: 11px; color: #721c24; margin-bottom: 10px; padding: 8px; background: #f8d7da; border-radius: 4px;">
                ⚠️ 삭제된 이미지는 투명 영역으로 대체됩니다
            </div>
            <button onclick="deleteCurrentImage()" style="width: 100%; padding: 10px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                ❌ 선택한 이미지 삭제
            </button>
        </div>

        <!-- Position Controls -->
        <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 6px;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">🎯 위치 조절</h4>

            <div style="margin-bottom: 12px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    좌우 (X): <span id="x-value" style="font-weight: bold; color: #007bff;">100%</span>
                </label>
                <input type="range" id="position-x" min="0" max="200" value="100" step="1" style="width: 100%;">
            </div>

            <div style="margin-bottom: 0;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    상하 (Y): <span id="y-value" style="font-weight: bold; color: #007bff;">100%</span>
                </label>
                <input type="range" id="position-y" min="0" max="200" value="100" step="1" style="width: 100%;">
            </div>
        </div>

        <!-- Scale Control -->
        <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 6px;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">🔍 확대/축소</h4>
            <div>
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    크기: <span id="scale-value" style="font-weight: bold; color: #28a745;">100%</span>
                </label>
                <input type="range" id="scale" min="50" max="500" value="100" step="1" style="width: 100%;">
            </div>
        </div>

        <!-- Reset Buttons -->
        <div style="margin-bottom: 20px; padding: 15px; background: #f8d7da; border-radius: 6px;">
            <h4 style="margin: 0 0 10px 0; font-size: 14px; font-weight: 600;">🔄 리셋</h4>
            <button onclick="resetCurrentImage()" style="width: 100%; padding: 8px; margin-bottom: 8px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                현재 이미지 리셋
            </button>
        </div>

        <!-- Gap Control (V4.3: Unified Gallery/Detail/Hero) -->
        <div style="margin-bottom: 20px; padding: 15px; background: #e8f5e9; border-radius: 6px;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">📐 이미지 간격 조정</h4>

            <!-- V4.3: Gap Type Selector -->
            <div style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    조정 대상:
                </label>
                <select id="gap-type-selector" style="width: 100%; padding: 6px; border: 1px solid #2e7d32; border-radius: 4px; font-size: 12px; background: white; cursor: pointer;">
                    <option value="gallery">갤러리 이미지 간격</option>
                    <option value="detail">디테일 섹션 간격</option>
                    <option value="hero">히어로-상품명 간격</option>
                </select>
            </div>

            <!-- V4.3: Gallery Section Selector (conditionally visible) -->
            <div id="gallery-section-selector-wrapper" style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    섹션 선택:
                </label>
                <select id="gallery-section-selector" style="width: 100%; padding: 6px; border: 1px solid #2e7d32; border-radius: 4px; font-size: 12px; background: white; cursor: pointer;">
                    <option value="all">전체 갤러리 (일괄 적용)</option>
                    <!-- 섹션 옵션은 JavaScript에서 동적 생성 -->
                </select>
            </div>

            <div>
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    간격: <span id="gap-value" style="font-weight: bold; color: #2e7d32;">21px</span>
                </label>
                <input type="range" id="gap-slider" min="0" max="300" value="21" step="1" style="width: 100%;">
            </div>

            <div id="gap-help-text" style="font-size: 10px; color: #2e7d32; margin-top: 8px; line-height: 1.5;">
                💡 갤러리 섹션의 이미지 간격을 조절합니다.
            </div>
        </div>

        <!-- Text Box Size Control (V4.2: Click to Select) -->
        <div id="text-box-control" style="display: none; margin-bottom: 20px; padding: 15px; background: #fff8e1; border-radius: 6px;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600;">📏 텍스트 박스 크기 조절</h4>

            <div style="margin-bottom: 10px; padding: 8px; background: #fff; border-radius: 4px; border: 1px solid #f57c00;">
                <div style="font-size: 11px; font-weight: 600; color: #666; margin-bottom: 5px;">선택된 요소:</div>
                <div id="selected-text-info" style="font-size: 12px; color: #333;">없음</div>
                <button id="deselect-text" onclick="deselectTextElement()" style="margin-top: 8px; width: 100%; padding: 6px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: 600;">
                    선택 해제
                </button>
            </div>

            <div style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    너비 (Width): <span id="text-width-value" style="font-weight: bold; color: #f57c00;">auto</span>
                </label>
                <input type="range" id="text-width" min="50" max="2000" value="200" step="10" style="width: 100%;">
            </div>

            <div style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    높이 (Height): <span id="text-height-value" style="font-weight: bold; color: #f57c00;">auto</span>
                </label>
                <input type="range" id="text-height" min="20" max="500" value="50" step="5" style="width: 100%;">
            </div>

            <div style="margin-bottom: 0;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px;">
                    글자 크기 (Font Size): <span id="text-fontsize-value" style="font-weight: bold; color: #f57c00;">14px</span>
                </label>
                <input type="range" id="text-fontsize" min="8" max="100" value="14" step="1" style="width: 100%;">
            </div>

            <div style="font-size: 10px; color: #f57c00; margin-top: 8px; line-height: 1.5;">
                💡 텍스트 요소를 클릭하여 선택한 후 크기를 조절하세요.
            </div>
        </div>

        <!-- Text Edit Mode Toggle + Format Tools -->
        <div style="margin-bottom: 20px; padding: 15px; background: #fff3cd; border-radius: 6px; border-left: 4px solid #ffc107;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #856404;">✏️ 텍스트 편집</h4>
            <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; cursor: pointer; margin-bottom: 12px;">
                <input type="checkbox" id="text-edit-mode" onchange="toggleTextEditing()" style="cursor: pointer;">
                <span>텍스트 편집 모드</span>
            </label>

            <!-- Format Toolbar (shown when edit mode is active) -->
            <div id="format-toolbar" style="display: none; margin-top: 12px; padding: 10px; background: #fff; border-radius: 4px; border: 1px solid #ddd;">
                <div style="margin-bottom: 8px; font-size: 11px; font-weight: 600; color: #666;">서식 도구:</div>

                <div style="display: flex; gap: 6px; margin-bottom: 10px;">
                    <button onclick="formatText('bold')" style="flex: 1; padding: 8px; background: #333; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: bold;" title="볼드 (Ctrl+B)">
                        <b>B</b> 볼드
                    </button>
                    <button onclick="formatText('removeFormat')" style="flex: 1; padding: 8px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 11px;" title="서식 제거">
                        ❌ 제거
                    </button>
                </div>

                <div style="margin-bottom: 0;">
                    <label style="display: block; margin-bottom: 6px; font-size: 11px; font-weight: 600;">글씨 크기:</label>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <button onclick="decreaseFontSize()" style="padding: 8px 12px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold;" title="글씨 크기 감소 (바로 적용)">
                            −
                        </button>
                        <input type="number" id="font-size-input" value="24" min="10" max="100" step="1" style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; text-align: center; font-size: 12px;" />
                        <button onclick="increaseFontSize()" style="padding: 8px 12px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold;" title="글씨 크기 증가 (바로 적용)">
                            +
                        </button>
                    </div>
                </div>
            </div>

            <div style="font-size: 10px; color: #856404; margin-top: 8px; line-height: 1.5;">
                💡 텍스트를 선택한 후 서식 도구를 사용하세요.
            </div>
        </div>

        <!-- Export Buttons -->
        <div style="margin-top: 20px; display: flex; gap: 10px; flex-direction: column;">
            <button onclick="exportHTML()" style="width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold;">
                ✅ HTML 다운로드
            </button>
            <button onclick="exportAsJPG()" style="width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold;">
                🖼️ 전체 페이지 JPG (타일링)
            </button>
        </div>
    </div>
    '''

    # Prepare JSON data for JavaScript (to avoid f-string format issues)
    image_list_json = json.dumps(image_list, ensure_ascii=False)

    # JavaScript 생성 (V4: 진짜 스포이드 도구 구현)
    javascript_code_template = '''
    <script>
        // Product code for localStorage
        const productCode = '__PRODUCT_CODE__';

        // Image list (generated from ProductData)
        const imageList = __IMAGE_LIST__;

        // Crop settings storage (V4: version field added)
        const cropSettings = {{
            version: 'v4',  // V4 version identifier for localStorage
            productCode: productCode,
            images: {{}}
        }};

        // Initialize crop settings
        imageList.forEach(img => {{
            cropSettings.images[img.id] = {{ x: 100, y: 100, scale: 100 }};
        }});

        // Current selected image
        let currentImageId = imageList.length > 0 ? imageList[0].id : null;

        // Selected thumbnail for replacement
        let selectedThumbnailId = null;

        // Page zoom level
        let pageZoom = 60;

        // Drag state
        let isDragging = false;
        let startX, startY, startObjX, startObjY;

        // V4: Eyedropper state
        let eyedropperActive = false;
        let extractedColor = null;

        // V4: Text edit mode
        let textEditMode = false;

        // V4.1: Gallery gap and text padding
        // V4.2: Changed to per-section gallery gaps
        // V4.3: Unified gap settings for gallery/detail/hero
        let gapSettings = {{
            gallery: {{all: 21}},  // Stores: section_index -> gap_px, all -> gap_px
            detail: 161,           // Detail section gap (single value)
            hero: 60               // Hero to product name spacing (single value)
        }};
        let currentGapType = 'gallery';         // Current gap type being edited
        let selectedGallerySection = 'all';     // Selected gallery section (only for gallery type)

        // V4.2: Text box size control (replaced padding)
        let selectedTextElement = null;  // Currently selected text element
        let textElementIdCounter = 0;    // Auto-increment ID for text elements
        let textSizes = {{}};              // Stores: element_id -> (width, height, fontSize)

        // V4: Toggle text editing
        function toggleTextEditing() {{
            textEditMode = !textEditMode;
            const formatToolbar = document.getElementById('format-toolbar');

            if (textEditMode) {{
                // Show format toolbar
                formatToolbar.style.display = 'block';

                // Enable text editing on all text elements
                document.querySelectorAll('.container *').forEach(el => {{
                    // 텍스트를 포함하고 이미지가 아닌 요소만
                    if (el.childNodes.length > 0 &&
                        !el.querySelector('img') &&
                        !el.classList.contains('control-panel') &&
                        !el.classList.contains('image-frame') &&
                        !el.closest('.control-panel')) {{

                        // 직접 텍스트 노드를 포함하는 요소만
                        let hasDirectText = false;
                        el.childNodes.forEach(node => {{
                            if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {{
                                hasDirectText = true;
                            }}
                        }});

                        if (hasDirectText || (el.innerText && el.innerText.trim() && el.children.length === 0)) {{
                            el.setAttribute('contenteditable', 'true');
                            el.style.outline = '1px dashed #007bff';
                            el.style.outlineOffset = '2px';
                        }}
                    }}
                }});
                console.log('✏️ 텍스트 편집 모드 활성화');
            }} else {{
                // Hide format toolbar
                formatToolbar.style.display = 'none';

                // Disable text editing
                document.querySelectorAll('[contenteditable="true"]').forEach(el => {{
                    el.removeAttribute('contenteditable');
                    el.style.outline = '';
                    el.style.outlineOffset = '';
                }});
                console.log('✏️ 텍스트 편집 모드 비활성화');
            }}
        }}

        // Format text (bold or remove formatting)
        function formatText(command) {{
            if (!textEditMode) {{
                alert('⚠️ 먼저 텍스트 편집 모드를 활성화하세요!');
                return;
            }}

            try {{
                if (command === 'bold') {{
                    document.execCommand('bold', false, null);
                    console.log('✅ 볼드 적용');
                }} else if (command === 'removeFormat') {{
                    document.execCommand('removeFormat', false, null);
                    console.log('✅ 서식 제거');
                }}
            }} catch (e) {{
                console.error('서식 적용 실패:', e);
                alert('❌ 서식 적용 실패: ' + e.message);
            }}
        }}

        // Apply font size to selected text (helper function)
        function applyFontSizeToSelection(size) {{
            if (!textEditMode) {{
                alert('⚠️ 먼저 텍스트 편집 모드를 활성화하세요!');
                return false;
            }}

            try {{
                const selection = window.getSelection();
                if (!selection.rangeCount) {{
                    alert('⚠️ 텍스트를 먼저 선택하세요!');
                    return false;
                }}

                const range = selection.getRangeAt(0);
                const selectedText = range.toString();

                if (!selectedText) {{
                    alert('⚠️ 텍스트를 먼저 선택하세요!');
                    return false;
                }}

                // Create a span element with the desired font size
                const span = document.createElement('span');
                span.style.fontSize = size;
                span.textContent = selectedText;

                // Replace the selected text with the span
                range.deleteContents();
                range.insertNode(span);

                // Re-select the newly inserted span to maintain selection
                const newRange = document.createRange();
                newRange.selectNodeContents(span);
                selection.removeAllRanges();
                selection.addRange(newRange);

                console.log(`✅ 글씨 크기 ${{size}} 적용`);
                return true;
            }} catch (e) {{
                console.error('글씨 크기 변경 실패:', e);
                alert('❌ 글씨 크기 변경 실패: ' + e.message);
                return false;
            }}
        }}

        // Decrease font size and apply immediately
        function decreaseFontSize() {{
            const input = document.getElementById('font-size-input');
            const currentSize = parseInt(input.value);
            const newSize = Math.max(10, currentSize - 2);  // Min 10px
            input.value = newSize;

            // Apply immediately
            applyFontSizeToSelection(newSize + 'px');
        }}

        // Increase font size and apply immediately
        function increaseFontSize() {{
            const input = document.getElementById('font-size-input');
            const currentSize = parseInt(input.value);
            const newSize = Math.min(100, currentSize + 2);  // Max 100px
            input.value = newSize;

            // Apply immediately
            applyFontSizeToSelection(newSize + 'px');
        }}

        // Initialize
        function init() {{
            console.log('✅ Editable mode V4.2 initialized');
            console.log(`📷 Total images: ${{imageList.length}}`);
            populateImageSelect();
            populateThumbnailGrid();  // NEW: Populate thumbnail grid instead of dropdown
            populateAddImageColorSelect();  // NEW: Populate color dropdown for adding images
            populateGallerySectionSelector();  // V4.2: Populate gallery section dropdown
            loadSettings();
            applyPageZoom();
            applyGap();              // V4.3 FIX: Apply gallery gap (per-section)
            setupEventListeners();
            setupColorChipHandlers();
            selectImage(currentImageId);
        }}

        // V4.2: Populate gallery section selector dropdown
        function populateGallerySectionSelector() {{
            const selector = document.getElementById('gallery-section-selector');
            const sections = document.querySelectorAll('.section--lifestyle-gallery[data-gallery-index]');

            sections.forEach(section => {{
                const index = section.getAttribute('data-gallery-index');
                const color = section.getAttribute('data-gallery-color');
                const option = document.createElement('option');
                option.value = index;
                option.textContent = `${{color}} 갤러리`;
                selector.appendChild(option);
            }});

            console.log(`📋 갤러리 섹션 드롭다운 생성: ${{sections.length}}개`);
        }}

        // Populate image dropdown
        function populateImageSelect() {{
            const select = document.getElementById('image-select');
            imageList.forEach(img => {{
                const option = document.createElement('option');
                option.value = img.id;
                option.textContent = img.label;
                select.appendChild(option);
            }});
        }}

        // Populate thumbnail grid
        function populateThumbnailGrid() {{
            const grid = document.getElementById('thumbnail-grid');
            if (!grid) {{
                console.error('❌ Thumbnail grid not found');
                return;
            }}

            // Clear existing thumbnails
            grid.innerHTML = '';

            imageList.forEach(img => {{
                // Find the actual image element in the DOM
                const frame = document.querySelector(`[data-id="${{img.id}}"]`);
                const imgElement = frame?.querySelector('.editable-image');

                if (!imgElement) {{
                    console.warn(`⚠️ Image not found for ${{img.id}}`);
                    return;
                }}

                // Create thumbnail container
                const thumbnailDiv = document.createElement('div');
                thumbnailDiv.className = 'thumbnail-item';
                thumbnailDiv.setAttribute('data-image-id', img.id);

                // Create thumbnail image
                const thumbnailImg = document.createElement('img');
                thumbnailImg.src = imgElement.src;
                thumbnailImg.alt = img.label;

                // Create label
                const label = document.createElement('div');
                label.className = 'thumbnail-label';
                label.textContent = img.label;

                // Append elements
                thumbnailDiv.appendChild(thumbnailImg);
                thumbnailDiv.appendChild(label);

                // Add click handler
                thumbnailDiv.addEventListener('click', () => {{
                    selectThumbnail(img.id);
                }});

                grid.appendChild(thumbnailDiv);
            }});

            console.log(`🖼️ ${{imageList.length}}개 썸네일 생성 완료`);
        }}

        // Select thumbnail for replacement
        function selectThumbnail(imageId) {{
            // Remove previous selection
            document.querySelectorAll('.thumbnail-item').forEach(item => {{
                item.classList.remove('selected');
            }});

            // Add selection to clicked thumbnail
            const selectedThumbnail = document.querySelector(`.thumbnail-item[data-image-id="${{imageId}}"]`);
            if (selectedThumbnail) {{
                selectedThumbnail.classList.add('selected');
                selectedThumbnailId = imageId;

                // Find image info
                const imageInfo = imageList.find(img => img.id === imageId);
                const label = imageInfo ? imageInfo.label : imageId;

                console.log(`👉 썸네일 선택: ${{label}}`);
            }}
        }}

        // Populate add image color dropdown
        function populateAddImageColorSelect() {{
            const select = document.getElementById('add-image-color-select');

            // Extract unique color names from imageList (color type only)
            const colorNames = new Set();
            imageList.forEach(img => {{
                if (img.type === 'color' && img.color_name) {{
                    colorNames.add(img.color_name);
                }}
            }});

            // Add options
            colorNames.forEach(colorName => {{
                const option = document.createElement('option');
                option.value = colorName;
                option.textContent = colorName;
                select.appendChild(option);
            }});

            console.log(`🎨 컬러 드롭다운에 ${{colorNames.size}}개 컬러 추가됨`);
        }}

        // Add image to gallery
        function addImageToGallery() {{
            const colorSelect = document.getElementById('add-image-color-select');
            const fileInput = document.getElementById('add-image-file');

            // Validation
            if (!colorSelect.value) {{
                alert('⚠️ 컬러를 먼저 선택하세요!');
                return;
            }}

            if (!fileInput.files || fileInput.files.length === 0) {{
                alert('⚠️ 이미지 파일을 선택하세요!');
                return;
            }}

            const selectedColor = colorSelect.value;
            const file = fileInput.files[0];

            if (!file.type.startsWith('image/')) {{
                alert('❌ 이미지 파일만 업로드할 수 있습니다!');
                return;
            }}

            // Read file as base64
            const reader = new FileReader();
            reader.onload = function(e) {{
                const imageData = e.target.result;

                // Find lifestyle gallery section
                const lifestyleGallery = document.querySelector('.section--lifestyle-gallery');
                if (!lifestyleGallery) {{
                    alert('❌ 라이프스타일 갤러리 섹션을 찾을 수 없습니다!');
                    return;
                }}

                // Find or create color group container
                let colorContainer = null;
                const allContainers = lifestyleGallery.querySelectorAll('[style*="margin-bottom: 56px"]');

                // Search for existing color container
                allContainers.forEach(container => {{
                    const colorChip = container.querySelector('[style*="42px"][style*="background"]');
                    if (colorChip) {{
                        const colorNameSpan = colorChip.parentElement?.querySelector('span');
                        if (colorNameSpan && colorNameSpan.textContent.trim() === selectedColor) {{
                            colorContainer = container;
                        }}
                    }}
                }});

                // Create new color container if not found
                if (!colorContainer) {{
                    alert(`⚠️ "${{selectedColor}}" 컬러의 갤러리 섹션을 찾을 수 없습니다.\\n\\n빈 컨테이너 생성 기능은 아직 구현되지 않았습니다.`);
                    return;
                }}

                // Create new image frame
                const newImageId = `gallery_${{selectedColor}}_added_${{Date.now()}}`;

                // Create image-frame div
                const imageFrame = document.createElement('div');
                imageFrame.className = 'image-frame';
                imageFrame.setAttribute('data-id', newImageId);
                imageFrame.style.cssText = 'width: 580px; height: 773px; margin-bottom: 20px; position: relative; overflow: hidden; cursor: move;';

                // Create img element
                const img = document.createElement('img');
                img.className = 'editable-image';
                img.src = imageData;
                img.style.cssText = 'position: absolute; top: 0; left: 0; width: auto; height: auto; max-width: none; max-height: none; transform-origin: top left;';

                // Append
                imageFrame.appendChild(img);

                // Find grid container (첫 번째 grid 컨테이너)
                const gridContainer = colorContainer.querySelector('[style*="display: grid"]');
                if (gridContainer) {{
                    gridContainer.appendChild(imageFrame);
                }} else {{
                    alert('❌ 이미지 그리드 컨테이너를 찾을 수 없습니다!');
                    return;
                }}

                // Add to imageList
                imageList.push({{
                    id: newImageId,
                    label: `${{selectedColor}} - 추가됨`,
                    type: 'gallery'
                }});

                // Add to cropSettings
                cropSettings.images[newImageId] = {{ x: 100, y: 100, scale: 100 }};

                // Wait for image to load, then apply transform
                img.onload = function() {{
                    const frameWidth = imageFrame.offsetWidth;
                    const frameHeight = imageFrame.offsetHeight;
                    const imgWidth = img.naturalWidth;
                    const imgHeight = img.naturalHeight;

                    const scaleX = frameWidth / imgWidth;
                    const scaleY = frameHeight / imgHeight;
                    const baseScale = Math.max(scaleX, scaleY);

                    img.style.transform = `translate(0px, 0px) scale(${{baseScale}})`;

                    console.log(`✅ 이미지 추가 완료: ${{newImageId}}`);
                    alert(`✅ "${{selectedColor}}" 갤러리에 이미지가 추가되었습니다!\\n\\n이미지를 클릭하여 편집할 수 있습니다.`);

                    // Select the new image
                    selectImage(newImageId);

                    // Re-setup event listeners for new image
                    setupEventListeners();
                }};

                // Clear file input
                fileInput.value = '';
            }};

            reader.onerror = function() {{
                alert('❌ 파일 읽기 실패!');
            }};

            reader.readAsDataURL(file);
        }}

        // Replace from internal image
        function replaceFromInternal() {{
            if (!selectedThumbnailId) {{
                alert('⚠️ 썸네일 그리드에서 교체할 이미지를 선택하세요!');
                return;
            }}

            if (!currentImageId) {{
                alert('⚠️ 먼저 편집할 이미지를 선택하세요!');
                return;
            }}

            const sourceFrame = document.querySelector(`[data-id="${{selectedThumbnailId}}"]`);
            const sourceImg = sourceFrame?.querySelector('.editable-image');
            if (!sourceImg) {{
                alert('❌ 선택한 이미지를 찾을 수 없습니다!');
                return;
            }}

            const keepCrop = document.getElementById('keep-crop-settings').checked;
            replaceImageSrc(sourceImg.src, keepCrop);
        }}

        // Replace from file upload
        function replaceFromFile() {{
            const fileInput = document.getElementById('replace-image-file');
            if (!fileInput.files || fileInput.files.length === 0) {{
                alert('⚠️ 업로드할 파일을 선택하세요!');
                return;
            }}

            if (!currentImageId) {{
                alert('⚠️ 먼저 편집할 이미지를 선택하세요!');
                return;
            }}

            const file = fileInput.files[0];
            if (!file.type.startsWith('image/')) {{
                alert('❌ 이미지 파일만 업로드할 수 있습니다!');
                return;
            }}

            const reader = new FileReader();
            reader.onload = function(e) {{
                const keepCrop = document.getElementById('keep-crop-settings').checked;
                replaceImageSrc(e.target.result, keepCrop);
                fileInput.value = '';
            }};
            reader.onerror = function() {{
                alert('❌ 파일 읽기 실패!');
            }};
            reader.readAsDataURL(file);
        }}

        // Core replacement logic (고정 뷰포트 + 전체 원본 이미지)
        function replaceImageSrc(newSrc, keepCrop) {{
            const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
            const img = frame?.querySelector('.editable-image');
            if (!img) {{
                alert('❌ 이미지를 찾을 수 없습니다!');
                return;
            }}

            // Replace image (frame size remains fixed)
            img.src = newSrc;

            // Reset crop settings if not keeping
            if (!keepCrop) {{
                cropSettings.images[currentImageId] = {{ x: 100, y: 100, scale: 100 }};
                updateSliders();
                applyCurrentCrop();
            }}

            autoSave();
            console.log(`✅ 이미지 교체 완료: ${{currentImageId}}`);
            alert(`✅ 이미지가 교체되었습니다!\\n${{keepCrop ? '크롭 설정 유지됨' : '크롭 설정 리셋됨'}}\\n\\n💡 전체 원본 이미지가 로드되었습니다. 확대/이동으로 숨겨진 영역을 탐색하세요!`);
        }}

        // Delete current image
        function deleteCurrentImage() {{
            if (!currentImageId) {{
                alert('⚠️ 먼저 삭제할 이미지를 선택하세요!');
                return;
            }}

            // Find image info
            const imageInfo = imageList.find(img => img.id === currentImageId);
            const imageName = imageInfo ? imageInfo.label : currentImageId;

            // Confirmation dialog
            const confirmed = confirm(`⚠️ "${{imageName}}" 이미지를 삭제하시겠습니까?\\n\\n삭제된 영역은 제거되고 아래 콘텐츠가 위로 올라옵니다.`);
            if (!confirmed) {{
                return;
            }}

            // Find frame
            const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
            if (!frame) {{
                alert('❌ 이미지를 찾을 수 없습니다!');
                return;
            }}

            // Animate and remove from DOM
            frame.style.transition = 'all 0.3s ease';
            frame.style.height = '0';
            frame.style.opacity = '0';
            frame.style.marginBottom = '0';
            frame.style.overflow = 'hidden';

            // Remove from DOM after animation
            setTimeout(() => {{
                frame.remove();
                console.log(`🗑️ 이미지 삭제 완료: ${{imageName}}`);

                // Select first available image
                const remainingFrames = document.querySelectorAll('.image-frame');
                if (remainingFrames.length > 0) {{
                    const firstFrame = remainingFrames[0];
                    const firstId = firstFrame.getAttribute('data-id');
                    selectImage(firstId);
                }} else {{
                    currentImageId = null;
                }}
            }}, 300);

            alert(`✅ "${{imageName}}" 이미지가 삭제됩니다!\\n\\n아래 콘텐츠가 위로 올라옵니다.`);
        }}

        // V4: Activate Eyedropper Tool
        function activateEyedropper() {{
            eyedropperActive = true;
            document.body.classList.add('eyedropper-active');
            document.getElementById('eyedropper-status').innerHTML = '🎯 <strong>이미지를 클릭하세요!</strong> (ESC로 취소)';
            document.getElementById('eyedropper-btn').style.background = '#ff6b6b';
            document.getElementById('eyedropper-btn').textContent = '❌ 취소 (ESC)';
            console.log('🔍 스포이드 도구 활성화');
        }}

        // V4: Deactivate Eyedropper Tool
        function deactivateEyedropper() {{
            eyedropperActive = false;
            document.body.classList.remove('eyedropper-active');
            document.getElementById('eyedropper-status').innerHTML = '💡 버튼 클릭 → 이미지 클릭 → 색상 추출';
            document.getElementById('eyedropper-btn').style.background = '#0066cc';
            document.getElementById('eyedropper-btn').textContent = '🔍 스포이드 활성화';
            console.log('🔍 스포이드 도구 비활성화');
        }}

        // V4: Extract color from image using Canvas
        function extractColorFromImage(imgElement, clientX, clientY) {{
            return new Promise((resolve, reject) => {{
                try {{
                    // Get click position relative to image
                    const rect = imgElement.getBoundingClientRect();
                    const x = clientX - rect.left;
                    const y = clientY - rect.top;

                    // Create canvas
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');

                    // Get image natural size
                    const img = new Image();
                    img.crossOrigin = 'anonymous';
                    img.onload = function() {{
                        canvas.width = img.naturalWidth;
                        canvas.height = img.naturalHeight;

                        // Draw image
                        ctx.drawImage(img, 0, 0);

                        // Calculate pixel position in natural size
                        const scaleX = img.naturalWidth / rect.width;
                        const scaleY = img.naturalHeight / rect.height;
                        const pixelX = Math.floor(x * scaleX);
                        const pixelY = Math.floor(y * scaleY);

                        // Get pixel data (5x5 area for averaging)
                        const size = 5;
                        const halfSize = Math.floor(size / 2);
                        let r = 0, g = 0, b = 0, count = 0;

                        for (let dy = -halfSize; dy <= halfSize; dy++) {{
                            for (let dx = -halfSize; dx <= halfSize; dx++) {{
                                const px = pixelX + dx;
                                const py = pixelY + dy;
                                if (px >= 0 && px < canvas.width && py >= 0 && py < canvas.height) {{
                                    const imageData = ctx.getImageData(px, py, 1, 1);
                                    const pixel = imageData.data;
                                    r += pixel[0];
                                    g += pixel[1];
                                    b += pixel[2];
                                    count++;
                                }}
                            }}
                        }}

                        // Average RGB
                        r = Math.round(r / count);
                        g = Math.round(g / count);
                        b = Math.round(b / count);

                        // Convert to hex
                        const hex = '#' + [r, g, b].map(c => {{
                            const hex = c.toString(16);
                            return hex.length === 1 ? '0' + hex : hex;
                        }}).join('');

                        resolve(hex);
                    }};

                    img.onerror = function() {{
                        reject(new Error('이미지 로드 실패'));
                    }};

                    img.src = imgElement.src;
                }} catch (e) {{
                    reject(e);
                }}
            }});
        }}

        // V4: Color Chip 핸들러 (Lifestyle Gallery + Color Selector 동기화)
        function setupColorChipHandlers() {{
            // Get all clickable chips from both sections
            const allColorChips = document.querySelectorAll('.color-chip-clickable');
            console.log(`🎨 총 컬러 칩 ${{allColorChips.length}}개 발견`);

            // Build a map of color names to chip elements
            const colorChipsByName = {{}};

            allColorChips.forEach(chip => {{
                // Find the color name from the sibling text (span with color name)
                const parent = chip.parentElement;
                if (!parent) return;

                const colorNameSpan = parent.querySelector('span');
                if (!colorNameSpan) return;

                const colorName = colorNameSpan.textContent.trim();
                if (!colorName) return;

                // Group chips by color name
                if (!colorChipsByName[colorName]) {{
                    colorChipsByName[colorName] = [];
                }}
                colorChipsByName[colorName].push(chip);
            }});

            // Log grouped chips
            console.log('🎨 컬러별 그룹:', Object.keys(colorChipsByName).map(name => {{
                return `${{name}}: ${{colorChipsByName[name].length}}개`;
            }}).join(', '));

            // Add click handlers
            allColorChips.forEach(chip => {{
                chip.addEventListener('click', (e) => {{
                    if (extractedColor) {{
                        // Find color name for this chip
                        const parent = chip.parentElement;
                        if (!parent) return;

                        const colorNameSpan = parent.querySelector('span');
                        if (!colorNameSpan) return;

                        const colorName = colorNameSpan.textContent.trim();

                        // Update ALL chips with this color name (both sections)
                        const chipsToUpdate = colorChipsByName[colorName] || [];
                        chipsToUpdate.forEach(c => {{
                            c.style.background = extractedColor;
                            c.style.backgroundColor = extractedColor;
                        }});

                        console.log(`🎨 "${{colorName}}" 컬러 칩 ${{chipsToUpdate.length}}개 업데이트: ${{extractedColor}}`);
                        alert(`✅ "${{colorName}}" 컬러 칩 ${{chipsToUpdate.length}}개가 ${{extractedColor}}로 업데이트되었습니다!`);
                    }} else {{
                        alert('⚠️ 먼저 스포이드 도구로 색상을 추출하세요!');
                    }}
                    e.stopPropagation();
                }});
            }});
        }}

        // Setup event listeners
        function setupEventListeners() {{
            // V4: ESC to deactivate eyedropper
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape' && eyedropperActive) {{
                    deactivateEyedropper();
                }}
            }});

            // V4: Click on image to extract color
            document.querySelectorAll('.image-frame').forEach(frame => {{
                const img = frame.querySelector('.editable-image');
                if (img) {{
                    img.addEventListener('click', async (e) => {{
                        if (eyedropperActive) {{
                            e.preventDefault();
                            e.stopPropagation();

                            try {{
                                const color = await extractColorFromImage(img, e.clientX, e.clientY);
                                extractedColor = color;

                                // Show extracted color
                                document.getElementById('eyedropper-result').style.display = 'flex';
                                document.getElementById('extracted-swatch').style.backgroundColor = color;
                                document.getElementById('extracted-hex').textContent = color;

                                console.log(`🎨 색상 추출 완료: ${{color}}`);
                                deactivateEyedropper();
                                // alert(`✅ 색상 추출 완료: ${{color}}\\n\\n이제 Color 섹션의 컬러 칩을 클릭하여 색상을 적용하세요!`);
                            }} catch (err) {{
                                console.error('색상 추출 실패:', err);
                                alert('❌ 색상 추출 실패: ' + err.message);
                                deactivateEyedropper();
                            }}
                        }}
                    }});
                }}
            }});

            // Page zoom
            document.getElementById('page-zoom').addEventListener('input', (e) => {{
                pageZoom = parseInt(e.target.value);
                document.getElementById('page-zoom-value').textContent = pageZoom + '%';
                applyPageZoom();
                autoSave();
            }});

            // Image select
            document.getElementById('image-select').addEventListener('change', (e) => {{
                selectImage(e.target.value);
            }});

            // Position/Scale sliders
            document.getElementById('position-x').addEventListener('input', (e) => {{
                const value = parseInt(e.target.value);
                cropSettings.images[currentImageId].x = value;
                document.getElementById('x-value').textContent = value + '%';
                applyCurrentCrop();
                autoSave();
            }});

            document.getElementById('position-y').addEventListener('input', (e) => {{
                const value = parseInt(e.target.value);
                cropSettings.images[currentImageId].y = value;
                document.getElementById('y-value').textContent = value + '%';
                applyCurrentCrop();
                autoSave();
            }});

            document.getElementById('scale').addEventListener('input', (e) => {{
                const value = parseInt(e.target.value);
                cropSettings.images[currentImageId].scale = value;
                document.getElementById('scale-value').textContent = value + '%';
                applyCurrentCrop();
                autoSave();
            }});

            // V4.3: Gap type selector
            document.getElementById('gap-type-selector').addEventListener('change', (e) => {{
                currentGapType = e.target.value;

                // Show/hide gallery section selector
                const gallerySelectorWrapper = document.getElementById('gallery-section-selector-wrapper');
                if (currentGapType === 'gallery') {{
                    gallerySelectorWrapper.style.display = 'block';
                }} else {{
                    gallerySelectorWrapper.style.display = 'none';
                }}

                // Update slider value and help text
                let currentGap;
                let helpText;

                if (currentGapType === 'gallery') {{
                    currentGap = gapSettings.gallery[selectedGallerySection] || gapSettings.gallery.all || 21;
                    helpText = '💡 갤러리 섹션의 이미지 간격을 조절합니다.';
                }} else if (currentGapType === 'detail') {{
                    currentGap = gapSettings.detail;
                    helpText = '💡 디테일 섹션의 이미지 간격을 조절합니다.';
                }} else {{ // hero
                    currentGap = gapSettings.hero;
                    helpText = '💡 히어로 이미지와 상품명 사이의 간격을 조절합니다.';
                }}

                document.getElementById('gap-slider').value = currentGap;
                document.getElementById('gap-value').textContent = currentGap + 'px';
                document.getElementById('gap-help-text').textContent = helpText;

                console.log(`📋 간격 조정 대상 변경: ${{currentGapType}} (현재: ${{currentGap}}px)`);
            }});

            // V4.2: Gallery section selector
            document.getElementById('gallery-section-selector').addEventListener('change', (e) => {{
                selectedGallerySection = e.target.value;

                // Update slider to show current section's gap
                const currentGap = gapSettings.gallery[selectedGallerySection] || gapSettings.gallery.all || 21;
                document.getElementById('gap-slider').value = currentGap;
                document.getElementById('gap-value').textContent = currentGap + 'px';

                console.log(`📋 갤러리 섹션 선택: ${{selectedGallerySection}} (현재 간격: ${{currentGap}}px)`);
            }});

            // V4.3: Unified gap slider
            document.getElementById('gap-slider').addEventListener('input', (e) => {{
                const gap = parseInt(e.target.value);

                // Update gap settings based on current type
                if (currentGapType === 'gallery') {{
                    gapSettings.gallery[selectedGallerySection] = gap;
                }} else if (currentGapType === 'detail') {{
                    gapSettings.detail = gap;
                }} else {{ // hero
                    gapSettings.hero = gap;
                }}

                document.getElementById('gap-value').textContent = gap + 'px';
                applyGap();
                autoSave();
            }});

            // V4.3 FIX: Text element click selection - canvas 내부만 선택
            const allTextElements = document.querySelectorAll('.canvas div, .canvas span, .canvas p, .canvas h1, .canvas h2, .canvas h3, .canvas h4, .canvas h5, .canvas h6');
            let passedFilters = 0;
            let filteredByParent = 0;
            let filteredByChildCount = 0;
            let filteredByTextLength = 0;

            console.log(`🔍 텍스트 요소 스캔 시작: ${{allTextElements.length}}개 후보`);

            allTextElements.forEach(el => {{
                // V4.3 FIX: Skip control panel and empty elements
                // NOTE: image-frame, canvas-wrapper 내부의 텍스트는 허용, 해당 요소 자체만 제외
                if (el.closest('.control-panel') ||
                    el.classList.contains('image-frame') ||    // image-frame 자체만 제외
                    el.classList.contains('canvas-wrapper') ||  // canvas-wrapper 자체만 제외
                    el.classList.contains('canvas') ||
                    !el.textContent.trim()) {{
                    filteredByParent++;
                    return;
                }}

                // V4.3 FIX: 실제 콘텐츠를 담은 요소만 선택 (자식이 많은 구조용 div 제외)
                const childDivs = el.querySelectorAll('div');
                if (childDivs.length > 10) {{  // 자식 div가 10개 이상이면 구조용 컨테이너로 간주
                    filteredByChildCount++;
                    return;
                }}

                // V4.3 FIX: 실제 텍스트 내용이 있는 요소만 선택
                const textContent = el.textContent.trim();
                if (textContent.length < 2) {{  // 2자 미만 제외
                    filteredByTextLength++;
                    return;
                }}

                passedFilters++;
                el.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    selectTextElement(el);
                }});

                // Add hover effect
                el.style.cursor = 'pointer';
                el.addEventListener('mouseenter', () => {{
                    if (el !== selectedTextElement) {{
                        el.style.outline = '1px solid rgba(76, 175, 80, 0.3)';
                    }}
                }});
                el.addEventListener('mouseleave', () => {{
                    if (el !== selectedTextElement) {{
                        el.style.outline = '';
                    }}
                }});
            }});

            // V4.3 FIX: 필터링 요약 로그
            console.log(`✅ 텍스트 요소 필터링 완료:`);
            console.log(`  - 전체 후보: ${{allTextElements.length}}개`);
            console.log(`  - 부모/클래스 필터: ${{filteredByParent}}개 제외`);
            console.log(`  - 자식 div 개수: ${{filteredByChildCount}}개 제외`);
            console.log(`  - 텍스트 길이: ${{filteredByTextLength}}개 제외`);
            console.log(`  - ✨ 최종 선택 가능: ${{passedFilters}}개`);

            // V4.2: Text size sliders
            document.getElementById('text-width').addEventListener('input', (e) => {{
                const width = parseInt(e.target.value);
                document.getElementById('text-width-value').textContent = width + 'px';
                applyTextSize('width', width);
            }});

            document.getElementById('text-height').addEventListener('input', (e) => {{
                const height = parseInt(e.target.value);
                document.getElementById('text-height-value').textContent = height + 'px';
                applyTextSize('height', height);
            }});

            document.getElementById('text-fontsize').addEventListener('input', (e) => {{
                const fontSize = parseInt(e.target.value);
                document.getElementById('text-fontsize-value').textContent = fontSize + 'px';
                applyTextSize('fontSize', fontSize);
            }});

            // Drag events on image frames (V4: 스포이드 모드 시 비활성화)
            document.querySelectorAll('.image-frame').forEach(frame => {{
                const img = frame.querySelector('.editable-image');
                if (img) {{
                    frame.addEventListener('mousedown', (e) => {{
                        if (eyedropperActive) return; // V4: 스포이드 모드에서는 드래그 비활성화

                        isDragging = true;
                        startX = e.clientX;
                        startY = e.clientY;

                        const imgId = frame.getAttribute('data-id');
                        const settings = cropSettings.images[imgId];
                        startObjX = settings.x;
                        startObjY = settings.y;

                        selectImage(imgId);
                        e.preventDefault();
                    }});
                }}
            }});

            document.addEventListener('mousemove', (e) => {{
                if (!isDragging || eyedropperActive) return;

                const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
                if (!frame) return;

                const dx = e.clientX - startX;
                const dy = e.clientY - startY;

                // Convert pixels to percentage (relative to frame size)
                const frameWidth = frame.offsetWidth;
                const frameHeight = frame.offsetHeight;

                const dxPercent = (dx / frameWidth) * 100;
                const dyPercent = (dy / frameHeight) * 100;

                cropSettings.images[currentImageId].x = Math.max(0, Math.min(200, startObjX + dxPercent));
                cropSettings.images[currentImageId].y = Math.max(0, Math.min(200, startObjY + dyPercent));

                updateSliders();
                applyCurrentCrop();
            }});

            document.addEventListener('mouseup', () => {{
                if (isDragging) {{
                    isDragging = false;
                    autoSave();
                }}
            }});

            // Wheel zoom on image frames
            document.querySelectorAll('.image-frame').forEach(frame => {{
                frame.addEventListener('wheel', (e) => {{
                    if (eyedropperActive) return; // V4: 스포이드 모드에서는 줌 비활성화

                    e.preventDefault();

                    const imgId = frame.getAttribute('data-id');
                    if (!imgId) return;

                    selectImage(imgId);

                    const delta = e.deltaY > 0 ? -5 : 5;
                    const currentScale = cropSettings.images[imgId].scale;
                    const newScale = Math.max(50, Math.min(500, currentScale + delta));

                    cropSettings.images[imgId].scale = newScale;
                    updateSliders();
                    applyCurrentCrop();
                    autoSave();
                }});
            }});
        }}

        // Select image
        function selectImage(id) {{
            // Remove previous selection
            document.querySelectorAll('.image-frame').forEach(f => f.classList.remove('selected'));

            // Add selection to current frame
            const frame = document.querySelector(`[data-id="${{id}}"]`);
            if (frame) {{
                frame.classList.add('selected');
            }}

            currentImageId = id;

            // Update dropdown
            document.getElementById('image-select').value = id;

            updateSliders();
        }}

        // Update sliders to match current image
        function updateSliders() {{
            const settings = cropSettings.images[currentImageId];
            if (settings) {{
                document.getElementById('position-x').value = settings.x;
                document.getElementById('x-value').textContent = Math.round(settings.x) + '%';
                document.getElementById('position-y').value = settings.y;
                document.getElementById('y-value').textContent = Math.round(settings.y) + '%';
                document.getElementById('scale').value = settings.scale;
                document.getElementById('scale-value').textContent = settings.scale + '%';
            }}
        }}

        // Apply crop to current image (V4: object-fit: cover 효과를 transform으로 구현)
        function applyCurrentCrop() {{
            const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
            if (!frame) return;

            const img = frame.querySelector('.editable-image');
            const settings = cropSettings.images[currentImageId];

            if (img && settings) {{
                // 원본 이미지 크기
                const imgWidth = img.naturalWidth;
                const imgHeight = img.naturalHeight;

                // Frame 크기 (뷰포트)
                const frameWidth = frame.offsetWidth;
                const frameHeight = frame.offsetHeight;

                // object-fit: cover 효과를 transform으로 구현
                const scaleX = frameWidth / imgWidth;
                const scaleY = frameHeight / imgHeight;
                const baseScale = Math.max(scaleX, scaleY);  // cover 효과

                // 사용자 스케일
                const userScale = settings.scale / 100;
                const totalScale = baseScale * userScale;

                // 위치 오프셋 (픽셀 단위)
                const tx = (settings.x - 100) / 100 * frameWidth;
                const ty = (settings.y - 100) / 100 * frameHeight;

                img.style.transform = `translate(${{tx}}px, ${{ty}}px) scale(${{totalScale}})`;
            }}
        }}

        // Apply page zoom
        function applyPageZoom() {{
            const container = document.querySelector('.container');
            if (container) {{
                const scale = pageZoom / 100;
                container.style.transform = `scale(${{scale}})`;

                // Adjust height to prevent whitespace
                const naturalHeight = container.scrollHeight;
                container.style.height = `${{naturalHeight * scale}}px`;
            }}
        }}

        // V4.2: Apply gallery gap to selected section(s)
        // V4.3: Unified gap application for gallery/detail/hero
        function applyGap() {{
            if (currentGapType === 'gallery') {{
                // Apply gallery gap
                if (selectedGallerySection === 'all') {{
                    // Apply to all gallery sections - V4.3 FIX: 더 안전한 DOM 쿼리
                    const gallerySections = document.querySelectorAll('.section--lifestyle-gallery');
                    gallerySections.forEach(section => {{
                        // 첫 번째 직접 자식 div 중 flex-direction: column을 가진 것 찾기
                        const containers = section.querySelectorAll(':scope > div');
                        containers.forEach(container => {{
                            const computedStyle = getComputedStyle(container);
                            if (computedStyle.flexDirection === 'column') {{
                                // gap 스타일 업데이트 (있으면 교체, 없으면 추가)
                                const currentStyle = container.getAttribute('style') || '';
                                let newStyle;
                                if (/gap:\s*\d+px/.test(currentStyle)) {{
                                    newStyle = currentStyle.replace(/gap:\s*\d+px/, `gap: ${{gapSettings.gallery.all}}px`);
                                }} else {{
                                    // gap이 없으면 추가
                                    newStyle = currentStyle + (currentStyle.endsWith(';') ? '' : '; ') + `gap: ${{gapSettings.gallery.all}}px;`;
                                }}
                                container.setAttribute('style', newStyle.trim());
                            }}
                        }});
                    }});
                    console.log(`📐 전체 갤러리 간격: ${{gapSettings.gallery.all}}px`);
                }} else {{
                    // Apply to specific gallery section - V4.3 FIX
                    const section = document.querySelector(`.section--lifestyle-gallery[data-gallery-index="${{selectedGallerySection}}"]`);
                    if (section) {{
                        const containers = section.querySelectorAll(':scope > div');
                        containers.forEach(container => {{
                            const computedStyle = getComputedStyle(container);
                            if (computedStyle.flexDirection === 'column') {{
                                const currentStyle = container.getAttribute('style') || '';
                                const gap = gapSettings.gallery[selectedGallerySection] || 21;
                                let newStyle;
                                if (/gap:\s*\d+px/.test(currentStyle)) {{
                                    newStyle = currentStyle.replace(/gap:\s*\d+px/, `gap: ${{gap}}px`);
                                }} else {{
                                    newStyle = currentStyle + (currentStyle.endsWith(';') ? '' : '; ') + `gap: ${{gap}}px;`;
                                }}
                                container.setAttribute('style', newStyle.trim());
                                console.log(`📐 갤러리 섹션 ${{selectedGallerySection}} 간격: ${{gap}}px`);
                            }}
                        }});
                    }}
                }}
            }} else if (currentGapType === 'detail') {{
                // Apply detail section gap - V4.3 FIX
                const detailSection = document.querySelector('.section--material-detail');
                if (detailSection) {{
                    const containers = detailSection.querySelectorAll(':scope > div');
                    containers.forEach(container => {{
                        const computedStyle = getComputedStyle(container);
                        if (computedStyle.flexDirection === 'column') {{
                            const currentStyle = container.getAttribute('style') || '';
                            let newStyle;
                            if (/gap:\s*\d+px/.test(currentStyle)) {{
                                newStyle = currentStyle.replace(/gap:\s*\d+px/, `gap: ${{gapSettings.detail}}px`);
                            }} else {{
                                newStyle = currentStyle + (currentStyle.endsWith(';') ? '' : '; ') + `gap: ${{gapSettings.detail}}px;`;
                            }}
                            container.setAttribute('style', newStyle.trim());
                            console.log(`📐 디테일 섹션 간격: ${{gapSettings.detail}}px`);
                        }}
                    }});
                }} else {{
                    console.warn('⚠️ 디테일 섹션을 찾을 수 없습니다.');
                }}
            }} else if (currentGapType === 'hero') {{
                // Apply hero to product name spacing (via margin-top of color-variants section) - V4.3 FIX
                const colorVariantsSection = document.querySelector('.section--color-variants');
                if (colorVariantsSection) {{
                    const currentStyle = colorVariantsSection.getAttribute('style') || '';
                    let newStyle;
                    if (/margin:\s*\d+px\s+auto\s+0/.test(currentStyle)) {{
                        newStyle = currentStyle.replace(/margin:\s*\d+px\s+auto\s+0/, `margin: ${{gapSettings.hero}}px auto 0`);
                    }} else {{
                        // margin 스타일이 없으면 추가
                        newStyle = currentStyle + (currentStyle.endsWith(';') ? '' : '; ') + `margin: ${{gapSettings.hero}}px auto 0;`;
                    }}
                    colorVariantsSection.setAttribute('style', newStyle.trim());
                    console.log(`📐 히어로-상품명 간격: ${{gapSettings.hero}}px`);
                }} else {{
                    console.warn('⚠️ 상품명 섹션을 찾을 수 없습니다.');
                }}
            }}
        }}

        // V4.2: Select text element
        function selectTextElement(element) {{
            // Deselect previous element
            if (selectedTextElement) {{
                selectedTextElement.style.outline = '';
            }}

            // Select new element
            selectedTextElement = element;
            element.style.outline = '2px dashed #4CAF50';

            // Assign ID if not exists
            if (!element.dataset.textId) {{
                element.dataset.textId = `text-element-${{textElementIdCounter++}}`;
            }}

            // V4.3: Add resize handles
            addResizeHandles(element);

            // Show control panel
            const panel = document.getElementById('text-box-control');
            panel.style.display = 'block';

            // Update info display
            const info = element.textContent.substring(0, 30) + (element.textContent.length > 30 ? '...' : '');
            document.getElementById('selected-text-info').textContent = info;

            // Load current sizes
            const savedSizes = textSizes[element.dataset.textId] || {{}};
            const currentWidth = savedSizes.width || parseInt(getComputedStyle(element).width) || 200;
            const currentHeight = savedSizes.height || parseInt(getComputedStyle(element).height) || 50;
            const currentFontSize = savedSizes.fontSize || parseInt(getComputedStyle(element).fontSize) || 14;

            // Update sliders
            document.getElementById('text-width').value = currentWidth;
            document.getElementById('text-width-value').textContent = currentWidth + 'px';
            document.getElementById('text-height').value = currentHeight;
            document.getElementById('text-height-value').textContent = currentHeight + 'px';
            document.getElementById('text-fontsize').value = currentFontSize;
            document.getElementById('text-fontsize-value').textContent = currentFontSize + 'px';
        }}

        // V4.2: Deselect text element
        function deselectTextElement() {{
            if (selectedTextElement) {{
                selectedTextElement.style.outline = '';
                selectedTextElement = null;
            }}

            // V4.3: Remove resize handles
            removeResizeHandles();

            // Hide control panel
            const panel = document.getElementById('text-box-control');
            panel.style.display = 'none';

            // Clear info
            document.getElementById('selected-text-info').textContent = '없음';
        }}

        // Helper: Compute offsetTop of a node relative to a section container
        function computeRelativeTop(node, section) {{
            if (!node) return 0;
            if (!section || node === section) return node.offsetTop || 0;

            let total = 0;
            let current = node;

            while (current && current !== section) {{
                total += current.offsetTop || 0;
                current = current.offsetParent;
            }}

            return total;
        }}

        // Helper: Convert absolute-bottom anchored containers to top-based anchors
        function ensureAnchorForHeight(element) {{
            let anchor = element;

            console.log('🔍 ensureAnchorForHeight 시작:', {{
                element: element.tagName,
                className: element.className,
                textContent: element.textContent?.substring(0, 20)
            }});

            while (anchor && anchor !== document.body) {{
                const style = getComputedStyle(anchor);

                console.log(`🔎 Anchor 검사:`, {{
                    position: style.position,
                    transform: style.transform,
                    top: style.top,
                    bottom: style.bottom,
                    className: anchor.className
                }});

                if (style.position === 'absolute' && style.bottom !== 'auto') {{
                    // 🔍 V4.3.1: bottom이 있어도 matrix 센터 앵커 체크를 우선 수행
                    const transform = style.transform || '';
                    let isCenterTransform = false;

                    // matrix 형식 감지: matrix(1, 0, 0, 1, translateX, translateY)
                    if (transform.startsWith('matrix')) {{
                        const matrixMatch = transform.match(/matrix\\(([^)]+)\\)/);
                        if (matrixMatch) {{
                            const values = matrixMatch[1].split(',').map(v => parseFloat(v.trim()));
                            if (values.length === 6) {{
                                const translateX = values[4];
                                const translateY = values[5];
                                const elementWidth = anchor.offsetWidth || 200;
                                const elementHeight = anchor.offsetHeight || 50;

                                if (translateX < 0 && translateY < 0) {{
                                    const isXCenter = Math.abs(translateX + elementWidth / 2) < 10;
                                    const isYCenter = Math.abs(translateY + elementHeight / 2) < 10;
                                    if (isXCenter || isYCenter) {{
                                        isCenterTransform = true;
                                        console.log('🔍 Matrix 센터 감지 (bottom 브랜치):', {{
                                            translateX: translateX,
                                            translateY: translateY,
                                            elementWidth: elementWidth,
                                            elementHeight: elementHeight,
                                            isXCenter: isXCenter,
                                            isYCenter: isYCenter
                                        }});
                                    }}
                                }}
                            }}
                        }}
                    }}

                    // translate(-50%, -50%) 패턴도 체크
                    if (!isCenterTransform && transform.includes('translate') && (
                        transform.includes('-50%, -50%') ||
                        (transform.includes('-50%') && transform.split(',').filter(p => p.includes('-50%')).length >= 2) ||
                        transform.match(/translate\(\\s*-50%.*-50%/) ||
                        transform.match(/translateX\\(\\s*-50%.*translateY\\(\\s*-50%/)
                    )) {{
                        isCenterTransform = true;
                        console.log('✅ Translate 센터 감지 (bottom 브랜치)');
                    }}

                    // 센터 앵커로 감지되면 center 모드로 처리
                    if (isCenterTransform) {{
                        console.log('✅ 센터 앵커 감지됨 (bottom 브랜치)!');
                        const section = anchor.closest('.section');

                        if (section && !section.dataset.originalHeight) {{
                            section.dataset.originalHeight = String(section.offsetHeight);
                        }}

                        if (!anchor.dataset.anchorMode) {{
                            anchor.dataset.anchorMode = 'center';

                            if (section && style.top) {{
                                const sectionHeight = section.offsetHeight;
                                let centerPx;
                                if (style.top.includes('%') && sectionHeight) {{
                                    const percent = parseFloat(style.top);
                                    centerPx = (percent / 100) * sectionHeight;
                                }} else {{
                                    centerPx = parseFloat(style.top) || 0;
                                }}

                                const ratio = centerPx / sectionHeight;
                                anchor.dataset.anchorCenterRatio = String(ratio);
                                console.log(`📌 Center anchor 설정: centerPx=${{centerPx}}, ratio=${{ratio.toFixed(3)}}`);
                            }}
                        }}

                        return {{ anchor, section }};
                    }}

                    // 일반 bottom 앵커 처리
                    const section = anchor.closest('.section');

                    if (section && !section.dataset.originalHeight) {{
                        section.dataset.originalHeight = String(section.offsetHeight);
                    }}

                    if (anchor.dataset.anchorConverted !== 'true') {{
                        let topWithinSection;
                        if (section) {{
                            const sectionHeight = section.offsetHeight;
                            const anchorHeight = anchor.offsetHeight || parseFloat(style.height) || 0;
                            const bottomValue = parseFloat(style.bottom) || 0;
                            topWithinSection = Math.max(0, sectionHeight - anchorHeight - bottomValue);
                        }} else {{
                            topWithinSection = parseFloat(style.top) || 0;
                        }}

                        anchor.dataset.anchorOriginalBottom = style.bottom;
                        anchor.dataset.anchorConverted = 'true';
                        anchor.dataset.anchorTop = String(topWithinSection);
                        anchor.style.bottom = 'auto';
                        anchor.style.top = `${{topWithinSection}}px`;
                        if (style.display === 'flex' && style.justifyContent !== 'flex-start') {{
                            anchor.dataset.anchorOriginalJustify = style.justifyContent;
                            anchor.style.justifyContent = 'flex-start';
                            console.log(`🎯 Anchor justify-content 조정: flex-start`);
                        }}
                        console.log(`📌 Anchor converted to top: top=${{anchor.style.top}} (was bottom=${{style.bottom}})`);
                    }}

                    return {{ anchor, section }};
                }} else if (
                    style.position === 'absolute' &&
                    style.top && style.top !== 'auto'
                ) {{
                    // 더 유연한 센터 앵커 감지
                    const transform = style.transform || '';

                    // matrix 형식 감지: matrix(1, 0, 0, 1, translateX, translateY)
                    let isCenterTransform = false;

                    // 1. translate(-50%, -50%) 패턴
                    if (transform.includes('translate') && (
                        transform.includes('-50%, -50%') ||
                        (transform.includes('-50%') && transform.split(',').filter(p => p.includes('-50%')).length >= 2) ||
                        transform.match(/translate\(\\s*-50%.*-50%/) ||
                        transform.match(/translateX\\(\\s*-50%.*translateY\\(\\s*-50%/)
                    )) {{
                        isCenterTransform = true;
                    }}

                    // 2. matrix 형식 감지 (예: matrix(1, 0, 0, 1, -101, -74.5))
                    if (!isCenterTransform && transform.startsWith('matrix')) {{
                        const matrixMatch = transform.match(/matrix\\(([^)]+)\\)/);
                        if (matrixMatch) {{
                            const values = matrixMatch[1].split(',').map(v => parseFloat(v.trim()));
                            if (values.length === 6) {{
                                const translateX = values[4];
                                const translateY = values[5];
                                // 음수 offset이면서 요소 크기의 절반 정도인 경우 센터 정렬로 판단
                                const elementWidth = anchor.offsetWidth || 200;
                                const elementHeight = anchor.offsetHeight || 50;

                                if (translateX < 0 && translateY < 0) {{
                                    const isXCenter = Math.abs(translateX + elementWidth / 2) < 10;
                                    const isYCenter = Math.abs(translateY + elementHeight / 2) < 10;
                                    if (isXCenter || isYCenter) {{
                                        isCenterTransform = true;
                                        console.log('🔍 Matrix 센터 감지:', {{
                                            translateX: translateX,
                                            translateY: translateY,
                                            elementWidth: elementWidth,
                                            elementHeight: elementHeight,
                                            isXCenter: isXCenter,
                                            isYCenter: isYCenter
                                        }});
                                    }}
                                }}
                            }}
                        }}
                    }}

                    console.log(`🎯 센터 변환 체크:`, {{
                        transform: transform,
                        isCenterTransform: isCenterTransform,
                        top: style.top
                    }});

                    if (isCenterTransform) {{
                        console.log('✅ 센터 앵커 감지됨!');
                        const section = anchor.closest('.section');

                        if (section && !section.dataset.originalHeight) {{
                            section.dataset.originalHeight = String(section.offsetHeight);
                        }}

                        if (!anchor.dataset.anchorMode) {{
                            anchor.dataset.anchorMode = 'center';

                            if (section) {{
                                const sectionHeight = section.offsetHeight;
                                let centerPx;
                                if (style.top.includes('%') && sectionHeight) {{
                                    const percent = parseFloat(style.top);
                                    centerPx = sectionHeight * (isNaN(percent) ? 0 : percent / 100);
                                }} else {{
                                    centerPx = parseFloat(style.top) || anchor.offsetTop || 0;
                                }}

                                if (sectionHeight) {{
                                    anchor.dataset.anchorCenterRatio = String(centerPx / sectionHeight);
                                }} else {{
                                    anchor.dataset.anchorCenterPx = String(centerPx);
                                }}

                                console.log(`📌 Center anchor 설정:`, {{
                                    centerPx: centerPx,
                                    ratio: anchor.dataset.anchorCenterRatio,
                                    sectionHeight: sectionHeight
                                }});
                            }}
                        }}

                        return {{ anchor, section }};
                    }}
                }}
                anchor = anchor.parentElement;
            }}

            return null;
        }}

        function handleHeightChange(element, desiredHeight) {{
            console.log('🔧 handleHeightChange 시작:', {{
                element: element.tagName,
                className: element.className,
                desiredHeight: desiredHeight
            }});

            const anchorInfo = ensureAnchorForHeight(element);
            const computedStyle = getComputedStyle(element);
            const currentHeight = element.offsetHeight || parseFloat(computedStyle.height) || 0;
            const target = Number(desiredHeight);
            const resolvedHeight = Number.isFinite(target) ? target : currentHeight;
            const delta = resolvedHeight - currentHeight;

            element.style.height = `${{resolvedHeight}}px`;

            const sectionForUpdate = anchorInfo?.section || element.closest('.section');
            if (sectionForUpdate && !sectionForUpdate.dataset.originalHeight) {{
                sectionForUpdate.dataset.originalHeight = String(sectionForUpdate.offsetHeight);
            }}

            if (anchorInfo) {{
                const {{ anchor, section }} = anchorInfo;

                console.log('📍 Anchor 정보:', {{
                    anchorMode: anchor.dataset.anchorMode,
                    anchorCenterRatio: anchor.dataset.anchorCenterRatio,
                    delta: delta
                }});

                if (anchor.dataset.anchorMode === 'center') {{
                    console.log('🎯 센터 모드: 위치 변경 없이 종료');
                    delete element.dataset.anchorRef;
                    return resolvedHeight;
                }}

                if (!anchor.dataset.anchorId) {{
                    anchor.dataset.anchorId = `anchor-${{Date.now()}}-${{Math.random().toString(36).slice(2, 8)}}`;
                }} else {{
                    const storedTop = parseFloat(anchor.dataset.anchorTop || computeRelativeTop(anchor, section));
                    anchor.dataset.anchorTop = String(storedTop);
                    anchor.style.top = `${{storedTop}}px`;
                    anchor.style.bottom = 'auto';
                }}

                element.dataset.anchorRef = anchor.dataset.anchorId;

                if (section) {{
                    const previousHeight = section.offsetHeight;
                    const relativeTop = computeRelativeTop(anchor, section);
                    const requiredHeight = Math.ceil(relativeTop + anchor.offsetHeight);
                    const baseHeight = Number(section.dataset.originalHeight || previousHeight);
                    const desiredSectionHeight = Math.max(baseHeight, requiredHeight);

                    if (Math.abs(previousHeight - desiredSectionHeight) > 0.5) {{
                        section.style.height = `${{desiredSectionHeight}}px`;
                        console.log(`🏗️ Section(${{section.className || section.id || 'anonymous'}}) height 조정: ${{previousHeight}}px → ${{desiredSectionHeight}}px`);
                    }}
                }}
            }}

            return resolvedHeight;
        }}

        // V4.2: Apply text size changes
        function applyTextSize(property, value) {{
            if (!selectedTextElement) return;

            const elementId = selectedTextElement.dataset.textId;

            // Initialize if not exists
            if (!textSizes[elementId]) {{
                textSizes[elementId] = {{}};
            }}

            // Apply style
            if (property === 'width') {{
                selectedTextElement.style.width = value + 'px';
                textSizes[elementId].width = value;
            }} else if (property === 'height') {{
                const resolvedHeight = handleHeightChange(selectedTextElement, value);
                textSizes[elementId].height = resolvedHeight;
                console.log(`📏 높이 변경: ${{resolvedHeight}}px`);
            }} else if (property === 'fontSize') {{
                selectedTextElement.style.fontSize = value + 'px';
                textSizes[elementId].fontSize = value;
            }}

            console.log(`📏 텍스트 크기 변경 [${{elementId}}]: ${{property}}=${{value}}px`);
            autoSave();
        }}

        // V4.3: Text box drag resize functionality
        let resizeActive = false;
        let resizeDirection = null;
        let resizeStartX, resizeStartY, resizeStartWidth, resizeStartHeight;
        let resizeStartTop, resizeStartLeft;  // V4.3 FIX: Store initial position

        // V4.3: Add resize handles to selected text element
        function addResizeHandles(element) {{
            // Remove existing handles first
            removeResizeHandles();

            // V4.3 FIX: Store and change parent .section overflow
            const sectionParent = element.closest('.section');
            if (sectionParent) {{
                element.dataset.sectionOriginalOverflow = getComputedStyle(sectionParent).overflow;
                sectionParent.style.overflow = 'visible';
                console.log(`🔓 .section overflow 열기: ${{element.dataset.sectionOriginalOverflow}} → visible`);
            }}

            // V4.3 FIX: 핸들은 absolute로 부모 기준 배치되므로 position 변경 불필요
            console.log(`📍 Position 변경 안 함 (레이아웃 보존)`);

            // V4.3 FIX: Store original z-index and overflow before changing
            const computedStyle = getComputedStyle(element);
            element.dataset.originalZIndex = computedStyle.zIndex;
            element.dataset.originalOverflow = computedStyle.overflow;
            console.log(`💾 원본 스타일 저장: zIndex=${{computedStyle.zIndex}}, overflow=${{computedStyle.overflow}}`);

            // V4.3 FIX: Apply z-index and overflow for handle visibility
            element.style.zIndex = '10';
            element.style.overflow = 'visible';
            console.log(`🔧 스타일 변경: zIndex=10, overflow=visible (핸들 표시용)`);

            // Add text-selected class
            element.classList.add('text-selected');

            // Create 4 edge handles (top, right, bottom, left)
            const directions = ['top', 'right', 'bottom', 'left'];
            directions.forEach(direction => {{
                const handle = document.createElement('div');
                handle.className = `resize-handle resize-handle-${{direction}}`;
                handle.dataset.direction = direction;

                // Add mousedown event
                handle.addEventListener('mousedown', (e) => {{
                    e.preventDefault();
                    e.stopPropagation();
                    startResize(e, direction);
                }});

                element.appendChild(handle);
            }});

            console.log(`✅ 리사이즈 핸들 추가: ${{element.dataset.textId}}`);
        }}

        // V4.3: Remove resize handles
        function removeResizeHandles() {{
            const handles = document.querySelectorAll('.resize-handle');
            handles.forEach(handle => handle.remove());

            // V4.3 FIX: Restore parent .section overflow
            const selectedElement = document.querySelector('.text-selected');
            if (selectedElement) {{
                const sectionParent = selectedElement.closest('.section');
                if (sectionParent && selectedElement.dataset.sectionOriginalOverflow) {{
                    sectionParent.style.overflow = selectedElement.dataset.sectionOriginalOverflow;
                    console.log(`🔒 .section overflow 복원: ${{selectedElement.dataset.sectionOriginalOverflow}}`);
                    delete selectedElement.dataset.sectionOriginalOverflow;
                }}

                // Restore anchor-specific adjustments
                if (selectedElement.dataset.anchorRef) {{
                    const anchorElement = document.querySelector('[data-anchor-id=\"' + selectedElement.dataset.anchorRef + '\"]');
                    if (anchorElement) {{
                        const originalJustify = anchorElement.dataset.anchorOriginalJustify;
                        if (originalJustify) {{
                            anchorElement.style.justifyContent = originalJustify;
                            delete anchorElement.dataset.anchorOriginalJustify;
                            console.log('🎯 Anchor justify-content 복원: ' + originalJustify);
                        }}

                        delete anchorElement.dataset.anchorTop;
                        delete anchorElement.dataset.anchorCenterRatio;
                        delete anchorElement.dataset.anchorCenterPx;
                        delete anchorElement.dataset.anchorMode;
                        delete anchorElement.dataset.anchorConverted;
                        delete anchorElement.dataset.anchorId;
                    }}
                    delete selectedElement.dataset.anchorRef;
                }}

                // V4.3 FIX: Restore element's original z-index and overflow
                if (selectedElement.dataset.originalZIndex) {{
                    selectedElement.style.zIndex = selectedElement.dataset.originalZIndex;
                    console.log(`🔙 z-index 복원: ${{selectedElement.dataset.originalZIndex}}`);
                    delete selectedElement.dataset.originalZIndex;
                }}
                if (selectedElement.dataset.originalOverflow) {{
                    selectedElement.style.overflow = selectedElement.dataset.originalOverflow;
                    console.log(`🔙 overflow 복원: ${{selectedElement.dataset.originalOverflow}}`);
                    delete selectedElement.dataset.originalOverflow;
                }}

                console.log(`✓ 원본 스타일 복원 완료`);
            }}

            // Remove text-selected class from all elements
            document.querySelectorAll('.text-selected').forEach(el => {{
                el.classList.remove('text-selected');
            }});
        }}

        // V4.3: Start resize operation
        function startResize(e, direction) {{
            if (!selectedTextElement) return;

            resizeActive = true;
            resizeDirection = direction;
            resizeStartX = e.clientX;
            resizeStartY = e.clientY;
            resizeStartWidth = parseInt(getComputedStyle(selectedTextElement).width);
            resizeStartHeight = parseInt(getComputedStyle(selectedTextElement).height);

            // V4.3 FIX: Only track top/left for absolute positioned elements
            const computedStyle = getComputedStyle(selectedTextElement);
            const positionType = computedStyle.position;

            if (positionType === 'absolute') {{
                resizeStartTop = parseInt(computedStyle.top) || 0;
                resizeStartLeft = parseInt(computedStyle.left) || 0;
                console.log(`📍 Position 추적: absolute (${{resizeStartTop}}px, ${{resizeStartLeft}}px)`);
            }} else {{
                resizeStartTop = 0;
                resizeStartLeft = 0;
                console.log(`📍 Position 타입: ${{positionType}} (top/left 조정 건너뜀)`);
            }}

            // Add global mousemove and mouseup listeners
            document.addEventListener('mousemove', doResize);
            document.addEventListener('mouseup', stopResize);

            console.log(`🔄 리사이즈 시작: ${{direction}}, 초기 크기: ${{resizeStartWidth}}x${{resizeStartHeight}}px`);
        }}

        // V4.3: Perform resize operation
        function doResize(e) {{
            if (!resizeActive || !selectedTextElement) return;

            const deltaX = e.clientX - resizeStartX;
            const deltaY = e.clientY - resizeStartY;

            let newWidth = resizeStartWidth;
            let newHeight = resizeStartHeight;
            let newTop = resizeStartTop;
            let newLeft = resizeStartLeft;

            // Calculate new dimensions based on direction
            if (resizeDirection === 'right') {{
                newWidth = resizeStartWidth + deltaX;
            }} else if (resizeDirection === 'left') {{
                // V4.3 FIX: Adjust both width and left position
                newWidth = resizeStartWidth - deltaX;
                newLeft = resizeStartLeft + deltaX;
            }} else if (resizeDirection === 'bottom') {{
                newHeight = resizeStartHeight + deltaY;
            }} else if (resizeDirection === 'top') {{
                // V4.3 FIX: Adjust both height and top position
                newHeight = resizeStartHeight - deltaY;
                newTop = resizeStartTop + deltaY;
            }}

            // Enforce minimum size
            const minWidth = 50;
            const minHeight = 20;

            if (newWidth < minWidth) {{
                // V4.3 FIX: Don't move left position if hitting minimum width
                if (resizeDirection === 'left') {{
                    newLeft = resizeStartLeft + (resizeStartWidth - minWidth);
                }}
                newWidth = minWidth;
            }}

            if (newHeight < minHeight) {{
                // V4.3 FIX: Don't move top position if hitting minimum height
                if (resizeDirection === 'top') {{
                    newTop = resizeStartTop + (resizeStartHeight - minHeight);
                }}
                newHeight = minHeight;
            }}

            // Apply new dimensions
            selectedTextElement.style.width = newWidth + 'px';

            if (resizeDirection === 'bottom') {
                newHeight = handleHeightChange(selectedTextElement, newHeight);
            } else {
                selectedTextElement.style.height = newHeight + 'px';
            }

            // V4.3 FIX: Only adjust top/left for absolute positioned elements
            // Don't force position change - this would break layout
            const currentPosition = getComputedStyle(selectedTextElement).position;
            if (currentPosition === 'absolute' && (resizeDirection === 'top' || resizeDirection === 'left')) {{
                if (resizeDirection === 'top') {{
                    selectedTextElement.style.top = newTop + 'px';
                    console.log(`↕️ Top 조정: ${{newTop}}px`);
                }}
                if (resizeDirection === 'left') {{
                    selectedTextElement.style.left = newLeft + 'px';
                    console.log(`↔️ Left 조정: ${{newLeft}}px`);
                }}
            }}

            // Update sliders
            document.getElementById('text-width').value = newWidth;
            document.getElementById('text-width-value').textContent = newWidth + 'px';
            document.getElementById('text-height').value = newHeight;
            document.getElementById('text-height-value').textContent = newHeight + 'px';
        }}

        // V4.3: Stop resize operation
        function stopResize(e) {{
            if (!resizeActive) return;

            resizeActive = false;

            // Remove global listeners
            document.removeEventListener('mousemove', doResize);
            document.removeEventListener('mouseup', stopResize);

            // Save final dimensions
            if (selectedTextElement) {{
                const elementId = selectedTextElement.dataset.textId;
                const finalWidth = parseInt(selectedTextElement.style.width);
                const finalHeight = parseInt(selectedTextElement.style.height);

                if (!textSizes[elementId]) {{
                    textSizes[elementId] = {{}};
                }}

                textSizes[elementId].width = finalWidth;
                textSizes[elementId].height = finalHeight;

                autoSave();

                console.log(`✅ 리사이즈 완료 [${{elementId}}]: ${{finalWidth}}x${{finalHeight}}px`);
            }}
        }}

        // V4.2: Auto-save to localStorage
        // V4.3: Save unified gap settings
        function autoSave() {{
            cropSettings.pageZoom = pageZoom;
            cropSettings.gapSettings = gapSettings;  // V4.3: Unified gap settings (gallery/detail/hero)
            cropSettings.textSizes = textSizes;      // V4.2: Text element sizes
            localStorage.setItem(`cropSettings_${{productCode}}`, JSON.stringify(cropSettings));
        }}

        // Load settings from localStorage
        function loadSettings() {{
            const saved = localStorage.getItem(`cropSettings_${{productCode}}`);
            if (saved) {{
                try {{
                    const settings = JSON.parse(saved);

                    // V4 FIX: Version check - ignore old settings and use defaults
                    if (settings.version !== 'v4') {{
                        console.log('⚠️ Old version settings detected, using defaults');
                        console.log(`   Old version: ${{settings.version || 'unknown'}}, Current: v4`);
                        // Don't return! Continue to apply default transforms below
                    }} else {{
                        // Load page zoom
                        if (settings.pageZoom) {{
                            pageZoom = settings.pageZoom;
                            document.getElementById('page-zoom').value = pageZoom;
                            document.getElementById('page-zoom-value').textContent = pageZoom + '%';
                        }}

                        // Load image settings
                        Object.keys(settings.images || {{}}).forEach(id => {{
                            if (cropSettings.images[id]) {{
                                cropSettings.images[id] = settings.images[id];
                            }}
                        }});

                        // V4.3: Load gap settings (unified gallery/detail/hero)
                        if (settings.gapSettings) {{
                            gapSettings = settings.gapSettings;
                            // Update slider for current gap type
                            let currentGap;
                            if (currentGapType === 'gallery') {{
                                currentGap = gapSettings.gallery[selectedGallerySection] || gapSettings.gallery.all || 21;
                            }} else if (currentGapType === 'detail') {{
                                currentGap = gapSettings.detail;
                            }} else {{ // hero
                                currentGap = gapSettings.hero;
                            }}
                            document.getElementById('gap-slider').value = currentGap;
                            document.getElementById('gap-value').textContent = currentGap + 'px';
                        }} else if (settings.galleryGaps) {{
                            // V4.2 backward compatibility: Convert old galleryGaps to new gapSettings
                            gapSettings.gallery = settings.galleryGaps;
                            const currentGap = gapSettings.gallery[selectedGallerySection] || gapSettings.gallery.all || 21;
                            document.getElementById('gap-slider').value = currentGap;
                            document.getElementById('gap-value').textContent = currentGap + 'px';
                        }}

                        // V4.2: Load text element sizes
                        if (settings.textSizes) {{
                            textSizes = settings.textSizes;
                            // Apply saved sizes to elements
                            Object.keys(textSizes).forEach(elementId => {{
                                const element = document.querySelector(`[data-text-id="${{elementId}}"]`);
                                if (element) {{
                                    const sizes = textSizes[elementId];
                                    if (sizes.width) element.style.width = sizes.width + 'px';
                                    if (sizes.height) element.style.height = sizes.height + 'px';
                                    if (sizes.fontSize) element.style.fontSize = sizes.fontSize + 'px';
                                }}
                            }});
                        }}
                    }}

                    console.log('✅ Settings loaded from localStorage');
                }} catch (e) {{
                    console.warn('Failed to load settings:', e);
                }}
            }}

            // V4 FIX: ALWAYS apply transforms (moved outside if block)
            // This ensures images display correctly on first load
            imageList.forEach(img => {{
                const frame = document.querySelector(`[data-id="${{img.id}}"]`);
                if (frame && cropSettings.images[img.id]) {{
                    const imgEl = frame.querySelector('.editable-image');
                    const s = cropSettings.images[img.id];
                    if (imgEl) {{
                        // 원본 이미지 크기
                        const imgWidth = imgEl.naturalWidth;
                        const imgHeight = imgEl.naturalHeight;

                        // Frame 크기 (뷰포트)
                        const frameWidth = frame.offsetWidth;
                        const frameHeight = frame.offsetHeight;

                        // object-fit: cover 효과를 transform으로 구현
                        const scaleX = frameWidth / imgWidth;
                        const scaleY = frameHeight / imgHeight;
                        const baseScale = Math.max(scaleX, scaleY);

                        // 사용자 스케일
                        const userScale = s.scale / 100;
                        const totalScale = baseScale * userScale;

                        // 위치 오프셋 (픽셀 단위)
                        const tx = (s.x - 100) / 100 * frameWidth;
                        const ty = (s.y - 100) / 100 * frameHeight;

                        imgEl.style.transform = `translate(${{tx}}px, ${{ty}}px) scale(${{totalScale}})`;
                    }}
                }}
            }});
        }}

        // Reset current image
        function resetCurrentImage() {{
            if (currentImageId && cropSettings.images[currentImageId]) {{
                cropSettings.images[currentImageId] = {{ x: 100, y: 100, scale: 100 }};
                updateSliders();
                applyCurrentCrop();
                autoSave();
            }}
        }}

        // Export HTML
        async function exportHTML() {{
            try {{
                // Clone container
                const container = document.querySelector('.container');
                const clone = container.cloneNode(true);

                // Remove transform
                clone.style.transform = 'none';
                clone.style.height = 'auto';

                // Get full HTML
                const fullHTML = document.documentElement.outerHTML;

                // Remove control panel
                const cleanHTML = fullHTML.replace(/<div class="control-panel">.*?<\\/div>/s, '');

                // Send to server
                const response = await fetch('http://localhost:5001/save-html', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        productCode: productCode,
                        htmlContent: cleanHTML
                    }})
                }});

                const result = await response.json();
                if (result.success) {{
                    alert(`✅ HTML 저장 완료!\\n파일: ${{result.filename}}`);
                }} else {{
                    alert('❌ HTML 저장 실패: ' + result.error);
                }}
            }} catch (e) {{
                alert('❌ HTML 저장 실패: ' + e.message);
                console.error(e);
            }}
        }}

        // Load image helper
        function loadImage(src) {{
            return new Promise((resolve, reject) => {{
                const img = new Image();
                img.crossOrigin = 'anonymous';
                img.onload = () => resolve(img);
                img.onerror = reject;
                img.src = src;
            }});
        }}

        // Generate flattened image data (Dana&Peta 방식)
        async function generateFlattenedImageData(frame, img, settings) {{
            const frameRect = frame.getBoundingClientRect();
            const frameWidth = Math.max(1, Math.round(frame.offsetWidth || frameRect.width || 0));
            const frameHeight = Math.max(1, Math.round(frame.offsetHeight || frameRect.height || 0));

            if (frameWidth === 0 || frameHeight === 0) {{
                throw new Error('Frame has zero size');
            }}

            const imageSource = img.currentSrc || img.src;
            const baseImage = await loadImage(imageSource);
            const naturalWidth = baseImage.naturalWidth || baseImage.width;
            const naturalHeight = baseImage.naturalHeight || baseImage.height;

            if (!naturalWidth || !naturalHeight) {{
                throw new Error('Unable to determine image dimensions');
            }}

            const baseScale = Math.max(frameWidth / naturalWidth, frameHeight / naturalHeight);
            const userScale = (typeof settings.scale === 'number' ? settings.scale : 100) / 100;
            const totalScale = baseScale * userScale;

            const displayWidth = naturalWidth * totalScale;
            const displayHeight = naturalHeight * totalScale;

            const offsetXPercent = (typeof settings.x === 'number' ? settings.x : 100) - 100;
            const offsetYPercent = (typeof settings.y === 'number' ? settings.y : 100) - 100;

            const translateX = frameWidth * (offsetXPercent / 100);
            const translateY = frameHeight * (offsetYPercent / 100);

            // V4 FIX: Use top-left origin to match CSS transform-origin (not center)
            const drawX = translateX;
            const drawY = translateY;

            const canvas = document.createElement('canvas');
            canvas.width = frameWidth;
            canvas.height = frameHeight;

            const ctx = canvas.getContext('2d', {{ willReadFrequently: true }});
            if (!ctx) {{
                throw new Error('Failed to acquire canvas context');
            }}

            ctx.clearRect(0, 0, frameWidth, frameHeight);
            ctx.drawImage(baseImage, drawX, drawY, displayWidth, displayHeight);

            return canvas.toDataURL('image/png');
        }}

        // Create flattened image map (Dana&Peta 방식)
        async function createFlattenedImageMap() {{
            const flattenedMap = {{}};
            const cacheKeyMap = new Map();

            for (const frame of document.querySelectorAll('.image-frame')) {{
                const id = frame.getAttribute('data-id');
                if (!id) continue;
                const img = frame.querySelector('.editable-image');
                if (!img) continue;

                const settings = cropSettings.images[id] || {{ x: 100, y: 100, scale: 100 }};
                const frameWidth = Math.round(frame.offsetWidth);
                const frameHeight = Math.round(frame.offsetHeight);
                const cacheKey = `${{img.currentSrc || img.src}}|${{settings.x}}|${{settings.y}}|${{settings.scale}}|${{frameWidth}}|${{frameHeight}}`;

                try {{
                    if (cacheKey && cacheKeyMap.has(cacheKey)) {{
                        flattenedMap[id] = cacheKeyMap.get(cacheKey);
                        continue;
                    }}

                    const flattenedData = await generateFlattenedImageData(frame, img, settings);
                    flattenedMap[id] = flattenedData;
                    if (cacheKey) {{
                        cacheKeyMap.set(cacheKey, flattenedData);
                    }}
                }} catch (error) {{
                    console.warn('Flatten image failed', id, error);
                }}
            }}

            return flattenedMap;
        }}

        // V4.5: Export JPG with Tiling (4-chunk approach for high resolution)
        async function exportAsJPG() {{
            try {{
                applyCurrentCrop();

                // V4: 모든 .selected 클래스 제거
                const selectedFrames = [];
                document.querySelectorAll('.image-frame.selected').forEach(frame => {{
                    selectedFrames.push(frame);
                    frame.classList.remove('selected');
                }});

                // Create flattened images
                const flattenedImageMap = await createFlattenedImageMap();
                const replacedImageStates = [];

                // Replace images with flattened versions
                document.querySelectorAll('.image-frame').forEach(frame => {{
                    const id = frame.getAttribute('data-id');
                    const img = frame.querySelector('.editable-image');
                    if (!img) return;

                    const flattenedSrc = id ? flattenedImageMap[id] : null;

                    if (flattenedSrc) {{
                        replacedImageStates.push({{
                            img,
                            src: img.src,
                            transform: img.style.transform,
                            origin: img.style.transformOrigin,
                            objectFit: img.style.objectFit
                        }});
                        img.src = flattenedSrc;
                        img.style.transform = 'none';
                        img.style.transformOrigin = 'center center';
                        img.style.objectFit = 'cover';
                    }}
                }});

                // Wait for images to load
                await Promise.all(replacedImageStates.map(state => {{
                    if (state.img.decode) {{
                        return state.img.decode().catch(() => undefined);
                    }}
                    return Promise.resolve();
                }}));

                const controlPanel = document.querySelector('.control-panel');
                const container = document.querySelector('.container');

                // Save original styles
                const originalTransform = container.style.transform;
                const originalHeight = container.style.height;

                // Hide control panel
                controlPanel.style.display = 'none';

                // Reset container for capture
                container.style.transform = 'none';
                container.style.height = 'auto';

                // Wait for layout
                await new Promise(resolve => setTimeout(resolve, 150));

                // V4.5: Tiling configuration
                const htmlSizeEstimate = document.documentElement.innerHTML.length / (1024 * 1024);  // MB
                const totalHeight = container.scrollHeight;
                const totalWidth = container.scrollWidth;
                const CHUNK_HEIGHT = 15000;  // Each chunk height
                const canvasScale = 1.5;  // High resolution scale

                console.log(`📊 HTML 크기: ${{htmlSizeEstimate.toFixed(1)}} MB`);
                console.log(`📐 페이지 크기: ${{totalWidth}}×${{totalHeight}}px`);
                console.log(`🔍 Scale: ${{canvasScale}}x`);

                // Calculate number of chunks
                const numChunks = Math.ceil(totalHeight / CHUNK_HEIGHT);
                console.log(`📦 총 ${{numChunks}}개 청크로 분할`);

                // Track download method
                let usedClientDownload = false;

                // Process each chunk
                for (let i = 0; i < numChunks; i++) {{
                    const startY = i * CHUNK_HEIGHT;
                    const endY = Math.min(startY + CHUNK_HEIGHT, totalHeight);
                    const chunkHeight = endY - startY;

                    console.log(`\\n[Chunk ${{i + 1}}/${{numChunks}}] 캡처 시작: Y=${{startY}}~${{endY}}px (높이: ${{chunkHeight}}px)`);

                    // Margin calculation (symmetric - good left margin setting)
                    const contentWidth = 1095;  // Good left margin setting
                    const marginX = Math.floor((totalWidth - contentWidth) / 2);  // 264px symmetric margins

                    // Capture chunk with html2canvas
                    const originalCanvas = await html2canvas(container, {{
                        scale: canvasScale,
                        useCORS: true,
                        backgroundColor: '#ffffff',
                        logging: false,
                        allowTaint: true,
                        windowWidth: totalWidth,
                        windowHeight: chunkHeight,
                        width: contentWidth,
                        height: chunkHeight,
                        x: marginX,
                        y: startY,
                        scrollY: -startY,
                        scrollX: -marginX
                    }});

                    // Validate canvas
                    if (!originalCanvas || originalCanvas.width === 0 || originalCanvas.height === 0) {{
                        console.error(`❌ Chunk ${{i + 1}} Canvas 생성 실패`);
                        throw new Error(`Chunk ${{i + 1}} Canvas 생성 실패`);
                    }}

                    console.log(`✅ Chunk ${{i + 1}} Canvas 생성 완료: ${{originalCanvas.width}}×${{originalCanvas.height}}px`);

                    // Post-processing: Crop right side only (asymmetric adjustment)
                    const rightCropAmount = 39;  // Remove 39px from right (58px in final JPG at 1.5x scale)
                    const croppedCanvas = document.createElement('canvas');
                    croppedCanvas.width = originalCanvas.width - rightCropAmount;
                    croppedCanvas.height = originalCanvas.height;
                    const ctx = croppedCanvas.getContext('2d');
                    ctx.drawImage(originalCanvas, 0, 0);  // Copy left portion, exclude right 39px
                    console.log(`✂️ Right crop applied: ${{originalCanvas.width}}px → ${{croppedCanvas.width}}px (removed ${{rightCropAmount}}px)`);

                    // Convert cropped canvas to base64
                    const base64Image = croppedCanvas.toDataURL('image/jpeg', 0.95);
                    console.log(`📦 Chunk ${{i + 1}} Base64 변환 완료: ${{(base64Image.length / 1024 / 1024).toFixed(2)}} MB`);

                    // Validate base64
                    if (base64Image.length < 1000) {{
                        console.error(`❌ Chunk ${{i + 1}} Base64 데이터가 너무 작습니다`);
                        throw new Error(`Chunk ${{i + 1}} 이미지 생성 실패`);
                    }}

                    // Try server save, fallback to client download
                    const chunkProductCode = `${{productCode}}_${{String(i + 1).padStart(2, '0')}}`;
                    let savedViaServer = false;

                    try {{
                        // Attempt server save
                        const response = await fetch('http://localhost:5001/save-jpg', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{
                                productCode: chunkProductCode,
                                imageData: base64Image
                            }})
                        }});

                        if (response.ok) {{
                            const result = await response.json();
                            if (result.success) {{
                                console.log(`✅ Chunk ${{i + 1}} 서버 저장 완료: ${{result.filename}}`);
                                savedViaServer = true;
                            }}
                        }}
                    }} catch (serverError) {{
                        console.warn(`⚠️ Chunk ${{i + 1}} 서버 저장 실패, 클라이언트 다운로드로 전환:`, serverError.message);
                    }}

                    // Fallback: Client-side download
                    if (!savedViaServer) {{
                        usedClientDownload = true;
                        console.log(`💾 Chunk ${{i + 1}} 클라이언트 다운로드 시작...`);

                        // Convert cropped canvas to blob
                        const blob = await new Promise((resolve, reject) => {{
                            croppedCanvas.toBlob((b) => {{
                                if (b) {{
                                    resolve(b);
                                }} else {{
                                    reject(new Error('Blob 변환 실패'));
                                }}
                            }}, 'image/jpeg', 0.95);
                        }});

                        // Create download link
                        const blobUrl = URL.createObjectURL(blob);
                        const downloadLink = document.createElement('a');
                        downloadLink.href = blobUrl;
                        downloadLink.download = `${{chunkProductCode}}.jpg`;

                        // Trigger download
                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);

                        // Clean up blob URL after short delay
                        setTimeout(() => {{
                            URL.revokeObjectURL(blobUrl);
                        }}, 100);

                        console.log(`✅ Chunk ${{i + 1}} 클라이언트 다운로드 완료: ${{chunkProductCode}}.jpg`);
                    }}
                }}

                // Restore images
                replacedImageStates.forEach(state => {{
                    state.img.src = state.src;
                    state.img.style.transform = state.transform;
                    state.img.style.transformOrigin = state.origin;
                    if (state.objectFit) {{
                        state.img.style.objectFit = state.objectFit;
                    }} else {{
                        state.img.style.removeProperty('object-fit');
                    }}
                }});

                // Restore container
                container.style.transform = originalTransform;
                container.style.height = originalHeight;
                controlPanel.style.display = 'block';

                // Restore .selected classes
                selectedFrames.forEach(frame => {{
                    frame.classList.add('selected');
                }});

                // Show completion message
                const message = usedClientDownload
                    ? `✅ JPG 다운로드 완료!\\n\\n총 ${{numChunks}}개 파일이 브라우저 다운로드로 저장되었습니다:\\n${{productCode}}_part1.jpg ~ ${{productCode}}_part${{numChunks}}.jpg\\n\\n💡 서버가 실행 중이지 않아 클라이언트 다운로드 방식을 사용했습니다.`
                    : `✅ JPG 저장 완료!\\n\\n총 ${{numChunks}}개 파일이 서버에 저장되었습니다:\\n${{productCode}}_part1.jpg ~ ${{productCode}}_part${{numChunks}}.jpg`;

                alert(message);
            }} catch (e) {{
                alert('❌ JPG 저장 실패: ' + e.message);
                console.error(e);

                // Restore control panel
                document.querySelector('.control-panel').style.display = 'block';
                const container = document.querySelector('.container');
                container.style.transform = `scale(${{pageZoom / 100}})`;
            }}
        }}

        // Initialize on page load
        window.addEventListener('DOMContentLoaded', init);
    </script>
    '''

    javascript_code = javascript_code_template.replace('__PRODUCT_CODE__', product.product_code).replace('__IMAGE_LIST__', image_list_json)
    javascript_code = javascript_code.replace('{{', '{').replace('}}', '}')

    # body 태그 처리: 기존 컨텐츠를 .container로 감싸기
    body = soup.find('body')
    if body:
        # 기존 body의 모든 컨텐츠를 가져오기
        body_contents = list(body.children)

        # 기존 컨텐츠를 div.container로 감싸기
        container = soup.new_tag('div', **{'class': 'container'})

        # body를 비우고 container 추가
        body.clear()
        body.append(container)

        # 기존 컨텐츠를 container에 추가
        for content in body_contents:
            container.append(content)

        # Control panel을 body 맨 앞에 추가
        control_panel_soup = BeautifulSoup(control_panel_html, 'html.parser')
        body.insert(0, control_panel_soup)

        # JavaScript를 body 맨 끝에 추가
        script_soup = BeautifulSoup(javascript_code, 'html.parser')
        body.append(script_soup)

    print("✅ Editable HTML V4 완성!")

    return str(soup)


def main():
    """메인 실행 함수"""
    # 환경변수 또는 기본값 (CWD 기준)
    service_account_file = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        str(cwd / "credentials" / "service-account.json")
    )
    sheet_id = os.getenv(
        "GOOGLE_SHEET_ID",
        "1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk"
    )

    # 커맨드 라인 인자로 제품 코드 받기 (기본값: VD25FPT003)
    target_product_code = sys.argv[1] if len(sys.argv) > 1 else "VD25FPT003"

    print("=" * 60)
    print("🎨 Figma Editable HTML 생성 V4")
    print("=" * 60)
    print(f"Service Account: {service_account_file}")
    print(f"Sheet ID: {sheet_id}")
    print(f"Target Product: {target_product_code}")
    print()

    # SheetsLoader 초기화
    try:
        loader = SheetsLoader(Path(service_account_file))
        print("✅ SheetsLoader 초기화 완료")
    except Exception as e:
        print(f"❌ SheetsLoader 초기화 실패: {e}")
        sys.exit(1)

    # 제품 코드 검색 (모든 행 스캔)
    print(f"\n🔍 제품 코드 '{target_product_code}' 검색 중...")
    try:
        # 헤더 행 (1행) 건너뛰고 2행부터 스캔
        found_row_index = None
        target_code_clean = target_product_code.strip()

        for row_index in range(2, 1000):  # 최대 1000개 행 검색
            try:
                row = loader.load_row(sheet_id, row_index)
                if row and len(row) > 0:
                    # 공백 제거 후 비교
                    code = str(row[0]).strip()
                    if code == target_code_clean:
                        found_row_index = row_index
                        print(f"✅ 제품 발견: {row_index}행 (코드: {code})")
                        break
            except HttpError as e:
                # 400 에러는 범위 초과 (더 이상 행 없음)
                if e.resp.status == 400:
                    break
                print(f"⚠️  Row {row_index} 스캔 실패 (HttpError): {e}")
            except Exception as e:
                # 기타 예외는 로그 출력 후 계속 진행
                print(f"⚠️  Row {row_index} 예외 발생: {e}")
                continue

        if found_row_index is None:
            print(f"❌ 제품 코드 '{target_product_code}'를 찾을 수 없습니다.")
            print(f"   검색 범위: 2-999행")
            print(f"   시트 탭: new_raw")
            sys.exit(1)

        # 찾은 행 데이터 로드
        row = loader.load_row(sheet_id, found_row_index)
        print(f"✅ 데이터 로드 완료: {len(row)}개 컬럼")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        sys.exit(1)

    # ProductDataBuilder 초기화 (색상 추출 활성화)
    builder = ProductDataBuilder(
        enable_color_extraction=True,
        sheets_loader=loader
    )

    # 데이터 변환
    try:
        print(f"\n🔄 ProductData 변환 중...")
        product = builder.build_product_data(row)
        print(f"✅ 제품: {product.product_code} - {product.product_name}")
    except Exception as e:
        print(f"❌ 데이터 변환 실패: {e}")
        sys.exit(1)

    # HTML 생성
    try:
        print(f"\n📝 Editable HTML V4 생성 중...")
        html_content = generate_editable_html(product, loader)

        # 파일 저장 (CWD 기준, 날짜 폴더 구조)
        today = datetime.now().strftime("%Y%m%d")
        output_dir = cwd / "output" / today / "editable"
        output_dir.mkdir(exist_ok=True, parents=True)
        output_file = output_dir / f"{product.product_code}_editable_v4.html"

        output_file.write_text(html_content, encoding="utf-8")
        print(f"✅ 파일 생성: {output_file}")
        print(f"   파일 크기: {len(html_content) / 1024 / 1024:.1f} MB")
    except Exception as e:
        import traceback
        print(f"❌ HTML 생성 실패: {e}")
        print("\n" + "="*60)
        print("FULL TRACEBACK:")
        print("="*60)
        traceback.print_exc()
        print("="*60 + "\n")
        sys.exit(1)

    print(f"\n📁 출력 폴더: {output_dir}")
    print("\n💡 다음 단계:")
    print("   1. Flask 서버 시작: python scripts/server.py")
    print("   2. 브라우저에서 열기: http://localhost:5001/editable/VD25FPT003_v4")
    print()

    print("🔧 V4 수정사항 (V3 문제 해결):")
    print("   1. ✅ V3 성공 사항 유지: .info 제거, .selected 제거, 컬러 칩 표시")
    print("   2. 🔧 이미지 왜곡 수정: inline object-fit 유지 (remove 함수 삭제)")
    print("   3. 🎨 진짜 스포이드 도구: Canvas 기반 색상 추출 + 컬러 칩 업데이트")
    print()
    print("📖 사용 방법:")
    print("   1. '스포이드 활성화' 버튼 클릭")
    print("   2. 원하는 이미지의 색상 부분을 클릭")
    print("   3. 추출된 색상이 표시됨")
    print("   4. Color 섹션의 컬러 칩을 클릭하여 색상 적용")
    print()


if __name__ == "__main__":
    main()
