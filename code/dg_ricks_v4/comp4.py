"""comp4 (Nov 22, 2026): David & Goliath v4 compositor. python3 comp4.py test t1,t2 | range a b"""
import sys, os, math, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import toon4 as T
from shots4 import SHOTS, TIMES, STARTS, LINES, DUR, END, P, FPS
W, H = 1080, 1920; R = os.path.dirname(os.path.abspath(__file__))
LIPS = json.load(open(f"{R}/lips.json"))
MF = "/home/claude/gnf/fonts/fontsource-montserrat-5.3.0/package/files/montserrat-latin-{}-{}.woff2"
_F = {}
def font(w, s):
    if (w, s) not in _F: _F[(w, s)] = ImageFont.truetype(MF.format(w, "normal"), s)
    return _F[(w, s)]
_BG = {}
def bgimg(n):
    if n not in _BG:
        if len(_BG) > 6: _BG.clear()
        _BG[n] = Image.open(f"{R}/bg/{n}.png").convert("RGB")
    return _BG[n]
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def ease_back(u, s=1.4):
    u = min(max(u, 0), 1); u -= 1; return u * u * ((s + 1) * u + s) + 1
def lerp(a, b, u): return a + (b - a) * u
def mix_pose(a, b, u):
    out = {}
    for k in set(T.REST) | set(a) | set(b):
        va, vb = a.get(k, T.REST.get(k)), b.get(k, T.REST.get(k))
        if isinstance(va, tuple) or isinstance(vb, tuple):
            va = va or T.REST[k]; vb = vb or T.REST[k]; out[k] = tuple(lerp(x, y, u) for x, y in zip(va, vb))
        elif isinstance(va, (int, float)) and isinstance(vb, (int, float)): out[k] = lerp(va, vb, u)
        else: out[k] = vb if u > 0.5 else va
    return out
def pose_at(keys, u):
    ks = [(f, P[p] if isinstance(p, str) else p) for f, p in keys]
    if u <= ks[0][0]: return dict(ks[0][1])
    for (f0, p0), (f1, p1) in zip(ks, ks[1:]):
        if u <= f1:
            w = (u - f0) / max(1e-6, f1 - f0); dur = f1 - f0
            return mix_pose(p0, p1, ease_back(min(1, w * 1.6), 1.2) if dur < 0.4 else ease(w))
    return dict(ks[-1][1])
def lip(line, t):
    if line is None: return 0.0, 0.5
    a = STARTS[line]; k = int((t - a) * FPS)
    tr = LIPS[line]
    if 0 <= k < len(tr["open"]): return tr["open"][k], tr["vis"][k]
    return 0.0, 0.5
