import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
W, H, CX = 1080, 1920, 515
F = "fonts/fontsource-cormorant-garamond-5.3.0/package/files/"
M = "fonts/fontsource-montserrat-5.3.0/package/files/"
SERIF_B, SERIF_I = F + "cormorant-garamond-latin-700-normal.woff", F + "cormorant-garamond-latin-600-italic.woff"
SANS, SANS_B = M + "montserrat-latin-600-normal.woff", M + "montserrat-latin-700-normal.woff"
BLACK = M + "montserrat-latin-900-normal.woff"
GOLD, YELLOW = (238, 206, 140), (250, 232, 70)
fnt = lambda p, s: ImageFont.truetype(p, s)
def bg(path, focus, dim, gray=False):
    im = Image.open(path).convert("RGB")
    if gray: im = ImageOps.grayscale(im).convert("RGB"); im = ImageEnhance.Contrast(im).enhance(1.15)
    else: im = ImageEnhance.Color(im).enhance(1.08); im = ImageEnhance.Contrast(im).enhance(1.05)
    sc = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * sc) + 1, round(im.height * sc) + 1), Image.LANCZOS)
    fx, fy = focus
    x0 = min(max(0, int(fx * im.width - W / 2)), im.width - W); y0 = min(max(0, int(fy * im.height - H / 2)), im.height - H)
    im = im.crop((x0, y0, x0 + W, y0 + H)); im = ImageEnhance.Brightness(im).enhance(dim)
    v = Image.new("L", (W, H), 0); d = ImageDraw.Draw(v)
    d.ellipse((-W * 0.35, -H * 0.2, W * 1.35, H * 1.2), fill=255); v = v.filter(ImageFilter.GaussianBlur(220))
    black = Image.new("RGB", (W, H), (4, 5, 12))
    return Image.composite(im, black, v.point(lambda p: int(110 + p * 145 / 255)))
def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width or not cur: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]
def block(canvas, text, f, cy, width=820, fill=(255, 255, 255), gap=1.1, scrim=0.38, stroke=0):
    d = ImageDraw.Draw(canvas); lines = wrap(d, text, f, width)
    asc, desc = f.getmetrics(); lh = int((asc + desc) * gap); h = lh * len(lines); top = int(cy - h / 2)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    bw = max(d.textlength(l, font=f) for l in lines)
    if scrim:
        s = Image.new("L", (W, H), 0)
        ImageDraw.Draw(s).rounded_rectangle((CX - bw / 2 - 70, top - 50, CX + bw / 2 + 70, top + h + 40), 50, fill=int(255 * scrim))
        s = s.filter(ImageFilter.GaussianBlur(50)); canvas.paste(Image.new("RGB", (W, H), (6, 7, 16)), (0, 0), s)
    for i, l in enumerate(lines):
        lw = d.textlength(l, font=f); ld.text((CX - lw / 2, top + i * lh), l, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(10, 10, 10, 255))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(layer.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.8)))
    out = Image.alpha_composite(sh, layer); canvas.paste(out, (0, 0), out)
    return top, top + h
def tracked(canvas, text, f, cy, fill, sp=6):
    d = ImageDraw.Draw(canvas)
    w = sum(d.textlength(c, font=f) for c in text) + sp * (len(text) - 1); x = CX - w / 2
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for c in text: ld.text((x, cy), c, font=f, fill=fill + (255,)); x += d.textlength(c, font=f) + sp
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(layer.split()[3].filter(ImageFilter.GaussianBlur(6)))
    out = Image.alpha_composite(sh, layer); canvas.paste(out, (0, 0), out)
def fitfont(canvas, text, path, size, width, maxlines):
    d = ImageDraw.Draw(canvas)
    while size > 40 and len(wrap(d, text, fnt(path, size), width)) > maxlines: size -= 4
    return fnt(path, size)
