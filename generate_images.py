#!/usr/bin/env python3
"""
Generate icon and presplash images for WhatsApp Blaster
Run this script to create the required images
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

print("Generating WhatsApp Blaster images...")

# 1. Create Icon (512x512)
print("\n✓ Creating icon.png (512x512)...")
icon = Image.new('RGB', (512, 512), color=(25, 118, 210))  # Material Blue

# Draw circle background
draw = ImageDraw.Draw(icon)
draw.ellipse([10, 10, 502, 502], fill=(33, 150, 243))  # Brighter blue

# Draw message bubble (envelope-like)
draw.polygon([
    (150, 180),  # Top left
    (362, 180),  # Top right
    (362, 320),  # Bottom right
    (150, 320),  # Bottom left
], fill=(255, 255, 255))  # White

# Draw triangle flap
draw.polygon([
    (150, 180),
    (362, 180),
    (256, 250),
], fill=(255, 255, 255))

# Draw WhatsApp-like checkmark
draw.line([(180, 280), (220, 320)], fill=(76, 175, 80), width=8)
draw.line([(220, 320), (340, 200)], fill=(76, 175, 80), width=8)

icon.save('data/icon.png')
print("  → Icon saved to data/icon.png")

# 2. Create Presplash (1280x720)
print("✓ Creating presplash.png (1280x720)...")
presplash = Image.new('RGB', (1280, 720), color=(25, 118, 210))  # Material Blue

# Create gradient-like effect with rectangles
draw = ImageDraw.Draw(presplash)

# Draw background gradient (top to bottom)
for i in range(720):
    ratio = i / 720
    r = int(25 + (70 - 25) * ratio)
    g = int(118 + (180 - 118) * ratio)
    b = int(210 + (230 - 210) * ratio)
    draw.line([(0, i), (1280, i)], fill=(r, g, b))

# Draw large message bubble in center
bubble_x1, bubble_y1 = 250, 200
bubble_x2, bubble_y2 = 1030, 500

# Draw rounded rectangle (message bubble)
arc_radius = 40
draw.rectangle([bubble_x1 + arc_radius, bubble_y1, bubble_x2 - arc_radius, bubble_y2], 
               fill=(255, 255, 255))
draw.rectangle([bubble_x1, bubble_y1 + arc_radius, bubble_x2, bubble_y2 - arc_radius], 
               fill=(255, 255, 255))
draw.ellipse([bubble_x1, bubble_y1, bubble_x1 + arc_radius * 2, bubble_y1 + arc_radius * 2], 
             fill=(255, 255, 255))
draw.ellipse([bubble_x2 - arc_radius * 2, bubble_y1, bubble_x2, bubble_y1 + arc_radius * 2], 
             fill=(255, 255, 255))
draw.ellipse([bubble_x1, bubble_y2 - arc_radius * 2, bubble_x1 + arc_radius * 2, bubble_y2], 
             fill=(255, 255, 255))
draw.ellipse([bubble_x2 - arc_radius * 2, bubble_y2 - arc_radius * 2, bubble_x2, bubble_y2], 
             fill=(255, 255, 255))

# Draw tail
tail_points = [(bubble_x1 + 80, bubble_y2), (bubble_x1 + 20, bubble_y2 + 60), (bubble_x1 + 40, bubble_y2)]
draw.polygon(tail_points, fill=(255, 255, 255))

# Add text
try:
    # Try to use a larger font if available
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Title
title = "WhatsApp Blaster"
title_bbox = draw.textbbox((0, 0), title, font=font_large)
title_width = title_bbox[2] - title_bbox[0]
title_x = (1280 - title_width) // 2
draw.text((title_x, 100), title, fill=(255, 255, 255), font=font_large)

# Subtitle in bubble
subtitle = "Send messages to multiple contacts"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (1280 - subtitle_width) // 2
draw.text((subtitle_x, 300), subtitle, fill=(25, 118, 210), font=font_small)

# Footer text
footer = "Powered by Kivy"
footer_bbox = draw.textbbox((0, 0), footer, font=font_small)
footer_width = footer_bbox[2] - footer_bbox[0]
footer_x = (1280 - footer_width) // 2
draw.text((footer_x, 650), footer, fill=(200, 200, 200), font=font_small)

presplash.save('data/presplash.png')
print("  → Presplash saved to data/presplash.png")

print("\n✅ Images created successfully!")
print("\nFiles created:")
print("  • data/icon.png (512x512)")
print("  • data/presplash.png (1280x720)")
print("\nYou can now run: buildozer android release")
