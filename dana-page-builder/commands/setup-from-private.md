---
description: PRIVATE_SETUP.md 파싱하여 자동 환경 구축
---

# Setup from Private

현재 프로젝트 폴더의 `PRIVATE_SETUP.md`를 파싱하여 Dana Page Builder 환경을 자동으로 구축합니다.

## 작업 프로세스

1. **PRIVATE_SETUP.md 파싱**: 프로젝트 폴더에서 파일 읽기
2. **Service Account 추출**: JSON 블록 파싱 (```json...```)
3. **credentials/ 폴더 생성**: 프로젝트 폴더에 credentials/ 디렉토리 생성
4. **service-account.json 저장**: 추출한 JSON을 credentials/service-account.json에 저장
5. **.env 파일 생성**: Dana 전용 환경 변수 설정
6. **Python 의존성 설치**: requirements.txt 기반 설치
7. **output/ 디렉토리 생성**: 출력 폴더 준비

## 사용법

```bash
# Step 1: PRIVATE_SETUP.md를 프로젝트 폴더에 복사
cp ~/.claude/plugins/marketplaces/dana-marketplace/dana-page-builder/PRIVATE_SETUP.md .

# Step 2: Claude Code에서 자동 세팅 실행
/dana-page-builder:setup-from-private
```

## 출력

```
🔍 Checking PRIVATE_SETUP.md...
✅ Found: /path/to/project/PRIVATE_SETUP.md

📋 Parsing service account JSON...
✅ Extracted service account JSON (1,234 bytes)

📁 Creating credentials/ directory...
✅ Created: /path/to/project/credentials/

💾 Saving service-account.json...
✅ Saved: /path/to/project/credentials/service-account.json

⚙️ Creating .env file...
✅ Created: /path/to/project/.env

📦 Installing Python dependencies...
✅ Installed: gspread, Pillow, Jinja2, Flask, numpy

📁 Creating output/ directory...
✅ Created: /path/to/project/output/

✅ Setup Complete!

📝 Next Steps:
1. /dana-page-builder:generate DN25FW001
2. /dana-page-builder:start-server
```

## 필수 조건

- **PRIVATE_SETUP.md**: 현재 프로젝트 폴더에 존재해야 함
- **Python 3.7+**: `python3 --version`
- **pip3**: Python 패키지 관리자

## 에러 처리

- **PRIVATE_SETUP.md 없음**: `❌ PRIVATE_SETUP.md not found in current directory` → 파일 복사 필요
- **JSON 파싱 실패**: `❌ Failed to extract service account JSON` → PRIVATE_SETUP.md 형식 확인
- **권한 에러**: `❌ Permission denied: credentials/` → `chmod 755 .` 실행

## .env 파일 내용

setup-from-private 커맨드가 생성하는 .env 파일:

```bash
GOOGLE_SHEET_ID=1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
FLASK_PORT=5002
FLASK_DEBUG=False
```

## 환경 설정 정보

- **Google Sheet ID**: `1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk`
- **Tab Name**: `요청서` (코드 내 하드코딩)
- **Flask Port**: 5002 (PB는 5001, Dana는 5002)
- **Service Account**: `test-account-n8n@damoa-fb351.iam.gserviceaccount.com`

## 구현

이 커맨드는 플러그인의 Python 스크립트를 실행합니다:

```bash
python3 scripts/setup_from_private.py
```

## 프로젝트 폴더 vs 플러그인 폴더

**중요한 차이점**:
- **플러그인 폴더**: `~/.claude/plugins/marketplaces/dana-marketplace/dana-page-builder/`
  - 플러그인 코드 위치
  - PRIVATE_SETUP.md 원본 위치
  - scripts/, templates/ 등 소스 코드

- **프로젝트 폴더**: Claude를 실행하는 현재 작업 디렉토리
  - PRIVATE_SETUP.md 복사 위치
  - credentials/ 생성 위치
  - .env 생성 위치
  - output/ 생성 위치

## Google Sheets 권한 설정

setup-from-private 실행 후, Google Sheets에 서비스 어카운트 접근 권한을 부여하세요:

1. Google Sheets 열기: https://docs.google.com/spreadsheets/d/1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk/edit
2. 우측 상단 "공유" 버튼 클릭
3. `test-account-n8n@damoa-fb351.iam.gserviceaccount.com` 이메일 추가
4. 권한: **뷰어** 선택
5. "보내기" 클릭

## 참고 문서

- `PRIVATE_SETUP.md` - 전체 세팅 가이드
- `README.md` - 플러그인 설명서
- `scripts/setup_from_private.py` - 실제 구현 코드
