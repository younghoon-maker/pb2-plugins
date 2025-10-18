# PB Product Generator - Claude Code Plugin

**Google Sheets 292컬럼 데이터 기반 제품 상세 페이지 생성기 - 완전 자동화 세팅**

Version: 0.2.1

---

## ✨ What's New in v0.2.1

🤖 **완전 자동 환경 설정**
- PRIVATE_SETUP.md 파일만 받으면 모든 설정 완료
- Service Account JSON 자동 추출 및 설정
- `/setup-from-private` 커맨드로 원클릭 설정
- Python 기반 스마트 파싱 (JSON, Sheet ID, Tab Name)

🎯 **2단계 간소화 워크플로우**
1. PRIVATE_SETUP.md 파일 받기 (사용자로부터 배포)
2. `/setup-from-private` 실행 → 완료!

📊 **70MB 고품질 출력**
- 원본 프로세스와 동일한 결과물 생성
- Base64 인코딩 이미지 (self-contained)
- Editable HTML V4 (crop/zoom, text edit)

---

## 🚀 Quick Start (2분)

### Step 1: Marketplace 등록 및 플러그인 설치

```bash
# Claude Code에서 실행
/plugin marketplace add younghoon-maker/pb2-plugins
/plugin install pb-product-generator@pb2-plugins
```

### Step 2: PRIVATE_SETUP.md 파일 받기

**관리자로부터 PRIVATE_SETUP.md 파일을 받아서 프로젝트 폴더에 복사**:

```bash
# PRIVATE_SETUP.md 파일을 프로젝트 폴더에 복사
cp /path/to/PRIVATE_SETUP.md ./
```

> **🔒 보안**: `PRIVATE_SETUP.md`는 Service Account JSON을 포함하므로 절대 Git에 커밋하지 마세요 (.gitignore 등록됨)

### Step 3: 자동 환경 설정

**Claude Code에서 실행**:

```bash
/setup-from-private
```

**자동으로 처리되는 작업**:
- ✅ Service Account JSON 자동 추출 및 생성
- ✅ Google Sheets ID, Tab Name 자동 설정
- ✅ `.env` 파일 자동 생성
- ✅ `credentials/service-account.json` 자동 생성
- ✅ Python 의존성 자동 설치
- ✅ 출력 폴더 자동 생성

**예상 출력**:
```
🚀 PB Product Generator - Automatic Setup
==================================================

✅ Found PRIVATE_SETUP.md

📋 Parsing PRIVATE_SETUP.md...
   ✓ Service Account: test-account-n8n@damoa-fb351.iam.gserviceaccount.com
   ✓ Sheet ID: 1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
   ✓ Tab Name: new_raw

✅ Setup completed successfully!
```

### Step 4: 사용

```bash
# Claude Code에서 실행
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
- **슬래시 커맨드**: `/setup-from-private`, `/generate`, `/batch-generate`, `/start-server`
- **전문 에이전트**: `@agent-product-builder`
- **원본 스크립트**: `generate_editable_html.py` (2116 lines)
- **자동 설정**: `auto_setup.py` (Python 기반 PRIVATE_SETUP.md 파싱)

---

## 📋 Commands

### 0. 자동 환경 설정 (필수 - 최초 1회)

```bash
/setup-from-private
```

**설명**: PRIVATE_SETUP.md 파일에서 자동으로 모든 환경 설정

**요구사항**: 프로젝트 폴더에 `PRIVATE_SETUP.md` 파일 존재

**자동 처리**:
- Service Account JSON 추출 및 생성
- Google Sheets ID, Tab Name 자동 설정
- .env 파일 생성
- Python 의존성 설치

**상세 문서**: [setup-from-private.md](./commands/setup-from-private.md)

---

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

**상세 문서**: [generate.md](./commands/generate.md)

---

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

**상세 문서**: [batch.md](./commands/batch.md)

---

### 3. Flask 편집 서버 실행

```bash
/start-server
```

**결과**:
- `http://localhost:5001` 자동 실행
- Editable HTML 파일 목록 제공
- 이미지 편집 및 HTML/JPG 익스포트

**상세 문서**: [server.md](./commands/server.md)

---

### 4. 에이전트 사용

```bash
@agent-product-builder "VD25FPT003 생성해줘"
```

**에이전트 작업**:
1. Google Sheets 데이터 로드
2. 이미지 다운로드 및 Base64 인코딩
3. Editable HTML 생성
4. 결과 검증 및 후속 조치 안내

**상세 문서**: [product-builder.md](./agents/product-builder.md)

---

## 📁 Plugin Structure

```
pb-product-generator-plugin/
├── .claude-plugin/
│   └── plugin.json                # 플러그인 메타데이터 (v0.2.1)
├── commands/
│   ├── setup-from-private.md      # /setup-from-private 커맨드 (NEW!)
│   ├── generate.md                # /generate 커맨드
│   ├── batch.md                   # /batch-generate 커맨드
│   └── server.md                  # /start-server 커맨드
├── agents/
│   └── product-builder.md         # Product Builder 에이전트
├── scripts/
│   ├── auto_setup.py              # 자동 환경 설정 (NEW! - PRIVATE_SETUP.md 파싱)
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
├── setup.sh                       # 자동 세팅 스크립트 (v0.2.1 - 스마트 감지)
├── PRIVATE_SETUP.md.template      # PRIVATE_SETUP.md 템플릿 (참고용)
├── PRIVATE_SETUP.md               # 프라이빗 세팅 가이드 (Git 제외, 관리자가 배포)
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
- [setup-from-private.md](./commands/setup-from-private.md) - 자동 환경 설정 ⭐
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

### v0.2.1 (2025-10-18) - 🤖 Intelligent Auto-Setup

**Major Changes**:
- ✅ **완전 자동 환경 설정**: PRIVATE_SETUP.md 파일만 받으면 모든 설정 완료
- ✅ **Python 기반 스마트 파싱**: Service Account JSON, Sheet ID, Tab Name 자동 추출
- ✅ **/setup-from-private 커맨드**: 원클릭 설정 (사용자 친화적)
- ✅ **setup.sh 스마트 감지**: JSON 포함 시 auto_setup.py 자동 위임
- ✅ **2단계 간소화 워크플로우**: PRIVATE_SETUP.md 받기 → /setup-from-private 실행

**New Files**:
- `scripts/auto_setup.py` - PRIVATE_SETUP.md 파싱 및 자동 설정
- `commands/setup-from-private.md` - 자동 설정 커맨드 문서

**Enhanced Files**:
- `setup.sh` v0.2.1 - PRIVATE_SETUP.md JSON 자동 감지 및 Python 위임
- `README.md` - Quick Start 2분으로 단축, 새 워크플로우 반영

---

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
