# Dana Page Builder - Claude Code Plugin

**Dana&Peta 브랜드 제품 상세 페이지 자동 생성 플러그인**

Google Sheets 102컬럼 데이터에서 Editable HTML을 자동으로 생성하는 Claude Code 플러그인입니다.

---

## ✨ 주요 기능

- 📊 **Google Sheets 연동**: 102컬럼 제품 데이터 자동 로드
- 🎨 **Figma 디자인 구현**: 픽셀 퍼펙트 레이아웃
- 🖼️ **이미지 자동 처리**: Google Drive 다운로드 + Base64 인코딩
- ✏️ **Editable HTML**: 브라우저에서 이미지 크롭/텍스트 편집
- 💾 **HTML/JPG 익스포트**: Flask 서버 기반 파일 저장
- 🎯 **10개 섹션**: 히어로, 디테일 포인트, 갤러리, 로고 그룹, Fabric, Product Info 등

---

## 🚀 빠른 시작 (5분 완성)

### 1단계: 플러그인 설치

```bash
# Claude Code에서 실행
claude

# Marketplace 추가
/plugin marketplace add younghoon-maker/dana-marketplace

# 플러그인 설치
/plugin install dana-page-builder@dana-marketplace

# Claude Code 재시작 (필수!)
/quit
claude
```

### 2단계: 자동 환경 구축

관리자로부터 `PRIVATE_SETUP.md` 파일을 받아 프로젝트 폴더에 복사:

```bash
# PRIVATE_SETUP.md를 프로젝트 폴더에 복사
cp /path/to/PRIVATE_SETUP.md /your/project/folder/

# 프로젝트 폴더로 이동
cd /your/project/folder/

# 자동 세팅 실행
/dana-page-builder:setup-from-private
```

**자동으로 수행되는 작업:**
- ✅ `credentials/service-account.json` 생성
- ✅ `.env` 파일 생성
- ✅ Python 의존성 설치
- ✅ `output/` 디렉토리 생성

### 3단계: 제품 생성

```bash
# 단일 제품 생성
/dana-page-builder:generate DN25FW001

# 또는 여러 제품 배치 생성
/dana-page-builder:batch-generate DN25FW001 DN25FW002
```

### 4단계: 브라우저에서 확인

```bash
# Flask 서버 시작 (Port 5002)
/dana-page-builder:start-server

# http://localhost:5002 자동 실행
```

---

## 📋 사용 가능한 커맨드

| 커맨드 | 설명 | 예시 |
|--------|------|------|
| `/dana-page-builder:setup-from-private` | 자동 환경 구축 | 최초 1회 실행 |
| `/dana-page-builder:generate` | 단일 제품 생성 | `DN25FW001` |
| `/dana-page-builder:batch-generate` | 여러 제품 배치 생성 | `DN25FW001 DN25FW002` |
| `/dana-page-builder:start-server` | Flask 서버 시작 | Port 5002 |

---

## 🎨 Dana&Peta 브랜드 특징

### 10개 섹션 구조

1. **Hero Section** (1565px): 브랜드 로고 + 메인 이미지 + 컬러 스와치
2. **Product Info**: 제품명 + 소구점 3개 + MD 코멘트
3. **Color Section**: 가로 스와치 레이아웃 (최대 4컬러)
4. **Detail Points**: 4개 포인트 (좌우 레이아웃)
5. **Gallery**: 컬러별 그룹화 + 로고 그룹 삽입
6. **Product Shots**: 컬러 라벨 오버레이
7. **Fabric Info**: 원단 이미지 + 설명 + 테이블
8. **Product Info**: 사이즈 이미지 + 제품 정보 테이블
9. **Size Tables**: 동적 컬럼 생성 (상의/하의)
10. **Model Info + Footer**: 모델 정보 + 브랜드 정보

### 갤러리 로고 그룹 패턴

- **로고 그룹 1** (이미지 4-5): 좌우 배치 + 45도 회전 로고 2개
- **로고 그룹 2** (이미지 7-8): 상하 배치 + 가로 로고 1개
- **효과**: `filter: invert(1)` (흑백 반전)
- **컬러별 독립 패턴**: 이미지 개수가 달라도 정상 작동

