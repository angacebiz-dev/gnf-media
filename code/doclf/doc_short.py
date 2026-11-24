"""VERTICAL 9:16 Short version of doc_story.py (Nov 24, 2026). Generic God No Filter documentary renderer (Nov 19, 2026; from rs/rs_story.py, Moses & the Red Sea).
DOC=<dir> python3 doc_story.py [--frames t1,...] | [--chunk i n]
<dir>/script.md "@key fx,fy [ring=x,y]" lines pick the image for the following beats (re-read here, so image edits need no re-voice);
<dir>/conf.json: hook [top, big, sub], next, labels {key: [big, small]}, gold [words]; images in <dir>/p/<key>.jpg."""
import sys, os, json, re
DIR = os.environ["DOC"]
os.environ["VERT"] = "1"
os.environ.setdefault("BEATS", f"{DIR}/beats.json")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from story60_lib import *

# ------------------------------------------------------------------ painting window (landscape)
BOX = (50, 390, 1030, 1350)
BW, BH = BOX[2] - BOX[0], BOX[3] - BOX[1]
P, BG = {}, {}
def reg(key, im, gamma=None, gain=1.0):
    im = im.convert("RGB")
    if gamma or gain != 1.0:
        a = np.asarray(im, np.float32) / 255
        if gamma: a = a ** gamma
        im = Image.fromarray(np.clip(a * gain * 255, 0, 255).astype(np.uint8))
    P[key] = im
    r = max(W / im.width, H / im.height); b = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.BILINEAR)
    x0 = (b.width - W) // 2; y0 = (b.height - H) // 2
    BG[key] = np.asarray(b.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(30)), np.float32) * 0.3

