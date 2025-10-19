# Google Cloud 설정 가이드

본 가이드는 Google Sheets API를 사용하기 위한 Google Cloud Console 설정 방법을 안내합니다.

---

## 목차

1. [Google Cloud 프로젝트 생성](#1-google-cloud-프로젝트-생성)
2. [Google Sheets API 활성화](#2-google-sheets-api-활성화)
3. [서비스 계정 생성](#3-서비스-계정-생성)
4. [서비스 계정 키 다운로드](#4-서비스-계정-키-다운로드)
5. [Google Sheet 공유 설정](#5-google-sheet-공유-설정)
6. [설정 검증](#6-설정-검증)
7. [문제 해결](#7-문제-해결)

---

## 1. Google Cloud 프로젝트 생성

### 1.1 Google Cloud Console 접속

1. 브라우저에서 [Google Cloud Console](https://console.cloud.google.com/) 접속
2. Google 계정으로 로그인

### 1.2 새 프로젝트 생성

1. 상단 메뉴에서 **프로젝트 선택** 클릭
2. **새 프로젝트** 클릭
3. 프로젝트 정보 입력:
   - **프로젝트 이름**: `pb-pb2-page-builder` (예시)
   - **위치**: 조직 없음 (개인용)
4. **만들기** 클릭

> **참고**: 프로젝트 생성은 약 30초 소요됩니다.

---

## 2. Google Sheets API 활성화

### 2.1 API 및 서비스 메뉴

1. 좌측 메뉴에서 **API 및 서비스** → **라이브러리** 클릭
2. 검색창에 `Google Sheets API` 입력
3. **Google Sheets API** 선택
4. **사용** 버튼 클릭

### 2.2 API 활성화 확인

1. 좌측 메뉴에서 **API 및 서비스** → **대시보드** 클릭
2. **Google Sheets API**가 목록에 표시되면 성공

---

## 3. 서비스 계정 생성

### 3.1 서비스 계정 메뉴

1. 좌측 메뉴에서 **API 및 서비스** → **사용자 인증 정보** 클릭
2. 상단 **+ 사용자 인증 정보 만들기** 클릭
3. **서비스 계정** 선택

### 3.2 서비스 계정 세부정보

1. **서비스 계정 이름**: `pb-pb2-sheets-reader` (예시)
2. **서비스 계정 ID**: 자동 생성됨 (예: `pb-pb2-sheets-reader@project-id.iam.gserviceaccount.com`)
3. **서비스 계정 설명**: `Google Sheets API 읽기 전용 계정` (선택사항)
4. **만들기 및 계속하기** 클릭

### 3.3 권한 부여 (선택사항)

1. **역할 선택**: 이 단계는 건너뛰어도 됩니다
2. **계속** 클릭
3. **완료** 클릭

---

## 4. 서비스 계정 키 다운로드

### 4.1 키 생성

1. **사용자 인증 정보** 페이지에서 방금 생성한 서비스 계정 클릭
2. 상단 **키** 탭 클릭
3. **키 추가** → **새 키 만들기** 클릭
4. **키 유형**: JSON 선택
5. **만들기** 클릭

### 4.2 JSON 파일 저장

1. JSON 파일이 자동으로 다운로드됨
2. 파일명을 `service-account.json`으로 변경
3. 프로젝트의 `credentials/` 폴더에 저장

```bash
# 프로젝트 루트 디렉토리에서 실행
mkdir -p credentials
mv ~/Downloads/project-id-xxxxx.json credentials/service-account.json
```

### 4.3 파일 권한 확인

```bash
# 파일 존재 확인
ls -lh credentials/service-account.json

# 파일 권한 설정 (읽기 전용)
chmod 600 credentials/service-account.json
```

---

## 5. Google Sheet 공유 설정

### 5.1 서비스 계정 이메일 복사

1. `credentials/service-account.json` 파일 열기
2. `client_email` 값 복사 (예: `pb-pb2-sheets-reader@project-id.iam.gserviceaccount.com`)

또는 터미널에서 추출:
```bash
# macOS/Linux
cat credentials/service-account.json | grep client_email

# 또는 jq 사용
jq -r '.client_email' credentials/service-account.json
```

### 5.2 Google Sheets 공유

1. 브라우저에서 Google Sheets 문서 열기
2. 우측 상단 **공유** 버튼 클릭
3. **사용자 추가** 필드에 서비스 계정 이메일 붙여넣기
4. 권한 설정:
   - **뷰어** (읽기 전용) - 권장
   - **편집자** (읽기/쓰기) - 필요 시에만
5. **전송** 클릭 (알림 전송 체크박스는 해제 가능)

> **중요**: 서비스 계정이 Google Sheets에 접근하려면 반드시 공유 설정이 필요합니다.

---

## 6. 설정 검증

### 6.1 환경 변수 설정

`.env` 파일 생성:
```bash
cp .env.example .env
```

`.env` 파일 편집:
```bash
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
```

**Sheet ID 찾기**:
- Google Sheets URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
- `{SHEET_ID}` 부분을 복사

### 6.2 연결 테스트

간단한 Python 스크립트로 연결 확인:

```python
# test_connection.py
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 서비스 계정 인증
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = service_account.Credentials.from_service_account_file(
    'credentials/service-account.json', scopes=SCOPES)

# Sheets API 클라이언트 생성
service = build('sheets', 'v4', credentials=creds)

# Sheet ID 입력
SHEET_ID = 'your_sheet_id_here'

# 데이터 읽기 테스트
try:
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range='A1:A1'
    ).execute()
    print("✅ 연결 성공!")
    print(f"   Sheet ID: {SHEET_ID}")
    print(f"   값: {result.get('values', [])}")
except Exception as e:
    print(f"❌ 연결 실패: {e}")
```

실행:
```bash
python3 test_connection.py
```

**성공 메시지**:
```
✅ 연결 성공!
   Sheet ID: 1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk
   값: [['Product Code']]
```

---

## 7. 문제 해결

### 7.1 `FileNotFoundError: service-account.json`

**원인**: 서비스 계정 파일이 없거나 경로가 잘못됨

**해결**:
```bash
# 파일 존재 확인
ls credentials/service-account.json

# 파일이 없다면 다시 다운로드
# Google Cloud Console → 서비스 계정 → 키 탭 → 새 키 만들기
```

### 7.2 `403 Forbidden: The caller does not have permission`

**원인**: Google Sheets가 서비스 계정과 공유되지 않음

**해결**:
1. Google Sheets 문서 열기
2. 우측 상단 **공유** 클릭
3. 서비스 계정 이메일 추가 (뷰어 권한)
4. 전송

### 7.3 `404 Not Found: Requested entity was not found`

**원인**: Sheet ID가 잘못되었거나 Sheet가 삭제됨

**해결**:
1. Google Sheets URL에서 Sheet ID 다시 확인
2. Sheet가 존재하는지 확인
3. `.env` 파일의 `GOOGLE_SHEET_ID` 업데이트

### 7.4 `API has not been used in project`

**원인**: Google Sheets API가 활성화되지 않음

**해결**:
1. Google Cloud Console → API 및 서비스 → 라이브러리
2. `Google Sheets API` 검색
3. **사용** 버튼 클릭
4. 5분 후 다시 시도

### 7.5 `Invalid JSON in credentials file`

**원인**: JSON 파일이 손상되었거나 잘못된 형식

**해결**:
```bash
# JSON 유효성 검사
python3 -c "import json; print(json.load(open('credentials/service-account.json')))"

# 오류 발생 시 새 키 다운로드
```

---

## 보안 권장사항

### 1. 서비스 계정 키 관리

✅ **권장**:
- `credentials/` 폴더를 `.gitignore`에 추가
- 파일 권한을 `600`으로 설정 (소유자만 읽기/쓰기)
- 키를 절대 공개 저장소에 커밋하지 않음

❌ **금지**:
- 키를 소스 코드에 하드코딩
- 키를 이메일로 전송
- 키를 공개 폴더에 저장

### 2. 최소 권한 원칙

- 서비스 계정에 **뷰어** 권한만 부여 (읽기 전용)
- 필요한 경우에만 **편집자** 권한 부여
- 정기적으로 사용하지 않는 키 삭제

### 3. 키 회전

- 6개월마다 새 키 생성 권장
- 이전 키는 즉시 삭제
- Google Cloud Console → 서비스 계정 → 키 탭에서 관리

---

## 다음 단계

설정이 완료되었으면:

1. **사용 가이드**: [USAGE_GUIDE.md](USAGE_GUIDE.md)에서 워크플로우 확인
2. **스키마 문서**: [GOOGLE_SHEETS_SCHEMA.md](GOOGLE_SHEETS_SCHEMA.md)에서 데이터 구조 확인
3. **예제 실행**: `examples/` 폴더의 스크립트로 HTML 생성

---

## 참고 자료

- [Google Sheets API 공식 문서](https://developers.google.com/sheets/api)
- [서비스 계정 가이드](https://cloud.google.com/iam/docs/service-accounts)
- [Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
- [OAuth 2.0 Scopes](https://developers.google.com/identity/protocols/oauth2/scopes)

---

**최종 업데이트**: 2025-10-16
**작성자**: MoAI-ADK
