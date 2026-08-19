import os
import glob
from PIL import Image

out_dir = "/Users/mon/Snap and Print photo edit/outfits"
pngs = glob.glob(os.path.join(out_dir, "*.png"))

print("Outfit details:")
for p in sorted(pngs):
    img = Image.open(p)
    w, h = img.size
    # Find topmost solid pixel near center (X: 450 to 550)
    alpha = img.split()[-1]
    top_y = -1
    for y in range(h):
        row = [alpha.getpixel((x, y)) for x in range(400, 600)]
        if any(v > 50 for v in row):
            top_y = y
            break
    
    # Find leftmost and rightmost solid pixel at Y = 400 (shoulder level)
    left_x, right_x = -1, -1
    for x in range(w):
        if alpha.getpixel((x, 400)) > 50:
            if left_x == -1: left_x = x
            right_x = x
            
    print(f"'{os.path.basename(p)}': top_collar_y={top_y}, shoulder_width={right_x - left_x if left_x != -1 else w}")