def char_layer(fr, c, t, u, sh_t0, sh_t1, cam):
    z, x0, y0, bw, bh = cam
    pose = pose_at(c["keys"], u); x, y = c["x"], c["y"]
    if c.get("move"): (ax, ay), (bx, by) = c["move"]; x, y = lerp(ax, bx, u), lerp(ay, by, u)
    st = t - sh_t0
    if c.get("walk") or c.get("run"):
        sp = c.get("walk") or c.get("run"); run = bool(c.get("run")); ph = st * sp * 2 * math.pi
        amp = 42 if run else 26; s_ = math.sin(ph)
        pose.update(lL=(amp * s_, 35 * max(0, -s_) + (20 if run else 8)), lR=(-amp * s_, 35 * max(0, s_) + (20 if run else 8)),
                    bob=abs(math.cos(ph)) * (0.09 if run else 0.045), lean=(14 if run else 3) + pose.get("lean", 0) * 0)
        if c["view"] == "side": pose.update(aL=(-amp * 0.8 * s_, 40 if run else 15), aR=(amp * 0.8 * s_ + (30 if c.get("itemR") == "basket" else 0), 40 if run else (70 if c.get("itemR") == "basket" else 15)))
        if c.get("stomp"): pose["sq"] = 1 - 0.04 * max(0, math.cos(ph * 2)) ** 8
    if c.get("tremble"): x += 0.0025 * c["tremble"] * math.sin(t * 60)
    if c.get("headshake"): pose["hx"] = pose.get("hx", 0) + 0.06 * math.sin(st * 9)
    if c.get("fall"):
        a, b = c["fall"]
        if u > a:
            w = min(1, (u - a) / (b - a)); pose["lean"] = 88 * w ** 2.4
            if w >= 1: pose["sq"] = 1 - 0.12 * math.exp(-(u - b) * 25)
    if c.get("sling"):
        sp = c["sling"] * (1 + st * 0.8); pose["sling_spin"] = st * sp * 2 * math.pi
        if pose.get("lean", 0) > 6: pose["sling_spin"] = None
    face = c["face"]
    if c.get("face2") and u > c["face2"][0]: face = c["face2"][1]
    op, vis = lip(c.get("talk"), t)
    if c.get("talk") is not None and op > 0.05:
        pose["tilt"] = pose.get("tilt", 0) + 3.5 * op * math.sin(t * 7)
        pose["bob"] = pose.get("bob", 0) + 0.012 * op
        if c.get("gest"): pose["aR"] = (pose.get("aR", T.REST["aR"])[0] + 14 * op, pose.get("aR", T.REST["aR"])[1])
    pose["sq"] = pose.get("sq", 1.0) * (1 + 0.012 * math.sin(t * 2.2 + hash(c["who"]) % 5))
    for k in ("itemL", "itemR"):
        if c.get(k) is not None: pose[k] = c[k]
    # draw (cap the drawing size; scale up if needed)
    ppu = c["s"] * H * z; pe = min(ppu, 430); T.SS = 3 if pe < 160 else 2
    im, fx_, fy_ = T.draw(c["who"], pose, t, pe, face, c["view"], c.get("look", (0, 0)), op, vis, c.get("flip", False))
    if ppu > pe:
        k = ppu / pe; im = im.resize((int(im.width * k), int(im.height * k)), Image.BICUBIC); fx_ *= k; fy_ *= k
    X = (x * bw - x0) / (bw / z) * W; Y = (y * bh - y0) / (bh / z) * H
    fr.alpha_composite(im, (int(X - fx_), int(Y - fy_))) if 0 <= int(X - fx_) and 0 <= int(Y - fy_) and int(X - fx_) + im.width <= W and int(Y - fy_) + im.height <= H else fr.paste(im, (int(X - fx_), int(Y - fy_)), im)
    return X, Y, ppu, pose
RNG = random.Random(3)
DUST = [(RNG.uniform(-1, 1), RNG.uniform(0.2, 1), RNG.uniform(0.5, 1.4)) for _ in range(40)]
def puff(d, x, y, r, a, col=(214, 186, 140)):
    for k in range(5):
        ang = k * 1.25; d.ellipse([x + math.cos(ang) * r * 0.6 - r * 0.6, y + math.sin(ang) * r * 0.3 - r * 0.5, x + math.cos(ang) * r * 0.6 + r * 0.6, y + math.sin(ang) * r * 0.3 + r * 0.5], fill=col + (int(a),))
