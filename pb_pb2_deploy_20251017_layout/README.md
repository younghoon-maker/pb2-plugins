# pb_pb2_new_page - Product Page Builder

Automated product detail page generator with pixel-perfect Figma implementation.

**Pipeline**: Google Sheets (292 columns) → Product Data (JSON) → HTML Pages (Editable + Export)

---

## Features

✨ **292-Column Google Sheets** - Comprehensive data structure supporting:
- Multiple color variants with 2x2 grid layout
- Detail points with images and descriptions
- Gallery images grouped by color
- Product shots with color labels
- Fabric info with properties table
- Complete size information (top/bottom)
- Model information

🎨 **Editable Mode** - Interactive HTML with advanced controls:
- Image crop editor (pan X/Y, zoom)
- Page zoom (30-100%)
- Text editing (contenteditable)
- Size image selector
- Settings persistence (localStorage)

🖼️ **Dual Output Modes**:
- **Editable**: Interactive HTML with crop controls + text editing
- **Export**: Clean HTML or high-resolution JPG (with automatic server/client fallback)

🚀 **Flask Server (V4)** - Local web server for editing and exporting:
- Port 5001
- Date-based folder structure (YYYYMMDD)
- HTML/JPG export endpoints

📱 **Pixel-Perfect Design** - Figma specifications implemented accurately

---

## Quick Start

### 1. Prerequisites

```bash
# Python 3.11+
python3 --version

# Install dependencies (Option A: Poetry)
poetry install

# Install dependencies (Option B: pip)
pip3 install -r requirements.txt
```

### 2. Setup Credentials

1. Download Service Account JSON from Google Cloud Console
2. Save to `credentials/service-account.json`
3. Share your Google Sheet with the Service Account email

**자세한 설정**: [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)

### 3. Configure

Copy `.env.example` to `.env` and edit:

```bash
cp .env.example .env
```

Edit `.env`:
```bash
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json
```

### 4. Generate HTML Pages

#### Single Product
```bash
python3 scripts/generate_editable_html.py VD25FCA004
```

#### Batch Processing
```bash
python3 scripts/generate_batch.py
```

**Expected output**:
```
✅ Successfully loaded 1 products
✅ Generated: output/20251016/editable/VD25FCA004_editable.html
```

### 5. Edit and Export

Start Flask server:
```bash
python3 scripts/server.py
```

Open browser:
```
http://localhost:5001
```

1. Select an editable HTML file from the list
2. Edit images (crop/zoom) and text
3. Click "HTML 다운로드" or "JPG 다운로드"
4. Files saved to `output/{date}/export/`

**자세한 사용법**: [docs/USAGE_GUIDE.md](docs/USAGE_GUIDE.md)

---

## Project Structure

```
pb_pb2_new_page/
├── src/
│   ├── clients/              # API clients (Google Sheets, Figma)
│   ├── models/               # Pydantic data models
│   ├── parsers/              # Data parsers
│   ├── sheets_loader/        # Google Sheets loader (9 files)
│   │   ├── loader.py
│   │   ├── product_builder.py
│   │   ├── column_mapping.py
│   │   └── color_extractor.py
│   ├── validators/           # Data validators
│   ├── utils/                # Utilities
│   ├── html_generator.py     # HTML generation logic
│   ├── layout_renderer.py    # Layout rendering
│   └── template_engine.py    # Jinja2 templating
├── templates/
│   ├── base.html.jinja2      # Base template
│   └── sections/             # Section templates (12 files)
├── scripts/
│   ├── server.py             # Flask server (Port 5001)
│   ├── generate_editable_html.py       # Single product (V4)
│   ├── generate_batch.py               # Batch processing (V4)
│   └── generate_final_html.py          # Final HTML generation (V4)
├── examples/
│   ├── load_sample.py        # Data load sample
│   ├── README.md             # Examples documentation
│   └── archive/              # Old version files (v1-v3)
├── credentials/
│   └── service-account.json  # Google API credentials (create this)
├── output/
│   └── {YYYYMMDD}/
│       ├── editable/         # Editable HTML files
│       └── export/           # Exported HTML/JPG files
├── docs/
│   ├── SETUP_GUIDE.md        # Google Cloud setup guide
│   ├── USAGE_GUIDE.md        # 4-step workflow guide
│   └── GOOGLE_SHEETS_SCHEMA.md # 292 columns documentation
├── pyproject.toml            # Poetry dependencies
├── requirements.txt          # pip dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) | Google Cloud Console setup |
| [USAGE_GUIDE.md](docs/USAGE_GUIDE.md) | 4-step workflow (Load → Generate → Edit → Export) |
| [GOOGLE_SHEETS_SCHEMA.md](docs/GOOGLE_SHEETS_SCHEMA.md) | 292 columns structure |
| [examples/README.md](examples/README.md) | Example scripts usage |

---

## Google Sheets Structure

**292 columns** (A~KJ) organized into categories:

| Category | Columns | Count | Description |
|----------|---------|-------|-------------|
| Basic Info | A~C | 3 | Product code, title, description |
| Hero | D~G | 4 | Main image, selling points |
| Colors | H~K | 4+ | Color variants with names, hex codes, images |
| Gallery | L~... | Variable | Gallery images by color |
| Detail Points | ... | Multiple | Detail images and descriptions |
| Product Shots | ... | Multiple | Product shot images by color |
| Fabric Info | ... | Multiple | Fabric images, composition, properties |
| Size Info | ... | Multiple | Size tables (top/bottom) |
| Model Info | ... | Multiple | Model information |

**Full schema**: [docs/GOOGLE_SHEETS_SCHEMA.md](docs/GOOGLE_SHEETS_SCHEMA.md)

---

## Editable Mode Features

### 1. Image Crop Editor
- **Pan X/Y**: Horizontal and vertical position (-50 to +50)
- **Zoom**: Zoom level (100% to 500%)
- **Drag**: Click and drag images to reposition
- **Wheel**: Mouse wheel to zoom in/out

### 2. Page Zoom
- **Range**: 30% ~ 100%
- **Default**: 60% (fits 1200px page on screen)
- **Keyboard**: Ctrl + Mouse Wheel

### 3. Text Editing
All text elements are contenteditable:
- Product title and descriptions
- Detail point texts
- Fabric information
- Size tables
- Model info

### 4. Size Image Selector
Change product info size illustration:
- 상의 (Top)
- 팬츠 (Pants)
- 스커트 (Skirt variants)
- 아우터 (Outer)
- 원피스 (Dress)
- 점프수트 (Jumpsuit)

### 5. Export Functions
- **HTML Export**: Clean HTML file with embedded images
- **JPG Export**: High-resolution image (scale: 2x) with **dual-mode support**
  - **Server Mode (default)**: Save to Flask server (`output/{date}/export/`)
  - **Client Download Mode (automatic fallback)**: Download directly to browser when server unavailable
  - Automatic mode switching without user intervention
  - Same filename and quality (95% JPEG) in both modes
- **Auto-save**: Settings saved to localStorage

---

## Flask Server (Port 5001)

### Endpoints

1. **`/` (GET)**: List available editable files
2. **`/editable/<product_code>` (GET)**: Serve editable HTML
3. **`/save-html` (POST)**: Save edited HTML
4. **`/save-jpg` (POST)**: Save page as JPG (optional - automatic client fallback when unavailable)

### Usage

```bash
# Start server
python3 scripts/server.py

