# pb-marketplace - Claude Code Plugin Marketplace

**PB 제품 상세 페이지 생성 도구 마켓플레이스 - 공식 Claude Code 표준 v2.0.0**

Version: 2.0.0

---

## 🎉 What's New in v2.0.0 - Major Rebranding

### 🚀 Breaking Changes
- **마켓플레이스 이름 변경**: pb2-marketplace → **pb-marketplace**
- **저장소 URL 변경**: `younghoon-maker/pb2-plugins` → `younghoon-maker/pb-plugins`
- **플러그인 리네이밍**: pb-product-generator → **pb2-page-builder**
- **커맨드 네임스페이스**: `/pb-product-generator:*` → `/pb2-page-builder:*`

### ✨ Major Version Bump
- pb-marketplace: 1.0.0 → **2.0.0**
- pb2-page-builder: 1.0.6 → **2.0.0**
- dana-page-builder: 1.0.3 → **2.0.0**

### 📚 마켓플레이스 중심 개편
- 양쪽 플러그인 균형있는 문서화
- 브랜드별 차별점 명확화 (VD vs DN)
- 통합 마이그레이션 가이드 제공

---

## 📦 Available Plugins

이 마켓플레이스는 **2개의 제품 상세 페이지 생성 플러그인**을 제공합니다:

### 🔵 pb2-page-builder (v2.0.0)

**PB2 제품 상세 페이지 생성기 - 292컬럼 기반 (VD 브랜드)**

**Features**:
- ✨ Google Sheets 292컬럼 데이터 통합 (VD 브랜드 특화)
- 🎨 Editable HTML V4 (이미지 crop/zoom, 텍스트 편집)
- 🚀 Flask 편집 서버 (Port 5001)
- 📊 배치 생성 지원
- 🔐 완전 자동화 세팅

**Commands** (네임스페이스 접두사 필수):
- `/pb2-page-builder:generate {product_code}` - 단일 제품 생성
- `/pb2-page-builder:batch {code1} {code2} ...` - 배치 생성
- `/pb2-page-builder:server` - Flask 편집 서버 실행
- `/pb2-page-builder:setup-from-private` - 자동 세팅
- `/pb2-page-builder:cleanup` - 파일 정리

**Agent**:
- `@agent-product-builder` - PB2 제품 페이지 생성 전문 에이전트

---

### 🟣 dana-page-builder (v2.0.0)

**Dana&Peta 브랜드 제품 상세 페이지 생성기 - 302컬럼 기반**

**Features**:
- ✨ Google Sheets 302컬럼 데이터 통합 (Dana&Peta 브랜드 특화)
- 🎨 Editable HTML with crop/zoom editor
- 🚀 Flask 편집 서버 (Port 5002)
- 📊 배치 생성 지원
- 🖼️ 라이프스타일 갤러리 확장 지원

**Commands** (네임스페이스 접두사 필수):
- `/dana-page-builder:generate {product_code}` - 단일 제품 생성
- `/dana-page-builder:batch-generate {code1} {code2} ...` - 배치 생성
- `/dana-page-builder:start-server` - Flask 편집 서버 실행 (Port 5002)
- `/dana-page-builder:setup-from-private` - 자동 세팅
- `/dana-page-builder:cleanup` - 파일 정리

**Agent**:
- `@agent-dana-page-builder` - Dana 302컬럼 전문 에이전트

---

### 📊 플러그인 비교

| 항목 | pb2-page-builder | dana-page-builder |
|------|------------------|-------------------|
| **브랜드** | VD (일반 PB) | DN (Dana&Peta) |
| **컬럼 수** | 292 | 302 |
| **Flask 포트** | 5001 | 5002 |
| **타겟 고객** | 일반 | 여성 고객 |
| **Agent** | @agent-product-builder | @agent-dana-page-builder |

---

## 🚀 Installation

### Quick Start (5분)

#### pb2-page-builder 설치

```bash
# Step 1: 마켓플레이스 추가
/plugin marketplace add younghoon-maker/pb-plugins

# Step 2: 플러그인 설치
/plugin install pb2-page-builder@pb-marketplace

# Step 3: Claude 재시작
/quit
claude

# Step 4: PRIVATE_SETUP.md를 관리자로부터 받아 프로젝트 폴더에 복사

# Step 5: 자동 세팅 실행
/pb2-page-builder:setup-from-private

# Step 6: 사용
/pb2-page-builder:generate VD25FPT003
```

#### dana-page-builder 설치