def paint(key, t, u, tl, f0, f1, z0, z1, ring=None, ring_at=0.6, dim=1.0, free=False):
    im = P[key]; pw, ph = im.size; u = ease(u)
    fx, fy = lerp(f0, f1, u); z = z0 + (z1 - z0) * u
    s = max(BW / pw, BH / ph) * z; cw, ch = BW / s, BH / s
    cx = clamp(fx * pw, cw / 2, pw - cw / 2) if cw < pw else pw / 2
    cy = (fy * ph if free else clamp(fy * ph, ch / 2, ph - ch / 2)) if ch < ph else ph / 2
    x0, y0 = cx - cw / 2, cy - ch / 2
    vx0, vy0, vx1, vy1 = max(0, x0), max(0, y0), min(pw, x0 + cw), min(ph, y0 + ch)
    ow, oh = max(1, int(round((vx1 - vx0) * s))), max(1, int(round((vy1 - vy0) * s)))
    fg = im.resize((ow, oh), Image.BICUBIC, box=(vx0, vy0, vx1, vy1))
    ox, oy = BOX[0] + int(round((vx0 - x0) * s)), BOX[1] + int(round((vy0 - y0) * s))
    base = Image.fromarray(np.clip(BG[key] * (0.97 + 0.03 * math.sin(t)), 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([ox - 16, oy - 16, ox + ow + 16, oy + oh + 16], fill=(0, 0, 0, 90))
    base.paste(fg, (ox, oy))
    d.rectangle([ox - 3, oy - 3, ox + ow + 2, oy + oh + 2], outline=(240, 200, 110, 230), width=3)
    if ring is not None:
        a = clamp((tl - ring_at) / 0.4)
        if a > 0:
            rx, ry = ox + (ring[0] * pw - vx0) * s, oy + (ring[1] * ph - vy0) * s
            r = 64 + 7 * math.sin(t * 5)
            if BOX[0] < rx < BOX[2] and BOX[1] < ry < BOX[3]:
                d.ellipse([rx - r, ry - r, rx + r, ry + r], outline=YEL + (int(240 * a),), width=7)
    out = np.asarray(base.convert("RGB"), np.float32)
    return out * dim if dim != 1.0 else out

# ------------------------------------------------------------------ images + auto shots
CONF = json.load(open(f"{DIR}/conf.json"))
IMGS, cur = [], None
for l in open(f"{DIR}/script.md", encoding="utf-8").read().split("## Opening", 1)[1].splitlines():
    l = l.strip()
    if l.startswith("@"):
        p = l[1:].split(); fx, fy = (float(v) for v in p[1].split(",")) if len(p) > 1 else (0.5, 0.5)
        ring = tuple(float(v) for v in p[2][5:].split(",")) if len(p) > 2 and p[2].startswith("ring=") else None
        cur = dict(key=p[0], focus=(fx, fy), ring=ring, j=0); continue
    if not l or l.startswith("#") or l.startswith("**") or l.startswith("## ") or l == "---": continue
    IMGS.append(dict(cur)); cur["j"] += 1; cur["ring"] = None
assert len(IMGS) == len(BEATS), (len(IMGS), len(BEATS))
for k in sorted({m["key"] for m in IMGS}): reg(k, Image.open(f"{DIR}/p/{k}.jpg"))

def S(key, f0=(0.5, 0.5), f1=None, z0=1.0, z1=1.1, ring=None, ring_at=0.6, free=False, dim=1.0):
    return dict(key=key, f0=f0, f1=f1 or f0, z0=z0, z1=z1, ring=ring, ring_at=ring_at, free=free, dim=dim)
LATE = -1
SHOTS, SEEN, LABELS = [], set(), {}
for i, m in enumerate(IMGS):
    k, (fx, fy), j = m["key"], m["focus"], m["j"]
    dim = 0.85 if BEATS[i]["sec"] in ("Prayer", "Close") else 1.0
    if k.startswith("d_"):   # our diagrams: always the whole chart, a slow gentle push, no label
        SHOTS.append(S(k, (0.5, 0.5), (0.5, 0.5), 1.0 + 0.02 * (j % 2), 1.05 - 0.02 * (j % 2), dim=dim)); SEEN.add(k); continue
    if j == 0:
        first = k not in SEEN
        z0 = 1.0 if first else 1.12; f0 = (0.5, 0.5) if first else (fx + (0.04 if i % 2 else -0.04), fy)
        SHOTS.append(S(k, f0, (fx, fy), z0, z0 + 0.22, ring=m["ring"], ring_at=LATE, dim=dim))
        SEEN.add(k)
    else:
        z = min(1.25 + 0.12 * j, 1.75); dx = 0.035 if j % 2 else -0.035
        SHOTS.append(S(k, (fx, fy), (fx + dx, fy - 0.01), z, z + (0.14 if j % 2 == 0 else -0.12), dim=dim))
DONE = set()
for i, m in enumerate(IMGS):   # label each image the first time it carries a beat after the title card (beats 0-1)
    if i > 1 and m["key"] not in DONE and m["key"] in CONF["labels"]: LABELS[i] = tuple(CONF["labels"][m["key"]]); DONE.add(m["key"])
STARTS = [max(0, bt(i) - 0.25) for i in range(len(BEATS))]


def render_shot(i, t):
    a = STARTS[i]; b = STARTS[i + 1] if i + 1 < len(STARTS) else DUR
    segs = SHOTS[i] if isinstance(SHOTS[i], list) else [(0.0, SHOTS[i])]
    U = clamp((t - a) / max(0.01, b - a))
    k = max(j for j, (u0, _) in enumerate(segs) if u0 <= U)
    u0 = segs[k][0]; u1 = segs[k + 1][0] if k + 1 < len(segs) else 1.0
    sa, sb = a + u0 * (b - a), a + u1 * (b - a)
    sp = segs[k][1]; u = clamp((t - sa) / max(0.01, sb - sa)); tl = t - sa
    ra = sp["ring_at"] if sp["ring_at"] != LATE else (sb - sa) * 0.7
    img = paint(sp["key"], t, u, tl, sp["f0"], sp["f1"], sp["z0"], sp["z1"], sp["ring"], ra, sp["dim"], sp["free"])
    if k > 0 and tl < 0.3:   # crossfade between segments inside one shot
        pp = segs[k - 1][1]; pa = a + segs[k - 1][0] * (b - a)
        prev = paint(pp["key"], t, 1.0, sa - pa, pp["f0"], pp["f1"], pp["z0"], pp["z1"], None, 0, pp["dim"], pp["free"])
        img = prev * (1 - tl / 0.3) + img * (tl / 0.3)
    return img

# ------------------------------------------------------------------ overlays (from jlf/story.py)
GOLDW = set(CONF["gold"])
CHAPTERS = {}
for i, b in enumerate(BEATS):
    s = b["sec"]
    if (i == 0 or BEATS[i - 1]["sec"] != s) and s not in ("Opening", "Close"):
        CHAPTERS[i] = s.upper().replace(". ", "  ·  ", 1) if s[0].isdigit() else s.upper()
def wrap(d, words, f, maxw):
    sp = d.textlength(" ", font=f); lines, cur, cw = [], [], 0
    for w in words:
        ww = d.textlength(w, font=f)
        if cur and cw + sp + ww > maxw: lines.append(cur); cur, cw = [], 0
        cur.append((w, ww)); cw += (sp if len(cur) > 1 else 0) + ww
    lines.append(cur); return lines, sp

def caption(d, t, i):
    b = BEATS[i]; words = b["text"].split()
    rate = (b["end"] - b["t"]) * 0.95 / len(words)
    f = F(MONT.format(800), 54); lines, sp = wrap(d, [w.upper() for w in words], f, 940)
    pages, k0 = [], 0                      # pages of <= 2 lines, so captions never cover the painting
    for p in range(0, len(lines), 2):
        pl = lines[p:p + 2]; n = sum(len(l) for l in pl); pages.append((k0, pl)); k0 += n
    cur = int(clamp((t - b["t"]) / rate, 0, len(words) - 1)) if t >= b["t"] else 0
    if t > b["end"]: cur = len(words) - 1
    k, pl = [pg for pg in pages if pg[0] <= cur][-1]
    y0 = 1440
    for li, ln in enumerate(pl):
        lw = sum(x for _, x in ln) + sp * (len(ln) - 1); x = (W - lw) / 2
        for w, ww in ln:
            al = clamp((t - b["t"] - rate * k + 0.12) / 0.12) * 0.75 + 0.25 if t >= b["t"] - 0.12 else 0.25
            if t > b["end"]: al = 1
            gold = words[k].strip(",.?!:;\"'").lower() in GOLDW or words[k].lower() in GOLDW
            d.text((x, y0 + li * 66), w, font=f, fill=(GOLD if gold else WHITE) + (int(255 * al),), stroke_width=5, stroke_fill=(0, 0, 0, int(230 * al)))
            x += ww + sp; k += 1

def verse_card(d, t, i):
    b = BEATS[i]; a = clamp((t - b["t"] + 0.3) / 0.35)
    d.rectangle([0, 0, W, H], fill=(8, 6, 10, int(160 * a)))
    words = b["text"].split()
    for size in (76, 70, 64, 58, 52):
        f = F(CORM.format(700, "italic"), size); lines, sp = wrap(d, words, f, 900)
        if len(lines) * size * 1.25 < 900: break
    lh = int(size * 1.25); y0 = (H - lh * len(lines)) / 2 + 30
    if b.get("ref"):
        fr = F(MONT.format(800), 56); rw = d.textlength(b["ref"].upper(), font=fr)
        d.text(((W - rw) / 2, y0 - 120), b["ref"].upper(), font=fr, fill=YEL + (int(255 * a),), stroke_width=4, stroke_fill=(0, 0, 0, int(255 * a)))
    rate = (b["end"] - b["t"]) * 0.95 / len(words); k = 0
    for li, ln in enumerate(lines):
        lw = sum(x for _, x in ln) + sp * (len(ln) - 1); x = (W - lw) / 2
        for w, ww in ln:
            r = clamp((t - b["t"] - rate * k + 0.1) / 0.2); al = a * (0.45 + 0.55 * r)
            d.text((x, y0 + li * lh), w, font=f, fill=(255, 246, 228, int(255 * al)), stroke_width=2, stroke_fill=(0, 0, 0, int(220 * al)))
            x += ww + sp; k += 1

def label(d, t, i):
    if i not in LABELS or i >= CLOSE0: return
    big, ref = LABELS[i]; u = clamp((t - bt(i) - 0.1) / 0.3)
    if u <= 0: return
    sc = 0.85 + 0.15 * ease(u); al = int(255 * u); sz = 96 if len(big) < 12 else 72
    while d.textlength(big, font=F(MONT.format(900), int(sz * sc))) > 960 and sz > 36: sz -= 4
    f = F(MONT.format(900), int(sz * sc))
    y = 160
    if ref:
        rs_ = 36
        while d.textlength(ref, font=F(MONT.format(800), rs_)) > 980 and rs_ > 20: rs_ -= 2
        fr = F(MONT.format(800), rs_); w = d.textlength(ref, font=fr)
        d.text(((W - w) / 2, y), ref, font=fr, fill=YEL + (al,), stroke_width=4, stroke_fill=(0, 0, 0, al)); y += 50
    w = d.textlength(big, font=f); d.text(((W - w) / 2, y), big, font=f, fill=WHITE + (al,), stroke_width=6, stroke_fill=(0, 0, 0, al))

def chapter(d, t, i):
    return
    keys = [k for k in CHAPTERS if bt(k) - 0.3 <= t]
    if not keys: return
    k = max(keys); s = t - bt(k) + 0.3
    if s > 3.2: return
    a = clamp(s / 0.4) * clamp((3.2 - s) / 0.5); f = F(MONT.format(800), 30)
    d.rectangle([50, 24, 50 + 7, 64], fill=GOLD + (int(255 * a),))
    d.text((72, 27), CHAPTERS[k], font=f, fill=WHITE + (int(255 * a),), stroke_width=3, stroke_fill=(0, 0, 0, int(200 * a)))

def hook_text(d, t):
    if t > be(1) + 0.2: return
    a = clamp((be(1) + 0.2 - t) / 0.4) * clamp(t / 0.6)
    def ct(y, s, f, col, sw):
        while d.textlength(s, font=f) > 1000 and f.size > 30: f = F(f.path, f.size - 4)
        w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=col + (int(255 * a),), stroke_width=sw, stroke_fill=(0, 0, 0, int(255 * a)))
    ct(110, CONF["hook"][0], F(MONT.format(700), 38), YEL, 4)
    ct(160, CONF["hook"][1], F(MONT.format(900), 100), WHITE, 8)
    ct(290, CONF["hook"][2], F(MONT.format(800), 46), GOLD, 5)

CLOSE0 = [i for i, b in enumerate(BEATS) if b["sec"] == "Close"][0]
def end_card(d, t):
    i = CLOSE0
    def ct(y, s, f, col, sw, a):
        if a <= 0: return
        w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=col + (int(255 * a),), stroke_width=sw, stroke_fill=(0, 0, 0, int(255 * a)))
    ct(150, "FOLLOW", F(MONT.format(900), 120), WHITE, 8, clamp((t - bt(i) - 0.6) / 0.4))
    ct(290, CONF["next"], F(MONT.format(800), 44), GOLD, 5, clamp((t - bt(i) - 2.0) / 0.4))
    ct(1700, "@GODNOFILTER", F(MONT.format(800), 50), YEL, 4, clamp((t - bt(i) - 1.0) / 0.4))

