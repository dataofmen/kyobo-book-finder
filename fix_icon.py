#!/usr/bin/env python3
from PIL import Image
import sys

# 원본 이미지 로드
img = Image.open('icons/app-icon.png')
print(f"원본 크기: {img.size}")

# 정사각형으로 크롭 (중앙 기준)
width, height = img.size
size = min(width, height)
left = (width - size) // 2
top = (height - size) // 2
right = left + size
bottom = top + size

img_cropped = img.crop((left, top, right, bottom))
print(f"크롭 후: {img_cropped.size}")

# 512x512로 리사이즈
img_resized = img_cropped.resize((512, 512), Image.Resampling.LANCZOS)
print(f"리사이즈 후: {img_resized.size}")

# 저장
img_resized.save('icons/app-icon-512.png', 'PNG', optimize=True)
print("✅ icons/app-icon-512.png 저장 완료!")

# 192x192도 생성
img_192 = img_cropped.resize((192, 192), Image.Resampling.LANCZOS)
img_192.save('icons/app-icon-192.png', 'PNG', optimize=True)
print("✅ icons/app-icon-192.png 저장 완료!")
