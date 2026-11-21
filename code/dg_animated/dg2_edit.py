"""David & Goliath v2 (Nov 21, 2026): AI-animated shots (Wan 2.2 5B on Lodo's RTX 4060 Ti, keyframes SDXL)
cut to the am_puck narration, pop captions from engine5 (HD), grade + grain. python3 dg2_edit.py range a b | test t,..."""
import sys, os, subprocess, numpy as np
from PIL import Image, ImageFilter, ImageEnhance
sys.path.insert(0, "/home/claude/gnf/s6"); os.chdir("/home/claude/gnf/s6")
_argv = sys.argv; sys.argv = ["engine5.py", "dg"]; import engine5 as E; sys.argv = _argv
W, H, FPS = 1080, 1920, 24; R = "/home/claude/gnf/dg2"; V = f"{R}/vid"
S = E.STARTS; END = E.END
CUT = lambda i: max(0.0, S[i] - 0.15) if i else 0.0
PLAN = [("v01", 0, 0.0), ("v02", 2, 0.0), ("v03", 4, 0.0), ("v04b", 6, 0.0), ("v05", 8, 0.0), ("v06", 10, 0.0), ("v07", 13, 0.0),
        ("v08", 14, 0.0), ("v09", 16, 0.0), ("v05", 17, 2.4), ("v10", 19, 0.0), ("v11", 21, 0.0), ("v12", 23, 0.0), ("v13", 25, 0.0)]
SEG = [(c, CUT(li), CUT(PLAN[k + 1][1]) if k + 1 < len(PLAN) else END + 0.1, off) for k, (c, li, off) in enumerate(PLAN)]
_C = {}
def clip(name):
    if name not in _C:
        _C.clear()
        p = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{V}/{name}.webm", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _C[name] = np.frombuffer(p, np.uint8).reshape(-1, 1280, 704, 3)
    return _C[name]
def clip_frame(name, u):
    a = clip(name); n = len(a); x = min(max(u * FPS, 0), n - 1); i = int(x); w = x - i
    if w < 0.02 or i + 1 >= n: return a[i]
    return (a[i] * (1 - w) + a[i + 1] * w).astype(np.uint8)
def seg_at(t):
    for k, s in enumerate(SEG):
        if s[1] <= t < s[2]: return k
    return len(SEG) - 1
RNG = np.random.default_rng(5); GR = [Image.fromarray((RNG.normal(128, 22, (H // 2, W // 2))).clip(0, 255).astype(np.uint8)).resize((W, H)) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W]; rr = np.sqrt(((xx - W / 2) / (W * 0.72)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
VIG = Image.fromarray((np.clip((rr - 0.6) * 1.3, 0, 1) ** 1.6 * 170).astype(np.uint8))
HIT = S[21] + 0.25; FALL = S[22] + 0.2
def frame(t):
    k = seg_at(t); c, t0, t1, off = SEG[k]
    n = len(clip(c)) / FPS; avail = n - off - 0.05; dur = t1 - t0
    sp = min(1.0, avail / dur) if dur > 0 else 1.0
    im = Image.fromarray(clip_frame(c, off + (t - t0) * sp)).resize((W, H), Image.LANCZOS)
    if t - t0 < 0.17 and k > 0:                                    # 4-frame dissolve
        c2, a0, a1, o2 = SEG[k - 1]; n2 = len(clip(c2)) / FPS
        prev = Image.fromarray(clip_frame(c2, min(n2 - 0.05, o2 + (t - a0) * min(1.0, (n2 - o2 - 0.05) / (a1 - a0))))).resize((W, H), Image.LANCZOS)
        im = Image.blend(prev, im, (t - t0) / 0.17)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    im = ImageEnhance.Contrast(im).enhance(1.05); im = ImageEnhance.Color(im).enhance(1.06)
    if FALL <= t < FALL + 0.6:                                     # impact shake
        a = (1 - (t - FALL) / 0.6) * 18; dx, dy = int(a * np.sin(t * 90)), int(a * np.cos(t * 77))
        im = im.transform((W, H), Image.AFFINE, (1, 0, dx, 0, 1, dy), Image.BICUBIC)
    im = Image.blend(im, Image.merge("RGB", [GR[int(t * FPS) % 6]] * 3), 0.03)
    fr = im.convert("RGBA"); v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); v.putalpha(VIG); fr.alpha_composite(v)
    if HIT <= t < HIT + 0.2:
        fr.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 235, int(230 * (1 - (t - HIT) / 0.2)))))
    E.caption(fr, t)
    if t < 0.12: fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / 0.12)))))
    if t > END - 0.5: fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * min(1, (t - END + 0.5) / 0.5)))))
    return fr.convert("RGB")
if __name__ == "__main__":
    if sys.argv[1] == "plan":
        for s in SEG: print("%s %6.2f %6.2f off %.1f" % s)
        print("END", END, "CUTS", ",".join("%.2f" % s[1] for s in SEG[1:]))
    elif sys.argv[1] == "test":
        for x in sys.argv[2].split(","): frame(float(x)).save(f"/tmp/dg2_{float(x):06.2f}.png")
    else:
        a, b = int(sys.argv[2]), int(sys.argv[3]); os.makedirs(f"{R}/fr", exist_ok=True)
        for n in range(a, min(b, int(END * FPS)) + 1):
            p = f"{R}/fr/f_{n:05d}.png"
            if not os.path.exists(p): frame(n / FPS).save(p, compress_level=1)