def beat_at(t):
    cur = 0
    for i, b in enumerate(BEATS):
        if b["t"] - 0.15 <= t: cur = i
    return cur

BOTG = (1 - 0.55 * np.clip((np.linspace(0, 1, H) - 0.78) / 0.22, 0, 1) ** 1.2)[:, None, None].astype(np.float32)
def frame(t):
    idx = max(i for i, s in enumerate(STARTS) if s <= t) if t >= STARTS[0] else 0
    img = render_shot(idx, t); a = STARTS[idx]
    if idx > 0 and t - a < 0.4: img = render_shot(idx - 1, a - 0.001) * (1 - (t - a) / 0.4) + img * ((t - a) / 0.4)
    if t < 0.6: img = img * (t / 0.6)
    if t > DUR - 1.2: img = img * clamp((DUR - t) / 1.2)
    img = img * BOTG
    base = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay)
    i = beat_at(t); b = BEATS[i]
    if b["kind"] == "verse" and t <= b["end"] + 0.7: verse_card(d, t, i)
    else:
        if i >= CLOSE0: end_card(d, t)
        if t <= b["end"] + 0.5: caption(d, t, i)
        label(d, t, i)
    chapter(d, t, i); hook_text(d, t)
    sh = Image.new("RGBA", (W, H)); sh.putalpha(lay.split()[3].filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.7)))
    return Image.alpha_composite(Image.alpha_composite(base, sh), lay).convert("RGB")

if __name__ == "__main__":
    if "--frames" in sys.argv:
        os.makedirs(f"{DIR}/chk", exist_ok=True)
        for t in [float(x) for x in sys.argv[sys.argv.index("--frames") + 1].split(",")]:
            frame(t).save(f"{DIR}/chk/f_{t:07.2f}.jpg", quality=88)
        sys.exit()
    ci, cn = (int(sys.argv[sys.argv.index("--chunk") + 1]), int(sys.argv[sys.argv.index("--chunk") + 2])) if "--chunk" in sys.argv else (0, 1)
    N = int(DUR * FPS); n0, n1 = N * ci // cn, N * (ci + 1) // cn
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"{DIR}/chunk_{ci}.mp4"], stdin=subprocess.PIPE)
    import time; t0 = time.time()
    for n in range(n0, n1):
        pr.stdin.write(frame(n / FPS).tobytes())
        if (n - n0) % 900 == 0: print(f"chunk {ci}: {n - n0}/{n1 - n0} frames, {time.time() - t0:.0f}s", flush=True)
    pr.stdin.close(); pr.wait(); print("CHUNK OK", ci)
