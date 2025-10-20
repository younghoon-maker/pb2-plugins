#!/usr/bin/env python3
"""
Compare actual Google Sheets headers with config.py TEMPLATE_COLUMNS mapping.
Identify misalignments causing validation errors.
"""

import json
from investigate_sheet_structure import get_sheet_headers

# Key fields that are known to be failing validation
FAILING_FIELDS = {
    'color1Hex': 8,          # Receiving '추천 코멘트' instead of hex
    'color1Gallery1': 23,    # Receiving '캘리포니아 레터링 맨투맨FFF' instead of URL
    'fabricImage': 127,      # Missing
    'fabricComposition': 128 # Missing
}

# Expected values at these indices based on error messages
ACTUAL_VALUES_AT_INDICES = {
    8: '추천 코멘트',  # Should be at index 5 (mdComment)
    23: '캘리포니아 레터링 맨투맨FFF'  # Looks like product title (should be index 1)
}

def analyze_misalignment(headers):
    """Analyze where the misalignment is occurring."""
    print("\n" + "=" * 80)
    print("MISALIGNMENT ANALYSIS")
    print("=" * 80)

    print("\n1. Checking failing fields:")
    print("-" * 80)

    for field, expected_idx in FAILING_FIELDS.items():
        if expected_idx < len(headers):
            actual_header = headers[expected_idx]
            print(f"  {field} (index {expected_idx}):")
            print(f"    → Actual header: '{actual_header}'")

            if field in ['color1Hex']:
                print(f"    → Error: Receiving '추천 코멘트' (should be hex code)")
            elif field in ['color1Gallery1']:
                print(f"    → Error: Receiving '캘리포니아 레터링 맨투맨FFF' (should be URL)")
            elif field in ['fabricImage', 'fabricComposition']:
                print(f"    → Error: Missing data")
        else:
            print(f"  {field} (index {expected_idx}): MISSING - sheet only has {len(headers)} columns")

    print("\n2. Searching for expected values in actual positions:")
    print("-" * 80)

    # Search for where '추천 코멘트' actually appears
    search_terms = ['추천', '코멘트', '상품코드', '상품명', '색상1', 'HEX', '디테일이미지1']

    for term in search_terms:
        matching_indices = []
        for i, header in enumerate(headers):
            if term in header:
                matching_indices.append((i, header))

        if matching_indices:
            print(f"\n  '{term}' found in:")
            for idx, header in matching_indices[:5]:  # Show first 5 matches
                column_letter = get_column_letter(idx)
                print(f"    Index {idx:3d} ({column_letter:3s}): {header}")

    print("\n3. Checking if there's a consistent shift pattern:")
    print("-" * 80)

    # Check first 10 columns for shift pattern
    expected_fields = ['productCode', 'title', 'sellingPoint1', 'sellingPoint2',
                      'sellingPoint3', 'mdComment', 'mainImage', 'color1Name', 'color1Hex']

    for i, field in enumerate(expected_fields):
        if i < len(headers):
            print(f"  Index {i:2d}: Config expects '{field}' → Actual: '{headers[i]}'")

    # Save detailed analysis
    output = {
        "total_columns": len(headers),
        "failing_fields_analysis": {
            field: {
                "expected_index": idx,
                "actual_header": headers[idx] if idx < len(headers) else "MISSING"
            }
            for field, idx in FAILING_FIELDS.items()
        },
        "first_50_headers": headers[:50]
    }

    with open("misalignment_analysis.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Detailed analysis saved to: misalignment_analysis.json")

def get_column_letter(idx):
    """Convert column index to Excel-style letter (A, B, ..., Z, AA, AB, ...)"""
    if idx < 26:
        return chr(65 + idx)
    elif idx < 702:  # Up to ZZ
        return chr(64 + idx // 26) + chr(65 + idx % 26)
    else:
        # For columns beyond ZZ, use simple notation
        return f"Col{idx}"

if __name__ == "__main__":
    try:
        print("Fetching Google Sheets headers...")
        headers = get_sheet_headers()

        print(f"\n✅ Retrieved {len(headers)} columns from sheet")
        print(f"   Expected: 302 columns (A-KP)")

        if len(headers) != 302:
            print(f"\n⚠️  WARNING: Column count mismatch!")
            print(f"   Sheet has {len(headers)} columns, config expects 302")

        analyze_misalignment(headers)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
