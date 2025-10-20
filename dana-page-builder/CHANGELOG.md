# Changelog - dana-page-builder

All notable changes to the dana-page-builder plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
