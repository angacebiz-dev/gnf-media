import os
"""bgs5 (Nov 19, 2026): procedural backgrounds for the 5 toon Shorts. World canvas WW x HH (1.5x a 720x1280 frame).
bg(key) -> list of (RGBA layer, parallax). Looks: dg = warm golden 2.5D with depth blur; dn = night, deep blue + lamp orange;
el = comic flat colours + black outlines; pt = storybook watercolour washes on paper; pr = paper cut-out, flat colours + drop shadows."""
import math, random, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

WW, HH = 1080, 1920

def grad(top, bot, h=HH, w=WW, curve=1.0):
    a = (np.linspace(0, 1, h) ** curve)[:, None, None]
    g = np.array(top)[None, None] * (1 - a) + np.array(bot)[None, None] * a
    return Image.fromarray(np.repeat(g, w, 1).astype(np.uint8)).convert("RGBA")

def ridge(y0, amp, seed, n=7, w=WW):
    r = random.Random(seed); ph = [r.uniform(0, 6.28) for _ in range(n)]
    return [(x, y0 + sum(amp / (k + 1) * math.sin(x / w * (k + 1) * 3.1 + ph[k]) for k in range(n))) for x in range(0, w + 9, 8)]

def layer(): return Image.new("RGBA", (WW, HH), (0, 0, 0, 0))

def soft(L, r):
    """alpha-correct blur (no dark fringes): blur colour*alpha and alpha, then divide"""
    a = np.asarray(L, np.float32); al = a[..., 3:4] / 255.0
    pm = Image.fromarray(np.clip(a[..., :3] * al, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    ab = Image.fromarray((al[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    A = np.asarray(ab, np.float32)[..., None] / 255.0
    rgb = np.asarray(pm, np.float32) / np.maximum(A, 1e-3)
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), A * 255]).astype(np.uint8), "RGBA")

def poly_fill(L, pts, col, outline=None, w=0):
    d = ImageDraw.Draw(L); d.polygon(pts, fill=col)
    if outline: d.line(pts + [pts[0]], fill=outline, width=w)

def hill(L, y0, amp, seed, col, outline=None, w=0, bottom=HH):
    pts = ridge(y0, amp, seed); poly_fill(L, pts + [(WW, bottom), (0, bottom)], col, outline, w)

def shadowed(L, off=(10, 14), blur=10, alpha=110):
    """paper cut-out: drop shadow under a layer's shapes"""
    a = L.split()[3]; sh = Image.new("RGBA", L.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: int(v * alpha / 255)).filter(ImageFilter.GaussianBlur(blur)))
    out = layer(); out.alpha_composite(sh, off); out.alpha_composite(L); return out

