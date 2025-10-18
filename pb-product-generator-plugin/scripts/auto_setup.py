#!/usr/bin/env python3
"""
PB Product Generator - Automatic Setup from PRIVATE_SETUP.md
Version: 0.2.1

This script automatically extracts configuration from PRIVATE_SETUP.md and sets up:
1. credentials/service-account.json (Service Account JSON)
2. .env file (Google Sheets ID, Tab Name, etc.)
3. Python dependencies installation
4. Validation of setup
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


class SetupError(Exception):
    """Custom exception for setup errors"""
    pass


class PrivateSetupParser:
    """Parse PRIVATE_SETUP.md and extract configuration"""

    def __init__(self, md_file_path: str):
        self.md_file_path = md_file_path
        self.content = self._read_file()

    def _read_file(self) -> str:
        """Read PRIVATE_SETUP.md file"""
        try:
            with open(self.md_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise SetupError(f"❌ PRIVATE_SETUP.md not found: {self.md_file_path}")
        except Exception as e:
            raise SetupError(f"❌ Failed to read PRIVATE_SETUP.md: {e}")

    def extract_service_account_json(self) -> Dict:
        """Extract Service Account JSON from ```json code block"""
        # Pattern: ```json\n{...}\n```
        pattern = r'```json\s*\n(\{.*?\})\s*\n```'
        matches = re.findall(pattern, self.content, re.DOTALL)

        if not matches:
            raise SetupError(
                "❌ Service Account JSON not found in PRIVATE_SETUP.md\n"
                "   Expected format:\n"
                "   ```json\n"
                "   {\n"
                '     "type": "service_account",\n'
                "     ...\n"
                "   }\n"
                "   ```"
            )

        # Take the first JSON block (should be Service Account)
        json_str = matches[0]

        try:
            service_account = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise SetupError(f"❌ Invalid JSON in Service Account block: {e}")

        # Validate required fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing_fields = [f for f in required_fields if f not in service_account]

        if missing_fields:
            raise SetupError(
                f"❌ Missing required fields in Service Account JSON: {', '.join(missing_fields)}"
            )

        if service_account['type'] != 'service_account':
            raise SetupError(
                f"❌ Invalid Service Account type: {service_account['type']} (expected: service_account)"
            )

        return service_account

    def extract_sheet_id(self) -> str:
        """Extract Google Sheets ID"""
        # Pattern 1: GOOGLE_SHEET_ID=value or GOOGLE_SHEET_ID: value
        pattern1 = r'GOOGLE_SHEET_ID[=:]?\s*`?([a-zA-Z0-9_-]+)`?'
        match1 = re.search(pattern1, self.content)

        # Pattern 2: **Sheet ID**: `value`
        pattern2 = r'\*\*Sheet ID\*\*:\s*`([a-zA-Z0-9_-]+)`'
        match2 = re.search(pattern2, self.content)

        # Pattern 3: - **Sheet ID**: `value`
        pattern3 = r'-\s*\*\*Sheet ID\*\*:\s*`([a-zA-Z0-9_-]+)`'
        match3 = re.search(pattern3, self.content)

        match = match1 or match2 or match3

        if not match:
            raise SetupError(
                "❌ Google Sheets ID not found in PRIVATE_SETUP.md\n"
                "   Expected format:\n"
                "   GOOGLE_SHEET_ID=1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk\n"
                "   or\n"
                "   - **Sheet ID**: `1ipkHdYdQhIAfUBkNUWHkFqcgP0aOXLVO14MYXWscEPk`"
            )

        return match.group(1)

    def extract_tab_name(self) -> str:
        """Extract Sheet Tab Name"""
        # Pattern 1: SHEET_TAB_NAME=value or SHEET_TAB_NAME: value
        pattern1 = r'SHEET_TAB_NAME[=:]?\s*`?([a-zA-Z0-9_-]+)`?'
        match1 = re.search(pattern1, self.content)

        # Pattern 2: **Tab Name**: `value`
        pattern2 = r'\*\*Tab Name\*\*:\s*`([^`]+)`'
        match2 = re.search(pattern2, self.content)

        # Pattern 3: - **Tab Name**: `value`
        pattern3 = r'-\s*\*\*Tab Name\*\*:\s*`([^`]+)`'
        match3 = re.search(pattern3, self.content)

        match = match1 or match2 or match3

        if not match:
            # Default to "new_raw" if not found
            print("⚠️  Tab Name not found in PRIVATE_SETUP.md, using default: new_raw")
            return "new_raw"

        return match.group(1)

    def extract_flask_port(self) -> str:
        """Extract Flask Port (optional)"""
        pattern = r'FLASK_PORT[=:]?\s*`?(\d+)`?'
        match = re.search(pattern, self.content)

        if not match:
            return "5001"  # Default

        return match.group(1)


