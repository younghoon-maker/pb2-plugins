# Migration Guide

pb-marketplace 버전 간 마이그레이션 가이드입니다.

---

## 📌 목차

- [v1.x → v2.0.0: Major Rebranding](#v1x--v200-major-rebranding)
- [v0.2.6 → v1.0.0: Claude Code Standard](#v026--v100-claude-code-standard)

---

# v1.x → v2.0.0: Major Rebranding

**마켓플레이스 및 플러그인 이름 변경으로 인한 완전 재설치 필요**

---

## 🚨 중요: Breaking Changes

### 1. 마켓플레이스 이름 변경
- `pb2-marketplace` → `pb-marketplace`

### 2. 저장소 URL 변경
- `younghoon-maker/pb2-plugins` → `younghoon-maker/pb-plugins`

### 3. 플러그인 이름 변경
- `pb-product-generator` → `pb2-page-builder`

### 4. 커맨드 네임스페이스 변경
- `/pb-product-generator:*` → `/pb2-page-builder:*`

### 5. 디렉토리 구조 변경
- `pb-product-generator-plugin/` → `pb2-page-builder/`

### 6. Major 버전 업그레이드
- pb-marketplace: `1.0.0` → `2.0.0`
- pb2-page-builder: `1.0.6` → `2.0.0`
- dana-page-builder: `1.0.3` → `2.0.0`

---

## 📋 마이그레이션 단계

### Step 1: 기존 마켓플레이스 제거

```bash
# 현재 마켓플레이스 확인
/plugin marketplace list

# 기존 마켓플레이스 제거
/plugin marketplace remove pb2-marketplace
```

### Step 2: 새 마켓플레이스 추가

```bash
# 새 저장소 URL로 마켓플레이스 추가
/plugin marketplace add younghoon-maker/pb-plugins
```

### Step 3: 플러그인 재설치

```bash
# pb2-page-builder 설치
/plugin install pb2-page-builder@pb-marketplace

# dana-page-builder 설치
/plugin install dana-page-builder@pb-marketplace
```

### Step 4: Claude 재시작

```bash
# Claude 종료
/quit

# Claude 재실행
claude
```

### Step 5: 검증

```bash
# 마켓플레이스 확인
/plugin marketplace list
# 출력: pb-marketplace (v2.0.0)

# 플러그인 확인
/plugin list
# 출력: pb2-page-builder@pb-marketplace (v2.0.0)
# 출력: dana-page-builder@pb-marketplace (v2.0.0)

# 커맨드 테스트 (pb2-page-builder)
/pb2-page-builder:generate VD25FPT003

# 커맨드 테스트 (dana-page-builder)
/dana-page-builder:generate DN25WOP002
```

---

## 🔄 구조 변경 사항

### Before (v1.x)

```
pb2-plugins/  (GitHub 저장소)
├── .claude-plugin/marketplace.json  (name: "pb2-marketplace")
├── pb-product-generator-plugin/    (v1.0.6)
└── dana-page-builder/               (v1.0.3)

로컬: ~/.claude/plugins/marketplaces/pb2-marketplace/
커맨드: /pb-product-generator:generate
```

### After (v2.0.0)

```
pb-plugins/  (GitHub 저장소)
├── .claude-plugin/marketplace.json  (name: "pb-marketplace", v2.0.0)
├── pb2-page-builder/                (v2.0.0)
└── dana-page-builder/               (v2.0.0)

로컬: ~/.claude/plugins/marketplaces/pb-marketplace/
커맨드: /pb2-page-builder:generate
```

---

## 📝 커맨드 변경 매핑

### pb2-page-builder (구: pb-product-generator)

| Before (v1.x) | After (v2.0.0) |
|---------------|----------------|
| `/pb-product-generator:generate` | `/pb2-page-builder:generate` |
| `/pb-product-generator:batch` | `/pb2-page-builder:batch` |
| `/pb-product-generator:server` | `/pb2-page-builder:server` |
| `/pb-product-generator:setup-from-private` | `/pb2-page-builder:setup-from-private` |
| `/pb-product-generator:cleanup` | `/pb2-page-builder:cleanup` |

### dana-page-builder (변경 없음)

| Before (v1.x) | After (v2.0.0) |
|---------------|----------------|
| `/dana-page-builder:generate` | `/dana-page-builder:generate` ✅ 동일 |
| `/dana-page-builder:batch-generate` | `/dana-page-builder:batch-generate` ✅ 동일 |
| `/dana-page-builder:start-server` | `/dana-page-builder:start-server` ✅ 동일 |
| `/dana-page-builder:setup-from-private` | `/dana-page-builder:setup-from-private` ✅ 동일 |
| `/dana-page-builder:cleanup` | `/dana-page-builder:cleanup` ✅ 동일 |

---

## 🤖 자동 마이그레이션 스크립트

전체 과정을 자동화하는 스크립트입니다:

```bash
#!/bin/bash
# v1.x → v2.0.0 마이그레이션 스크립트

echo "🚀 pb-marketplace v2.0.0 마이그레이션 시작..."

# Step 1: 기존 마켓플레이스 제거
echo "1️⃣ 기존 마켓플레이스 제거 중..."
# 수동으로 Claude에서 실행:
# /plugin marketplace remove pb2-marketplace

# Step 2: 새 마켓플레이스 추가
echo "2️⃣ 새 마켓플레이스 추가 중..."
# 수동으로 Claude에서 실행:
# /plugin marketplace add younghoon-maker/pb-plugins

# Step 3: 플러그인 재설치
echo "3️⃣ 플러그인 재설치 중..."
# 수동으로 Claude에서 실행:
# /plugin install pb2-page-builder@pb-marketplace
# /plugin install dana-page-builder@pb-marketplace

# Step 4: Claude 재시작
echo "4️⃣ Claude 재시작 필요..."
# 수동으로 실행: /quit && claude

echo "✅ 마이그레이션 스크립트 완료!"
echo "📝 Claude에서 위의 커맨드들을 순서대로 실행하세요."
```

---

## 🐛 문제 해결

### "Marketplace not found" 에러

```bash
# 저장소 URL 확인
# ❌ 잘못된 URL: younghoon-maker/pb2-plugins
# ✅ 올바른 URL: younghoon-maker/pb-plugins

/plugin marketplace add younghoon-maker/pb-plugins
```

### "Plugin not found" 에러

```bash
# 플러그인 이름 확인
# ❌ 잘못된 이름: pb-product-generator
# ✅ 올바른 이름: pb2-page-builder

/plugin install pb2-page-builder@pb-marketplace
```

### "Command not found" 에러

```bash
# 커맨드 네임스페이스 확인
# ❌ 잘못된 커맨드: /pb-product-generator:generate
# ✅ 올바른 커맨드: /pb2-page-builder:generate

/pb2-page-builder:generate VD25FPT003
```

### 캐시 문제

```bash
# Claude 캐시 클리어 (터미널에서)
rm -rf ~/.claude/cache/*

# Claude 재시작
claude
```

---

## ⚠️ 주의사항

### 1. 커맨드 히스토리 무효화
- v1.x 커맨드 히스토리는 v2.0.0에서 작동하지 않음
- 새로운 네임스페이스로 재실행 필요

### 2. 북마크/스크립트 업데이트
- 기존 커맨드를 사용하는 문서/스크립트 모두 업데이트 필요
- 예: `/pb-product-generator:*` → `/pb2-page-builder:*`

### 3. 프로젝트 파일 영향 없음
- `credentials/`, `output/` 폴더는 프로젝트 폴더에 유지
- 재설치 후에도 기존 설정 그대로 사용 가능
- PRIVATE_SETUP.md 재사용 가능

---

## 📞 Support

문제가 지속되는 경우:
1. GitHub Issues: https://github.com/younghoon-maker/pb-plugins/issues
2. 로그 확인: `dana_page_generation.log`, `batch_generation.log`
3. 마켓플레이스 상태: `/plugin marketplace list`
4. 플러그인 상태: `/plugin list`

---

**마이그레이션 날짜**: 2025-10-21
**버전**: v1.x → v2.0.0
**영향도**: 🔴 High (완전 재설치 필요)

---
---

# v0.2.6 → v1.0.0: Claude Code Standard

공식 Claude Code 플러그인 표준으로 마이그레이션하는 가이드입니다.

---

## 🎯 주요 변경사항

### 1. 공식 표준 준수
- 커스텀 구현 → 공식 Claude Code 플러그인 시스템 표준
- 디렉토리 구조 표준화
- plugin.json 스키마 표준화

### 2. dana-page-builder 통합
- **Before**: 심볼릭 링크 (독립 저장소)
- **After**: 마켓플레이스에 포함 (실제 디렉토리)

### 3. 버전 Major 업데이트
- pb2-marketplace: `0.2.6` → `1.0.0`
- pb-product-generator: `0.2.5` → `1.0.0`
- dana-page-builder: `0.1.0` → `1.0.0`

---

## 📋 마이그레이션 단계

### Step 1: 기존 플러그인 제거

```bash
# 설치된 플러그인 확인
/plugin list

# 플러그인 제거 (필요한 경우)
/plugin uninstall pb-product-generator@pb2-marketplace
/plugin uninstall dana-page-builder@pb2-marketplace
```

### Step 2: 마켓플레이스 업데이트

```bash
# 마켓플레이스 업데이트
/plugin marketplace update pb2-marketplace

# 또는 재설치
/plugin marketplace remove pb2-marketplace
/plugin marketplace add younghoon-maker/pb2-plugins
```

### Step 3: 플러그인 재설치

```bash
# pb-product-generator 설치
/plugin install pb-product-generator@pb2-marketplace

# dana-page-builder 설치
/plugin install dana-page-builder@pb2-marketplace
```

### Step 4: Claude 재시작

```bash
# Claude 종료
/quit

# Claude 재실행
claude
```

### Step 5: 검증

```bash
# 플러그인 설치 확인
/plugin list

# 커맨드 테스트
/pb-product-generator:generate VD25FTS002
/dana-page-builder:generate DN25FW001
```

---

## 🔄 구조 변경 사항

### pb2-marketplace

**Before (v0.2.6)**:
```
pb2-marketplace/
├── .claude-plugin/marketplace.json
├── pb-product-generator-plugin/  (실제 디렉토리)
└── dana-page-builder -> {symlink}
```

**After (v1.0.0)**:
```
pb2-marketplace/
├── .claude-plugin/marketplace.json
├── pb-product-generator-plugin/  (v1.0.0)
└── dana-page-builder/             (v1.0.0, 실제 디렉토리)
```

### dana-page-builder

**Before (v0.1.0)**:
```
dana-page-builder/
├── .claude-plugin/
│   ├── plugin.json
│   ├── commands/batch.md  ❌ 구버전 위치
│   └── agents/            ❌ 빈 디렉토리
└── ...
```

**After (v1.0.0)**:
```
dana-page-builder/
├── .claude-plugin/
│   └── plugin.json        ✅ 표준 위치
├── commands/              ✅ 루트 레벨
│   ├── generate.md
│   ├── batch-generate.md
│   ├── setup-from-private.md
│   └── start-server.md
├── agents/                ✅ 루트 레벨
│   └── dana-page-builder.md
└── ...
```

---

## ⚠️ Breaking Changes

### 1. 디렉토리 경로 변경
- **Impact**: 플러그인 재설치 필요
- **Action**: 위의 마이그레이션 단계 실행

### 2. plugin.json 스키마 변경
- **Impact**: 커스텀 설정 무효화 가능
- **Action**: 기본 설정으로 재설정

### 3. 심볼릭 링크 제거
- **Impact**: 로컬 개발 환경 변경 필요
- **Action**: dana-page-builder는 이제 마켓플레이스에 포함

---

## 🆕 새로운 기능

### dana-page-builder Agent
```bash
# 에이전트 호출
@agent-dana-page-builder "DN25FW001 생성해줘"
```

### 공식 표준 컴포넌트
- ✅ Commands (4개씩)
- ✅ Agents (각 1개)
- ⚠️ Skills (향후 추가 예정)
- ⚠️ Hooks (향후 추가 예정)
- ⚠️ MCP Servers (향후 추가 예정)

---

## 📊 호환성

### 지원되는 버전
- Claude Code: latest
- Python: 3.8+
- Google Sheets API: v4
- Google Drive API: v3

### 지원 중단
- ❌ 심볼릭 링크 패턴
- ❌ 구버전 디렉토리 구조

---

## 🐛 문제 해결

### "Plugin not found" 에러
```bash
# 마켓플레이스 재등록
/plugin marketplace remove pb2-marketplace
/plugin marketplace add younghoon-maker/pb2-plugins
```

### "Command not found" 에러
```bash
# 플러그인 재설치
/plugin uninstall {plugin-name}@pb2-marketplace
/plugin install {plugin-name}@pb2-marketplace

# Claude 재시작
/quit
claude
```

### 캐시 문제
```bash
# Claude 캐시 클리어 (터미널에서)
rm -rf ~/.claude/cache/*

# Claude 재시작
claude
```

---

## 📞 Support

문제가 지속되는 경우:
1. GitHub Issues: https://github.com/younghoon-maker/pb2-plugins/issues (v1.x URL)
2. 로그 확인: `dana_page_generation.log`, `batch_generation.log`
3. 플러그인 상태 확인: `/plugin list`

---

## 🎉 다음 단계

마이그레이션 완료 후:
1. ✅ 플러그인 설치 확인
2. ✅ 커맨드 테스트
3. ✅ 에이전트 테스트
4. 📖 새로운 CHANGELOG 확인
5. 🚀 제품 페이지 생성 시작!

---

**마이그레이션 날짜**: 2025-10-20
**최종 업데이트**: 2025-10-21
