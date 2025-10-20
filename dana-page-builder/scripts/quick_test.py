#!/usr/bin/env python3
"""Quick test to verify column mapping fix."""

import sys
sys.path.insert(0, '/Users/younghoonjung/ai-project/pb_pb2_new_page/dana-page-builder/scripts')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import SHEET_ID, SHEET_NAME, SHEET_RANGE, TEMPLATE_COLUMNS, SERVICE_ACCOUNT_FILE

def test_mapping():
    """Test that column mapping is correct."""
    print("Authenticating...")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    print(f"Fetching data from sheet: {SHEET_ID}")
    print(f"Range: {SHEET_NAME}!{SHEET_RANGE}\n")

    # Get data
    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!{SHEET_RANGE}"
    ).execute()

    rows = result.get('values', [])

    if not rows:
        print("❌ No data found")
        return

    print(f"✅ Found {len(rows)} rows\n")

    # Test first product
    first_row = rows[0]
    while len(first_row) < 302:
        first_row.append("")

    print("=" * 80)
    print("TESTING FIRST PRODUCT")
    print("=" * 80)

    # Test critical fields
    tests = {
        'productCode': 0,
        'title': 1,
        'sellingPoint4': 5,  # NEW FIELD
        'mdComment': 6,      # Was 5, now 6
        'mainImage': 7,      # Was 6, now 7
        'color1Name': 8,     # Was 7, now 8
        'color1Hex': 9,      # Was 8, now 9
        'color1Gallery1': 24, # Was 23, now 24
        'fabricImage': 128,   # Was 127, now 128
        'fabricComposition': 129,  # Was 128, now 129
    }

    print("\nCritical Fields Test:")
    print("-" * 80)

    all_passed = True
    for field, idx in tests.items():
        value = first_row[idx] if idx < len(first_row) else "MISSING"

        # Truncate for display
        display_value = value[:50] + "..." if len(value) > 50 else value

        # Validation
        passed = True
        expected_type = ""

        if field == 'color1Hex':
            passed = value.startswith('#') and len(value) == 7
            expected_type = "#RRGGBB format"
        elif 'Gallery' in field or field == 'mainImage' or field == 'fabricImage':
            passed = value.startswith('http')
            expected_type = "URL"
        elif field == 'mdComment':
            # Should NOT be product name
            passed = '캘리포니아' not in value and '맨투맨' not in value
            expected_type = "comment (not product name)"

        status = "✅" if passed else "❌"
        print(f"  {status} {field:20s} (idx {idx:3d}): {display_value}")

        if not passed:
            print(f"      Expected: {expected_type}")
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("✅ ALL TESTS PASSED - Column mapping is correct!")
    else:
        print("❌ SOME TESTS FAILED - Check output above")
    print("=" * 80)

if __name__ == "__main__":
    try:
        test_mapping()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
