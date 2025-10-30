# Changelog - pb-product-generator

All notable changes to the pb-product-generator plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.2] - 2025-10-30

### 🐛 Fixed
- **ModuleNotFoundError 해결** - 신규 설치 시 `No module named 'scripts.generate_final_html'` 오류 수정
  - `scripts/__init__.py` 추가: Python 패키지로 인식되도록 패키지 초기화 파일 생성
  - `generate_editable_html.py` (Line 239-250): 견고한 import 로직 추가
  - try-except 구문으로 플러그인/프로젝트 디렉토리 양쪽에서 실행 가능
  - 프로젝트 디렉토리에서 실행 시 자동으로 플러그인 경로를 sys.path에 추가

### 📦 Files Changed
- `scripts/__init__.py` (신규 생성, 20 lines)
  - 패키지 docstring 및 메타데이터 포함
- `scripts/generate_editable_html.py` (Line 239-250)
  - 견고한 import 로직으로 대체 (12 lines 추가)

### 🎯 Impact
- ✅ **신규 설치 즉시 사용 가능**: 별도 설정 없이 모든 환경에서 작동
- ✅ **하위 호환성 100% 유지**: 기존 사용자에게 영향 없음
- ✅ **유연한 실행 환경**: 플러그인 디렉토리와 프로젝트 디렉토리 양쪽 지원

---

## [2.0.1] - 2025-10-29

### 🐛 Fixed
- **Canvas 높이 자동 조절** - min-height 고정값 제거로 페이지 하단 과도한 여백 해결
  - `generate_final_html.py` (Line 240): Canvas div `min-height: 24018px` 제거
  - 페이지 컨테이너가 실제 콘텐츠 높이에 맞춰 자동 조절됨
  - 사이즈표 하단 과도한 공백 문제 완전 해결

- **Lifestyle Gallery 레이아웃 개선** - 이미지 간격 최적화
  - `generate_final_html.py` (Line 355): 갤러리 이미지 간격 `104px` → `21px`로 조정
  - 더 깔끔하고 밀도 높은 갤러리 레이아웃 제공

### ✨ Added
- **갤러리 섹션 인덱싱** - V4.2 Editable 기능 향상
  - `generate_editable_html.py` (Line 160-183): `add_gallery_section_indexes()` 함수 추가
  - 각 Lifestyle Gallery 섹션에 `data-gallery-index`, `data-gallery-color` 속성 부여
  - 색상별 갤러리 식별 및 관리 용이성 향상

### 📦 Files Changed
- `scripts/generate_final_html.py` (Line 240, 355)
  - Canvas min-height 제거
  - Gallery 이미지 간격 조정
- `scripts/generate_editable_html.py` (Line 160-183, 260-263)
  - 갤러리 섹션 인덱싱 함수 추가
  - 인덱싱 로직 통합

### 🎯 Impact
- ✅ 페이지 하단 여백 문제 완전 해결
- ✅ 갤러리 UI/UX 개선
- ✅ Editable 기능 확장성 향상
- ✅ 사용자 경험 개선 (불필요한 스크롤 제거)

---

## [1.0.6] - 2025-10-21

### ✨ Added
- **프로덕트 데이터 정리 기능 추가** - products.json 파일 자동 정리
  - `--data`: 프로덕트 데이터만 정리 (data/products.json)
  - `--data --days N`: N일 이전 products.json 파일 삭제
  - 서브 디렉토리의 products.json도 자동 감지 및 정리
  - `--data-dir PATH`: 데이터 디렉토리 경로 지정 (기본: data/)

### 📋 Changed
- **cleanup 커맨드 4가지 타입으로 확장** - HTML, 이미지, 데이터, 캐시 분리
  - `--all`: HTML + 이미지 + 데이터 + Figma 캐시 모두 삭제 (기존: HTML + 이미지 + 캐시)
  - `--stats`: 4가지 타입 통합 통계 표시
  - 타이틀: "Storage Cleanup (세분화)" 유지

### 📦 Files Changed
- `scripts/cleanup.py`: 프로덕트 데이터 정리 함수 추가 (596 → 713 lines, +117 lines)
  - `cleanup_products()`: products.json 파일 정리 함수
  - `show_stats()`: 프로덕트 데이터 통계 추가 (4번째 타입)
  - `cleanup_all()`: 4가지 타입 통합 삭제 (HTML + 이미지 + 데이터 + 캐시)
  - `main()`: --data, --data-dir 옵션 추가
- `commands/cleanup.md`: 프로덕트 데이터 정리 문서 추가 (399 → 455 lines, +56 lines)
  - 스토리지 구조에 data/ 디렉토리 추가
  - "4. 프로덕트 데이터만 정리" 섹션 신규 작성
  - 워크플로우 예시에 --data 옵션 추가
  - 옵션 테이블 업데이트 (--data, --data-dir 추가)

