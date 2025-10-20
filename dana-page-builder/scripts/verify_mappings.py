"""
Verify that REQUEST_FORM_COLUMNS mapping matches actual CSV structure
"""
import csv
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import REQUEST_FORM_COLUMNS

# Path to actual CSV file
CSV_FILE = Path(__file__).parent.parent / "다나앤페타_상세페이지_raw - 시트4.csv"

def verify_mappings():
    """Verify column mappings against actual CSV"""
    print("=" * 60)
    print("Verifying REQUEST_FORM_COLUMNS Mapping")
    print("=" * 60)

    # Read CSV header
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

    print(f"\n✅ CSV Header has {len(header)} columns")
    print(f"✅ REQUEST_FORM_COLUMNS has {len(REQUEST_FORM_COLUMNS)} mappings")

    # Verify each mapping
    errors = []
    for field_name, column_index in REQUEST_FORM_COLUMNS.items():
        if column_index >= len(header):
            errors.append(f"❌ {field_name}: index {column_index} exceeds column count {len(header)}")
        else:
            actual_header = header[column_index]
            print(f"✅ {field_name:30} → [{column_index:3}] {actual_header}")

    # Check critical mappings
    print("\n" + "=" * 60)
    print("Critical Field Verification")
    print("=" * 60)

    critical_fields = {
        "productCode": "상품코드",
        "mdComment": "MD코멘트",
        "mainColor": "Main Color",
        "size1Name": "호칭1",
        "size1Shoulder": "호칭1_어깨너비(화장)",
        "title": "p상품명칸",
        "fabricComposition": "p소재칸",
        "fabricTransparency": "비침",
        "fabric1": "Fabric_1",
        "productInfo1": "참고 사항_1"
    }

    for field, expected_header in critical_fields.items():
        if field in REQUEST_FORM_COLUMNS:
            idx = REQUEST_FORM_COLUMNS[field]
            if idx < len(header):
                actual = header[idx]
                if actual == expected_header:
                    print(f"✅ {field:30} → {actual}")
                else:
                    print(f"❌ {field:30} → Expected: {expected_header}, Got: {actual}")
                    errors.append(f"{field} mismatch")
            else:
                print(f"❌ {field:30} → Index {idx} out of range")
                errors.append(f"{field} out of range")
        else:
            print(f"❌ {field:30} → Not found in REQUEST_FORM_COLUMNS")
            errors.append(f"{field} not mapped")

    # Summary
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ Verification FAILED with {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ All mappings verified successfully!")
        print("=" * 60)
        return True

if __name__ == "__main__":
    success = verify_mappings()
    sys.exit(0 if success else 1)