def fx(fr, sh, t, u, cs, st):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); F = sh.get("fx", [])
    X, Y, ppu = cs[0][:3] if cs else (W / 2, H * 0.8, 200)
    if "dust_walk" in F or "dust_run" in F:
        sp = 2.6 if "dust_run" in F else 1.0
        for k in range(6):
            age = (st * 2 * sp + k / 6) % 1
            puff(d, X - (age * 0.5 + 0.1) * ppu * (1 if sh["chars"][0].get("flip") else -1) * 0.8, Y - age * 0.15 * ppu, 0.12 * ppu * (0.5 + age), 120 * (1 - age))
    if "fall_dust" in F and u > 0.72:
        w = (u - 0.72) / 0.28
        for dx, dy, s in DUST: puff(d, X + dx * ppu * 2.2 * (0.3 + w), Y - dy * ppu * 0.5 * w, 0.25 * ppu * s * (0.4 + w), 200 * (1 - w * 0.6))
    if "settle_dust" in F:
        for dx, dy, s in DUST[:20]: puff(d, X + dx * ppu * 2.6, Y - dy * ppu * 0.6 - st * 0.1 * ppu, 0.3 * ppu * s, max(0, 110 - st * 70))
    if "rays" in F:
        for k in range(9):
            a = -math.pi / 2 + (k - 4) * 0.22 + 0.05 * math.sin(t + k)
            d.polygon([(W * 0.5, -H * 0.1), (W * 0.5 + math.cos(a - 0.05) * H * 1.3, -H * 0.1 - math.sin(a - 0.05) * -H * 1.3), (W * 0.5 + math.cos(a + 0.05) * H * 1.3, -H * 0.1 - math.sin(a + 0.05) * -H * 1.3)], fill=(255, 236, 180, 38))
    if "speedlines" in F:
        for k in range(26):
            yy = (k * 97 + int(t * 900)) % H; ln = 160 + (k * 53) % 260; xx = (k * 211 + int(t * 2600)) % (W + ln) - ln
            d.line([(xx, yy), (xx + ln, yy)], fill=(255, 255, 255, 120), width=4)
    if "whoosh_lines" in F and cs:
        for k in range(3):
            r = ppu * (0.9 + k * 0.18); d.arc([X - r, Y - 2.6 * ppu - r * 0.5, X + r, Y - 2.6 * ppu + r * 0.5], (t * 900 + k * 40) % 360, (t * 900 + k * 40 + 90) % 360, fill=(255, 255, 255, 170), width=6)
    if "stones5" in F:
        n = min(5, int(u * 6.5))
        for k in range(n):
            x = W * (0.22 + k * 0.14); y = H * 0.30; pop = min(1, (u * 6.5 - k) * 3)
            r = 46 * (0.6 + 0.4 * pop); d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=(214, 210, 200, 255), outline=(28, 22, 24), width=7)
            d.text((x, y), str(k + 1), font=font(900, 54), fill=(40, 30, 30), anchor="mm")
    if "stone_streak" in F:
        w = min(1, u * 1.15); sx, sy = lerp(W * 0.05, X, w), lerp(H * 1.0, Y - 2.0 * ppu, w)
        for k in range(8): d.ellipse([sx - (8 - k) * 3 - k * 26 * 0.6, sy + k * 30 * 0.6 - 10, sx - k * 26 * 0.6 + 12, sy + k * 30 * 0.6 + 10], fill=(255, 255, 255, 30 + k * 8))
        d.ellipse([sx - 22, sy - 18, sx + 22, sy + 18], fill=(210, 206, 196, 255), outline=(28, 22, 24), width=6)
    if "impact_star" in F and u > 0.86:
        w = (u - 0.86) / 0.14; cx, cy = X, Y - 2.0 * ppu; r = 220 * (0.5 + w)
        pts = [(cx + math.cos(k * math.pi / 8) * (r if k % 2 else r * 0.45), cy + math.sin(k * math.pi / 8) * (r if k % 2 else r * 0.45)) for k in range(16)]
        d.polygon(pts, fill=(255, 240, 120, int(255 * (1 - w * 0.5))), outline=(28, 22, 24))
    if "shine" in F:
        k = (st * 1.6) % 1; cx, cy = W * (0.35 + 0.3 * k), H * 0.30
        for a in range(4): d.line([(cx, cy), (cx + math.cos(a * math.pi / 2) * 60, cy + math.sin(a * math.pi / 2) * 60)], fill=(255, 255, 230, 220), width=6)
    if "flash_claw" in F and st < 0.5:
        a = int(200 * (1 - st / 0.5))
        for k in range(3): d.line([(W * (0.3 + k * 0.15), H * 0.15), (W * (0.15 + k * 0.15), H * 0.55)], fill=(255, 255, 255, a), width=22)
    if "confetti_dust" in F:
        for k in range(40):
            x = (k * 137) % W; y = ((k * 263) + st * 300 * (0.5 + (k % 5) / 5)) % H
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 230, 150, 170))
    fr.alpha_composite(L)
def caption(fr, t):
    for i, l in enumerate(LINES):
        a = STARTS[i]; b = a + DUR[i]
        if a - 0.05 <= t < b + 0.15:
            words = l["text"].replace("LORD", "LORD").split(); n = len(words)
            # weights by word length -> word start times
            wts = [len(w) + 2 for w in words]; tot = sum(wts); ts = [a + DUR[i] * sum(wts[:k]) / tot for k in range(n)]
            chunks, k = [], 0
            while k < n:
                take = 1 if len(words[k]) > 7 or k + 1 >= n or len(words[k + 1]) > 7 else 2
                chunks.append((ts[k], " ".join(words[k:k + take]))); k += take
            cur = None
            for st_, txt in chunks:
                if t >= st_ - 0.03: cur = (st_, txt)
            if not cur: return
            age = t - cur[0]; sc_ = 1 + 0.25 * math.exp(-age * 18); txt = cur[1].upper()
            f = font(900, int(96 * sc_)); d = ImageDraw.Draw(fr)
            w = d.textlength(txt, font=f); x = W / 2 - w / 2; y = H * 0.70
            if w > W * 0.92:
                f = font(900, int(96 * sc_ * W * 0.92 / w)); w = d.textlength(txt, font=f); x = W / 2 - w / 2
            hi = l["who"] != "N"
            d.text((x + 5, y + 8), txt, font=f, fill=(0, 0, 0, 140), stroke_width=12, stroke_fill=(0, 0, 0, 140))
            d.text((x, y), txt, font=f, fill=(255, 214, 90) if hi else (255, 255, 255), stroke_width=12, stroke_fill=(20, 16, 18))
            return
