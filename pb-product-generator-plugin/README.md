# PB Product Generator - Claude Code Plugin

**Google Sheets 292컬럼 데이터 기반 제품 상세 페이지 생성기 - 완전 자동화 세팅**

Version: 1.0.2

---

## ✨ What's New in v1.0.2

🐛 **Bug Fixes**
- setup-from-private 커맨드 Bash 파싱 에러 수정
- 복잡한 변수 할당 `$(...)` 구문을 단계별 실행으로 변경
- Claude 실행 지침 명확화 (Step 1, 2, 3 분리)

## ✨ What's New in v1.0.1

🎨 **UX Improvements**
- 라이프스타일 갤러리: 이미지가 없는 컬러는 컬러칩 포함 전체 숨김 처리
- 빈 컨테이너 "이미지 추가" 로직 제거 (더 깔끔한 UI)

## ✨ What's New in v1.0.0

🏗️ **Official Claude Code Standard**
- 공식 Claude Code 플러그인 표준 준수
- plugin.json 스키마 표준화
- 버전 Major 업데이트 (안정 버전 출시)
- 292-columns 키워드 추가 (명확한 컬럼 수 표시)

## ✨ What's New in v0.2.6

🐛 **Critical Bug Fixes**
- 음수 사이즈 값 처리 개선 (음수를 빈 셀로 자동 처리)
- 사이즈표 누락 컬럼 추가 (상의: 밑단/소매통, 하의: 총장)
- 날짜 기반 폴더 구조 적용 (output/{date}/editable/)
- 서버 OUTPUT_DIR 환경변수 지원 (.env 기반 경로 설정)

## ✨ What's New in v0.2.1

🐛 **Bug Fixes**
- 사이즈표 파싱 로직 버그 수정 (hem, sleeve_cuff, length 필드 추가)
- product_description 필드 볼드 서식 지원
- safe_float() 헬퍼 함수로 안정성 향상

## ✨ What's New in v0.2.0

🎯 **완전 자동화 세팅**
- 5분 만에 설치부터 실행까지 완료
- `setup.sh` 스크립트로 원클릭 설정
- `PRIVATE_SETUP.md` 프라이빗 세팅 가이드 제공

🏗️ **원본 코드 포함**
- 검증된 원본 스크립트 (2116 lines) 직접 실행
- 전체 소스 코드 (`src/`, `templates/`) 패키징
- 코드 재생성 없이 안정적인 결과물 보장

📊 **70MB 고품질 출력**
- 원본 프로세스와 동일한 결과물 생성
- Base64 인코딩 이미지 (self-contained)
- Editable HTML V4 (crop/zoom, text edit)

---

## 🚀 Quick Start (5분)

### Step 1: 마켓플레이스 추가

```bash
# Claude Code 실행
/plugin marketplace add younghoon-maker/pb2-plugins
```

### Step 2: 플러그인 설치

```bash
/plugin install pb-product-generator@pb2-plugins
```

### Step 3: Claude 재시작

```bash
/quit
claude
```

### Step 4: 자동 세팅

PRIVATE_SETUP.md 파일을 관리자로부터 받아 프로젝트 폴더에 복사한 후:

```bash
/pb-product-generator:setup-from-private
```

**자동으로 처리되는 작업**:
- ✅ credentials/ 폴더 생성
- ✅ service-account.json 생성
- ✅ .env 파일 생성
- ✅ Python 의존성 설치
- ✅ output/ 폴더 생성

### Step 5: 사용

```bash
/pb-product-generator:generate VD25FPT003
```

**예상 결과**:
```
✅ Successfully loaded 1 products
✅ Generated: output/20251018/editable/VD25FPT003_editable_v4.html (70 MB)

🎨 Features:
- Image crop/zoom editor
- Text editing (contenteditable)
- Page zoom (30-100%)
- HTML/JPG download
```

---

## 📦 Features

### ✨ Google Sheets 통합
- **292컬럼 완벽 지원** (A-KN)
- **Service Account 인증** (자동 설정)
- **Google Drive 이미지** 자동 다운로드
- **Sheet ID**: `1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk`
- **Tab Name**: `new_raw` (하드코딩)

### 🎨 Editable HTML V4
- **이미지 편집**: Pan X/Y (-50~+50), Zoom (100~500%)
- **텍스트 편집**: contenteditable 전체 텍스트
- **페이지 줌**: 30-100% (기본 60%)
- **익스포트**: HTML/JPG 다운로드

### 🚀 Claude Code 플러그인
- **슬래시 커맨드**: `/pb-product-generator:generate`, `/pb-product-generator:batch`, `/pb-product-generator:server`
- **자동 세팅**: `/pb-product-generator:setup-from-private`
- **원본 스크립트**: `generate_editable_html.py` (2116 lines)

