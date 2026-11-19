"""v3 Jonah compositor: 2D camera moves on 3D background plates, toon3 characters, FX, Ricks-style captions.
usage: python3 comp3.py <frame_start> <frame_end>   -> comp3/c_#####.png (720x1280)
       python3 comp3.py --test t1,t2,...           -> /tmp/v3t_<t>.png"""
import os, sys, json, math, random
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots3 import BG, SHOTS, TIMES, LINES, STARTS, END, FPS, WHO
import toon3

D = os.path.dirname(os.path.abspath(__file__))
W, H = 720, 1280
ANCH = json.load(open(os.path.join(D, "anchors3.json")))
FD = "/home/claude/gnf/fonts/fontsource-montserrat-5.3.0/package/files/"
FONT = {}
def F(w, s):
    k = (w, s)
    if k not in FONT: FONT[k] = ImageFont.truetype(FD + f"montserrat-latin-{w}-normal.woff2", s)
    return FONT[k]
OUTL = (28, 22, 24)
def ease(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)

# ---------- talk envelopes (mouth flaps) ----------
ENV = {}
for i in range(len(LINES)):
    a, sr = sf.read(os.path.join(D, f"audio/l{i:02d}.wav"))
    hop = sr // FPS; n = len(a) // hop + 1
    ENV[i] = np.array([np.sqrt(np.mean(a[k * hop:(k + 1) * hop] ** 2)) if len(a[k * hop:(k + 1) * hop]) else 0 for k in range(n)])
    ENV[i] = ENV[i] / (ENV[i].max() + 1e-6)
def talk_at(t):
    for i, s0 in enumerate(STARTS):
        k = int((t - s0) * FPS)
        if 0 <= k < len(ENV[i]): return float(ENV[i][k])
    return 0.0

# ---------- captions: 1-3 word chunks, sentence case ----------
CAPS = []
for i, (txt, dur) in enumerate(LINES):
    words = txt.replace("...", "…").split()
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) >= 9 or w.endswith((",", ".", "?", "!", "…")): chunks.append(" ".join(cur)); cur = []
    if cur: chunks.append(" ".join(cur))
    tot = sum(len(c) + 3 for c in chunks); acc = 0.0
    for c in chunks:
        a = STARTS[i] + dur * 0.97 * acc / tot; acc += len(c) + 3; b = STARTS[i] + dur * 0.97 * acc / tot
        CAPS.append((a, b + 0.12, c))
def caption(im, t):
    for a, b, c in CAPS:
        if a <= t < b:
            pop = 1 + 0.12 * max(0.0, 1 - (t - a) / 0.08)
            f = F(800, int(60 * pop)); d = ImageDraw.Draw(im)
            tw = d.textlength(c, font=f); x = (W - tw) / 2; y = int(H * 0.70 - 30 * pop)
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
            ds.text((x + 4, y + 6), c, font=f, fill=(0, 0, 0, 150), stroke_width=7, stroke_fill=(0, 0, 0, 150))
            im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
            d = ImageDraw.Draw(im); d.text((x, y), c, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=OUTL)
            return

# ---------- 2D camera ----------
def shot_cam(k, u, t):
    li, f0, f1, bg, move, zoom, chars, fx = SHOTS[k]
    Z, cx, cy, rot = 1.0, 0.5, 0.5, 0.0
    if zoom:
        z0, key, up = zoom
        a = ANCH[bg][key]; Z = z0
        cx, cy = a[0], a[1] - up * a[3] * 0.95
    if move == "push": Z *= 1 + 0.07 * u
    elif move == "punch": Z *= 1 + 0.22 * (1 - ease(u * 5)) + 0.03 * u
    elif move == "pan": Z *= 1.30; cx = 0.5 + (u - 0.5) * 0.28
    elif move == "shake":
        r = random.Random(int(t * FPS) * 13 + k)
        Z *= 1.06 + 0.02 * u; cx += r.uniform(-0.006, 0.006); cy += r.uniform(-0.006, 0.006); rot = math.sin(t * 2.3) * 2.2 + r.uniform(-0.5, 0.5)
    half_w, half_h = 0.5 / Z, 0.5 / Z
    cx = min(max(cx, half_w), 1 - half_w); cy = min(max(cy, half_h), 1 - half_h)
    return Z, cx, cy, rot
