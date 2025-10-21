# 팀원 온보딩 가이드

**PB Product Generator Claude Code 플러그인 설치 및 사용법**

---

## 📋 사전 준비물

설치 전 다음 항목을 준비해 주세요:

- [ ] **Claude Code** 설치됨 (VS Code Extension)
- [ ] **Python 3.11+** 설치됨
- [ ] **Google Service Account JSON** 파일 (팀 관리자에게 요청)
- [ ] **Google Sheets ID** (팀 관리자에게 요청)

---

## 🚀 설치 단계 (10분)

### Step 1: Claude Code 실행

VS Code에서 Claude Code 확장 실행:
```bash
Cmd + Shift + P (Mac) 또는 Ctrl + Shift + P (Windows)
→ "Claude Code: Start" 선택
```

### Step 2: 플러그인 마켓플레이스 추가

Claude Code 채팅 창에서:
```bash
/plugin marketplace add /Volumes/SharedDrive/pb-marketplace
```

또는 로컬 경로:
```bash
/plugin marketplace add ~/team/pb-marketplace
```

### Step 3: 플러그인 설치

```bash
/plugin install pb-product-generator@pb-marketplace
```

설치 확인:
```bash
/help
```

다음 커맨드들이 표시되면 성공:
- `/generate` - 단일 제품 생성
- `/batch-generate` - 배치 생성
- `/start-server` - 편집 서버 실행

### Step 4: Google Sheets 인증 설정

1. **credentials 폴더 생성**:
   ```bash
   mkdir -p credentials
   ```

2. **Service Account JSON 복사**:
   ```bash
   # 팀 관리자에게 받은 파일 복사
   cp /path/to/service-account.json credentials/
   ```

3. **.env 파일 생성**:
   ```bash
   cp .env.example .env
   ```

4. **.env 파일 편집**:
   ```bash
   GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
   GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
   FLASK_PORT=5001
   ```

### Step 5: Python 의존성 설치

```bash
pip3 install -r pb-product-generator-plugin/requirements.txt
```

---

## ✅ 설치 확인

다음 명령으로 정상 작동 확인:

```bash
/generate VD25FTS002
```

**성공 메시지**:
```
✅ Successfully loaded 1 products
✅ Generated: output/20251017/editable/VD25FTS002_editable_v4.html (51.4 MB)
```

---

## 📖 일상 사용법

### 1. 단일 제품 생성

```bash
/generate {제품코드}
```

**예시**:
```bash
/generate VD25FTS002
```

### 2. 여러 제품 한 번에 생성

```bash
/batch-generate {코드1} {코드2} {코드3}
```

**예시**:
```bash
/batch-generate VD25FTS002 VD25FPT003 VD25FCA004
```

### 3. 편집 서버 실행

```bash
/start-server
```

브라우저가 자동으로 열리면서 `http://localhost:5001`로 접속됩니다.

**편집 기능**:
- 이미지 crop/zoom 조정
- 텍스트 직접 수정
- 페이지 줌 조절 (30-100%)
- HTML 또는 JPG로 다운로드

### 4. 에이전트 사용 (대화형)

```bash
@agent-product-builder "VD25FTS002 생성하고 결과 알려줘"
```

에이전트가 자동으로:
1. 제품 데이터 로드
2. HTML 생성
3. 결과 보고 및 다음 단계 안내

---

## 🔧 자주 발생하는 문제 해결

### 문제 1: Service Account 파일 없음

**증상**:
```
❌ Service Account file not found
```

**해결**:
1. `credentials/` 폴더에 JSON 파일 있는지 확인
2. `.env` 파일의 경로가 정확한지 확인
3. 팀 관리자에게 파일 재요청

### 문제 2: API 권한 에러

**증상**:
```
❌ Authentication failed: 403 Forbidden
```

**해결**:
1. Google Sheets 스프레드시트 열기
2. "공유" 버튼 클릭
3. Service Account 이메일 추가 (Viewer 권한)
   - 이메일: `service-account.json` 파일 안의 `client_email` 값

### 문제 3: Port 충돌

**증상**:
```
Address already in use: 5001
```

**해결**:
```bash
# 기존 프로세스 종료
lsof -ti:5001 | xargs kill -9

# 또는 .env에서 포트 변경
FLASK_PORT=5002
```

### 문제 4: Python 모듈 없음

**증상**:
```
ModuleNotFoundError: No module named 'pydantic'
```

**해결**:
```bash
# 의존성 재설치
pip3 install -r pb-product-generator-plugin/requirements.txt
```

---

## 📁 출력 폴더 구조

생성된 파일은 다음 위치에 저장됩니다:

```
output/
└── {YYYYMMDD}/              # 예: 20251017
    ├── editable/
    │   └── {제품코드}_editable_v4.html
    └── export/
        ├── {제품코드}_export.html
        └── {제품코드}_export.jpg
```

**예시**:
```
output/
└── 20251017/
    ├── editable/
    │   ├── VD25FTS002_editable_v4.html (51.4 MB)
    │   └── VD25FPT003_editable_v4.html (73.2 MB)
    └── export/
        ├── VD25FTS002_export.html
        └── VD25FTS002_export.jpg
```

---

## 🎓 추가 학습 자료

- **플러그인 README**: `pb-product-generator-plugin/README.md`
- **커맨드 문서**: `pb-product-generator-plugin/commands/`
- **에이전트 가이드**: `pb-product-generator-plugin/agents/product-builder.md`

---

## 💬 지원

질문이나 문제가 있으면:

1. **이 문서 먼저 확인**: 대부분의 문제 해결 방법 포함
2. **팀 슬랙 채널**: `#pb-product-generator`
3. **팀 관리자 연락**: Google Sheets 권한 또는 인증 파일 문제

---

**Happy Generating! 🎨**

팀원 여러분의 빠른 온보딩을 응원합니다.
