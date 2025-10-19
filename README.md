# PB2 Plugins - Claude Code Marketplace

**제품 상세 페이지 생성 도구 플러그인 마켓플레이스**

Version: 0.2.2

---

## 📦 Available Plugins

### pb-product-generator (v0.2.2)

Google Sheets 292컬럼 데이터 기반 제품 상세 페이지 생성기 - **완전 자동화 세팅**

**✨ What's New in v0.2.2**:
- 🐛 스크립트 경로 버그 수정 (CWD 기반으로 변경)
- 📂 서비스 어카운트 및 출력 폴더가 프로젝트 폴더에 정상 저장
- 🔧 .env 파일 자동 로드 추가

**✨ v0.2.0 Features**:
- 🎯 5분 완성 자동 세팅 (`/pb-product-generator:setup-from-private`)
- 🏗️ 원본 코드 직접 포함 (2116 lines)
- 📊 70MB 고품질 출력 보장
- 🔐 PRIVATE_SETUP.md (서비스 어카운트 JSON 포함)

**Features**:
- ✨ Google Sheets 292컬럼 데이터 통합
- 🎨 Editable HTML V4 (이미지 crop/zoom, 텍스트 편집)
- 🚀 Flask 편집 서버 (Port 5001)
- 📊 배치 생성 지원

**Commands** (네임스페이스 접두사 필수):
- `/pb-product-generator:generate {product_code}` - 단일 제품 생성
- `/pb-product-generator:batch {code1} {code2} ...` - 배치 생성
- `/pb-product-generator:server` - Flask 편집 서버 실행
- `/pb-product-generator:setup-from-private` - 자동 세팅

**Agent**:
- `@agent-product-builder` - 제품 페이지 생성 전문 에이전트

---

## 🚀 Installation

### Quick Start (5분)

```bash
# Step 1: 마켓플레이스 추가
/plugin marketplace add younghoon-maker/pb2-plugins

# Step 2: 플러그인 설치
/plugin install pb-product-generator@pb2-plugins

# Step 3: Claude 재시작
/quit
claude

# Step 4: PRIVATE_SETUP.md를 관리자로부터 받아 프로젝트 폴더에 복사
# (중요: Claude를 실행하는 프로젝트 폴더에 복사)

# Step 5: 자동 세팅 실행
/pb-product-generator:setup-from-private

# Step 6: 사용
/pb-product-generator:generate VD25FPT003
```

---

## 📋 Prerequisites

### System Requirements

- **Claude Code**: Latest version
- **Python**: 3.11+
- **Git**: For repository cloning

### Required Files (팀 내부 전달)

**PRIVATE_SETUP.md**를 Slack/이메일로 받으세요:
- 서비스 어카운트 JSON 포함
- Sheet ID 및 탭 이름 명기
- 5분 완성 세팅 가이드

---

## 📚 Documentation

### 플러그인 문서
- **Plugin README**: [pb-product-generator-plugin/README.md](./pb-product-generator-plugin/README.md)
- **Onboarding Guide**: [pb-product-generator-plugin/ONBOARDING.md](./pb-product-generator-plugin/ONBOARDING.md)
- **Command Docs**: [pb-product-generator-plugin/commands/](./pb-product-generator-plugin/commands/)

### 사용 예시

#### 1. 단일 제품 생성
```bash
/pb-product-generator:generate VD25FPT003
```

#### 2. 배치 생성
```bash
/pb-product-generator:batch VD25FPT003 VD25FPT005 VD25FCA004
```

#### 3. Flask 서버
```bash
/pb-product-generator:server
# http://localhost:5001 자동 실행
```

---

## 🔧 Troubleshooting

### Plugin Not Found

**Issue**: Can't see plugin after adding marketplace

**Solution**:
1. Verify marketplace added: `/plugin marketplace list`
2. Refresh: `/plugin marketplace update pb2-marketplace`
3. Restart Claude Code

### Service Account 에러

**Issue**: `❌ Service Account file NOT found`

**Solution**:
- PRIVATE_SETUP.md 파일을 팀원에게 요청
- Step 2.2 (서비스 어카운트 JSON 생성) 실행

### Python Module Errors

**Issue**: `ModuleNotFoundError`

**Solution**:
```bash
cd ~/.claude/plugins/pb-product-generator/
pip3 install -r requirements.txt
```

---

