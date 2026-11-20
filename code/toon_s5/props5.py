"""props5 (Nov 19, 2026): animals + props for the 5 toon Shorts, drawn in the toon5 look (thick outline, cel shade, big eyes).
Every function draws onto an RGBA image `im` in screen pixels: f(im, x, y, s, t, ...) where (x, y) = foot/base point, s = size unit (px)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
import toon5 as T

def _o(): return T.STYLE["out"]
def _lw(s): return max(2, int(s * 0.045 * T.STYLE["lw"]))
def _pz(c):
    p = T.STYLE["pastel"]
    return tuple(int(v + (250 - v) * p) for v in c) if p else c

def eye(d, x, y, r, look=(0, 0), closed=False):
    if closed:
        d.arc([x - r, y - r * 0.4, x + r, y + r], 200, 340, fill=_o(), width=max(2, int(r * 0.35))); return
    d.ellipse([x - r, y - r * 1.15, x + r, y + r * 1.15], fill=(255, 255, 255), outline=_o(), width=max(2, int(r * 0.25)))
    pr = r * 0.45; px, py = x + look[0] * r * 0.4, y + look[1] * r * 0.4 + r * 0.1
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=_o()); d.ellipse([px - pr * 0.5, py - pr * 0.7, px - pr * 0.05, py - pr * 0.25], fill=(255, 255, 255))

def lion(im, x, y, s, t=0.0, flip=False, mouth=0.0, sleepy=False, walk=0.0):
    """side-view lion, faces right (flip -> left). mouth 0 = shut, 1 = roaring."""
    W_, H_ = int(s * 3.2), int(s * 2.4)
    L = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(L); o = _o(); lw = _lw(s)
    body, bsh, mane, msh = _pz((214, 168, 92)), _pz((176, 132, 66)), _pz((150, 88, 40)), _pz((112, 62, 28))
    fy = H_ - s * 0.12; bx, by = s * 1.35, fy - s * 0.95
    ph = math.sin(walk * 2 * math.pi)
    for i, lx in enumerate((bx - s * 0.7, bx - s * 0.45, bx + s * 0.45, bx + s * 0.7)):
        sw = (ph if i % 2 else -ph) * s * 0.12
        d.line([(lx, by + s * 0.25), (lx + sw, fy - s * 0.05)], fill=o, width=int(lw * 4.2))
        d.line([(lx, by + s * 0.25), (lx + sw, fy - s * 0.05)], fill=bsh, width=int(lw * 2.4))
        d.ellipse([lx + sw - s * 0.12, fy - s * 0.12, lx + sw + s * 0.12, fy + s * 0.02], fill=body, outline=o, width=lw)
    tw = math.sin(t * 3) * s * 0.15
    d.line([(bx - s * 0.95, by), (bx - s * 1.3, by - s * 0.3 + tw), (bx - s * 1.25, by - s * 0.6 + tw)], fill=o, width=int(lw * 2.2), joint="curve")
    d.line([(bx - s * 0.95, by), (bx - s * 1.3, by - s * 0.3 + tw), (bx - s * 1.25, by - s * 0.6 + tw)], fill=body, width=lw, joint="curve")
    d.ellipse([bx - s * 1.37, by - s * 0.78 + tw, bx - s * 1.13, by - s * 0.5 + tw], fill=mane, outline=o, width=lw)
    d.ellipse([bx - s * 1.0, by - s * 0.42, bx + s * 0.9, by + s * 0.45], fill=body, outline=o, width=lw)
    d.chord([bx - s * 1.0, by - s * 0.1, bx + s * 0.9, by + s * 0.45], 0, 180, fill=bsh)
    d.ellipse([bx - s * 1.0, by - s * 0.42, bx + s * 0.9, by + s * 0.45], outline=o, width=lw)
    hx, hy = bx + s * 0.85, by - s * 0.45 + math.sin(t * 2) * s * 0.02
    pts = []
    for k in range(18):
        a = k / 18 * 2 * math.pi; r = s * (0.78 if k % 2 == 0 else 0.62)
        pts.append((hx + math.cos(a) * r, hy + math.sin(a) * r))
    d.polygon(pts, fill=mane, outline=o); d.line(pts + [pts[0]], fill=o, width=lw)
    d.ellipse([hx - s * 0.47, hy - s * 0.47, hx + s * 0.47, hy + s * 0.44], fill=body, outline=o, width=lw)
    for ex in (-0.32, 0.32):
        d.ellipse([hx + ex * s - s * 0.12, hy - s * 0.58, hx + ex * s + s * 0.12, hy - s * 0.36], fill=body, outline=o, width=lw)
    eye(d, hx + s * 0.05, hy - s * 0.12, s * 0.11, (0.6, 0), closed=sleepy)
    eye(d, hx + s * 0.30, hy - s * 0.12, s * 0.10, (0.6, 0), closed=sleepy)
    mzx, mzy = hx + s * 0.28, hy + s * 0.15
    d.ellipse([mzx - s * 0.22, mzy - s * 0.12, mzx + s * 0.22, mzy + s * 0.14], fill=_pz((236, 210, 160)), outline=o, width=lw)
    d.polygon([(mzx - s * 0.07, mzy - s * 0.1), (mzx + s * 0.07, mzy - s * 0.1), (mzx, mzy - s * 0.02)], fill=(60, 36, 30))
    if mouth > 0.05:
        mh = s * 0.30 * mouth
        d.ellipse([mzx - s * 0.16, mzy + s * 0.04, mzx + s * 0.16, mzy + s * 0.08 + mh], fill=(110, 30, 40), outline=o, width=lw)
        for k in (-1, 1): d.polygon([(mzx + k * s * 0.10, mzy + s * 0.06), (mzx + k * s * 0.06, mzy + s * 0.06), (mzx + k * s * 0.08, mzy + s * 0.14)], fill=(255, 255, 255))
    else:
        d.arc([mzx - s * 0.12, mzy + s * 0.0, mzx, mzy + s * 0.1], 0, 180, fill=o, width=lw)
        d.arc([mzx, mzy + s * 0.0, mzx + s * 0.12, mzy + s * 0.1], 0, 180, fill=o, width=lw)
    if flip: L = L.transpose(Image.FLIP_LEFT_RIGHT)
    im.alpha_composite(L, (int(x - W_ / 2), int(y - fy))) if 0 <= int(x - W_ / 2) and int(y - fy) >= 0 and int(x - W_ / 2) + W_ <= im.width and int(y - fy) + H_ <= im.height else im.paste(L, (int(x - W_ / 2), int(y - fy)), L)

def pig(im, x, y, s, t=0.0, flip=False, walk=0.0):
    W_, H_ = int(s * 2.6), int(s * 2.0)
    L = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(L); o = _o(); lw = _lw(s)
    pink, psh = _pz((242, 160, 170)), _pz((214, 120, 136))
    fy = H_ - s * 0.1; bx, by = s * 1.2, fy - s * 0.75
    ph = math.sin(walk * 2 * math.pi + t)
    for i, lx in enumerate((bx - s * 0.5, bx - s * 0.25, bx + s * 0.3, bx + s * 0.55)):
        sw = (ph if i % 2 else -ph) * s * 0.08
        d.rectangle([lx - s * 0.07 + sw, by + s * 0.2, lx + s * 0.07 + sw, fy], fill=psh, outline=o, width=lw)
    d.ellipse([bx - s * 0.85, by - s * 0.45, bx + s * 0.75, by + s * 0.42], fill=pink, outline=o, width=lw)
    d.chord([bx - s * 0.85, by - s * 0.0, bx + s * 0.75, by + s * 0.42], 0, 180, fill=psh); d.ellipse([bx - s * 0.85, by - s * 0.45, bx + s * 0.75, by + s * 0.42], outline=o, width=lw)
    d.arc([bx - s * 1.05, by - s * 0.25, bx - s * 0.8, by], 90, 360, fill=o, width=lw)
    hx, hy = bx + s * 0.75, by - s * 0.2
    d.ellipse([hx - s * 0.42, hy - s * 0.4, hx + s * 0.42, hy + s * 0.38], fill=pink, outline=o, width=lw)
    d.polygon([(hx - s * 0.3, hy - s * 0.3), (hx - s * 0.12, hy - s * 0.62), (hx - s * 0.02, hy - s * 0.32)], fill=psh, outline=o)
    eye(d, hx + s * 0.02, hy - s * 0.1, s * 0.09, (0.5, 0)); eye(d, hx + s * 0.22, hy - s * 0.1, s * 0.08, (0.5, 0))
    d.ellipse([hx + s * 0.2, hy + s * 0.04, hx + s * 0.52, hy + s * 0.28], fill=psh, outline=o, width=lw)
    for k in (0.31, 0.41): d.ellipse([hx + k * s - s * 0.025, hy + s * 0.12, hx + k * s + s * 0.025, hy + s * 0.2], fill=o)
    if flip: L = L.transpose(Image.FLIP_LEFT_RIGHT)
    im.paste(L, (int(x - W_ / 2), int(y - fy)), L)

def sheep(im, x, y, s, t=0.0, flip=False):
    W_, H_ = int(s * 2.4), int(s * 2.0)
    L = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(L); o = _o(); lw = _lw(s)
    wool, face = _pz((248, 246, 238)), _pz((70, 60, 56))
    fy = H_ - s * 0.1; bx, by = s * 1.1, fy - s * 0.75
    for lx in (bx - s * 0.4, bx - s * 0.15, bx + s * 0.25, bx + s * 0.45):
        d.line([(lx, by), (lx, fy)], fill=face, width=int(lw * 1.6))
    for k in range(9):
        a = k / 9 * 2 * math.pi
        d.ellipse([bx + math.cos(a) * s * 0.55 - s * 0.25, by + math.sin(a) * s * 0.3 - s * 0.25, bx + math.cos(a) * s * 0.55 + s * 0.25, by + math.sin(a) * s * 0.3 + s * 0.25], fill=wool, outline=o, width=lw)
    d.ellipse([bx - s * 0.6, by - s * 0.35, bx + s * 0.6, by + s * 0.35], fill=wool)
    hx, hy = bx + s * 0.7, by - s * 0.25 + math.sin(t * 2) * s * 0.03
    d.ellipse([hx - s * 0.25, hy - s * 0.3, hx + s * 0.28, hy + s * 0.32], fill=face, outline=o, width=lw)
    eye(d, hx + s * 0.06, hy - s * 0.06, s * 0.08, (0.5, 0))
    if flip: L = L.transpose(Image.FLIP_LEFT_RIGHT)
    im.paste(L, (int(x - W_ / 2), int(y - fy)), L)

def boat(im, x, y, s, t=0.0, front=None):
    """fishing boat, waterline at y; returns deck y (for placing people)."""
    d = ImageDraw.Draw(im); o = _o(); lw = _lw(s)
    rock = math.sin(t * 1.6) * s * 0.06
    wood, wsh = _pz((150, 96, 54)), _pz((112, 68, 36))
    pts = [(x - s * 1.9, y - s * 0.55 + rock), (x + s * 1.9, y - s * 0.55 - rock), (x + s * 1.45, y + s * 0.2), (x - s * 1.45, y + s * 0.2)]
    d.polygon(pts, fill=wood, outline=o); d.line(pts + [pts[0]], fill=o, width=lw)
    for k in (0.3, 0.55): d.line([(x - s * 1.8 + k * 0.4 * s, y - s * 0.55 + k * s * 0.7 + rock * (1 - k)), (x + s * 1.8 - k * 0.4 * s, y - s * 0.55 + k * s * 0.7 - rock * (1 - k))], fill=wsh, width=lw)
    d.line([(x, y - s * 0.55), (x, y - s * 3.2)], fill=o, width=int(lw * 2.2)); d.line([(x, y - s * 0.55), (x, y - s * 3.2)], fill=wood, width=lw)
    return y - s * 0.5

def altar(im, x, y, s, t=0.0, wet=0.0, fire=0.0, wood=True):
    d = ImageDraw.Draw(im); o = _o(); lw = _lw(s)
    rnd = random.Random(12)
    for row in range(3):
        n = 5 - row
        for k in range(n):
            sx = x + (k - (n - 1) / 2) * s * 0.42; sy = y - s * 0.22 - row * s * 0.34
            c = _pz((150 + rnd.randint(-15, 15), 146 + rnd.randint(-15, 15), 140 + rnd.randint(-10, 10)))
            if wet > 0: c = tuple(int(v * (1 - 0.35 * wet) + b * 0.35 * wet) for v, b in zip(c, (60, 110, 170)))
            d.rounded_rectangle([sx - s * 0.2, sy - s * 0.16, sx + s * 0.2, sy + s * 0.18], radius=int(s * 0.06), fill=c, outline=o, width=lw)
    if wood:
        for k in range(4):
            d.rounded_rectangle([x - s * 0.8, y - s * 1.13 - k * s * 0.1, x + s * 0.8, y - s * 1.05 - k * s * 0.1], radius=int(s * 0.04), fill=_pz((130, 84, 46)), outline=o, width=max(1, lw // 2))
    if wet > 0:
        d.ellipse([x - s * 1.4, y - s * 0.12, x + s * 1.4, y + s * 0.16], fill=_pz((90, 150, 210)), outline=o, width=lw)
    if fire > 0: flames(im, x, y - s * 1.2, s * 1.4 * fire, t)

def flames(im, x, y, s, t=0.0):
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for col, sc in (((240, 80, 30), 1.0), ((255, 170, 40), 0.72), ((255, 240, 150), 0.42)):
        pts = []
        for k in range(15):
            u = k / 14; xx = x - s * 0.7 * sc + u * s * 1.4 * sc
            h = s * (1.0 + 0.6 * math.sin(t * 9 + k * 1.7)) * sc * (0.4 + math.sin(u * math.pi))
            pts.append((xx, y - h))
        pts += [(x + s * 0.75 * sc, y), (x - s * 0.75 * sc, y)]
        d.polygon(pts, fill=col + (235,))
    glow = L.filter(ImageFilter.GaussianBlur(max(2, s * 0.12)))
    im.alpha_composite(glow); im.alpha_composite(L)

def stone_proj(im, x, y, s):
    d = ImageDraw.Draw(im); d.ellipse([x - s, y - s * 0.8, x + s, y + s * 0.8], fill=_pz((150, 146, 140)), outline=_o(), width=max(2, int(s * 0.3)))
