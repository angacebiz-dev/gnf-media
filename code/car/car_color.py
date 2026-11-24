"""COLOUR 4-slide carousel (hook / silence / verse+note / cta). usage: python3 car_color.py <spec.json> <outdir>"""
import json, sys, os
from car_common import *
spec = json.load(open(sys.argv[1])); od = sys.argv[2]; os.makedirs(od, exist_ok=True)
for i, s in enumerate(spec["slides"], 1):
    c = bg(s["img"], s.get("focus", (0.5, 0.5)), s.get("dim", 0.6))
    if s["kind"] == "hook":
        t = s["text"].upper(); top, bot = block(c, t, fitfont(c, t, BLACK, 100, 880, 5), s.get("cy", 900), width=880, scrim=0.4)
        tracked(c, "SWIPE  >>", fnt(SANS_B, 30), bot + 80, (255, 255, 255))
    elif s["kind"] == "silence":
        top, bot = block(c, "Read this in silence.", fnt(SERIF_I, 112), 900, scrim=0.35)
        tracked(c, "TAKE A BREATH FIRST", fnt(SANS_B, 28), bot + 70, GOLD, 5)
    elif s["kind"] == "verse":
        ft = fitfont(c, s["text"], SERIF_I, 84, 840, 7); top, bot = block(c, s["text"], ft, 900, width=840, scrim=0.45)
        block(c, s["ref"], fnt(SANS_B, 84 if len(s["ref"]) <= 15 else 70), top - 120, fill=YELLOW, scrim=0, stroke=6)
        block(c, s["note"], fnt(SANS_B, 46), bot + 150, width=760, fill=(255, 255, 255), scrim=0.35, gap=1.18)
    elif s["kind"] == "cta":
        t = s["text"].upper(); top, bot = block(c, t, fitfont(c, t, BLACK, 88, 880, 5), 800, width=880, scrim=0.42)
        t2, b2 = block(c, s["amen"], fnt(SANS_B, 52), bot + 150, width=760, fill=YELLOW, scrim=0.3, stroke=3)
        block(c, "Follow for a verse every day", fnt(SANS, 42), b2 + 110, scrim=0)
    tracked(c, "@GODNOFILTER", fnt(SANS_B, 24), 210, (235, 235, 235), 5)
    fn = f"{od}/{spec['id']}_{i:02d}.png"; c.save(fn, optimize=True); print(fn)
