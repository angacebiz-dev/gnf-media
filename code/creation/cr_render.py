"""Creation cinematic Short (Nov 20, 2026) — 'Let There Be Light'. 1080x1920 @24.
Painted plates (SDXL on Lodo's RTX 4060 Ti) + slow camera, morph chains, light FX, verse cards.
python3 cr_render.py plan | test t1,t2 | range a b"""
import sys, os, json, math, random, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
W, H, FPS = 1080, 1920, 24
R = "/home/claude/gnf/cr"; IMG = f"{R}/img"
S = json.load(open(f"{R}/script.json")); DUR = dict(json.load(open(f"{R}/audio/lines.json")))
MF = "/home/claude/gnf/fonts/fontsource-montserrat-5.3.0/package/files/montserrat-latin-{}-{}.woff2"
CG = "/home/claude/gnf/fonts/fontsource-cormorant-garamond-5.3.0/package/files/cormorant-garamond-latin-{}-{}.woff"
_F = {}
def font(p, s):
    k = (p, s)
    if k not in _F: _F[k] = ImageFont.truetype(p, s)
    return _F[k]
# ---------------- timeline
HOOK = 1.6                                   # opening flash of the finished world
PRE = {"b00": 1.0, "b05": 1.2, "b06": 1.1, "b09": 0.9, "b11": 0.9, "b12": 0.8, "b13": 0.6, "b15": 0.7, "b16": 0.9, "b17": 1.3, "b19": 0.6, "b20": 0.5}
GAP = 0.55
T = {}; t = HOOK
for b in S["beats"]:
    t += PRE.get(b["id"], 0) + (GAP if T else 0); T[b["id"]] = (t, t + DUR[b["id"]]); t += DUR[b["id"]]
END = t + 2.6
# image segments: consecutive beats sharing an image; segment starts at the first beat's PRE gap
SEG = [("hook", 0, HOOK, "c11_good")]
for b in S["beats"]:
    if SEG[-1][3] == b["img"]: continue
    s0 = T[b["id"]][0] - (0.25 if SEG[-1][3] in ("m1", "m2") else PRE.get(b["id"], 0) + GAP * 0.5)
    SEG.append((b["id"], s0, None, b["img"]))
SEG = [(a, s0, (SEG[i + 1][1] if i + 1 < len(SEG) else END), img) for i, (a, s0, _, img) in enumerate(SEG)]
XF = 0.9                                     # crossfade seconds
# ---------------- plates
_P = {}
def plate(key):
    if key not in _P:
        f = f"{IMG}/{key}.png"; im = Image.open(f).convert("RGB")
        if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS)
        _P[key] = im
    return _P[key]
MORPH = {"m1": sorted(glob.glob(f"{IMG}/m1_*.png")), "m2": sorted(glob.glob(f"{IMG}/m2_*.png"))}
def ease(u): u = min(max(u, 0), 1); return u * u * (3 - 2 * u)
def cam(im, u, k):
    """slow push/drift; k = segment index decides direction"""
    z = 1.04 + 0.10 * ease(u) if k % 2 == 0 else 1.14 - 0.10 * ease(u)
    dx = (0.5 + (0.03 if k % 3 == 0 else -0.03) * (u - 0.5)); dy = 0.5 + (0.02 if k % 2 else -0.02) * (u - 0.5)
    vw, vh = W / z, H / z; x0 = min(max(dx * W - vw / 2, 0), W - vw); y0 = min(max(dy * H - vh / 2, 0), H - vh)
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + vw, y0 + vh))
def seg_frame(i, t):
    a, s0, s1, key = SEG[i]; u = (t - s0) / max(0.01, s1 - s0)
    if key in MORPH and MORPH[key]:
        fs = MORPH[key]; n = len(fs); p = ease(min(1, u * 1.15)) * (n - 1); j = int(min(p, n - 2)); w = p - j
        im = Image.blend(Image.open(fs[j]).convert("RGB").resize((W, H)), Image.open(fs[j + 1]).convert("RGB").resize((W, H)), w)
        return cam(im, u, i)
    return cam(plate(key), u, i)
