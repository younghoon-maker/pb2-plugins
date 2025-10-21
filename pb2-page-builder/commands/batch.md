---
description: 여러 제품을 한 번에 배치 생성
---

# Batch Generate Product Pages

여러 제품 코드를 받아 순차적으로 Editable HTML을 생성합니다.

## 작업 프로세스

1. **제품 코드 목록 입력**: 공백 또는 쉼표로 구분된 제품 코드
2. **순차 생성**: 각 제품별로 Google Sheets 데이터 로드 및 HTML 생성
3. **진행 상황 보고**: 실시간 진행 상황 및 성공/실패 통계
4. **일괄 저장**: `output/{YYYYMMDD}/editable/` 폴더에 모든 파일 저장

## 사용법

### 기본: 수동 입력
```bash
/pb2-page-builder:batch {product_code1} {product_code2} {product_code3} ...
```

**예시**:
```bash
/pb2-page-builder:batch VD25FTS002 VD25FPT003 VD25FCA004
```

### 전체 제품 생성
Google Sheets A열의 모든 제품 코드를 자동으로 감지하여 생성:
```bash
/pb2-page-builder:batch --all
```

### 필터링 생성
특정 패턴과 매칭되는 제품만 생성 (대소문자 무시):
```bash
/pb2-page-builder:batch --filter=FTS      # FTS 포함하는 제품만
/pb2-page-builder:batch --filter=VD25     # VD25 포함하는 제품만
/pb2-page-builder:batch --filter=FPT003   # FPT003 포함하는 제품만
```

## 출력

### 수동 입력 모드
```
📋 수동 입력: 3개 제품
🚀 Batch Generation Started
📋 Products: 3

[1/3] VD25FTS002 ✅ (51.4 MB)
[2/3] VD25FPT003 ✅ (73.2 MB)
[3/3] VD25FCA004 ✅ (45.8 MB)

✅ Batch Complete: 3 succeeded, 0 failed
📁 Output: output/20251017/editable/
```

### --all 플래그
```
📊 시트에서 47개 제품 발견
🚀 Batch Generation Started
📋 Products: 47

[1/47] VD25FTS002 ✅ (51.4 MB)
[2/47] VD25FPT003 ✅ (73.2 MB)
[3/47] VD25FCA004 ✅ (45.8 MB)
...
[47/47] VD25FDP013 ✅ (62.1 MB)

✅ Batch Complete: 45 succeeded, 2 failed
📁 Output: output/20251017/editable/
```

### --filter 플래그
```
🔍 8개 제품 매칭 (필터: FTS)
🚀 Batch Generation Started
📋 Products: 8

[1/8] VD25FTS002 ✅ (51.4 MB)
[2/8] VD25FTS005 ✅ (68.1 MB)
[3/8] VD25FTS009 ✅ (55.3 MB)
...
[8/8] VD25FTS027 ✅ (71.2 MB)

✅ Batch Complete: 8 succeeded, 0 failed
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

## 구현

이 커맨드는 플러그인 내부의 원본 배치 생성 스크립트를 직접 실행합니다:

```python
# pb2-page-builder/scripts/generate_batch.py
python3 scripts/generate_batch.py {product_code1} {product_code2} ...
```
