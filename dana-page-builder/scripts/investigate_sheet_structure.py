#!/usr/bin/env python3
"""
Investigate Google Sheets '템플릿' tab structure to identify column mapping issues.
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration (from config.py)
SHEET_ID = "1m1f784rij74eSpuHOEOqbAzQu97ZenfLa3QuO-Egjxk"  # DANA&PETA Products Sheet
SHEET_NAME = "템플릿"
SERVICE_ACCOUNT_FILE = "../credentials/service-account.json"

def get_sheet_headers():
    """Fetch the first row (headers) from the sheet."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )

    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()

    # Get first row (headers)
    range_name = f"{SHEET_NAME}!A1:KP1"
    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range=range_name
    ).execute()

    headers = result.get('values', [[]])[0]

    return headers

def analyze_headers(headers):
    """Analyze headers and compare with expected config."""
    print(f"Total columns found: {len(headers)}\n")
    print("First 50 column headers:")
    print("=" * 80)

    for i, header in enumerate(headers[:50]):
        column_letter = chr(65 + i) if i < 26 else f"{chr(65 + i//26 - 1)}{chr(65 + i%26)}"
        print(f"{i:3d} | {column_letter:3s} | {header}")

    print("\n" + "=" * 80)
    print("\nKey columns to verify:")
    print("-" * 80)

    # Check specific columns that are failing
    key_columns = {
        0: "productCode (A)",
        1: "title (B)",
        5: "mdComment (F)",
        6: "mainImage (G)",
        7: "color1Name (H)",
        8: "color1Hex (I)",
        23: "color1Gallery1 (X)",
        127: "fabricImage",
        128: "fabricComposition"
    }

    for idx, expected_field in key_columns.items():
        if idx < len(headers):
            actual_header = headers[idx]
            print(f"Index {idx:3d}: Expected '{expected_field}' → Actual: '{actual_header}'")
        else:
            print(f"Index {idx:3d}: MISSING (sheet has only {len(headers)} columns)")

    # Save full headers to JSON for reference
    output = {
        "total_columns": len(headers),
        "headers": {i: header for i, header in enumerate(headers)},
        "column_map": {header: i for i, header in enumerate(headers) if header}
    }

    with open("sheet_headers.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Full headers saved to: sheet_headers.json")

if __name__ == "__main__":
    try:
        print("Fetching sheet headers from Google Sheets...")
        print(f"Sheet ID: {SHEET_ID}")
        print(f"Sheet Name: {SHEET_NAME}\n")

        headers = get_sheet_headers()
        analyze_headers(headers)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