### 🎯 Use Cases
- **products.json 관리**: Google Sheets 로드 후 생성된 데이터 정리
- **개발/테스트 정리**: 반복 테스트로 누적된 임시 데이터 삭제
- **타입별 선택 정리**: HTML, 이미지, 데이터, 캐시 각각 독립적 관리
- **재생성 가능 데이터**: load_from_sheets.py 재실행으로 복구 가능

### 🔧 Technical Details
- 데이터 디렉토리: `data/` (기본값, 변경 가능)
- 서브 디렉토리 자동 감지: `data/*/products.json` 패턴 지원
- 날짜 기반 정리: products.json 수정 시간 기준
- 재생성 가능: Google Sheets API로 언제든 재생성

---

## [1.0.5] - 2025-10-20

### ✨ Added
- **스토리지 타입별 세분화 정리** - HTML, 이미지, 캐시를 개별 선택 가능
  - `--html --days N`: HTML 파일만 정리 (날짜별 폴더 + 루트 HTML)
  - `--images`: 이미지 캐시만 정리 (output/assets/images/)
  - `--images --days N`: N일 이전 이미지만 정리
  - `--cache`: Figma 캐시만 정리 (기존 기능 유지)

### 📋 Changed
- **cleanup 커맨드 완전 재구성** - 타입별 선택적 정리
  - `--all`: HTML + 이미지 + Figma 캐시 모두 삭제 (기존: HTML + 캐시)
  - `--stats`: HTML, 이미지, Figma 캐시 통합 통계 표시
  - 타이틀 변경: "Output & Cache Cleanup" → "Storage Cleanup (세분화)"
  - `--max-size`: HTML 파일만 해당 (명확화)

### 📦 Files Changed
- `scripts/cleanup.py`: 타입별 정리 함수 추가 (439 → 596 lines, +157 lines)
  - `cleanup_images()`: 이미지 캐시 정리 함수
  - `cleanup_html()`: HTML 파일 정리 함수 (별칭)
  - `cleanup_cache()`: Figma 캐시 정리 함수 (기존)
  - `cleanup_all()`: HTML + 이미지 + 캐시 통합 삭제
  - `show_stats()`: 3가지 타입 통합 통계
- `commands/cleanup.md`: 세분화 가이드 전면 개편 (328 → 399 lines, +71 lines)
  - 스토리지 구조 섹션 추가
  - 타입별 정리 방법 상세 설명
  - 워크플로우 타입별로 재구성

### 🎯 Use Cases
- **선택적 정리**: HTML만, 이미지만, 캐시만 개별 정리 가능
- **디스크 최적화**: 용량이 큰 이미지부터 선택적 삭제
- **정밀 관리**: 각 스토리지 타입에 다른 정책 적용 가능
- **타입별 주기 설정**: HTML 14일, 이미지 7일, 캐시 30일 등

### 🔧 Technical Details
- 이미지 디렉토리: `output/assets/images/` (기본값, 변경 가능)
- 지원 이미지 형식: jpg, jpeg, png, webp, gif
- HTML 폴더: `output/` (날짜별 폴더 + 루트 HTML)
- Figma 캐시: `.cache/figma/` (JSON 메타데이터)

---

## [1.0.4] - 2025-10-20

### ✨ Added
- **캐시 정리 기능 추가** - .cache/figma 폴더 자동 정리
  - `--cache`: 캐시 파일만 정리
  - `--cache --days N`: N일 이전 캐시 파일 삭제
  - 통합 스토리지 통계 (output + cache)

### 📋 Changed
- **cleanup 커맨드 확장** - Output과 캐시를 통합 관리
  - `--all`: output + cache 모두 삭제 (기존: output만)
  - `--stats`: output과 cache 통합 통계 표시
  - 타이틀 변경: "Output Cleanup" → "Storage Cleanup"

### 📦 Files Changed
- `scripts/cleanup.py`: 캐시 정리 함수 추가 (330 → 439 lines, +109 lines)
  - `cleanup_cache()`: 캐시 파일 정리 함수
  - `cleanup_all()`: output + cache 통합 삭제
  - `show_stats()`: 통합 통계 표시
- `commands/cleanup.md`: 캐시 정리 문서 추가 (262 → 328 lines, +66 lines)
  - 캐시만 정리 섹션 추가
  - 정리 대상에 캐시 폴더 추가
  - 워크플로우 예시 확장

### 🎯 Use Cases
- **캐시 관리**: Figma 메타데이터 캐시 주기적 정리
- **디스크 절약**: output + cache 통합 관리로 효율성 향상
- **선택적 정리**: output만, cache만, 또는 전체 정리 선택 가능