def frame(t):
    k = max(i for i, (a, b) in enumerate(TIMES) if a <= t) if t >= 0 else 0
    sh = SHOTS[k]; a, b = TIMES[k]; u = (t - a) / max(0.01, b - a); st = t - a
    bg = bgimg(sh["bg"]); bw, bh = bg.size
    (z0, cx0, cy0), (z1, cx1, cy1) = sh["cam"]; e = ease(u)
    z = lerp(z0, z1, e) * (1 + 0.07 * math.exp(-st * 14)) * (1 + (0.12 * math.exp(-st * 6) if "punch_in" in sh.get("fx", []) else 0))
    cx, cy = lerp(cx0, cx1, e) * bw, lerp(cy0, cy1, e) * bh
    sk = 0.0; F = sh.get("fx", [])
    if "shake_s" in F: sk = 4
    if "shake_m" in F: sk = 10
    if "stomp_shake" in F: sk = 16 * max(0, math.cos(st * 0.9 * 2 * math.pi * 2)) ** 12
    if "impact_shake" in F and u > 0.74: sk = 30 * math.exp(-(u - 0.74) * 12)
    cx += sk * math.sin(t * 71) * bw / W; cy += sk * math.cos(t * 53) * bh / H
    vw, vh = bw / z, bh / z; x0 = min(max(cx - vw / 2, 0), bw - vw); y0 = min(max(cy - vh / 2, 0), bh - vh)
    fr = bg.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh)).convert("RGBA")
    cam = (z, x0, y0, bw, bh); cs = []
    for c in sorted(sh["chars"], key=lambda c: c["y"]):
        cs.append(char_layer(fr, c, t, u, a, b, cam))
    fx(fr, sh, t, u, cs, st)
    if "end_card" in F and t > STARTS[16] + DUR[16] + 0.2:
        w = min(1, (t - STARTS[16] - DUR[16] - 0.2) / 0.4); d = ImageDraw.Draw(fr)
        d.text((W / 2, H * 0.24), "WHAT GIANT", font=font(900, 110), fill=(255, 214, 90, int(255 * w)), anchor="mm", stroke_width=12, stroke_fill=(20, 16, 18, int(255 * w)))
        d.text((W / 2, H * 0.31), "ARE YOU FACING?", font=font(900, 96), fill=(255, 255, 255, int(255 * w)), anchor="mm", stroke_width=12, stroke_fill=(20, 16, 18, int(255 * w)))
        d.text((W / 2, H * 0.88), "1 Samuel 17  •  Follow for more", font=font(700, 44), fill=(255, 255, 255, int(230 * w)), anchor="mm", stroke_width=6, stroke_fill=(20, 16, 18, int(200 * w)))
    caption(fr, t)
    # warm grade + vignette
    rgb = fr.convert("RGB"); rgb = ImageEnhance.Color(rgb).enhance(1.08); rgb = ImageEnhance.Contrast(rgb).enhance(1.04)
    if t < 0.1: rgb = Image.blend(Image.new("RGB", (W, H)), rgb, t / 0.1)
    if t > END - 0.4: rgb = Image.blend(rgb, Image.new("RGB", (W, H)), min(1, (t - END + 0.4) / 0.4))
    return rgb
if __name__ == "__main__":
    if sys.argv[1] == "test":
        for x in sys.argv[2].split(","): frame(float(x)).save(f"/tmp/d4_{float(x):06.2f}.png")
    else:
        a0, b0 = int(sys.argv[2]), int(sys.argv[3]); os.makedirs(f"{R}/fr", exist_ok=True)
        for n in range(a0, min(b0, int(END * FPS) - 1) + 1):
            p = f"{R}/fr/f_{n:05d}.png"
            if not os.path.exists(p): frame(n / FPS).save(p, compress_level=1)
