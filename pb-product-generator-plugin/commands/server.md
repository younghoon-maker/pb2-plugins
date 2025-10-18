---
description: Flask 편집 서버 실행 (Port 5001)
tools: [Bash]
---

# Start Edit Server

Editable HTML 파일 목록 제공 및 HTML/JPG 익스포트 기능을 제공하는 Flask 서버를 실행합니다.

## 작업 프로세스

1. **서버 시작**: Flask 서버 Port 5001에서 실행
2. **브라우저 오픈**: 자동으로 `http://localhost:5001` 열림
3. **파일 목록**: `output/{YYYYMMDD}/editable/` 폴더의 모든 Editable HTML 표시
4. **편집 및 익스포트**: 이미지 크롭/줌, 텍스트 편집, HTML/JPG 다운로드

## 사용법

```bash
/start-server
```

**브라우저 자동 실행**:
```
🚀 Flask Server Started on http://localhost:5001
🌐 Opening browser...
```

## 서버 엔드포인트

1. **`/` (GET)**: 사용 가능한 Editable HTML 파일 목록
2. **`/editable/{product_code}` (GET)**: 특정 제품 Editable HTML 제공
3. **`/save-html` (POST)**: 편집된 HTML 저장
4. **`/save-jpg` (POST)**: 페이지를 JPG로 익스포트

## Editable 기능

### 1. 이미지 편집
- **Pan X/Y**: 이미지 수평/수직 위치 조정 (-50 ~ +50)
- **Zoom**: 확대/축소 (100% ~ 500%)
- **Drag**: 마우스 드래그로 이미지 이동
- **Wheel**: 마우스 휠로 줌 조정

### 2. 페이지 줌
- **범위**: 30% ~ 100%
- **기본값**: 60% (1200px 페이지가 화면에 맞게)
- **단축키**: Ctrl + 마우스 휠

### 3. 텍스트 편집
- 모든 텍스트 요소 contenteditable
- 제품명, 설명, 상세 포인트, 패브릭 정보, 사이즈 표, 모델 정보

### 4. 익스포트
- **HTML 다운로드**: 편집된 내용을 포함한 완전한 HTML
- **JPG 다운로드**: 고해상도 이미지 (scale: 2x, JPEG 95% 품질)
- **자동 저장**: `output/{YYYYMMDD}/export/` 폴더에 저장

## Port 변경

`.env` 파일에서 포트 변경 가능:
```bash
FLASK_PORT=5002
```

## 에러 처리

- **Port 충돌**: `Address already in use`
  ```bash
  lsof -ti:5001 | xargs kill -9
  ```

- **파일 없음**: `No editable files found`
  → `/generate` 또는 `/batch-generate`로 먼저 파일 생성

## 필수 설정

### PRIVATE_SETUP.md 사용 (권장)

서버 실행 전 프로젝트 폴더에서 설정 완료:

```bash
# 1. 템플릿 복사
cp ~/.claude/plugins/pb-product-generator/PRIVATE_SETUP.md.template ./PRIVATE_SETUP.md

# 2. PRIVATE_SETUP.md 편집 (Service Account, Sheet ID 등)
# 3. 자동 설정 실행
~/.claude/plugins/pb-product-generator/setup.sh
```

자세한 설정 방법은 `/generate` 커맨드 문서 참조.

## 구현

현재 프로젝트 폴더의 `output/` 디렉토리를 기준으로 서버를 실행합니다:

```bash
python3 ~/.claude/plugins/pb-product-generator/scripts/server.py
```

**참고**:
- 서버는 현재 작업 디렉토리의 `output/` 폴더를 스캔하여 Editable HTML을 제공합니다.
- 익스포트 파일도 현재 작업 디렉토리의 `output/{YYYYMMDD}/export/`에 저장됩니다.

## 서버 종료

Claude Code 터미널에서 `Ctrl + C` 또는:
```bash
lsof -ti:5001 | xargs kill -9
```