---

## 🖼️ Editable HTML 기능

### 이미지 편집 (우측 컨트롤 패널)
- **드래그**: 이미지 위에서 클릭 + 드래그로 위치 이동
- **휠**: 마우스 휠로 확대/축소
- **슬라이더**: 가로/세로 위치 (0-200%), 확대/축소 (10-300%)

### 페이지 줌
- **범위**: 30% ~ 100%
- **기본값**: 60%
- **단축키**: Ctrl + 마우스 휠

### 사이즈 이미지 선택
- Product Info 섹션의 사이즈 일러스트레이션 변경
- 7가지 옵션: 상의, 팬츠, 스커트-H라인, 스커트-플레어, 아우터, 원피스, 점프수트

### LocalStorage 자동 저장
- 이미지 크롭/줌 설정
- 페이지 줌 레벨
- 사이즈 이미지 선택
- 브라우저 재시작 후에도 유지

---

## 💾 HTML/JPG 익스포트

Flask 서버에서 편집 후 익스포트:

1. **HTML 다운로드**: 편집된 상태 그대로 HTML 저장
2. **JPG 다운로드**: html2canvas로 전체 페이지 이미지 저장

**저장 경로**: `output/날짜/익스포트/`

```
output/20251020/익스포트/
├── DN25FW001_exported_dana.html  (HTML 파일)
└── DN25FW001_dana.jpg             (JPG 파일, 2-3 MB)
```

---

## 📊 Google Sheets 구조

### Spreadsheet ID
```
1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk
```

### 탭 구조
- **요청서** (A2:CV100): 102개 컬럼 제품 정보
- **이미지** (A2:AU100): 이미지 URL (하이퍼링크)

### 컬럼 분류
| 범위 | 카테고리 | 개수 | 설명 |
|------|----------|------|------|
| A~C | 기본 정보 | 3 | 제품코드, 제목, 태그라인 |
| D~F | 소구점 | 3 | 3가지 소구점 |
| G | 메인 이미지 | 1 | 히어로 이미지 |
| H~K | 컬러 이미지 | 4 | 4개 컬러 변형 |
| L~AA | 컬러 정보 | 16 | 4컬러 × 4필드 |
| AB~AI | 디테일 포인트 | 8 | 4포인트 × 2필드 |
| AJ~AQ | 갤러리 | 8 | 8개 갤러리 이미지 |
| AR~AU | 제품샷 | 4 | 4개 제품샷 |
| AV~BA | 원단 정보 | 6 | 이미지, 이름, 설명, 구성 |
| BB~BF | 원단 속성 | 5 | 투명도, 신축성, 안감, 두께, 시즌 |
| BG~BL | 제품 정보 | 6 | 6개 케어 지침 |
| BM~BT | 상의 사이즈 | 8 | 8개 측정값 |
| BU~CB | 하의 사이즈 | 8 | 8개 측정값 |
| CC~CF | 모델 정보 | 4 | 2모델 × 2필드 |
| CG~CH | 샷 주의사항 | 2 | 2개 주의사항 라인 |
| CI | 사이즈 권장사항 | 1 | 사이징 가이드 |
| CJ~CR | 예약 | 11 | 향후 확장 |

---

## 🔧 기술 스택

### Backend
- **Python 3.8+**: 코어 로직
- **Google Sheets API**: 데이터 로드
- **Google Drive API**: 이미지 다운로드
- **Pillow**: 이미지 처리
- **NumPy**: K-means 컬러 추출
- **Flask**: 로컬 웹 서버 (Port 5002)
- **Flask-CORS**: Cross-Origin 요청

### Frontend
- **HTML5 + CSS3**: 레이아웃
- **JavaScript (Vanilla)**: 이미지 편집 로직
- **html2canvas**: JPG 익스포트
- **LocalStorage**: 설정 저장
- **Google Fonts**: Cormorant Garamond, Pretendard

### Template
- **Jinja2**: Python f-string 기반 HTML 생성
- **Base64 인코딩**: 단일 파일 HTML (5-10 MB)

