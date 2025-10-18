---
description: 여러 제품을 한 번에 배치 생성 (개별 선택 또는 전체 자동)
tools: [Bash]
---

# Batch Generate Product Pages

여러 제품을 순차적으로 Editable HTML을 생성합니다. 개별 제품 코드 지정 또는 시트 전체 자동 생성을 지원합니다.

## 작업 프로세스

1. **제품 선택**: 개별 코드, 전체 자동, 행 범위, 또는 특정 행 선택
2. **순차 생성**: 각 제품별로 Google Sheets 데이터 로드 및 HTML 생성
3. **진행 상황 보고**: 실시간 진행 상황 및 성공/실패 통계
4. **일괄 저장**: `output/{YYYYMMDD}/editable/` 폴더에 모든 파일 저장

## 사용법

### 방법 1: 개별 제품 코드 지정 (기존 방식)

```bash
/batch-generate {product_code1} {product_code2} {product_code3} ...
```

**예시**:
```bash
/batch-generate VD25FTS002 VD25FPT003 VD25FCA004
```

### 방법 2: 시트의 모든 제품 자동 생성 ⭐ NEW

```bash
/batch-generate --all
```

**동작**:
- Google Sheets를 스캔하여 제품 코드가 있는 모든 행 자동 탐지
- 빈 행 건너뛰기
- 모든 제품 순차 생성

### 방법 3: 행 범위 지정

```bash
/batch-generate --start N --end M
```

**예시**:
```bash
# 2번 행부터 50번 행까지 생성
/batch-generate --start 2 --end 50
```

### 방법 4: 특정 행 선택

```bash
/batch-generate --rows N,M,K
```

**예시**:
```bash
# 2번, 5번, 10번, 15번 행만 생성
/batch-generate --rows 2,5,10,15
```

## 출력

### 개별 제품 코드 지정 시:

```
🚀 Batch Generation Started
📋 Products: 3

[1/3] VD25FTS002 ✅ (51.4 MB)
[2/3] VD25FPT003 ✅ (73.2 MB)
[3/3] VD25FCA004 ✅ (45.8 MB)

✅ Batch Complete: 3 succeeded, 0 failed
📁 Output: output/20251018/editable/
```

### `--all` 사용 시:

```
🚀 Batch Generation Started
📋 Scanning sheet for all products...
✅ Found 15 products

[1/15] VD25FPT003 ✅ (73.2 MB)
[2/15] VD25FPT005 ✅ (68.5 MB)
[3/15] VD25FCA004 ✅ (45.8 MB)
...
[15/15] VD25XXX015 ✅ (55.1 MB)

✅ Batch Complete: 15 succeeded, 0 failed
📁 Output: output/20251018/editable/
⏱️  Total time: 3m 45s
```

## 성능

- **순차 처리**: 메모리 효율성을 위해 한 번에 한 제품씩 처리
- **예상 시간**: 제품당 약 10-15초 (이미지 다운로드 포함)
- **메모리 사용**: 제품당 ~100MB, 순차 처리로 메모리 재사용

## 에러 처리

개별 제품 생성 실패 시 다음 제품 계속 진행:

```
[1/3] VD25FTS002 ✅ (51.4 MB)
[2/3] VD25FPT003 ❌ Product not found in sheets
[3/3] VD25FCA004 ✅ (45.8 MB)

✅ Batch Complete: 2 succeeded, 1 failed
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

### 방법 2: 수동 설정

Service Account 및 환경 변수 설정이 필요합니다. `/generate` 커맨드 문서 참조.

## 구현

현재 프로젝트 폴더의 `output/{YYYYMMDD}/editable/`에 HTML 파일을 생성합니다.

**스크립트 위치**:
```bash
~/.claude/plugins/marketplaces/{marketplace-name}/{plugin-name}/scripts/generate_batch.py
```

**실행 예시**:
```bash
# 스크립트 경로 자동 탐지
SCRIPT_PATH=$(find ~/.claude/plugins -name "generate_batch.py" -path "*/pb-product-generator*/scripts/*" | head -1)

# 환경 변수 로드 및 실행
# 모든 제품 생성
GOOGLE_SERVICE_ACCOUNT_FILE="$PWD/credentials/service-account.json" \
GOOGLE_SHEET_ID="$(grep GOOGLE_SHEET_ID .env 2>/dev/null | cut -d '=' -f2)" \
SHEET_TAB_NAME="$(grep SHEET_TAB_NAME .env 2>/dev/null | cut -d '=' -f2 || echo 'new_raw')" \
python3 "$SCRIPT_PATH" --all

# 특정 행 선택
GOOGLE_SERVICE_ACCOUNT_FILE="$PWD/credentials/service-account.json" \
GOOGLE_SHEET_ID="$(grep GOOGLE_SHEET_ID .env 2>/dev/null | cut -d '=' -f2)" \
SHEET_TAB_NAME="$(grep SHEET_TAB_NAME .env 2>/dev/null | cut -d '=' -f2 || echo 'new_raw')" \
python3 "$SCRIPT_PATH" --rows 2,5,10

# 행 범위 지정
GOOGLE_SERVICE_ACCOUNT_FILE="$PWD/credentials/service-account.json" \
GOOGLE_SHEET_ID="$(grep GOOGLE_SHEET_ID .env 2>/dev/null | cut -d '=' -f2)" \
SHEET_TAB_NAME="$(grep SHEET_TAB_NAME .env 2>/dev/null | cut -d '=' -f2 || echo 'new_raw')" \
python3 "$SCRIPT_PATH" --start 2 --end 50
```

**참고**:
- 출력 파일은 현재 작업 디렉토리의 `output/` 폴더에 저장됩니다
- 마켓플레이스 이름은 설치 방법에 따라 다를 수 있습니다 (예: `pb2-marketplace`)
