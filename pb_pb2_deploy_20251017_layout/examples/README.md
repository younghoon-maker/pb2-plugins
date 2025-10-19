# Examples - 예제 스크립트

pb_pb2_new_page 프로젝트의 샘플 및 테스트 스크립트 모음입니다.

> **⚠️ 정규 스크립트는 `scripts/` 폴더로 이동되었습니다**
> - 단일 제품 생성: `scripts/generate_editable_html.py`
> - 배치 생성: `scripts/generate_batch.py`
> - 최종 HTML 생성: `scripts/generate_final_html.py`
>
> 구버전 파일들은 `examples/archive/`에 보관되어 있습니다.

---

## 📋 목차

1. [정규 스크립트 (Production)](#정규-스크립트-production)
2. [예제 스크립트](#예제-스크립트)
3. [아카이브 (구버전)](#아카이브-구버전)
4. [사전 준비](#사전-준비)
5. [사용 방법](#사용-방법)
6. [문제 해결](#문제-해결)

---

## 정규 스크립트 (Production)

> **프로덕션 스크립트는 `../scripts/` 폴더에 있습니다**

### 1. `scripts/generate_editable_html.py` - 단일 상품 생성 ⭐

**가장 많이 사용되는 스크립트**입니다. 하나의 상품 코드를 지정하여 Editable HTML을 생성합니다.

```bash
# 사용법
python3 scripts/generate_editable_html.py <PRODUCT_CODE>

# 예시
python3 scripts/generate_editable_html.py VD25FCA004
```

**출력**:
- `output/{날짜}/editable/{PRODUCT_CODE}_editable_v4.html`

**특징**:
- 이미지 크롭/줌 컨트롤
- 텍스트 편집 (contenteditable)
- 페이지 줌 (30-100%)
- 사이즈 이미지 선택기
- localStorage 설정 저장
- 스포이드 도구 (Canvas 기반 색상 추출)
- JPG 익스포트 (타일링 방식)

---

### 2. `scripts/generate_batch.py` - 배치 생성 ⚡

여러 상품을 한 번에 생성합니다.

```bash
# 특정 행 범위
python3 scripts/generate_batch.py --start 2 --end 5

# 모든 제품
python3 scripts/generate_batch.py --all

# 특정 행만
python3 scripts/generate_batch.py --rows 2,7,10
```

**출력**:
- `output/{날짜}/editable/{CODE}_editable_v4.html` (각 상품마다)

---

### 3. `scripts/generate_final_html.py` - 최종 HTML 생성

최종 버전 HTML을 생성합니다 (편집 기능 없음).

```bash
python3 scripts/generate_final_html.py <PRODUCT_CODE>
```

---

## 예제 스크립트

### `load_sample.py` - 데이터 로드 테스트 🔍

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
python3 scripts/generate_editable_html.py VD25FCA004
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

**실행**:
```bash
# 특정 행 범위
python3 scripts/generate_batch.py --start 2 --end 5

# 모든 제품
python3 scripts/generate_batch.py --all

# 특정 행만
python3 scripts/generate_batch.py --rows 2,7,10
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

### Step 4: Flask 서버로 편집 및 익스포트 (또는 독립 실행)

#### 방법 A: Flask 서버 사용 (권장)
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
4. **HTML 다운로드**: 서버에 저장 (`output/{날짜}/export/`)
5. **JPG 다운로드**: 서버에 저장 (`output/{날짜}/export/`)

#### 방법 B: 독립 실행 (서버 없이)
**Editable HTML 직접 열기**:
```bash
# 파일 탐색기에서 더블클릭 또는
open output/20251016/editable/VD25FCA004_editable_v4.html
```

**편집 및 익스포트**:
1. 이미지 크롭/줌 조정
2. 텍스트 편집
3. **JPG 다운로드**: 브라우저 다운로드 폴더에 직접 저장 (자동 fallback)

**제한사항**:
- ❌ HTML 익스포트 불가 (서버 필요)
- ✅ JPG 익스포트 가능 (클라이언트 다운로드)
- ❌ 파일 목록 브라우징 불가

**출력**:
- **서버 모드**: `output/{날짜}/export/{PRODUCT_CODE}_partN.jpg`
- **클라이언트 모드**: `~/Downloads/{PRODUCT_CODE}_partN.jpg`

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

### 7. `❌ JPG 익스포트 실패: 서버 연결 오류`

**원인**: Flask 서버가 실행 중이지 않음

**해결**:
자동 fallback이 작동하지 않을 경우:
1. 브라우저 콘솔 확인 (F12 → Console 탭)
2. Blob API 지원 여부 확인 (모던 브라우저 필수)
3. 브라우저 다운로드 권한 확인

또는 서버 실행:
```bash
python3 scripts/server.py
```

---

## V4 변경 이력

### 2025-10-17 - 히어로 섹션 레이아웃 개선 (v4.6)
- 🎨 **히어로 섹션 화이트 배경 최적화**
  - 화이트 배경 높이: 300px (이미지 1382px + 여백 300px = 1682px)
  - 이전 버전: 467px (기본) → 180px → 250px → **300px (최종)**
  - 상품명과 설명이 더 잘 보이도록 여백 확대
  - 파일: `scripts/generate_final_html.py` (Line 257: `height: 1682px`)
  - 영향: 모든 editable HTML 생성에 자동 적용
  - 배포 패키지: `pb_pb2_deploy_20251017_layout.tar.gz` 포함

### 2025-10-16 - 버그 수정
- 🐛 **이미지 디폴트 표시 버그 수정**
  - 첫 로딩 시 이미지가 x:100, y:100, scale:100 (중앙, 100% 줌)으로 올바르게 표시됨
  - localStorage가 없을 때도 CSS transform이 정상 적용되도록 수정
  - 파일: `generate_figma_editable_v4.py`
  - 배포 패키지: `pb_pb2_deploy_20251016_bugfix.tar.gz` 포함

---

## 아카이브 (구버전)

구버전 스크립트들은 `archive/` 폴더에 보관되어 있습니다.

### V4 이전 버전 (참고용)

| 파일 | 설명 | 비고 |
|------|------|------|
| `archive/generate_figma_editable.py` | V1 Editable HTML | 첫 버전 |
| `archive/generate_figma_editable_v2.py` | V2 개선 버전 | 크롭 기능 추가 |
| `archive/generate_figma_editable_v3.py` | V3 추가 기능 | 스포이드 초기 버전 |
| `archive/generate_figma_batch.py` | 배치 생성 (구버전) | 행 번호 하드코딩 |
| `archive/generate_figma_final.py.backup` | 최종 HTML 백업 | 백업 파일 |
| `archive/generate_figma_continuous.py` | 연속 레이아웃 테스트 | 실험용 |
| `archive/generate_figma_continuous_2x.py` | 2배율 연속 레이아웃 | 실험용 |
| `archive/generate_test_html.py` | HTML 테스트 | 개발 전용 |
| `archive/generate_figma_html.py` | 기본 Figma HTML | 개발 전용 |

> ⚠️ 아카이브된 파일들은 더 이상 사용하지 않습니다. `scripts/` 폴더의 V4 스크립트를 사용하세요.

---

## 다음 단계

1. ✅ **데이터 검증**: `examples/load_sample.py`로 Google Sheets 데이터 검증
2. ✅ **테스트 생성**: `scripts/generate_editable_html.py`로 단일 상품 생성
3. ✅ **Flask 서버**: `python3 scripts/server.py`로 편집 및 익스포트
4. ✅ **배치 생성**: `scripts/generate_batch.py`로 여러 상품 생성

---

## 관련 문서

- **설정 가이드**: [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md)
- **사용 가이드**: [../docs/USAGE_GUIDE.md](../docs/USAGE_GUIDE.md)
- **스키마 문서**: [../docs/GOOGLE_SHEETS_SCHEMA.md](../docs/GOOGLE_SHEETS_SCHEMA.md)
- **프로젝트 README**: [../README.md](../README.md)

---

**최종 업데이트**: 2025-10-16
**작성자**: MoAI-ADK
