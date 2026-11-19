"""Crop William Blake Job plates to the engraved picture (Nov 19, 2026): densest contiguous run of dark rows, then cols within it."""
import sys, numpy as np
from PIL import Image
def run(v, thr):
    best, cur, s0 = (0, 0, 0), 0, 0
    for i, x in enumerate(np.append(v > thr, False)):
        if x and cur == 0: s0 = i
        cur = cur + 1 if x else 0
        if not x and i > 0 and (i - s0) > best[0] and v[s0:i].size and (v[s0:i] > thr).all(): best = (i - s0, s0, i)
    return best[1], best[2]
for k in sys.argv[2:]:
    im = Image.open(f"{sys.argv[1]}/img/{k}.jpg").convert("RGB"); a = np.asarray(im.convert("L"), np.float32) < 150
    rows = np.convolve(a.mean(1), np.ones(15) / 15, "same"); y0, y1 = run(rows, 0.22)
    cols = np.convolve(a[y0:y1].mean(0), np.ones(15) / 15, "same"); x0, x1 = run(cols, 0.22)
    pad = 6; box = (x0 + pad, y0 + pad, x1 - pad, y1 - pad); out = im.crop(box); s = 3000 / max(out.size)
    if s < 1: out = out.resize((int(out.width * s), int(out.height * s)), Image.LANCZOS)
    out.save(f"{sys.argv[1]}/p/{k}.jpg", quality=92); print(k, box, out.size)
