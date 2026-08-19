import os
import glob
from PIL import Image, ImageFilter, ImageDraw

src_dir = "/Users/mon/.gemini/antigravity-ide/brain/a2fc95d8-6c8a-4d50-b2dc-98a5883e73d2"
out_dir = "/Users/mon/Snap and Print photo edit/outfits"
os.makedirs(out_dir, exist_ok=True)

image_map = {
    "men_suit_black": "gen_men_suit_black_*.jpg",
    "men_suit_navy": "gen_men_suit_navy_*.jpg",
    "men_suit_grey": "gen_men_suit_grey_*.jpg",
    "women_suit_black": "gen_women_suit_black_*.jpg",
    "women_suit_navy": "gen_women_suit_navy_*.jpg",
    "women_suit_beige": "gen_women_suit_beige_*.jpg",
    "thai_khaki_men": "gen_thai_khaki_1*.jpg",
    "thai_khaki_women": "gen_thai_khaki_women_*.jpg",
    "thai_white_men": "gen_thai_white_*.jpg",
    "shirt_men_tie": "gen_shirt_men_tie_*.jpg",
    "student_men": "gen_student_men_*.jpg",
    "student_women": "gen_student_women_*.jpg",
    "doctor_coat": "gen_doctor_coat_*.jpg",
}

def remove_background_and_neck(img, out_name):
    # Convert image to RGBA
    img = img.convert("RGBA")
    w, h = img.size
    
    # Get pixel data
    datas = img.getdata()
    
    newData = []
    # Build mask
    for item in datas:
        r, g, b, a = item
        # Check if white background
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        diff = max_c - min_c
        bright = (r + g + b) / 3
        
        if bright > 240 and diff < 20:
            # Fully transparent
            newData.append((r, g, b, 0))
        elif bright > 220 and diff < 15:
            # Feather edge
            alpha = int(255 * (1.0 - (bright - 220) / 20.0))
            newData.append((r, g, b, max(0, min(255, alpha))))
        else:
            newData.append((r, g, b, 255))
            
    img.putdata(newData)
    
    # Use ImageDraw to punch clean neck hole if skin or mannequin neck is present
    cx = w // 2
    draw = ImageDraw.Draw(img)
    
    if "student_women" in out_name:
        draw.ellipse([cx - int(w*0.13), -int(h*0.05), cx + int(w*0.13), int(h*0.21)], fill=(0,0,0,0))
    elif "student_men" in out_name:
        draw.ellipse([cx - int(w*0.14), -int(h*0.05), cx + int(w*0.14), int(h*0.20)], fill=(0,0,0,0))
    elif "women_suit_black" in out_name:
        draw.ellipse([cx - int(w*0.14), -int(h*0.05), cx + int(w*0.14), int(h*0.22)], fill=(0,0,0,0))
    elif "thai_khaki_women" in out_name:
        draw.ellipse([cx - int(w*0.13), -int(h*0.05), cx + int(w*0.13), int(h*0.18)], fill=(0,0,0,0))
    elif "thai_khaki_men" in out_name:
        draw.ellipse([cx - int(w*0.12), -int(h*0.05), cx + int(w*0.12), int(h*0.14)], fill=(0,0,0,0))
    elif "thai_white_men" in out_name:
        draw.ellipse([cx - int(w*0.12), -int(h*0.05), cx + int(w*0.12), int(h*0.13)], fill=(0,0,0,0))
    else:
        # Standard men suit collar hole clearance
        draw.ellipse([cx - int(w*0.13), -int(h*0.05), cx + int(w*0.13), int(h*0.15)], fill=(0,0,0,0))
        
    return img

def process_outfit(out_name, pattern):
    files = glob.glob(os.path.join(src_dir, pattern))
    if not files:
        print(f"File not found for {out_name}: {pattern}")
        return
    file_path = files[0]
    print(f"Processing {out_name} from {file_path}")
    
    img = Image.open(file_path)
    img = remove_background_and_neck(img, out_name)
    w, h = img.size
    
    # Get bounding box of non-transparent pixels
    bbox = img.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        center = (left + right) // 2
        half_w = max(center - left, right - center)
        new_left = max(0, center - half_w)
        new_right = min(w, center + half_w)
        
        cropped = img.crop((new_left, top, new_right, bottom))
        cw, ch = cropped.size
        
        # Standardize into 1000x1000 square with perfect shoulder centering
        final_img = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
        scale = min(960 / cw, 860 / ch)
        nw, nh = int(cw * scale), int(ch * scale)
        res_cropped = cropped.resize((nw, nh), Image.LANCZOS)
        
        offset_x = (1000 - nw) // 2
        offset_y = 130 # Place collar top around Y = 130-180
        
        final_img.paste(res_cropped, (offset_x, offset_y), res_cropped)
        
        out_path = os.path.join(out_dir, f"{out_name}.png")
        final_img.save(out_path, "PNG", optimize=True)
        print(f"-> Saved {out_path} ({final_img.size})")

for k, v in image_map.items():
    process_outfit(k, v)

print("All outfits converted to high-res transparent PNGs successfully!")
