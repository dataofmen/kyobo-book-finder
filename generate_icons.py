#!/usr/bin/env python3
"""
Generate PNG icons from SVG for PWA
Requires: pip install cairosvg pillow
"""

import os
from pathlib import Path

try:
    import cairosvg
    from PIL import Image
    import io
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'cairosvg', 'pillow'])
    import cairosvg
    from PIL import Image
    import io

# Icon sizes needed for PWA
SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def generate_icons():
    """Generate PNG icons from SVG"""
    svg_path = Path('icons/icon.svg')
    
    if not svg_path.exists():
        print(f"Error: {svg_path} not found")
        return
    
    print("Generating PNG icons from SVG...")
    
    for size in SIZES:
        output_path = Path(f'icons/icon-{size}x{size}.png')
        
        # Convert SVG to PNG using cairosvg
        png_data = cairosvg.svg2png(
            url=str(svg_path),
            output_width=size,
            output_height=size
        )
        
        # Save PNG
        with open(output_path, 'wb') as f:
            f.write(png_data)
        
        print(f"✓ Generated {output_path}")
    
    print(f"\n✅ Successfully generated {len(SIZES)} icon sizes!")

if __name__ == '__main__':
    generate_icons()
