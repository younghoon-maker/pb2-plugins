"""
Figma 템플릿 기반 HTML 페이지 생성 (Editable 버전)

기존 generate_figma_final.py를 기반으로 하되, 브라우저 내 편집 기능 추가:
- 이미지 크롭/줌/팬 조절
- Control panel
- LocalStorage 저장
- HTML/JPG export

실행 방법:
  python examples/generate_figma_editable.py
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

    # 색상 이미지
    for i, color in enumerate(product.colors):
        image_list.append({
            "id": f"color{i+1}",
            "label": f"컬러 {color.color_name}",
            "type": "color"
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


def wrap_images_with_frames(soup, image_list):
    """BeautifulSoup으로 이미지를 image-frame으로 감싸기"""

    # 모든 img 태그 찾기
    all_imgs = soup.find_all('img')

    print(f"   총 {len(all_imgs)}개 이미지 발견")

    # 이미지 카운터 (각 타입별로)
    counters = {
        "main": 0,
        "color": 0,
        "gallery": {},
        "detail": 0,
        "fabric": 0,
        "checkpoint": 0,
        "model": 0
    }

    for img in all_imgs:
        # 이미지 소스로 타입 판별
        src = img.get('src', '')

        # 이미 image-frame으로 감싸진 경우 스킵
        if img.parent and img.parent.get('class') and 'image-frame' in img.parent.get('class', []):
            continue

        # 이미지 ID 결정 (휴리스틱)
        image_id = None

        # style 속성으로 섹션 판별
        parent_section = img.find_parent(['div', 'section'])
        if parent_section:
            section_style = parent_section.get('style', '')

            # 메인 이미지 (가장 위쪽)
            if counters["main"] == 0 and 'margin-bottom: 0' in section_style:
                image_id = "mainImage"
                counters["main"] += 1

            # 색상 이미지
            elif 'display: flex' in section_style and counters["color"] < len([i for i in image_list if i["type"] == "color"]):
                counters["color"] += 1
                image_id = f"color{counters['color']}"

            # 디테일 포인트
            elif 'flex-direction: column' in section_style and counters["detail"] < len([i for i in image_list if i["type"] == "detail"]):
                counters["detail"] += 1
                image_id = f"detail{counters['detail']}"

            # 소재 이미지
            elif '소재' in parent_section.get_text() or 'Fabric' in parent_section.get_text():
                if counters["fabric"] == 0:
                    image_id = "fabricImage"
                    counters["fabric"] += 1

            # 체크포인트
            elif '체크' in parent_section.get_text() or 'Check' in parent_section.get_text():
                if counters["checkpoint"] == 0:
                    image_id = "checkpointImage"
                    counters["checkpoint"] += 1

            # 모델 이미지
            elif '모델' in parent_section.get_text() or 'Model' in parent_section.get_text():
                if counters["model"] < len([i for i in image_list if i["type"] == "model"]):
                    counters["model"] += 1
                    image_id = f"model{counters['model']}"

        # 갤러리 이미지 (가장 많은 수)
        if not image_id:
            # 색상별 갤러리 추론
            gallery_images = [i for i in image_list if i["type"] == "gallery"]
            if gallery_images:
                # 첫 번째 갤러리 색상
                if not counters["gallery"]:
                    first_color = gallery_images[0]["id"].split("_")[1]
                    counters["gallery"][first_color] = 0

                # 카운터 증가
                for color in counters["gallery"]:
                    counters["gallery"][color] += 1
                    image_id = f"gallery_{color}_{counters['gallery'][color]}"
                    break

        # ID가 결정되지 않으면 임시 ID
        if not image_id:
            image_id = f"unknown_{all_imgs.index(img)}"

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

    # BeautifulSoup로 파싱
    soup = BeautifulSoup(base_html, 'html.parser')

    # imageList 동적 생성
    print("   🎯 이미지 리스트 생성 중...")
    image_list = build_image_list(product)
    print(f"   총 {len(image_list)}개 이미지 발견")

    # 이미지를 image-frame으로 감싸기
    print("   🖼️  이미지 frame 래핑 중...")
    wrap_images_with_frames(soup, image_list)

    # html2canvas 스크립트 추가 (head에)
    head = soup.find('head')
    if head:
        html2canvas_script = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js')
        head.append(html2canvas_script)

    # CSS 추가 (image-frame, editable-image, control-panel)
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
            object-fit: cover;
            transform-origin: center center;
            transition: none;
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
        '''
        style_tag.string = style_tag.string + additional_css

    # Control panel HTML 생성
    control_panel_html = f'''
    <div class="control-panel">
        <h3 style="margin: 0 0 20px 0; font-size: 18px; font-weight: bold; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px;">
            이미지 편집 도구
        </h3>

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

    # JavaScript 생성
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

        // Export JPG
        async function exportAsJPG() {{
            try {{
                // Hide control panel temporarily
                const controlPanel = document.querySelector('.control-panel');
                controlPanel.style.display = 'none';

                const container = document.querySelector('.container');

                // Reset page zoom for capture
                const originalTransform = container.style.transform;
                container.style.transform = 'scale(1)';

                // Use html2canvas
                const canvas = await html2canvas(container, {{
                    scale: 2,
                    useCORS: true,
                    allowTaint: true,
                    backgroundColor: '#ffffff'
                }});

                // Restore
                container.style.transform = originalTransform;
                controlPanel.style.display = 'block';

                // Convert to blob
                canvas.toBlob(async (blob) => {{
                    const reader = new FileReader();
                    reader.onloadend = async () => {{
                        const base64data = reader.result;

                        // Send to server
                        const response = await fetch('http://localhost:5001/save-jpg', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{
                                productCode: productCode,
                                imageData: base64data
                            }})
                        }});

                        const result = await response.json();
                        if (result.success) {{
                            alert(`✅ JPG 저장 완료!\\n파일: ${{result.filename}}`);
                        }} else {{
                            alert('❌ JPG 저장 실패: ' + result.error);
                        }}
                    }};
                    reader.readAsDataURL(blob);
                }}, 'image/jpeg', 0.95);
            }} catch (e) {{
                alert('❌ JPG 저장 실패: ' + e.message);
                console.error(e);

                // Restore control panel
                document.querySelector('.control-panel').style.display = 'block';
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

    print("✅ Editable HTML 완성!")

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
    row_number = 2  # VD25FCA004

    print("=" * 60)
    print("🎨 Figma Editable HTML 생성")
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

    # ProductDataBuilder 초기화
    builder = ProductDataBuilder(
        enable_color_extraction=True,
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
        print(f"\n📝 Editable HTML 생성 중...")
        html_content = generate_editable_html(product, loader)

        # 파일 저장
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{product.product_code}_editable.html"

        output_file.write_text(html_content, encoding="utf-8")
        print(f"✅ 파일 생성: {output_file}")
        print(f"   파일 크기: {len(html_content):,} bytes")
    except Exception as e:
        print(f"❌ HTML 생성 실패: {e}")
        sys.exit(1)

    print(f"\n📁 출력 폴더: {output_dir}")
    print("\n💡 다음 단계:")
    print("   1. Flask 서버 시작: python scripts/server.py")
    print("   2. 브라우저에서 열기: http://localhost:5001")
    print()


if __name__ == "__main__":
    main()
