---
description: 스토리지 세분화 정리 (HTML, 이미지, 캐시 개별 정리)
tools: [Bash]
---

# Storage Cleanup - 세분화 자동 정리

스토리지를 타입별로 세분화하여 선택적으로 정리합니다.

## 문제 상황

- HTML 파일이 각각 50-130MB (base64 이미지 포함)
- 이미지 캐시가 누적 (output/assets/images/)
- Figma 캐시 파일들이 누적 (.cache/figma/)
- 타입별 선택적 정리 필요

## 스토리지 구조

```
프로젝트/
├── output/                    # HTML 파일 (--html)
│   ├── 20251017/
│   │   ├── editable/          # 편집 가능 HTML
│   │   └── export/            # JPG 파일
│   └── *.html                 # 루트 HTML
├── output/assets/images/      # 이미지 캐시 (--images)
│   ├── DN25WOP002_01.jpg
│   └── ...
├── data/                      # 프로덕트 데이터 (--data)
│   ├── products.json
│   └── dana-page-builder/
│       └── products.json
└── .cache/figma/              # Figma 캐시 (--cache)
    ├── 1-95.json
    └── ...
```

## 사용법

### 1. 통계 확인 (전체)
```bash
/pb2-page-builder:cleanup --stats
```

**출력 예시**:
```
📊 스토리지 통계
=================================================
📄 HTML 파일: /path/to/output
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

🖼️  이미지 캐시: output/assets/images
💾 크기: 45.0 MB
📄 이미지 파일: 128개

📦 프로덕트 데이터: data
💾 크기: 2.5 MB
📄 products.json 파일: 2개

   products.json - 1.2 MB (3일 전)
   dana-page-builder/products.json - 1.3 MB (1일 전)

📦 Figma 캐시: .cache/figma
💾 크기: 5.2 MB
📄 캐시 파일: 24개

💾 전체 크기: 836.7 MB
```

### 2. HTML 파일만 정리
```bash
/pb2-page-builder:cleanup --html --days 7
```

**기능**:
- 7일 이상 오래된 날짜 폴더 삭제
- 7일 이상 오래된 루트 HTML 파일 삭제
- 이미지와 캐시는 그대로 유지

**시뮬레이션**:
```bash
/pb2-page-builder:cleanup --html --days 7 --dry-run
```

### 3. 이미지만 정리
```bash
/pb2-page-builder:cleanup --images
```

**기능**:
- output/assets/images/ 폴더의 모든 이미지 삭제
- HTML과 캐시는 그대로 유지

**날짜 기반 이미지 정리**:
```bash
/pb2-page-builder:cleanup --images --days 7
```

**시뮬레이션**:
```bash
/pb2-page-builder:cleanup --images --dry-run
/pb2-page-builder:cleanup --images --days 7 --dry-run
```

### 4. 프로덕트 데이터만 정리
```bash
/pb2-page-builder:cleanup --data
```

**기능**:
- data/ 폴더의 모든 products.json 파일 삭제
- HTML, 이미지, 캐시는 그대로 유지

**날짜 기반 데이터 정리**:
```bash
/pb2-page-builder:cleanup --data --days 7
```

**시뮬레이션**:
```bash
/pb2-page-builder:cleanup --data --dry-run
/pb2-page-builder:cleanup --data --days 7 --dry-run
```

### 5. Figma 캐시만 정리
```bash
/pb2-page-builder:cleanup --cache
```

**기능**:
- .cache/figma/ 폴더의 모든 캐시 파일 삭제
- HTML과 이미지는 그대로 유지

**날짜 기반 캐시 정리**:
```bash
/pb2-page-builder:cleanup --cache --days 7
```

**시뮬레이션**:
```bash
/pb2-page-builder:cleanup --cache --dry-run
/pb2-page-builder:cleanup --cache --days 7 --dry-run
```

### 6. 크기 기반 정리 (HTML만)
```bash
/pb2-page-builder:cleanup --max-size 500
```

**기능**:
- HTML 폴더를 최대 500MB로 제한
- 초과 시 오래된 것부터 자동 삭제

**시뮬레이션**:
```bash
/pb2-page-builder:cleanup --max-size 500 --dry-run
```

### 7. 전체 삭제 (주의!)
```bash
/pb2-page-builder:cleanup --all
```

**경고**:
- HTML 전체 삭제
- 이미지 전체 삭제
- 프로덕트 데이터 전체 삭제
- Figma 캐시 전체 삭제
- 사용자 확인 필요 (yes 입력)

**시뮬레이션**:
```bash
/pb2-page-builder:cleanup --all --dry-run
```

## 추천 워크플로우

### 일반 사용자 (타입별 정리)
```bash
# 1. 통계 확인
/pb2-page-builder:cleanup --stats

# 2. HTML만 정리 (1주일 이전)
/pb2-page-builder:cleanup --html --days 7

# 3. 이미지만 정리 (1주일 이전)
/pb2-page-builder:cleanup --images --days 7

# 4. 프로덕트 데이터만 정리 (1주일 이전)
/pb2-page-builder:cleanup --data --days 7

# 5. Figma 캐시만 정리 (1주일 이전)
/pb2-page-builder:cleanup --cache --days 7
```

### 디스크 공간 부족 시
```bash
# 1. 통계 확인
/pb2-page-builder:cleanup --stats

# 2. 이미지 전체 삭제 (가장 큰 용량)
/pb2-page-builder:cleanup --images

# 3. 프로덕트 데이터 전체 삭제 (재생성 가능)
/pb2-page-builder:cleanup --data

# 4. Figma 캐시 전체 삭제 (즉시 효과)
/pb2-page-builder:cleanup --cache

# 5. HTML 크기 제한 (예: 300MB)
/pb2-page-builder:cleanup --max-size 300
```

