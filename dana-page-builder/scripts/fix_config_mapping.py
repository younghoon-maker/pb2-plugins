#!/usr/bin/env python3
"""
Generate corrected TEMPLATE_COLUMNS mapping for config.py.
Fix: Add missing 'sellingPoint4' at index 5, shift all subsequent indices by +1.
"""

# Original mapping (indices 0-4 are correct)
CORRECT_PREFIX = {
    'productCode': 0,       # A - 상품코드
    'title': 1,             # B - 상품명
    'sellingPoint1': 2,     # C - 설명1
    'sellingPoint2': 3,     # D - 설명2
    'sellingPoint3': 4,     # E - 설명3
}

# NEW: Add missing field
MISSING_FIELD = {
    'sellingPoint4': 5,     # F - 설명4 (MISSING in original config!)
}

# All fields from old index 5 onwards, shifted by +1
SHIFTED_FIELDS = {
    # Basic Info (shifted from 5-6 to 6-7)
    'mdComment': 6,         # G - 추천 코멘트 (was 5)
    'mainImage': 7,         # H - 메인이미지_url (was 6)

    # Color Names & HEX (shifted from 7-14 to 8-15)
    'color1Name': 8,        # I - 색상1_이름 (was 7)
    'color1Hex': 9,         # J - 색상1_HEX (was 8)
    'color2Name': 10,       # K - 색상2_이름 (was 9)
    'color2Hex': 11,        # L - 색상2_HEX (was 10)
    'color3Name': 12,       # M - 색상3_이름 (was 11)
    'color3Hex': 13,        # N - 색상3_HEX (was 12)
    'color4Name': 14,       # O - 색상4_이름 (was 13)
    'color4Hex': 15,        # P - 색상4_HEX (was 14)

    # Detail Points (shifted from 15-22 to 16-23)
    'detailPoint1Image': 16,    # Q - 디테일포인트1_url (was 15)
    'detailPoint1Text': 17,     # R - 디테일포인트1_설명 (was 16)
    'detailPoint2Image': 18,    # S - 디테일포인트2_url (was 17)
    'detailPoint2Text': 19,     # T - 디테일포인트2_설명 (was 18)
    'detailPoint3Image': 20,    # U - 디테일포인트3_url (was 19)
    'detailPoint3Text': 21,     # V - 디테일포인트3_설명 (was 20)
    'detailPoint4Image': 22,    # W - 디테일포인트4_url (was 21)
    'detailPoint4Text': 23,     # X - 디테일포인트4_설명 (was 22)
}

def generate_gallery_mappings():
    """Generate color gallery mappings (24-119)"""
    mappings = {}
    old_start = 23  # Original start index
    new_start = 24  # New start index (shifted by +1)

    for color_num in range(1, 9):  # Color1-8
        for img_num in range(1, 13):  # 12 images each
            old_idx = old_start + (color_num - 1) * 12 + (img_num - 1)
            new_idx = new_start + (color_num - 1) * 12 + (img_num - 1)
            field_name = f'color{color_num}Gallery{img_num}'
            mappings[field_name] = new_idx

    return mappings

def generate_product_shot_mappings():
    """Generate product shot mappings (120-127)"""
    mappings = {}
    old_start = 119
    new_start = 120

    for color_num in range(1, 9):
        old_idx = old_start + (color_num - 1)
        new_idx = new_start + (color_num - 1)
        field_name = f'color{color_num}ProductShot'
        mappings[field_name] = new_idx

    return mappings

def generate_fabric_mappings():
    """Generate fabric info mappings (128-135)"""
    old_indices = {
        'fabricImage': 127,
        'fabricComposition': 128,
        'fabricDesc': 129,
        'fabricTransparency': 130,
        'fabricStretch': 131,
        'fabricLining': 132,
        'fabricThickness': 133,
        'fabricSeason': 134,
    }

    return {field: old_idx + 1 for field, old_idx in old_indices.items()}

def generate_product_info_mappings():
    """Generate product info mappings (136-142)"""
    old_indices = {
        'sizeImage': 135,
        'productName': 136,
        'colorName': 137,
        'sizeName': 138,
        'fabric': 139,
        'washingInfo': 140,
        'origin': 141,
    }

    return {field: old_idx + 1 for field, old_idx in old_indices.items()}