def watercolour(L, seed=0, blur=3):
    """storybook: soften shapes, darken edges like pigment pooling, add paper grain"""
    a = L.split()[3]; soft = L.filter(ImageFilter.GaussianBlur(blur))
    edge = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(5)), a.filter(ImageFilter.MinFilter(9)))
    rnd = Image.effect_noise(L.size, 40).filter(ImageFilter.GaussianBlur(6))
    out = soft.copy(); dark = Image.new("RGBA", L.size, (60, 40, 50, 0)); dark.putalpha(ImageChops.multiply(edge, rnd).point(lambda v: int(v * 0.35)))
    out.alpha_composite(dark); out.putalpha(ImageChops.multiply(soft.split()[3], rnd.point(lambda v: 200 + v // 5)))
    return out

def paper_tex(im, k=0.10):
    n = Image.effect_noise(im.size, 30).filter(ImageFilter.GaussianBlur(1.2)).convert("RGB")
    return Image.blend(im.convert("RGB"), ImageChops.multiply(im.convert("RGB"), Image.merge("RGB", [n.split()[0].point(lambda v: 205 + v // 5)] * 3)), k * 4).convert("RGBA")

def tent(d, x, y, s, col, sh, out=(28, 22, 24), w=4, flag=None):
    d.polygon([(x - s, y), (x, y - s * 0.95), (x + s, y)], fill=col, outline=out); d.line([(x - s, y), (x, y - s * 0.95), (x + s, y)], fill=out, width=w)
    d.polygon([(x, y - s * 0.95), (x + s, y), (x + s * 0.25, y)], fill=sh)
    d.polygon([(x - s * 0.18, y), (x, y - s * 0.4), (x + s * 0.18, y)], fill=(40, 30, 26))
    if flag:
        d.line([(x, y - s * 0.95), (x, y - s * 1.45)], fill=out, width=w); d.polygon([(x, y - s * 1.45), (x + s * 0.45, y - s * 1.32), (x, y - s * 1.2)], fill=flag, outline=out)

def stars(L, n, seed, ymax):
    d = ImageDraw.Draw(L); r = random.Random(seed)
    for _ in range(n):
        x, y, s = r.uniform(0, WW), r.uniform(0, ymax), r.choice((1, 1, 2, 2, 3))
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 250, 230, r.randint(120, 255)))

def glow(L, x, y, r, col, a=180):
    m = Image.new("L", L.size, 0); ImageDraw.Draw(m).ellipse([x - r, y - r, x + r, y + r], fill=a)
    g = Image.new("RGBA", L.size, col + (0,)); g.putalpha(m.filter(ImageFilter.GaussianBlur(r * 0.45))); L.alpha_composite(g)

# ---------------------------------------------------------------- A: David & Goliath (warm golden, depth blur)
def dg(key):
    sky = grad((255, 214, 150), (250, 236, 200), curve=0.8); glow(sky, WW * 0.72, HH * 0.30, 260, (255, 246, 210), 200)
    far = layer(); hill(far, HH * 0.46, 70, 3, (196, 160, 130, 255)); hill(far, HH * 0.52, 50, 4, (176, 140, 104, 255)); far = soft(far, 7)
    if key == "valley":
        mid = layer(); d = ImageDraw.Draw(mid)
        poly_fill(mid, [(0, HH * 0.55), (WW * 0.35, HH * 0.6), (WW * 0.42, HH * 0.75), (0, HH * 0.78)], (150, 134, 70, 255))
        poly_fill(mid, [(WW, HH * 0.53), (WW * 0.64, HH * 0.6), (WW * 0.57, HH * 0.75), (WW, HH * 0.78)], (160, 128, 70, 255))
        for k in range(5): tent(d, 60 + k * 70, HH * 0.6 + k * 4, 34, (236, 226, 200), (196, 184, 156), w=3, flag=(60, 100, 190) if k % 2 else None)
        for k in range(5): tent(d, WW - 60 - k * 70, HH * 0.585 + k * 4, 36, (200, 120, 90), (160, 90, 66), w=3, flag=(190, 50, 40) if k % 2 == 0 else None)
        mid = soft(mid, 2)
        near = layer(); hill(near, HH * 0.74, 22, 9, (190, 168, 92, 255)); d = ImageDraw.Draw(near)
        brook = [(WW * 0.38 + 30 * math.sin(y / 70), y) for y in range(int(HH * 0.74), HH, 20)]
        for x, y in brook: d.ellipse([x - 40 - (y - HH * 0.74) * 0.08, y - 12, x + 40 + (y - HH * 0.74) * 0.08, y + 12], fill=(110, 170, 200, 255))
        return [(sky, 0.2), (far, 0.35), (mid, 0.6), (near, 1.0)]
    if key == "camp":
        mid = layer(); d = ImageDraw.Draw(mid); hill(mid, HH * 0.66, 18, 7, (170, 150, 84, 255))
        for k in range(4): tent(d, 120 + k * 260, HH * 0.67, 120, (236, 226, 200), (196, 184, 156), w=6, flag=(60, 100, 190) if k % 2 else None)
        mid = soft(mid, 3)
        near = layer(); hill(near, HH * 0.80, 14, 11, (188, 166, 96, 255))
        return [(sky, 0.2), (far, 0.35), (mid, 0.6), (near, 1.0)]
    if key == "brook":
        near = layer(); hill(near, HH * 0.6, 16, 13, (150, 170, 80, 255)); d = ImageDraw.Draw(near)
        d.polygon([(0, HH * 0.72), (WW, HH * 0.68), (WW, HH * 0.86), (0, HH * 0.9)], fill=(110, 176, 210, 255))
        r = random.Random(5)
        for _ in range(40):
            x, y, s = r.uniform(0, WW), r.uniform(HH * 0.7, HH * 0.9), r.uniform(14, 34)
            d.ellipse([x - s, y - s * 0.6, x + s, y + s * 0.6], fill=(170, 164, 150, 255), outline=(28, 22, 24), width=4)
        for k in range(14): d.line([(r.uniform(0, WW), r.uniform(HH * 0.72, HH * 0.86)), (r.uniform(0, WW), r.uniform(HH * 0.72, HH * 0.86))], fill=(220, 240, 250, 140), width=3)
        return [(sky, 0.2), (soft(far, 6), 0.35), (near, 1.0)]
    if key == "lowsky":
        near = layer(); hill(near, HH * 0.86, 10, 15, (186, 160, 90, 255))
        clouds = layer(); d = ImageDraw.Draw(clouds); r = random.Random(8)
        for _ in range(9):
            x, y, s = r.uniform(0, WW), r.uniform(100, HH * 0.5), r.uniform(80, 160)
            d.ellipse([x - s * 1.6, y - s * 0.5, x + s * 1.6, y + s * 0.5], fill=(255, 248, 236, 170))
        return [(sky, 0.2), (soft(clouds, 14), 0.3), (near, 1.0)]
    raise KeyError(key)

# ---------------------------------------------------------------- B: Daniel (night, deep blue + lamp orange)
def dn(key):
    sky = grad((14, 18, 46), (54, 46, 96), curve=1.2)
    if key in ("dawn", "dentop_dawn"): sky = grad((90, 110, 170), (250, 170, 140), curve=0.9)
    stars(sky, 160 if "dawn" not in key else 20, 1, HH * 0.5)
    if key == "city":
        glow(sky, WW * 0.75, HH * 0.18, 70, (255, 246, 214), 255); glow(sky, WW * 0.75, HH * 0.18, 180, (150, 160, 230), 120)
        far = layer(); d = ImageDraw.Draw(far); r = random.Random(2)
        x = 0
        while x < WW:
            w, h = r.uniform(60, 140), r.uniform(120, 360); y = HH * 0.62 - h
            d.rectangle([x, y, x + w, HH * 0.7], fill=(22, 20, 44, 255))
            for k in range(int(h // 40)):
                if r.random() < 0.35: d.rectangle([x + w * 0.3, y + 20 + k * 40, x + w * 0.45, y + 34 + k * 40], fill=(255, 190, 90, 255))
            x += w + r.uniform(4, 20)
        for k in range(4): d.rectangle([WW * 0.25 - 150 + k * 50, HH * 0.62 - 420 + k * 90, WW * 0.25 + 150 - k * 50, HH * 0.62 - 330 + k * 90], fill=(18, 16, 38, 255))
        near = layer(); hill(near, HH * 0.7, 8, 3, (10, 10, 24, 255))
        return [(sky, 0.15), (soft(far, 1.5), 0.5), (near, 1.0)]
    if key == "room":
        wall = grad((50, 34, 40), (30, 20, 28)); d = ImageDraw.Draw(wall)
        wx0, wy0, wx1, wy1 = WW * 0.22, HH * 0.18, WW * 0.78, HH * 0.52
        win = sky.crop((0, 0, int(wx1 - wx0), int(wy1 - wy0))); glow(win, (wx1 - wx0) * 0.7, 140, 60, (255, 246, 214), 255)
        wall.paste(win, (int(wx0), int(wy0))); d.rectangle([wx0, wy0, wx1, wy1], outline=(16, 10, 14), width=26)
        d.line([((wx0 + wx1) / 2, wy0), ((wx0 + wx1) / 2, wy1)], fill=(16, 10, 14), width=16)
        d.rectangle([0, HH * 0.72, WW, HH], fill=(40, 26, 30, 255))
        glow(wall, WW * 0.2, HH * 0.62, 160, (255, 160, 70), 150)
        light = layer(); ImageDraw.Draw(light).polygon([(wx0, wy0), (wx1, wy0), (wx1 + 160, HH * 0.85), (wx0 + 40, HH * 0.85)], fill=(150, 170, 255, 40))
        return [(wall, 0.6), (soft(light, 30), 1.0)]
    if key == "palace":
        hall = grad((40, 22, 50), (20, 12, 26)); d = ImageDraw.Draw(hall)
        for k in range(5):
            x = 80 + k * 230; d.rectangle([x, HH * 0.15, x + 90, HH * 0.75], fill=(60, 40, 72)); d.rectangle([x - 14, HH * 0.15, x + 104, HH * 0.18], fill=(80, 56, 90)); glow(hall, x + 45, HH * 0.4, 50, (255, 170, 80), 140)
        d.rectangle([0, HH * 0.75, WW, HH], fill=(46, 28, 40)); d.rectangle([WW * 0.35, HH * 0.55, WW * 0.65, HH * 0.75], fill=(120, 30, 50))
        return [(hall, 0.7)]
    if key == "den":
        rock = grad((26, 22, 30), (12, 10, 14)); d = ImageDraw.Draw(rock); r = random.Random(4)
        for _ in range(60):
            x, y, s = r.uniform(0, WW), r.uniform(0, HH), r.uniform(40, 140); c = r.randint(26, 44)
            d.ellipse([x - s, y - s * 0.7, x + s, y + s * 0.7], fill=(c, c - 4, c + 6), outline=(8, 6, 10), width=6)
        d.rectangle([0, HH * 0.78, WW, HH], fill=(30, 24, 26))
        light = layer(); ImageDraw.Draw(light).polygon([(WW * 0.38, 0), (WW * 0.62, 0), (WW * 0.8, HH * 0.8), (WW * 0.2, HH * 0.8)], fill=(170, 190, 255, 55))
        return [(rock, 0.6), (soft(light, 40), 1.0)]
    if key in ("dentop", "dentop_dawn"):
        far = layer(); hill(far, HH * 0.55, 30, 6, (20, 18, 36, 255) if key == "dentop" else (90, 70, 90, 255))
        near = layer(); d = ImageDraw.Draw(near); hill(near, HH * 0.7, 10, 8, (34, 28, 40, 255) if key == "dentop" else (130, 100, 100, 255))
        d.ellipse([WW * 0.2, HH * 0.66, WW * 0.8, HH * 0.8], fill=(16, 12, 18, 255))
        d.rounded_rectangle([WW * 0.25, HH * 0.64, WW * 0.75, HH * 0.75], radius=30, fill=(90, 86, 96, 255) if key == "dentop" else (160, 150, 150, 255), outline=(10, 8, 12), width=10)
        d.ellipse([WW * 0.47, HH * 0.67, WW * 0.53, HH * 0.705], fill=(170, 40, 40, 255), outline=(10, 8, 12), width=5)
        return [(sky, 0.2), (far, 0.5), (near, 1.0)]
    raise KeyError(key)

# ---------------------------------------------------------------- C: Elijah (comic: flat colours, black outlines)
K = (0, 0, 0)
def el(key):
    if key == "burst":
        b = Image.new("RGBA", (WW, HH), (255, 214, 40, 255)); d = ImageDraw.Draw(b); cx, cy = WW / 2, HH * 0.45
        for k in range(28):
            a0, a1 = k / 28 * 2 * math.pi, (k + 0.5) / 28 * 2 * math.pi
            d.polygon([(cx, cy), (cx + math.cos(a0) * 2400, cy + math.sin(a0) * 2400), (cx + math.cos(a1) * 2400, cy + math.sin(a1) * 2400)], fill=(255, 140, 30, 255))
        return [(b, 0.4)]
    if key == "nightburst":
        b = Image.new("RGBA", (WW, HH), (40, 30, 80, 255)); d = ImageDraw.Draw(b); cx, cy = WW / 2, HH * 0.45
        for k in range(28):
            a0, a1 = k / 28 * 2 * math.pi, (k + 0.5) / 28 * 2 * math.pi
            d.polygon([(cx, cy), (cx + math.cos(a0) * 2400, cy + math.sin(a0) * 2400), (cx + math.cos(a1) * 2400, cy + math.sin(a1) * 2400)], fill=(80, 50, 140, 255))
        return [(b, 0.4)]
    storm = key in ("carmel_dark", "sky_fire")
    sky = Image.new("RGBA", (WW, HH), (110, 196, 250, 255) if not storm else (70, 60, 110, 255)); d = ImageDraw.Draw(sky)
    r = random.Random(3)
    for _ in range(6):
        x, y, s = r.uniform(0, WW), r.uniform(80, HH * 0.4), r.uniform(70, 130)
        for k in range(3): d.ellipse([x - s + k * s * 0.6, y - s * 0.5 - (k % 2) * 30, x + k * s * 0.6, y + s * 0.4], fill=(255, 255, 255) if not storm else (110, 100, 150), outline=K, width=7)
    if key == "sky_fire": return [(sky, 0.3)]
    mid = layer(); hill(mid, HH * 0.56, 60, 2, (120, 170, 90, 255), K, 8)
    near = layer(); dd = ImageDraw.Draw(near)
    poly_fill(near, [(0, HH * 0.68), (WW, HH * 0.66), (WW, HH), (0, HH)], (214, 180, 120, 255), K, 8)
    if key == "crowd":
        for row in range(2):
            for k in range(11):
                x = k * 105 + (row * 50); y = HH * (0.74 + row * 0.06)
                c = random.Random(k * 7 + row).choice([(230, 90, 70), (90, 140, 210), (240, 200, 80), (120, 180, 120)])
                dd.ellipse([x - 50, y - 160, x + 50, y - 60], fill=(240, 214, 180), outline=K, width=7); dd.rounded_rectangle([x - 60, y - 70, x + 60, y + 90], radius=40, fill=c, outline=K, width=7)
    return [(sky, 0.25), (mid, 0.55), (near, 1.0)]

# ---------------------------------------------------------------- D: Peter (storybook watercolour)
def pt(key):
    calm = key == "sea_calm"
    sky = grad((70, 80, 140), (170, 150, 190)) if not calm else grad((250, 200, 180), (250, 236, 210))
    if not calm: glow(sky, WW * 0.7, HH * 0.15, 70, (255, 248, 220), 255); stars(sky, 60, 2, HH * 0.4)
    clouds = layer(); d = ImageDraw.Draw(clouds); r = random.Random(7)
    for _ in range(12):
        x, y, s = r.uniform(-100, WW + 100), r.uniform(60, HH * 0.42), r.uniform(80, 200)
        d.ellipse([x - s * 1.5, y - s * 0.45, x + s * 1.5, y + s * 0.45], fill=(110, 110, 160, 200) if not calm else (255, 230, 220, 200))
    clouds = watercolour(clouds, 1, 10)
    sea = layer(); d = ImageDraw.Draw(sea)
    top = HH * (0.5 if key != "deck" else 0.42)
    for k in range(9):
        y = top + k * 90; a = 18 + k * 6 if not calm else 6
        pts = [(x, y + a * math.sin(x / 70 + k * 1.3)) for x in range(-10, WW + 20, 12)]
        col = (60 + k * 6, 100 + k * 8, 160 + k * 6, 255) if not calm else (150 + k * 6, 180 + k * 5, 210, 255)
        d.polygon(pts + [(WW + 20, HH), (-10, HH)], fill=col)
        d.line(pts, fill=(235, 240, 250, 200), width=6)
    sea = watercolour(sea, 2, 2)
    return [(sky, 0.2), (clouds, 0.35), (sea, 1.0)]

# ---------------------------------------------------------------- E: Prodigal son (paper cut-out)
def pr(key):
    if key == "city":
        sky = Image.new("RGBA", (WW, HH), (255, 120, 150, 255)); glow(sky, WW * 0.3, HH * 0.2, 200, (255, 230, 120), 220)
    elif key in ("road", "feast"):
        sky = grad((255, 150, 90), (255, 220, 140))
    elif key == "pigpen":
        sky = Image.new("RGBA", (WW, HH), (226, 206, 150, 255))
    else:
        sky = Image.new("RGBA", (WW, HH), (130, 210, 240, 255)); glow(sky, WW * 0.8, HH * 0.12, 90, (255, 240, 120), 255)
    far = layer(); d = ImageDraw.Draw(far)
    if key == "city":
        r = random.Random(3); x = 0
        while x < WW:
            w, h = r.uniform(90, 170), r.uniform(220, 520); c = r.choice([(250, 200, 80), (120, 80, 200), (60, 200, 180), (250, 110, 60)])
            d.rectangle([x, HH * 0.62 - h, x + w, HH * 0.7], fill=c + (255,))
            for k in range(int(h // 70)): d.rectangle([x + w * 0.3, HH * 0.62 - h + 30 + k * 70, x + w * 0.55, HH * 0.62 - h + 60 + k * 70], fill=(255, 250, 220, 255))
            x += w + 10
        for k in range(9): d.ellipse([60 + k * 115 - 16, HH * 0.3 - 16 + (k % 2) * 30, 60 + k * 115 + 16, HH * 0.3 + 16 + (k % 2) * 30], fill=(255, 240, 120, 255))
    else:
        hill(far, HH * 0.55, 40, 5, (120, 200, 110, 255) if key not in ("pigpen",) else (190, 160, 100, 255))
        if key in ("farm", "road", "feast"):
            hx = WW * (0.72 if key == "farm" else 0.82); hy = HH * (0.6 if key == "farm" else 0.56); s = 170 if key == "farm" else 90
            d.rectangle([hx - s, hy - s, hx + s, hy + s * 0.4], fill=(250, 236, 200, 255)); d.polygon([(hx - s * 1.2, hy - s), (hx, hy - s * 1.8), (hx + s * 1.2, hy - s)], fill=(220, 80, 60, 255))
            d.rectangle([hx - s * 0.25, hy - s * 0.3, hx + s * 0.25, hy + s * 0.4], fill=(140, 90, 50, 255))
    far = shadowed(far, (6, 10), 8, 90)
    near = layer(); d = ImageDraw.Draw(near)
    if key == "road":
        hill(near, HH * 0.66, 12, 9, (100, 180, 90, 255)); d.polygon([(WW * 0.46, HH * 0.6), (WW * 0.56, HH * 0.6), (WW * 0.95, HH), (WW * 0.1, HH)], fill=(230, 200, 150, 255))
    elif key == "pigpen":
        hill(near, HH * 0.68, 8, 4, (160, 120, 80, 255)); r = random.Random(6)
        for _ in range(12): x, y = r.uniform(0, WW), r.uniform(HH * 0.72, HH); d.ellipse([x - 70, y - 18, x + 70, y + 18], fill=(130, 96, 66, 255))
        for k in range(8): d.rectangle([k * 150 + 20, HH * 0.62, k * 150 + 44, HH * 0.76], fill=(170, 120, 70, 255))
        d.rectangle([0, HH * 0.65, WW, HH * 0.67], fill=(170, 120, 70, 255)); d.rectangle([0, HH * 0.71, WW, HH * 0.73], fill=(170, 120, 70, 255))
    elif key == "feast":
        hill(near, HH * 0.7, 6, 10, (120, 200, 110, 255)); d.rounded_rectangle([WW * 0.1, HH * 0.73, WW * 0.9, HH * 0.78], radius=20, fill=(190, 120, 70, 255))
        for k in range(8): d.ellipse([140 + k * 105 - 26, HH * 0.715, 140 + k * 105 + 26, HH * 0.735], fill=(250, 230, 120, 255))
        for k in range(10): d.line([(k * 120, HH * 0.3), (k * 120 + 120, HH * 0.32)], fill=(255, 255, 255, 255), width=4); d.ellipse([k * 120 - 18, HH * 0.3 - 18, k * 120 + 18, HH * 0.3 + 18], fill=(255, 200, 80, 255))
    else:
        hill(near, HH * 0.7, 10, 12, (90, 170, 90, 255) if key != "city" else (70, 50, 110, 255))
    near = shadowed(near, (8, 12), 10, 110)
    return [(paper_tex(sky), 0.2), (far, 0.5), (near, 1.0)]

HDBG = "/home/claude/gnf/hd/bg"
HDKEEP = {("el", "crowd"): [(2, 0.845)]}
HAZE = {"pt": (60, 70, 110)}          # (sid, key) -> indices of vector layers to keep on top of the painting
@functools.lru_cache(maxsize=8)
def bg(sid, key):
    f = f"{HDBG}/{sid}_{key}.png"
    if os.path.exists(f):
        from PIL import ImageEnhance
        im = Image.open(f).convert("RGB").resize((WW, HH), Image.LANCZOS)
        im = ImageEnhance.Contrast(im).enhance(0.82); im = ImageEnhance.Color(im).enhance(0.9)
        im = Image.blend(im, Image.new("RGB", im.size, HAZE.get(sid, (250, 226, 180))), 0.16).filter(ImageFilter.GaussianBlur(1.3))
        L = [(im.convert("RGBA"), 0.85)]
        if os.path.exists(f"{HDBG}/{sid}_{key}_over.png"): L.append((Image.open(f"{HDBG}/{sid}_{key}_over.png").convert("RGBA"), 1.0))
        if (sid, key) in HDKEEP:
            V = {"dg": dg, "dn": dn, "el": el, "pt": pt, "pr": pr}[sid](key)
            for i, ymax in HDKEEP[(sid, key)]:
                l = V[i][0].convert("RGBA"); a = l.split()[3]
                a.paste(0, (0, int(ymax * HH), WW, HH)); l.putalpha(a); L.append((l, V[i][1]))
        return L
    L = {"dg": dg, "dn": dn, "el": el, "pt": pt, "pr": pr}[sid](key)
    return [(l.convert("RGBA"), p) for l, p in L]
