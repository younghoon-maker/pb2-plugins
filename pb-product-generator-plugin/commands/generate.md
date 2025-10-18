---
description: Google Sheets 데이터로 단일 제품 Editable HTML 생성
tools: [Bash]
---

# Generate Product Page

특정 제품 코드(예: VD25FTS002)의 Google Sheets 데이터를 로드하여 Editable HTML V4를 생성합니다.

## 작업 프로세스

1. **Google Sheets API 호출**: 292컬럼 데이터 로드
2. **이미지 처리**: Google Drive 이미지 다운로드 및 Base64 인코딩
3. **HTML 생성**: Jinja2 템플릿으로 Editable HTML V4 렌더링
4. **파일 저장**: `output/{YYYYMMDD}/editable/{product_code}_editable_v4.html`

## 사용법

```bash
/generate {product_code}
```

**예시**:
```bash
/generate VD25FTS002
```

## 출력

```
✅ Successfully loaded 1 products
✅ Generated: output/20251017/editable/VD25FTS002_editable_v4.html (51.4 MB)

🎨 Features:
- Image crop/zoom editor
- Text editing (contenteditable)
- Page zoom (30-100%)
- HTML/JPG download
```

## 필수 설정

### 방법 1: PRIVATE_SETUP.md 사용 (권장)

**프로젝트 폴더에서 한 번만 설정**:

```bash
# 1. 템플릿 복사
cp ~/.claude/plugins/pb-product-generator/PRIVATE_SETUP.md.template ./PRIVATE_SETUP.md

# 2. PRIVATE_SETUP.md 편집 (Service Account, Sheet ID 등)
# 3. 자동 설정 실행
~/.claude/plugins/pb-product-generator/setup.sh
```

**PRIVATE_SETUP.md 예시**:
```
SERVICE_ACCOUNT_FILE=credentials/service-account.json
GOOGLE_SHEET_ID=your_google_sheet_id
SHEET_TAB_NAME=new_raw
```

### 방법 2: 수동 설정

1. **Service Account 인증**: `credentials/service-account.json`
2. **환경 변수**: `.env` 파일
   ```bash
   GOOGLE_SHEET_ID=your_google_sheet_id
   GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
   SHEET_TAB_NAME=new_raw
   ```

## 에러 처리

- **Service Account 없음**: `❌ Service Account file not found` → credentials/ 폴더에 JSON 파일 복사
- **API 권한 에러**: `❌ Authentication failed: 403` → Google Sheets에 Service Account 이메일 공유
- **제품 코드 없음**: `❌ Product {code} not found` → 스프레드시트에 해당 제품 존재 여부 확인

## 구현

현재 프로젝트 폴더의 `output/`에 HTML 파일을 생성합니다:

```bash
# 스크립트 경로 자동 탐지
SCRIPT_PATH=$(find ~/.claude/plugins -name "generate_editable_html.py" -path "*/pb-product-generator*/scripts/*" | head -1)

# 환경 변수 로드 및 실행
GOOGLE_SERVICE_ACCOUNT_FILE="$PWD/credentials/service-account.json" \
GOOGLE_SHEET_ID="$(grep GOOGLE_SHEET_ID .env 2>/dev/null | cut -d '=' -f2)" \
SHEET_TAB_NAME="$(grep SHEET_TAB_NAME .env 2>/dev/null | cut -d '=' -f2 || echo 'new_raw')" \
python3 "$SCRIPT_PATH" {product_code}
```

**참고**: 출력 파일은 현재 작업 디렉토리의 `output/` 폴더에 저장됩니다.