def generate_size_mappings():
    """Generate top and bottom size mappings (143-301)"""
    mappings = {}

    # Top sizes (142-221 → 143-222)
    for size_num in range(1, 11):  # 10 sizes
        old_base = 142 + (size_num - 1) * 8
        new_base = 143 + (size_num - 1) * 8

        mappings[f'topSize{size_num}Name'] = new_base
        mappings[f'topSize{size_num}Shoulder'] = new_base + 1
        mappings[f'topSize{size_num}Chest'] = new_base + 2
        mappings[f'topSize{size_num}Hem'] = new_base + 3
        mappings[f'topSize{size_num}SleeveLength'] = new_base + 4
        mappings[f'topSize{size_num}SleeveOpening'] = new_base + 5
        mappings[f'topSize{size_num}TotalLength'] = new_base + 6
        mappings[f'topSize{size_num}Optional'] = new_base + 7

    # Bottom sizes (222-300 → 223-301)
    # NOTE: bottomSize10Optional does NOT exist in sheet (last column is index 301: 하의_총장_10)
    for size_num in range(1, 10):  # Sizes 1-9 have 8 fields
        old_base = 222 + (size_num - 1) * 8
        new_base = 223 + (size_num - 1) * 8

        mappings[f'bottomSize{size_num}Name'] = new_base
        mappings[f'bottomSize{size_num}Waist'] = new_base + 1
        mappings[f'bottomSize{size_num}Hip'] = new_base + 2
        mappings[f'bottomSize{size_num}Thigh'] = new_base + 3
        mappings[f'bottomSize{size_num}Hem'] = new_base + 4
        mappings[f'bottomSize{size_num}Rise'] = new_base + 5
        mappings[f'bottomSize{size_num}TotalLength'] = new_base + 6
        mappings[f'bottomSize{size_num}Optional'] = new_base + 7

    # Size 10 has only 7 fields (no Optional field)
    old_base = 222 + 9 * 8  # = 294
    new_base = 223 + 9 * 8  # = 295
    mappings['bottomSize10Name'] = new_base
    mappings['bottomSize10Waist'] = new_base + 1
    mappings['bottomSize10Hip'] = new_base + 2
    mappings['bottomSize10Thigh'] = new_base + 3
    mappings['bottomSize10Hem'] = new_base + 4
    mappings['bottomSize10Rise'] = new_base + 5
    mappings['bottomSize10TotalLength'] = new_base + 6
    # NO bottomSize10Optional!

    return mappings

def main():
    """Generate complete corrected TEMPLATE_COLUMNS."""
    corrected = {}

    # Add all sections
    corrected.update(CORRECT_PREFIX)
    corrected.update(MISSING_FIELD)
    corrected.update(SHIFTED_FIELDS)
    corrected.update(generate_gallery_mappings())
    corrected.update(generate_product_shot_mappings())
    corrected.update(generate_fabric_mappings())
    corrected.update(generate_product_info_mappings())
    corrected.update(generate_size_mappings())

    # Verify total count
    print(f"✅ Generated {len(corrected)} field mappings")
    print(f"   Expected: 302 fields (indices 0-301)")

    # Output as Python dict format
    print("\nCorrected TEMPLATE_COLUMNS = {")

    # Group by sections
    sections = [
        ("Basic Info", ['productCode', 'title', 'sellingPoint1', 'sellingPoint2',
                       'sellingPoint3', 'sellingPoint4', 'mdComment', 'mainImage']),
        ("Color Names & HEX", [f'color{i}{t}' for i in range(1, 5) for t in ['Name', 'Hex']]),
        ("Detail Points", [f'detailPoint{i}{t}' for i in range(1, 5) for t in ['Image', 'Text']]),
    ]

    for section_name, fields in sections:
        print(f"    # {section_name}")
        for field in fields:
            if field in corrected:
                print(f"    '{field}': {corrected[field]},")
        print()

    print("    # ... (remaining fields)")
    print("}\n")

    # Save to file
    with open("corrected_template_columns.txt", "w", encoding="utf-8") as f:
        f.write("TEMPLATE_COLUMNS = {\n")

        for field, idx in sorted(corrected.items(), key=lambda x: x[1]):
            f.write(f"    '{field}': {idx},\n")

        f.write("}\n")

    print("✅ Full corrected mapping saved to: corrected_template_columns.txt")

    # Verify critical fields
    print("\nVerifying critical fields:")
    critical = {
        'mdComment': 6,
        'mainImage': 7,
        'color1Hex': 9,
        'color1Gallery1': 24,
        'fabricImage': 128,
        'fabricComposition': 129,
    }

    for field, expected in critical.items():
        actual = corrected.get(field)
        status = "✅" if actual == expected else "❌"
        print(f"  {status} {field}: {actual} (expected {expected})")

if __name__ == "__main__":
    main()
