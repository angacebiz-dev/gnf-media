"""engine5 (Nov 19, 2026): 2.5D toon Short renderer for the 5 style variants.
python3 engine5.py <sid> [--test t1,t2,...] [--range f0 f1]   (frames -> s5/<sid>/fr/f_00000.png; tests -> /tmp/s5_<sid>_<t>.png)
Shot list in shots_<sid>.py: STYLE, PAUSE, SHOTS (each shot starts at a voice line), SFX.
World = 1080x1920 canvas (bgs5), camera = zoom + centre (eased), background layers move with parallax."""
import sys, os, json, math, random, importlib
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import toon5 as T, props5 as P, bgs5 as B

W, H, FPS = 720, 1280, 24
WW, HH = B.WW, B.HH
MF = "/home/claude/gnf/fonts/fontsource-montserrat-5.3.0/package/files/montserrat-latin-{}-{}.woff2"
CG = "/home/claude/gnf/fonts/fontsource-cormorant-garamond-5.3.0/package/files/cormorant-garamond-latin-{}-{}.woff"
_F = {}
def font(path, size):
    k = (path, size)
    if k not in _F: _F[k] = ImageFont.truetype(path, size)
    return _F[k]

SID = sys.argv[1]; D = f"/home/claude/gnf/s5/{SID}"
SH = importlib.import_module(f"shots_{SID}")
ST = SH.STYLE; T.STYLE.update(ST["toon"])
LINES = json.load(open(f"{D}/audio/lines.json"))
STARTS, t = [], 0.3
for i, (txt, dur) in enumerate(LINES):
    STARTS.append(t)
    t += dur + ST["gap"] * (1.7 if txt.rstrip()[-1] in ".?!" else 1.0) + SH.PAUSE.get(i, 0.0)