### 🔧 Technical Details
- 캐시 디렉토리: `.cache/figma/` (기본값, 변경 가능)
- 캐시 파일 형식: `{node-id}.json` (예: `1-95.json`)
- TTL 기반 캐시 (기본 1시간)
- 재생성 가능 (삭제 시 자동 재생성)

---

## [1.0.3] - 2025-10-20

### ✨ Added
- **cleanup 커맨드 추가** - output 폴더 자동 정리 기능
  - `/pb-product-generator:cleanup --stats`: 용량 및 파일 통계 표시
  - `/pb-product-generator:cleanup --days N`: N일 이전 파일 자동 삭제
  - `/pb-product-generator:cleanup --max-size MB`: 폴더 크기 제한
  - `/pb-product-generator:cleanup --all`: 전체 삭제 (확인 필요)
  - `--dry-run` 모드: 실제 삭제 전 시뮬레이션

### 📦 Files Changed
- `scripts/cleanup.py`: 정리 스크립트 (230 lines)
- `commands/cleanup.md`: 커맨드 문서
- `.claude-plugin/plugin.json`: cleanup 커맨드 등록

### 🎯 Use Cases
- **용량 관리**: output 폴더가 수백 MB 이상일 때 자동 정리
- **주기적 유지보수**: 오래된 파일 자동 삭제 (예: 7일 이전)
- **크기 제한**: 최대 크기 설정 (예: 500MB)
- **통계 확인**: 현재 용량 및 파일 현황 파악

### 🔧 Technical Details
- 날짜별 폴더 (YYYYMMDD) 기반 정리
- 파일 수정 시간 기준 정렬
- 크기 계산 및 포맷팅 (KB/MB/GB)
- 안전한 삭제 (dry-run, 사용자 확인)

---

## [1.0.2] - 2025-10-20

### 🐛 Fixed
- **setup-from-private 커맨드 Bash 파싱 에러 수정**
  - 복잡한 변수 할당 `$(...)` 구문을 단계별 실행으로 변경
  - Step 1, 2, 3 명확하게 분리하여 파싱 에러 방지
  - Claude 실행 지침 추가 (Internal section)

### 📦 Files Changed
- `commands/setup-from-private.md`: Lines 210-245 수정

### 🔧 Technical Details
- 기존: `SCRIPT_PATH=$(find ...) && python3 "$SCRIPT_PATH"` (파싱 에러)
- 개선: Step 1 (파일 확인) → Step 2 (경로 찾기) → Step 3 (실행) 분리
- 각 단계를 별도의 Bash 도구 호출로 실행하도록 명시

---

## [1.0.1] - 2025-10-20

### 🎨 Changed
- **라이프스타일 갤러리 UX 개선**: 이미지가 없는 컬러는 컬러칩 포함 전체 숨김 처리
  - 빈 컨테이너 "이미지 추가" 로직 제거 (17줄 삭제)
  - 더 깔끔한 레이아웃 제공
  - 사용자 경험 향상

### 📦 Files Changed
- `scripts/generate_final_html.py`: Lines 332-359 수정

### 🔧 Technical Details
- 이미지 확인 로직 개선: 컬러별 이미지 유무를 먼저 체크
- continue 문으로 빈 컬러 건너뛰기
- 불필요한 if-else 분기 제거

---

## [1.0.0] - 2025-10-20

### 🏗️ Breaking Changes
- **공식 Claude Code 플러그인 표준 준수**
- plugin.json 스키마 표준화
- 버전 Major 업데이트 (안정 버전 출시)

### ✨ Added
- **292-columns** 키워드 추가 (명확한 컬럼 수 표시)

### 📋 Changed
- plugin.json version: `0.2.5` → `1.0.0`
- Description 간결화: "Editable HTML V4" 명시
- 공식 플러그인 시스템 표준 완전 준수

### 🎯 Features (기존 유지)
- Google Sheets 292컬럼 데이터 로드
- PB 브랜드 제품 페이지 생성
- Editable HTML V4 with crop/zoom editor
- Flask 서버 (Port 5001)
- 이미지 캐싱 및 병렬 다운로드
- Product Builder Agent

### 📦 Technical
- Python 3.8+
- Google Sheets API v4
- Google Drive API
- Jinja2 템플릿 엔진
- Pydantic 데이터 검증
- Flask 웹 서버

---

## [0.2.5] - 2025-10-17

### Added
- 완전 자동화 세팅 기능
- PRIVATE_SETUP.md 기반 초기 설정

### Fixed
- 이미지 에디터 버그 수정
- 컬럼 매핑 개선

---

## [0.2.0] - 2025-10-15

### Added
- Editable HTML V4
- 이미지 crop/zoom 기능
- 브라우저 내 편집 기능

---

## [0.1.0] - 2025-10-10

### Initial Release
- 첫 번째 베타 버전
- 기본 HTML 생성 기능
- 292컬럼 지원
