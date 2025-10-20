---
description: Output 폴더 및 캐시 자동 정리 (오래된 파일 삭제)
tools: [Bash]
---

# Storage Cleanup - 자동 정리

오래된 output 파일과 캐시 파일들을 자동으로 정리하여 디스크 공간을 확보합니다.

## 문제 상황

- HTML 파일이 각각 50-130MB (base64 이미지 포함)
- output 폴더가 수백 MB~GB까지 증가
- Figma 캐시 파일들이 누적
- 주기적인 정리 필요

## 사용법

### 1. 통계 확인
```bash
/pb-product-generator:cleanup --stats
```

**출력 예시**:
```
📊 스토리지 통계
=================================================
📁 Output 폴더: /path/to/output
💾 크기: 784.0 MB
📅 날짜별 폴더: 4개
📄 루트 HTML 파일: 12개

📅 날짜별 폴더 상세:
   20251016/ -   45.2 MB (4일 전)
   20251017/ -  128.7 MB (3일 전)
   20251018/ -   62.5 MB (2일 전)
   20251020/ -   67.4 MB (0일 전)

📄 루트 HTML 파일:
   VD25FDP013_editable_v4_backup.html -  128.2 MB (4일 전)
   VD25FJP003_editable_v4.html -   62.1 MB (1일 전)
   ...

📦 캐시 폴더: .cache/figma
💾 크기: 5.2 MB
📄 캐시 파일: 24개

💾 전체 크기: 789.2 MB
```

### 2. 날짜 기반 정리 (권장)
```bash
/pb-product-generator:cleanup --days 7
```

**기능**:
- 7일 이상 오래된 날짜 폴더 삭제
- 7일 이상 오래된 루트 HTML 파일 삭제

**시뮬레이션 (삭제 예정 목록만 표시)**:
```bash
/pb-product-generator:cleanup --days 7 --dry-run
```

### 3. 크기 기반 정리
```bash
/pb-product-generator:cleanup --max-size 500
```

**기능**:
- output 폴더를 최대 500MB로 제한
- 초과 시 오래된 것부터 자동 삭제

**예시**:
```bash
# 현재 784MB → 500MB로 축소
/pb-product-generator:cleanup --max-size 500

# 시뮬레이션
/pb-product-generator:cleanup --max-size 500 --dry-run
```

### 4. 캐시만 정리
```bash
/pb-product-generator:cleanup --cache
```

**기능**:
- .cache/figma 폴더의 모든 캐시 파일 삭제
- Figma 메타데이터 캐시 초기화

**날짜 기반 캐시 정리**:
```bash
/pb-product-generator:cleanup --cache --days 7
```

**시뮬레이션**:
```bash
/pb-product-generator:cleanup --cache --dry-run
/pb-product-generator:cleanup --cache --days 7 --dry-run
```

### 5. 전체 삭제 (주의!)
```bash
/pb-product-generator:cleanup --all
```

**경고**:
- output 폴더 전체 삭제
- .cache/figma 폴더 전체 삭제
- 사용자 확인 필요 (yes 입력)

**시뮬레이션**:
```bash
/pb-product-generator:cleanup --all --dry-run
```

## 추천 워크플로우

### 일반 사용자
```bash
# 1. 통계 확인
/pb-product-generator:cleanup --stats

# 2. 1주일 이전 output 정리
/pb-product-generator:cleanup --days 7

# 3. 오래된 캐시 정리
/pb-product-generator:cleanup --cache --days 7
```

### 디스크 공간 부족 시
```bash
# 1. 통계 확인
/pb-product-generator:cleanup --stats

# 2. 캐시 전체 삭제 (즉시 효과)
/pb-product-generator:cleanup --cache

# 3. 크기 제한 (예: 300MB)
/pb-product-generator:cleanup --max-size 300
```

### 정기 유지보수
```bash
# 매주 실행 (cron 등)
/pb-product-generator:cleanup --days 14
/pb-product-generator:cleanup --cache --days 30
```

## 옵션 상세

| 옵션 | 설명 | 예시 |
|-----|------|------|
| `--stats` | 통계만 표시 | `--stats` |
| `--days N` | N일 이전 파일 삭제 | `--days 7` |
| `--max-size MB` | 최대 크기 제한 (MB) | `--max-size 500` |
| `--cache` | 캐시 파일만 정리 | `--cache` |
| `--all` | 전체 삭제 (output + cache) | `--all` |
| `--dry-run` | 시뮬레이션 (실제 삭제 안함) | `--dry-run` |
| `--output-dir PATH` | output 디렉토리 경로 | `--output-dir /custom/path` |
| `--cache-dir PATH` | 캐시 디렉토리 경로 | `--cache-dir .cache/figma` |