class AutoSetup:
    """Automatic setup orchestrator"""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.private_setup_path = self.project_dir / "PRIVATE_SETUP.md"
        self.credentials_dir = self.project_dir / "credentials"
        self.service_account_path = self.credentials_dir / "service-account.json"
        self.env_path = self.project_dir / ".env"

    def run(self):
        """Execute automatic setup"""
        print("🚀 PB Product Generator - Automatic Setup")
        print("=" * 50)
        print()

        # Step 1: Check PRIVATE_SETUP.md exists
        if not self.private_setup_path.exists():
            raise SetupError(
                f"❌ PRIVATE_SETUP.md not found in current directory\n"
                f"   Expected: {self.private_setup_path}\n"
                f"   \n"
                f"   Please ensure PRIVATE_SETUP.md is in your project folder."
            )

        print(f"✅ Found PRIVATE_SETUP.md: {self.private_setup_path}")
        print()

        # Step 2: Parse PRIVATE_SETUP.md
        print("📋 Parsing PRIVATE_SETUP.md...")
        parser = PrivateSetupParser(str(self.private_setup_path))

        service_account = parser.extract_service_account_json()
        sheet_id = parser.extract_sheet_id()
        tab_name = parser.extract_tab_name()
        flask_port = parser.extract_flask_port()

        print(f"   ✓ Service Account: {service_account['client_email']}")
        print(f"   ✓ Sheet ID: {sheet_id}")
        print(f"   ✓ Tab Name: {tab_name}")
        print(f"   ✓ Flask Port: {flask_port}")
        print()

        # Step 3: Create credentials directory
        print("📁 Creating credentials directory...")
        self.credentials_dir.mkdir(exist_ok=True)
        print(f"   ✓ {self.credentials_dir}")
        print()

        # Step 4: Write service-account.json
        print("🔐 Writing Service Account JSON...")
        with open(self.service_account_path, 'w', encoding='utf-8') as f:
            json.dump(service_account, f, indent=2)
        print(f"   ✓ {self.service_account_path}")
        print()

        # Step 5: Write .env file
        print("⚙️  Writing .env file...")
        env_content = f"""# Google Sheets Configuration
GOOGLE_SHEET_ID={sheet_id}
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service-account.json

# Sheet Tab Name
SHEET_TAB_NAME={tab_name}

# Flask Server (Optional)
FLASK_PORT={flask_port}
FLASK_DEBUG=False

# Output Directory
OUTPUT_DIR=output
"""
        with open(self.env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"   ✓ {self.env_path}")
        print()

        # Step 6: Install Python dependencies
        print("📦 Installing Python dependencies...")
        plugin_dir = Path(__file__).parent.parent
        requirements_path = plugin_dir / "requirements.txt"

        if requirements_path.exists():
            import subprocess
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-q", "-r", str(requirements_path)],
                    check=True,
                    capture_output=True
                )
                print("   ✓ Dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️  Some packages may have failed to install")
                print(f"      Error: {e.stderr.decode()}")
        else:
            print("   ⚠️  requirements.txt not found, skipping")
        print()

        # Step 7: Create output directory
        output_dir = self.project_dir / "output"
        output_dir.mkdir(exist_ok=True)
        print(f"✅ Output directory ready: {output_dir}")
        print()

        # Step 8: Final summary
        print("=" * 50)
        print("✅ Setup completed successfully!")
        print()
        print("You can now use:")
        print("  /generate VD25FPT003")
        print("  /batch-generate VD25FPT003 VD25FPT005")
        print("  /start-server")
        print()
        print("For more details, see:")
        print("  - README.md (plugin documentation)")
        print("  - commands/*.md (command reference)")
        print()


def main():
    """Main entry point"""
    try:
        # Get current working directory (project folder)
        cwd = os.getcwd()

        # Run auto setup
        setup = AutoSetup(cwd)
        setup.run()

        return 0

    except SetupError as e:
        print(str(e), file=sys.stderr)
        print()
        print("💡 Troubleshooting:")
        print("  1. Ensure PRIVATE_SETUP.md is in your project folder")
        print("  2. Check Service Account JSON format (```json ... ```)")
        print("  3. Verify Google Sheets ID is present")
        print()
        return 1

    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
