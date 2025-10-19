# 사용 가이드 (Usage Guide)

본 가이드는 Google Sheets 데이터로부터 Editable HTML 페이지를 생성하고, 편집 후 익스포트하는 전체 워크플로우를 안내합니다.

---

## 목차

1. [워크플로우 개요](#워크플로우-개요)
2. [Step 1: 데이터 준비](#step-1-데이터-준비)
3. [Step 2: HTML 생성](#step-2-html-생성)
4. [Step 3: 편집](#step-3-편집)
5. [Step 4: 익스포트](#step-4-익스포트)
6. [고급 기능](#고급-기능)
7. [문제 해결](#문제-해결)

---

## 워크플로우 개요

```
┌─────────────────────┐
│ Step 1: 데이터 준비   │
│ Google Sheets에      │
│ 292컬럼 데이터 입력   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 2: HTML 생성    │
│ 배치 스크립트로      │
│ Editable HTML 생성   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 3: 편집         │
│ Flask 서버에서       │
│ 이미지 크롭/텍스트   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Step 4: 익스포트     │
│ HTML/JPG 저장        │
│ output/{날짜}/export/│
└─────────────────────┘
```

---

## Step 1: 데이터 준비

### 1.1 Google Sheets 템플릿

**292개 컬럼** (A~KJ)을 사용합니다.

주요 카테고리:
- **기본 정보** (A~C): 제품 코드, 제목, 설명
- **히어로** (D~G): 메인 이미지, 소구점
- **컬러** (H~...): 컬러 배리언트 (이름, 헥스코드, 이미지)
- **갤러리** (...): 컬러별 갤러리 이미지
- **디테일 포인트** (...): 상세 이미지 + 설명
- **제품 컷** (...): 컬러별 제품 샷
- **원단 정보** (...): 원단 이미지, 구성, 특성
- **사이즈** (...): 사이즈표 (상의/하의)
- **모델 정보** (...): 모델 신상

**전체 스키마**: [GOOGLE_SHEETS_SCHEMA.md](GOOGLE_SHEETS_SCHEMA.md) 참조

### 1.2 데이터 입력

1. Google Sheets 문서 열기
2. 각 행에 제품 데이터 입력
3. 이미지 URL은 **하이퍼링크**로 삽입:
   - 셀 우클릭 → **링크 삽입**
   - Google Drive 이미지 URL 붙여넣기
   - 셀 텍스트는 `이미지` 또는 파일명

**예시**:
| 컬럼 | 값 | 설명 |
|------|-----|------|
| A2 | VD25FCA004 | 제품 코드 |
| B2 | 플리츠 롱 스커트 | 제품명 |
| D2 | [이미지](https://drive.google.com/...) | 메인 이미지 (하이퍼링크) |

### 1.3 이미지 준비

**권장 이미지 사양**:
- **형식**: JPG, PNG
- **해상도**: 1200px 이상 (너비)
- **용량**: 5MB 이하
- **저장 위치**: Google Drive
- **공유 설정**: "링크가 있는 모든 사용자" (뷰어)

---

## Step 2: HTML 생성

### 2.1 단일 제품 생성

```bash
python3 examples/generate_figma_editable_v4.py VD25FCA004
```

**출력**:
```
📊 Google Sheets에서 제품 데이터 로드 중...
✅ Successfully loaded 1 products

🖼️  이미지 다운로드 중...
✅ Downloaded: VD25FCA004_main.jpg
✅ Downloaded: VD25FCA004_color1.jpg
...

📝 HTML 생성 중...
✅ Generated: output/20251016/editable/VD25FCA004_editable.html

✨ 완료!
```

### 2.2 배치 생성 (여러 제품)

```bash
python3 examples/generate_figma_editable_v4_batch.py
```

**출력**:
```
📊 Google Sheets에서 제품 데이터 로드 중...
✅ Successfully loaded 3 products

🖼️  이미지 다운로드 중...
✅ Downloaded 45 images (12 cached)

📝 HTML 생성 중...
✅ Generated: output/20251016/editable/VD25FCA004_editable.html
✅ Generated: output/20251016/editable/VD25FPT003_editable.html
✅ Generated: output/20251016/editable/VD25FDP013_editable.html

✨ 완료! (총 12.3초)
```

### 2.3 생성된 파일 확인

```bash
# 최신 날짜 폴더 확인
ls output/$(ls output/ | grep -E '^[0-9]{8}$' | tail -1)/editable/

# 결과:
# VD25FCA004_editable.html  (67MB)
# VD25FPT003_editable.html  (54MB)
# VD25FDP013_editable.html  (72MB)
```

---

## Step 3: 편집

### 3.1 Flask 서버 시작

```bash
python3 scripts/server.py
```

**출력**:
```
============================================================
🚀 pb_pb2_new_page 에디터블 서버 시작
============================================================
📂 Output Directory: /path/to/pb_pb2_new_page/output
🌐 Server URL: http://localhost:5001
============================================================
 * Running on http://0.0.0.0:5001
```

### 3.2 브라우저에서 접속

```
http://localhost:5001
```

**화면**: 에디터블 파일 목록
- VD25FCA004
- VD25FPT003
- VD25FDP013

클릭하여 에디터블 HTML 열기.

### 3.3 이미지 편집

#### 우측 컨트롤 패널

```
┌─────────────────────────────┐
│ 🎨 Image Crop Editor        │
├─────────────────────────────┤
│ 🔍 페이지 줌: [===|===] 60% │
├─────────────────────────────┤
│ 📐 사이즈 이미지 선택        │
│ [상의 ▼]                    │
├─────────────────────────────┤
│ 🖼️ 편집할 이미지 선택       │
│ [히어로 이미지 ▼]           │
├─────────────────────────────┤
│ 📊 이미지 조정               │
│ 가로: [=====|====] 100%     │
│ 세로: [=====|====] 100%     │
│ 확대: [=====|====] 100%     │
├─────────────────────────────┤
│ [초기화] [자동저장 ✓]       │
└─────────────────────────────┘
```

#### 편집 방법

**1. 페이지 줌 조정**:
- 슬라이더: 30% ~ 100%
- 기본값: 60% (전체 페이지 한눈에)
- 용도: 전체 레이아웃 파악

**2. 이미지 선택**:
- 드롭다운에서 편집할 이미지 선택
- 선택된 이미지는 녹색 테두리 표시

**3. 이미지 크롭/줌**:
- **슬라이더**: 가로/세로 위치, 확대/축소
- **드래그**: 이미지 위에서 클릭+드래그로 이동
- **휠**: 마우스 휠로 확대/축소

**4. 텍스트 편집**:
- 텍스트 클릭 → 직접 수정
- 제품명, 소구점, 디테일 포인트, 사이즈표 등

**5. 사이즈 이미지 변경**:
- 드롭다운에서 선택 (상의, 팬츠, 스커트 등)
- Product Info 섹션 이미지 즉시 교체

### 3.4 자동 저장

모든 설정은 **localStorage**에 자동 저장됩니다:
- 이미지 크롭 설정
- 페이지 줌 레벨
- 사이즈 이미지 선택

브라우저를 닫아도 설정이 유지됩니다.

---

## Step 4: 익스포트

### 4.1 HTML 익스포트

1. 편집 완료 후 **"HTML 다운로드"** 버튼 클릭
2. 서버가 HTML 파일 저장
3. 경로 알림: `output/20251016/export/VD25FCA004_exported.html`

**생성되는 HTML**:
- 컨트롤 패널 제거
- 스크립트 제거
- 이미지 크롭이 인라인 스타일로 적용
- contenteditable 속성 제거
- **Base64 이미지 포함** (단일 파일)

### 4.2 JPG 익스포트

1. 편집 완료 후 **"JPG 다운로드"** 버튼 클릭
2. html2canvas가 페이지 캡처 (고해상도, scale: 2x)
3. 서버가 JPG 파일 저장
4. 경로 알림: `output/20251016/export/VD25FCA004.jpg`

**생성되는 JPG**:
- 고해상도 (2400px 너비)
- 품질: 95%
- 녹색 테두리 없음 (선택 스타일 제거)
- 이미지 크롭 적용

### 4.3 중복 파일명 처리

같은 제품을 여러 번 익스포트하면 자동으로 suffix 추가:
- `VD25FCA004_exported.html`
- `VD25FCA004_exported_1.html`
- `VD25FCA004_exported_2.html`

JPG도 동일:
- `VD25FCA004.jpg`
- `VD25FCA004_1.jpg`
- `VD25FCA004_2.jpg`

---

## 고급 기능

### 1. 캐시 시스템

이미지는 `output/assets/images/`에 캐시됩니다.

**장점**:
- 중복 다운로드 방지
- 빠른 재생성
- 대역폭 절약

**캐시 확인**:
```bash
ls -lh output/assets/images/VD25FCA004*
```

**캐시 삭제** (필요 시):
```bash
rm -rf output/assets/images/
```

### 2. 컬러별 갤러리

갤러리는 컬러별로 그룹화됩니다.

**예시**:
```
베이지
[이미지 1] [이미지 2] [이미지 3]
...

블랙
[이미지 1] [이미지 2] [이미지 3]
...
```

각 컬러의 모든 이미지를 드롭다운에서 선택 가능.

### 3. 날짜별 폴더 구조

출력 폴더는 날짜별로 자동 생성됩니다:

```
output/
├── 20251015/
│   ├── editable/
│   └── export/
├── 20251016/
│   ├── editable/
│   └── export/
└── assets/
    └── images/
```

**최신 폴더 찾기**:
```bash
ls output/ | grep -E '^[0-9]{8}$' | tail -1
```

### 4. 갤러리 기본값 유지

각 컬러의 **첫 번째 갤러리 이미지**는 항상 기본 상태 유지:
- x: 100%
- y: 100%
- scale: 100%

localStorage 설정이 적용되지 않아 항상 풀프레임 표시.

---

## 문제 해결

### Step 2: HTML 생성 실패

#### `❌ Service Account file not found`

**해결**:
```bash
# 파일 존재 확인
ls credentials/service-account.json

# 없다면 SETUP_GUIDE.md 참조
```

#### `❌ Google Sheets Access Denied`

**해결**:
1. Google Sheets 문서 열기
2. 우측 상단 **공유** 클릭
3. 서비스 계정 이메일 추가 (뷰어 권한)

#### `❌ Image download failed`

**원인**: Google Drive 이미지 URL이 잘못되었거나 공유 설정 문제

**해결**:
1. 이미지 URL이 하이퍼링크 형식인지 확인
2. Google Drive 공유 설정: "링크가 있는 모든 사용자"
3. URL이 유효한지 브라우저에서 테스트

### Step 3: 편집 문제

#### `❌ Flask server connection failed`

**해결**:
```bash
# 서버 실행 중인지 확인
lsof -ti:5001

# 실행 중이 아니면 시작
python3 scripts/server.py
```

#### 이미지 편집이 안 됨

**해결**:
1. 드롭다운에서 이미지 선택 확인
2. 녹색 테두리가 표시되는지 확인
3. 브라우저 콘솔 확인 (F12 → Console 탭)

#### localStorage 설정이 안 불러와짐

**해결**:
```javascript
// 브라우저 콘솔에서 실행 (F12)
localStorage.clear()
location.reload()
```

### Step 4: 익스포트 문제

#### `❌ Failed to save HTML`

**해결**:
```bash
# export 폴더 권한 확인
ls -ld output/$(ls output/ | grep -E '^[0-9]{8}$' | tail -1)/export

# 폴더가 없으면 생성
mkdir -p output/$(date +%Y%m%d)/export
```

#### JPG에 녹색 테두리가 나타남

**원인**: 구 버전 스크립트 사용

**해결**:
- 최신 `generate_figma_editable_v4.py` 사용
- 이미지 선택 해제 후 JPG 익스포트

#### JPG 해상도가 낮음

**원인**: html2canvas scale 설정

**해결**:
- 현재 scale: 2x (2400px 너비)
- 더 높은 해상도 필요 시 코드 수정 가능

---

## 워크플로우 예시

### 시나리오: 3개 제품 일괄 처리

```bash
# 1. 데이터 준비 (Google Sheets에 3개 제품 입력)

# 2. HTML 생성
python3 examples/generate_figma_editable_v4_batch.py

# 출력:
# ✅ Generated 3 products

# 3. 서버 시작
python3 scripts/server.py

# 4. 브라우저에서 편집
# http://localhost:5001

# 5. 각 제품 편집 후 익스포트
# - VD25FCA004: HTML + JPG 저장
# - VD25FPT003: HTML + JPG 저장
# - VD25FDP013: HTML + JPG 저장

# 6. 결과 확인
ls output/20251016/export/
# VD25FCA004_exported.html  VD25FCA004.jpg
# VD25FPT003_exported.html  VD25FPT003.jpg
# VD25FDP013_exported.html  VD25FDP013.jpg
```

---

## 다음 단계

워크플로우를 익혔다면:

1. **스키마 문서**: [GOOGLE_SHEETS_SCHEMA.md](GOOGLE_SHEETS_SCHEMA.md)에서 292컬럼 상세 구조 확인
2. **예제 스크립트**: `examples/README.md`에서 고급 옵션 확인
3. **설정 가이드**: [SETUP_GUIDE.md](SETUP_GUIDE.md)에서 추가 설정 확인

---

## 참고 자료

- [README.md](../README.md) - 프로젝트 개요 및 Quick Start
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Google Cloud 설정
- [GOOGLE_SHEETS_SCHEMA.md](GOOGLE_SHEETS_SCHEMA.md) - 292 columns 구조
- [examples/README.md](../examples/README.md) - 예제 스크립트

---

**최종 업데이트**: 2025-10-16
**작성자**: MoAI-ADK
