"""Noah long-form diagrams (Nov 19, 2026): na/p/d_dims.jpg, d_decks.jpg, d_count.jpg. All numbers = estimates on an 18-inch cubit (labelled)."""
from PIL import Image, ImageDraw, ImageFont
FD = "fonts/fontsource-montserrat-5.3.0/package/files/montserrat-latin-{}-normal.woff"
def F(w, s): return ImageFont.truetype(FD.format(w), s)
W, H = 2400, 1350; BG = (18, 20, 28); GOLD = (240, 200, 110); YEL = (250, 232, 70); WH = (240, 236, 226); GR = (120, 125, 140); WOOD = (120, 82, 48)
def base(title, sub):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(26, 29, 40))
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(26, 29, 40))
    d.text((120, 90), title, font=F(900, 92), fill=WH); d.text((124, 200), sub, font=F(700, 42), fill=YEL); return im, d
def ctext(d, x, y, s, f, fill): w = d.textlength(s, font=f); d.text((x - w / 2, y), s, font=f, fill=fill)
def person(d, x, yb, h):
    r = h * 0.09; d.ellipse([x - r, yb - h, x + r, yb - h + 2 * r], fill=WH); d.line([(x, yb - h + 2 * r), (x, yb - h * 0.42)], fill=WH, width=4)
    d.line([(x, yb - h * 0.42), (x - h * 0.13, yb)], fill=WH, width=4); d.line([(x, yb - h * 0.42), (x + h * 0.13, yb)], fill=WH, width=4)
    d.line([(x - h * 0.15, yb - h * 0.68), (x + h * 0.15, yb - h * 0.68)], fill=WH, width=4)
# 1. dimensions + football field
im, d = base("300 × 50 × 30 CUBITS", "GENESIS 6:15  ·  1 CUBIT = ABOUT 18 INCHES (ESTIMATE)")
s = 3.6; x0 = 220; yb = 760; L, Hh = 450 * s, 45 * s
d.rectangle([x0, yb - Hh, x0 + L, yb], fill=WOOD, outline=GOLD, width=5)
for k in (1, 2): d.line([(x0, yb - Hh * k / 3), (x0 + L, yb - Hh * k / 3)], fill=(90, 60, 34), width=3)
d.polygon([(x0 - 10, yb - Hh), (x0 + L / 2, yb - Hh - 40), (x0 + L + 10, yb - Hh)], fill=(95, 64, 38), outline=GOLD)
d.rectangle([x0 + L * 0.45, yb - Hh * 0.62, x0 + L * 0.5, yb - Hh * 0.08], fill=(60, 40, 24), outline=GOLD, width=3)
d.line([(x0, yb + 50), (x0 + L, yb + 50)], fill=YEL, width=4); d.line([(x0, yb + 35), (x0, yb + 65)], fill=YEL, width=4); d.line([(x0 + L, yb + 35), (x0 + L, yb + 65)], fill=YEL, width=4)
ctext(d, x0 + L / 2, yb + 70, "ABOUT 450 FEET LONG", F(900, 64), YEL)
d.line([(x0 + L + 50, yb - Hh), (x0 + L + 50, yb)], fill=YEL, width=4); d.text((x0 + L + 75, yb - Hh / 2 - 50), "ABOUT 45 FT", font=F(900, 52), fill=YEL); d.text((x0 + L + 75, yb - Hh / 2 + 10), "(4 STORIES)", font=F(700, 34), fill=WH)
person(d, x0 + L * 0.47 + 70, yb, 6 * s)
d.text((x0 + L * 0.47 + 100, yb - 50), "6-FT PERSON", font=F(700, 30), fill=WH)
fy = 1080; fL = 360 * s
d.rectangle([x0, fy, x0 + fL, fy + 120], fill=(40, 110, 60), outline=WH, width=4)
for k in range(1, 12): xx = x0 + 30 * s + (300 * s) * k / 12; d.line([(xx, fy), (xx, fy + 120)], fill=(200, 230, 200), width=2)
d.rectangle([x0, fy, x0 + 30 * s, fy + 120], fill=(30, 85, 48)); d.rectangle([x0 + fL - 30 * s, fy, x0 + fL, fy + 120], fill=(30, 85, 48))
d.text((x0 + fL + 40, fy + 6), "FOOTBALL FIELD,", font=F(800, 40), fill=WH)
d.text((x0 + fL + 40, fy + 54), "END ZONES INCLUDED: 360 FT", font=F(800, 40), fill=WH)
d.text((x0, fy + 140), "THE ARK IS ABOUT 90 FT LONGER (ESTIMATE)", font=F(800, 44), fill=YEL)
im.save("na/p/d_dims.jpg", quality=92)
# 2. three decks
im, d = base("LOWER, MIDDLE, UPPER DECKS", "GENESIS 6:16  ·  A ROOF, A DOOR IN THE SIDE, THREE DECKS")
x0, yb, L, Hh = 260, 1170, 1880, 660
d.polygon([(x0 - 20, yb - Hh), (x0 + L / 2, yb - Hh - 110), (x0 + L + 20, yb - Hh)], fill=(95, 64, 38), outline=GOLD)
d.rectangle([x0, yb - Hh, x0 + L, yb], fill=(60, 42, 26), outline=GOLD, width=6)
d.rectangle([x0, yb - Hh, x0 + L, yb - Hh + 46], fill=(30, 26, 22)); d.text((x0 + L - 690, yb - Hh + 4), "WINDOW GAP · 1 CUBIT FROM THE TOP", font=F(700, 30), fill=YEL)
names = ["UPPER DECK", "MIDDLE DECK", "LOWER DECK"]; dh = (Hh - 46) / 3
for k in range(3):
    y = yb - Hh + 46 + dh * k
    d.line([(x0, y), (x0 + L, y)], fill=GOLD, width=4)
    for c in range(1, 12): d.line([(x0 + L * c / 12, y + 20), (x0 + L * c / 12, y + dh - 6)], fill=(85, 60, 38), width=3)
    ctext(d, x0 + L / 2, y + dh / 2 - 34, names[k], F(900, 58), WH)
