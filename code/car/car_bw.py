"""B&W 7-slide carousel (hook / 5 verses / cta). Nov 22: optional "pre" line above a verse (myth-buster: the saying people quote). usage: python3 car_bw.py <spec.json> <outdir>"""
import json, sys, os
from car_common import *
spec = json.load(open(sys.argv[1])); od = sys.argv[2]; os.makedirs(od, exist_ok=True)
for i, s in enumerate(spec["slides"], 1):
    c = bg(s["img"], s.get("focus", (0.5, 0.5)), s.get("dim", 0.62), gray=True)
    if s["kind"] == "hook":
        top, bot = block(c, s["text"].upper(), fitfont(c, s["text"].upper(), BLACK, 96, 820, 5), s.get("cy", 900), scrim=0.42)
        tracked(c, s.get("label", "SAVE THIS FOR TONIGHT"), fnt(SANS_B, 30), top - 95, GOLD)
        tracked(c, s.get("swipe", "SWIPE FOR ALL 5"), fnt(SANS_B, 30), bot + 70, (255, 255, 255))
    elif s["kind"] == "verse":
        ftext = fnt(SERIF_I, 84 if len(s["text"]) < 130 else 74)
        top, bot = block(c, s["text"], ftext, 1080 if s.get("pre") else 960)
        tracked(c, s["n"], fnt(SANS_B, 28), top - 245, GOLD)
        block(c, s["ref"], fnt(SANS_B, 88 if len(s["ref"]) <= 15 else 70), top - 130, fill=YELLOW, scrim=0, stroke=6)
        if s.get("pre"): block(c, s["pre"], fnt(SANS_B, 44), top - 400, width=860, fill=(215, 215, 215), scrim=0.3, gap=1.15)
        if s.get("note"): block(c, s["note"], fnt(SANS_B, 46), bot + 120, width=760, fill=GOLD, scrim=0, gap=1.15)
    elif s["kind"] == "cta":
        top, bot = block(c, s["text"].upper(), fitfont(c, s["text"].upper(), BLACK, 92, 820, 5), 820, scrim=0.42)
        t2, b2 = block(c, s.get("sub", "Follow for a verse every day"), fnt(SANS, 50), bot + 110, width=860, scrim=0)
        tracked(c, s.get("label", "SAVE THIS FOR THE NEXT SLEEPLESS NIGHT"), fnt(SANS_B, 26), b2 + 70, GOLD, 4)
    tracked(c, "@GODNOFILTER", fnt(SANS_B, 24), 210, (225, 225, 225), 5)
    fn = f"{od}/{spec['id']}_{i:02d}.png"; c.save(fn, optimize=True); print(fn)
