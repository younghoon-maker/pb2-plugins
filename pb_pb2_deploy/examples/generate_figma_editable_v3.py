"""
Figma 템플릿 기반 HTML 페이지 생성 (Editable 버전 V3)

V3 수정사항 (4가지 버그 수정):
1. ✅ 불필요한 .info 섹션 제거 (제품 정보 박스, 푸터)
2. ✅ 인라인 object-fit: cover 제거하여 크롭 이미지 자유롭게 조정
3. ✅ Color Selector 섹션에 클릭 가능한 컬러 칩 표시 (cursor: pointer + hover)
4. ✅ JPG 익스포트 시 .selected 클래스 제거하여 녹색 테두리 제거

실행 방법:
  python examples/generate_figma_editable_v3.py
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


def remove_inline_object_fit(soup):
    """
    모든 img 태그의 inline object-fit 스타일 제거
    (크롭된 이미지도 전체 조정 가능하도록)
    """
    all_imgs = soup.find_all('img')
    modified_count = 0

    for img in all_imgs:
        style = img.get('style', '')
        if 'object-fit' in style:
            # object-fit 관련 스타일 제거
            style = re.sub(r'object-fit\s*:\s*[^;]+;?', '', style)
            img['style'] = style.strip()
            modified_count += 1

    if modified_count > 0:
        print(f"   ✅ {modified_count}개 이미지의 object-fit 제거 완료")
    return soup


def add_color_selector_styles(soup):
    """
    Color Selector 섹션의 컬러 칩에 클릭 가능 표시 추가
    """
    # Color Selector 섹션 찾기
    color_selector = soup.find('div', class_='section--color-selector')
    if not color_selector:
        print("   ⚠️ Color Selector 섹션을 찾을 수 없습니다")
        return soup

    # 컬러 칩 div들 찾기 (width: 26px; height: 26px가 있는 div)
    color_chips = color_selector.find_all('div', style=lambda s: s and '26px' in s)

    for chip in color_chips:
        # 클릭 가능하도록 cursor: pointer 추가
        style = chip.get('style', '')
        if 'cursor' not in style:
            chip['style'] = style + ' cursor: pointer; transition: transform 0.2s ease;'
        chip['class'] = chip.get('class', []) + ['color-chip-clickable']

    print(f"   ✅ {len(color_chips)}개 컬러 칩에 클릭 표시 추가 완료")
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

    # V3 수정 1: .info 섹션 제거
    print("   🗑️ .info 섹션 제거 중...")
    soup = remove_info_sections(soup)

    # V3 수정 2: inline object-fit 제거
    print("   ✂️ object-fit 스타일 제거 중...")
    soup = remove_inline_object_fit(soup)

    # V3 수정 3: Color Selector 컬러 칩에 클릭 표시
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

    # CSS 추가
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

        .editable-image {
            width: 100%;
            height: 100%;
            object-fit: unset !important;  /* Dana&Peta 방식: 원본 이미지 전체 조정 가능 */
            object-position: unset !important;
            transform-origin: center center;
            transition: none;
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
            width: 300px;
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

    # Control panel HTML 생성 (컬러 스포이드 안내 개선)
    control_panel_html = f'''
    <div class="control-panel">
        <h3 style="margin: 0 0 20px 0; font-size: 18px; font-weight: bold; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px;">
            이미지 편집 도구
        </h3>

        <!-- Color Picker (스포이드) -->
        <div style="margin-bottom: 20px; padding: 15px; background: #fff3cd; border-radius: 6px; border-left: 4px solid #ffc107;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #856404;">🎨 컬러 스포이드</h4>
            <div id="color-info" style="font-size: 13px; color: #856404; font-weight: 500; line-height: 1.5;">
                💡 페이지 하단의 <strong>"Color"</strong> 섹션에서<br>
                &nbsp;&nbsp;&nbsp;&nbsp;작은 컬러 칩(26x26px)을 클릭하세요!<br>
                <span style="font-size: 11px; color: #999;">* 컬러 칩에 마우스를 올리면 커서가 변합니다</span>
            </div>
            <div id="color-display" class="color-display" style="display: none;">
                <div id="color-swatch" class="color-swatch"></div>
                <div style="flex: 1;">
                    <div id="color-name" style="font-weight: bold; font-size: 14px; margin-bottom: 4px;"></div>
                    <div id="color-hex" style="font-size: 13px; color: #666; font-family: 'Courier New', monospace;"></div>
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

        <!-- Export Buttons -->
        <div style="margin-top: 20px; display: flex; gap: 10px; flex-direction: column;">
            <button onclick="exportHTML()" style="width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold;">
                ✅ HTML 다운로드
            </button>
            <button onclick="exportAsJPG()" style="width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold;">
                🖼️ JPG 다운로드
            </button>
        </div>
    </div>
    '''

    # JavaScript 생성 (V3 수정: Color Selector 타겟팅 및 .selected 제거)
    javascript_code = f'''
    <script>
        // Product code for localStorage
        const productCode = '{product.product_code}';

        // Image list (generated from ProductData)
        const imageList = {json.dumps(image_list, ensure_ascii=False)};

        // Crop settings storage
        const cropSettings = {{
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

        // Initialize
        function init() {{
            console.log('✅ Editable mode initialized');
            console.log(`📷 Total images: ${{imageList.length}}`);
            populateImageSelect();
            loadSettings();
            applyPageZoom();
            setupEventListeners();
            setupColorChipHandlers();  // V3: Color Selector 핸들러
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

        // V3: Color Selector 핸들러 (Section 5의 컬러 칩 타겟팅)
        function setupColorChipHandlers() {{
            const colorSelector = document.querySelector('.section--color-selector');
            if (!colorSelector) {{
                console.warn('⚠️ Color Selector 섹션을 찾을 수 없습니다');
                return;
            }}

            // 26x26px 컬러 칩 찾기
            const colorChips = colorSelector.querySelectorAll('.color-chip-clickable');
            console.log(`🎨 컬러 칩 ${{colorChips.length}}개 발견`);

            colorChips.forEach((chip, index) => {{
                // 색상 정보 찾기 (형제 span에서)
                const parentDiv = chip.parentElement;
                const colorNameSpan = parentDiv ? parentDiv.querySelector('span') : null;
                const colorName = colorNameSpan ? colorNameSpan.textContent.trim() : `컬러 ${{index + 1}}`;

                // background 색상 추출
                const bgColor = chip.style.background || chip.style.backgroundColor || '#cccccc';

                chip.addEventListener('click', (e) => {{
                    // 색상 정보 표시
                    document.getElementById('color-info').style.display = 'none';
                    document.getElementById('color-display').style.display = 'flex';
                    document.getElementById('color-swatch').style.backgroundColor = bgColor;
                    document.getElementById('color-name').textContent = colorName;
                    document.getElementById('color-hex').textContent = bgColor;

                    console.log(`🎨 컬러 선택: ${{colorName}} (${{bgColor}})`);
                    e.stopPropagation();
                }});
            }});
        }}

        // Setup event listeners
        function setupEventListeners() {{
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

            // Drag events on image frames
            document.querySelectorAll('.image-frame').forEach(frame => {{
                const img = frame.querySelector('.editable-image');
                if (img) {{
                    frame.addEventListener('mousedown', (e) => {{
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
                if (!isDragging) return;

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

        // Apply crop to current image
        function applyCurrentCrop() {{
            const frame = document.querySelector(`[data-id="${{currentImageId}}"]`);
            if (!frame) return;

            const img = frame.querySelector('.editable-image');
            const settings = cropSettings.images[currentImageId];

            if (img && settings) {{
                const scale = settings.scale / 100;
                const tx = settings.x - 100;
                const ty = settings.y - 100;
                img.style.transform = `translate(${{tx}}%, ${{ty}}%) scale(${{scale}})`;
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

                    // Apply all crops
                    imageList.forEach(img => {{
                        const frame = document.querySelector(`[data-id="${{img.id}}"]`);
                        if (frame && cropSettings.images[img.id]) {{
                            const imgEl = frame.querySelector('.editable-image');
                            const s = cropSettings.images[img.id];
                            const scale = s.scale / 100;
                            const tx = s.x - 100;
                            const ty = s.y - 100;
                            if (imgEl) {{
                                imgEl.style.transform = `translate(${{tx}}%, ${{ty}}%) scale(${{scale}})`;
                            }}
                        }}
                    }});

                    console.log('✅ Settings loaded from localStorage');
                }} catch (e) {{
                    console.warn('Failed to load settings:', e);
                }}
            }}
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

            const drawX = (frameWidth - displayWidth) / 2 + translateX;
            const drawY = (frameHeight - displayHeight) / 2 + translateY;

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

        // V3: Export JPG (Dana&Peta 방식 + .selected 클래스 제거)
        async function exportAsJPG() {{
            try {{
                applyCurrentCrop();

                // V3 수정 4: 모든 .selected 클래스 제거 (녹색 테두리 제거)
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

                // Capture with html2canvas
                const canvas = await html2canvas(container, {{
                    scale: 2,  // Dana&Peta uses scale 2 with flattened images
                    useCORS: true,
                    backgroundColor: '#ffffff',
                    logging: false,
                    allowTaint: true,
                    windowWidth: container.scrollWidth,
                    windowHeight: container.scrollHeight,
                    width: container.scrollWidth,
                    height: container.scrollHeight
                }});

                // Convert to base64
                const base64Image = canvas.toDataURL('image/jpeg', 0.95);

                // Send to server
                const response = await fetch('http://localhost:5001/save-jpg', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        productCode: productCode,
                        imageData: base64Image
                    }})
                }});

                const result = await response.json();

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

                // V3: Restore .selected classes
                selectedFrames.forEach(frame => {{
                    frame.classList.add('selected');
                }});

                if (result.success) {{
                    alert(`✅ JPG 저장 완료!\\n파일: ${{result.filename}}`);
                }} else {{
                    alert('❌ JPG 저장 실패: ' + result.error);
                }}
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

    print("✅ Editable HTML V3 완성!")

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
    print("🎨 Figma Editable HTML 생성 V3")
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
        print(f"\n📝 Editable HTML V3 생성 중...")
        html_content = generate_editable_html(product, loader)

        # 파일 저장
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{product.product_code}_editable_v3.html"

        output_file.write_text(html_content, encoding="utf-8")
        print(f"✅ 파일 생성: {output_file}")
        print(f"   파일 크기: {len(html_content) / 1024 / 1024:.1f} MB")
    except Exception as e:
        print(f"❌ HTML 생성 실패: {e}")
        sys.exit(1)

    print(f"\n📁 출력 폴더: {output_dir}")
    print("\n💡 다음 단계:")
    print("   1. Flask 서버 시작: python scripts/server.py")
    print("   2. 브라우저에서 열기: http://localhost:5001/editable/VD25FPT003_v3")
    print()

    print("🔧 V3 수정사항 (4가지 버그 수정):")
    print("   1. ✅ 불필요한 .info 섹션 제거 (제품 정보 박스, 푸터)")
    print("   2. ✅ 인라인 object-fit: cover 제거하여 크롭 이미지 자유롭게 조정")
    print("   3. ✅ Color Selector 섹션에 클릭 가능한 컬러 칩 표시 (cursor: pointer + hover)")
    print("   4. ✅ JPG 익스포트 시 .selected 클래스 제거하여 녹색 테두리 제거")
    print()


if __name__ == "__main__":
    main()
