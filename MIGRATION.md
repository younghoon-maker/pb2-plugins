# Migration Guide: v0.2.6 → v1.0.0

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
1. GitHub Issues: https://github.com/younghoon-maker/pb2-plugins/issues
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
**최종 업데이트**: 2025-10-20
