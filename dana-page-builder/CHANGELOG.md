# Changelog - dana-page-builder

All notable changes to the dana-page-builder plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2025-10-21

### 🐛 Fixed
- **사이즈표 특수문자 입력 문제 해결**
  - 사이즈표에서 `-`, `=`, `+` 문자 입력 불가 문제 해결
  - 브라우저 줌 단축키(Cmd/Ctrl + `-`, `=`, `+`)와 충돌 방지
  - 사이즈표 헤더(`<th>`)와 셀(`<td class="editable">`) 모두 keydown 이벤트 처리 추가
  - `stopPropagation()`으로 브라우저 기본 동작 차단
- **플러그인 경로 수정**
  - 커맨드 파일 경로 수정: `pb2-marketplace` → `pb-marketplace`
  - `/dana-page-builder:generate`, `/dana-page-builder:batch-generate`, `/dana-page-builder:start-server` 커맨드 정상화

### 📝 Details
**사이즈표 문제 원인**:
- 브라우저는 Cmd/Ctrl + `-`/`=`/`+` 키를 줌 단축키로 사용
- contenteditable 요소에서도 이 단축키가 우선 처리되어 문자 입력 불가
- 사용자가 `-`, `=`, `+` 입력 시 브라우저가 줌 동작 실행

**해결 방법**:
- `.size-table th, .size-table td.editable` 요소에 keydown 이벤트 리스너 추가
- `-`, `=`, `+` 키 감지 시 `e.stopPropagation()` 호출
- 브라우저 기본 동작을 차단하여 정상적인 문자 입력 가능

**수정 파일**:
- `scripts/generate_pages_dana.py` (line 1124-1132)
- `commands/batch-generate.md` (line 92)
- `commands/generate.md` (line 82)
- `commands/start-server.md` (line 131)

**테스트 방법**:
```bash
# HTML 재생성
/dana-page-builder:generate DN25WBL001

# 브라우저에서 강력 새로고침 (캐시 무시)
Cmd + Shift + R (Mac) / Ctrl + Shift + R (Windows)

# 사이즈표 셀 클릭 후 -, =, + 입력 테스트
```

---

## [1.0.3] - 2025-10-21

### ✨ Added
- **Storage Cleanup 커맨드 추가**
  - `/dana-page-builder:cleanup` 슬래시 커맨드 추가
  - HTML, 이미지, 프로덕트 데이터를 타입별로 선택적 정리 가능
  - 통계 확인, 날짜 기반 정리, 크기 기반 정리 지원
  - Dry-run 모드로 안전한 시뮬레이션 가능

### 📝 Details
**주요 기능**:
- `--stats`: 전체 스토리지 통계 표시 (HTML + 이미지 + 데이터)
- `--html --days N`: HTML 파일만 정리 (N일 이전)
- `--images`: 이미지 캐시만 정리
- `--data`: 프로덕트 데이터만 정리
- `--all`: 전체 삭제 (사용자 확인 필요)
- `--max-size MB`: HTML 크기 제한 (초과 시 자동 삭제)
- `--dry-run`: 시뮬레이션 모드

**추가 파일**:
- `scripts/cleanup.py`: 스토리지 정리 스크립트
- `commands/cleanup.md`: 커맨드 문서
- `.claude-plugin/plugin.json`: cleanup 커맨드 등록

**사용 예시**:
```bash
/dana-page-builder:cleanup --stats
/dana-page-builder:cleanup --html --days 7
/dana-page-builder:cleanup --images
/dana-page-builder:cleanup --all --dry-run
```

---

## [1.0.2] - 2025-10-20

### 🐛 Fixed
- **출력 경로 문제 수정**
  - `config.py`: `PROJECT_ROOT`가 현재 작업 디렉토리(`Path.cwd()`)를 사용하도록 변경
  - 출력 파일이 플러그인 폴더 대신 프로젝트 폴더의 `output/`에 저장됨