## 정리 대상

### 1. Output 폴더

**날짜별 폴더 (YYYYMMDD)**:
```
output/
  ├── 20251016/   ← 오래된 폴더
  │   ├── editable/  (편집 가능 HTML)
  │   └── export/    (JPG 파일)
  ├── 20251017/
  └── 20251020/   ← 최신 폴더 (보존)
```

**루트 HTML 파일**:
```
output/
  ├── VD25FDP013_editable_v4.html  ← 수정 시간 기준
  ├── VD25FJP003_editable_v4.html
  └── ...
```

### 2. 캐시 폴더

**Figma 메타데이터 캐시**:
```
.cache/
  └── figma/
      ├── 1-95.json   ← Figma 노드 캐시
      ├── 1-96.json
      └── ...
```

**캐시 특성**:
- TTL 기반 (기본 1시간)
- 재생성 가능 (삭제해도 다음 실행 시 재생성)
- 네트워크 요청 감소용

## 자동화 예시

### Bash 스크립트
```bash
#!/bin/bash
# weekly_cleanup.sh

cd /path/to/project
python3 ~/.claude/plugins/marketplaces/pb2-marketplace/pb-product-generator-plugin/scripts/cleanup.py --days 14

echo "✅ Weekly cleanup completed"
```

### macOS Launchd (매주 일요일 자동 실행)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pb.product-generator.cleanup</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>/Users/username/.claude/plugins/marketplaces/pb2-marketplace/pb-product-generator-plugin/scripts/cleanup.py</string>
        <string>--days</string>
        <string>14</string>
        <string>--output-dir</string>
        <string>/Users/username/project/output</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

## 안전 기능

1. **Dry Run**: `--dry-run`으로 실제 삭제 전 시뮬레이션
2. **사용자 확인**: `--all` 옵션은 'yes' 입력 필요
3. **상세 로그**: 삭제되는 파일/폴더 목록 표시
4. **크기 표시**: 확보되는 공간 표시

## 트러블슈팅

### ❌ Permission denied
**원인**: 파일/폴더 권한 부족

**해결**:
```bash
chmod -R u+w output/
```

### ❌ Output folder not found
**원인**: output 폴더가 없음

**해결**:
```bash
mkdir -p output
```

### ⚠️ 잘못 삭제된 경우
**복구 불가능**: Time Machine 또는 백업에서 복구

**예방**:
- 항상 `--dry-run`으로 먼저 확인
- 중요한 파일은 별도 백업

## ⚙️ Claude 실행 지침 (Internal)

**이 커맨드를 실행할 때 다음 단계를 따르세요**:

### Step 1: cleanup.py 스크립트 경로 찾기
```bash
find ~/.claude/plugins -name "cleanup.py" -path "*/pb-product-generator*/scripts/*" 2>/dev/null | head -1
```

### Step 2: 사용자에게 옵션 확인
- `--stats` (통계만 표시)
- `--days N` (N일 이전 파일 삭제)
- `--max-size MB` (크기 제한)
- `--cache` (캐시만 정리)
- `--all` (전체 삭제: output + cache)
- `--dry-run` (시뮬레이션)

### Step 3: Python 스크립트 실행
```bash
python3 {SCRIPT_PATH} {OPTIONS}
```

**예시**:
```bash
# 통계 표시
python3 /path/to/cleanup.py --stats

# 7일 이전 output 파일 삭제
python3 /path/to/cleanup.py --days 7

# 캐시만 정리 (전체)
python3 /path/to/cleanup.py --cache

# 캐시만 정리 (7일 이전)
python3 /path/to/cleanup.py --cache --days 7

# 크기 제한 (500MB)
python3 /path/to/cleanup.py --max-size 500

# 전체 삭제 (output + cache)
python3 /path/to/cleanup.py --all

# 시뮬레이션
python3 /path/to/cleanup.py --days 7 --dry-run
python3 /path/to/cleanup.py --cache --dry-run
```

**중요**:
- Step 1과 Step 3은 **별도의 Bash 도구 호출**로 실행
- 변수 할당 `$(...)` 사용 금지
- 사용자가 옵션을 지정하지 않으면 `--stats` 기본 실행
