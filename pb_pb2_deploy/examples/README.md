# Examples - 예제 스크립트

pb_pb2_new_page 프로젝트의 HTML 생성 및 테스트를 위한 예제 스크립트 모음입니다.

---

## 📋 목차

1. [주요 스크립트](#주요-스크립트)
2. [사전 준비](#사전-준비)
3. [사용 방법](#사용-방법)
4. [출력 구조](#출력-구조)
5. [문제 해결](#문제-해결)
6. [스크립트 목록](#스크립트-목록)

---

## 주요 스크립트

### 1. `generate_figma_editable_v4.py` - 단일 상품 생성 ⭐

**가장 많이 사용되는 스크립트**입니다. 하나의 상품 코드를 지정하여 Editable HTML을 생성합니다.

```bash
# 사용법
python3 examples/generate_figma_editable_v4.py <PRODUCT_CODE>

# 예시
python3 examples/generate_figma_editable_v4.py VD25FCA004
```

**출력**:
- `output/{날짜}/editable/{PRODUCT_CODE}_editable.html`

**특징**:
- 이미지 크롭/줌 컨트롤
- 텍스트 편집 (contenteditable)
- 페이지 줌 (30-100%)
- 사이즈 이미지 선택기
- localStorage 설정 저장

---

### 2. `generate_figma_editable_v4_batch.py` - 배치 생성 ⚡

여러 상품을 한 번에 생성합니다. 상품 코드 목록을 스크립트 내부에서 수정하여 사용합니다.

```bash
# 사용법
python3 examples/generate_figma_editable_v4_batch.py
```

**스크립트 수정**:
```python
# 생성할 상품 코드 목록 수정
PRODUCT_CODES = [
    "VD25FCA004",
    "VD25FPT003",
    "VD25FDP013",
    # ... 원하는 상품 코드 추가
]
```

**출력**:
- `output/{날짜}/editable/{CODE}_editable.html` (각 상품마다)

---

### 3. `load_sample.py` - 데이터 로드 테스트 🔍

Google Sheets에서 데이터를 로드하고 ProductData 모델로 변환하는 테스트 스크립트입니다.

```bash
# 사용법 (환경변수 설정 필수)
export GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
export GOOGLE_SHEET_ID=your_sheet_id_here

python3 examples/load_sample.py
```

**출력**:
- 콘솔에 데이터 검증 결과 출력
- HTML 파일 생성 없음 (데이터 검증만)

---

## 사전 준비

### 1. 환경 설정

**필수 환경 변수**:
```bash
# .env 파일 생성 또는 직접 export
export GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
export GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
```

또는 `.env` 파일에 저장:
```bash
cp .env.example .env
# .env 파일 편집
```

### 2. Google Sheets API 설정

**Google Cloud Console 설정** (상세 가이드: [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md)):
1. Google Cloud 프로젝트 생성
2. Google Sheets API 활성화
3. 서비스 계정 생성 및 JSON 키 다운로드
4. `credentials/service-account.json`에 저장

**Google Sheets 공유**:
1. Google Sheets 문서 열기
2. 우측 상단 **공유** 클릭
3. 서비스 계정 이메일 추가 (`credentials/service-account.json`의 `client_email` 값)
4. **뷰어** 권한 부여

### 3. 의존성 설치

```bash
# Option A: Poetry (권장)
poetry install

# Option B: pip
pip3 install -r requirements.txt
```

---

## 사용 방법

### Step 1: Google Sheets 데이터 준비

Google Sheets에 294개 컬럼 데이터 입력:
- **컬럼 A~KN**: 총 294개 컬럼
- **1행**: 헤더 (스킵됨)
- **2행 이상**: 상품 데이터

**스키마**: [../docs/GOOGLE_SHEETS_SCHEMA.md](../docs/GOOGLE_SHEETS_SCHEMA.md) 참조

### Step 2: 단일 상품 생성

```bash
python3 examples/generate_figma_editable_v4.py VD25FCA004
```

**출력 예시**:
```
============================================================
📋 Google Sheets 데이터 로드 및 HTML 생성
============================================================
Sheet ID: 1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
Product Code: VD25FCA004

✅ SheetsLoader 초기화 완료
✅ 데이터 로드 성공: 294개 컬럼

📦 상품 정보:
  코드: VD25FCA004
  이름: 베이직 코튼 티셔츠
  색상 개수: 4

✅ HTML 생성 완료: output/20251016/editable/VD25FCA004_editable.html
```

### Step 3: 배치 생성 (여러 상품)

**스크립트 수정**:
```python
# examples/generate_figma_editable_v4_batch.py
PRODUCT_CODES = [
    "VD25FCA004",
    "VD25FPT003",
    "VD25FDP013",
]
```

**실행**:
```bash
python3 examples/generate_figma_editable_v4_batch.py
```

**출력 예시**:
```
============================================================
📦 배치 HTML 생성 시작
============================================================
생성할 상품: 3개

[1/3] VD25FCA004 처리 중...
✅ 생성 완료: output/20251016/editable/VD25FCA004_editable.html

[2/3] VD25FPT003 처리 중...
✅ 생성 완료: output/20251016/editable/VD25FPT003_editable.html

[3/3] VD25FDP013 처리 중...
✅ 생성 완료: output/20251016/editable/VD25FDP013_editable.html

============================================================
✅ 배치 생성 완료: 3/3 성공
============================================================
```

### Step 4: Flask 서버로 편집 및 익스포트

**Flask 서버 실행**:
```bash
python3 scripts/server.py
```

**브라우저 열기**:
```
http://localhost:5001
```

**편집 및 익스포트**:
1. 파일 목록에서 editable HTML 선택
2. 이미지 크롭/줌 조정
3. 텍스트 편집
4. **HTML 다운로드** 또는 **JPG 다운로드** 클릭

**출력**:
- `output/{날짜}/export/{PRODUCT_CODE}_final.html`
- `output/{날짜}/export/{PRODUCT_CODE}_final.jpg`

---

## 출력 구조

```
output/
└── 20251016/                    # 날짜별 폴더 (YYYYMMDD)
    ├── editable/                # 편집 가능한 HTML
    │   ├── VD25FCA004_editable.html
    │   ├── VD25FPT003_editable.html
    │   └── VD25FDP013_editable.html
    └── export/                  # 익스포트된 파일
        ├── VD25FCA004_final.html
        ├── VD25FCA004_final.jpg
        ├── VD25FPT003_final.html
        └── VD25FPT003_final.jpg
```

---

## 문제 해결

### 1. `❌ Service Account 파일을 찾을 수 없습니다`

**원인**: 서비스 계정 파일이 없거나 경로가 잘못됨

**해결**:
```bash
# 파일 존재 확인
ls credentials/service-account.json

# 없으면 Google Cloud Console에서 다운로드
# docs/SETUP_GUIDE.md 참조
```

### 2. `❌ Sheet ID를 설정해주세요`

**원인**: 환경 변수 `GOOGLE_SHEET_ID`가 설정되지 않음

**해결**:
```bash
# .env 파일 확인
cat .env

# GOOGLE_SHEET_ID 값이 없으면 추가
echo "GOOGLE_SHEET_ID=your_sheet_id_here" >> .env
```

### 3. `❌ 403 Forbidden: The caller does not have permission`

**원인**: Google Sheets가 서비스 계정과 공유되지 않음

**해결**:
1. Google Sheets 문서 열기
2. 우측 상단 **공유** 클릭
3. 서비스 계정 이메일 추가 (뷰어 권한)
4. 전송

**서비스 계정 이메일 확인**:
```bash
grep client_email credentials/service-account.json
```

### 4. `❌ 404 Not Found: Requested entity was not found`

**원인**: Sheet ID가 잘못되었거나 Sheet가 삭제됨

**해결**:
```bash
# Google Sheets URL에서 Sheet ID 다시 확인
# https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
# {SHEET_ID} 부분을 복사하여 .env에 입력
```

### 5. `ModuleNotFoundError: No module named '...'`

**원인**: 필요한 패키지가 설치되지 않음

**해결**:
```bash
# Poetry 사용
poetry install

# 또는 pip
pip3 install -r requirements.txt
```

### 6. `⚠️ 컬럼 개수 불일치: 예상 294개, 실제 150개`

**원인**: Google Sheets의 실제 컬럼 개수가 294개보다 적음

**해결**:
1. Google Sheets 열기
2. 컬럼 A~KN까지 294개 확인
3. 누락된 컬럼이 있으면 추가 또는 빈 열 삽입

---

## 스크립트 목록

### 추천 스크립트 (V4)

| 스크립트 | 설명 | 사용 시점 |
|---------|------|----------|
| `generate_figma_editable_v4.py` | 단일 상품 Editable HTML 생성 | 테스트/개별 생성 |
| `generate_figma_editable_v4_batch.py` | 여러 상품 배치 생성 | 대량 생성 |
| `load_sample.py` | 데이터 로드 테스트 | 데이터 검증 |

### 레거시 스크립트 (V1~V3)

| 스크립트 | 설명 | 비고 |
|---------|------|------|
| `generate_figma_editable.py` | V1 Editable HTML | V4 사용 권장 |
| `generate_figma_editable_v2.py` | V2 개선 버전 | V4 사용 권장 |
| `generate_figma_editable_v3.py` | V3 추가 기능 | V4 사용 권장 |
| `generate_figma_batch.py` | 배치 생성 (레거시) | V4 batch 사용 권장 |
| `generate_figma_final.py` | 최종 버전 (레거시) | V4 사용 권장 |
| `generate_figma_continuous.py` | 연속 레이아웃 테스트 | 참고용 |
| `generate_figma_continuous_2x.py` | 2배율 연속 레이아웃 | 참고용 |
| `generate_test_html.py` | HTML 테스트 | 개발 전용 |
| `generate_figma_html.py` | 기본 Figma HTML | 개발 전용 |

---

## 다음 단계

1. ✅ **데이터 검증**: `load_sample.py`로 Google Sheets 데이터 검증
2. ✅ **테스트 생성**: `generate_figma_editable_v4.py`로 단일 상품 생성
3. ✅ **Flask 서버**: `python3 scripts/server.py`로 편집 및 익스포트
4. ✅ **배치 생성**: `generate_figma_editable_v4_batch.py`로 여러 상품 생성

---

## 관련 문서

- **설정 가이드**: [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md)
- **사용 가이드**: [../docs/USAGE_GUIDE.md](../docs/USAGE_GUIDE.md)
- **스키마 문서**: [../docs/GOOGLE_SHEETS_SCHEMA.md](../docs/GOOGLE_SHEETS_SCHEMA.md)
- **프로젝트 README**: [../README.md](../README.md)

---

**최종 업데이트**: 2025-10-16
**작성자**: MoAI-ADK
