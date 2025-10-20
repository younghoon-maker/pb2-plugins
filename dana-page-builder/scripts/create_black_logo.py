"""
Create black version of DANA&PETA logo for gallery use
Converts white logo PNG to black while preserving transparency
"""

from PIL import Image
from pathlib import Path

# Paths
logo_white_path = Path(__file__).parent.parent / "reference" / "dana&peta_logo.png"
logo_black_path = Path(__file__).parent.parent / "reference" / "dana&peta_logo_black.png"

# Load white logo
logo = Image.open(logo_white_path)

# Convert to RGBA if not already
logo = logo.convert('RGBA')

# Get pixel data
pixels = logo.load()

# Convert all non-transparent pixels to black
for y in range(logo.height):
    for x in range(logo.width):
        r, g, b, a = pixels[x, y]
        if a > 0:  # Only modify non-transparent pixels
            pixels[x, y] = (0, 0, 0, a)  # Black with original alpha

# Save black logo
logo.save(logo_black_path)

print(f"✅ Black logo created: {logo_black_path}")
print(f"   Size: {logo.width}x{logo.height}")
