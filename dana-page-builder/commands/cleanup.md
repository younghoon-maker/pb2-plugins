---
description: 스토리지 정리 (HTML, 이미지, 데이터 개별 정리)
tools: [Bash]
---

# Storage Cleanup - Dana Page Builder

Dana&Peta 제품 페이지 스토리지를 타입별로 세분화하여 선택적으로 정리합니다.

## 문제 상황

- HTML 파일이 각각 50-130MB (base64 이미지 포함)
- 이미지 캐시가 누적 (output/assets/images/)
- 날짜별 폴더가 누적 (output/YYYY-MM-DD/)
- 타입별 선택적 정리 필요

## 스토리지 구조

```
플러그인 output/
├── 2025-10-20/              # HTML 파일 (--html)
│   ├── 원본/                # 원본 HTML
│   ├── 에디터블/            # 편집 가능 HTML
│   └── 익스포트/            # JPG 파일
├── output/assets/images/    # 이미지 캐시 (--images)
│   ├── DN25WOP002_01.jpg
│   └── ...
└── data/                    # 프로덕트 데이터 (--data)
    └── products.json
```

## 사용법

### 1. 통계 확인 (전체)
```bash
/dana-page-builder:cleanup --stats
```

**출력 예시**:
```
📊 Dana Page Builder 스토리지 통계
=================================================
📄 HTML 파일: output/
💾 크기: 450.0 MB
📅 날짜별 폴더: 3개

📅 날짜별 폴더 상세:
   2025-10-18/ -   62.5 MB (2일 전) [원본(10개), 에디터블(10개)]
   2025-10-19/ -   67.4 MB (1일 전) [원본(8개), 에디터블(8개)]
   2025-10-20/ -  128.7 MB (0일 전) [원본(20개), 에디터블(20개)]

🖼️  이미지 캐시: output/assets/images
💾 크기: 45.0 MB
📄 이미지 파일: 128개

📦 프로덕트 데이터: data
💾 크기: 1.5 MB
📄 products.json 파일: 1개

💾 전체 크기: 496.5 MB
```

### 2. HTML 파일만 정리
```bash
/dana-page-builder:cleanup --html --days 7
```

**기능**:
- 7일 이상 오래된 날짜 폴더 삭제
- 이미지와 데이터는 그대로 유지

**시뮬레이션**:
```bash
/dana-page-builder:cleanup --html --days 7 --dry-run
```

### 3. 이미지만 정리
```bash
/dana-page-builder:cleanup --images
```

**기능**:
- output/assets/images/ 폴더의 모든 이미지 삭제
- HTML과 데이터는 그대로 유지

**날짜 기반 이미지 정리**:
```bash
/dana-page-builder:cleanup --images --days 7
```

**시뮬레이션**:
```bash
/dana-page-builder:cleanup --images --dry-run
/dana-page-builder:cleanup --images --days 7 --dry-run
```

### 4. 프로덕트 데이터만 정리
```bash
/dana-page-builder:cleanup --data
```

**기능**:
- data/ 폴더의 모든 products.json 파일 삭제
- HTML, 이미지는 그대로 유지

**날짜 기반 데이터 정리**:
```bash
/dana-page-builder:cleanup --data --days 7
```

**시뮬레이션**:
```bash
/dana-page-builder:cleanup --data --dry-run
/dana-page-builder:cleanup --data --days 7 --dry-run
```

### 5. 크기 기반 정리 (HTML만)
```bash
/dana-page-builder:cleanup --max-size 500
```

**기능**:
- HTML 폴더를 최대 500MB로 제한
- 초과 시 오래된 것부터 자동 삭제

**시뮬레이션**:
```bash
/dana-page-builder:cleanup --max-size 500 --dry-run
```

### 6. 전체 삭제 (주의!)
```bash
/dana-page-builder:cleanup --all
```

**경고**:
- HTML 전체 삭제
- 이미지 전체 삭제
- 프로덕트 데이터 전체 삭제
- 사용자 확인 필요 (yes 입력)

