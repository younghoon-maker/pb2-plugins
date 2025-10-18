---
description: PRIVATE_SETUP.md 파일로 자동 환경 설정
tools: [Bash]
---

# Setup from PRIVATE_SETUP.md

PRIVATE_SETUP.md 파일을 읽어서 자동으로 전체 환경을 설정합니다.

## 작업 프로세스

1. **PRIVATE_SETUP.md 읽기**: 현재 프로젝트 폴더의 PRIVATE_SETUP.md 파일 탐지
2. **Service Account 추출**: ```json 코드 블록에서 Service Account JSON 추출
3. **설정값 추출**: Google Sheets ID, Tab Name, Flask Port 추출
4. **파일 생성**: credentials/service-account.json, .env 자동 생성
5. **의존성 설치**: Python 패키지 설치
6. **검증**: 설정 완료 확인

## 사용법

**프로젝트 폴더에 PRIVATE_SETUP.md 파일이 있어야 합니다**:

```bash
/setup-from-private
```

## 출력

```
🚀 PB Product Generator - Automatic Setup
==================================================

✅ Found PRIVATE_SETUP.md: /path/to/PRIVATE_SETUP.md

📋 Parsing PRIVATE_SETUP.md...
   ✓ Service Account: test-account-n8n@damoa-fb351.iam.gserviceaccount.com
   ✓ Sheet ID: 1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
   ✓ Tab Name: new_raw
   ✓ Flask Port: 5001

📁 Creating credentials directory...
   ✓ /path/to/credentials

🔐 Writing Service Account JSON...
   ✓ /path/to/credentials/service-account.json

⚙️  Writing .env file...
   ✓ /path/to/.env

📦 Installing Python dependencies...
   ✓ Dependencies installed

✅ Output directory ready: /path/to/output

==================================================
✅ Setup completed successfully!

You can now use:
  /generate VD25FPT003
  /batch-generate VD25FPT003 VD25FPT005
  /start-server
```

## PRIVATE_SETUP.md 형식

**필수 요소**:

### 1. Service Account JSON (```json 코드 블록)
```markdown
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "your-service-account@project.iam.gserviceaccount.com",
  ...
}
```
```

### 2. Google Sheets ID
다음 형식 중 하나:
```markdown
GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
```
또는
```markdown
- **Sheet ID**: `1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk`
```

### 3. Tab Name (선택사항)
다음 형식 중 하나:
```markdown
SHEET_TAB_NAME=new_raw
```
또는
```markdown
- **Tab Name**: `new_raw`
```

**없으면 기본값 `new_raw` 사용**

### 4. Flask Port (선택사항)
```markdown
FLASK_PORT=5001
```

**없으면 기본값 `5001` 사용**

## 에러 처리

### ❌ PRIVATE_SETUP.md not found
**원인**: 현재 프로젝트 폴더에 PRIVATE_SETUP.md 파일이 없음

**해결**:
```bash
# PRIVATE_SETUP.md 파일이 프로젝트 폴더에 있는지 확인
ls PRIVATE_SETUP.md

# 없으면 사용자로부터 받은 PRIVATE_SETUP.md를 프로젝트 폴더에 복사
cp /path/to/PRIVATE_SETUP.md ./
```

### ❌ Service Account JSON not found
**원인**: PRIVATE_SETUP.md에 ```json 코드 블록이 없거나 형식이 잘못됨

**해결**:
- PRIVATE_SETUP.md 파일에 다음 형식으로 JSON 블록이 있는지 확인:
```markdown
```json
{
  "type": "service_account",
  ...
}
```
```

### ❌ Invalid JSON in Service Account block
**원인**: JSON 구문 오류

**해결**:
- JSON 유효성 검사: https://jsonlint.com/
- 쉼표, 중괄호, 따옴표 확인

### ❌ Missing required fields
**원인**: Service Account JSON에 필수 필드 누락

**필수 필드**:
- `type` (= "service_account")
- `project_id`
- `private_key`
- `client_email`

### ❌ Google Sheets ID not found
**원인**: PRIVATE_SETUP.md에 Sheet ID 정보 없음

**해결**:
다음 형식 중 하나로 추가:
```markdown
GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
```
또는
```markdown
- **Sheet ID**: `1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk`
```

## 보안 주의사항

- **PRIVATE_SETUP.md는 절대 Git에 커밋하지 마세요**
- `.gitignore`에 이미 등록되어 있음
- Service Account private key는 민감한 정보입니다
- 개인적으로만 전달하고, 공개 채널에 업로드 금지

## 다음 단계

설정 완료 후:

1. **제품 생성 테스트**:
   ```bash
   /generate VD25FPT003
   ```

2. **서버 실행**:
   ```bash
   /start-server
   ```

3. **배치 생성**:
   ```bash
   /batch-generate VD25FPT003 VD25FPT005 VD25FCA004
   ```

## 구현

현재 프로젝트 폴더의 PRIVATE_SETUP.md를 읽어서 자동 설정합니다.

**스크립트 위치**:
플러그인이 마켓플레이스를 통해 설치된 경우, 경로는 다음과 같습니다:
```bash
~/.claude/plugins/marketplaces/{marketplace-name}/{plugin-name}/scripts/auto_setup.py
```

예시:
```bash
~/.claude/plugins/marketplaces/pb2-marketplace/pb-product-generator-plugin/scripts/auto_setup.py
```

**자동 탐지 방법**:
```bash
# find 명령으로 동적으로 경로 찾기
SCRIPT_PATH=$(find ~/.claude/plugins -name "auto_setup.py" -path "*/pb-product-generator*/scripts/*" | head -1)
python3 "$SCRIPT_PATH"
```

**참고**:
- 스크립트는 현재 작업 디렉토리 기준으로 실행됩니다
- 모든 파일은 프로젝트 폴더에 생성됩니다 (credentials/, .env, output/)
- 마켓플레이스 이름은 설치 방법에 따라 다를 수 있습니다
