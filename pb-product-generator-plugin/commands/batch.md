---
description: 여러 제품을 한 번에 배치 생성
tools: [Bash]
---

# Batch Generate Product Pages

여러 제품 코드를 받아 순차적으로 Editable HTML을 생성합니다.

## 작업 프로세스

1. **제품 코드 목록 입력**: 공백 또는 쉼표로 구분된 제품 코드
2. **순차 생성**: 각 제품별로 Google Sheets 데이터 로드 및 HTML 생성
3. **진행 상황 보고**: 실시간 진행 상황 및 성공/실패 통계
4. **일괄 저장**: `output/{YYYYMMDD}/editable/` 폴더에 모든 파일 저장

## 사용법

```bash
/batch-generate {product_code1} {product_code2} {product_code3} ...
```

**예시**:
```bash
/batch-generate VD25FTS002 VD25FPT003 VD25FCA004
```

## 출력

```
🚀 Batch Generation Started
📋 Products: 3

[1/3] VD25FTS002 ✅ (51.4 MB)
[2/3] VD25FPT003 ✅ (73.2 MB)
[3/3] VD25FCA004 ✅ (45.8 MB)

✅ Batch Complete: 3 succeeded, 0 failed
📁 Output: output/20251017/editable/
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

현재 프로젝트 폴더의 `output/{YYYYMMDD}/editable/`에 HTML 파일을 생성합니다:

```bash
python3 ~/.claude/plugins/pb-product-generator/scripts/generate_batch.py --rows 2,5,10
```

**참고**: 출력 파일은 현재 작업 디렉토리의 `output/` 폴더에 저장됩니다.