---

## 📋 Commands

### 1. 단일 제품 생성

```bash
/pb-product-generator:generate {product_code}
```

**예시**:
```bash
/pb-product-generator:generate VD25FPT003
```

**출력**:
```
✅ Successfully loaded 1 products
✅ Generated: output/20251018/editable/VD25FPT003_editable_v4.html (70 MB)
```

### 2. 여러 제품 배치 생성

```bash
/pb-product-generator:batch {code1} {code2} {code3} ...
```

**예시**:
```bash
/pb-product-generator:batch VD25FPT003 VD25FPT005 VD25FCA004
```

**출력**:
```
🚀 Batch Generation Started
📋 Products: 3

[1/3] VD25FPT003 ✅ (70 MB)
[2/3] VD25FPT005 ✅ (68 MB)
[3/3] VD25FCA004 ✅ (65 MB)

✅ Batch Complete: 3 succeeded, 0 failed
```

### 3. Flask 편집 서버 실행

```bash
/pb-product-generator:server
```

**결과**:
- `http://localhost:5001` 자동 실행
- Editable HTML 파일 목록 제공
- 이미지 편집 및 HTML/JPG 익스포트

### 4. 자동 세팅

```bash
/pb-product-generator:setup-from-private
```

**자동 설정 작업**:
1. PRIVATE_SETUP.md 파일 읽기
2. Service Account JSON 추출
3. credentials/ 폴더 및 파일 생성
4. .env 파일 생성
5. Python 의존성 설치

---

## 📁 Plugin Structure

```
pb-product-generator-plugin/
├── .claude-plugin/
│   └── plugin.json                # 플러그인 메타데이터 (v0.2.1)
├── commands/
│   ├── generate.md                # /generate 커맨드
│   ├── batch.md                   # /batch-generate 커맨드
│   └── server.md                  # /start-server 커맨드
├── agents/
│   └── product-builder.md         # Product Builder 에이전트
├── scripts/
│   ├── generate_editable_html.py  # 원본 단일 제품 생성 (2116 lines)
│   ├── generate_batch.py          # 원본 배치 생성 (311 lines)
│   └── server.py                  # 원본 Flask 서버 (13K)
├── src/                           # 전체 Python 소스 코드
│   ├── sheets_loader/
│   │   ├── loader.py              # TAB_NAME = "new_raw"
│   │   ├── product_builder.py
│   │   └── column_mapping.py      # 292컬럼 매핑
│   ├── models/
│   │   └── product_data.py        # Pydantic ProductData
│   ├── parsers/
│   ├── clients/
│   ├── utils/
│   └── validators/
├── templates/                     # 전체 Jinja2 템플릿
│   ├── base.html.jinja2
│   └── sections/                  # 10개 섹션 템플릿
├── credentials/
│   └── service-account.json       # Service Account (자동 생성)
├── .env                           # 환경 변수 (자동 생성)
├── .gitignore                     # PRIVATE_SETUP.md 제외
├── setup.sh                       # 자동 세팅 스크립트
├── PRIVATE_SETUP.md               # 프라이빗 세팅 가이드 (Git 제외)
├── requirements.txt               # Python 의존성
└── README.md
```

---

## 🔧 Environment Configuration

**자동 생성되는 .env 파일**:
```bash
GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
FLASK_PORT=5001
FLASK_DEBUG=False

# 서버 사용 시 출력 디렉토리 (절대 경로 권장)
# OUTPUT_DIR=/Users/yourname/project/output
```

**하드코딩된 값**:
- **Sheet ID**: `1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk`
- **Tab Name**: `new_raw` (src/sheets_loader/loader.py)
- **Flask Port**: 5001

---

## 📚 Documentation

### 🚀 시작하기
- **⭐ 프라이빗 세팅 가이드 (필독)**: `PRIVATE_SETUP.md` (Git 제외)
  - 서비스 어카운트 JSON 포함
  - 5분 완성 세팅 가이드
  - Sheet ID 및 탭 이름 명기
- **📖 플러그인 가이드**: [pb-plugins/INSTALLATION_GUIDE.md](../INSTALLATION_GUIDE.md)

### 📝 커맨드 문서
- [generate.md](./commands/generate.md) - 단일 제품 생성
- [batch.md](./commands/batch.md) - 배치 생성
- [server.md](./commands/server.md) - Flask 서버

### 🤖 에이전트 문서
- [product-builder.md](./agents/product-builder.md) - 제품 페이지 생성 전문가

---

## 🔍 Troubleshooting

### ❌ Service Account 파일 없음

