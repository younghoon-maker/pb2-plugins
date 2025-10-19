# Google Sheets 스키마 (294 Columns)

본 문서는 제품 데이터를 입력하기 위한 Google Sheets의 294개 컬럼 구조를 상세히 설명합니다.

---

## 목차

1. [스키마 개요](#스키마-개요)
2. [컬럼 구조](#컬럼-구조)
3. [카테고리별 상세](#카테고리별-상세)
4. [데이터 입력 가이드](#데이터-입력-가이드)
5. [예시 데이터](#예시-데이터)
6. [검증 규칙](#검증-규칙)

---

## 스키마 개요

### 전체 통계

- **총 컬럼 수**: 294개 (A~KN)
- **필수 컬럼**: 약 50개
- **선택 컬럼**: 약 244개
- **이미지 컬럼**: 약 150개

### 컬럼 범위 요약

| 범위 | 카테고리 | 컬럼 수 | 설명 |
|------|----------|--------|------|
| A~C | 기본 정보 | 3 | 제품 코드, 제품명, 메인 이미지 |
| D~I | 색상 이미지 | 6 | 6개 색상 이미지 |
| J~U | 색상 메타데이터 | 12 | 6개 색상 × 2필드 (이름, HEX) |
| V~DR | 갤러리 | 96 | 8개 색상 × 12개 이미지 |
| DS~DX | 디테일 포인트 | 6 | 3개 포인트 × 2필드 (이미지, 텍스트) |
| DY~EA | 소재 정보 | 3 | 이미지, 구성, 관리 |
| EB~EC | 체크포인트 | 2 | 이미지, 텍스트 |
| ED~EI | 모델 정보 | 6 | 2개 모델 × 3필드 (이미지, 신장, 사이즈) |
| EJ~HM | 상의 사이즈 | 80 | 10개 사이즈 × 8필드 |
| HN~KN | 하의 사이즈 | 80 | 10개 사이즈 × 8필드 |

---

## 컬럼 구조

### 1. 기본 정보 (A~C, 3 columns)

| Excel | Index | 필드명 | 타입 | 필수 | 설명 | 예시 |
|-------|-------|--------|------|------|------|------|
| A | 0 | product_code | String | ✅ | 제품 코드 | VD25FCA004 |
| B | 1 | product_name | String | ✅ | 제품명 | 플리츠 롱 스커트 |
| C | 2 | main_image | URL | ✅ | 메인 이미지 (하이퍼링크) | Google Drive URL |

### 2. 색상 이미지 (D~I, 6 columns)

| Excel | Index | 필드명 | 타입 | 필수 | 설명 | 예시 |
|-------|-------|--------|------|------|------|------|
| D | 3 | color1_image | URL | ⚠️ | 색상 1 이미지 (하이퍼링크) | Google Drive URL |
| E | 4 | color2_image | URL | ⚠️ | 색상 2 이미지 | Google Drive URL |
| F | 5 | color3_image | URL | ⚠️ | 색상 3 이미지 | Google Drive URL |
| G | 6 | color4_image | URL | ⚠️ | 색상 4 이미지 | Google Drive URL |
| H | 7 | color5_image | URL | ⚠️ | 색상 5 이미지 | Google Drive URL |
| I | 8 | color6_image | URL | ⚠️ | 색상 6 이미지 | Google Drive URL |

### 3. 색상 메타데이터 (J~U, 12 columns)

각 색상마다 2개 필드 (이름, HEX 코드)

| Excel | Index | 필드명 | 타입 | 필수 | 설명 | 예시 |
|-------|-------|--------|------|------|------|------|
| J | 9 | color1_name | String | ⚠️ | 색상 1 이름 | 베이지 |
| K | 10 | color1_hex | String | ⚠️ | 색상 1 HEX 코드 | #D4C5B8 |
| L | 11 | color2_name | String | ⚠️ | 색상 2 이름 | 블랙 |
| M | 12 | color2_hex | String | ⚠️ | 색상 2 HEX 코드 | #2B2B2B |
| ... | ... | ... | ... | ... | ... | ... |
| T | 19 | color6_name | String | ⚠️ | 색상 6 이름 | 그레이 |
| U | 20 | color6_hex | String | ⚠️ | 색상 6 HEX 코드 | #A8A8A8 |

### 4. 갤러리 (V~DR, 96 columns)

8개 색상 × 12개 이미지 = 96 컬럼

**색상 1 갤러리** (V~AG, 12 columns):
| Excel | Index | 필드명 | 타입 | 필수 | 설명 |
|-------|-------|--------|------|------|------|
| V | 21 | color1_gallery1 | URL | ⚠️ | 색상 1 갤러리 이미지 1 |
| W | 22 | color1_gallery2 | URL | ⚠️ | 색상 1 갤러리 이미지 2 |
| ... | ... | ... | ... | ... | ... |
| AG | 32 | color1_gallery12 | URL | ⚠️ | 색상 1 갤러리 이미지 12 |

**색상 2~8 갤러리** (AH~DR, 84 columns):
- 각 색상마다 12개 이미지
- 색상 2: AH~AS (33~44)
- 색상 3: AT~BE (45~56)
- 색상 4: BF~BQ (57~68)
- 색상 5: BR~CC (69~80)
- 색상 6: CD~CO (81~92)
- 색상 7: CP~DA (93~104)
- 색상 8: DB~DM (105~116)

### 5. 디테일 포인트 (DS~DX, 6 columns)

3개 포인트 × 2필드 (이미지, 텍스트)

| Excel | Index | 필드명 | 타입 | 필수 | 설명 | 예시 |
|-------|-------|--------|------|------|------|------|
| DS | 117 | detail_point1_image | URL | ⚠️ | 디테일 포인트 1 이미지 | Google Drive URL |
| DT | 118 | detail_point1_text | String | ⚠️ | 디테일 포인트 1 설명 | 깔끔한 라인 |
| DU | 119 | detail_point2_image | URL | ⚠️ | 디테일 포인트 2 이미지 | Google Drive URL |
| DV | 120 | detail_point2_text | String | ⚠️ | 디테일 포인트 2 설명 | 편안한 착용감 |
| DW | 121 | detail_point3_image | URL | ⚠️ | 디테일 포인트 3 이미지 | Google Drive URL |
| DX | 122 | detail_point3_text | String | ⚠️ | 디테일 포인트 3 설명 | 다양한 스타일링 |

### 6. 소재 정보 (DY~EA, 3 columns)

| Excel | Index | 필드명 | 타입 | 필수 | 설명 | 예시 |
|-------|-------|--------|------|------|------|------|
| DY | 123 | fabric_image | URL | ⚠️ | 소재 이미지 | Google Drive URL |
| DZ | 124 | fabric_composition | String | ⚠️ | 소재 구성 | 폴리에스터 100% |
| EA | 125 | fabric_care | String | ⚠️ | 관리 방법 | 손세탁 권장 |

### 7. 체크포인트 (EB~EC, 2 columns)

| Excel | Index | 필드명 | 타입 | 필수 | 설명 | 예시 |
|-------|-------|--------|------|------|------|------|
| EB | 126 | checkpoint_image | URL | ❌ | 체크포인트 이미지 | Google Drive URL |
| EC | 127 | checkpoint_text | String | ❌ | 체크포인트 텍스트 | 주의사항 |

### 8. 모델 정보 (ED~EI, 6 columns)

2개 모델 × 3필드 (이미지, 신장, 사이즈)

| Excel | Index | 필드명 | 타입 | 필수 | 설명 | 예시 |
|-------|-------|--------|------|------|------|------|
| ED | 128 | model1_image | URL | ❌ | 모델 1 이미지 | Google Drive URL |
| EE | 129 | model1_height | String | ❌ | 모델 1 신장 | 168cm |
| EF | 130 | model1_size | String | ❌ | 모델 1 착용 사이즈 | FREE |
| EG | 131 | model2_image | URL | ❌ | 모델 2 이미지 | Google Drive URL |
| EH | 132 | model2_height | String | ❌ | 모델 2 신장 | 173cm |
| EI | 133 | model2_size | String | ❌ | 모델 2 착용 사이즈 | FREE |

### 9. 상의 사이즈 (EJ~HM, 80 columns)

10개 사이즈 × 8필드 = 80 컬럼

**각 사이즈 필드** (8 columns):
| Offset | 필드명 | 타입 | 설명 | 예시 |
|--------|--------|------|------|------|
| +0 | size_name | String | 사이즈명 | S, M, L, FREE |
| +1 | shoulder | String | 어깨너비 (cm) | 42 |
| +2 | chest | String | 가슴둘레 (cm) | 92 |
| +3 | hem | String | 밑단둘레 (cm) | 88 |
| +4 | sleeve | String | 소매길이 (cm) | 58 |
| +5 | sleeve_cuff | String | 소매통 (cm) | 30 |
| +6 | length | String | 총장 (cm) | 65 |
| +7 | optional | String | 옵셔널 (무시) | - |

**사이즈 1** (EJ~EQ):
| Excel | Index | 필드명 | 예시 |
|-------|-------|--------|------|
| EJ | 134 | top_size1_name | FREE |
| EK | 135 | top_size1_shoulder | 42 |
| EL | 136 | top_size1_chest | 92 |
| EM | 137 | top_size1_hem | 88 |
| EN | 138 | top_size1_sleeve | 58 |
| EO | 139 | top_size1_sleeve_cuff | 30 |
| EP | 140 | top_size1_length | 65 |
| EQ | 141 | top_size1_optional | - |

**사이즈 2~10** (ER~HM):
- 각 사이즈마다 8개 필드
- 사이즈 2: ER~EY (142~149)
- 사이즈 3: EZ~FG (150~157)
- ...
- 사이즈 10: HF~HM (206~213)

### 10. 하의 사이즈 (HN~KN, 80 columns)

10개 사이즈 × 8필드 = 80 컬럼

**각 사이즈 필드** (8 columns):
| Offset | 필드명 | 타입 | 설명 | 예시 |
|--------|--------|------|------|------|
| +0 | size_name | String | 사이즈명 | S, M, L, FREE |
| +1 | waist | String | 허리둘레 (cm) | 64 |
| +2 | hip | String | 엉덩이둘레 (cm) | 94 |
| +3 | thigh | String | 허벅지둘레 (cm) | 60 |
| +4 | hem | String | 밑단둘레 (cm) | 40 |
| +5 | rise | String | 밑위길이 (cm) | 28 |
| +6 | length | String | 총장 (cm) | 98 |
| +7 | optional | String | 옵셔널 (무시) | - |

**사이즈 1** (HN~HU):
| Excel | Index | 필드명 | 예시 |
|-------|-------|--------|------|
| HN | 214 | bottom_size1_name | FREE |
| HO | 215 | bottom_size1_waist | 64 |
| HP | 216 | bottom_size1_hip | 94 |
| HQ | 217 | bottom_size1_thigh | 60 |
| HR | 218 | bottom_size1_hem | 40 |
| HS | 219 | bottom_size1_rise | 28 |
| HT | 220 | bottom_size1_length | 98 |
| HU | 221 | bottom_size1_optional | - |

**사이즈 2~10** (HV~KN):
- 각 사이즈마다 8개 필드
- 사이즈 2: HV~IC (222~229)
- 사이즈 3: ID~IK (230~237)
- ...
- 사이즈 10: KG~KN (286~293)

---

## 카테고리별 상세

### 필수 필드

반드시 입력해야 하는 필드:
1. **제품 코드** (A): 고유 식별자
2. **제품명** (B): 제품 이름
3. **메인 이미지** (C): 대표 이미지

**최소 1개 색상 정보**:
- 색상 이미지 (D)
- 색상명 (J)
- 색상 HEX 코드 (K)

### 선택 필드

입력하지 않으면 HTML에서 제외되는 필드:
- 색상 2~6 정보
- 갤러리 이미지
- 디테일 포인트
- 소재 정보
- 체크포인트
- 모델 정보
- 사이즈 정보

### 이미지 필드 입력 방법

**Google Drive 하이퍼링크 사용**:

1. Google Drive에 이미지 업로드
2. 이미지 우클릭 → **링크 가져오기**
3. **링크 복사**
4. Google Sheets 셀에서:
   - 셀 우클릭 → **링크 삽입** (또는 Ctrl+K)
   - URL 붙여넣기
   - 셀 텍스트는 `이미지` 또는 파일명

**예시**:
```
표시 텍스트: 이미지
링크 URL: https://drive.google.com/file/d/1abc...xyz/view?usp=sharing
```

---

## 데이터 입력 가이드

### 1. 제품 코드 규칙

**형식**: `{브랜드코드}{시즌}{카테고리}{일련번호}`

**예시**:
- `VD25FCA004`: Vendor 2025 Fall Casual 004
- `VD25FPT003`: Vendor 2025 Fall Pants 003
- `VD25FDP013`: Vendor 2025 Fall Dress 013

### 2. HEX 코드 규칙

**형식**: `#RRGGBB` (6자리 16진수)

**예시**:
- `#D4C5B8` (베이지)
- `#2B2B2B` (블랙)
- `#FFFFFF` (화이트)

**자동 추출**:
- HEX 코드를 비워두면 색상 이미지에서 자동 추출
- K-means 알고리즘 사용 (정확도 높음)

### 3. 사이즈 입력 규칙

**단위**: cm (센티미터)
**형식**: 정수 또는 소수점 1자리

**예시**:
- `42` (정수)
- `42.5` (소수점)
- `FREE` (원사이즈)

**비어있는 사이즈**:
- 사이즈명이 비어있으면 해당 사이즈는 제외
- 예: 사이즈 1~3만 입력하면 3개 사이즈만 표시

---

## 예시 데이터

### 예시 1: 상의 (니트)

| 컬럼 | 값 | 비고 |
|------|-----|------|
| A | VD25FKN001 | 제품 코드 |
| B | 케이블 라운드넥 니트 | 제품명 |
| C | [이미지](drive.google.com/...) | 메인 이미지 |
| D | [이미지](drive.google.com/...) | 색상 1 이미지 (베이지) |
| E | [이미지](drive.google.com/...) | 색상 2 이미지 (블랙) |
| J | 베이지 | 색상 1 이름 |
| K | #D4C5B8 | 색상 1 HEX |
| L | 블랙 | 색상 2 이름 |
| M | #2B2B2B | 색상 2 HEX |
| ... | ... | 갤러리 생략 |
| EJ | FREE | 상의 사이즈 1 이름 |
| EK | 42 | 어깨너비 |
| EL | 92 | 가슴둘레 |
| ... | ... | ... |

### 예시 2: 하의 (스커트)

| 컬럼 | 값 | 비고 |
|------|-----|------|
| A | VD25FSK002 | 제품 코드 |
| B | 플리츠 롱 스커트 | 제품명 |
| C | [이미지](drive.google.com/...) | 메인 이미지 |
| D | [이미지](drive.google.com/...) | 색상 1 이미지 (네이비) |
| J | 네이비 | 색상 1 이름 |
| K | #1A1A3C | 색상 1 HEX |
| ... | ... | 갤러리 생략 |
| HN | FREE | 하의 사이즈 1 이름 |
| HO | 64 | 허리둘레 |
| HP | 94 | 엉덩이둘레 |
| HQ | 60 | 허벅지둘레 |
| HR | 40 | 밑단둘레 |
| HS | 28 | 밑위길이 |
| HT | 98 | 총장 |

---

## 검증 규칙

### 자동 검증

스크립트 실행 시 자동으로 검증:

1. **필수 필드**: 제품 코드, 제품명, 메인 이미지
2. **색상 일관성**: 이미지가 있으면 이름도 필수
3. **HEX 코드 형식**: `#` + 6자리 16진수
4. **이미지 URL**: Google Drive 링크 형식
5. **사이즈 값**: 숫자 또는 `FREE`

### 경고 메시지

```
⚠️ Warning: Product VD25FCA004
   - Color 2 image exists but name is missing
   - Gallery color 1: Only 5 images (expected 12)
```

### 오류 메시지

```
❌ Error: Product VD25FCA004
   - Missing required field: product_code
   - Invalid HEX code: #GGGGGG (must be 6-digit hex)
   - Image URL not accessible: https://drive.google.com/...
```

---

## 비교: 96 vs 294 Columns

### Dana & Peta (96 columns)
- 4개 색상 지원
- 갤러리: 고정 8개
- 디테일 포인트: 4개
- 사이즈: 상/하의 각 1개

### 현재 시스템 (294 columns)
- **6개 색상** 지원 (50% 증가)
- **갤러리: 8색상 × 12개** = 96개 (10배 증가)
- **디테일 포인트**: 3개
- **사이즈: 상/하의 각 10개** (10배 증가)
- **체크포인트, 모델 정보** 추가

---

## 다음 단계

스키마를 익혔다면:

1. **Google Sheets 템플릿 생성**: 294개 컬럼 헤더 작성
2. **샘플 데이터 입력**: 1개 제품으로 테스트
3. **HTML 생성**: `examples/generate_figma_editable_v4.py` 실행
4. **워크플로우 확인**: [USAGE_GUIDE.md](USAGE_GUIDE.md) 참조

---

## 참고 자료

- [README.md](../README.md) - 프로젝트 개요
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Google Cloud 설정
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 4단계 워크플로우
- [column_mapping.py](../src/sheets_loader/column_mapping.py) - 컬럼 인덱스 매핑 코드

---

**최종 업데이트**: 2025-10-16
**작성자**: MoAI-ADK
**스키마 버전**: v1.0.0