d.rectangle([x0 + 230, yb - dh * 2 + 10, x0 + 330, yb - dh - 20], fill=(25, 18, 12), outline=YEL, width=5)
d.text((x0 + 200, yb - dh * 2 - 50), "DOOR", font=F(900, 40), fill=YEL)
d.text((x0, yb + 40), "ROOMS (GENESIS 6:14) · LAYOUT INSIDE NOT DESCRIBED — THIS DRAWING IS ONE GUESS", font=F(700, 34), fill=GR)
d.text((x0, 300), "ALL 3 DECKS: ABOUT 101,000 SQ FT OF FLOOR (ESTIMATE)", font=F(900, 46), fill=YEL)
im.save("na/p/d_decks.jpg", quality=92)
# 3. animal estimates
im, d = base("HOW MANY ANIMALS?", "THE BIBLE GIVES NO HEADCOUNT  ·  THESE ARE MODERN ESTIMATES")
x0, y0, bw = 240, 420, 1800
rows = [(16000, "UP TO ABOUT 16,000", "JOHN WOODMORAPPE, NOAH'S ARK: A FEASIBILITY STUDY (1996) · A GENEROUS MAXIMUM"),
        (7000, "ABOUT 7,000", "ARK ENCOUNTER RESEARCHERS · ABOUT 1,400 KINDS OF LAND ANIMALS AND BIRDS")]
for k, (n, big, src) in enumerate(rows):
    y = y0 + k * 300; w = bw * n / 16000
    d.rectangle([x0, y, x0 + w, y + 120], fill=(GOLD if k == 0 else YEL)); d.text((x0 + 30, y + 22), big, font=F(900, 66), fill=BG)
    d.text((x0, y + 140), src, font=F(700, 34), fill=WH)
d.text((x0, 1080), "\"KIND\" (GENESIS 6:20) IS NOT \"SPECIES\": ONE DOG KIND, NOT EVERY BREED", font=F(800, 44), fill=WH)
d.text((x0, 1150), "MOST LAND ANIMALS ARE SMALL  ·  SKEPTICS DISPUTE THESE ASSUMPTIONS", font=F(800, 40), fill=GR)
im.save("na/p/d_count.jpg", quality=92)
print("DIAGRAMS OK")
