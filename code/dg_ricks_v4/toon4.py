"""toon4 (Nov 22, 2026): upgraded Ricks-Clips-style cartoon rig for David & Goliath.
Continuous pose params (eased between keyframes by the comp), 2-bone arms/legs, lean + squash/stretch,
lip-sync mouth (open amount + round/wide shape), blinks, eye look, props in hand.
draw(who, pose, t, ppu, face, view, look, talk, vis, flip) -> (RGBA image, foot_x, foot_y) in image pixels."""
import math, random
from PIL import Image, ImageDraw, ImageChops, ImageFilter
OUT = (28, 22, 24); SS = 3  # comp may lower SS for big characters
CHARS = {
 "david":   dict(head=(240, 214, 178), robe=(232, 220, 190), robe_sh=(196, 182, 150), trim=(150, 100, 60), belt=(120, 72, 40), hair=(70, 42, 26), beard=None, size=0.86, curls=True),
 "goliath": dict(head=(226, 190, 160), robe=(120, 60, 48), robe_sh=(90, 42, 34), trim=(200, 150, 70), belt=(70, 50, 36), beard=(34, 26, 22), size=1.55, armor=(176, 128, 60), helm=(190, 140, 64)),
 "saul":    dict(head=(236, 210, 180), robe=(110, 54, 130), robe_sh=(80, 36, 96), trim=(240, 200, 90), belt=(60, 40, 30), beard=(200, 198, 192), size=1.0, crown=True),
 "soldier": dict(head=(232, 204, 170), robe=(60, 96, 160), robe_sh=(42, 70, 124), trim=(230, 210, 150), belt=(80, 56, 36), beard=(60, 40, 28), size=0.95, helm=(150, 120, 80)),
 "brother": dict(head=(230, 200, 166), robe=(150, 110, 70), robe_sh=(116, 84, 52), trim=(220, 190, 130), belt=(70, 50, 36), beard=(52, 34, 24), size=1.0, wrap=(236, 226, 200)),
}
REST = dict(lean=0.0, bob=0.0, sq=1.0, tilt=0.0, aL=(12, 8), aR=(12, 8), lL=(4, 0), lR=(4, 0), hx=0.0)
def _e(d, cx, cy, rx, ry, fill, w, outline=OUT): d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=outline, width=w)
def _limb(o, a1, a2, L1, L2, side, view):
    """2-bone limb from origin o; angles in degrees from straight down; positive = outward (front) / forward (side)."""
    s = side if view == "front" else 1
    r1 = math.radians(a1); r2 = math.radians(a1 + a2)
    p1 = (o[0] + s * math.sin(r1) * L1, o[1] + math.cos(r1) * L1)
    p2 = (p1[0] + s * math.sin(r2) * L2, p1[1] + math.cos(r2) * L2)
    return [o, p1, p2]
_GR = {}
def grain(size):
    if size not in _GR:
        if len(_GR) > 30: _GR.clear()
        _GR[size] = Image.effect_noise(size, 22).filter(ImageFilter.GaussianBlur(1.2))
    return _GR[size]