```bash
# Step 1: 마켓플레이스 추가 (이미 추가했다면 생략)
/plugin marketplace add younghoon-maker/pb-plugins

# Step 2: 플러그인 설치
/plugin install dana-page-builder@pb-marketplace

# Step 3: Claude 재시작
/quit
claude

# Step 4: PRIVATE_SETUP.md를 관리자로부터 받아 프로젝트 폴더에 복사

# Step 5: 자동 세팅 실행
/dana-page-builder:setup-from-private

# Step 6: 사용
/dana-page-builder:generate DN25WOP002
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

### pb2-page-builder 문서
- **Plugin README**: [pb2-page-builder/README.md](./pb2-page-builder/README.md)
- **Command Docs**: [pb2-page-builder/commands/](./pb2-page-builder/commands/)
- **CHANGELOG**: [pb2-page-builder/CHANGELOG.md](./pb2-page-builder/CHANGELOG.md)

### dana-page-builder 문서
- **Plugin README**: [dana-page-builder/README.md](./dana-page-builder/README.md)
- **Command Docs**: [dana-page-builder/commands/](./dana-page-builder/commands/)
- **CHANGELOG**: [dana-page-builder/CHANGELOG.md](./dana-page-builder/CHANGELOG.md)

### 마켓플레이스 문서
- **Installation Guide**: [INSTALLATION_GUIDE.md](./INSTALLATION_GUIDE.md)
- **Migration Guide**: [MIGRATION.md](./MIGRATION.md) - v1.x → v2.0.0 가이드

---

## 🔧 사용 예시

### pb2-page-builder 예시

#### 1. 단일 제품 생성 (VD 브랜드)
```bash
/pb2-page-builder:generate VD25FPT003
```

#### 2. 배치 생성
```bash
/pb2-page-builder:batch VD25FPT003 VD25FPT005 VD25FCA004
```

#### 3. Flask 서버
```bash
/pb2-page-builder:server
# http://localhost:5001 자동 실행
```

#### 4. 파일 정리
```bash
/pb2-page-builder:cleanup --html --days 7
```

### dana-page-builder 예시

#### 1. 단일 제품 생성 (DN 브랜드)
```bash
/dana-page-builder:generate DN25WOP002
```

#### 2. 배치 생성
```bash
/dana-page-builder:batch-generate DN25WOP002 DN25FDP001
```

#### 3. Flask 서버
```bash
/dana-page-builder:start-server
# http://localhost:5002 자동 실행
```

#### 4. 파일 정리
```bash
/dana-page-builder:cleanup --images --days 7
```

---

## 🏗️ Directory Structure

```
pb-plugins/                            # GitHub repository (v2.0.0)
├── .claude-plugin/
│   └── marketplace.json               # Marketplace definition (v2.0.0)
├── pb2-page-builder/                  # PB2 Plugin (v2.0.0)
│   ├── .claude-plugin/
│   │   └── plugin.json                # Plugin manifest
│   ├── commands/                      # Slash commands
│   │   ├── generate.md
│   │   ├── batch.md
│   │   ├── server.md
│   │   ├── setup-from-private.md
│   │   └── cleanup.md
│   ├── agents/                        # Agents
│   │   └── product-builder.md
│   ├── scripts/                       # Python scripts
│   │   ├── generate_editable_html.py
│   │   ├── generate_batch.py
│   │   ├── server.py
│   │   ├── cleanup.py
│   │   └── auto_setup.py
│   ├── src/                           # Full source code
│   ├── templates/                     # Jinja2 templates
│   ├── requirements.txt
│   ├── CHANGELOG.md
│   └── README.md
├── dana-page-builder/                 # Dana Plugin (v2.0.0)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/                      # Slash commands
│   │   ├── generate.md
│   │   ├── batch-generate.md
│   │   ├── start-server.md
│   │   ├── setup-from-private.md
│   │   └── cleanup.md
│   ├── agents/
│   │   └── dana-page-builder.md
│   ├── scripts/
│   ├── src/
│   ├── templates/
│   ├── requirements.txt
│   ├── CHANGELOG.md
│   └── README.md
├── .gitignore                         # PRIVATE_SETUP.md excluded
├── INSTALLATION_GUIDE.md              # 통합 설치 가이드
├── MIGRATION.md                       # v1.x → v2.0.0 마이그레이션
└── README.md                          # This file
```

---

## 🔧 Troubleshooting

### Plugin Not Found

**Issue**: Can't see plugin after adding marketplace

**Solution**:
1. Verify marketplace added: `/plugin marketplace list`
2. Refresh: `/plugin marketplace update pb-marketplace`
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
# pb2-page-builder
cd ~/.claude/plugins/marketplaces/pb-marketplace/pb2-page-builder/
pip3 install -r requirements.txt

# dana-page-builder
cd ~/.claude/plugins/marketplaces/pb-marketplace/dana-page-builder/
pip3 install -r requirements.txt
```

### 포트 충돌

**Issue**: Flask 서버 실행 시 포트 충돌

**Solution**:
- pb2-page-builder: Port 5001
- dana-page-builder: Port 5002
- 두 서버를 동시에 실행 가능 (다른 포트 사용)

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

### v2.0.0 (2025-10-21) - 🚀 Major Rebranding

**BREAKING CHANGES**:
- ❌ 마켓플레이스: pb2-marketplace → pb-marketplace
- ❌ 저장소: pb2-plugins → pb-plugins
- ❌ 플러그인: pb-product-generator → pb2-page-builder
- ❌ 커맨드: `/pb-product-generator:*` → `/pb2-page-builder:*`
- ❌ 폴더명: pb-product-generator-plugin → pb2-page-builder

**마이그레이션 필요**:
- 기존 사용자는 마켓플레이스/플러그인 재설치 필요
- 상세 가이드: [MIGRATION.md](./MIGRATION.md)

**Major Version Bump**:
- pb-marketplace: 1.0.0 → 2.0.0
- pb2-page-builder: 1.0.6 → 2.0.0
- dana-page-builder: 1.0.3 → 2.0.0

### v1.0.0 (2025-10-20) - 🏗️ Claude Code Standard

**Features**:
- ✨ 공식 Claude Code 플러그인 표준 완전 준수
- ✨ dana-page-builder 마켓플레이스 통합
- 📚 통합 문서화 (CHANGELOG, MIGRATION)

---

## 🤝 Support

**팀 지원**:
- **이메일**: pb-team@company.com
- **슬랙**: #pb-plugins

**문제 보고**:
1. Plugin README 및 PRIVATE_SETUP.md 참고
2. 환경 변수 설정 확인
3. Google Sheets 권한 검증
4. 팀 슬랙 채널에 문의

---

## 🔗 Links

- **Homepage**: https://github.com/younghoon-maker/pb-plugins
- **Issues**: https://github.com/younghoon-maker/pb-plugins/issues
- **Marketplace**: pb-marketplace v2.0.0

---

## 📝 License

Private project.

© 2025 PB Product Team. All Rights Reserved.
