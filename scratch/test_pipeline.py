import os
import glob
from PIL import Image, ImageDraw

outfits_dir = "/Users/mon/Snap and Print photo edit/outfits"
png_files = sorted(glob.glob(f"{outfits_dir}/*.png"))

print(f"Found {len(png_files)} outfit PNG assets:")
for f in png_files:
    img = Image.open(f)
    print(f" - {os.path.basename(f)}: size={img.size}, mode={img.mode}")

# Create a test composite simulating an ID photo
test_bg = Image.new("RGBA", (1200, 1600), (255, 255, 255, 255))
# Simulate person head & neck
person_layer = Image.new("RGBA", (1200, 1600), (0, 0, 0, 0))
draw = ImageDraw.Draw(person_layer)

# Face center (600, 600), chin at Y=850, face height = 500
face_cx = 600
chin_y = 850
face_h = 500

# Draw head & neck & old green t-shirt
draw.ellipse([420, 350, 780, 850], fill=(235, 195, 170, 255)) # Head
draw.rectangle([510, 780, 690, 1100], fill=(225, 185, 160, 255)) # Neck
draw.polygon([(250, 1600), (450, 1050), (750, 1050), (950, 1600)], fill=(34, 139, 34, 255)) # Old Green Shirt

# Simulate Smart Inpainting & Masking
# 1. Base Studio BG
test_bg = Image.new("RGBA", (1200, 1600), (255, 255, 255, 255))

# 2. Draw Synthesized Neck Skin directly on canvas
neck_draw = ImageDraw.Draw(test_bg)
neck_draw.polygon([
    (face_cx - 120, chin_y - 20),
    (face_cx - 140, chin_y + 200),
    (face_cx + 140, chin_y + 200),
    (face_cx + 120, chin_y - 20)
], fill=(232, 194, 168, 255))

# 3. Person Layer: Head with old clothing erased outside neck
# Erase old clothing below chin
for y in range(int(chin_y + 20), 1600):
    for x in range(0, 1200):
        person_layer.putpixel((x, y), (0, 0, 0, 0))

test_bg.paste(person_layer, (0, 0), person_layer)

# 4. Paste Men Black Suit
suit_img = Image.open(f"{outfits_dir}/men_suit_black.png").convert("RGBA")
suit_w = int(face_h * 2.60)
suit_h = suit_w
suit_img = suit_img.resize((suit_w, suit_h), Image.Resampling.LANCZOS)

suit_x = int(face_cx - suit_w / 2)
suit_y = int((chin_y + face_h * 0.05) - (suit_h * (145 / 1000)))

test_bg.paste(suit_img, (suit_x, suit_y), suit_img)
output_path = "/Users/mon/Snap and Print photo edit/scratch/test_composite_result.png"
test_bg.save(output_path)
print(f"\nVerification composite saved to {output_path} successfully!")
