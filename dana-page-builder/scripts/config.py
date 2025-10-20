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
    'productCode': 0,
    'title': 1,
    'sellingPoint1': 2,
    'sellingPoint2': 3,
    'sellingPoint3': 4,
    'sellingPoint4': 5,
    'mdComment': 6,
    'mainImage': 7,
    'color1Name': 8,
    'color1Hex': 9,
    'color2Name': 10,
    'color2Hex': 11,
    'color3Name': 12,
    'color3Hex': 13,
    'color4Name': 14,
    'color4Hex': 15,
    'detailPoint1Image': 16,
    'detailPoint1Text': 17,
    'detailPoint2Image': 18,
    'detailPoint2Text': 19,
    'detailPoint3Image': 20,
    'detailPoint3Text': 21,
    'detailPoint4Image': 22,
    'detailPoint4Text': 23,
    'color1Gallery1': 24,
    'color1Gallery2': 25,
    'color1Gallery3': 26,
    'color1Gallery4': 27,
    'color1Gallery5': 28,
    'color1Gallery6': 29,
    'color1Gallery7': 30,
    'color1Gallery8': 31,
    'color1Gallery9': 32,
    'color1Gallery10': 33,
    'color1Gallery11': 34,
    'color1Gallery12': 35,
    'color2Gallery1': 36,
    'color2Gallery2': 37,
    'color2Gallery3': 38,
    'color2Gallery4': 39,
    'color2Gallery5': 40,
    'color2Gallery6': 41,
    'color2Gallery7': 42,
    'color2Gallery8': 43,
    'color2Gallery9': 44,
    'color2Gallery10': 45,
    'color2Gallery11': 46,
    'color2Gallery12': 47,
    'color3Gallery1': 48,
    'color3Gallery2': 49,
    'color3Gallery3': 50,
    'color3Gallery4': 51,
    'color3Gallery5': 52,
    'color3Gallery6': 53,
    'color3Gallery7': 54,
    'color3Gallery8': 55,
    'color3Gallery9': 56,
    'color3Gallery10': 57,
    'color3Gallery11': 58,
    'color3Gallery12': 59,
    'color4Gallery1': 60,
    'color4Gallery2': 61,
    'color4Gallery3': 62,
    'color4Gallery4': 63,
    'color4Gallery5': 64,
    'color4Gallery6': 65,
    'color4Gallery7': 66,
    'color4Gallery8': 67,
    'color4Gallery9': 68,
    'color4Gallery10': 69,
    'color4Gallery11': 70,
    'color4Gallery12': 71,
    'color5Gallery1': 72,
    'color5Gallery2': 73,
    'color5Gallery3': 74,
    'color5Gallery4': 75,
    'color5Gallery5': 76,
    'color5Gallery6': 77,
    'color5Gallery7': 78,
    'color5Gallery8': 79,
    'color5Gallery9': 80,
    'color5Gallery10': 81,
    'color5Gallery11': 82,
    'color5Gallery12': 83,
    'color6Gallery1': 84,
    'color6Gallery2': 85,
    'color6Gallery3': 86,
    'color6Gallery4': 87,
    'color6Gallery5': 88,
    'color6Gallery6': 89,
    'color6Gallery7': 90,
    'color6Gallery8': 91,
    'color6Gallery9': 92,
    'color6Gallery10': 93,
    'color6Gallery11': 94,
    'color6Gallery12': 95,
    'color7Gallery1': 96,
    'color7Gallery2': 97,
    'color7Gallery3': 98,
    'color7Gallery4': 99,
    'color7Gallery5': 100,
    'color7Gallery6': 101,
    'color7Gallery7': 102,
    'color7Gallery8': 103,
    'color7Gallery9': 104,
    'color7Gallery10': 105,
    'color7Gallery11': 106,
    'color7Gallery12': 107,
    'color8Gallery1': 108,
    'color8Gallery2': 109,
    'color8Gallery3': 110,
    'color8Gallery4': 111,
    'color8Gallery5': 112,
    'color8Gallery6': 113,
    'color8Gallery7': 114,
    'color8Gallery8': 115,
    'color8Gallery9': 116,
    'color8Gallery10': 117,
    'color8Gallery11': 118,
    'color8Gallery12': 119,
    'color1ProductShot': 120,
    'color2ProductShot': 121,
    'color3ProductShot': 122,
    'color4ProductShot': 123,
    'color5ProductShot': 124,
    'color6ProductShot': 125,
    'color7ProductShot': 126,
    'color8ProductShot': 127,
    'fabricImage': 128,
    'fabricComposition': 129,
    'fabricDesc': 130,
    'fabricTransparency': 131,
    'fabricStretch': 132,
    'fabricLining': 133,
    'fabricThickness': 134,
    'fabricSeason': 135,
    'sizeImage': 136,
    'productName': 137,
    'colorName': 138,
    'sizeName': 139,
    'fabric': 140,
    'washingInfo': 141,
    'origin': 142,
    'topSize1Name': 143,
    'topSize1Shoulder': 144,
    'topSize1Chest': 145,
    'topSize1Hem': 146,
    'topSize1SleeveLength': 147,
    'topSize1SleeveOpening': 148,
    'topSize1TotalLength': 149,
    'topSize1Optional': 150,
    'topSize2Name': 151,
    'topSize2Shoulder': 152,
    'topSize2Chest': 153,
    'topSize2Hem': 154,
    'topSize2SleeveLength': 155,
    'topSize2SleeveOpening': 156,
    'topSize2TotalLength': 157,
    'topSize2Optional': 158,
    'topSize3Name': 159,
    'topSize3Shoulder': 160,
    'topSize3Chest': 161,
    'topSize3Hem': 162,
    'topSize3SleeveLength': 163,
    'topSize3SleeveOpening': 164,
    'topSize3TotalLength': 165,
    'topSize3Optional': 166,
    'topSize4Name': 167,
    'topSize4Shoulder': 168,
    'topSize4Chest': 169,
    'topSize4Hem': 170,
    'topSize4SleeveLength': 171,
    'topSize4SleeveOpening': 172,
    'topSize4TotalLength': 173,
    'topSize4Optional': 174,
    'topSize5Name': 175,
    'topSize5Shoulder': 176,
    'topSize5Chest': 177,
    'topSize5Hem': 178,
    'topSize5SleeveLength': 179,
    'topSize5SleeveOpening': 180,
    'topSize5TotalLength': 181,
    'topSize5Optional': 182,
    'topSize6Name': 183,
    'topSize6Shoulder': 184,
    'topSize6Chest': 185,
    'topSize6Hem': 186,
    'topSize6SleeveLength': 187,
    'topSize6SleeveOpening': 188,
    'topSize6TotalLength': 189,
    'topSize6Optional': 190,
    'topSize7Name': 191,
    'topSize7Shoulder': 192,
    'topSize7Chest': 193,
    'topSize7Hem': 194,
    'topSize7SleeveLength': 195,
    'topSize7SleeveOpening': 196,
    'topSize7TotalLength': 197,
    'topSize7Optional': 198,
    'topSize8Name': 199,
    'topSize8Shoulder': 200,
    'topSize8Chest': 201,
    'topSize8Hem': 202,
    'topSize8SleeveLength': 203,
    'topSize8SleeveOpening': 204,
    'topSize8TotalLength': 205,
    'topSize8Optional': 206,
    'topSize9Name': 207,
    'topSize9Shoulder': 208,
    'topSize9Chest': 209,
    'topSize9Hem': 210,
    'topSize9SleeveLength': 211,
    'topSize9SleeveOpening': 212,
    'topSize9TotalLength': 213,
    'topSize9Optional': 214,
    'topSize10Name': 215,
    'topSize10Shoulder': 216,
    'topSize10Chest': 217,
    'topSize10Hem': 218,
    'topSize10SleeveLength': 219,
    'topSize10SleeveOpening': 220,
    'topSize10TotalLength': 221,
    'topSize10Optional': 222,
    'bottomSize1Name': 223,
    'bottomSize1Waist': 224,
    'bottomSize1Hip': 225,
    'bottomSize1Thigh': 226,
    'bottomSize1Hem': 227,
    'bottomSize1Rise': 228,
    'bottomSize1TotalLength': 229,
    'bottomSize1Optional': 230,
    'bottomSize2Name': 231,
    'bottomSize2Waist': 232,
    'bottomSize2Hip': 233,
    'bottomSize2Thigh': 234,
    'bottomSize2Hem': 235,
    'bottomSize2Rise': 236,
    'bottomSize2TotalLength': 237,
    'bottomSize2Optional': 238,
    'bottomSize3Name': 239,
    'bottomSize3Waist': 240,
    'bottomSize3Hip': 241,
    'bottomSize3Thigh': 242,
    'bottomSize3Hem': 243,
    'bottomSize3Rise': 244,
    'bottomSize3TotalLength': 245,
    'bottomSize3Optional': 246,
    'bottomSize4Name': 247,
    'bottomSize4Waist': 248,
    'bottomSize4Hip': 249,
    'bottomSize4Thigh': 250,
    'bottomSize4Hem': 251,
    'bottomSize4Rise': 252,
    'bottomSize4TotalLength': 253,
    'bottomSize4Optional': 254,
    'bottomSize5Name': 255,
    'bottomSize5Waist': 256,
    'bottomSize5Hip': 257,
    'bottomSize5Thigh': 258,
    'bottomSize5Hem': 259,
    'bottomSize5Rise': 260,
    'bottomSize5TotalLength': 261,
    'bottomSize5Optional': 262,
    'bottomSize6Name': 263,
    'bottomSize6Waist': 264,
    'bottomSize6Hip': 265,
    'bottomSize6Thigh': 266,
    'bottomSize6Hem': 267,
    'bottomSize6Rise': 268,
    'bottomSize6TotalLength': 269,
    'bottomSize6Optional': 270,
    'bottomSize7Name': 271,
    'bottomSize7Waist': 272,
    'bottomSize7Hip': 273,
    'bottomSize7Thigh': 274,
    'bottomSize7Hem': 275,
    'bottomSize7Rise': 276,
    'bottomSize7TotalLength': 277,
    'bottomSize7Optional': 278,
    'bottomSize8Name': 279,
    'bottomSize8Waist': 280,
    'bottomSize8Hip': 281,
    'bottomSize8Thigh': 282,
    'bottomSize8Hem': 283,
    'bottomSize8Rise': 284,
    'bottomSize8TotalLength': 285,
    'bottomSize8Optional': 286,
    'bottomSize9Name': 287,
    'bottomSize9Waist': 288,
    'bottomSize9Hip': 289,
    'bottomSize9Thigh': 290,
    'bottomSize9Hem': 291,
    'bottomSize9Rise': 292,
    'bottomSize9TotalLength': 293,
    'bottomSize9Optional': 294,
    'bottomSize10Name': 295,
    'bottomSize10Waist': 296,
    'bottomSize10Hip': 297,
    'bottomSize10Thigh': 298,
    'bottomSize10Hem': 299,
    'bottomSize10Rise': 300,
    'bottomSize10TotalLength': 301,
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
