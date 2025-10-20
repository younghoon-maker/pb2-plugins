---
description: 여러 Dana&Peta 제품 HTML 배치 생성
---

# Batch Generate Products

Google Sheets에서 여러 제품 데이터를 한 번에 로드하여 Editable HTML을 배치 생성합니다.

## 사용법

```bash
# 개별 제품 코드 나열
/dana-page-builder:batch-generate DN25FW001 DN25FW002 DN25FW003

# 또는 all로 전체 제품 생성
/dana-page-builder:batch-generate all
```

## 작업 프로세스

1. **제품 코드 파싱**: 인자로 전달된 제품 코드 목록 파싱
2. **Google Sheets 연결**: 서비스 어카운트로 인증
3. **데이터 로드**: 요청서 탭에서 모든 제품 데이터 로드
4. **제품 필터링**: 지정된 제품만 선택 (all일 경우 전체)
5. **이미지 다운로드**: Google Drive 이미지 일괄 다운로드 (캐시 활용)
6. **HTML 배치 생성**: 각 제품마다 Editable HTML 생성
7. **진행상황 표시**: 완료된 제품 수 / 전체 제품 수
8. **요약 보고**: 성공/실패 통계

## 출력 예시

```
📋 Loading products from Google Sheets...
✅ Found 3 products to generate

📥 Downloading images from Google Drive...
✅ Downloaded 67 images (45.2 MB)
   Cache hits: 12 images (8.1 MB)

🎨 Generating HTML pages...
[1/3] ✅ DN25FW001 (22 images, 45 MB)
[2/3] ✅ DN25FW002 (23 images, 47 MB)
[3/3] ✅ DN25FW003 (22 images, 44 MB)

📊 Summary:
   Total: 3 products
   Success: 3 products
   Failed: 0 products
   Total size: 136 MB

📁 Created files in output/20251020/에디터블/:
   - DN25FW001_editable.html
   - DN25FW002_editable.html
   - DN25FW003_editable.html

🎯 Next steps:
   /dana-page-builder:start-server
```

## 필수 조건

- **credentials/service-account.json**: 서비스 어카운트 파일 존재
- **.env**: 환경 변수 설정
- **Python 3.8+**: python3 실행 가능
- **의존성**: gspread, Pillow, jinja2, numpy 설치됨

## 에러 처리

### 제품 코드 누락
```
❌ At least one product code is required
   Usage: /dana-page-builder:batch-generate DN25FW001 DN25FW002
   Or: /dana-page-builder:batch-generate all
```

### 일부 제품 실패
```
📊 Summary:
   Total: 3 products
   Success: 2 products
   Failed: 1 product

❌ Failed products:
   - DN25FW999: Product not found in Google Sheets
```

## 구현

이 커맨드는 다음 Python 스크립트를 실행합니다:

```bash
PLUGIN_DIR="$HOME/.claude/plugins/marketplaces/pb2-marketplace/dana-page-builder"

# 개별 제품
python3 "$PLUGIN_DIR/scripts/generate_pages_dana.py" --products DN25FW001 DN25FW002

# 전체 제품
python3 "$PLUGIN_DIR/scripts/generate_pages_dana.py"
```

## 출력 파일 구조

```
output/
└── 20251020/
    └── 에디터블/
        ├── DN25FW001_editable.html
        ├── DN25FW002_editable.html
        └── DN25FW003_editable.html
```

## 성능 최적화

### 이미지 캐싱
- **캐시 위치**: `output/assets/images/`
- **캐시 크기**: 최대 100 MB
- **캐시 히트율**: 일반적으로 80% 이상
- **다운로드 시간**: 캐시 활용 시 10배 이상 빠름

### 병렬 처리
- **이미지 다운로드**: 10개씩 병렬 처리
- **HTML 생성**: 순차 처리 (메모리 사용량 제어)

## 사용 사례

### 1. 신규 제품 전체 생성
```bash
# 모든 제품 생성
/dana-page-builder:batch-generate all
```

### 2. 특정 카테고리만 생성
```bash
# 여성복 상의 3개
/dana-page-builder:batch-generate DN25FW001 DN25FW002 DN25FW003
```

### 3. 업데이트된 제품만 재생성
```bash
# 데이터가 변경된 제품만
/dana-page-builder:batch-generate DN25FW001 DN25FW005
```

## 다음 단계

생성 후 다음과 같이 활용할 수 있습니다:

### Flask 서버로 확인
```bash
/dana-page-builder:start-server
# http://localhost:5002 접속
```

### 개별 제품 재생성
```bash
# 특정 제품만 다시 생성
/dana-page-builder:generate DN25FW001
```

## 로그 파일

배치 생성 과정은 다음 로그 파일에 기록됩니다:

```
dana_page_generation.log
```

로그 확인:
```bash
tail -f dana_page_generation.log
```

## 참고

- **권장 제품 수**: 10개 이하 (메모리 사용량 고려)
- **대량 생성 시**: 분할하여 실행 (예: 10개씩)
- **캐시 정리**: `rm -rf output/assets/images/*`
- **Sheet ID**: `1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk`
