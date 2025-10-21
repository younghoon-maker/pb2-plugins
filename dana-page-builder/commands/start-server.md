---
description: Flask 편집 서버 실행 (Port 5002)
---

# Start Flask Server

Dana&Peta Editable HTML 파일을 제공하고 HTML/JPG 익스포트를 처리하는 Flask 로컬 서버를 실행합니다.

## 사용법

```bash
/dana-page-builder:start-server
```

## 작업 프로세스

1. **환경 검증**: output/ 디렉토리 및 Editable HTML 파일 확인
2. **Flask 서버 시작**: Port 5002에서 서버 실행
3. **브라우저 자동 열기**: `http://localhost:5002` 자동 실행
4. **대기 모드**: 사용자 요청 대기

## 출력 예시

```
============================================================
🚀 DANA&PETA 에디터블 서버 시작
============================================================
📂 Output Directory: /path/to/project/output
🌐 Server URL: http://localhost:5002
============================================================

✅ Found 3 editable HTML files:
   - DN25FW001_editable.html
   - DN25FW002_editable.html
   - DN25FW003_editable.html

🌐 Opening browser: http://localhost:5002

 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://0.0.0.0:5002
 * Press CTRL+C to quit
```

## 서버 엔드포인트

### 1. 홈 페이지: `/` (GET)
- 사용 가능한 Editable HTML 파일 목록 표시
- 각 파일 클릭하여 편집 모드 열기

### 2. Editable HTML 제공: `/editable/{product_code}` (GET)
- 예: `http://localhost:5002/editable/DN25FW001`
- Editable HTML 파일 제공
- 브라우저에서 이미지/텍스트 편집 가능

### 3. HTML 저장: `/save-html` (POST)
- 요청 본문: `{productCode, htmlContent}`
- 저장 경로: `output/날짜/익스포트/{productCode}_exported_dana.html`
- 중복 시 자동 suffix 추가 (_1, _2, ...)

### 4. JPG 저장: `/save-jpg` (POST)
- 요청 본문: `{productCode, imageData}` (base64)
- 저장 경로: `output/날짜/익스포트/{productCode}_dana.jpg`
- 중복 시 자동 suffix 추가

## 사용 워크플로우

### Step 1: 서버 시작
```bash
/dana-page-builder:start-server
```

### Step 2: 브라우저 접속
자동으로 `http://localhost:5002` 열림

### Step 3: 제품 선택
홈 페이지에서 편집할 제품 클릭

### Step 4: 이미지/텍스트 편집
- 우측 컨트롤 패널에서 이미지 크롭/줌 조정
- 페이지 줌 조절 (30-100%)
- 사이즈 이미지 선택
- 텍스트 직접 클릭하여 수정

### Step 5: 익스포트
- **HTML 다운로드** 버튼: 편집된 HTML 저장
- **JPG 다운로드** 버튼: 전체 페이지 이미지 저장

### Step 6: 결과 확인
```
output/날짜/익스포트/
├── DN25FW001_exported_dana.html
└── DN25FW001_dana.jpg
```

## 필수 조건

- **Editable HTML**: `output/날짜/에디터블/` 디렉토리에 파일 존재
- **Python 3.8+**: python3 실행 가능
- **Flask 설치**: `pip3 install flask flask-cors`
- **Port 5002**: 사용 가능 (5001은 PB가 사용)

## 에러 처리

### Port 5002 이미 사용 중
```
❌ Address already in use (Port 5002)
→ 기존 프로세스 종료:
   lsof -ti:5002 | xargs kill -9
```

### Editable HTML 파일 없음
```
❌ No editable HTML files found in output/
→ Generate products first:
   /dana-page-builder:generate DN25FW001
```

### Flask 미설치
```
❌ ModuleNotFoundError: No module named 'flask'
→ Install Flask:
   pip3 install flask flask-cors
```

## 구현

이 커맨드는 다음 Python 스크립트를 실행합니다:

```bash
PLUGIN_DIR="$HOME/.claude/plugins/marketplaces/pb-marketplace/dana-page-builder"
cd "$PLUGIN_DIR"
python3 scripts/server.py
```

## 서버 기능 상세

### 파일명 중복 처리
```python
# 중복 시 자동 suffix 추가
DN25FW001_dana.jpg       # 첫 번째
DN25FW001_dana_1.jpg     # 두 번째
DN25FW001_dana_2.jpg     # 세 번째
```

### html2canvas 기반 JPG 생성
- **해상도**: scale=2 (Retina 대응)
- **품질**: JPEG 95%
- **크기**: 약 2-3 MB (1200px 너비 기준)
- **선택 스타일 제거**: 녹색 테두리 자동 제거

### LocalStorage 설정 유지
- 이미지 크롭/줌 설정
- 페이지 줌 레벨
- 사이즈 이미지 선택
- 브라우저 재시작해도 유지

## 서버 중지

터미널에서 `CTRL+C` 입력:

```
^C
⚠️  Server stopped by user
```

## CORS 설정

Flask-CORS로 Cross-Origin 요청 허용:
- 브라우저에서 서버로 POST 요청 가능
- 파일 시스템 접근 제한 우회

## 참고

- **Port**: 5002 (PB는 5001 사용)
- **Debug Mode**: 개발 중 활성화
- **Hot Reload**: 코드 변경 시 자동 재시작
- **로그**: 터미널에 모든 요청 기록
- **.env FLASK_PORT**: 환경 변수로 포트 변경 가능

## 다음 단계

### 익스포트 파일 확인
```bash
ls -lh output/*/익스포트/
```

### 새로운 제품 추가 생성
```bash
# 서버 중지 (CTRL+C) 후
/dana-page-builder:generate DN25FW004

# 서버 재시작
/dana-page-builder:start-server
```

## 트러블슈팅

### 브라우저가 자동으로 열리지 않음
수동으로 접속:
```
http://localhost:5002
```

### 익스포트 버튼 클릭해도 반응 없음
- 콘솔 확인 (F12 → Console 탭)
- 서버 로그 확인 (터미널)
- 서버 재시작 시도

### JPG 품질이 낮음
`scripts/server.py` 수정:
```python
# scale=2를 scale=3으로 변경 (더 고해상도)
canvas = await html2canvas(container, {
    scale: 3,  # 원래 2
    ...
})
```

## 프로덕션 배포

이 서버는 로컬 개발용입니다. 프로덕션 배포 시:

```bash
# Gunicorn 사용 (권장)
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5002 server:app
```