# ---------------- FX
rnd = random.Random(7)
MOTES = [(rnd.random(), rnd.random(), rnd.uniform(1.5, 4.5), rnd.uniform(0.004, 0.02), rnd.random() * 6.28) for _ in range(90)]
def motes(fr, t, alpha):
    if alpha <= 0: return
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x, y, r, v, ph in MOTES:
        px = (x + 0.012 * math.sin(t * 0.4 + ph)) % 1 * W; py = (y - v * t) % 1 * H
        a = int(alpha * (110 + 90 * math.sin(t * 1.3 + ph)))
        d.ellipse([px - r, py - r, px + r, py + r], fill=(255, 236, 190, max(0, a)))
    fr.alpha_composite(L.filter(ImageFilter.GaussianBlur(1.2)))
GRAIN = [Image.effect_noise((W // 2, H // 2), 22).resize((W, H)) for _ in range(6)]
def grade(im, t):
    im = ImageEnhance.Contrast(im).enhance(1.06)
    g = GRAIN[int(t * FPS) % 6]; im = Image.blend(im, Image.merge("RGB", [g] * 3), 0.035)
    return im
VIG = None
def vignette(fr):
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
        a = np.clip((r - 0.55) * 1.4, 0, 1) ** 1.5 * 200; VIG = Image.fromarray(a.astype(np.uint8))
    v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); v.putalpha(VIG); fr.alpha_composite(v)
# ---------------- text
def wrap(d, txt, f, maxw):
    words = txt.split(); lines = [""]
    for w_ in words:
        tt = (lines[-1] + " " + w_).strip()
        if d.textlength(tt, font=f) <= maxw: lines[-1] = tt
        else: lines.append(w_)
    return lines
def verse_card(fr, b, t):
    t0, t1 = T[b["id"]]; hold = t1 + 0.15
    if not (t0 - 0.1 <= t <= hold + 0.35): return
    txt = b["say"].replace("“", "“").strip(); d = ImageDraw.Draw(fr)
    f = font(CG.format(600, "italic"), 74); lines = wrap(d, txt, f, W * 0.82); words = txt.split(); nw = len(words)
    shown = nw * min(1, max(0, (t - t0) / max(0.3, (t1 - t0) * 0.92)))
    out = max(0, min(1, (t - hold) / 0.35)); A = 1 - out
    lh = 88; y = H * 0.60 - len(lines) * lh / 2
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L); sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    k = 0
    for ln in lines:
        x = W / 2 - dl.textlength(ln, font=f) / 2
        for w_ in ln.split():
            al = max(0, min(1, shown - k)) * A; k += 1
            if al > 0:
                dl.text((x, y), w_, font=f, fill=(255, 248, 232, int(255 * al))); ds.text((x, y + 4), w_, font=f, fill=(0, 0, 0, int(200 * al)))
            x += dl.textlength(w_ + " ", font=f)
        y += lh
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9))); fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3))); fr.alpha_composite(L)
    fr2 = font(MF.format(600, "normal"), 34); ref = b["verse"].upper().replace(" ", "  ", 0)
    ra = max(0, min(1, (t - t0 - 0.4) / 0.5)) * A; tw = d.textlength(ref, font=fr2)
    ImageDraw.Draw(fr).text((W / 2 - tw / 2, y + 26), ref, font=fr2, fill=(255, 214, 140, int(235 * ra)))
    ImageDraw.Draw(fr).line([(W / 2 - 50, y + 12), (W / 2 + 50, y + 12)], fill=(255, 214, 140, int(160 * ra)), width=2)
