---
description: 단일 Dana&Peta 제품 HTML 생성
---

```bash
# Execute single product generation with explicit path
cd "$HOME/.claude/plugins/marketplaces/pb-marketplace/dana-page-builder"

# First argument is the product code
python3 scripts/generate_pages_dana.py --product "$1"
```

# Generate Single Product

Google Sheets에서 단일 제품 데이터를 로드하여 Editable HTML을 생성합니다.

## 사용법

```bash
/dana-page-builder:generate DN25FW001
```

## 작업 프로세스

1. **제품 코드 확인**: 인자로 전달된 제품 코드 검증
2. **Google Sheets 연결**: 서비스 어카운트로 인증
3. **데이터 로드**: 요청서 탭에서 제품 데이터 추출
4. **이미지 다운로드**: Google Drive 이미지 다운로드
5. **HTML 생성**: Editable HTML 파일 생성 (Base64 이미지 임베드)
6. **출력**: `output/날짜/에디터블/{제품코드}_editable.html`

## 출력 예시

```
📋 Loading product data from Google Sheets...
✅ Found product: DN25FW001 - 라인 스판 반밴딩 와이드 슬랙스

📥 Downloading images from Google Drive...
✅ Downloaded 22 images (15.3 MB)

🎨 Generating HTML page...
✅ Generated: output/20251020/에디터블/DN25FW001_editable.html (45 MB)

📁 Created files:
   - output/20251020/에디터블/DN25FW001_editable.html

🎯 Next steps:
   1. Open with: open output/20251020/에디터블/DN25FW001_editable.html
   2. Or start server: /dana-page-builder:start-server
```

## 필수 조건

- **credentials/service-account.json**: 서비스 어카운트 파일 존재
- **.env**: 환경 변수 설정 (GOOGLE_SHEET_ID 등)
- **Python 3.8+**: python3 실행 가능
- **의존성**: gspread, Pillow, jinja2, numpy 설치됨

## 에러 처리

### 제품 코드 누락
```
❌ Product code is required
   Usage: /dana-page-builder:generate DN25FW001
```

### credentials 파일 없음
```
❌ credentials/service-account.json not found
   Run: /dana-page-builder:setup-from-private
```

### Google Sheets 접근 거부
```
❌ HttpError 403: Forbidden
   → Share Google Sheet with: test-account-n8n@damoa-fb351.iam.gserviceaccount.com
```

### 제품 데이터 없음
```
❌ Product DN25FW999 not found in Google Sheets
   → Check product code in 요청서 tab
```

## 구현

이 커맨드는 다음 Python 스크립트를 실행합니다:

```bash
PLUGIN_DIR="$HOME/.claude/plugins/marketplaces/pb-marketplace/dana-page-builder"
python3 "$PLUGIN_DIR/scripts/generate_pages_dana.py" --product {제품코드}
```

## 출력 파일 구조

```
output/
└── 20251020/
    └── 에디터블/
        └── DN25FW001_editable.html   # Editable HTML (Base64 이미지 포함)
```

## Editable HTML 기능

생성된 HTML은 브라우저에서 다음 편집이 가능합니다:

1. **이미지 크롭/줌**: 우측 컨트롤 패널에서 조정
2. **페이지 줌**: 30-100% (전체 뷰 조절)
3. **사이즈 이미지 선택**: Product Info 이미지 변경
4. **텍스트 편집**: contenteditable 속성으로 직접 수정
5. **설정 저장**: LocalStorage에 자동 저장

## 다음 단계

생성 후 다음과 같이 활용할 수 있습니다:

### 방법 1: Flask 서버로 열기 (권장)
```bash
/dana-page-builder:start-server
# http://localhost:5002 접속 후 제품 선택
```

### 방법 2: 파일 직접 열기
```bash
open output/20251020/에디터블/DN25FW001_editable.html
```

### 방법 3: 여러 제품 배치 생성
```bash
/dana-page-builder:batch-generate DN25FW001 DN25FW002 DN25FW003
```

## 참고

- Sheet ID: `1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk`
- Tab Name: `요청서` (102 columns: A-CV)
- Flask Port: 5002
- 이미지 캐시: `output/assets/images/`
