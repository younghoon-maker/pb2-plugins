#!/bin/bash
# PB Product Generator - Automatic Setup Script
# Version: 0.2.1

set -e  # 오류 발생 시 즉시 종료

echo "🚀 PB Product Generator Setup"
echo "================================"
echo ""

# 색상 코드
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 현재 디렉토리 (플러그인 루트)
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PLUGIN_DIR"

echo "📂 Plugin directory: $PLUGIN_DIR"
echo ""

# Auto-detect PRIVATE_SETUP.md with JSON and delegate to Python script
if [ -f "PRIVATE_SETUP.md" ]; then
    # Check if PRIVATE_SETUP.md contains JSON blocks (```json)
    if grep -q '```json' "PRIVATE_SETUP.md"; then
        echo -e "${GREEN}📋 PRIVATE_SETUP.md with Service Account JSON detected${NC}"
        echo "   Delegating to auto_setup.py for full parsing..."
        echo ""

        # Run Python auto setup script
        if command -v python3 &> /dev/null; then
            python3 "$PLUGIN_DIR/scripts/auto_setup.py"
            exit $?
        else
            echo -e "${RED}❌ python3 not found${NC}"
            echo "   Please install Python 3 to use auto setup"
            exit 1
        fi
    fi
fi

# Step 1: credentials 폴더 확인
echo "Step 1/4: Checking credentials..."
if [ -d "credentials" ]; then
    echo -e "${GREEN}✅ Credentials directory exists${NC}"
else
    echo -e "${YELLOW}⚠️  Creating credentials directory...${NC}"
    mkdir -p credentials
    echo -e "${GREEN}✅ Created credentials/${NC}"
fi

# Step 2: 서비스 어카운트 파일 확인
if [ -f "credentials/service-account.json" ]; then
    echo -e "${GREEN}✅ Service Account file found${NC}"
    # 서비스 어카운트 이메일 확인
    EMAIL=$(python3 -c "import json; data = json.load(open('credentials/service-account.json')); print(data['client_email'])" 2>/dev/null || echo "unknown")
    echo "   Account: $EMAIL"
else
    echo -e "${RED}❌ Service Account file NOT found${NC}"
    echo ""
    echo "Please create credentials/service-account.json"
    echo "See PRIVATE_SETUP.md Step 2.2 for instructions"
    exit 1
fi
echo ""

# Step 3: PRIVATE_SETUP.md에서 설정 읽기 (있는 경우)
echo "Step 2/4: Loading configuration..."

# 기본값
SERVICE_ACCOUNT_FILE="credentials/service-account.json"
GOOGLE_SHEET_ID="1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk"
SHEET_TAB_NAME="new_raw"
FLASK_PORT="5001"
OUTPUT_DIR="output"

# PRIVATE_SETUP.md 파일이 있으면 읽기
if [ -f "PRIVATE_SETUP.md" ]; then
    echo -e "${GREEN}📋 PRIVATE_SETUP.md 파일 발견, 설정 적용 중...${NC}"

    # 각 설정값 추출 (주석이 아닌 KEY=VALUE 형식만)
    while IFS='=' read -r key value; do
        # 공백 및 주석 제거
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)

        # 주석이나 빈 줄 무시
        if [[ -z "$key" ]] || [[ "$key" == \#* ]] || [[ "$key" == "" ]]; then
            continue
        fi

        # 변수 할당
        case "$key" in
            SERVICE_ACCOUNT_FILE)
                SERVICE_ACCOUNT_FILE="$value"
                echo "   ✓ Service Account: $value"
                ;;
            GOOGLE_SHEET_ID)
                GOOGLE_SHEET_ID="$value"
                echo "   ✓ Sheet ID: $value"
                ;;
            SHEET_TAB_NAME)
                SHEET_TAB_NAME="$value"
                echo "   ✓ Tab Name: $value"
                ;;
            FLASK_PORT)
                FLASK_PORT="$value"
                echo "   ✓ Flask Port: $value"
                ;;
            OUTPUT_DIR)
                OUTPUT_DIR="$value"
                echo "   ✓ Output Dir: $value"
                ;;
        esac
    done < PRIVATE_SETUP.md

    echo -e "${GREEN}✅ Custom configuration loaded${NC}"
else
    echo -e "${YELLOW}⚠️  PRIVATE_SETUP.md not found, using default values${NC}"
    echo "   Create PRIVATE_SETUP.md for custom configuration"
    echo "   See: PRIVATE_SETUP.md.template"
fi
echo ""

# .env 파일 생성
echo "Step 3/4: Creating .env file..."
cat > .env << EOF
# Google Sheets Configuration
GOOGLE_SHEET_ID=$GOOGLE_SHEET_ID
GOOGLE_SERVICE_ACCOUNT_FILE=$SERVICE_ACCOUNT_FILE

# Sheet Tab Name
SHEET_TAB_NAME=$SHEET_TAB_NAME

# Flask Server (Optional)
FLASK_PORT=$FLASK_PORT
FLASK_DEBUG=False

# Output Directory
OUTPUT_DIR=$OUTPUT_DIR
EOF

echo -e "${GREEN}✅ .env file created${NC}"
echo "   Sheet ID: $GOOGLE_SHEET_ID"
echo "   Tab Name: $SHEET_TAB_NAME"
echo "   Service Account: $SERVICE_ACCOUNT_FILE"
echo ""

# Step 4: Python 의존성 설치
echo "Step 4/5: Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    # pip3 또는 pip 사용
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        echo -e "${RED}❌ pip not found${NC}"
        echo "Please install Python and pip first"
        exit 1
    fi

    echo "   Using: $PIP_CMD"
    $PIP_CMD install -q -r requirements.txt || {
        echo -e "${YELLOW}⚠️  Some packages may have failed to install${NC}"
        echo "   Try: $PIP_CMD install -r requirements.txt"
    }
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found${NC}"
fi
echo ""

# Step 5: 스크립트 실행 권한 설정
echo "Step 5/5: Setting script permissions..."
if [ -d "scripts" ]; then
    chmod +x scripts/*.py 2>/dev/null || true
    echo -e "${GREEN}✅ Script permissions set${NC}"
fi

# Step 6: output 폴더 생성
mkdir -p output
echo -e "${GREEN}✅ Output directory ready${NC}"
echo ""

# 완료 메시지
echo "================================"
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""
echo "You can now use:"
echo "  /generate VD25FPT003"
echo "  /batch-generate VD25FPT003 VD25FPT005"
echo "  /start-server"
echo ""
echo "For more details, see:"
echo "  - PRIVATE_SETUP.md (full setup guide)"
echo "  - README.md (plugin documentation)"
echo ""