# Open browser
open http://localhost:5001
```

---

## Dependencies

### Core Dependencies
- **pydantic** (^2.12.2) - Data validation
- **requests** (>=2.32.5) - HTTP requests
- **jinja2** (>=3.1.6) - HTML templating
- **google-api-python-client** (^2.184.0) - Google Sheets API
- **google-auth** (^2.41.1) - Service Account authentication
- **flask** (>=3.1.2) - Web server
- **flask-cors** (>=6.0.1) - CORS support

### Dev Dependencies
- **pytest** (>=8.4.2) - Testing
- **mypy** (>=1.18.2) - Type checking
- **ruff** (>=0.14.0) - Linting

---

## Troubleshooting

### Service Account Error

**Error**: `❌ Service Account file not found`

**Fix**:
```bash
# Check file exists
ls credentials/service-account.json

# Download from Google Cloud Console if missing
```

### Google Sheets Access Denied

**Error**: `❌ Authentication failed: 403 Forbidden`

**Fix**:
1. Open Google Sheet in browser
2. Click "Share"
3. Add Service Account email (from `credentials/service-account.json` → `client_email`)
4. Grant "Viewer" permissions

### Port 5001 Already in Use

**Error**: `Address already in use`

**Fix**:
```bash
# Kill existing process
lsof -ti:5001 | xargs kill -9

# Or use different port in .env
FLASK_PORT=5002
```

### Missing Dependencies

**Error**: `ModuleNotFoundError`

**Fix**:
```bash
# Reinstall dependencies
poetry install --no-root

# Or with pip
pip3 install -r requirements.txt
```

---

## Performance

**Typical execution time** (single product with 50 images):
- Data load: ~10 seconds (includes image download)
- HTML generation: ~2 seconds
- **Total**: ~12 seconds

**Optimization**:
- Images cached in `output/assets/images/`
- Skip re-download if images exist
- Base64 encoding done once per image

---

## Version

**v0.1.1** - Hero section layout optimization

**Changes**:
- 🎨 Hero section white background optimized to 300px
- 📝 Documentation updated (V4.6 changelog)
- 📦 Deploy package: `pb_pb2_deploy_20251017_layout.tar.gz`

**Built with**:
- Python 3.11+
- Google Sheets API
- Jinja2 templating
- Flask web server
- Pydantic data validation

**Based on**: MoAI-ADK SPEC-First TDD methodology

---

## Support

For issues or questions:

1. Check [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for configuration issues
2. Check [USAGE_GUIDE.md](docs/USAGE_GUIDE.md) for workflow questions
3. Check [GOOGLE_SHEETS_SCHEMA.md](docs/GOOGLE_SHEETS_SCHEMA.md) for data structure
4. Verify Google Sheets permissions

---

## License

Private project.

© 2025 All Rights Reserved
