# Changelog - pb-product-generator

All notable changes to the pb-product-generator plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-20

### 🏗️ Breaking Changes
- **공식 Claude Code 플러그인 표준 준수**
- plugin.json 스키마 표준화
- 버전 Major 업데이트 (안정 버전 출시)

### ✨ Added
- **292-columns** 키워드 추가 (명확한 컬럼 수 표시)

### 📋 Changed
- plugin.json version: `0.2.5` → `1.0.0`
- Description 간결화: "Editable HTML V4" 명시
- 공식 플러그인 시스템 표준 완전 준수

### 🎯 Features (기존 유지)
- Google Sheets 292컬럼 데이터 로드
- PB 브랜드 제품 페이지 생성
- Editable HTML V4 with crop/zoom editor
- Flask 서버 (Port 5001)
- 이미지 캐싱 및 병렬 다운로드
- Product Builder Agent

### 📦 Technical
- Python 3.8+
- Google Sheets API v4
- Google Drive API
- Jinja2 템플릿 엔진
- Pydantic 데이터 검증
- Flask 웹 서버

---

## [0.2.5] - 2025-10-17

### Added
- 완전 자동화 세팅 기능
- PRIVATE_SETUP.md 기반 초기 설정

### Fixed
- 이미지 에디터 버그 수정
- 컬럼 매핑 개선

---

## [0.2.0] - 2025-10-15

### Added
- Editable HTML V4
- 이미지 crop/zoom 기능
- 브라우저 내 편집 기능

---

## [0.1.0] - 2025-10-10

### Initial Release
- 첫 번째 베타 버전
- 기본 HTML 생성 기능
- 292컬럼 지원
