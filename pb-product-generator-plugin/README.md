# PB Product Generator - Claude Code Plugin

**Google Sheets 292컬럼 데이터 기반 제품 상세 페이지 생성기 - 완전 자동화 세팅**

Version: 0.2.0

---

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

### Step 1: 플러그인 설치

```bash
# Claude Code에서 실행
/plugin marketplace add /path/to/pb-marketplace
/plugin install pb-product-generator@pb-marketplace
```

### Step 2: 자동 세팅

```bash
# 플러그인 디렉토리로 이동
cd ~/.claude/plugins/pb-product-generator/

# PRIVATE_SETUP.md 열어서 서비스 어카운트 JSON 복사
# (프라이빗 가이드 - Git에 올리지 않음)

# 자동 세팅 스크립트 실행
bash setup.sh
```

**setup.sh가 자동으로 처리**:
- ✅ credentials/ 폴더 확인
- ✅ .env 파일 생성 (Sheet ID, 탭 이름 하드코딩)
- ✅ Python 의존성 설치
- ✅ 실행 권한 설정

### Step 3: 사용

```bash
# Claude Code로 돌아와서
/generate VD25FPT003
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
- **슬래시 커맨드**: `/generate`, `/batch-generate`, `/start-server`
- **전문 에이전트**: `@agent-product-builder`
- **원본 스크립트**: `generate_editable_html.py` (2116 lines)

---

## 📋 Commands

### 1. 단일 제품 생성

```bash
/generate {product_code}
```

**예시**:
```bash
/generate VD25FPT003
```

**출력**:
```
✅ Successfully loaded 1 products
✅ Generated: output/20251018/editable/VD25FPT003_editable_v4.html (70 MB)
```

### 2. 여러 제품 배치 생성

```bash
/batch-generate {code1} {code2} {code3} ...
```

**예시**:
```bash
/batch-generate VD25FPT003 VD25FPT005 VD25FCA004
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
/start-server
```

**결과**:
- `http://localhost:5001` 자동 실행
- Editable HTML 파일 목록 제공
- 이미지 편집 및 HTML/JPG 익스포트

### 4. 에이전트 사용

```bash
@agent-product-builder "VD25FPT003 생성해줘"
```

**에이전트 작업**:
1. Google Sheets 데이터 로드
2. 이미지 다운로드 및 Base64 인코딩
3. Editable HTML 생성
4. 결과 검증 및 후속 조치 안내

---

## 📁 Plugin Structure

```
pb-product-generator-plugin/
├── .claude-plugin/
│   └── plugin.json                # 플러그인 메타데이터 (v0.2.0)
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
