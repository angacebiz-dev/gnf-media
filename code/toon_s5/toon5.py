"""toon5 (Nov 19, 2026): v3 characters + crowns/helmet/armour/hair, new poses (reach, hug, sling, arms_up, sink, sit), per-style outline colour/width (STYLE dict).
v3 cartoon characters (our own designs, Ricks-Clips-like look): big cream heads, huge expressive eyes with
eye-bags, thick dark outline, stick arms/legs with round mitts, detailed robes (folds, stitching, belt buckle),
soft paper-grain texture, ground shadow. Drawn at SSx on a small canvas, downscaled (anti-aliased).
draw(base_rgba, cx, foot_y, ppu, who, view, pose, face, t, flip, look, ret, lie)"""
import math, random
from PIL import Image, ImageDraw, ImageChops, ImageFilter

OUT = (28, 22, 24)
SS = 3
STYLE = dict(out=(28, 22, 24), lw=1.0, grain=True, pastel=0.0)
CHARS = {
    "jonah":   dict(head=(238, 222, 196), robe=(70, 150, 120), robe_sh=(48, 112, 90), trim=(236, 200, 120), wrap=(244, 236, 214), band=(178, 128, 60), beard=(74, 46, 32), belt=(120, 72, 40)),
    "sailor1": dict(head=(236, 214, 186), robe=(48, 98, 176), robe_sh=(34, 70, 138), trim=(240, 220, 160), wrap=(200, 70, 56), band=(120, 40, 30), beard=(40, 28, 22), belt=(90, 60, 40), stache=True),
    "sailor2": dict(head=(242, 226, 200), robe=(206, 72, 52), robe_sh=(160, 50, 38), trim=(250, 230, 170), wrap=(236, 220, 176), band=(70, 110, 80), beard=None, belt=(70, 50, 36)),
    "captain": dict(head=(234, 212, 182), robe=(110, 54, 120), robe_sh=(80, 36, 90), trim=(240, 200, 90), wrap=(46, 52, 92), band=(230, 186, 64), beard=(205, 205, 200), belt=(60, 40, 30)),
    "david":   dict(head=(240, 218, 186), robe=(196, 160, 96), robe_sh=(156, 124, 70), trim=(120, 70, 40), wrap=(110, 66, 40), band=(170, 50, 40), beard=None, belt=(110, 70, 40), hair=(110, 66, 40)),
    "goliath": dict(head=(226, 196, 160), robe=(176, 128, 58), robe_sh=(130, 90, 40), trim=(220, 180, 100), wrap=(176, 128, 58), band=(120, 80, 36), beard=(40, 26, 20), belt=(80, 50, 30), helmet=True, armor=True),
    "saul":    dict(head=(236, 214, 186), robe=(120, 40, 60), robe_sh=(88, 26, 42), trim=(236, 196, 90), wrap=(120, 40, 60), band=(236, 196, 90), beard=(70, 46, 30), belt=(60, 40, 30), crown=True),
    "soldier": dict(head=(236, 214, 186), robe=(120, 110, 90), robe_sh=(90, 82, 66), trim=(200, 170, 110), wrap=(150, 116, 70), band=(100, 70, 40), beard=(60, 40, 30), belt=(70, 50, 34), helmet=True),
    "daniel":  dict(head=(236, 214, 186), robe=(56, 84, 150), robe_sh=(40, 60, 112), trim=(236, 200, 120), wrap=(236, 226, 206), band=(90, 110, 170), beard=(206, 204, 198), belt=(120, 80, 50)),
    "darius":  dict(head=(232, 208, 176), robe=(104, 50, 140), robe_sh=(76, 34, 104), trim=(240, 200, 90), wrap=(104, 50, 140), band=(240, 200, 90), beard=(36, 26, 22), belt=(200, 160, 60), crown=True),
    "official":dict(head=(234, 210, 180), robe=(150, 40, 46), robe_sh=(112, 28, 32), trim=(236, 190, 90), wrap=(60, 46, 40), band=(200, 150, 60), beard=(30, 22, 18), belt=(60, 40, 30), stache=True),
    "elijah":  dict(head=(230, 204, 170), robe=(120, 84, 52), robe_sh=(88, 60, 36), trim=(70, 50, 30), wrap=(150, 112, 70), band=(90, 64, 40), beard=(190, 188, 180), belt=(60, 40, 26), sack=True),
    "baalp":   dict(head=(236, 212, 182), robe=(190, 50, 40), robe_sh=(140, 32, 26), trim=(250, 200, 80), wrap=(250, 200, 80), band=(190, 50, 40), beard=(36, 26, 20), belt=(250, 200, 80)),
    "israelite":dict(head=(240, 220, 190), robe=(90, 140, 170), robe_sh=(64, 104, 130), trim=(240, 220, 170), wrap=(230, 220, 200), band=(150, 110, 70), beard=(70, 50, 30), belt=(100, 70, 40)),
    "jesus":   dict(head=(232, 206, 174), robe=(246, 240, 228), robe_sh=(206, 198, 184), trim=(70, 110, 170), wrap=(246, 240, 228), band=(70, 110, 170), beard=(92, 62, 40), belt=(70, 110, 170), hair=(92, 62, 40)),
    "peter":   dict(head=(236, 210, 178), robe=(214, 120, 54), robe_sh=(170, 90, 36), trim=(240, 220, 160), wrap=(214, 120, 54), band=(120, 70, 40), beard=(110, 100, 92), belt=(90, 60, 40), hair=(110, 100, 92)),
    "disciple":dict(head=(238, 216, 188), robe=(100, 150, 110), robe_sh=(72, 112, 80), trim=(230, 220, 170), wrap=(230, 214, 180), band=(120, 90, 60), beard=(60, 42, 30), belt=(90, 64, 40)),
    "son":     dict(head=(242, 222, 194), robe=(220, 60, 120), robe_sh=(170, 40, 90), trim=(250, 210, 80), wrap=(60, 40, 30), band=(60, 40, 30), beard=None, belt=(250, 210, 80), hair=(60, 40, 30)),
    "son_rag": dict(head=(226, 204, 174), robe=(140, 118, 90), robe_sh=(104, 86, 64), trim=(110, 90, 66), wrap=(60, 40, 30), band=(60, 40, 30), beard=None, belt=(90, 70, 50), hair=(60, 40, 30), sack=True),
    "son_robe":dict(head=(242, 222, 194), robe=(240, 236, 226), robe_sh=(200, 194, 180), trim=(230, 180, 60), wrap=(60, 40, 30), band=(60, 40, 30), beard=None, belt=(230, 180, 60), hair=(60, 40, 30)),
    "father":  dict(head=(236, 212, 182), robe=(50, 110, 160), robe_sh=(34, 80, 120), trim=(240, 210, 130), wrap=(240, 232, 214), band=(50, 110, 160), beard=(214, 212, 206), belt=(120, 80, 40)),
    "servant": dict(head=(234, 208, 176), robe=(200, 176, 130), robe_sh=(160, 138, 96), trim=(120, 90, 60), wrap=(200, 176, 130), band=(120, 90, 60), beard=None, belt=(110, 80, 50)),
    "ninevite": dict(head=(240, 222, 192), robe=(150, 120, 80), robe_sh=(116, 90, 58), trim=(90, 70, 50), wrap=(150, 120, 80), band=(110, 86, 56), beard=(60, 40, 30), belt=(80, 60, 40), sack=True),
}
_GRAIN = {}
def grain(size):
    if size not in _GRAIN:
        if len(_GRAIN) > 40: _GRAIN.clear()
        r = random.Random(1)
        g = Image.effect_noise(size, 22).filter(ImageFilter.GaussianBlur(1.2))
        _GRAIN[size] = g
    return _GRAIN[size]