- **슬래시 커맨드 경로 문제 수정**
  - 하드코딩된 절대 경로 제거
  - `PLUGIN_DIR` 환경변수를 사용한 동적 경로 설정
  - 불필요한 파일 탐색 제거

### 📝 Details
**수정 전 동작**:
- 출력 위치: `~/.claude/plugins/.../dana-page-builder/output/`
- 슬래시 커맨드: 존재하지 않는 경로로 `cd` 시도
- 파일 탐색: 불필요한 코드 탐색 발생

**수정 후 동작**:
- 출력 위치: 프로젝트 폴더의 `output/` (예: `/Users/user/project/output/`)
- 슬래시 커맨드: 플러그인 스크립트를 절대 경로로 실행
- 파일 탐색: 명확한 경로로 즉시 실행

**수정 파일**:
- `scripts/config.py` (line 10)
- `commands/generate.md` (lines 82-83)
- `commands/batch-generate.md` (lines 92-98)
- `commands/start-server.md` (lines 131-132)

---

## [1.0.1] - 2025-10-20

### 🐛 Fixed
- **JPG 익스포트 폴백 기능 수정**
  - 서버 미연결 시 브라우저 다운로드가 정상 작동하도록 개선
  - `base64Image` 변수 스코프 수정 (try 블록 밖에서 선언)
  - 서버 500 에러 시에도 폴백 다운로드 실행
  - catch 블록에서 `base64Image` 존재 여부 확인 추가

### 📝 Details
**수정 전 동작**:
- 서버 미실행 → ✅ 폴백 다운로드
- 서버 실행 + 500 에러 → ❌ 에러 메시지만 표시

**수정 후 동작**:
- 서버 미실행 → ✅ 폴백 다운로드
- 서버 실행 + 500 에러 → ✅ 폴백 다운로드

**파일**: `scripts/generate_pages_dana.py` (1640, 1673, 1699 라인)

---

## [1.0.0] - 2025-10-20

### 🏗️ Breaking Changes
- **공식 Claude Code 플러그인 표준 준수**
- 디렉토리 구조 전면 재편
- commands 경로 변경: `.claude-plugin/commands` → `./commands` (루트 레벨)
- plugin.json 스키마 표준화

### ✨ Added
- **Dana Page Builder Agent**: 302컬럼 전문 에이전트 (`agents/dana-page-builder.md`)
- **4개 Commands**: generate, batch-generate, setup-from-private, start-server
- **공식 표준 준수**: Claude Code 플러그인 시스템 공식 문서 기준

### 📁 Changed
- Directory structure standardized:
  ```
  dana-page-builder/
  ├── .claude-plugin/plugin.json  (메타데이터만)
  ├── commands/                    (루트 레벨로 이동)
  ├── agents/                      (신규 추가)
  ├── scripts/
  ├── src/
  └── templates/
  ```
- plugin.json version: `0.1.0` → `1.0.0`
- Description: "302컬럼 데이터 기반" 명시

### 🔄 Migration Guide
기존 사용자는 플러그인 재설치가 필요합니다:

```bash
# 1. 기존 플러그인 제거
/plugin uninstall dana-page-builder@pb2-marketplace

# 2. 마켓플레이스 업데이트
/plugin marketplace update pb2-marketplace

# 3. 플러그인 재설치
/plugin install dana-page-builder@pb2-marketplace

# 4. Claude 재시작
/quit
claude
```

### 🎯 Features
- Google Sheets 302컬럼 데이터 로드
- Dana&Peta 브랜드 특화 페이지 생성
- Editable HTML with crop/zoom editor
- Flask 서버 (Port 5002)
- 이미지 캐싱 및 병렬 다운로드

### 📦 Technical
- Python 3.8+
- Google Sheets API v4
- Google Drive API
- Jinja2 템플릿 엔진
- Pydantic 데이터 검증

---

## [0.1.0] - 2025-10-17

### Initial Release
- 첫 번째 베타 버전
- 기본 기능 구현
- 302컬럼 지원
