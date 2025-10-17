# 📦 PB Product Generator - 설치 가이드

**Google Sheets 292컬럼 데이터 기반 제품 상세 페이지 생성기 v0.2.0**

> **⏱️ 총 소요 시간: 10분**
> - Phase 1: GitHub 설치 (2분)
> - Phase 2: 자동 세팅 (5분)
> - Phase 3: 기능 테스트 (3분)

---

## 📋 사전 요구사항

- ✅ **Claude Code**: 최신 버전 설치
- ✅ **Python**: 3.11+ 설치 (`python3 --version` 확인)
- ✅ **Git**: Git 설치 (`git --version` 확인)
- ✅ **PRIVATE_SETUP.md**: 팀에서 전달받은 프라이빗 세팅 가이드

---

## 🚀 Phase 1: GitHub 기반 설치 (2분)

### Step 1.1: 마켓플레이스 추가

Claude Code를 실행하고 다음 명령어 중 하나를 입력하세요:

```bash
# 방법 1: GitHub 사용자명/저장소명 (권장)
/plugin marketplace add younghoon-maker/pb2-plugins

# 방법 2: 전체 HTTPS URL
/plugin marketplace add https://github.com/younghoon-maker/pb2-plugins

# 방법 3: Git URL
/plugin marketplace add git@github.com:younghoon-maker/pb2-plugins.git
```

**예상 결과**:
```
✅ Marketplace "pb2-marketplace" added successfully
📦 Available plugins: pb-product-generator (v0.2.0)
```

### Step 1.2: 플러그인 설치

```bash
/plugin install pb-product-generator@pb2-marketplace
```

**예상 결과**:
```
✅ Plugin "pb-product-generator" (v0.2.0) installed successfully
📁 Location: ~/.claude/plugins/pb-product-generator/
```

**설치 위치 확인**:
```bash
# macOS/Linux
ls -la ~/.claude/plugins/pb-product-generator/

# Windows
dir %USERPROFILE%\.claude\plugins\pb-product-generator\
```

---

## 🔧 Phase 2: 자동 세팅 (5분)

### Step 2.1: 플러그인 디렉토리로 이동

```bash
cd ~/.claude/plugins/pb-product-generator/
```

### Step 2.2: PRIVATE_SETUP.md 파일 준비

**⚠️ 중요**: 이 파일은 Git에 포함되어 있지 않습니다. 팀에서 Slack/이메일로 전달받은 **PRIVATE_SETUP.md**를 준비하세요.

**PRIVATE_SETUP.md 파일 위치**:
- 팀 Slack 채널: #pb-product-generator
- 또는 이메일로 전달받은 첨부 파일

**파일에 포함된 내용**:
- ✅ 서비스 어카운트 JSON (Google Sheets 접근 인증)
- ✅ Google Sheet ID 및 탭 이름
- ✅ 자동 세팅 상세 가이드

### Step 2.3: 서비스 어카운트 JSON 생성

PRIVATE_SETUP.md의 **Step 2.2** 섹션을 참고하여 서비스 어카운트 JSON을 생성하세요:

```bash
# PRIVATE_SETUP.md에서 서비스 어카운트 JSON 복사
mkdir -p credentials
cat > credentials/service-account.json << 'EOF'
{
  # PRIVATE_SETUP.md의 JSON 내용을 여기에 붙여넣기
}
EOF
```

**또는 수동으로 생성**:
1. `credentials/` 폴더 생성: `mkdir -p credentials`
2. 텍스트 에디터로 `credentials/service-account.json` 파일 생성
3. PRIVATE_SETUP.md에서 JSON 내용 복사/붙여넣기

### Step 2.4: 자동 세팅 스크립트 실행

```bash
bash setup.sh
```

**스크립트가 자동으로 처리하는 작업**:
1. ✅ `credentials/` 폴더 확인/생성
2. ✅ `.env` 파일 자동 생성 (Sheet ID, 탭 이름 하드코딩)
3. ✅ Python 의존성 자동 설치 (`requirements.txt`)
4. ✅ 스크립트 실행 권한 설정