def _e(d, cx, cy, rx, ry, fill, w, outline=None):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=outline or OUT, width=w)

def draw(base, cx, foot_y, ppu, who="jonah", view="front", pose="stand", face="calm", t=0.0, flip=False,
         look=(0.0, 0.0), ret=False, phase=0.0, talk=0.0, shadow=True):
    global OUT
    OUT = STYLE["out"]
    c = dict(CHARS[who])
    if STYLE["pastel"]:
        pz = STYLE["pastel"]
        for k_, v_ in list(c.items()):
            if isinstance(v_, tuple) and len(v_) == 3: c[k_] = tuple(int(x + (250 - x) * pz) for x in v_)
    u = ppu * SS
    Wc, Hc = int(3.6 * u), int(3.8 * u)
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ox, fy = Wc / 2, Hc - 0.18 * u
    lw = max(3, int(0.07 * u * STYLE["lw"])); sw = max(3, int(0.075 * u * STYLE["lw"])); thin = max(2, lw // 2)
    walk = pose in ("walk", "run")
    sp = 2.0 if pose == "run" else 1.0
    s = math.sin(phase * 2 * math.pi)
    bob = (abs(math.cos(phase * 2 * math.pi)) * 0.06 * sp if walk else 0.015 * math.sin(t * 2.4)) * u
    if pose == "kneel": bob = -0.28 * u
    if pose == "sit": bob = -0.32 * u
    hip_y = fy - 0.50 * u - bob
    # ground shadow
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([ox - 0.55 * u, fy - 0.08 * u, ox + 0.55 * u, fy + 0.08 * u], fill=(0, 0, 0, 70))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(0.05 * u))); d = ImageDraw.Draw(im)
    # legs + feet
    for side in (-1, 1):
        hx = ox + side * 0.15 * u
        if walk:
            k = (s if side < 0 else -s) * 0.24 * u * sp
            knee = (hx + k * 0.6, hip_y + 0.27 * u); foot = (hx + k, fy - max(0, (s if side < 0 else -s)) * 0.07 * u)
        elif pose == "kneel":
            knee = (hx + side * 0.05 * u, fy - 0.02 * u); foot = (hx - 0.25 * u, fy)
        else:
            knee = (hx, hip_y + 0.26 * u); foot = (hx + side * 0.03 * u, fy)
        d.line([(hx, hip_y), knee, foot], fill=OUT, width=sw, joint="curve")
        fx_ = foot[0] + (0.09 * u if view == "side" else side * 0.04 * u)
        _e(d, fx_, foot[1] - 0.03 * u, 0.13 * u, 0.07 * u, (60, 44, 34), thin)
    # robe body (egg) + cel shade + folds + stitching + belt
    bx = 0.42 * u if view == "front" else 0.34 * u
    by0, by1 = hip_y - 0.92 * u, hip_y + 0.10 * u
    body = [ox - bx, by0, ox + bx, by1]; rad = int(0.34 * u)
    d.rounded_rectangle(body, radius=rad, fill=c["robe"])
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle(body, radius=rad, fill=255)
    cut = Image.new("L", im.size, 0); ImageDraw.Draw(cut).ellipse([ox - bx * 2.3, by0 - 0.4 * u, ox + bx * 0.5, by1 + 0.4 * u], fill=255)
    im.paste(Image.new("RGBA", im.size, c["robe_sh"] + (255,)), (0, 0), ImageChops.subtract(m, cut))
    d = ImageDraw.Draw(im)
    for fxo in (-0.18, 0.12):   # fold lines
        d.line([(ox + fxo * u, by0 + 0.62 * u), (ox + (fxo - 0.03) * u, by1 - 0.06 * u)], fill=c["robe_sh"], width=thin)
    if c.get("armor"):
        for r_ in range(6):
            for k in range(-3, 4):
                xx = ox + k * 0.13 * u + (0.065 * u if r_ % 2 else 0); yy = by0 + (0.20 + r_ * 0.11) * u
                if abs(xx - ox) < bx - 0.08 * u: d.arc([xx - 0.065 * u, yy - 0.05 * u, xx + 0.065 * u, yy + 0.06 * u], 0, 180, fill=c["robe_sh"], width=thin)
    if c.get("sack"):
        for k in range(4):
            d.line([(ox - bx + 0.1 * u, by0 + (0.25 + k * 0.17) * u), (ox + bx - 0.1 * u, by0 + (0.27 + k * 0.17) * u)], fill=c["robe_sh"], width=thin)
    # neckline trim + stitching
    d.arc([ox - 0.22 * u, by0 - 0.10 * u, ox + 0.22 * u, by0 + 0.22 * u], 20, 160, fill=c["trim"], width=max(3, int(0.05 * u)))
    for k in range(7):
        yy = by0 + (0.18 + k * 0.09) * u
        d.line([(ox - 0.015 * u + (0.0 if view == "front" else 0.12 * u), yy), (ox - 0.015 * u + (0.0 if view == "front" else 0.12 * u), yy + 0.045 * u)], fill=c["trim"], width=max(2, thin))
    by = by0 + 0.56 * u
    d.rectangle([ox - bx + lw * 0.6, by, ox + bx - lw * 0.6, by + 0.11 * u], fill=c["belt"])
    d.line([(ox - bx + lw, by), (ox + bx - lw, by)], fill=OUT, width=thin); d.line([(ox - bx + lw, by + 0.11 * u), (ox + bx - lw, by + 0.11 * u)], fill=OUT, width=thin)
    bkx = ox + (0.12 * u if view == "side" else 0)
    d.rounded_rectangle([bkx - 0.08 * u, by - 0.01 * u, bkx + 0.08 * u, by + 0.12 * u], radius=int(0.02 * u), fill=(226, 186, 90), outline=OUT, width=thin)
    d.rounded_rectangle(body, radius=rad, outline=OUT, width=lw)
    # arms (sticks) + mitts
    shy = by0 + 0.24 * u
    for side in (-1, 1):
        sx0 = ox + side * (bx - 0.05 * u)
        if pose == "panic":
            w = math.sin(t * 10 + side * 1.7) * 0.14 * u
            pts = [(sx0, shy), (sx0 + side * 0.34 * u, shy - 0.30 * u), (sx0 + side * 0.30 * u + w, shy - 0.72 * u)]
        elif pose == "pray":
            pts = [(sx0, shy), (sx0 + side * 0.18 * u, shy + 0.20 * u), (ox + side * 0.05 * u, shy - 0.05 * u)]
        elif pose == "point" and side == 1:
            pts = [(sx0, shy), (sx0 + 0.38 * u, shy - 0.06 * u), (sx0 + 0.76 * u, shy - 0.16 * u)]
        elif pose == "throw":
            pts = [(sx0, shy), (sx0 + side * 0.22 * u, shy - 0.36 * u), (sx0 + side * 0.10 * u, shy - 0.74 * u)]
        elif pose == "shake" and side == 1:
            w = math.sin(t * 16) * 0.08 * u
            pts = [(sx0, shy), (sx0 + 0.36 * u, shy + 0.02 * u + w), (sx0 + 0.70 * u, shy - 0.02 * u + w)]
        elif pose == "row":
            w = math.sin(t * 7) * 0.16 * u
            pts = [(sx0, shy), (sx0 + 0.34 * u + w, shy + 0.10 * u), (sx0 + 0.66 * u + w, shy + 0.22 * u)]
        elif pose == "reach":
            pts = [(sx0, shy), (sx0 + 0.34 * u, shy - 0.02 * u + side * 0.05 * u), (sx0 + 0.70 * u, shy - 0.10 * u + side * 0.06 * u)]
        elif pose == "hug":
            pts = [(sx0, shy), (sx0 + side * 0.30 * u, shy + 0.06 * u), (ox + side * 0.10 * u + 0.30 * u, shy + 0.18 * u)]
        elif pose == "sling" and side == 1:
            a_ = t * 14
            pts = [(sx0, shy), (sx0 + 0.16 * u, shy - 0.40 * u), (sx0 + 0.16 * u + math.cos(a_) * 0.30 * u, shy - 0.62 * u + math.sin(a_) * 0.12 * u)]
        elif pose in ("arms_up", "sink"):
            w = math.sin(t * (12 if pose == "sink" else 3) + side) * 0.08 * u
            pts = [(sx0, shy), (sx0 + side * 0.24 * u, shy - 0.36 * u), (sx0 + side * 0.36 * u + w, shy - 0.78 * u)]
        elif pose == "fists":
            pts = [(sx0, shy), (sx0 + side * 0.22 * u, shy + 0.28 * u), (sx0 + side * 0.06 * u, shy + 0.46 * u)]
        elif walk:
            a = (-s if side < 0 else s) * 0.24 * u * sp
            pts = [(sx0, shy), (sx0 + side * 0.12 * u + a * 0.5, shy + 0.30 * u), (sx0 + side * 0.10 * u + a, shy + 0.58 * u)]
        else:
            pts = [(sx0, shy), (sx0 + side * 0.16 * u, shy + 0.30 * u), (sx0 + side * 0.14 * u, shy + 0.60 * u)]
        d.line(pts, fill=OUT, width=sw, joint="curve")
        _e(d, pts[-1][0], pts[-1][1], 0.085 * u, 0.085 * u, (250, 246, 238), thin)
    # head
    hr = 0.56 * u
    hcx = ox + (0.05 * u if view == "side" else 0) + (math.sin(t * 22) * 0.02 * u if face in ("scared", "shocked") else 0)
    hcy = by0 - 0.40 * u
    _e(d, hcx, hcy, hr, hr * 0.96, c["head"], lw)
    hm = Image.new("L", im.size, 0); ImageDraw.Draw(hm).ellipse([hcx - hr, hcy - hr * 0.96, hcx + hr, hcy + hr * 0.96], fill=255)
    hc = Image.new("L", im.size, 0); ImageDraw.Draw(hc).ellipse([hcx - hr * 1.6, hcy - hr * 1.25, hcx + hr * 0.6, hcy + hr * 1.1], fill=255)
    im.paste(Image.new("RGBA", im.size, tuple(int(v * 0.86) for v in c["head"]) + (255,)), (0, 0), ImageChops.subtract(hm, hc))
    d = ImageDraw.Draw(im)
    _e(d, hcx, hcy, hr, hr * 0.96, None, lw)
    d.arc([hcx - hr * 0.80, hcy - hr * 0.82, hcx + hr * 0.10, hcy + hr * 0.20], 200, 245, fill=(255, 252, 244), width=max(3, thin))
    fxo = 0.24 * u if view == "side" else 0.0
    # beard / mustache
    if c["beard"]:
        bc = [hcx - hr * 0.86 + fxo * 0.6, hcy + hr * 0.10, hcx + hr * 0.86 + fxo * 0.6, hcy + hr * 1.12]
        d.chord(bc, 0, 180, fill=c["beard"], outline=OUT, width=thin)
    if c.get("stache"):
        for side in (-1, 1):
            d.ellipse([hcx + fxo + side * 0.13 * u - 0.12 * u, hcy + 0.16 * u, hcx + fxo + side * 0.13 * u + 0.12 * u, hcy + 0.27 * u], fill=(40, 28, 22), outline=OUT, width=thin)
    # eyes
    blink = ((t + hash(who) % 5) % 3.3) < 0.1 and face not in ("sleep", "shocked", "scared")
    eyes = [(-0.20, 0), (0.20, 0)] if view == "front" else [(0.30, 0)]
    big = {"shocked": 1.35, "scared": 1.2}.get(face, 1.0)
    ey = hcy - 0.04 * u
    for ex, _ in eyes:
        x = hcx + ex * u + (fxo * 0.25 if view == "side" else 0)
        rx, ry = 0.135 * u * big, 0.16 * u * big
        if face == "sleep" or blink:
            d.arc([x - rx, ey - ry * 0.3, x + rx, ey + ry * 0.9], 200, 340, fill=OUT, width=max(3, thin + 1))
        else:
            _e(d, x, ey, rx, ry, (255, 255, 255), thin)
            pr = 0.055 * u * (0.7 if face in ("shocked", "scared") else 1.0)
            px = x + look[0] * rx * 0.45 + (0.05 * u if view == "side" else 0); py = ey + look[1] * ry * 0.4 + 0.02 * u
            _e(d, px, py, pr, pr * 1.1, OUT, 1)
            d.ellipse([px - pr * 0.45, py - pr * 0.7, px - pr * 0.05, py - pr * 0.3], fill=(255, 255, 255))
            if face in ("smug", "angry", "tired"):   # heavy upper lid
                d.chord([x - rx * 1.05, ey - ry * 1.05, x + rx * 1.05, ey + ry * 0.2], 180, 360, fill=c["head"], outline=OUT, width=thin)
        # eye-bags
        d.arc([x - rx * 0.8, ey + ry * 0.55, x + rx * 0.8, ey + ry * 1.35], 30, 150, fill=tuple(int(v * 0.7) for v in c["head"]), width=thin)
        # brows
        tilt = {"worried": -0.07, "scared": -0.09, "shocked": -0.05, "angry": 0.09, "smug": 0.03, "stern": 0.06}.get(face, 0.0)
        side = -1 if ex < 0 else 1
        if view == "side": side = 1
        by_ = ey - ry - 0.07 * u - (0.05 * u if face == "shocked" else 0)
        d.line([(x - 0.12 * u, by_ + side * tilt * u), (x + 0.12 * u, by_ - side * tilt * u)], fill=OUT, width=max(3, int(lw * 0.9)))
    # mouth
    mx = hcx + (0.34 * u if view == "side" else 0); my = hcy + (0.36 * u if c["beard"] else 0.30 * u)
    open_ = max(talk, {"shocked": 1.0, "scared": 0.8, "yell": 1.0}.get(face, 0.0))
    if face == "sleep":
        d.arc([mx - 0.05 * u, my - 0.02 * u, mx + 0.05 * u, my + 0.05 * u], 0, 180, fill=OUT, width=thin)
    elif face in ("angry", "yell") or (face == "scared" and who != "jonah"):
        d.rounded_rectangle([mx - 0.15 * u, my - 0.05 * u, mx + 0.15 * u, my + 0.09 * u], radius=int(0.04 * u), fill=(255, 255, 255), outline=OUT, width=thin)
        d.line([(mx - 0.13 * u, my + 0.02 * u), (mx + 0.13 * u, my + 0.02 * u)], fill=OUT, width=thin)
        for k in range(-2, 3):
            d.line([(mx + k * 0.05 * u, my - 0.05 * u), (mx + k * 0.05 * u, my + 0.09 * u)], fill=OUT, width=max(1, thin // 2))
    elif open_ > 0.15:
        _e(d, mx, my + 0.02 * u, 0.07 * u, 0.04 * u + 0.07 * u * open_, (110, 30, 40), thin)
        d.ellipse([mx - 0.04 * u, my + 0.04 * u + 0.03 * u * open_, mx + 0.04 * u, my + 0.08 * u + 0.05 * u * open_], fill=(220, 90, 100))
    elif face in ("smug",):
        d.arc([mx - 0.10 * u, my - 0.08 * u, mx + 0.10 * u, my + 0.06 * u], 10, 120, fill=OUT, width=thin)
    elif face in ("worried", "tired", "stern"):
        d.arc([mx - 0.08 * u, my, mx + 0.08 * u, my + 0.10 * u], 200, 340, fill=OUT, width=thin)
    else:
        d.arc([mx - 0.08 * u, my - 0.06 * u, mx + 0.08 * u, my + 0.04 * u], 20, 160, fill=OUT, width=thin)
    # sweat drop
    if face in ("worried", "scared", "shocked"):
        sxp, syp = hcx + hr * 0.78, hcy - hr * 0.35 + (t * 0.25 % 0.3) * u
        d.polygon([(sxp, syp - 0.11 * u), (sxp - 0.06 * u, syp), (sxp + 0.06 * u, syp)], fill=(150, 210, 255), outline=OUT)
        _e(d, sxp, syp + 0.01 * u, 0.06 * u, 0.06 * u, (150, 210, 255), max(1, thin // 2))
    # headwear
    if c.get("helmet"):
        d.chord([hcx - hr * 1.08, hcy - hr * 1.18, hcx + hr * 1.08, hcy + hr * 0.30], 180, 360, fill=c["wrap"], outline=OUT, width=lw)
        d.rectangle([hcx - hr * 1.02, hcy - hr * 0.50, hcx + hr * 1.02, hcy - hr * 0.40], fill=c["band"], outline=OUT, width=thin)
        d.polygon([(hcx - hr * 0.14, hcy - hr * 1.12), (hcx, hcy - hr * 1.62), (hcx + hr * 0.14, hcy - hr * 1.12)], fill=(190, 50, 40), outline=OUT, width=thin)
        for side in (-1, 1):
            d.polygon([(hcx + side * hr * 1.0, hcy - hr * 0.42), (hcx + side * hr * 1.02, hcy + hr * 0.30), (hcx + side * hr * 0.78, hcy + hr * 0.14)], fill=c["wrap"], outline=OUT, width=thin)
    elif c.get("hair") and not c.get("crown"):
        hcol = c["hair"]
        d.chord([hcx - hr * 1.02, hcy - hr * 1.06, hcx + hr * 1.02, hcy + hr * 0.10], 180, 360, fill=hcol, outline=OUT, width=lw)
        for k in range(-3, 4):
            _e(d, hcx + k * hr * 0.28, hcy - hr * 0.72 - (0.08 * hr if k % 2 else 0), hr * 0.20, hr * 0.18, hcol, thin)
        for side in (-1, 1):   # small curls at the temples, outside the eyes
            _e(d, hcx + side * hr * 0.96, hcy - hr * 0.28, hr * 0.16, hr * 0.22, hcol, thin)
    elif c.get("crown"):
        d.chord([hcx - hr * 1.04, hcy - hr * 1.12, hcx + hr * 1.04, hcy + hr * 0.12], 180, 360, fill=c["wrap"], outline=OUT, width=lw)
        gold = (240, 200, 70); y0c, y1c = hcy - hr * 1.30, hcy - hr * 0.62
        pts = [(hcx - hr * 0.84, y1c)]
        for k in range(5):
            xk = hcx - hr * 0.84 + k * hr * 0.42
            pts += [(xk, y0c + (0.0 if k % 2 == 0 else hr * 0.16)), (xk + hr * 0.21, y1c - hr * 0.30)]
        pts += [(hcx + hr * 0.84, y0c), (hcx + hr * 0.84, y1c)]
        d.polygon(pts, fill=gold, outline=OUT, width=thin)
        for k in (-1, 0, 1): _e(d, hcx + k * hr * 0.42, y1c - hr * 0.16, hr * 0.07, hr * 0.07, (190, 40, 50), max(1, thin // 2))
    elif c.get("hat"):
        d.rounded_rectangle([hcx - hr * 1.15, hcy - hr * 0.72, hcx + hr * 1.15, hcy - hr * 0.52], radius=int(0.04 * u), fill=c["wrap"], outline=OUT, width=thin)
        d.rounded_rectangle([hcx - hr * 0.72, hcy - hr * 1.30, hcx + hr * 0.72, hcy - hr * 0.62], radius=int(0.1 * u), fill=c["wrap"], outline=OUT, width=lw)
        d.rectangle([hcx - hr * 0.70, hcy - hr * 0.82, hcx + hr * 0.70, hcy - hr * 0.70], fill=c["band"])
    else:
        d.chord([hcx - hr * 1.04, hcy - hr * 1.12, hcx + hr * 1.04, hcy + hr * 0.12], 180, 360, fill=c["wrap"], outline=OUT, width=lw)
        d.rectangle([hcx - hr * 0.99, hcy - hr * 0.60, hcx + hr * 0.99, hcy - hr * 0.48], fill=c["band"])
        d.line([(hcx - hr, hcy - hr * 0.60), (hcx + hr, hcy - hr * 0.60)], fill=OUT, width=thin)
        d.line([(hcx - hr, hcy - hr * 0.48), (hcx + hr, hcy - hr * 0.48)], fill=OUT, width=thin)
        if c.get("crown") or c.get("helmet"): pass
        tail = -1 if view == "side" else -1
        d.polygon([(hcx + tail * hr * 0.92, hcy - hr * 0.52), (hcx + tail * hr * 1.42, hcy + hr * 0.42), (hcx + tail * hr * 1.02, hcy + hr * 0.40), (hcx + tail * hr * 0.80, hcy - hr * 0.12)], fill=c["wrap"], outline=OUT, width=thin)
    # paper grain on the drawn pixels
    a = im.split()[3]
    g = grain(im.size) if STYLE["grain"] else Image.new("L", im.size, 128)
    tex = Image.merge("RGBA", [g, g, g, a.point(lambda v: int(v * 0.10))])
    shade = Image.new("RGBA", im.size, (0, 0, 0, 0)); shade.paste(Image.new("RGBA", im.size, (40, 30, 30, 255)), (0, 0), ImageChops.multiply(a, g.point(lambda v: int(max(0, 128 - v) * 0.35))))
    im.alpha_composite(shade)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    small = im.resize((Wc // SS, Hc // SS), Image.LANCZOS)
    foot_off = (Hc - 0.18 * u) / SS
    if ret: return small, foot_off
    x0, y0 = int(cx - small.width / 2), int(foot_y - foot_off)
    base.alpha_composite(small, (x0, y0)) if x0 >= 0 and y0 >= 0 and x0 + small.width <= base.width and y0 + small.height <= base.height else base.paste(small, (x0, y0), small)
    return base

