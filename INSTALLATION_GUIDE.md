# 📦 PB Product Generator - 설치 가이드

**Google Sheets 292컬럼 데이터 기반 제품 상세 페이지 생성기 v0.2.1**

> **⏱️ 총 소요 시간: 5분**
> - 마켓플레이스 추가 및 플러그인 설치 (1분)
> - Claude 재시작 (1분)
> - 자동 세팅 실행 (3분)

---

## 📋 사전 요구사항

- ✅ **Claude Code**: 최신 버전 설치
- ✅ **Python**: 3.11+ 설치 (`python3 --version` 확인)
- ✅ **Git**: Git 설치 (`git --version` 확인)
- ✅ **PRIVATE_SETUP.md**: 팀에서 전달받은 프라이빗 세팅 가이드

---

## 🚀 Installation Steps

### Step 1: 마켓플레이스 추가

Claude Code를 실행하고 다음 명령어를 입력하세요:

```bash
/plugin marketplace add younghoon-maker/pb2-plugins
```

**예상 결과**:
```
✅ Marketplace "pb2-plugins" added successfully
📦 Available plugins: pb-product-generator (v0.2.1)
```

### Step 2: 플러그인 설치

```bash
/plugin install pb-product-generator@pb2-plugins
```

**예상 결과**:
```
✅ Plugin "pb-product-generator" (v0.2.1) installed successfully
```

### Step 3: Claude 재시작

**⚠️ 중요**: 플러그인이 제대로 로드되려면 Claude를 재시작해야 합니다.

```bash
/quit
```

그리고 터미널에서 다시 시작:
```bash
claude
```

### Step 4: PRIVATE_SETUP.md 파일 복사

**⚠️ 중요**: 팀에서 전달받은 PRIVATE_SETUP.md 파일을 **Claude를 실행하는 프로젝트 폴더**에 복사하세요.

```bash
# 예시: Downloads에서 현재 프로젝트 폴더로 복사
cp ~/Downloads/PRIVATE_SETUP.md .
```

**PRIVATE_SETUP.md 위치**:
- 팀 Slack 채널: #pb-product-generator
- 또는 이메일로 전달받은 첨부 파일

**파일에 포함된 내용**:
- ✅ 서비스 어카운트 JSON (Google Sheets 접근 인증)
- ✅ Google Sheet ID 및 탭 이름
- ✅ 자동 세팅 가이드

### Step 5: 자동 세팅 실행

```bash
/pb-product-generator:setup-from-private
```

**자동으로 처리되는 작업**:
1. ✅ PRIVATE_SETUP.md 파일 읽기
2. ✅ Service Account JSON 추출
3. ✅ `credentials/` 폴더 생성
4. ✅ `service-account.json` 파일 생성
5. ✅ `.env` 파일 생성 (Sheet ID, 탭 이름 자동 설정)
6. ✅ Python 의존성 설치

**예상 출력**:
```
🚀 PB Product Generator - Automatic Setup
==================================================

✅ Found PRIVATE_SETUP.md
📋 Parsing PRIVATE_SETUP.md...
   ✓ Service Account: test-account-n8n@damoa-fb351.iam.gserviceaccount.com
   ✓ Sheet ID: 1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk

📁 Creating credentials directory...
🔐 Writing Service Account JSON...
⚙️  Writing .env file...
📦 Installing Python dependencies...

✅ Setup completed successfully!

You can now use:
  /pb-product-generator:generate VD25FPT003
  /pb-product-generator:batch VD25FPT003 VD25FPT005
  /pb-product-generator:server
```

### Step 6: Google Sheets 권한 설정

Google Sheets에 Service Account 이메일을 공유해야 합니다:

1. Google Sheets 열기: https://docs.google.com/spreadsheets/d/1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk/edit
2. 공유 버튼 클릭
3. Service Account 이메일 추가: `test-account-n8n@damoa-fb351.iam.gserviceaccount.com`
4. 권한: **뷰어** 선택
5. 보내기 클릭

### Step 7: 테스트 실행

```bash
/pb-product-generator:generate VD25FPT003
```

**예상 결과**:
```
✅ Successfully loaded 1 products
✅ Generated: output/20251019/editable/VD25FPT003_editable_v4.html (70 MB)
```

---

## 🎨 사용 가능한 커맨드

| 커맨드 | 설명 | 예시 |
|--------|------|------|
| `/pb-product-generator:generate` | 단일 제품 HTML 생성 | `/pb-product-generator:generate VD25FPT003` |
| `/pb-product-generator:batch` | 여러 제품 배치 생성 | `/pb-product-generator:batch VD25FPT003 VD25FPT005 VD25FCA004` |
| `/pb-product-generator:server` | Flask 편집 서버 실행 | `/pb-product-generator:server` |
| `/pb-product-generator:setup-from-private` | 자동 세팅 | `/pb-product-generator:setup-from-private` |

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
/pb-product-generator:generate VD25FPT005
/pb-product-generator:generate VD25FCA004
```

### 2. 배치 생성
```bash
/pb-product-generator:batch VD25FPT003 VD25FPT005 VD25FCA004
```

### 3. Flask 서버로 편집
```bash
/pb-product-generator:server
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

**Version**: 0.2.1
**Last Updated**: 2025-10-19
**Repository**: https://github.com/younghoon-maker/pb2-plugins

**Happy Generating! 🎨**
