"""
DANA&PETA Page Builder Configuration
96-column Google Sheets structure (A~CR)
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Google Sheets Configuration
SHEET_ID = "1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk"  # DANA&PETA Products Sheet

# Unified Template System: Single "템플릿" tab
SHEET_NAME = "템플릿"  # Unified template tab
SHEET_RANGE = "A2:KP100"  # 302 columns (A~KP), up to 100 products

# Unified Template Column Definitions (템플릿 tab - 302 columns)
TEMPLATE_COLUMNS = {
    # Basic Info (columns 0-5)
    'productCode': 0,       # A - 상품코드
    'title': 1,             # B - 상품명
    'sellingPoint1': 2,     # C - 설명1
    'sellingPoint2': 3,     # D - 설명2
    'sellingPoint3': 4,     # E - 설명3
    'mdComment': 5,         # F - 추천 코멘트

    # Main Image (column 6)
    'mainImage': 6,         # G - 메인이미지_url

    # Color Names & HEX (columns 7-14)
    'color1Name': 7,        # - 색상1_이름
    'color1Hex': 8,         # - 색상1_HEX
    'color2Name': 9,        # - 색상2_이름
    'color2Hex': 10,         # - 색상2_HEX
    'color3Name': 11,        # - 색상3_이름
    'color3Hex': 12,         # - 색상3_HEX
    'color4Name': 13,        # - 색상4_이름
    'color4Hex': 14,         # - 색상4_HEX

    # Detail Points (columns 15-22)
    'detailPoint1Image': 15,    # - 디테일포인트1_url
    'detailPoint1Text': 16,     # - 디테일포인트1_설명
    'detailPoint2Image': 17,    # - 디테일포인트2_url
    'detailPoint2Text': 18,     # - 디테일포인트2_설명
    'detailPoint3Image': 19,    # - 디테일포인트3_url
    'detailPoint3Text': 20,     # - 디테일포인트3_설명
    'detailPoint4Image': 21,    # - 디테일포인트4_url
    'detailPoint4Text': 22,     # - 디테일포인트4_설명

    # Gallery Images by Color (columns 23-118)
    # Color1-8, each with 12 detail images
    'color1Gallery1': 23,  # - Color1_디테일이미지1
    'color1Gallery2': 24,  # - Color1_디테일이미지2
    'color1Gallery3': 25,  # - Color1_디테일이미지3
    'color1Gallery4': 26,  # - Color1_디테일이미지4
    'color1Gallery5': 27,  # - Color1_디테일이미지5
    'color1Gallery6': 28,  # - Color1_디테일이미지6
    'color1Gallery7': 29,  # - Color1_디테일이미지7
    'color1Gallery8': 30,  # - Color1_디테일이미지8
    'color1Gallery9': 31,  # - Color1_디테일이미지9
    'color1Gallery10': 32,  # - Color1_디테일이미지10
    'color1Gallery11': 33,  # - Color1_디테일이미지11
    'color1Gallery12': 34,  # - Color1_디테일이미지12
    'color2Gallery1': 35,  # - Color2_디테일이미지1
    'color2Gallery2': 36,  # - Color2_디테일이미지2
    'color2Gallery3': 37,  # - Color2_디테일이미지3
    'color2Gallery4': 38,  # - Color2_디테일이미지4
    'color2Gallery5': 39,  # - Color2_디테일이미지5
    'color2Gallery6': 40,  # - Color2_디테일이미지6
    'color2Gallery7': 41,  # - Color2_디테일이미지7
    'color2Gallery8': 42,  # - Color2_디테일이미지8
    'color2Gallery9': 43,  # - Color2_디테일이미지9
    'color2Gallery10': 44,  # - Color2_디테일이미지10
    'color2Gallery11': 45,  # - Color2_디테일이미지11
    'color2Gallery12': 46,  # - Color2_디테일이미지12
    'color3Gallery1': 47,  # - Color3_디테일이미지1
    'color3Gallery2': 48,  # - Color3_디테일이미지2
    'color3Gallery3': 49,  # - Color3_디테일이미지3
    'color3Gallery4': 50,  # - Color3_디테일이미지4
    'color3Gallery5': 51,  # - Color3_디테일이미지5
    'color3Gallery6': 52,  # - Color3_디테일이미지6
    'color3Gallery7': 53,  # - Color3_디테일이미지7
    'color3Gallery8': 54,  # - Color3_디테일이미지8
    'color3Gallery9': 55,  # - Color3_디테일이미지9
    'color3Gallery10': 56,  # - Color3_디테일이미지10
    'color3Gallery11': 57,  # - Color3_디테일이미지11
    'color3Gallery12': 58,  # - Color3_디테일이미지12
    'color4Gallery1': 59,  # - Color4_디테일이미지1
    'color4Gallery2': 60,  # - Color4_디테일이미지2
    'color4Gallery3': 61,  # - Color4_디테일이미지3
    'color4Gallery4': 62,  # - Color4_디테일이미지4
    'color4Gallery5': 63,  # - Color4_디테일이미지5
    'color4Gallery6': 64,  # - Color4_디테일이미지6
    'color4Gallery7': 65,  # - Color4_디테일이미지7
    'color4Gallery8': 66,  # - Color4_디테일이미지8
    'color4Gallery9': 67,  # - Color4_디테일이미지9
    'color4Gallery10': 68,  # - Color4_디테일이미지10
    'color4Gallery11': 69,  # - Color4_디테일이미지11
    'color4Gallery12': 70,  # - Color4_디테일이미지12
    'color5Gallery1': 71,  # - Color5_디테일이미지1
    'color5Gallery2': 72,  # - Color5_디테일이미지2
    'color5Gallery3': 73,  # - Color5_디테일이미지3
    'color5Gallery4': 74,  # - Color5_디테일이미지4
    'color5Gallery5': 75,  # - Color5_디테일이미지5
    'color5Gallery6': 76,  # - Color5_디테일이미지6
    'color5Gallery7': 77,  # - Color5_디테일이미지7
    'color5Gallery8': 78,  # - Color5_디테일이미지8
    'color5Gallery9': 79,  # - Color5_디테일이미지9
    'color5Gallery10': 80,  # - Color5_디테일이미지10
    'color5Gallery11': 81,  # - Color5_디테일이미지11
    'color5Gallery12': 82,  # - Color5_디테일이미지12
    'color6Gallery1': 83,  # - Color6_디테일이미지1
    'color6Gallery2': 84,  # - Color6_디테일이미지2
    'color6Gallery3': 85,  # - Color6_디테일이미지3
    'color6Gallery4': 86,  # - Color6_디테일이미지4
    'color6Gallery5': 87,  # - Color6_디테일이미지5
    'color6Gallery6': 88,  # - Color6_디테일이미지6
    'color6Gallery7': 89,  # - Color6_디테일이미지7
    'color6Gallery8': 90,  # - Color6_디테일이미지8
    'color6Gallery9': 91,  # - Color6_디테일이미지9
    'color6Gallery10': 92,  # - Color6_디테일이미지10
    'color6Gallery11': 93,  # - Color6_디테일이미지11
    'color6Gallery12': 94,  # - Color6_디테일이미지12
    'color7Gallery1': 95,  # - Color7_디테일이미지1
    'color7Gallery2': 96,  # - Color7_디테일이미지2
    'color7Gallery3': 97,  # - Color7_디테일이미지3
    'color7Gallery4': 98,  # - Color7_디테일이미지4
    'color7Gallery5': 99,  # - Color7_디테일이미지5
    'color7Gallery6': 100,  # - Color7_디테일이미지6
    'color7Gallery7': 101,  # - Color7_디테일이미지7
    'color7Gallery8': 102,  # - Color7_디테일이미지8
    'color7Gallery9': 103,  # - Color7_디테일이미지9
    'color7Gallery10': 104,  # - Color7_디테일이미지10
    'color7Gallery11': 105,  # - Color7_디테일이미지11
    'color7Gallery12': 106,  # - Color7_디테일이미지12
    'color8Gallery1': 107,  # - Color8_디테일이미지1
    'color8Gallery2': 108,  # - Color8_디테일이미지2
    'color8Gallery3': 109,  # - Color8_디테일이미지3
    'color8Gallery4': 110,  # - Color8_디테일이미지4
    'color8Gallery5': 111,  # - Color8_디테일이미지5
    'color8Gallery6': 112,  # - Color8_디테일이미지6
    'color8Gallery7': 113,  # - Color8_디테일이미지7
    'color8Gallery8': 114,  # - Color8_디테일이미지8
    'color8Gallery9': 115,  # - Color8_디테일이미지9
    'color8Gallery10': 116,  # - Color8_디테일이미지10
    'color8Gallery11': 117,  # - Color8_디테일이미지11
    'color8Gallery12': 118,  # - Color8_디테일이미지12

    # Product Shots by Color (columns 119-126)
    'color1ProductShot': 119,     # - 컬러1_상품컷_url
    'color2ProductShot': 120,     # - 컬러2_상품컷_url
    'color3ProductShot': 121,     # - 컬러3_상품컷_url
    'color4ProductShot': 122,     # - 컬러4_상품컷_url
    'color5ProductShot': 123,     # - 컬러5_상품컷_url
    'color6ProductShot': 124,     # - 컬러6_상품컷_url
    'color7ProductShot': 125,     # - 컬러7_상품컷_url
    'color8ProductShot': 126,     # - 컬러8_상품컷_url

    # Fabric Info (columns 127-134)
    'fabricImage': 127,       # DX - 소재이미지
    'fabricComposition': 128, # DY - 소재구성
    'fabricDesc': 129,        # DZ - 소재설명1
    'fabricTransparency': 130,  # EA - 비침
    'fabricStretch': 131,       # EB - 신축성
    'fabricLining': 132,        # EC - 안감
    'fabricThickness': 133,     # ED - 두께감
    'fabricSeason': 134,        # EE - 계절감

    # Size Image (column 135)
    'sizeImage': 135,         # EF - 사이즈 이미지

    # Product Info (columns 136-141)
    'productName': 136,       # EG - 제품명
    'colorName': 137,         # EH - 컬러명
    'sizeName': 138,          # EI - 사이즈
    'fabric': 139,            # EJ - 패브릭
    'washingInfo': 140,       # EK - 세탁법
    'origin': 141,            # EL - 생산지

    # Top Sizes (columns 142-221) - 10 sizes, 8 fields each
    'topSize1Name': 142,      # - 상의_사이즈_1
    'topSize1Shoulder': 143,  # - 상의_어깨너비_1
    'topSize1Chest': 144,     # - 상의_가슴둘레_1
    'topSize1Hem': 145,       # - 상의_밑단둘레_1
    'topSize1SleeveLength': 146, # - 상의_소매길이_1
    'topSize1SleeveOpening': 147, # - 상의_소매통_1
    'topSize1TotalLength': 148,  # - 상의_총장_1
    'topSize1Optional': 149,     # - 상의_옵셔널Row_1
    'topSize2Name': 150,      # - 상의_사이즈_2
    'topSize2Shoulder': 151,  # - 상의_어깨너비_2
    'topSize2Chest': 152,     # - 상의_가슴둘레_2
    'topSize2Hem': 153,       # - 상의_밑단둘레_2
    'topSize2SleeveLength': 154, # - 상의_소매길이_2
    'topSize2SleeveOpening': 155, # - 상의_소매통_2
    'topSize2TotalLength': 156,  # - 상의_총장_2
    'topSize2Optional': 157,     # - 상의_옵셔널Row_2
    'topSize3Name': 158,      # - 상의_사이즈_3
    'topSize3Shoulder': 159,  # - 상의_어깨너비_3
    'topSize3Chest': 160,     # - 상의_가슴둘레_3
    'topSize3Hem': 161,       # - 상의_밑단둘레_3
    'topSize3SleeveLength': 162, # - 상의_소매길이_3
    'topSize3SleeveOpening': 163, # - 상의_소매통_3
    'topSize3TotalLength': 164,  # - 상의_총장_3
    'topSize3Optional': 165,     # - 상의_옵셔널Row_3
    'topSize4Name': 166,      # - 상의_사이즈_4
    'topSize4Shoulder': 167,  # - 상의_어깨너비_4
    'topSize4Chest': 168,     # - 상의_가슴둘레_4
    'topSize4Hem': 169,       # - 상의_밑단둘레_4
    'topSize4SleeveLength': 170, # - 상의_소매길이_4
    'topSize4SleeveOpening': 171, # - 상의_소매통_4
    'topSize4TotalLength': 172,  # - 상의_총장_4
    'topSize4Optional': 173,     # - 상의_옵셔널Row_4
    'topSize5Name': 174,      # - 상의_사이즈_5
    'topSize5Shoulder': 175,  # - 상의_어깨너비_5
    'topSize5Chest': 176,     # - 상의_가슴둘레_5
    'topSize5Hem': 177,       # - 상의_밑단둘레_5
    'topSize5SleeveLength': 178, # - 상의_소매길이_5
    'topSize5SleeveOpening': 179, # - 상의_소매통_5
    'topSize5TotalLength': 180,  # - 상의_총장_5
    'topSize5Optional': 181,     # - 상의_옵셔널Row_5
    'topSize6Name': 182,      # - 상의_사이즈_6
    'topSize6Shoulder': 183,  # - 상의_어깨너비_6
    'topSize6Chest': 184,     # - 상의_가슴둘레_6
    'topSize6Hem': 185,       # - 상의_밑단둘레_6
    'topSize6SleeveLength': 186, # - 상의_소매길이_6
    'topSize6SleeveOpening': 187, # - 상의_소매통_6
    'topSize6TotalLength': 188,  # - 상의_총장_6
    'topSize6Optional': 189,     # - 상의_옵셔널Row_6
    'topSize7Name': 190,      # - 상의_사이즈_7
    'topSize7Shoulder': 191,  # - 상의_어깨너비_7
    'topSize7Chest': 192,     # - 상의_가슴둘레_7
    'topSize7Hem': 193,       # - 상의_밑단둘레_7
    'topSize7SleeveLength': 194, # - 상의_소매길이_7
    'topSize7SleeveOpening': 195, # - 상의_소매통_7
    'topSize7TotalLength': 196,  # - 상의_총장_7
    'topSize7Optional': 197,     # - 상의_옵셔널Row_7
    'topSize8Name': 198,      # - 상의_사이즈_8
    'topSize8Shoulder': 199,  # - 상의_어깨너비_8
    'topSize8Chest': 200,     # - 상의_가슴둘레_8
    'topSize8Hem': 201,       # - 상의_밑단둘레_8
    'topSize8SleeveLength': 202, # - 상의_소매길이_8
    'topSize8SleeveOpening': 203, # - 상의_소매통_8
    'topSize8TotalLength': 204,  # - 상의_총장_8
    'topSize8Optional': 205,     # - 상의_옵셔널Row_8
    'topSize9Name': 206,      # - 상의_사이즈_9
    'topSize9Shoulder': 207,  # - 상의_어깨너비_9
    'topSize9Chest': 208,     # - 상의_가슴둘레_9
    'topSize9Hem': 209,       # - 상의_밑단둘레_9
    'topSize9SleeveLength': 210, # - 상의_소매길이_9
    'topSize9SleeveOpening': 211, # - 상의_소매통_9
    'topSize9TotalLength': 212,  # - 상의_총장_9
    'topSize9Optional': 213,     # - 상의_옵셔널Row_9
    'topSize10Name': 214,      # - 상의_사이즈_10
    'topSize10Shoulder': 215,  # - 상의_어깨너비_10
    'topSize10Chest': 216,     # - 상의_가슴둘레_10
    'topSize10Hem': 217,       # - 상의_밑단둘레_10
    'topSize10SleeveLength': 218, # - 상의_소매길이_10
    'topSize10SleeveOpening': 219, # - 상의_소매통_10
    'topSize10TotalLength': 220,  # - 상의_총장_10
    'topSize10Optional': 221,     # - 상의_옵셔널Row_10

    # Bottom Sizes (columns 222-301) - 10 sizes, 8 fields each
    'bottomSize1Name': 222,      # - 하의_사이즈_1
    'bottomSize1Waist': 223,     # - 하의_허리둘레_1
    'bottomSize1Hip': 224,       # - 하의_엉덩이둘레_1
    'bottomSize1Thigh': 225,     # - 하의_허벅지둘레_1
    'bottomSize1Hem': 226,       # - 하의_밑단둘레_1
    'bottomSize1Rise': 227,      # - 하의_밑위길이_1
    'bottomSize1TotalLength': 228,  # - 하의_총장_1
    'bottomSize1Optional': 229,     # - 하의_옵셔널Row_1
    'bottomSize2Name': 230,      # - 하의_사이즈_2
    'bottomSize2Waist': 231,     # - 하의_허리둘레_2
    'bottomSize2Hip': 232,       # - 하의_엉덩이둘레_2
    'bottomSize2Thigh': 233,     # - 하의_허벅지둘레_2
    'bottomSize2Hem': 234,       # - 하의_밑단둘레_2
    'bottomSize2Rise': 235,      # - 하의_밑위길이_2
    'bottomSize2TotalLength': 236,  # - 하의_총장_2
    'bottomSize2Optional': 237,     # - 하의_옵셔널Row_2
    'bottomSize3Name': 238,      # - 하의_사이즈_3
    'bottomSize3Waist': 239,     # - 하의_허리둘레_3
    'bottomSize3Hip': 240,       # - 하의_엉덩이둘레_3
    'bottomSize3Thigh': 241,     # - 하의_허벅지둘레_3
    'bottomSize3Hem': 242,       # - 하의_밑단둘레_3
    'bottomSize3Rise': 243,      # - 하의_밑위길이_3
    'bottomSize3TotalLength': 244,  # - 하의_총장_3
    'bottomSize3Optional': 245,     # - 하의_옵셔널Row_3
    'bottomSize4Name': 246,      # - 하의_사이즈_4
    'bottomSize4Waist': 247,     # - 하의_허리둘레_4
    'bottomSize4Hip': 248,       # - 하의_엉덩이둘레_4
    'bottomSize4Thigh': 249,     # - 하의_허벅지둘레_4
    'bottomSize4Hem': 250,       # - 하의_밑단둘레_4
    'bottomSize4Rise': 251,      # - 하의_밑위길이_4
    'bottomSize4TotalLength': 252,  # - 하의_총장_4
    'bottomSize4Optional': 253,     # - 하의_옵셔널Row_4
    'bottomSize5Name': 254,      # - 하의_사이즈_5
    'bottomSize5Waist': 255,     # - 하의_허리둘레_5
    'bottomSize5Hip': 256,       # - 하의_엉덩이둘레_5
    'bottomSize5Thigh': 257,     # - 하의_허벅지둘레_5
    'bottomSize5Hem': 258,       # - 하의_밑단둘레_5
    'bottomSize5Rise': 259,      # - 하의_밑위길이_5
    'bottomSize5TotalLength': 260,  # - 하의_총장_5
    'bottomSize5Optional': 261,     # - 하의_옵셔널Row_5
    'bottomSize6Name': 262,      # - 하의_사이즈_6
    'bottomSize6Waist': 263,     # - 하의_허리둘레_6
    'bottomSize6Hip': 264,       # - 하의_엉덩이둘레_6
    'bottomSize6Thigh': 265,     # - 하의_허벅지둘레_6
    'bottomSize6Hem': 266,       # - 하의_밑단둘레_6
    'bottomSize6Rise': 267,      # - 하의_밑위길이_6
    'bottomSize6TotalLength': 268,  # - 하의_총장_6
    'bottomSize6Optional': 269,     # - 하의_옵셔널Row_6
    'bottomSize7Name': 270,      # - 하의_사이즈_7
    'bottomSize7Waist': 271,     # - 하의_허리둘레_7
    'bottomSize7Hip': 272,       # - 하의_엉덩이둘레_7
    'bottomSize7Thigh': 273,     # - 하의_허벅지둘레_7
    'bottomSize7Hem': 274,       # - 하의_밑단둘레_7
    'bottomSize7Rise': 275,      # - 하의_밑위길이_7
    'bottomSize7TotalLength': 276,  # - 하의_총장_7
    'bottomSize7Optional': 277,     # - 하의_옵셔널Row_7
    'bottomSize8Name': 278,      # - 하의_사이즈_8
    'bottomSize8Waist': 279,     # - 하의_허리둘레_8
    'bottomSize8Hip': 280,       # - 하의_엉덩이둘레_8
    'bottomSize8Thigh': 281,     # - 하의_허벅지둘레_8
    'bottomSize8Hem': 282,       # - 하의_밑단둘레_8
    'bottomSize8Rise': 283,      # - 하의_밑위길이_8
    'bottomSize8TotalLength': 284,  # - 하의_총장_8
    'bottomSize8Optional': 285,     # - 하의_옵셔널Row_8
    'bottomSize9Name': 286,      # - 하의_사이즈_9
    'bottomSize9Waist': 287,     # - 하의_허리둘레_9
    'bottomSize9Hip': 288,       # - 하의_엉덩이둘레_9
    'bottomSize9Thigh': 289,     # - 하의_허벅지둘레_9
    'bottomSize9Hem': 290,       # - 하의_밑단둘레_9
    'bottomSize9Rise': 291,      # - 하의_밑위길이_9
    'bottomSize9TotalLength': 292,  # - 하의_총장_9
    'bottomSize9Optional': 293,     # - 하의_옵셔널Row_9
    'bottomSize10Name': 294,      # - 하의_사이즈_10
    'bottomSize10Waist': 295,     # - 하의_허리둘레_10
    'bottomSize10Hip': 296,       # - 하의_엉덩이둘레_10
    'bottomSize10Thigh': 297,     # - 하의_허벅지둘레_10
    'bottomSize10Hem': 298,       # - 하의_밑단둘레_10
    'bottomSize10Rise': 299,      # - 하의_밑위길이_10
    'bottomSize10TotalLength': 300,  # - 하의_총장_10
    'bottomSize10Optional': 301,     # - 하의_옵셔널Row_10
}

SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "credentials" / "service-account.json"

# API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

# Output Directories
OUTPUT_DIR = PROJECT_ROOT / "output"
ASSETS_DIR = OUTPUT_DIR / "assets" / "images"
EXPORTS_DIR = PROJECT_ROOT / "exports"
STANDALONE_EXPORTS_DIR = EXPORTS_DIR / "standalone"
IMAGES_EXPORTS_DIR = EXPORTS_DIR / "images"

# Data Files
DATA_DIR = PROJECT_ROOT / "data"
PRODUCTS_DATA_PATH = DATA_DIR / "products.json"
TEMPLATE_PATH = DATA_DIR / "templates" / "dana_product_template.json"

# Logging Configuration
LOG_FILE = PROJECT_ROOT / "dana_page_generation.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# HTML Template Settings
BRAND_NAME = "DANA&PETA"
BRAND_LOGO_TEXT = "queenit made"

# Image Processing Settings
COLOR_EXTRACTION_CROP_PERCENT = 0.3  # Center crop 30%
COLOR_EXTRACTION_BRIGHTNESS_THRESHOLD = 240  # Filter out bright pixels
COLOR_EXTRACTION_KMEANS_CLUSTERS = 3  # Number of K-means clusters
COLOR_EXTRACTION_KMEANS_ITERATIONS = 10  # Max iterations

# Date format for output folders
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y%m%d_%H%M%S"

# Folder names
ORIGINAL_FOLDER = "원본"
EDITABLE_FOLDER = "에디터블"
EXPORT_FOLDER = "익스포트"

# File naming patterns
ORIGINAL_FILE_PATTERN = "{productCode}.html"
EDITABLE_FILE_PATTERN = "{productCode}_editable.html"
STANDALONE_FILE_PATTERN = "{productCode}_standalone_{timestamp}.html"
IMAGE_FILE_PATTERN = "{productCode}_{timestamp}.jpg"

# Validation settings
REQUIRED_FIELDS = ["productCode", "title", "mainImage"]

# Export settings
STANDALONE_QUALITY = 85  # Base64 quality
IMAGE_QUALITY = 85  # JPG quality for exports
IMAGE_VIEWPORT_WIDTH = 360  # Mobile viewport width

# Version
VERSION = "1.0.0"