### 정기 유지보수
```bash
# 매주 실행 (cron 등) - 타입별
/pb2-page-builder:cleanup --html --days 14
/pb2-page-builder:cleanup --images --days 14
/pb2-page-builder:cleanup --data --days 14
/pb2-page-builder:cleanup --cache --days 30
```

## 옵션 상세

| 옵션 | 설명 | 예시 |
|-----|------|------|
| `--stats` | 통계만 표시 (HTML + 이미지 + 데이터 + 캐시) | `--stats` |
| `--html` | HTML 파일만 정리 (--days 필수) | `--html --days 7` |
| `--images` | 이미지만 정리 | `--images` |
| `--data` | 프로덕트 데이터만 정리 (products.json) | `--data` |
| `--cache` | Figma 캐시만 정리 | `--cache` |
| `--all` | 전체 삭제 (HTML + 이미지 + 데이터 + 캐시) | `--all` |
| `--days N` | N일 이전 파일 삭제 | `--days 7` |
| `--max-size MB` | 최대 크기 제한 (HTML만, MB) | `--max-size 500` |
| `--dry-run` | 시뮬레이션 (실제 삭제 안함) | `--dry-run` |
| `--output-dir PATH` | HTML 디렉토리 경로 | `--output-dir /custom/path` |
| `--images-dir PATH` | 이미지 디렉토리 경로 | `--images-dir output/assets/images` |
| `--data-dir PATH` | 데이터 디렉토리 경로 | `--data-dir data` |
| `--cache-dir PATH` | 캐시 디렉토리 경로 | `--cache-dir .cache/figma` |

## 정리 대상 (타입별)

### 1. HTML 파일 (--html)

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

### 2. 이미지 캐시 (--images)

**제품 이미지**:
```
output/assets/images/
  ├── DN25WOP002_01.jpg
  ├── DN25WOP002_02.jpg
  └── ...
```

**특성**:
- 용량이 가장 큼 (수십~수백 MB)
- 재다운로드 가능
- 네트워크 대역폭 절약용

### 3. 프로덕트 데이터 (--data)

**products.json 파일**:
```
data/
  ├── products.json
  └── dana-page-builder/
      └── products.json
```

**특성**:
- Google Sheets에서 생성된 제품 데이터
- 재생성 가능 (load_from_sheets.py 재실행)
- 개발/테스트 시 누적되는 임시 데이터

### 4. Figma 캐시 (--cache)

**Figma 메타데이터 캐시**:
```
.cache/figma/
  ├── 1-95.json   ← Figma 노드 캐시
  ├── 1-96.json
  └── ...
```

**특성**:
- TTL 기반 (기본 1시간)
- 재생성 가능 (삭제해도 다음 실행 시 재생성)
- Figma API 요청 감소용

## 자동화 예시

### Bash 스크립트
```bash
#!/bin/bash
# weekly_cleanup.sh

cd /path/to/project
python3 ~/.claude/plugins/marketplaces/pb2-marketplace/pb2-page-builder/scripts/cleanup.py --days 14

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
        <string>/Users/username/.claude/plugins/marketplaces/pb2-marketplace/pb2-page-builder/scripts/cleanup.py</string>
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
find ~/.claude/plugins -name "cleanup.py" -path "*/pb2-page-builder*/scripts/*" 2>/dev/null | head -1
```

### Step 2: 사용자에게 옵션 확인
- `--stats` (통계만 표시)
- `--html --days N` (HTML만 정리)
- `--images` (이미지만 정리)
- `--data` (프로덕트 데이터만 정리)
- `--cache` (Figma 캐시만 정리)
- `--all` (전체 삭제: HTML + 이미지 + 데이터 + 캐시)
- `--max-size MB` (HTML 크기 제한)
- `--dry-run` (시뮬레이션)

### Step 3: Python 스크립트 실행
```bash
python3 {SCRIPT_PATH} {OPTIONS}
```

**예시**:
```bash
# 통계 표시
python3 /path/to/cleanup.py --stats

# HTML만 정리 (7일 이전)
python3 /path/to/cleanup.py --html --days 7

# 이미지만 정리 (전체)
python3 /path/to/cleanup.py --images

# 이미지만 정리 (7일 이전)
python3 /path/to/cleanup.py --images --days 7

# 프로덕트 데이터만 정리 (전체)
python3 /path/to/cleanup.py --data

# 프로덕트 데이터만 정리 (7일 이전)
python3 /path/to/cleanup.py --data --days 7

# Figma 캐시만 정리 (전체)
python3 /path/to/cleanup.py --cache

# Figma 캐시만 정리 (7일 이전)
python3 /path/to/cleanup.py --cache --days 7

# HTML 크기 제한 (500MB)
python3 /path/to/cleanup.py --max-size 500

# 전체 삭제 (HTML + 이미지 + 데이터 + 캐시)
python3 /path/to/cleanup.py --all

# 시뮬레이션
python3 /path/to/cleanup.py --html --days 7 --dry-run
python3 /path/to/cleanup.py --images --dry-run
python3 /path/to/cleanup.py --all --dry-run
```

**중요**:
- Step 1과 Step 3은 **별도의 Bash 도구 호출**로 실행
- 변수 할당 `$(...)` 사용 금지
- 사용자가 옵션을 지정하지 않으면 도움말 표시