**시뮬레이션**:
```bash
/dana-page-builder:cleanup --all --dry-run
```

## 추천 워크플로우

### 일반 사용자 (타입별 정리)
```bash
# 1. 통계 확인
/dana-page-builder:cleanup --stats

# 2. HTML만 정리 (1주일 이전)
/dana-page-builder:cleanup --html --days 7

# 3. 이미지만 정리 (1주일 이전)
/dana-page-builder:cleanup --images --days 7

# 4. 프로덕트 데이터만 정리 (1주일 이전)
/dana-page-builder:cleanup --data --days 7
```

### 디스크 공간 부족 시
```bash
# 1. 통계 확인
/dana-page-builder:cleanup --stats

# 2. 이미지 전체 삭제 (가장 큰 용량)
/dana-page-builder:cleanup --images

# 3. 프로덕트 데이터 전체 삭제 (재생성 가능)
/dana-page-builder:cleanup --data

# 4. HTML 크기 제한 (예: 300MB)
/dana-page-builder:cleanup --max-size 300
```

### 정기 유지보수
```bash
# 매주 실행 - 타입별
/dana-page-builder:cleanup --html --days 14
/dana-page-builder:cleanup --images --days 14
/dana-page-builder:cleanup --data --days 14
```

## 옵션 상세

| 옵션 | 설명 | 예시 |
|-----|------|------|
| `--stats` | 통계만 표시 (HTML + 이미지 + 데이터) | `--stats` |
| `--html` | HTML 파일만 정리 (날짜별 폴더) | `--html --days 7` |
| `--images` | 이미지만 정리 | `--images` |
| `--data` | 프로덕트 데이터만 정리 (products.json) | `--data` |
| `--all` | 전체 삭제 (HTML + 이미지 + 데이터) | `--all` |
| `--days N` | N일 이전 파일 삭제 | `--days 7` |
| `--max-size MB` | 최대 크기 제한 (HTML만, MB) | `--max-size 500` |
| `--dry-run` | 시뮬레이션 (실제 삭제 안함) | `--dry-run` |
| `--output-dir PATH` | HTML 디렉토리 경로 | `--output-dir /custom/path` |
| `--images-dir PATH` | 이미지 디렉토리 경로 | `--images-dir output/assets/images` |
| `--data-dir PATH` | 데이터 디렉토리 경로 | `--data-dir data` |

## 정리 대상 (타입별)

### 1. HTML 파일 (--html)

**날짜별 폴더 (YYYY-MM-DD)**:
```
output/
  ├── 2025-10-18/   ← 오래된 폴더
  │   ├── 원본/
  │   ├── 에디터블/
  │   └── 익스포트/
  ├── 2025-10-19/
  └── 2025-10-20/   ← 최신 폴더 (보존)
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
  └── products.json
```

**특성**:
- Google Sheets에서 생성된 제품 데이터
- 재생성 가능 (load_from_sheets.py 재실행)
- 개발/테스트 시 누적되는 임시 데이터

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
find ~/.claude/plugins -name "cleanup.py" -path "*/dana-page-builder/scripts/*" 2>/dev/null | head -1
```

### Step 2: 사용자에게 옵션 확인
- `--stats` (통계만 표시)
- `--html --days N` (HTML만 정리)
- `--images` (이미지만 정리)
- `--data` (프로덕트 데이터만 정리)
- `--all` (전체 삭제: HTML + 이미지 + 데이터)
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

# HTML 크기 제한 (500MB)
python3 /path/to/cleanup.py --max-size 500

# 전체 삭제 (HTML + 이미지 + 데이터)
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

## 참고

- **프로덕트 데이터 재생성**: `/dana-page-builder:setup-from-private` 또는 Google Sheets 재로드
- **이미지 재다운로드**: 페이지 재생성 시 자동 다운로드
- **정기 정리 권장**: 매주 또는 매월 실행 권장
