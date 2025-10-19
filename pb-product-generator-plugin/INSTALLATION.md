# Installation Guide

Complete installation guide for pb-product-generator Claude plugin.

Version: 0.2.1

---

## Overview

This guide walks you through:
1. Adding GitHub marketplace
2. Installing the plugin
3. Restarting Claude
4. Receiving and copying PRIVATE_SETUP.md
5. Running auto-setup command
6. Granting Google Sheets permissions
7. Testing the installation

**Total time**: ~5 minutes

---

## Prerequisites

- **Claude Code** installed and running
- **Python 3.8+** installed
- **Google Cloud Service Account** with Sheets API access
- **PRIVATE_SETUP.md** file (provided by admin)

---

## Installation Steps

### Step 1: Add GitHub Marketplace

In your Claude Code session:

```bash
/plugin marketplace add younghoon-maker/pb2-plugins
```

**Expected output**:
```
✅ Marketplace added: pb2-plugins
```

---

### Step 2: Install Plugin

```bash
/plugin install pb-product-generator@pb2-plugins
```

**Expected output**:
```
✅ Plugin installed: pb-product-generator (v0.2.1)
📂 Location: ~/.claude/plugins/pb-product-generator/
```

---

### Step 3: Restart Claude

**IMPORTANT**: You must quit and restart Claude for the plugin to be loaded.

```bash
/quit
```

Then in your terminal:

```bash
claude
```

**Expected output**:
```
✅ Loaded plugins: pb-product-generator (v0.2.1)
```

---

### Step 4: Receive PRIVATE_SETUP.md

**From Admin**: You will receive `PRIVATE_SETUP.md` file from the plugin administrator.

**Copy to Your Project Folder**:

```bash
# Copy PRIVATE_SETUP.md to the folder where you run Claude
# (Your current working directory, NOT the plugin folder)
cp /path/to/PRIVATE_SETUP.md .
```

**⚠️ Important**:
- The file must be in **your current working directory** (your project folder)
- NOT in `~/.claude/plugins/pb-product-generator/`

**Verify**:
```bash
ls -la PRIVATE_SETUP.md
```

**Expected output**:
```
-rw-r--r--  1 you  staff  12345 Oct 19 10:00 PRIVATE_SETUP.md
```

---

### Step 5: Run Auto-Setup

In Claude Code, run:

```bash
/pb-product-generator:setup-from-private
```

**What it does**:
1. ✅ Reads PRIVATE_SETUP.md from your project folder
2. ✅ Creates `credentials/` folder
3. ✅ Generates `credentials/service-account.json`
4. ✅ Creates `.env` file
5. ✅ Installs Python dependencies
6. ✅ Creates `output/` folder

**Expected output**:
```
🚀 PB Product Generator - Automatic Setup
==================================================

✅ Found PRIVATE_SETUP.md

📋 Parsing PRIVATE_SETUP.md...
   ✓ Service Account: test-account-n8n@damoa-fb351.iam.gserviceaccount.com
   ✓ Sheet ID: 1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk

📁 Creating directories...
   ✓ credentials/
   ✓ output/

📄 Writing files...
   ✓ credentials/service-account.json
   ✓ .env

📦 Installing Python dependencies...
   Installing gspread... ✓
   Installing Pillow... ✓
   Installing jinja2... ✓
   Installing flask... ✓

✅ Setup completed successfully!

📁 Created files:
   - credentials/service-account.json
   - .env
   - output/

🎯 Next step:
   /pb-product-generator:generate VD25FPT003
```

**Verify setup**:
```bash
# Check folder structure
ls -la

# Expected folders:
# drwxr-xr-x   credentials/
# -rw-r--r--   .env
# -rw-r--r--   PRIVATE_SETUP.md
# drwxr-xr-x   output/
```

---

### Step 6: Google Sheets Permissions (One-time)

Grant access to the Service Account:

1. **Open Google Sheets**:
   https://docs.google.com/spreadsheets/d/1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk/edit

2. **Click Share button** (top-right corner)

3. **Add Service Account email**:
   ```
   test-account-n8n@damoa-fb351.iam.gserviceaccount.com
   ```

4. **Set permission**: **Viewer** (read-only)

5. **Click Send**

**Verify permissions**:
```
✅ test-account-n8n@damoa-fb351.iam.gserviceaccount.com has Viewer access
```

---

### Step 7: Test Generation

Test the installation with a sample product:

```bash
/pb-product-generator:generate VD25FPT003
```

**Expected output**:
```
📊 Loading product data from Google Sheets...
✅ Successfully loaded 1 products

🖼️  Downloading images and converting to Base64...
   - Main image (3.2 MB)
   - Gallery images (12 items)
   - Detail images (3 items)

🎨 Generating HTML with Figma template...
✅ Generated: output/20251019/editable/VD25FPT003_editable_v4.html (70 MB)

🎨 Features:
- Image crop/zoom editor
- Text editing (contenteditable)
- Page zoom (30-100%)
- HTML/JPG download

📁 File location:
   output/20251019/editable/VD25FPT003_editable_v4.html
```

**Open the generated file**:

**macOS**:
```bash
open output/20251019/editable/VD25FPT003_editable_v4.html
```

**Windows**:
```cmd
start output\20251019\editable\VD25FPT003_editable_v4.html
```

---

## 🎉 Installation Complete!

You're now ready to use the plugin. Try these commands:

**Single product**:
```bash
/pb-product-generator:generate {product_code}
```

**Batch generation**:
```bash
/pb-product-generator:batch {code1} {code2} {code3}
```

**Flask server**:
```bash
/pb-product-generator:server
```

---

## Troubleshooting

### ❌ "Service Account file NOT found"

**Cause**: `credentials/service-account.json` is missing

**Solution**:
```bash
# Re-run auto-setup
/pb-product-generator:setup-from-private
```

### ❌ "HttpError 403: Forbidden"

**Cause**: Service Account doesn't have access to Google Sheets

**Solution**:
1. Check Service Account email:
   ```bash
   cat credentials/service-account.json | grep client_email
   ```

2. Share Google Sheets with this email (Step 6)

### ❌ "ModuleNotFoundError: No module named 'gspread'"

**Cause**: Python dependencies not installed

**Solution**:
```bash
# Re-run auto-setup
/pb-product-generator:setup-from-private

# Or manually install
pip3 install -r ~/.claude/plugins/pb-product-generator/requirements.txt
```

### ❌ "Command not found: /pb-product-generator:generate"

**Cause**: Plugin not loaded or Claude not restarted

**Solution**:
```bash
# Verify plugin installation
/plugin list

# If missing, reinstall
/plugin install pb-product-generator@pb2-plugins

# Restart Claude
/quit
claude
```

### ❌ "Product {code} not found in sheets"

**Cause**: Product code doesn't exist in Google Sheets or tab name is wrong

**Solution**:
1. Open Google Sheets and verify product code exists
2. Check `.env` file:
   ```bash
   cat .env | grep SHEET_TAB_NAME
   ```
3. Verify tab name matches the sheet (default: `new_raw`)

---

## Next Steps

**Quick Reference**:
- [README.md](./README.md) - Overview and features
- [commands/generate.md](./commands/generate.md) - Single product generation
- [commands/batch.md](./commands/batch.md) - Batch generation
- [commands/server.md](./commands/server.md) - Flask server

**Support**:
- GitHub Issues: https://github.com/younghoon-maker/pb2-plugins/issues
- Plugin Documentation: https://github.com/younghoon-maker/pb2-plugins/tree/main/pb-product-generator-plugin

---

**Version**: 0.2.1
**Last Updated**: 2025-10-19