def to_screen(x, y, Z, cx, cy):
    return (x - cx) * Z * W + W / 2, (y - cy) * Z * H + H / 2

PLATES = {}
def plate(bg, f):
    if BG.get(bg, {}).get("anim"):
        p = os.path.join(D, f"bg3/{bg}_{min(f, 999):03d}.png")
        while not os.path.exists(p) and f > 0: f -= 1; p = os.path.join(D, f"bg3/{bg}_{f:03d}.png")
        return Image.open(p).convert("RGB").resize((W, H), Image.BICUBIC)
    if bg not in PLATES: PLATES[bg] = Image.open(os.path.join(D, f"bg3/{bg}.png")).convert("RGB")
    return PLATES[bg]

# ---------- FX helpers ----------
random.seed(3)
DROPS = [(random.uniform(-100, W + 200), random.uniform(0, H), random.uniform(30, 70)) for _ in range(380)]
def fx_rain(im, t, a=1.0):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); sh = (t * 1700) % H
    for x, y, ln in DROPS:
        yy = (y + sh) % H; xx = x - yy * 0.3
        d.line([(xx, yy), (xx - ln * 0.3, yy + ln)], fill=(220, 230, 245, int(115 * a)), width=2)
    im.alpha_composite(lay)
def fx_flash(im, a):
    if a > 0: im.alpha_composite(Image.new("RGBA", im.size, (235, 240, 255, int(255 * min(1, a)))))
def fx_vignette(im, col=(0, 0, 0), strength=170):
    if not hasattr(fx_vignette, "m"):
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        fx_vignette.m = np.clip((r - 0.55) / 0.75, 0, 1) ** 1.6
    m = Image.fromarray((fx_vignette.m * strength).astype(np.uint8))
    lay = Image.new("RGBA", im.size, col + (255,)); lay.putalpha(m); im.alpha_composite(lay)
def outlined_ellipse(d, cx, cy, rx, ry, fill, w=4):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=OUTL, width=w)
def fx_rays(im, t, col=(255, 220, 140)):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    ox, oy = W * 0.62, -120
    for k in range(9):
        a = math.radians(70 + k * 6 + math.sin(t * 0.8 + k) * 1.5); L = 1900; wdt = math.radians(1.6 + (k % 3))
        p1 = (ox + math.cos(a - wdt) * L, oy + math.sin(a - wdt) * L); p2 = (ox + math.cos(a + wdt) * L, oy + math.sin(a + wdt) * L)
        d.polygon([(ox, oy), p1, p2], fill=col + (38,))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
def fx_glow(im, x, y, r, col=(255, 210, 120), a=150):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.polygon([(x - r * 0.35, -10), (x + r * 0.35, -10), (x + r * 1.1, y + r * 0.3), (x - r * 1.1, y + r * 0.3)], fill=col + (int(a * 0.5),))
    d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(r * 0.45)))
def fx_zzz(im, x, y, t, s):
    d = ImageDraw.Draw(im)
    for k in range(3):
        ph = (t * 0.7 + k / 3) % 1.0; f = F(900, int(s * (0.6 + 0.7 * ph)))
        d.text((x + ph * s * 1.5, y - ph * s * 2.4), "Z", font=f, fill=(255, 255, 255, int(255 * (1 - ph) ** 0.7)), stroke_width=5, stroke_fill=OUTL + (int(255 * (1 - ph) ** 0.7),))
def fx_speedlines(im, t, ymid):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = random.Random(int(t * FPS))
    for k in range(22):
        y = ymid + r.uniform(-260, 160); x = r.uniform(-200, W); L = r.uniform(120, 360)
        d.line([(x, y), (x + L, y)], fill=(255, 255, 255, r.randint(60, 140)), width=r.randint(2, 5))
    im.alpha_composite(lay)
def fx_dust(im, x, y, t, s):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(6):
        ph = (t * 2.2 + k / 6) % 1.0; rr = s * (0.12 + 0.25 * ph)
        d.ellipse([x - s * 0.5 - ph * s * 1.4 - rr, y - ph * s * 0.4 - rr, x - s * 0.5 - ph * s * 1.4 + rr, y - ph * s * 0.4 + rr], fill=(222, 196, 150, int(170 * (1 - ph))))
    im.alpha_composite(lay)
