#!/bin/bash
# PB Product Generator - Automatic Setup Script
# Version: 0.2.0

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

# Step 3: .env 파일 생성
echo "Step 2/4: Creating .env file..."
cat > .env << 'EOF'
# Google Sheets Configuration
GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json

# Flask Server (Optional)
FLASK_PORT=5001
FLASK_DEBUG=False
EOF

echo -e "${GREEN}✅ .env file created${NC}"
echo "   Sheet ID: 1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk"
echo "   Tab Name: new_raw (hardcoded in src/sheets_loader/loader.py)"
echo ""

# Step 4: Python 의존성 설치
echo "Step 3/4: Installing Python dependencies..."
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
echo "Step 4/4: Setting script permissions..."
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
