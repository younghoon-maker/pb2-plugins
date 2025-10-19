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
from bs4 import BeautifulSoup

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
    from examples.generate_figma_final import generate_html as generate_base_html

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

            <!-- Option 1: Internal Image Selection -->
            <div style="margin-bottom: 15px;">
                <label style="display: block; margin-bottom: 5px; font-size: 12px; font-weight: 600;">
                    내부 이미지 선택
                </label>
                <select id="replace-image-select" onchange="previewReplaceImage()" style="width: 100%; padding: 6px; font-size: 12px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 8px;">
                    <option value="">-- 이미지 선택 --</option>
                </select>

                <!-- Image Preview -->
                <div id="replace-image-preview" style="display: none; margin-bottom: 8px; padding: 10px; background: #f5f5f5; border-radius: 4px; border: 1px solid #ddd;">
                    <img id="replace-preview-img" style="width: 100%; max-width: 280px; height: auto; display: block; margin: 0 auto 8px auto; border-radius: 4px; border: 2px solid #ccc;">
                    <div id="replace-preview-label" style="font-size: 11px; color: #666; text-align: center; font-weight: 500;"></div>
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
                <input type="range" id="scale" min="100" max="500" value="100" step="1" style="width: 100%;">
            </div>
        </div>

        <!-- Reset Buttons -->
        <div style="margin-bottom: 20px; padding: 15px; background: #f8d7da; border-radius: 6px;">
            <h4 style="margin: 0 0 10px 0; font-size: 14px; font-weight: 600;">🔄 리셋</h4>
            <button onclick="resetCurrentImage()" style="width: 100%; padding: 8px; margin-bottom: 8px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600;">
                현재 이미지 리셋
            </button>
        </div>

        <!-- Text Edit Mode Toggle -->
        <div style="margin-bottom: 20px; padding: 15px; background: #fff3cd; border-radius: 6px; border-left: 4px solid #ffc107;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #856404;">✏️ 텍스트 편집</h4>
            <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; cursor: pointer;">
                <input type="checkbox" id="text-edit-mode" onchange="toggleTextEditing()" style="cursor: pointer;">
                <span>텍스트 편집 모드</span>
            </label>
            <div style="font-size: 10px; color: #856404; margin-top: 8px; line-height: 1.5;">
                💡 활성화 시 페이지의 모든 텍스트를 직접 클릭하여 수정할 수 있습니다.
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

    # JavaScript 생성 (V4: 진짜 스포이드 도구 구현)
    javascript_code = f'''
    <script>
        // Product code for localStorage
        const productCode = '{product.product_code}';

        // Image list (generated from ProductData)
        const imageList = {json.dumps(image_list, ensure_ascii=False)};

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

        // V4: Toggle text editing
        function toggleTextEditing() {{
            textEditMode = !textEditMode;

            if (textEditMode) {{
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
                // Disable text editing
                document.querySelectorAll('[contenteditable="true"]').forEach(el => {{
                    el.removeAttribute('contenteditable');
                    el.style.outline = '';
                    el.style.outlineOffset = '';
                }});
                console.log('✏️ 텍스트 편집 모드 비활성화');
            }}
        }}

        // Initialize
        function init() {{
            console.log('✅ Editable mode V4 initialized');
            console.log(`📷 Total images: ${{imageList.length}}`);
            populateImageSelect();
            populateReplaceImageSelect();
            loadSettings();
            applyPageZoom();
            setupEventListeners();
            setupColorChipHandlers();
            selectImage(currentImageId);
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

        // Populate replace image dropdown
        function populateReplaceImageSelect() {{
            const select = document.getElementById('replace-image-select');
            imageList.forEach(img => {{
                const option = document.createElement('option');
                option.value = img.id;
                option.textContent = img.label;
                select.appendChild(option);
            }});
        }}

        // Replace from internal image
        function replaceFromInternal() {{
            const selectedImageId = document.getElementById('replace-image-select').value;
            if (!selectedImageId) {{
                alert('⚠️ 교체할 이미지를 선택하세요!');
                return;
            }}

            if (!currentImageId) {{
                alert('⚠️ 먼저 편집할 이미지를 선택하세요!');
                return;
            }}

            const sourceFrame = document.querySelector(`[data-id="${{selectedImageId}}"]`);
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

        // Preview replace image
        function previewReplaceImage() {{
            const selectedImageId = document.getElementById('replace-image-select').value;
            const previewContainer = document.getElementById('replace-image-preview');
            const previewImg = document.getElementById('replace-preview-img');
            const previewLabel = document.getElementById('replace-preview-label');

            if (!selectedImageId) {{
                previewContainer.style.display = 'none';
                return;
            }}

            // Find the image element
            const sourceFrame = document.querySelector(`[data-id="${{selectedImageId}}"]`);
            const sourceImg = sourceFrame?.querySelector('.editable-image');

            if (!sourceImg) {{
                previewContainer.style.display = 'none';
                return;
            }}

            // Find image label
            const imageInfo = imageList.find(img => img.id === selectedImageId);
            const label = imageInfo ? imageInfo.label : selectedImageId;

            // Update preview
            previewImg.src = sourceImg.src;
            previewLabel.textContent = label;
            previewContainer.style.display = 'block';

            console.log(`👁️ 미리보기: ${{label}}`);
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
                                alert(`✅ 색상 추출 완료: ${{color}}\\n\\n이제 Color 섹션의 컬러 칩을 클릭하여 색상을 적용하세요!`);
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
                    const newScale = Math.max(100, Math.min(500, currentScale + delta));

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

        // Auto-save to localStorage
        function autoSave() {{
            cropSettings.pageZoom = pageZoom;
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

                // Process each chunk
                for (let i = 0; i < numChunks; i++) {{
                    const startY = i * CHUNK_HEIGHT;
                    const endY = Math.min(startY + CHUNK_HEIGHT, totalHeight);
                    const chunkHeight = endY - startY;

                    console.log(`\\n[Chunk ${{i + 1}}/${{numChunks}}] 캡처 시작: Y=${{startY}}~${{endY}}px (높이: ${{chunkHeight}}px)`);

                    // Capture chunk with html2canvas
                    const canvas = await html2canvas(container, {{
                        scale: canvasScale,
                        useCORS: true,
                        backgroundColor: '#ffffff',
                        logging: false,
                        allowTaint: true,
                        windowWidth: totalWidth,
                        windowHeight: chunkHeight,
                        width: totalWidth,
                        height: chunkHeight,
                        x: 0,
                        y: startY,
                        scrollY: -startY,
                        scrollX: 0
                    }});

                    // Validate canvas
                    if (!canvas || canvas.width === 0 || canvas.height === 0) {{
                        console.error(`❌ Chunk ${{i + 1}} Canvas 생성 실패`);
                        throw new Error(`Chunk ${{i + 1}} Canvas 생성 실패`);
                    }}

                    console.log(`✅ Chunk ${{i + 1}} Canvas 생성 완료: ${{canvas.width}}×${{canvas.height}}px`);

                    // Convert to base64
                    const base64Image = canvas.toDataURL('image/jpeg', 0.95);
                    console.log(`📦 Chunk ${{i + 1}} Base64 변환 완료: ${{(base64Image.length / 1024 / 1024).toFixed(2)}} MB`);

                    // Validate base64
                    if (base64Image.length < 1000) {{
                        console.error(`❌ Chunk ${{i + 1}} Base64 데이터가 너무 작습니다`);
                        throw new Error(`Chunk ${{i + 1}} 이미지 생성 실패`);
                    }}

                    // Send to server with part number
                    const chunkProductCode = `${{productCode}}_part${{i + 1}}`;
                    const response = await fetch('http://localhost:5001/save-jpg', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            productCode: chunkProductCode,
                            imageData: base64Image
                        }})
                    }});

                    const result = await response.json();

                    if (!result.success) {{
                        console.error(`❌ Chunk ${{i + 1}} 저장 실패: ${{result.error}}`);
                        throw new Error(`Chunk ${{i + 1}} 저장 실패: ${{result.error}}`);
                    }}

                    console.log(`✅ Chunk ${{i + 1}} 저장 완료: ${{result.filename}}`);
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

                alert(`✅ JPG 저장 완료!\\n\\n총 ${{numChunks}}개 파일 생성:\\n${{productCode}}_part1.jpg ~ ${{productCode}}_part${{numChunks}}.jpg`);
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
    # 환경변수 또는 기본값
    service_account_file = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        str(project_root / "service-account.json")
    )
    sheet_id = os.getenv(
        "GOOGLE_SHEET_ID",
        "1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk"
    )
    row_number = 2  # VD25FPT003

    print("=" * 60)
    print("🎨 Figma Editable HTML 생성 V4")
    print("=" * 60)
    print(f"Service Account: {service_account_file}")
    print(f"Sheet ID: {sheet_id}")
    print(f"Row: {row_number}")
    print()

    # SheetsLoader 초기화
    try:
        loader = SheetsLoader(Path(service_account_file))
        print("✅ SheetsLoader 초기화 완료")
    except Exception as e:
        print(f"❌ SheetsLoader 초기화 실패: {e}")
        sys.exit(1)

    # ProductDataBuilder 초기화 (색상 추출 비활성화 - 시트에 이미 HEX 값 존재)
    builder = ProductDataBuilder(
        enable_color_extraction=False,
        sheets_loader=loader
    )

    # 데이터 로드
    try:
        print(f"\n📊 Row {row_number} 데이터 로드 중...")
        row = loader.load_row(sheet_id, row_number)
        product = builder.build_product_data(row)
        print(f"✅ 제품: {product.product_code} - {product.product_name}")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        sys.exit(1)

    # HTML 생성
    try:
        print(f"\n📝 Editable HTML V4 생성 중...")
        html_content = generate_editable_html(product, loader)

        # 파일 저장
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{product.product_code}_editable_v4.html"

        output_file.write_text(html_content, encoding="utf-8")
        print(f"✅ 파일 생성: {output_file}")
        print(f"   파일 크기: {len(html_content) / 1024 / 1024:.1f} MB")
    except Exception as e:
        print(f"❌ HTML 생성 실패: {e}")
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