---

## 📁 프로젝트 구조

```
dana-page-builder/
├── .claude-plugin/
│   └── plugin.json              # 플러그인 메타데이터
├── commands/                    # 슬래시 커맨드 정의
│   ├── setup-from-private.md
│   ├── generate.md
│   ├── batch-generate.md
│   └── start-server.md
├── scripts/                     # Python 스크립트
│   ├── setup_from_private.py    # 자동 환경 구축
│   ├── load_from_sheets.py      # Google Sheets 로더
│   ├── generate_pages_dana.py   # HTML 생성기
│   └── server.py                # Flask 서버
├── size_images/                 # 사이즈 일러스트레이션
│   ├── 상의.png
│   ├── 팬츠.png
│   ├── 스커트-H라인.png
│   ├── 스커트-플레어.png
│   ├── 아우터.png
│   ├── 원피스.png
│   └── 점프수트.png
├── reference/                   # 레퍼런스 자료
│   └── logo/
│       ├── dana&peta_logo.png
│       └── dana&peta_logo_black.png
├── credentials/                 # 🔐 서비스 어카운트 (Git 제외)
│   └── service-account.json
├── PRIVATE_SETUP.md             # 🔐 프라이빗 세팅 가이드 (Git 제외)
├── requirements.txt             # Python 의존성
├── .gitignore                   # Git 제외 파일
└── README.md                    # 본 파일
```

**생성되는 폴더 (프로젝트 폴더)**:
```
your-project-folder/
├── credentials/                 # setup-from-private가 생성
├── .env                         # setup-from-private가 생성
└── output/                      # generate가 생성
    └── 20251020/
        ├── 에디터블/            # Editable HTML
        └── 익스포트/            # HTML/JPG 익스포트
```

---

## ⚙️ 환경 변수 (.env)

setup-from-private 커맨드가 자동으로 생성:

```bash
GOOGLE_SHEET_ID=1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
FLASK_PORT=5002
FLASK_DEBUG=False
```

---

## 🔐 보안

### 서비스 어카운트 보호
- ✅ `.gitignore`에 `credentials/` 추가
- ✅ `.gitignore`에 `PRIVATE_SETUP.md` 추가
- ✅ 서비스 어카운트 JSON은 절대 커밋하지 마세요!

### Google Sheets 권한
PRIVATE_SETUP.md의 서비스 어카운트 이메일을 Google Sheets에 공유:

1. https://docs.google.com/spreadsheets/d/1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk
2. 공유 버튼 클릭
3. `test-account-n8n@damoa-fb351.iam.gserviceaccount.com` 추가
4. 권한: **뷰어** 선택

---

## 🐛 트러블슈팅

### 1. PRIVATE_SETUP.md not found
```bash
# PRIVATE_SETUP.md를 프로젝트 폴더에 복사했는지 확인
ls -la PRIVATE_SETUP.md

# 관리자로부터 파일을 받아 복사
cp /path/to/PRIVATE_SETUP.md .
```

### 2. HttpError 403: Forbidden
```bash
# Google Sheet가 서비스 어카운트와 공유되었는지 확인
# test-account-n8n@damoa-fb351.iam.gserviceaccount.com 추가
```

### 3. Port 5002 already in use
```bash
# 기존 프로세스 종료 (macOS/Linux)
lsof -ti:5002 | xargs kill -9

# Windows
netstat -ano | findstr :5002
taskkill /PID <PID> /F
```

### 4. ModuleNotFoundError
```bash
# Python 의존성 재설치
pip3 install -r requirements.txt

# 또는 setup-from-private 재실행
/dana-page-builder:setup-from-private
```

---

## 📚 참고 문서

- [Google Sheets API](https://developers.google.com/sheets/api)
- [Figma Design](https://www.figma.com/design/xz6yXxIX4r2gA0TUYOkpS5/)
- [Claude Code Plugin 개발 가이드](https://docs.anthropic.com/claude-code)

---

## 📝 라이센스

MIT License

---

## 👥 지원

- **이슈**: GitHub Issues
- **이메일**: dana-team@company.com

---

**Happy Generating! 🎨**
