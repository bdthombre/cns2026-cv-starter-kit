"""One click per instrument -> SAM 2 mask -> bounding box -> YOLO label line."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ultralytics import SAM

frame, out_img = sys.argv[1], sys.argv[2]
img = Image.open(frame).convert("RGB")
W, H = img.size
objs = [("suction", 0, [740, 610], (255, 162, 77)), ("ring curette", 1, [712, 372], (90, 200, 250))]

sam = SAM("sam2.1_b.pt")
res = sam(frame, points=[o[2] for o in objs], labels=[1] * len(objs), verbose=False)[0]
masks = res.masks.data.cpu().numpy().astype(bool)

arr = np.array(img).astype(float)
for m, (_, _, _, c) in zip(masks, objs):
    arr[m] = arr[m] * 0.6 + np.array(c) * 0.4
im = Image.fromarray(arr.astype(np.uint8))
d = ImageDraw.Draw(im)
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
for m, (name, cls, (px, py), c) in zip(masks, objs):
    ys, xs = np.where(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    d.rectangle([x0, y0, x1, y1], outline=c, width=5)
    tw = d.textlength(name, font=font)
    ty = max(y0 - 44, 4)
    d.rectangle([x0, ty, x0 + tw + 20, ty + 40], fill=c)
    d.text((x0 + 10, ty + 3), name, fill=(23, 25, 28), font=font)
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    cx, cy, bw, bh = (x0 + x1) / 2 / W, (y0 + y1) / 2 / H, (x1 - x0) / W, (y1 - y0) / H
    print(f"{cls} {cx:.3f} {cy:.3f} {bw:.3f} {bh:.3f}   # {name}")
im.crop((240, 0, 1014, 720)).save(out_img, quality=90)