**예상 출력**:
```
🔍 Step 1: Environment Check
✅ credentials/ directory exists
✅ Service Account file found

🔧 Step 2: Environment Configuration
✅ .env file created

📦 Step 3: Python Dependencies
✅ Installing dependencies...
✅ All dependencies installed successfully

✅ Setup Complete! Ready to use.

You can now use:
  /generate VD25FPT003
  /batch-generate VD25FPT003 VD25FPT005
  /start-server
```

---

## 🎯 Phase 3: 기능 테스트 (3분)

### Step 3.1: 단일 제품 생성 테스트

Claude Code로 돌아와서 다음 명령어를 실행하세요:

```bash
/generate VD25FPT003
```

**예상 결과**:
```
✅ Successfully loaded 1 products
✅ Generated: output/20251018/editable/VD25FPT003_editable_v4.html (70 MB)

🎨 Features:
- Image crop/zoom editor (Pan X/Y: -50~+50, Zoom: 100~500%)
- Text editing (contenteditable - 모든 텍스트 편집 가능)
- Page zoom (30-100%, 기본 60%)
- HTML/JPG download (Export 기능)
```

### Step 3.2: 결과물 확인

```bash
# 생성된 파일 확인
ls -lh ~/.claude/plugins/pb-product-generator/output/*/editable/*.html

# 브라우저에서 열기 (macOS)
open ~/.claude/plugins/pb-product-generator/output/20251018/editable/VD25FPT003_editable_v4.html

# 브라우저에서 열기 (Linux)
xdg-open ~/.claude/plugins/pb-product-generator/output/20251018/editable/VD25FPT003_editable_v4.html

# 브라우저에서 열기 (Windows)
start %USERPROFILE%\.claude\plugins\pb-product-generator\output\20251018\editable\VD25FPT003_editable_v4.html
```

### Step 3.3: Flask 편집 서버 테스트 (선택적)

```bash
/start-server
```

**예상 결과**:
```
🚀 Flask server starting on port 5001...
✅ Server running at http://localhost:5001
🌐 Opening browser...
```

**브라우저 자동 실행**: http://localhost:5001
- 생성된 모든 Editable HTML 파일 목록 표시
- 이미지 편집 및 HTML/JPG 익스포트 기능 사용

---

## 🎨 사용 가능한 커맨드

| 커맨드 | 설명 | 예시 |
|--------|------|------|
| `/generate` | 단일 제품 HTML 생성 | `/generate VD25FPT003` |
| `/batch-generate` | 여러 제품 배치 생성 | `/batch-generate VD25FPT003 VD25FPT005 VD25FCA004` |
| `/start-server` | Flask 편집 서버 실행 | `/start-server` |

### 에이전트 사용

```bash
# Product Builder 에이전트에게 작업 요청
@agent-product-builder "VD25FPT003 제품 페이지 생성해줘"
```

**에이전트 자동 작업**:
1. Google Sheets 데이터 로드
2. 이미지 다운로드 및 Base64 인코딩
3. Editable HTML V4 생성
4. 결과 검증 및 후속 조치 안내

---

## 🔧 트러블슈팅

### ❌ "Service Account file NOT found"

**원인**: `credentials/service-account.json` 파일이 없음

**해결**:
```bash
cd ~/.claude/plugins/pb-product-generator/
ls credentials/service-account.json  # 파일 존재 확인

# 없으면 Phase 2 Step 2.3 다시 실행
```

### ❌ "ModuleNotFoundError: No module named 'google'"

**원인**: Python 의존성 미설치

**해결**:
```bash
cd ~/.claude/plugins/pb-product-generator/
pip3 install -r requirements.txt
```

### ❌ "HttpError 403: Forbidden"

**원인**: Service Account가 Google Sheets에 공유되지 않음