## 🏗️ Directory Structure

```
pb2-plugins/                          # GitHub repository
├── .claude-plugin/
│   └── marketplace.json              # Marketplace definition (v0.2.0)
├── pb-product-generator-plugin/      # Plugin directory
│   ├── .claude-plugin/
│   │   └── plugin.json               # Plugin manifest (v0.2.0)
│   ├── commands/                     # Slash commands
│   │   ├── generate.md
│   │   ├── batch.md
│   │   └── server.md
│   ├── agents/                       # Agents
│   │   └── product-builder.md
│   ├── scripts/                      # Original scripts (2116 lines)
│   │   ├── generate_editable_html.py
│   │   ├── generate_batch.py
│   │   └── server.py
│   ├── src/                          # Full source code
│   ├── templates/                    # Jinja2 templates
│   ├── setup.sh                      # Auto setup script
│   ├── PRIVATE_SETUP.md              # Private guide (NOT in Git)
│   ├── requirements.txt
│   └── README.md
├── .gitignore                        # PRIVATE_SETUP.md excluded
└── README.md                         # This file
```

---

## 🔐 Security

**PRIVATE_SETUP.md는 Git에 포함되지 않습니다**:
- `.gitignore`에 명시적으로 제외
- 서비스 어카운트 JSON 포함
- 팀 내부에서만 Slack/이메일로 전달

**민감 정보 제외**:
- `credentials/`
- `service-account.json`
- `.env` 파일

---

## 📊 Version History

### v0.2.2 (2025-10-19) - 🐛 Path Fix

**Bug Fixes**:
- ✅ 스크립트 경로를 CWD 기반으로 수정
  - generate_batch.py: service_account, output 경로를 CWD 사용
  - server.py: OUTPUT_DIR을 CWD 기반으로 변경
  - .env 파일 자동 로드 추가 (python-dotenv)
- ✅ 서비스 어카운트 파일이 프로젝트 폴더에서 정상 로드
- ✅ 결과물이 프로젝트 폴더의 output/에 저장

**Technical Changes**:
- `Path(__file__).parent.parent` (플러그인 디렉토리) → `Path.cwd()` (현재 작업 디렉토리)
- 기존: `~/.claude/plugins/.../service-account.json`
- 수정: `{프로젝트 폴더}/credentials/service-account.json`

### v0.2.1 (2025-10-19) - 🐛 Bug Fixes

**Bug Fixes**:
- ✅ 사이즈표 파싱 로직 버그 수정
  - _parse_top_sizes(): hem, sleeve_cuff 필드 추가
  - _parse_bottom_sizes(): length 필드 추가
  - safe_float() 헬퍼 함수 도입
  - 검증 로직 개선 (size_name만 필수)
- ✅ product_description 필드 볼드 서식 지원
- ✅ column_mapping.py 인덱스 보정 (+1 shift)

**Documentation**:
- ✅ 네임스페이스 접두사 추가 (`/pb-product-generator:*`)
- ✅ GitHub 마켓플레이스 URL 업데이트
- ✅ 사용자 프로젝트 폴더 기반 워크플로우 문서화

### v0.2.0 (2025-10-18) - 🎯 Complete Automation

**Major Changes**:
- ✅ 완전 자동화 세팅 (setup.sh)
- ✅ 원본 코드 직접 포함 (코드 재생성 제거)
- ✅ 프라이빗 세팅 가이드 (PRIVATE_SETUP.md)
- ✅ 70MB 고품질 출력 보장

**Breaking Changes**:
- ❌ `.env.example` 제거 (자동 생성으로 대체)
- ❌ 수동 설정 과정 제거 (setup.sh로 자동화)
- ❌ 코드 생성 래퍼 제거 (원본 스크립트 사용)

---

## 🤝 Support

**팀 지원**:
- **이메일**: pb-team@company.com
- **슬랙**: #pb-product-generator

**문제 보고**:
1. Plugin README 및 PRIVATE_SETUP.md 참고
2. 환경 변수 설정 확인
3. Google Sheets 권한 검증
4. 팀 슬랙 채널에 문의

---

## 🔗 Links

- **Homepage**: https://github.com/younghoon-maker/pb2-plugins
- **Issues**: https://github.com/younghoon-maker/pb2-plugins/issues

---

## 📝 License

Private project.

© 2025 PB Product Team. All Rights Reserved.