END = t + ST.get("tail", 0.8)
DUR = [d for _, d in LINES]
ENV = []
for i in range(len(LINES)):
    a, sr = sf.read(f"{D}/audio/l{i:02d}.wav"); hop = sr // FPS
    e = np.array([np.sqrt(np.mean(a[k * hop:(k + 1) * hop] ** 2)) if len(a[k * hop:(k + 1) * hop]) else 0 for k in range(len(a) // hop + 1)])
    ENV.append(e / (e.max() + 1e-6))
def talk_amt(t):
    for i, s0 in enumerate(STARTS):
        if s0 <= t < s0 + DUR[i]:
            k = int((t - s0) * FPS); return float(ENV[i][min(k, len(ENV[i]) - 1)]), i
    return 0.0, None

SHOTS = SH.SHOTS
for s in SHOTS: s["t0"] = STARTS[s["l"]] + s.get("f", 0.0) * DUR[s["l"]] - 0.06
SHOTS[0]["t0"] = 0.0
for k, s in enumerate(SHOTS): s["t1"] = SHOTS[k + 1]["t0"] if k + 1 < len(SHOTS) else END

def ease(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def lerp(a, b, u): return a + (b - a) * u

def camera(s, t):
    u = (t - s["t0"]) / max(0.01, s["t1"] - s["t0"]); e = ease(u)
    z0, z1, c0, c1 = s.get("cam", (1.0, 1.08, (0.5, 0.5), (0.5, 0.5)))
    z = lerp(z0, z1, e); cx, cy = lerp(c0[0], c1[0], e), lerp(c0[1], c1[1], e)
    if s.get("punch"): z *= 1 + 0.18 * math.exp(-(t - s["t0"]) * 9)
    sh = s.get("shake", 0.0)
    if sh: cx += sh * 0.012 * math.sin(t * 43); cy += sh * 0.010 * math.sin(t * 37 + 1)
    return z, cx, cy

def view(z, cx, cy):
    vw, vh = WW / z, HH / z
    x0 = min(max(cx * WW - vw / 2, 0), WW - vw); y0 = min(max(cy * HH - vh / 2, 0), HH - vh)
    return x0, y0, vw, vh

def render_bg(s, z, cx, cy):
    out = None
    for L, p in B.bg(SID, s["bg"]):
        zl = 1 + (z - 1) * p; cxl, cyl = 0.5 + (cx - 0.5) * p, 0.5 + (cy - 0.5) * p
        x0, y0, vw, vh = view(zl, cxl, cyl)
        im = L.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + vw, y0 + vh))
        if out is None: out = im
        else: out.alpha_composite(im)
    return out

# ---------------------------------------------------------------- character styling per look
def dilate(a, r): return a.filter(ImageFilter.MaxFilter(r * 2 + 1)) if r > 0 else a
def style_char(im):
    k = ST["char"]
    if k == "rim":                    # B: night silhouette with warm rim light; eyes/teeth stay bright
        a = im.split()[3]; arr = np.asarray(im, np.float32)
        lum = arr[..., :3].mean(-1); keep = (lum > 225)[..., None]
        dark = arr[..., :3] * 0.22 + np.array([10, 12, 30])
        rgb = np.where(keep, arr[..., :3] * 0.9, dark)
        out = Image.fromarray(np.dstack([rgb, arr[..., 3]]).astype(np.uint8), "RGBA")
        sh = ImageChops.offset(a, 5, 4); rim = ImageChops.subtract(a, sh).filter(ImageFilter.GaussianBlur(1))
        rc = Image.new("RGBA", im.size, (255, 170, 80, 0)); rc.putalpha(rim); out.alpha_composite(rc)
        return out
    if k == "ink":                    # C: heavy black comic outline
        a = im.split()[3]; ol = Image.new("RGBA", im.size, (0, 0, 0, 0)); ol.putalpha(dilate(a, 3))
        pad = Image.new("RGBA", im.size, (0, 0, 0, 0)); pad.alpha_composite(ol); pad.alpha_composite(im); return pad
    if k == "sticker":                # E: white paper edge + drop shadow
        a = im.split()[3]; big = dilate(a, 4)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(big.point(lambda v: v * 90 // 255).filter(ImageFilter.GaussianBlur(4)))
        wh = Image.new("RGBA", im.size, (255, 255, 255, 0)); wh.putalpha(big)
        out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (5, 7)) if True else None
        out = ImageChops.offset(out, 0, 0); out.alpha_composite(wh); out.alpha_composite(im); return out
    if k == "soft":                   # D: soft storybook edge + gentle shadow
        a = im.split()[3]; sh = Image.new("RGBA", im.size, (60, 40, 70, 0)); sh.putalpha(a.point(lambda v: v * 60 // 255).filter(ImageFilter.GaussianBlur(5)))
        out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 6)); out.alpha_composite(im.filter(ImageFilter.GaussianBlur(0.5))); return out
    return im

def paste(base, im, x, y):
    x, y = int(round(x)), int(round(y))
    if x >= 0 and y >= 0 and x + im.width <= base.width and y + im.height <= base.height: base.alpha_composite(im, (x, y))
    else: base.paste(im, (x, y), im)

def char_layer(c, t, s, scale, x0, y0):
    """draw one character spec onto a frame-sized RGBA, returns (layer, screen foot y) for depth sorting"""
    u = (t - s["t0"]) / max(0.01, s["t1"] - s["t0"]); e = ease(u) if c.get("ease", True) else min(max(u, 0), 1)
    wx = (c["x"] + c.get("mx", 0.0) * e) * WW; wy = (c["y"] + c.get("my", 0.0) * e) * HH
    if c.get("hop"): wy -= abs(math.sin((t - s["t0"]) * c["hop"] * math.pi)) * 0.02 * HH
    sx, sy = (wx - x0) * scale, (wy - y0) * scale; ppu = c["s"] * WW * scale
    tt = t if not ST.get("twos") else math.floor(t * 12) / 12
    talk = 0.0
    if c.get("talk"):
        a_, li = talk_amt(t); talk = a_ if (c["talk"] is True or li in c["talk"]) else 0.0
    T.SS = 3 if ppu < 110 else 2
    small, foot = T.draw(None, sx, sy, ppu, c["w"], c.get("v", "front"), c.get("p", "stand"), c.get("f", "calm"), tt + c.get("dt", 0), c.get("flip", False),
                         c.get("look", (0.0, 0.0)), ret=True, phase=(tt * c.get("ph", 0.0)) % 1, talk=talk)
    small = style_char(small)
    if ST.get("twos") and c.get("jig", True):
        ang = (random.Random(int(tt * 12) + hash(c["w"]) % 97).random() - 0.5) * 3.0
        small = small.rotate(ang, Image.BICUBIC, expand=False)
    if c.get("sink"):
        cut = int(small.height * (1 - c["sink"] * e)); m = Image.new("L", small.size, 0); ImageDraw.Draw(m).rectangle([0, 0, small.width, cut], fill=255)
        small.putalpha(ImageChops.multiply(small.split()[3], m))
    if c.get("alpha", 1.0) < 1: small.putalpha(small.split()[3].point(lambda v: int(v * c["alpha"])))
    return small, sx - small.width / 2, sy - foot, sy

def prop_draw(fr, p, t, s, scale, x0, y0):
    u = ease((t - s["t0"]) / max(0.01, s["t1"] - s["t0"]))
    wx = (p["x"] + p.get("mx", 0.0) * u) * WW; wy = (p["y"] + p.get("my", 0.0) * u) * HH
    sx, sy, sz = (wx - x0) * scale, (wy - y0) * scale, p["s"] * WW * scale
    k = p["k"]; tt = t if not ST.get("twos") else math.floor(t * 12) / 12
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if k == "lion": P.lion(L, sx, sy, sz, tt + p.get("dt", 0), p.get("flip", False), p.get("mouth", 0.0) * (0.6 + 0.4 * math.sin(t * 8)) if p.get("roar") else p.get("mouth", 0.0), p.get("sleepy", False), (tt * p.get("ph", 0)) % 1)
    elif k == "pig": P.pig(L, sx, sy, sz, tt + p.get("dt", 0), p.get("flip", False), (tt * p.get("ph", 0)) % 1)
    elif k == "sheep": P.sheep(L, sx, sy, sz, tt, p.get("flip", False))
    elif k == "boat": P.boat(L, sx, sy, sz, tt)
    elif k == "altar": P.altar(L, sx, sy, sz, tt, p.get("wet", 0.0) * (u if p.get("wetgrow") else 1), p.get("fire", 0.0))
    elif k == "flames": P.flames(L, sx, sy, sz, tt)
    elif k == "stone": P.stone_proj(L, sx, sy, sz)
    elif k == "giantfall":   # Goliath tipping over around his feet
        small, foot = T.draw(None, sx, sy, sz, "goliath", "front", "stand", "shocked", tt, False, ret=True)
        small = style_char(small); R = int(max(small.width, small.height) * 2.2)
        pad = Image.new("RGBA", (R, R), (0, 0, 0, 0)); pad.alpha_composite(small, (int(R / 2 - small.width / 2), int(R / 2 - foot)))
        ang = min(1, max(0, (t - s["t0"] - p.get("delay", 0.3)) / 0.45)) ** 2 * 86
        pad = pad.rotate(ang, Image.BICUBIC)
        paste(L, pad, sx - R / 2, sy - R / 2)
    elif k == "seal":
        d = ImageDraw.Draw(L); d.ellipse([sx - sz, sy - sz, sx + sz, sy + sz], fill=(180, 40, 40), outline=(20, 10, 10), width=max(2, int(sz * 0.15)))
    if k in ("lion", "pig", "sheep", "boat", "altar") and ST["char"] in ("rim", "ink", "sticker"):
        bb = L.getbbox()
        if bb:
            bb = (max(0, bb[0] - 12), max(0, bb[1] - 12), min(W, bb[2] + 12), min(H, bb[3] + 12))
            L2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L2.alpha_composite(style_char(L.crop(bb)), (bb[0], bb[1])); L = L2
    return L

# ---------------------------------------------------------------- effects
RND = random.Random(5)
DUST = [(RND.random(), RND.random(), RND.uniform(1.5, 4)) for _ in range(70)]
def fx_draw(fr, f, t, s, scale, x0, y0):
    k = f[0]; d = ImageDraw.Draw(fr, "RGBA"); lt = t - s["t0"]
    if k == "rain":
        for i in range(160):
            x = (DUST[i % 70][0] * W + i * 37) % W; y = (DUST[i % 70][1] * H + t * 1500 + i * 53) % H
            d.line([(x, y), (x - 8, y + 30)], fill=(210, 220, 255, 110), width=2)
    elif k == "dust":
        for x, y, r in DUST:
            yy = (y * H - t * 18 * r) % H; xx = (x * W + math.sin(t + r) * 20) % W
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 240, 200, 90))
    elif k == "sparks":
        for x, y, r in DUST[:40]:
            yy = (y * H - t * 120 * r) % H; xx = (x * W + math.sin(t * 2 + r) * 30) % W
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=(255, 200, 90, 200))
    elif k == "flash":
        a = max(0.0, 1 - lt / f[1]) if len(f) > 1 else max(0.0, 1 - lt / 0.25)
        if a > 0: fr.alpha_composite(Image.new("RGBA", fr.size, (255, 250, 235, int(230 * a))))
    elif k == "rays":
        px, py = (f[1] * WW - x0) * scale, (f[2] * HH - y0) * scale
        L = Image.new("RGBA", fr.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        for j in range(12):
            a0 = j / 12 * 2 * math.pi + t * 0.15; a1 = a0 + 0.12
            dd.polygon([(px, py), (px + math.cos(a0) * 2000, py + math.sin(a0) * 2000), (px + math.cos(a1) * 2000, py + math.sin(a1) * 2000)], fill=f[3] + (40,))
        fr.alpha_composite(L.filter(ImageFilter.GaussianBlur(10)))
    elif k == "glow":
        px, py = (f[1] * WW - x0) * scale, (f[2] * HH - y0) * scale; r = f[3] * WW * scale * (1 + 0.05 * math.sin(t * 3))
        m = Image.new("L", fr.size, 0); ImageDraw.Draw(m).ellipse([px - r, py - r, px + r, py + r], fill=f[5] if len(f) > 5 else 150)
        g = Image.new("RGBA", fr.size, f[4] + (0,)); g.putalpha(m.filter(ImageFilter.GaussianBlur(r * 0.5))); fr.alpha_composite(g)
    elif k == "speed":
        cxs, cys = W / 2, H * 0.45
        for j in range(40):
            a = j / 40 * 2 * math.pi + RND.random() * 0.05; r0 = 260 + (j * 37 % 120)
            d.line([(cxs + math.cos(a) * r0, cys + math.sin(a) * r0), (cxs + math.cos(a) * 1200, cys + math.sin(a) * 1200)], fill=(255, 255, 255, 150), width=3)
    elif k == "word":                 # comic burst word: ("word", text, x, y, size)
        u = min(1, lt / 0.18); sz = int(f[4] * (0.6 + 0.4 * u) * (1 + 0.03 * math.sin(t * 20)))
        x, y = f[2] * W, f[3] * H; fnt = font(MF.format(900, "italic"), sz)
        pts = [(x + math.cos(a) * sz * (2.3 if j % 2 else 1.5), y + math.sin(a) * sz * (1.3 if j % 2 else 0.9)) for j, a in enumerate(np.linspace(0, 2 * math.pi, 24, endpoint=False))]
        d.polygon(pts, fill=(255, 236, 60), outline=(0, 0, 0)); d.line(pts + [pts[0]], fill=(0, 0, 0), width=6)
        tw = d.textlength(f[1], font=fnt); d.text((x - tw / 2, y - sz * 0.62), f[1], font=fnt, fill=(230, 40, 30), stroke_width=5, stroke_fill=(0, 0, 0))
    elif k == "firefall":             # column of fire from the sky onto (x, y)
        px, py = (f[1] * WW - x0) * scale, (f[2] * HH - y0) * scale; u = min(1, lt / 0.35)
        L = Image.new("RGBA", fr.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(L); w0 = 60 * scale * 1.5
        for col, wm in (((240, 80, 30), 1.0), ((255, 180, 40), 0.65), ((255, 245, 170), 0.3)):
            pts = []
            for j in range(30):
                yy = j / 29 * py * u; ww_ = w0 * wm * (0.5 + 0.5 * j / 29) * (1 + 0.25 * math.sin(t * 25 + j))
                pts.append((px - ww_, yy))
            pts += [(px + w0 * wm * (0.5 + 0.5 * j / 29) * (1 + 0.25 * math.sin(t * 23 + j * 1.3)), j / 29 * py * u) for j in range(29, -1, -1)]
            dd.polygon(pts, fill=col + (230,))
        fr.alpha_composite(L.filter(ImageFilter.GaussianBlur(3))); fr.alpha_composite(L)
    elif k == "projectile":           # ("projectile", x0, y0, x1, y1, dur, size)
        u = min(1, lt / f[5]); px = lerp(f[1], f[3], u) * WW; py = lerp(f[2], f[4], u) * HH - math.sin(u * math.pi) * 0.04 * HH
        sx, sy = (px - x0) * scale, (py - y0) * scale
        if u < 1:
            for j in range(6): d.ellipse([sx - 10 + j * 6, sy - 2, sx - 6 + j * 6, sy + 2], fill=(255, 255, 255, 60))
            P.stone_proj(fr, sx, sy, f[6] * scale)
    elif k == "confetti":
        for j, (x, y, r) in enumerate(DUST):
            yy = (y * H + t * 160 * r) % H; xx = (x * W + math.sin(t * 2 + j) * 30) % W
            col = [(240, 80, 90), (250, 200, 60), (80, 180, 240), (120, 210, 120)][j % 4]
            d.rectangle([xx - 4, yy - 7, xx + 4, yy + 7], fill=col + (230,))
    elif k == "splash":
        px, py = (f[1] * WW - x0) * scale, (f[2] * HH - y0) * scale; u = min(1, lt / 0.6)
        for j in range(14):
            a = math.pi + j / 13 * math.pi; r = 120 * u * scale * 2
            d.ellipse([px + math.cos(a) * r - 7, py + math.sin(a) * r * 0.8 - 7, px + math.cos(a) * r + 7, py + math.sin(a) * r * 0.8 + 7], fill=(230, 245, 255, int(220 * (1 - u))))
    elif k == "wavefront":            # foreground wave band (in front of characters) for sinking shots
        yb = (f[1] * HH - y0) * scale
        pts = [(x, yb + 18 * math.sin(x / 50 + t * 3)) for x in range(-10, W + 20, 10)]
        d.polygon(pts + [(W + 20, H), (-10, H)], fill=(70, 110, 170, 235)); d.line(pts, fill=(235, 240, 250, 230), width=6)
    elif k == "hearts":
        for j in range(8):
            x = W * (0.2 + 0.08 * j); y = H * 0.5 - (lt * 120 + j * 40) % 500
            d.ellipse([x - 14, y - 10, x, y + 4], fill=(240, 80, 110, 200)); d.ellipse([x, y - 10, x + 14, y + 4], fill=(240, 80, 110, 200)); d.polygon([(x - 14, y - 2), (x + 14, y - 2), (x, y + 16)], fill=(240, 80, 110, 200))

# ---------------------------------------------------------------- grade + captions
_TEX = {}
def post(fr, t):
    k = ST["post"]; im = fr.convert("RGB")
    if k == "warm":
        im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.05)
    elif k == "night":
        im = ImageEnhance.Color(im).enhance(1.1)
    elif k == "comic":
        im = ImageEnhance.Color(im).enhance(1.3); im = ImageEnhance.Contrast(im).enhance(1.08)
        if "dots" not in _TEX:
            m = Image.new("L", (W, H), 255); dd = ImageDraw.Draw(m)
            for y in range(0, H, 9):
                for x in range((y // 9 % 2) * 4, W, 9): dd.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=215)
            _TEX["dots"] = Image.merge("RGB", [m] * 3)
        im = ImageChops.multiply(im, _TEX["dots"])
    elif k in ("paper", "paper2"):
        if "paper" not in _TEX:
            n = Image.effect_noise((W, H), 26).filter(ImageFilter.GaussianBlur(1.1))
            _TEX["paper"] = Image.merge("RGB", [n.point(lambda v: 222 + v // 8)] * 3)
        im = ImageChops.multiply(im, _TEX["paper"]); im = ImageEnhance.Color(im).enhance(1.12 if k == "paper2" else 0.95)
        if k == "paper": im = ImageEnhance.Brightness(im).enhance(1.06)
    if "vig" not in _TEX:
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        _TEX["vig"] = np.clip(1 - ST.get("vig", 0.3) * np.clip(r - 0.55, 0, 1) ** 1.4, 0, 1)[..., None]
    a = np.asarray(im, np.float32) * _TEX["vig"]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def chunks(i):
    txt, dur = LINES[i]; words = txt.split(); mx = ST["capmax"]; out, cur = [], []
    for w in words:
        cur.append(w)
        if len(" ".join(cur)) >= mx or w.endswith((",", ".", "?", "!", ":")): out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    tot = sum(len(c) + 3 for c in out); res, a = [], STARTS[i]
    for c in out:
        b = a + dur * (len(c) + 3) / tot; res.append((a, b, c)); a = b
    return res
CAPS = [c for i in range(len(LINES)) for c in chunks(i)]

def caption(fr, t):
    cur = [c for c in CAPS if c[0] - 0.02 <= t < c[1] + 0.12]
    if not cur or any(s["t0"] <= t < s["t1"] and s.get("nocap") for s in SHOTS): return
    a, b, txt = cur[-1]; d = ImageDraw.Draw(fr, "RGBA"); k = ST["cap"]; u = min(1, (t - a) / 0.12)
    y = H * ST.get("capy", 0.70)
    if k == "pop":                    # A: v3 style
        f = font(MF.format(800, "normal"), int(60 * (0.9 + 0.1 * u))); tw = d.textlength(txt, font=f)
        d.text((W / 2 - tw / 2 + 3, y + 5), txt, font=f, fill=(0, 0, 0, 120)); d.text((W / 2 - tw / 2, y), txt, font=f, fill=(255, 255, 255), stroke_width=6, stroke_fill=(30, 20, 20))
    elif k == "glow":                 # B
        f = font(MF.format(700, "normal"), 46); tw = d.textlength(txt, font=f); al = int(255 * u)
        g = Image.new("RGBA", fr.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text((W / 2 - tw / 2, y), txt, font=f, fill=(255, 170, 80, al))
        fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(8))); d.text((W / 2 - tw / 2, y), txt, font=f, fill=(255, 244, 226, al), stroke_width=2, stroke_fill=(20, 10, 10, al))
    elif k == "comic":                # C
        f = font(MF.format(900, "italic"), 54); txt = txt.upper(); tw = d.textlength(txt, font=f); sc = 0.85 + 0.15 * u
        L = Image.new("RGBA", (int(tw + 60), 96), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        dl.rectangle([6, 6, L.width - 6, L.height - 6], fill=(255, 236, 60), outline=(0, 0, 0), width=6); dl.text((30, 14), txt, font=f, fill=(0, 0, 0))
        L = L.rotate(-2.5 if hash(txt) % 2 else 2.5, Image.BICUBIC, expand=True); L = L.resize((int(L.width * sc), int(L.height * sc)))
        paste(fr, L, W / 2 - L.width / 2, y - 10)
    elif k == "serif":                # D
        f = font(CG.format(700, "italic"), 64); tw = d.textlength(txt, font=f); al = int(255 * u)
        g = Image.new("RGBA", fr.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text((W / 2 - tw / 2, y + 3), txt, font=f, fill=(40, 30, 60, int(al * 0.7)))
        fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(5))); d.text((W / 2 - tw / 2, y), txt, font=f, fill=(255, 252, 244, al))
    elif k == "strip":                # E
        f = font(MF.format(800, "normal"), 48); tw = d.textlength(txt, font=f)
        L = Image.new("RGBA", (int(tw + 50), 84), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        dl.rectangle([4, 4, L.width - 4, L.height - 4], fill=(255, 255, 255)); dl.text((25, 12), txt, font=f, fill=(30, 26, 30))
        sh = Image.new("RGBA", L.size, (0, 0, 0, 0)); sh.putalpha(L.split()[3].point(lambda v: v * 80 // 255))
        ang = (hash(txt) % 5 - 2) * 1.2; L = L.rotate(ang, Image.BICUBIC, expand=True); sh = sh.rotate(ang, Image.BICUBIC, expand=True)
        paste(fr, sh.filter(ImageFilter.GaussianBlur(3)), W / 2 - L.width / 2 + 5, y + 6); paste(fr, L, W / 2 - L.width / 2, y)

# ---------------------------------------------------------------- frame
def frame(t):
    s = [x for x in SHOTS if x["t0"] <= t][-1]
    z, cx, cy = camera(s, t); x0, y0, vw, vh = view(z, cx, cy); scale = W / vw
    fr = render_bg(s, z, cx, cy)
    for f in s.get("fx", []):
        if f[0] in ("rays", "glow", "dust") and (len(f) < 7 or True) and f[0] != "dust": fx_draw(fr, f, t, s, scale, x0, y0)
    items = []
    for p in s.get("props", []): items.append((p.get("z", (p["y"] + p.get("my", 0)) * HH), "p", p))
    for c in s.get("chars", []): items.append((c.get("z", c["y"] * HH), "c", c))
    for _, kind, it in sorted(items, key=lambda q: q[0]):
        if kind == "p": fr.alpha_composite(prop_draw(fr, it, t, s, scale, x0, y0))
        else:
            im, px, py, _ = char_layer(it, t, s, scale, x0, y0); paste(fr, im, px, py)
    for f in s.get("fx", []):
        if f[0] not in ("rays", "glow"): fx_draw(fr, f, t, s, scale, x0, y0)
    if t < 0.25: fr.alpha_composite(Image.new("RGBA", fr.size, (0, 0, 0, int(255 * (1 - t / 0.25)))))
    if t > END - 0.4: fr.alpha_composite(Image.new("RGBA", fr.size, (0, 0, 0, int(255 * min(1, (t - END + 0.4) / 0.4)))))
    fr = post(fr, t); caption(fr, t)
    return fr.convert("RGB")

if __name__ == "__main__":
    if "--test" in sys.argv:
        for x in sys.argv[sys.argv.index("--test") + 1].split(","):
            frame(float(x)).save(f"/tmp/s5_{SID}_{float(x):06.2f}.png")
        sys.exit()
    os.makedirs(f"{D}/fr", exist_ok=True)
    N = int(END * FPS); a, b = (int(sys.argv[sys.argv.index("--range") + 1]), int(sys.argv[sys.argv.index("--range") + 2])) if "--range" in sys.argv else (0, N - 1)
    for n in range(a, min(b, N - 1) + 1):
        p = f"{D}/fr/f_{n:05d}.png"
        if not os.path.exists(p): frame(n / FPS).save(p, compress_level=1)
    print("FRAMES OK", SID, a, b, "of", N, "END", round(END, 2))
