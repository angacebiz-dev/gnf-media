"""Crop museum scans for documentary long-forms (Nov 19, 2026). python3 doc_crop.py <dir> key=auto|x0,y0,x1,y1(fractions)|keep ...
auto = trim paper margins: rows/cols whose share of pixels darker than THR is below FRAC are margin. Long side capped at 3000 px."""
import sys, numpy as np
from PIL import Image
D = sys.argv[1]
for arg in sys.argv[2:]:
    k, how = arg.split("=")
    im = Image.open(f"{D}/img/{k}.jpg").convert("RGB"); a = np.asarray(im.convert("L"), np.float32)
    if how.startswith("auto"):
        thr, frac = (165, 0.06) if how == "auto" else (int(how.split(":")[1]), float(how.split(":")[2]))
        dark = a < thr
        r = np.where(dark.mean(1) > frac)[0]; c = np.where(dark.mean(0) > frac)[0]
        y0, y1, x0, x1 = r[0], r[-1], c[0], c[-1]
        pad = int(0.004 * max(im.size)); box = (max(0, x0 + pad), max(0, y0 + pad), min(im.width, x1 - pad), min(im.height, y1 - pad))
    elif how == "keep": box = (0, 0, im.width, im.height)
    else:
        f = [float(v) for v in how.split(",")]; box = (int(f[0] * im.width), int(f[1] * im.height), int(f[2] * im.width), int(f[3] * im.height))
    out = im.crop(box); s = 3000 / max(out.size)
    if s < 1: out = out.resize((int(out.width * s), int(out.height * s)), Image.LANCZOS)
    out.save(f"{D}/p/{k}.jpg", quality=92); print(k, box, out.size)
