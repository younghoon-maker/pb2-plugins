"""pb2-page-builder scripts package

PB2 Page Builder Scripts Package

Modules:
    - generate_editable_html: Editable HTML V4 generation (image crop/zoom, text editing)
    - generate_final_html: Base HTML generation (Figma design rendering)
    - generate_batch: Batch generation (multiple products)
    - server: Flask editing server (Port 5001)
    - cleanup: Output directory cleanup
    - auto_setup: Automatic setup from PRIVATE_SETUP.md

Usage:
    from scripts.generate_editable_html import main as generate_editable
    from scripts.generate_final_html import generate_html
"""

__version__ = "2.0.3"
__author__ = "PB Product Team"
