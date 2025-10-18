# PB Product Generator - 완전 초보자 가이드

> **Google Sheets 292컬럼 기반 제품 상세 페이지 생성기**
>
> Editable HTML V4 with Image Editor & Flask Server

**버전**: 0.2.2
**최종 업데이트**: 2025-10-18
**난이도**: ⭐ 초급 (코딩 경험 불필요)

---

## 📋 목차

1. [이 플러그인이 하는 일](#-이-플러그인이-하는-일)
2. [사전 준비물](#-사전-준비물)
3. [단계별 설치 가이드](#-단계별-설치-가이드)
4. [Google Cloud 설정 (처음 하는 분을 위한 상세 가이드)](#-google-cloud-설정-처음-하는-분을-위한-상세-가이드)
5. [사용 방법](#-사용-방법)
6. [문제 해결](#-문제-해결)
7. [FAQ (자주 묻는 질문)](#-faq-자주-묻는-질문)

---

## 🎯 이 플러그인이 하는 일

### 간단 설명

Google Sheets에 292개 컬럼으로 정리된 제품 데이터를 읽어서, **편집 가능한 HTML 상세 페이지**를 자동으로 만들어줍니다.

### 예시

**입력**: Google Sheets의 제품 코드 `VD25FPT003`

**출력**: `VD25FPT003_editable_v4.html` (73MB)
- 이미지 자르기/확대 가능
- 텍스트 직접 수정 가능
- HTML/JPG로 다운로드 가능

### 어떤 분들이 사용하나요?

- 📦 **이커머스 운영자**: 제품 상세 페이지 빠르게 생성
- 🎨 **디자이너**: Figma 디자인 기반 HTML 자동 생성
- 📊 **데이터 관리자**: Google Sheets로 대량 제품 관리

---

## 🛠️ 사전 준비물

### 필수 소프트웨어

#### 1. Claude Code 설치

**다운로드**: https://claude.ai/download

**확인 방법**:
```bash
# 터미널에서 실행
claude --version
```

**예상 출력**:
```
Claude Code v1.x.x
```

#### 2. Python 3.11 이상 설치

**macOS**:
```bash
# Homebrew로 설치
brew install python@3.11
```

**Windows**:
1. https://www.python.org/downloads/ 접속
2. "Download Python 3.11.x" 클릭
3. 설치 시 "Add Python to PATH" 체크 필수

**확인 방법**:
```bash
python3 --version
```

**예상 출력**:
```
Python 3.11.x
```

#### 3. pip (Python 패키지 관리자)

Python 설치 시 자동으로 설치됩니다.

**확인 방법**:
```bash
pip3 --version
```

**예상 출력**:
```
pip 23.x.x from /usr/local/lib/python3.11/site-packages/pip (python 3.11)
```

---

### 필수 계정

#### 1. Google Cloud Console 계정

**무료 평가판**: 300달러 크레딧 제공 (90일)

**가입 방법**:
1. https://console.cloud.google.com/ 접속
2. Gmail 계정으로 로그인
3. "무료로 시작하기" 클릭
4. 신용카드 등록 (무료 평가판 종료 후 자동 과금 없음)

#### 2. Google Sheets 접근 권한

**제품 데이터 시트**:
- 292개 컬럼 구조
- 제품 코드가 포함된 시트

---

## 📥 단계별 설치 가이드

### Step 1: Claude Code 실행

**macOS/Linux**:
```bash
claude
```

**Windows**:
```cmd
claude
```

**화면 예시**:
```
Welcome to Claude Code!
>
```

---

### Step 2: 마켓플레이스 추가

**명령어 입력**:
```bash
/plugin marketplace add younghoon-maker/pb2-plugins
```

**설명**:
- `/plugin marketplace add`: 새로운 플러그인 저장소를 추가하는 명령어
- `younghoon-maker/pb2-plugins`: GitHub 저장소 주소

**예상 출력**:
```
✅ Marketplace added: pb2-plugins
📁 Repository: https://github.com/younghoon-maker/pb2-plugins
```

**만약 에러가 발생하면**:
```
❌ Error: Repository not found
```
→ 인터넷 연결 확인 또는 GitHub 저장소 주소 확인

---

### Step 3: 플러그인 설치

**명령어 입력**:
```bash
/plugin install pb-product-generator@pb2-plugins
```

**설명**:
- `/plugin install`: 플러그인을 설치하는 명령어
- `pb-product-generator`: 플러그인 이름
- `@pb2-plugins`: 어느 마켓플레이스에서 설치할지 지정

**예상 출력**:
```
📦 Installing pb-product-generator v0.2.2...
✅ Plugin installed successfully!

📁 Location:
   ~/.claude/plugins/marketplaces/pb2-marketplace/pb-product-generator-plugin/

📚 Available commands:
   /pb-product-generator:generate
   /pb-product-generator:batch
   /pb-product-generator:server
   /pb-product-generator:setup-from-private
```

**설치 확인**:
```bash
/plugin list
```

**예상 출력**:
```
Installed plugins:
  - pb-product-generator v0.2.2 (pb2-plugins)
```

---

### Step 4: 작업 폴더 생성 및 이동

**새 프로젝트 폴더 만들기**:

**macOS/Linux**:
```bash
# 1. 홈 디렉토리로 이동
cd ~

# 2. 프로젝트 폴더 생성
mkdir my-product-pages

# 3. 폴더로 이동
cd my-product-pages
```

**Windows**:
```cmd
# 1. 문서 폴더로 이동
cd %USERPROFILE%\Documents

# 2. 프로젝트 폴더 생성
mkdir my-product-pages

# 3. 폴더로 이동
cd my-product-pages
```

**현재 위치 확인**:
```bash
pwd
```

**예상 출력**:
```
/Users/yourname/my-product-pages
```

---

## 🔐 Google Cloud 설정 (처음 하는 분을 위한 상세 가이드)

### 왜 필요한가요?

Google Sheets API를 사용하려면 **Service Account**라는 인증 키가 필요합니다. 이것은 마치 "로봇 계정"처럼, 우리 프로그램이 Google Sheets에 접근할 수 있게 해주는 열쇠입니다.

---

### Step 1: Google Cloud Console 접속

1. 브라우저에서 https://console.cloud.google.com/ 접속
2. Gmail 계정으로 로그인

---

### Step 2: 새 프로젝트 만들기

**화면 상단 프로젝트 선택 드롭다운 클릭**:

![프로젝트 선택](https://via.placeholder.com/600x100/4285F4/FFFFFF?text=Select+a+project)

1. **"새 프로젝트"** 클릭
2. **프로젝트 이름** 입력: `my-product-generator` (원하는 이름)
3. **조직**: 없음 (개인 계정)
4. **만들기** 클릭

**대기 시간**: 약 10-30초

**완료 확인**:
```
✅ 프로젝트 'my-product-generator'가 생성되었습니다
```

---

### Step 3: Google Sheets API 활성화

1. **왼쪽 메뉴 → API 및 서비스 → 라이브러리** 클릭

![API 라이브러리](https://via.placeholder.com/600x100/34A853/FFFFFF?text=API+Library)

2. 검색창에 **"Google Sheets API"** 입력

3. **Google Sheets API** 클릭

4. **사용 설정** 버튼 클릭 (파란색 버튼)

**완료 확인**:
```
✅ Google Sheets API가 활성화되었습니다
```

---

### Step 4: Service Account 만들기

1. **왼쪽 메뉴 → API 및 서비스 → 사용자 인증 정보** 클릭

![사용자 인증 정보](https://via.placeholder.com/600x100/FBBC04/FFFFFF?text=Credentials)

2. **사용자 인증 정보 만들기 → 서비스 계정** 클릭

3. **서비스 계정 세부정보** 입력:
   - **서비스 계정 이름**: `product-generator-bot`
   - **서비스 계정 ID**: 자동 생성됨 (예: `product-generator-bot@my-project.iam.gserviceaccount.com`)
   - **서비스 계정 설명**: `제품 페이지 생성을 위한 봇`

4. **만들기 및 계속** 클릭

5. **이 서비스 계정에 프로젝트에 대한 액세스 권한 부여(선택사항)** → **건너뛰기**

6. **완료** 클릭

---

### Step 5: Service Account JSON 키 다운로드

1. **생성된 Service Account** 클릭 (예: `product-generator-bot@my-project.iam.gserviceaccount.com`)

2. **키** 탭 클릭

3. **키 추가 → 새 키 만들기** 클릭

4. **키 유형**: JSON 선택

5. **만들기** 클릭

**자동 다운로드**:
```
my-project-xxxxxxxxxxxx.json
```

**⚠️ 중요**:
- 이 파일은 **절대 공개하면 안 됩니다**
- GitHub에 업로드 금지
- 이메일로 전송 금지
- 안전한 폴더에 보관

**다운로드 위치 확인**:
- **macOS**: `~/Downloads/my-project-xxxxxxxxxxxx.json`
- **Windows**: `C:\Users\YourName\Downloads\my-project-xxxxxxxxxxxx.json`

---

### Step 6: Google Sheets에 Service Account 공유

**중요**: Service Account가 Google Sheets를 읽으려면 **공유 권한**이 필요합니다.

1. **Google Sheets 문서 열기** (제품 데이터가 있는 시트)

2. **공유 버튼** 클릭 (우측 상단)

![공유 버튼](https://via.placeholder.com/100x40/34A853/FFFFFF?text=Share)

3. **사용자 및 그룹 추가** 입력란에 **Service Account 이메일** 복사-붙여넣기:
   ```
   product-generator-bot@my-project.iam.gserviceaccount.com
   ```

   **이메일 확인 방법**:
   - Google Cloud Console → 서비스 계정 목록
   - 또는 다운로드한 JSON 파일 열기 → `client_email` 값 확인

4. **권한 선택**: **뷰어** (읽기 전용)

5. **보내기** 클릭

**완료 확인**:
```
✅ product-generator-bot@my-project.iam.gserviceaccount.com님에게 공유되었습니다
```

---

### Step 7: Google Sheets ID 확인

**Google Sheets URL 예시**:
```
https://docs.google.com/spreadsheets/d/1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk/edit
                                        ↑ 이 부분이 Sheet ID
```

**Sheet ID 복사**:
```
1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
```

**Sheet ID를 어디에 쓰나요?**
→ 다음 단계의 PRIVATE_SETUP.md 파일에 입력합니다.

---

## ⚙️ 자동 설정 (PRIVATE_SETUP.md 방식)

### Step 1: 템플릿 파일 복사

**Claude Code에서 실행** (프로젝트 폴더에서):

```bash
cp ~/.claude/plugins/marketplaces/pb2-marketplace/pb-product-generator-plugin/PRIVATE_SETUP.md.template ./PRIVATE_SETUP.md
```

**설명**:
- `cp`: 파일 복사 명령어
- `~/.claude/plugins/.../PRIVATE_SETUP.md.template`: 원본 템플릿 위치
- `./PRIVATE_SETUP.md`: 현재 폴더에 복사

**복사 확인**:
```bash
ls -la PRIVATE_SETUP.md
```

**예상 출력**:
```
-rw-r--r--  1 you  staff  12345 Oct 18 10:00 PRIVATE_SETUP.md
```

---

### Step 2: PRIVATE_SETUP.md 파일 열기

**텍스트 편집기로 열기**:

**macOS**:
```bash
open -a TextEdit PRIVATE_SETUP.md
```

**Windows**:
```cmd
notepad PRIVATE_SETUP.md
```

**또는 VS Code 사용**:
```bash
code PRIVATE_SETUP.md
```

---

### Step 3: Service Account JSON 내용 복사

1. **다운로드한 JSON 파일 열기**:
   ```bash
   # macOS
   open ~/Downloads/my-project-xxxxxxxxxxxx.json

   # Windows
   notepad %USERPROFILE%\Downloads\my-project-xxxxxxxxxxxx.json
   ```

2. **전체 내용 복사** (Ctrl+A, Ctrl+C)

**JSON 예시**:
```json
{
  "type": "service_account",
  "project_id": "my-project-123456",
  "private_key_id": "abc123def456...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBg...\n-----END PRIVATE KEY-----\n",
  "client_email": "product-generator-bot@my-project.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...",
  "universe_domain": "googleapis.com"
}
```

---

### Step 4: PRIVATE_SETUP.md 편집

**PRIVATE_SETUP.md 파일에서 찾기**:

```yaml
```json
{
  "type": "service_account",
  "project_id": "YOUR_PROJECT_ID",           # ← 여기부터
  "private_key_id": "YOUR_PRIVATE_KEY_ID",
  ...
}
```
```

**교체 작업**:

1. **기존 JSON 블록 전체 삭제** (플레이스홀더 포함)

2. **복사한 실제 JSON 붙여넣기**

3. **환경 변수 섹션 수정**:
   ```
   GOOGLE_SHEET_ID=YOUR_GOOGLE_SHEET_ID_HERE
   ```

   **변경 후**:
   ```
   GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
   ```

4. **시트 탭 이름 확인**:
   ```
   SHEET_TAB_NAME=YOUR_TAB_NAME_HERE
   ```

   **변경 후** (시트 하단 탭 이름):
   ```
   SHEET_TAB_NAME=new_raw
   ```

**저장**: Ctrl+S (Windows) / Cmd+S (macOS)

---

### Step 5: 자동 설정 실행

**Claude Code에서 실행**:

```bash
/pb-product-generator:setup-from-private
```

**무엇을 하나요?**:
1. ✅ `PRIVATE_SETUP.md` 파일 읽기
2. ✅ `credentials/` 폴더 생성
3. ✅ `credentials/service-account.json` 자동 생성
4. ✅ `.env` 파일 자동 생성
5. ✅ Python 패키지 자동 설치 (gspread, Pillow, jinja2, flask 등)
6. ✅ `output/` 폴더 생성

**예상 출력**:
```
🚀 PB Product Generator - Automatic Setup
==================================================

✅ Found PRIVATE_SETUP.md

📋 Parsing PRIVATE_SETUP.md...
   ✓ Service Account: product-generator-bot@my-project.iam.gserviceaccount.com
   ✓ Sheet ID: 1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
   ✓ Tab Name: new_raw

📁 Creating directories...
   ✓ credentials/
   ✓ output/

📄 Writing files...
   ✓ credentials/service-account.json
   ✓ .env

📦 Installing Python dependencies...
   Installing gspread... ✓
   Installing oauth2client... ✓
   Installing Pillow... ✓
   Installing jinja2... ✓
   Installing flask... ✓

✅ Setup completed successfully!

📁 Created files:
   - credentials/service-account.json
   - .env
   - output/

🎯 Next step:
   /pb-product-generator:generate VD25FPT003
```

**소요 시간**: 약 1-2분 (네트워크 속도에 따라)

---

### Step 6: 설정 확인

**파일 구조 확인**:
```bash
ls -la
```

**예상 출력**:
```
drwxr-xr-x   credentials/
-rw-r--r--   .env
-rw-r--r--   PRIVATE_SETUP.md
drwxr-xr-x   output/
```

**credentials/service-account.json 확인**:
```bash
cat credentials/service-account.json
```

**예상 출력**: JSON 형식의 Service Account 정보

**.env 파일 확인**:
```bash
cat .env
```

**예상 출력**:
```
GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
SHEET_TAB_NAME=new_raw
FLASK_PORT=5001
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
```

---

## 🎨 사용 방법

### 1. 단일 제품 HTML 생성

**시나리오**: `VD25FPT003` 제품의 상세 페이지를 만들고 싶어요.

**명령어**:
```bash
/pb-product-generator:generate VD25FPT003
```

**무슨 일이 일어나나요?**:

1. **Google Sheets 데이터 로드**
   ```
   📊 Loading product data from Google Sheets...
   ✅ Successfully loaded 1 products
   ```

2. **이미지 다운로드**
   ```
   🖼️  이미지 다운로드 및 Base64 변환 중...
     - 메인 이미지: https://drive.google.com/file/d/xxx (3.2 MB)
     - 갤러리 이미지 1/5 (1.8 MB)
     - 갤러리 이미지 2/5 (2.1 MB)
     - 상세 이미지 1/3 (1.5 MB)
   ```

3. **HTML 생성**
   ```
   🎨 Generating HTML with Figma template...
   ✅ Generated: output/20251018/editable/VD25FPT003_editable_v4.html (73.2 MB)
   ```

4. **완료**
   ```
   🎨 Features:
   - Image crop/zoom editor (Canvas-based)
   - Text editing (contenteditable)
   - Page zoom (30-100%)
   - HTML/JPG download

   📁 File location:
      output/20251018/editable/VD25FPT003_editable_v4.html
   ```

**소요 시간**: 약 15-30초 (이미지 개수에 따라)

---

### 2. 생성된 HTML 파일 열기

**macOS**:
```bash
open output/20251018/editable/VD25FPT003_editable_v4.html
```

**Windows**:
```cmd
start output\20251018\editable\VD25FPT003_editable_v4.html
```

**브라우저에서 열림**:
- Chrome, Safari, Edge 등 모든 모던 브라우저 지원

---

### 3. HTML에서 편집하기

#### 이미지 편집

1. **이미지 위에 마우스 오버** → 편집 아이콘 표시

2. **편집 아이콘 클릭** → 편집 모드 진입

3. **슬라이더 조작**:
   - **Crop Left/Right**: 좌우 자르기
   - **Crop Top/Bottom**: 상하 자르기
   - **Zoom**: 확대/축소 (1.0 ~ 3.0배)

4. **확인** 버튼 클릭 → 변경 사항 적용

#### 텍스트 편집

1. **텍스트 영역 클릭** → 커서 깜빡임

2. **직접 입력** → 실시간 반영

3. **Enter** 키 → 줄바꿈

#### 페이지 줌

**화면 우측 하단 줌 컨트롤**:
- `-` 버튼: 축소
- `+` 버튼: 확대
- 범위: 30% ~ 100%

#### 다운로드

**화면 우측 상단 다운로드 버튼**:
- **HTML 다운로드**: 편집 내용 포함된 HTML
- **JPG 다운로드**: 이미지로 변환 (인쇄용)

---

### 4. 여러 제품 한 번에 생성 (배치)

**시나리오**: 3개 제품을 한 번에 만들고 싶어요.

**명령어**:
```bash
/pb-product-generator:batch VD25FPT003 VD25FPT005 VD25FCA004
```

**출력**:
```
🚀 Batch Generation Started
📋 Products: 3

[1/3] VD25FPT003
   📊 Loading data...
   🖼️  Downloading images...
   ✅ Generated (73.2 MB)

[2/3] VD25FPT005
   📊 Loading data...
   🖼️  Downloading images...
   ✅ Generated (68.5 MB)

[3/3] VD25FCA004
   📊 Loading data...
   🖼️  Downloading images...
   ✅ Generated (45.8 MB)

✅ Batch Complete: 3 succeeded, 0 failed
📁 Output: output/20251018/editable/
⏱️  Total time: 1m 23s
```

**소요 시간**: 제품당 약 15-30초

---

### 5. 시트 전체 자동 생성

**시나리오**: Google Sheets에 있는 모든 제품을 자동으로 생성하고 싶어요.

**명령어**:
```bash
/pb-product-generator:batch --all
```

**무슨 일이 일어나나요?**:

1. **시트 스캔**
   ```
   📋 Scanning Google Sheets...
   ```

2. **제품 코드 자동 탐지**
   ```
   ✅ Found 15 products:
      - Row 2: VD25FPT003
      - Row 3: VD25FPT005
      - Row 5: VD25FCA004
      ... (빈 행 자동 건너뛰기)
   ```

3. **순차 생성**
   ```
   [1/15] VD25FPT003 ✅ (73.2 MB)
   [2/15] VD25FPT005 ✅ (68.5 MB)
   ...
   [15/15] VD25XXX015 ✅ (55.1 MB)
   ```

4. **완료**
   ```
   ✅ Batch Complete: 15 succeeded, 0 failed
   📁 Output: output/20251018/editable/
   ⏱️  Total time: 3m 45s
   ```

**소요 시간**: 제품 15개 기준 약 3-5분

---

### 6. Flask 서버로 실시간 편집

**시나리오**: 브라우저에서 편집 후 자동 저장하고 싶어요.

**명령어**:
```bash
/pb-product-generator:server
```

**서버 시작**:
```
🚀 Flask Server Starting...
📁 Output directory: /Users/you/my-product-pages/output

 * Running on http://127.0.0.1:5001
 * Press CTRL+C to quit

🌐 Open in browser:
   http://localhost:5001
```

**브라우저 접속**:
1. 브라우저에서 `http://localhost:5001` 접속
2. 생성된 HTML 파일 목록 표시
3. 클릭하여 편집
4. 편집 내용 자동 저장

**서버 중단**:
```
CTRL+C
```

---

## 🔧 문제 해결

### ❌ "Service Account 파일을 찾을 수 없습니다"

**전체 에러 메시지**:
```
❌ SheetsLoader 초기화 실패: Service Account 파일을 찾을 수 없습니다
   경로: /Users/you/my-product-pages/credentials/service-account.json
```

**원인**:
- `credentials/service-account.json` 파일이 없음
- 파일 경로가 잘못됨

**해결 방법 1: 자동 설정 재실행**
```bash
/pb-product-generator:setup-from-private
```

**해결 방법 2: 수동 확인**
```bash
# 파일 존재 확인
ls -la credentials/service-account.json

# 없으면 다운로드한 JSON 파일 복사
cp ~/Downloads/my-project-xxxxxxxxxxxx.json credentials/service-account.json
```

**해결 방법 3: 파일 내용 확인**
```bash
# JSON 형식이 올바른지 확인
cat credentials/service-account.json
```

**올바른 JSON 형식**:
```json
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  ...
}
```

---

### ❌ "HttpError 403: Forbidden"

**전체 에러 메시지**:
```
❌ Google Sheets API 에러: 403 Forbidden
   The caller does not have permission
```

**원인**:
- Service Account가 Google Sheets에 공유되지 않음

**해결 방법**:

1. **Google Sheets 열기**

2. **공유 버튼 클릭** (우측 상단)

3. **Service Account 이메일 확인**:
   ```bash
   cat credentials/service-account.json | grep client_email
   ```

   **출력 예시**:
   ```
   "client_email": "product-generator-bot@my-project.iam.gserviceaccount.com"
   ```

4. **이메일 복사 후 공유 대화상자에 붙여넣기**

5. **권한 선택**: **뷰어** (읽기 전용)

6. **보내기** 클릭

7. **재시도**:
   ```bash
   /pb-product-generator:generate VD25FPT003
   ```

---

### ❌ "ModuleNotFoundError: No module named 'gspread'"

**전체 에러 메시지**:
```
ModuleNotFoundError: No module named 'gspread'
```

**원인**:
- Python 패키지가 설치되지 않음

**해결 방법 1: 자동 설치**
```bash
/pb-product-generator:setup-from-private
```

**해결 방법 2: 수동 설치**
```bash
pip3 install gspread oauth2client Pillow jinja2 flask
```

**설치 확인**:
```bash
pip3 list | grep gspread
```

**예상 출력**:
```
gspread                4.1.0
```

---

### ❌ "Product {code} not found in sheets"

**전체 에러 메시지**:
```
❌ Product VD25FPT003 not found in sheets
```

**원인**:
1. 제품 코드가 Google Sheets에 없음
2. 제품 코드 철자가 다름 (대소문자 구분)
3. 시트 탭 이름이 잘못됨

**해결 방법 1: Google Sheets 확인**
1. Google Sheets 열기
2. Ctrl+F (찾기)
3. 제품 코드 검색 (예: `VD25FPT003`)
4. 정확한 철자 확인

**해결 방법 2: 시트 탭 이름 확인**
```bash
cat .env | grep SHEET_TAB_NAME
```

**출력 예시**:
```
SHEET_TAB_NAME=new_raw
```

**시트 하단 탭 이름과 일치하는지 확인**

**해결 방법 3: .env 파일 수정**
```bash
# 텍스트 편집기로 열기
nano .env

# SHEET_TAB_NAME 수정
SHEET_TAB_NAME=올바른_탭_이름

# 저장: Ctrl+X, Y, Enter
```

---

### ❌ "Command not found: /pb-product-generator:generate"

**전체 에러 메시지**:
```
❌ Unknown command: /pb-product-generator:generate
```

**원인**:
- 플러그인이 설치되지 않음
- Claude Code 세션이 오래됨

**해결 방법 1: 플러그인 설치 확인**
```bash
/plugin list
```

**예상 출력**:
```
Installed plugins:
  - pb-product-generator v0.2.2
```

**출력이 없으면**:
```bash
/plugin install pb-product-generator@pb2-plugins
```

**해결 방법 2: Claude Code 재시작**
```bash
# Claude Code 종료
exit

# 다시 실행
claude
```

**해결 방법 3: 플러그인 업데이트**
```bash
/plugin update pb-product-generator@pb2-plugins
```

---

### ⚠️ HTML 파일이 너무 커요 (50MB 이상)

**원인**:
- 이미지가 Base64로 인코딩되어 HTML에 포함됨
- 고해상도 이미지 사용

**정상입니다**:
- 평균 파일 크기: 50-80MB
- 이미지 개수에 따라 달라짐

**장점**:
- HTML 파일 하나로 모든 것 포함
- 별도 이미지 파일 불필요
- 이메일 첨부 가능

**단점**:
- 파일 크기 큼
- 로딩 시간 소요

**해결 방법** (파일 크기 줄이기):
→ 향후 버전에서 외부 이미지 링크 옵션 제공 예정

---

## ❓ FAQ (자주 묻는 질문)

### Q1: 플러그인 사용에 비용이 드나요?

**A**: 플러그인 자체는 무료입니다. 하지만:

- **Google Cloud**: 무료 평가판 (300달러 크레딧, 90일)
- **Google Sheets API**: 무료 (일일 할당량 내)
- **할당량**: 하루 100,000 읽기 요청 (충분함)

**비용 발생 조건**:
- 무료 평가판 종료 후 계속 사용 시
- 대량 API 요청 (할당량 초과 시)

**권장**:
- 개인/소규모 프로젝트: 무료 범위 내
- 대규모 프로젝트: Google Cloud 요금제 확인

---

### Q2: 한 번에 몇 개까지 생성할 수 있나요?

**A**: 제한 없음

**하지만**:
- **메모리**: 제품당 약 100MB 사용
- **시간**: 제품당 15-30초
- **권장**: 한 번에 50개 이하

**예시**:
- 10개 제품: 약 3분
- 50개 제품: 약 15분
- 100개 제품: 약 30분

---

### Q3: 오프라인에서도 사용할 수 있나요?

**A**: 부분적으로 가능

**온라인 필요**:
- Google Sheets 데이터 로드
- Google Drive 이미지 다운로드
- 플러그인 설치/업데이트

**오프라인 가능**:
- 생성된 HTML 파일 열기
- HTML 편집
- Flask 서버 실행 (로컬)

---

### Q4: 생성된 HTML을 쇼핑몰에 업로드할 수 있나요?

**A**: 가능하지만 주의 필요

**그대로 사용**:
- 정적 페이지로 업로드
- GitHub Pages, Netlify 등

**쇼핑몰 CMS**:
- HTML → 복사-붙여넣기
- 이미지는 별도 업로드 필요할 수 있음

**권장**:
- JPG 다운로드 후 이미지로 업로드
- 또는 HTML 소스 코드 수정

---

### Q5: 에러가 계속 발생해요. 어떻게 하나요?

**A**: 체크리스트 확인

**1단계: 기본 확인**
```bash
# Python 버전
python3 --version  # 3.11 이상

# pip 버전
pip3 --version

# Claude Code 버전
claude --version
```

**2단계: 플러그인 확인**
```bash
# 설치 확인
/plugin list

# 업데이트
/plugin update pb-product-generator@pb2-plugins
```

**3단계: 설정 파일 확인**
```bash
# credentials 확인
ls -la credentials/service-account.json

# .env 확인
cat .env
```

**4단계: 재설정**
```bash
# 완전 재설정
rm -rf credentials/ .env output/

# 자동 설정 재실행
/pb-product-generator:setup-from-private
```

**그래도 안 되면**:
- GitHub Issues: https://github.com/younghoon-maker/pb2-plugins/issues
- 에러 메시지 전체 복사-붙여넣기
- 환경 정보 포함 (OS, Python 버전 등)

---

### Q6: PRIVATE_SETUP.md를 Git에 올려도 되나요?

**A**: 절대 안 됩니다! 🚫

**이유**:
- Service Account JSON 포함
- Google Cloud 인증 키 노출
- 악의적 사용자가 Google Sheets 접근 가능

**자동 보호**:
- `.gitignore`에 자동 등록됨
- Git 커밋 시 제외됨

**확인 방법**:
```bash
cat .gitignore
```

**예상 출력**:
```
PRIVATE_SETUP.md
credentials/
.env
```

**만약 Git에 올렸다면**:
1. 즉시 Google Cloud Console에서 Service Account 키 삭제
2. 새 키 생성
3. Git 히스토리에서 완전 제거

---

### Q7: 다른 사람과 공유하려면 어떻게 하나요?

**A**: 두 가지 방법

**방법 1: 생성된 HTML만 공유**
- `output/` 폴더의 HTML 파일만 전달
- 안전함 (인증 정보 없음)

**방법 2: 프로젝트 전체 공유**
1. **제외 파일**:
   ```
   credentials/service-account.json   ← 절대 공유 금지
   PRIVATE_SETUP.md                   ← 절대 공유 금지
   .env                                ← 절대 공유 금지
   ```

2. **공유 가능 파일**:
   ```
   output/                             ← 생성된 HTML
   README.md                           ← 문서
   ```

3. **상대방 설정**:
   - 자신의 Google Cloud Service Account 생성
   - 자신의 PRIVATE_SETUP.md 작성
   - `/pb-product-generator:setup-from-private` 실행

---

### Q8: 업데이트는 어떻게 하나요?

**A**: 간단한 명령어 하나

```bash
/plugin update pb-product-generator@pb2-plugins
```

**업데이트 확인**:
```bash
/plugin list
```

**자동 알림**:
- Claude Code가 새 버전 자동 감지
- 업데이트 권장 메시지 표시

---

### Q9: 제품 데이터 구조는 어떻게 되나요?

**A**: Google Sheets 292개 컬럼

**주요 컬럼**:
1. **기본 정보** (1-20번)
   - 제품 코드
   - 제품명
   - 가격
   - 할인율

2. **이미지** (21-100번)
   - 메인 이미지 (Google Drive URL)
   - 갤러리 이미지 (최대 10개)
   - 상세 이미지 (최대 20개)

3. **색상** (101-120번)
   - 색상 코드 (HEX)
   - 색상 이름

4. **상세 정보** (121-200번)
   - 소재
   - 사이즈
   - 모델 핏
   - 사이즈 차트

5. **기타** (201-292번)
   - SEO 정보
   - 카테고리
   - 태그

**템플릿 다운로드**:
→ 향후 제공 예정

---

### Q10: Flask 서버가 자꾸 꺼져요.

**A**: 정상 동작입니다

**Flask 서버 특성**:
- 개발용 서버
- CTRL+C로 수동 종료
- 터미널 종료 시 자동 종료

**계속 실행하려면**:
- 터미널 창 유지
- 백그라운드 실행 (고급 사용자):
  ```bash
  nohup /pb-product-generator:server &
  ```

**프로덕션 배포**:
- Gunicorn, uWSGI 사용 (별도 설정 필요)
- 클라우드 호스팅 (Heroku, AWS 등)

---

## 🎓 다음 단계

### 초급 사용자

1. ✅ 설치 및 설정 완료
2. ✅ 첫 HTML 생성 성공
3. 🎯 **다음**: 여러 제품 배치 생성 시도

```bash
/pb-product-generator:batch VD25FPT003 VD25FPT005
```

---

### 중급 사용자

1. ✅ 배치 생성 숙달
2. 🎯 **다음**: Flask 서버로 실시간 편집

```bash
/pb-product-generator:server
```

---

### 고급 사용자

1. ✅ 모든 기능 숙달
2. 🎯 **다음**: 커스터마이징
   - Jinja2 템플릿 수정
   - CSS 스타일 변경
   - 이미지 처리 로직 수정

**커스터마이징 가이드**:
→ 향후 제공 예정

---

## 📞 지원 및 문의

### GitHub Issues

**버그 리포트**:
https://github.com/younghoon-maker/pb2-plugins/issues

**템플릿**:
```markdown
## 환경
- OS: macOS 14.0 / Windows 11
- Python: 3.11.5
- Claude Code: 1.2.3

## 문제
[에러 메시지 전체 복사]

## 재현 방법
1. /pb-product-generator:generate VD25FPT003
2. 에러 발생

## 기대 결과
HTML 파일 생성

## 실제 결과
Service Account 에러
```

---

### 커뮤니티

- **디스코드**: (준비 중)
- **슬랙**: (준비 중)

---

## 🎉 축하합니다!

이제 **PB Product Generator**를 사용할 준비가 완료되었습니다!

**첫 HTML 생성해보기**:
```bash
/pb-product-generator:generate VD25FPT003
```

**Happy Generating! 🚀**