def draw_crate(d, x, y, s, rot):
    pts = [(-1, -1), (1, -1), (1, 1), (-1, 1)]; c, sn = math.cos(rot), math.sin(rot)
    P = [(x + (px * c - py * sn) * s, y + (px * sn + py * c) * s) for px, py in pts]
    d.polygon(P, fill=(150, 92, 48), outline=OUTL, width=4)
    d.line([P[0], P[2]], fill=OUTL, width=3); d.line([P[1], P[3]], fill=OUTL, width=3)
def draw_stone(d, x, y, s, k):
    outlined_ellipse(d, x, y, s, s * 0.75, (150 + k * 12, 145 + k * 10, 140 + k * 8), 3)
    d.arc([x - s * 0.6, y - s * 0.5, x + s * 0.2, y + s * 0.1], 200, 260, fill=(240, 240, 235), width=2)
def fx_splash(im, x, y, ph, s, col=(220, 240, 255)):
    d = ImageDraw.Draw(im); r = random.Random(7)
    for k in range(16):
        a = math.radians(r.uniform(200, 340)); v = r.uniform(0.6, 1.3) * s * 2.4
        px = x + math.cos(a) * v * ph; py = y + math.sin(a) * v * ph + 3.2 * s * ph * ph
        rr = s * 0.13 * (1 - ph * 0.6)
        outlined_ellipse(d, px, py, rr, rr * 1.2, col, 3)
def fx_steam(im, x, y, t, s):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(4):
        ph = (t * 1.3 + k / 4) % 1.0; side = -1 if k % 2 else 1
        cx_, cy_ = x + side * s * (0.55 + 0.4 * ph), y - ph * s * 1.3; rr = s * (0.12 + 0.18 * ph)
        d.ellipse([cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr], fill=(255, 255, 255, int(220 * (1 - ph))), outline=OUTL + (int(200 * (1 - ph)),), width=3)
    im.alpha_composite(lay)
def fx_drips(im, t):
    d = ImageDraw.Draw(im); r = random.Random(5)
    for k in range(7):
        x = r.uniform(40, W - 40); sp = r.uniform(0.6, 1.0); ph = (t * sp + r.random()) % 1.0
        y = -20 + ph * H * 0.9
        d.polygon([(x, y - 16), (x - 8, y), (x + 8, y)], fill=(170, 220, 160)); outlined_ellipse(d, x, y + 2, 8, 9, (170, 220, 160), 2)
def seaweed(im, hx, hy, s):
    d = ImageDraw.Draw(im); w = max(3, int(s * 0.045)); g = (40, 120, 50)
    for sx in (-1, 1):  # two strands hang down the sides of the head, clear of the eyes
        x0 = hx + sx * s * 0.30
        d.line([(x0, hy - s * 0.50), (x0 + sx * s * 0.14, hy - s * 0.25), (x0 + sx * s * 0.20, hy + s * 0.05), (x0 + sx * s * 0.17, hy + s * 0.22)], fill=g, width=w, joint="curve")
    d.line([(hx - s * 0.12, hy - s * 0.52), (hx + s * 0.02, hy - s * 0.42), (hx + s * 0.16, hy - s * 0.50)], fill=g, width=w, joint="curve")

# ---------- fish + underwater ----------
def underwater_bg(t, dark=0.0):
    a = np.linspace(0, 1, H)[:, None]
    top = np.array([40, 150, 200]) * (1 - dark) + np.array([10, 40, 80]) * dark
    bot = np.array([6, 30, 70]) * (1 - dark * 0.6)
    img = (top * (1 - a) + bot * a)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    im = Image.fromarray(img.astype(np.uint8)).convert("RGBA")
    fx_rays(im, t, (180, 230, 255))
    d = ImageDraw.Draw(im); r = random.Random(11)
    for k in range(40):
        x = r.uniform(0, W); sp = r.uniform(0.05, 0.2); y = (r.uniform(0, H) - t * sp * H) % H
        rr = r.uniform(3, 12)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(220, 245, 255, 170), width=2)
    return im