def narr_cap(fr, b, t):
    t0, t1 = T[b["id"]]
    if not (t0 - 0.1 <= t <= t1 + 0.35): return
    f = font(MF.format(600, "normal"), 54); d = ImageDraw.Draw(fr)
    lines = wrap(d, b["say"], f, W * 0.8); a = min(1, (t - t0 + 0.1) / 0.25, (t1 + 0.35 - t) / 0.3)
    y = H * 0.70 - len(lines) * 31
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for i, ln in enumerate(lines):
        x = W / 2 - d.textlength(ln, font=f) / 2
        ds.text((x, y + i * 64 + 3), ln, font=f, fill=(0, 0, 0, int(220 * a)))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    for i, ln in enumerate(lines):
        x = W / 2 - d.textlength(ln, font=f) / 2; d.text((x, y + i * 64), ln, font=f, fill=(255, 255, 255, int(255 * a)))
def title(fr, t):
    if t < HOOK + 0.2:
        a = min(1, t / 0.3, (HOOK + 0.2 - t) / 0.3)
        f = font(CG.format(700, "normal"), 112); d = ImageDraw.Draw(fr); s = "How it all began"
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 - d.textlength(s, font=f) / 2, H * 0.42 + 5), s, font=f, fill=(0, 0, 0, int(230 * a)))
        fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10))); d.text((W / 2 - d.textlength(s, font=f) / 2, H * 0.42), s, font=f, fill=(255, 246, 225, int(255 * a)))
    if t > END - 2.4:
        a = min(1, (t - END + 2.4) / 0.6) * min(1, (END - 0.3 - t) / 0.4 + 1)
        f = font(MF.format(600, "normal"), 40); d = ImageDraw.Draw(fr); s = "Follow for more hope  •  God No Filter"
        d.text((W / 2 - d.textlength(s, font=f) / 2, H * 0.86), s, font=f, fill=(255, 230, 190, int(230 * a)))
# ---------------- frame
LIGHT_T = T["b05"][0] + 1.25                 # the word "light" lands about here
def frame(t):
    i = max(j for j, s in enumerate(SEG) if s[1] <= t)
    im = seg_frame(i, t)
    if i > 0 and t - SEG[i][1] < XF and SEG[i][3] not in ("m1", "m2") and SEG[i - 1][3] not in ("m1", "m2"):
        im = Image.blend(seg_frame(i - 1, t), im, ease((t - SEG[i][1]) / XF))
    elif i > 0 and t - SEG[i][1] < 0.5:
        im = Image.blend(seg_frame(i - 1, t), im, ease((t - SEG[i][1]) / 0.5))
    if SEG[i][0] == "hook" or (i == 1 and t - SEG[1][1] < 0.4):   # hard flash out of the hook into darkness
        pass
    im = grade(im, t); fr = im.convert("RGBA")
    dark = SEG[i][3] in ("c01_void", "c02_spirit", "c13_dark")
    motes(fr, t, 0.35 if dark else 0.9)
    if LIGHT_T - 0.15 <= t <= LIGHT_T + 1.6:                  # "let there be light" flash + bloom
        u = (t - LIGHT_T + 0.15); a = min(1, u / 0.15) * max(0, 1 - (u - 0.15) / 1.45)
        fr.alpha_composite(Image.new("RGBA", (W, H), (255, 246, 220, int(235 * a))))
    vignette(fr)
    for b in S["beats"]:
        (verse_card if "verse" in b else narr_cap)(fr, b, t)
    title(fr, t)
    if t < 0.15: fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / 0.15)))))
    if t > END - 0.6: fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * min(1, (t - END + 0.6) / 0.6)))))
    return fr.convert("RGB")
if __name__ == "__main__":
    if sys.argv[1] == "plan":
        print("END %.2f" % END)
        for s in SEG: print("%-5s %6.2f %6.2f %s" % s)
    elif sys.argv[1] == "test":
        for x in sys.argv[2].split(","): frame(float(x)).save(f"/tmp/cr_{float(x):06.2f}.png")
    else:
        a, b = int(sys.argv[2]), int(sys.argv[3]); os.makedirs(f"{R}/fr", exist_ok=True)
        for n in range(a, min(b, int(END * FPS) - 1) + 1):
            p = f"{R}/fr/f_{n:05d}.png"
            if not os.path.exists(p): frame(n / FPS).save(p, compress_level=1)