def prop(d, kind, hand, u, side, view, t, lw, thin, P):
    hx, hy = hand
    if kind == "spear":
        L = 2.6 * u; ang = math.radians(P.get("spear_ang") or -8)
        x2, y2 = hx + math.sin(ang) * L * 0.75, hy - math.cos(ang) * L * 0.75; x1, y1 = hx - math.sin(ang) * L * 0.25, hy + math.cos(ang) * L * 0.25
        d.line([(x1, y1), (x2, y2)], fill=(90, 60, 36), width=int(0.09 * u)); d.line([(x1, y1), (x2, y2)], fill=OUT, width=max(2, thin // 2))
        tip = [(x2 + math.sin(ang) * 0.32 * u, y2 - math.cos(ang) * 0.32 * u), (x2 + math.cos(ang) * 0.1 * u, y2 + math.sin(ang) * 0.1 * u), (x2 - math.cos(ang) * 0.1 * u, y2 - math.sin(ang) * 0.1 * u)]
        d.polygon(tip, fill=(200, 200, 210), outline=OUT)
    elif kind == "sling":
        spin = P.get("sling_spin", None)
        if spin is not None:
            r = 0.55 * u; a = spin
            px, py = hx + math.cos(a) * r, hy + math.sin(a) * r * 0.5 - 0.2 * u
            d.line([(hx, hy), (px, py)], fill=(120, 80, 40), width=max(2, thin))
            _e(d, px, py, 0.07 * u, 0.07 * u, (150, 110, 70), max(1, thin // 2))
            for k in range(1, 5):                                     # motion arc
                aa = a - k * 0.35
                d.arc([hx - r, hy - r * 0.5 - 0.2 * u, hx + r, hy + r * 0.5 - 0.2 * u], math.degrees(aa) - 12, math.degrees(aa), fill=(255, 255, 255), width=max(1, thin // 2))
        else:
            d.line([(hx, hy), (hx + 0.05 * u, hy + 0.45 * u)], fill=(120, 80, 40), width=max(2, thin))
            _e(d, hx + 0.05 * u, hy + 0.48 * u, 0.07 * u, 0.05 * u, (150, 110, 70), max(1, thin // 2))
    elif kind == "basket":
        d.rounded_rectangle([hx - 0.34 * u, hy - 0.05 * u, hx + 0.34 * u, hy + 0.32 * u], radius=int(0.08 * u), fill=(180, 130, 70), outline=OUT, width=thin)
        for k in range(3): _e(d, hx - 0.18 * u + k * 0.18 * u, hy - 0.06 * u, 0.12 * u, 0.08 * u, (226, 170, 90), max(1, thin // 2))
        for k in range(4): d.line([(hx - 0.3 * u, hy + 0.04 * u + k * 0.07 * u), (hx + 0.3 * u, hy + 0.04 * u + k * 0.07 * u)], fill=(140, 96, 50), width=max(1, thin // 2))
    elif kind == "staff":
        d.line([(hx, hy - 0.9 * u), (hx, hy + 0.95 * u)], fill=(110, 74, 40), width=int(0.07 * u)); d.arc([hx - 0.25 * u, hy - 1.15 * u, hx + 0.05 * u, hy - 0.75 * u], 180, 360, fill=(110, 74, 40), width=int(0.07 * u))
    elif kind == "stone":
        _e(d, hx, hy - 0.04 * u, 0.08 * u, 0.065 * u, (200, 198, 190), max(1, thin // 2))
    elif kind == "shield":
        _e(d, hx + side * 0.05 * u, hy, 0.42 * u, 0.46 * u, (150, 100, 50), lw); _e(d, hx + side * 0.05 * u, hy, 0.12 * u, 0.12 * u, (210, 170, 80), thin)
    elif kind == "fist":
        pass
def draw(who, P=None, t=0.0, ppu=200, face="calm", view="front", look=(0, 0), talk=0.0, vis=0.5, flip=False, shadow=True):
    c = CHARS[who]; P = dict(REST, **(P or {})); u = ppu * c["size"] * SS
    Wc, Hc = int(5.6 * u), int(5.2 * u)
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ox, fy = Wc / 2, Hc - 0.5 * u
    lw = max(3, int(0.07 * u)); sw = max(3, int(0.08 * u)); thin = max(2, lw // 2)
    bob = P["bob"] * u + 0.012 * u * math.sin(t * 2.4)
    hip_y = fy - 0.53 * u - bob
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([ox - 0.6 * u, fy - 0.09 * u, ox + 0.6 * u, fy + 0.09 * u], fill=(0, 0, 0, 80))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(0.05 * u)))
    body = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(body)
    # legs
    for side, key in ((-1, "lL"), (1, "lR")):
        a1, a2 = P[key]
        pts = _limb((ox + side * 0.15 * u, hip_y), a1, -abs(a2) if view == "front" else -a2, 0.27 * u, 0.27 * u, side, view)
        d.line(pts, fill=OUT, width=sw, joint="curve")
        fx_ = pts[-1][0] + (0.09 * u if view == "side" else side * 0.04 * u)
        _e(d, fx_, pts[-1][1] - 0.02 * u, 0.13 * u, 0.07 * u, (60, 44, 34), thin)
    # body
    bx = (0.42 if view == "front" else 0.34) * u * (1.12 if who == "goliath" else 1.0)
    by0, by1 = hip_y - 0.92 * u, hip_y + 0.10 * u
    bb = [ox - bx, by0, ox + bx, by1]; rad = int(0.34 * u)
    d.rounded_rectangle(bb, radius=rad, fill=c["robe"])
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle(bb, radius=rad, fill=255)
    cut = Image.new("L", im.size, 0); ImageDraw.Draw(cut).ellipse([ox - bx * 2.3, by0 - 0.4 * u, ox + bx * 0.5, by1 + 0.4 * u], fill=255)
    body.paste(Image.new("RGBA", im.size, c["robe_sh"] + (255,)), (0, 0), ImageChops.subtract(m, cut)); d = ImageDraw.Draw(body)
    if c.get("armor"):                                   # bronze scale armour
        for row in range(6):
            for col in range(-3, 4):
                cx_ = ox + col * 0.13 * u + (0.065 * u if row % 2 else 0); cy_ = by0 + 0.22 * u + row * 0.1 * u
                if abs(cx_ - ox) < bx - 0.08 * u: d.chord([cx_ - 0.07 * u, cy_ - 0.05 * u, cx_ + 0.07 * u, cy_ + 0.07 * u], 0, 180, fill=c["armor"], outline=OUT, width=max(1, thin // 2))
    for fxo in (-0.18, 0.12): d.line([(ox + fxo * u, by0 + 0.64 * u), (ox + (fxo - 0.03) * u, by1 - 0.06 * u)], fill=c["robe_sh"], width=thin)
    d.arc([ox - 0.22 * u, by0 - 0.10 * u, ox + 0.22 * u, by0 + 0.22 * u], 20, 160, fill=c["trim"], width=max(3, int(0.05 * u)))
    by = by0 + 0.58 * u
    d.rectangle([ox - bx + lw * 0.6, by, ox + bx - lw * 0.6, by + 0.11 * u], fill=c["belt"])
    d.line([(ox - bx + lw, by), (ox + bx - lw, by)], fill=OUT, width=thin); d.line([(ox - bx + lw, by + 0.11 * u), (ox + bx - lw, by + 0.11 * u)], fill=OUT, width=thin)
    if who == "david":                                    # shepherd's bag strap + pouch
        d.line([(ox - bx * 0.7, by0 + 0.15 * u), (ox + bx * 0.6, by - 0.02 * u)], fill=(120, 80, 44), width=max(3, int(0.05 * u)))
        d.rounded_rectangle([ox + bx * 0.35, by - 0.04 * u, ox + bx * 0.95, by + 0.24 * u], radius=int(0.05 * u), fill=(150, 104, 60), outline=OUT, width=thin)
    d.rounded_rectangle(bb, radius=rad, outline=OUT, width=lw)
    # arms + props
    shy = by0 + 0.24 * u
    for side, key in ((-1, "aL"), (1, "aR")):
        a1, a2 = P[key]
        sx0 = ox + side * (bx - 0.05 * u) if view == "front" else ox + 0.02 * u
        pts = _limb((sx0, shy), a1, a2, 0.32 * u, 0.30 * u, side, view)
        item = P.get("item" + ("L" if side < 0 else "R"))
        if item == "shield": prop(d, item, pts[-1], u, side, view, t, lw, thin, P)
        d.line(pts, fill=OUT, width=sw, joint="curve")
        _e(d, pts[-1][0], pts[-1][1], 0.09 * u, 0.09 * u, (250, 246, 238), thin)
        if item and item != "shield": prop(d, item, pts[-1], u, side, view, t, lw, thin, P)
    # head
    hr = 0.56 * u
    hcx = ox + (0.05 * u if view == "side" else 0) + P["hx"] * u + (math.sin(t * 22) * 0.02 * u if face in ("scared", "shocked") else 0)
    hcy = by0 - 0.40 * u
    head = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(head)
    _e(d, hcx, hcy, hr, hr * 0.96, c["head"], lw)
    hm = Image.new("L", im.size, 0); ImageDraw.Draw(hm).ellipse([hcx - hr, hcy - hr * 0.96, hcx + hr, hcy + hr * 0.96], fill=255)
    hc = Image.new("L", im.size, 0); ImageDraw.Draw(hc).ellipse([hcx - hr * 1.6, hcy - hr * 1.25, hcx + hr * 0.6, hcy + hr * 1.1], fill=255)
    head.paste(Image.new("RGBA", im.size, tuple(int(v * 0.86) for v in c["head"]) + (255,)), (0, 0), ImageChops.subtract(hm, hc)); d = ImageDraw.Draw(head)
    _e(d, hcx, hcy, hr, hr * 0.96, None, lw)
    d.arc([hcx - hr * 0.80, hcy - hr * 0.82, hcx + hr * 0.10, hcy + hr * 0.20], 200, 245, fill=(255, 252, 244), width=max(3, thin))
    fxo = 0.24 * u if view == "side" else 0.0
    if c["beard"]:
        d.chord([hcx - hr * 0.86 + fxo * 0.6, hcy + hr * 0.10, hcx + hr * 0.86 + fxo * 0.6, hcy + hr * 1.12], 0, 180, fill=c["beard"], outline=OUT, width=thin)
    # eyes
    blink = ((t + hash(who) % 7 * 0.37) % 3.1) < 0.1 and face not in ("sleep", "shocked", "scared")
    eyes = [(-0.20, 0), (0.20, 0)] if view == "front" else [(0.30, 0)]
    big = {"shocked": 1.35, "scared": 1.2, "amazed": 1.25}.get(face, 1.0)
    ey = hcy - 0.04 * u
    for ex, _ in eyes:
        x = hcx + ex * u + (fxo * 0.25 if view == "side" else 0); rx, ry = 0.135 * u * big, 0.16 * u * big
        if face == "sleep" or blink:
            d.arc([x - rx, ey - ry * 0.3, x + rx, ey + ry * 0.9], 200, 340, fill=OUT, width=max(3, thin + 1))
        elif face == "laugh":
            d.arc([x - rx, ey - ry * 0.2, x + rx, ey + ry * 1.0], 200, 340, fill=OUT, width=max(3, thin + 1))
        else:
            _e(d, x, ey, rx, ry, (255, 255, 255), thin)
            pr = 0.058 * u * (0.7 if face in ("shocked", "scared") else 1.0)
            px = x + look[0] * rx * 0.45 + (0.05 * u if view == "side" else 0); py = ey + look[1] * ry * 0.4 + 0.02 * u
            _e(d, px, py, pr, pr * 1.1, OUT, 1); d.ellipse([px - pr * 0.45, py - pr * 0.7, px - pr * 0.05, py - pr * 0.3], fill=(255, 255, 255))
            if face in ("smug", "angry", "tired", "determined"):
                d.chord([x - rx * 1.05, ey - ry * 1.05, x + rx * 1.05, ey + ry * (0.05 if face == "determined" else 0.2)], 180, 360, fill=c["head"], outline=OUT, width=thin)
        d.arc([x - rx * 0.8, ey + ry * 0.55, x + rx * 0.8, ey + ry * 1.35], 30, 150, fill=tuple(int(v * 0.7) for v in c["head"]), width=thin)
        tilt = {"worried": -0.07, "scared": -0.09, "shocked": -0.05, "angry": 0.10, "smug": 0.03, "stern": 0.06, "determined": 0.07, "sad": -0.08, "laugh": -0.03}.get(face, 0.0)
        sd = -1 if ex < 0 else 1
        if view == "side": sd = 1
        by_ = ey - ry - 0.07 * u - (0.05 * u if face in ("shocked", "amazed") else 0)
        d.line([(x - 0.12 * u, by_ + sd * tilt * u), (x + 0.12 * u, by_ - sd * tilt * u)], fill=OUT, width=max(3, int(lw * 0.9)))
    # mouth: talk = open 0..1, vis = 0 wide (ee) .. 1 round (oo)
    mx = hcx + (0.34 * u if view == "side" else 0); my = hcy + (0.36 * u if c["beard"] else 0.30 * u)
    op = max(talk, {"shocked": 0.9, "scared": 0.6, "yell": 1.0, "laugh": 0.8}.get(face, 0.0))
    if op > 0.08:
        wdt = (0.16 - 0.08 * vis) * u * (1.15 if face in ("yell", "laugh") else 1.0); hgt = (0.03 + 0.15 * op) * u
        d.rounded_rectangle([mx - wdt, my - hgt * 0.35, mx + wdt, my + hgt], radius=int(min(wdt, hgt) * 0.9), fill=(110, 30, 40), outline=OUT, width=thin)
        if op > 0.35: d.rectangle([mx - wdt * 0.7, my - hgt * 0.35 + thin, mx + wdt * 0.7, my - hgt * 0.35 + thin + 0.035 * u], fill=(255, 255, 255))
        d.ellipse([mx - wdt * 0.55, my + hgt * 0.35, mx + wdt * 0.55, my + hgt * 0.95], fill=(220, 90, 100))
    elif face in ("smug", "happy", "calm", "determined"):
        d.arc([mx - 0.09 * u, my - 0.07 * u, mx + 0.09 * u, my + 0.05 * u], 20 if face != "smug" else 10, 160 if face != "smug" else 120, fill=OUT, width=thin)
    else:
        d.arc([mx - 0.08 * u, my, mx + 0.08 * u, my + 0.10 * u], 200, 340, fill=OUT, width=thin)
    if face in ("worried", "scared", "shocked"):
        sxp, syp = hcx + hr * 0.78, hcy - hr * 0.35 + (t * 0.25 % 0.3) * u
        d.polygon([(sxp, syp - 0.11 * u), (sxp - 0.06 * u, syp), (sxp + 0.06 * u, syp)], fill=(150, 210, 255), outline=OUT); _e(d, sxp, syp + 0.01 * u, 0.06 * u, 0.06 * u, (150, 210, 255), max(1, thin // 2))
    # headwear / hair
    if c.get("curls"):
        for k in range(9):
            a = math.pi * (1.05 + k * 0.11); cx_ = hcx + math.cos(a) * hr * 0.92; cy_ = hcy + math.sin(a) * hr * 0.86
            _e(d, cx_, cy_, 0.17 * u, 0.15 * u, c["hair"], thin)
        _e(d, hcx - hr * 0.2, hcy - hr * 0.8, 0.2 * u, 0.14 * u, c["hair"], thin); _e(d, hcx + hr * 0.25, hcy - hr * 0.82, 0.2 * u, 0.14 * u, c["hair"], thin)
    elif c.get("helm"):
        d.chord([hcx - hr * 1.06, hcy - hr * 1.18, hcx + hr * 1.06, hcy + hr * 0.2], 180, 360, fill=c["helm"], outline=OUT, width=lw)
        d.rectangle([hcx - hr * 1.02, hcy - hr * 0.50, hcx + hr * 1.02, hcy - hr * 0.38], fill=tuple(int(v * 0.8) for v in c["helm"]))
        d.line([(hcx - hr * 1.02, hcy - hr * 0.38), (hcx + hr * 1.02, hcy - hr * 0.38)], fill=OUT, width=thin)
        if who == "goliath":
            d.polygon([(hcx - 0.1 * u, hcy - hr * 1.12), (hcx + 0.1 * u, hcy - hr * 1.12), (hcx + 0.05 * u, hcy - hr * 1.75), (hcx - 0.35 * u, hcy - hr * 1.6)], fill=(170, 40, 30), outline=OUT)
            d.line([(hcx, hcy - hr * 0.40), (hcx, hcy + hr * 0.02)], fill=c["helm"], width=int(0.08 * u)); d.line([(hcx, hcy - hr * 0.40), (hcx, hcy + hr * 0.02)], fill=OUT, width=thin)
    elif c.get("crown"):
        d.chord([hcx - hr * 1.04, hcy - hr * 1.12, hcx + hr * 1.04, hcy + hr * 0.12], 180, 360, fill=(240, 232, 214), outline=OUT, width=lw)
        pts = [(hcx - hr * 0.7, hcy - hr * 0.75)]
        for k in range(5): pts += [(hcx - hr * 0.7 + (k + 0.5) * hr * 0.28, hcy - hr * 1.35), (hcx - hr * 0.7 + (k + 1) * hr * 0.28, hcy - hr * 1.0)]
        pts += [(hcx + hr * 0.7, hcy - hr * 0.75)]
        d.polygon(pts, fill=(236, 190, 60), outline=OUT, width=thin)
    else:
        wr = c.get("wrap", (236, 226, 200))
        d.chord([hcx - hr * 1.04, hcy - hr * 1.12, hcx + hr * 1.04, hcy + hr * 0.12], 180, 360, fill=wr, outline=OUT, width=lw)
        d.rectangle([hcx - hr * 0.99, hcy - hr * 0.60, hcx + hr * 0.99, hcy - hr * 0.48], fill=(150, 90, 50))
    # head tilt about the neck
    if abs(P["tilt"]) > 0.1: head = head.rotate(-P["tilt"], resample=Image.BICUBIC, center=(hcx, by0 + 0.05 * u))
    body.alpha_composite(head)
    # paper grain
    a = body.split()[3]; g = grain(body.size)
    shade = Image.new("RGBA", body.size, (0, 0, 0, 0)); shade.paste(Image.new("RGBA", body.size, (40, 30, 30, 255)), (0, 0), ImageChops.multiply(a, g.point(lambda v: int(max(0, 128 - v) * 0.35))))
    body.alpha_composite(shade)
    # lean (rotate about feet) + squash/stretch
    if abs(P["lean"]) > 0.1: body = body.rotate(-P["lean"], resample=Image.BICUBIC, center=(ox, fy))
    if abs(P["sq"] - 1) > 0.01:
        sy = P["sq"]; sx = 1 / math.sqrt(sy); nw, nh = int(Wc * sx), int(Hc * sy)
        b2 = body.resize((nw, nh), Image.BICUBIC); body = Image.new("RGBA", im.size, (0, 0, 0, 0))
        body.alpha_composite(b2, (int(ox - ox * sx), int(fy - fy * sy))) if nw <= Wc and nh <= Hc else body.paste(b2.crop((0, 0, Wc, Hc)), (0, 0))
    im.alpha_composite(body)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    small = im.resize((Wc // SS, Hc // SS), Image.LANCZOS)
    return small, small.width / 2, fy / SS
if __name__ == "__main__":
    bg = Image.new("RGBA", (2000, 760), (150, 190, 230, 255))
    tests = [("david", dict(aR=(150, 30), itemR="sling"), "determined", 0.6, 0.3), ("goliath", dict(aR=(60, 40), itemR="spear", lean=-6), "yell", 1.0, 0.4),
             ("saul", dict(aL=(30, 120), aR=(20, 10)), "worried", 0.0, 0.5), ("soldier", dict(itemL="shield"), "scared", 0.0, 0.5),
             ("david", dict(aL=(40, 90), aR=(40, 90), itemR="basket"), "happy", 0.3, 0.2), ("goliath", dict(lean=12, aL=(30, 10), aR=(60, 10), tilt=-12), "laugh", 0.8, 0.5)]
    x = 170
    for who, P, face, talk, vis in tests:
        im, fx, fy = draw(who, P, 0.4, 130, face, "front", (0.3, 0), talk, vis)
        bg.alpha_composite(im, (int(x - fx), int(720 - fy))); x += 330
    bg.convert("RGB").save("/tmp/toon4_test.png")