**해결**:
1. Google Sheets 열기: https://docs.google.com/spreadsheets/d/1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk/edit
2. 공유 버튼 클릭
3. PRIVATE_SETUP.md에 명시된 Service Account 이메일 추가
4. 권한: **뷰어** 선택
5. 보내기 클릭

### ❌ "Address already in use (Port 5001)"

**원인**: Flask 서버가 이미 실행 중

**해결**:
```bash
# macOS/Linux
lsof -ti:5001 | xargs kill -9

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### ❌ "PRIVATE_SETUP.md 파일을 못 찾겠어요"

**원인**: 팀에서 전달받은 프라이빗 가이드 파일이 없음

**해결**:
- **팀 슬랙**: #pb-product-generator 채널에서 요청
- **이메일**: pb-team@company.com으로 문의
- **담당자**: 프로젝트 관리자에게 직접 연락

---

## 📊 생성된 파일 구조

```
~/.claude/plugins/pb-product-generator/
├── credentials/
│   └── service-account.json    # ✅ 서비스 어카운트 인증 (Git 제외)
├── output/
│   └── 20251018/
│       ├── editable/
│       │   └── VD25FPT003_editable_v4.html  # ✅ 생성 결과 (70 MB)
│       └── export/
│           ├── VD25FPT003_export.html
│           └── VD25FPT003_export.jpg
├── .env                        # ✅ 환경 변수 (자동 생성)
├── scripts/
│   ├── generate_editable_html.py  # 원본 스크립트 (2116 lines)
│   ├── generate_batch.py          # 원본 배치 스크립트 (311 lines)
│   └── server.py                  # 원본 Flask 서버 (13K)
├── src/                        # 원본 전체 Python 모듈
├── templates/                  # 원본 전체 Jinja2 템플릿
├── setup.sh                    # 자동 세팅 스크립트
└── README.md                   # 플러그인 README
```

---

## 📖 추가 문서

- **플러그인 상세 가이드**: `~/.claude/plugins/pb-product-generator/README.md`
- **온보딩 가이드**: `~/.claude/plugins/pb-product-generator/ONBOARDING.md`
- **커맨드 문서**:
  - `commands/generate.md` - 단일 제품 생성
  - `commands/batch.md` - 배치 생성
  - `commands/server.md` - Flask 서버
- **에이전트 문서**: `agents/product-builder.md`

---

## 📞 지원 및 문의

### 팀 지원
- **슬랙**: #pb-product-generator
- **이메일**: pb-team@company.com

### 문제 보고 절차
1. 이 가이드 및 README.md 참고
2. 환경 변수 설정 확인 (`.env` 파일)
3. Google Sheets 권한 검증
4. 트러블슈팅 섹션 확인
5. 팀 슬랙 채널에 문의

---

## 🎉 다음 단계

### 1. 추가 제품 생성
```bash
/generate VD25FPT005
/generate VD25FCA004
```

### 2. 배치 생성
```bash
/batch-generate VD25FPT003 VD25FPT005 VD25FCA004
```

### 3. Flask 서버로 편집
```bash
/start-server
# http://localhost:5001에서 이미지 편집 및 익스포트
```

### 4. 팀 워크플로우 통합
- CI/CD 파이프라인에 통합
- 자동화된 제품 페이지 생성 워크플로우 구축
- 디자인 시스템과 연동

---

## 🔐 보안 주의사항

**⚠️ 절대 Git에 커밋하지 마세요**:
- ❌ `PRIVATE_SETUP.md` (서비스 어카운트 JSON 포함)
- ❌ `credentials/service-account.json`
- ❌ `.env` 파일

이 파일들은 `.gitignore`에 자동으로 제외되어 있습니다.

---

**Version**: 0.2.0
**Last Updated**: 2025-10-18
**Repository**: https://github.com/younghoon-maker/pb2-plugins

**Happy Generating! 🎨**