**증상**: `❌ Service Account file NOT found`

**해결**:
```bash
cd ~/.claude/plugins/pb-product-generator/
ls credentials/service-account.json  # 파일 존재 확인

# 없으면 PRIVATE_SETUP.md Step 2.2 다시 실행
```

### ❌ API 권한 에러

**증상**: `❌ HttpError 403: Forbidden`

**해결**:
1. Google Sheets 열기: https://docs.google.com/spreadsheets/d/1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk/edit
2. 공유 버튼 클릭
3. Service Account 이메일 추가: `test-account-n8n@damoa-fb351.iam.gserviceaccount.com`
4. 권한: **뷰어** 선택
5. 보내기 클릭

### ❌ Python 의존성 에러

**증상**: `ModuleNotFoundError: No module named 'google'`

**해결**:
```bash
cd ~/.claude/plugins/pb-product-generator/
pip3 install -r requirements.txt
```

### ❌ Port 충돌

**증상**: `Address already in use (Port 5001)`

**해결**:
```bash
# macOS/Linux
lsof -ti:5001 | xargs kill -9

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

---

## 📊 Version History

### v0.2.6 (2025-10-20) - 🐛 Critical Bug Fixes

**Bug Fixes**:
- ✅ 음수 사이즈 값 처리: safe_float() 함수에서 음수를 None으로 변환
  - VD25FJP003 같은 케이스에서 -86 값 자동 제외
- ✅ 사이즈표 누락 컬럼 수정:
  - 상의: hem(밑단), sleeve_cuff(소매통) 추가
  - 하의: length(총장) 추가
  - 빈 값 처리 로직 추가 (`if value else '-'`)
- ✅ 날짜 기반 폴더 구조: output/{YYYYMMDD}/editable/ 적용
- ✅ 서버 경로 설정: OUTPUT_DIR 환경변수 지원
  - dotenv 로딩 추가
  - .env 파일에서 절대 경로 설정 가능

**Verification**:
- ✅ VD25FPT007, VD25FJP003 생성 테스트 통과
- ✅ 사이즈표 모든 컬럼 정상 출력
- ✅ JPG 다운로드 정확한 경로 저장 확인 (4.7MB, 3.7MB)

### v0.2.1 (2025-10-19) - 🐛 Bug Fixes

**Bug Fixes**:
- ✅ 사이즈표 파싱 로직 버그 수정
  - _parse_top_sizes(): hem, sleeve_cuff 필드 추가
  - _parse_bottom_sizes(): length 필드 추가
  - safe_float() 헬퍼 함수 도입
  - 검증 로직 개선 (size_name만 필수)
- ✅ product_description 필드 볼드 서식 지원
- ✅ column_mapping.py 인덱스 보정 (+1 shift)

**Documentation**:
- ✅ 네임스페이스 접두사 추가 (`/pb-product-generator:*`)
- ✅ GitHub 마켓플레이스 URL 업데이트
- ✅ 사용자 프로젝트 폴더 기반 워크플로우 문서화

### v0.2.0 (2025-10-18) - 🎯 Complete Automation

**Major Changes**:
- ✅ 완전 자동화 세팅 (`setup.sh` 스크립트)
- ✅ 원본 코드 직접 포함 (코드 재생성 제거)
- ✅ 프라이빗 세팅 가이드 (`PRIVATE_SETUP.md`)
- ✅ Sheet ID 및 탭 이름 하드코딩
- ✅ 원본 스크립트 직접 호출 (wrapper 제거)
- ✅ 70MB 고품질 출력 보장

**Breaking Changes**:
- ❌ `.env.example` 제거 (자동 생성으로 대체)
- ❌ 수동 설정 과정 제거 (setup.sh로 자동화)
- ❌ 코드 생성 래퍼 제거 (원본 스크립트 사용)

### v0.1.2 (2025-10-17) - Lifestyle Gallery & Data Enhancement

**Changes**:
- 🎨 Lifestyle Gallery 이미지 비율 수정
- 📊 Product description 필드 추가
- 🖼️ Model 및 fabric 이미지 지원
- 🔧 Google Drive 이미지 다운로드 통합

---

## 🤝 Support

**팀 지원**:
- **이메일**: pb-team@company.com
- **슬랙**: #pb-product-generator
- **문서**: `README.md`, `PRIVATE_SETUP.md`, `commands/`

**문제 보고**:
1. README.md 및 PRIVATE_SETUP.md 참고
2. 환경 변수 설정 확인 (`.env`)
3. Google Sheets 권한 검증
4. 팀 슬랙 채널에 문의

---

## 📝 License

Private project.

© 2025 PB Product Team. All Rights Reserved.
