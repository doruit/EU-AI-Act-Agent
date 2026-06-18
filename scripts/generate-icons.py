#!/usr/bin/env python3
"""
generate-icons.py
─────────────────
Generates the two required M365 app icon files for the EU AI Act Compliance Agent:
  - appPackage/color.png   → 192 × 192 px  (full-color app icon)
  - appPackage/outline.png →  32 × 32 px   (monochrome outline icon)

Requirements:
  pip install Pillow

Usage:
  python scripts/generate-icons.py

The generated icons are simple placeholder icons that satisfy the M365 app package
validation rules. Replace them with your own branded icons before publishing.
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow is required. Install it with: pip install Pillow")
    raise

# ─── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "appPackage"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Color icon (192 × 192) ───────────────────────────────────────────────────
COLOR_SIZE = (192, 192)
EU_BLUE = (0, 51, 153)       # EU flag blue
EU_YELLOW = (255, 204, 0)    # EU flag yellow
WHITE = (255, 255, 255)

def make_color_icon():
    img = Image.new("RGBA", COLOR_SIZE, EU_BLUE)
    draw = ImageDraw.Draw(img)

    # Draw a white rounded rectangle as background badge
    margin = 20
    draw.rounded_rectangle(
        [margin, margin, COLOR_SIZE[0] - margin, COLOR_SIZE[1] - margin],
        radius=24,
        fill=EU_BLUE,
        outline=EU_YELLOW,
        width=6,
    )

    # Draw "EU" label
    cx, cy = COLOR_SIZE[0] // 2, COLOR_SIZE[1] // 2 - 20
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except (IOError, OSError):
        font = ImageFont.load_default()
        small_font = font

    draw.text((cx, cy), "EU", font=font, fill=EU_YELLOW, anchor="mm")
    draw.text((cx, cy + 46), "AI Act", font=small_font, fill=WHITE, anchor="mm")

    path = OUTPUT_DIR / "color.png"
    img.save(path, "PNG")
    print(f"✅  color.png  → {path}")


# ─── Outline icon (32 × 32) ───────────────────────────────────────────────────
OUTLINE_SIZE = (32, 32)
TRANSPARENT = (0, 0, 0, 0)
OUTLINE_WHITE = (255, 255, 255, 255)

def make_outline_icon():
    img = Image.new("RGBA", OUTLINE_SIZE, TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Simple white rounded square outline
    draw.rounded_rectangle(
        [2, 2, 29, 29],
        radius=5,
        fill=None,
        outline=OUTLINE_WHITE,
        width=2,
    )

    # "EU" text in white (small)
    cx, cy = OUTLINE_SIZE[0] // 2, OUTLINE_SIZE[1] // 2
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except (IOError, OSError):
        font = ImageFont.load_default()

    draw.text((cx, cy), "EU", font=font, fill=OUTLINE_WHITE, anchor="mm")

    path = OUTPUT_DIR / "outline.png"
    img.save(path, "PNG")
    print(f"✅  outline.png → {path}")


if __name__ == "__main__":
    make_color_icon()
    make_outline_icon()
    print("\nDone. Replace these placeholder icons with your own branded versions before publishing.")