def draw_fish(im, cx, cy, s, t, mouth=0.0, face="calm", view="side", sweat=False):
    d = ImageDraw.Draw(im); body = (78, 112, 150); belly = (190, 205, 210); lw = max(4, int(s * 0.03))
    if view == "side":
        tail = [(cx - s * 1.0, cy), (cx - s * 1.55, cy - s * 0.55 + math.sin(t * 6) * s * 0.08), (cx - s * 1.45, cy + s * 0.55 + math.sin(t * 6) * s * 0.08)]
        d.polygon(tail, fill=body, outline=OUTL, width=lw)
        d.ellipse([cx - s * 1.15, cy - s * 0.62, cx + s * 1.05, cy + s * 0.62], fill=body, outline=OUTL, width=lw)
        d.chord([cx - s * 0.95, cy - s * 0.2, cx + s * 0.95, cy + s * 0.6], 0, 180, fill=belly)
        d.ellipse([cx - s * 1.15, cy - s * 0.62, cx + s * 1.05, cy + s * 0.62], outline=OUTL, width=lw)
        d.polygon([(cx - s * 0.2, cy - s * 0.58), (cx + s * 0.25, cy - s * 0.95), (cx + s * 0.45, cy - s * 0.52)], fill=body, outline=OUTL, width=lw)
        ex, ey = cx + s * 0.55, cy - s * 0.18
        outlined_ellipse(d, ex, ey, s * 0.17, s * 0.19, (255, 255, 255), lw)
        outlined_ellipse(d, ex + s * 0.05, ey + s * 0.02, s * 0.065, s * 0.075, OUTL, 1)
        if face == "stern": d.line([(ex - s * 0.18, ey - s * 0.26), (ex + s * 0.16, ey - s * 0.18)], fill=OUTL, width=lw)
        else: d.line([(ex - s * 0.16, ey - s * 0.17), (ex + s * 0.16, ey - s * 0.28)], fill=OUTL, width=lw)
        mo = s * (0.05 + 0.25 * mouth)
        d.pieslice([cx + s * 0.62, cy + s * 0.02 - mo, cx + s * 1.12, cy + s * 0.10 + mo], 150, 210, fill=(120, 30, 40), outline=OUTL, width=lw)
        for k in range(3): d.arc([cx + s * (0.05 + k * 0.12), cy - s * 0.25, cx + s * (0.25 + k * 0.12), cy + s * 0.25], 300, 60, fill=(50, 80, 110), width=lw)
        if sweat:
            sx, sy = cx + s * 0.85, cy - s * 0.55
            d.polygon([(sx, sy - s * 0.14), (sx - s * 0.07, sy), (sx + s * 0.07, sy)], fill=(160, 220, 255), outline=OUTL)
            outlined_ellipse(d, sx, sy + 2, s * 0.07, s * 0.07, (160, 220, 255), 3)
    else:   # front: huge open mouth
        d.ellipse([cx - s * 1.2, cy - s * 1.0, cx + s * 1.2, cy + s * 1.05], fill=body, outline=OUTL, width=lw)
        for side in (-1, 1):
            ex = cx + side * s * 0.62; ey = cy - s * 0.55
            outlined_ellipse(d, ex, ey, s * 0.24, s * 0.26, (255, 255, 255), lw)
            outlined_ellipse(d, ex - side * s * 0.05, ey + s * 0.04, s * 0.09, s * 0.1, OUTL, 1)
            d.line([(ex - s * 0.22, ey - s * 0.36 - side * s * 0.05), (ex + s * 0.22, ey - s * 0.36 + side * s * 0.05)], fill=OUTL, width=lw)
        mo = 0.35 + 0.65 * mouth
        d.ellipse([cx - s * 0.75, cy - s * 0.15, cx + s * 0.75, cy - s * 0.15 + s * 1.05 * mo], fill=(90, 18, 30), outline=OUTL, width=lw)
        d.ellipse([cx - s * 0.45, cy + s * 0.35 * mo, cx + s * 0.45, cy - s * 0.15 + s * 1.0 * mo], fill=(190, 70, 90))
        for k in range(-3, 4):
            x = cx + k * s * 0.18
            d.polygon([(x - s * 0.06, cy - s * 0.12), (x + s * 0.06, cy - s * 0.12), (x, cy + s * 0.02)], fill=(250, 248, 235), outline=OUTL)

def toon_sprite(who, ppu, view, pose, face, t, flip=False, look=(0, 0), talk=0.0, phase=0.0):
    return toon3.draw(None, 0, 0, ppu, who, view, pose, face, t, flip, look, ret=True, phase=phase, talk=talk)

def paste(im, spr, x, y):
    im.alpha_composite(spr, (int(x), int(y))) if x >= 0 and y >= 0 and x + spr.width <= im.width and y + spr.height <= im.height else im.paste(spr, (int(x), int(y)), spr)

# ---------- frame ----------
def frame(n):
    t = n / FPS
    k = max(i for i, (a, b) in enumerate(TIMES) if a <= t) if t >= 0 else 0
    a, b = TIMES[k]; u = (t - a) / max(0.01, b - a); fl = int((t - a) * FPS)
    li, f0, f1, bg, move, zoom, chars, fx = SHOTS[k]
    talk = talk_at(t)
    # ----- underwater shots: fully 2D -----
    if bg.startswith("u_"):
        im = underwater_bg(t, 0.5 if bg == "u_sink" else 0.15)
        if bg == "u_sink":
            spr, fo = toon_sprite("jonah", 120, "front", "panic", "scared", t)
            spr = spr.rotate(math.sin(t * 2) * 25 + 20, expand=True, resample=Image.BICUBIC)
            paste(im, spr, W / 2 - spr.width / 2, -120 + ease(u) * 520)
            sil = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sil)
            fx_x = -500 + u * 1500
            ds.ellipse([fx_x - 420, 980, fx_x + 420, 1220], fill=(5, 15, 30, 200)); ds.polygon([(fx_x - 400, 1100), (fx_x - 620, 960), (fx_x - 600, 1240)], fill=(5, 15, 30, 200))
            im.alpha_composite(sil.filter(ImageFilter.GaussianBlur(14)))
        elif bg == "u_fish":
            s = 230 + 140 * ease(u)
            draw_fish(im, W / 2, H * 0.40 + 20, s, t, mouth=0.5 + 0.5 * math.sin(t * 3) ** 2, view="front")
            spr, fo = toon_sprite("jonah", 70, "front", "panic", "shocked", t)
            paste(im, spr, W / 2 - spr.width / 2, H * 0.80 - fo)
        else:
            draw_fish(im, W * (0.25 + 0.5 * u), H * 0.45, 230, t, mouth=0.2, face="stern", view="side", sweat=True)
            fx_speedlines(im, t, H * 0.45)
        fx_vignette(im, (0, 10, 30), 150)
        caption(im, t)
        return im.convert("RGB")
    # ----- 3D plate shots -----
    Z, cx, cy, rot = shot_cam(k, u, t)
    src = plate(bg, fl)
    sw, shh = src.size
    box = ((cx - 0.5 / Z) * sw, (cy - 0.5 / Z) * shh, (cx + 0.5 / Z) * sw, (cy + 0.5 / Z) * shh)
    im = src.resize((W, H), Image.BICUBIC, box=box)
    im = ImageEnhance.Color(im).enhance(1.28); im = ImageEnhance.Contrast(im).enhance(1.07)
    if "flashback" in fx:
        g = im.convert("L"); im = Image.merge("RGB", [g.point(lambda v: min(255, int(v * 1.05 + 18))), g.point(lambda v: int(v * 0.92 + 8)), g.point(lambda v: int(v * 0.70))])
    im = im.convert("RGBA")
    A = ANCH.get(bg, {})
    # characters, far first
    order = sorted(chars, key=lambda c: -(A[c["at"]][2] if isinstance(c["at"], str) else A[c["at"][0]][2]))
    for c in order:
        who = WHO.get(c["who"], c["who"])
        if isinstance(c["at"], tuple):
            p0, p1 = A[c["at"][0]], A[c["at"][1]]
            uu = u if not c.get("fly") else min(1, u * 1.15)
            x = p0[0] + (p1[0] - p0[0]) * uu; y = p0[1] + (p1[1] - p0[1]) * uu; pp = p0[3] + (p1[3] - p0[3]) * uu
            if c.get("fly"): y -= math.sin(math.pi * uu) * 0.18
        else:
            x, y, _, pp = A[c["at"]]
        X, Y = to_screen(x, y, Z, cx, cy); ppu = pp * H * Z * 0.95
        if c.get("lie"): ppu *= 0.62
        tk = talk if c.get("talk") else 0.0
        spr, fo = toon_sprite(who, ppu, c["view"], c["pose"], c["face"], t + len(who), c["flip"], c["look"], tk, phase=t * 1.6 * (2 if c["pose"] == "run" else 1))
        if c.get("lie"):
            spr = spr.rotate(90, expand=True, resample=Image.BICUBIC)
            px, py = X - spr.width / 2, Y - spr.height * 0.62
            paste(im, spr, px, py)
            if "zzz" in fx: fx_zzz(im, X + spr.width * 0.05, py + spr.height * 0.15, t, int(ppu * 0.45))
            continue
        if c.get("fly"):
            if c.get("fly") and fx and ("splat_end" in fx or "splash_end" in fx) and u > 0.86:
                pass
            spr = spr.rotate(-u * 540 if "splash_end" in fx else -u * 300, expand=True, resample=Image.BICUBIC)
            if not (u > 0.88 and "splash_end" in fx):
                paste(im, spr, X - spr.width / 2, Y - spr.height / 2)
            continue
        if c.get("sink"):
            drop = ease(u) * c["sink"] * ppu; top = Y - fo + drop
            keep = int(Y - top)
            if keep > 0: paste(im, spr.crop((0, 0, spr.width, min(spr.height, keep))), X - spr.width / 2, top)
            continue
        paste(im, spr, X - spr.width / 2, Y - fo)
        hx, hy = X, Y - fo + spr.height * 0.18
        if c.get("seaweed"): seaweed(im, hx + (0.05 * ppu if c["view"] == "side" else 0), Y - 2.05 * ppu, ppu)
        if "steam" in fx and c["who"] == "jonah": fx_steam(im, X, Y - 2.4 * ppu, t, ppu)
        if "tear" in fx: ImageDraw.Draw(im).ellipse([X - 0.25 * ppu, Y - 1.85 * ppu + u * 0.3 * ppu, X - 0.16 * ppu, Y - 1.72 * ppu + u * 0.3 * ppu], fill=(150, 210, 255), outline=OUTL, width=2)
        if "dust" in fx: fx_dust(im, X, Y, t, ppu)
        if "glow" in fx: pass
    # FX
    dr = ImageDraw.Draw(im)
    if "coin" in fx and len(order) >= 2:
        cA = A["jonah"]; cB = A["captain"]
        xa, ya = to_screen(cA[0], cA[1], Z, cx, cy); xb, yb = to_screen(cB[0], cB[1], Z, cx, cy)
        ppu_ = cA[3] * H * Z * 0.95; uu = ease(min(1, u * 1.6))
        x = xa + 0.6 * ppu_ + (xb - xa - 1.2 * ppu_) * uu; y = ya - 1.0 * ppu_ - math.sin(math.pi * uu) * ppu_ * 0.6
        outlined_ellipse(dr, x, y, ppu_ * 0.13, ppu_ * 0.13, (245, 200, 70), 3); dr.text((x - 5, y - 12), "*", fill=(255, 255, 255), font=F(900, 18))
    if "crates" in fx:
        s2 = A["s2"]; x0, y0 = to_screen(s2[0], s2[1], Z, cx, cy); pp = s2[3] * H * Z * 0.95
        for j in range(3):
            uu = ((u * 1.4) - j * 0.18)
            if 0 < uu < 1:
                x = x0 + (j - 1) * pp * 0.5 + uu * pp * (1.8 + j * 0.4); y = y0 - 2.6 * pp - math.sin(math.pi * uu) * pp * 1.4 + uu * uu * pp * 2.2
                draw_crate(dr, x, y, pp * 0.22, uu * 6 + j)
    if "stones" in fx:
        st = A["stones"]; x0, y0 = to_screen(st[0], st[1], Z, cx, cy); pp = st[3] * H * Z * 0.95
        for j in range(4):
            bounce = abs(math.sin((u * 3 + j * 0.4) * math.pi)) * (1 - u) * pp * 0.5
            draw_stone(dr, x0 + (j - 1.5) * pp * 0.35, y0 - pp * 0.08 - bounce, pp * 0.1, j)
        if u > 0.6:
            dr.text((x0 - pp * 0.62 - 6, y0 - pp * 0.62), "!", font=F(900, int(pp * 0.4)), fill=(255, 220, 90), stroke_width=4, stroke_fill=OUTL)
    if "oars" in fx:
        for key in ("s1", "s2"):
            if key in A and any(c["at"] == key for c in chars):
                s_ = A[key]; x0, y0 = to_screen(s_[0], s_[1], Z, cx, cy); pp = s_[3] * H * Z * 0.95
                w = math.sin((t + len(key)) * 7) * 0.16 * pp
                dr.line([(x0 + 0.95 * pp + w, y0 - 1.2 * pp), (x0 + 1.9 * pp + w * 2, y0 + 0.9 * pp)], fill=(130, 80, 40), width=max(6, int(pp * 0.09)))
    if "splash_end" in fx and u > 0.82:
        p1 = A[chars[0]["at"][1]]; x, y = to_screen(p1[0], p1[1], Z, cx, cy); fx_splash(im, x, y, (u - 0.82) / 0.18, p1[3] * H * Z * 0.9)
    if "splat_end" in fx and u > 0.8:
        p1 = A[chars[0]["at"][1]]; x, y = to_screen(p1[0], p1[1], Z, cx, cy); fx_splash(im, x, y, (u - 0.8) / 0.2, p1[3] * H * Z * 0.8, (225, 190, 130))
    if "glow" in fx:
        j = A["jonah"]; x, y = to_screen(j[0], j[1], Z, cx, cy); fx_glow(im, x, y - 1.6 * j[3] * H * Z, j[3] * H * Z * 1.3, a=int(90 + 60 * u))
    if "drips" in fx: fx_drips(im, t)
    if "rays" in fx: fx_rays(im, t)
    if "speedlines" in fx: fx_speedlines(im, t, H * 0.55)
    if "wind" in fx:
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = random.Random(int(t * 12))
        for j in range(10):
            y = r.uniform(80, H - 200); x = (r.uniform(0, W) + t * 900) % (W + 400) - 300
            d.arc([x, y, x + 300, y + 60], 200, 340, fill=(255, 255, 255, 120), width=4)
        im.alpha_composite(lay)
    if "rain" in fx: fx_rain(im, t, 1.0)
    if "lightning" in fx:
        fl_a = 0.0
        for c0, pk in ((0.32, 0.85), (0.55, 0.5)):
            dd = u - c0
            if 0 <= dd < 0.08: fl_a = max(fl_a, pk * (1 - dd / 0.08))
        fx_flash(im, fl_a)
    if "vignette_red" in fx: fx_vignette(im, (120, 10, 10), 190)
    fx_vignette(im, (0, 0, 0), 120)
    if "flashback" in fx:
        g = Image.effect_noise((W, H), 40).convert("L"); lay = Image.merge("RGBA", [g, g, g, g.point(lambda v: 26)]); im.alpha_composite(lay)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=False, center=(W / 2, H / 2), fillcolor=(0, 0, 0, 255))
        im = im.resize((int(W * 1.05), int(H * 1.05)), Image.BICUBIC).crop((int(W * 0.025), int(H * 0.025), int(W * 0.025) + W, int(H * 0.025) + H))
    caption(im, t)
    return im.convert("RGB")

if __name__ == "__main__":
    if sys.argv[1] == "--test":
        for tt in [float(x) for x in sys.argv[2].split(",")]:
            frame(int(tt * FPS)).save(f"/tmp/v3t_{tt:05.2f}.png")
        sys.exit()
    os.makedirs(os.path.join(D, "comp3"), exist_ok=True)
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for n in range(a, b + 1):
        p = os.path.join(D, f"comp3/c_{n:05d}.png")
        if not os.path.exists(p): frame(n).save(p)
    print("COMP OK", a, b)
