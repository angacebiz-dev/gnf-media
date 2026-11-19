"""Documentary thumbnail maker (1280x720 JPG) - God No Filter, Nov 16 2026.

Look: public-domain painting full-bleed + dark gradient + yellow ring on the object
+ 2-4 giant Montserrat 900 words (one gold word) + optional small yellow kicker.
Usage: python3 doc_thumb.py spec.json   (renders with headless Chrome via playwright)

spec.json = [
  {"out": "thumb_A.jpg", "img": "ufo/decani_detail.png", "crop": [0, 0, 636, 398],
   "pad_left": 120,                      # optional: reflect-pad on the left to push the object right
   "shade": "left" | "top" | "bottom",   # where the dark gradient + text sit
   "ring": [858, 372, 150, 190],         # cx, cy, rx, ry in the 1280x720 frame (optional)
   "lines": ["WHO'S", "*INSIDE?"],       # a leading * = gold line; "*" inside a line: "EZEKIEL SAW *WHAT?"
   "size": 132, "kicker": "CHURCH FRESCO · c.1350"}
]
Used for the UFO doc: A = Decani fresco "WHO'S INSIDE?", B = Merian Ezekiel "EZEKIEL SAW WHAT?"
(crop 0,190,1045,778 sepia - keeps the figure of God out), C = Nuremberg 1561 "A WHOLE CITY / SAW IT".
Rules: a count on a thumbnail must be exact; question, never a claim; never pair "UFO"/"alien"
wording with God, angels, the Holy Spirit or the star; YouTube limit 2 MB.
"""
import asyncio, html, json, os, sys
import numpy as np
from PIL import Image, ImageFilter

GNF = os.path.dirname(os.path.abspath(__file__))
FONT = f"{GNF}/fonts/fontsource-montserrat-5.3.0/package/files"


def background(s, path):
    im = Image.open(os.path.join(GNF, s["img"])).convert("RGB").crop(tuple(s["crop"]))
    a = np.array(im)
    pl = s.get("pad_left", 0)
    if pl:
        h = a.shape[0]; w = a.shape[1] + pl
        th = round(w * 9 / 16); pv = max(0, th - h)
        a = np.pad(a, ((pv // 2, pv - pv // 2), (pl, 0), (0, 0)), mode="reflect")
    out = Image.fromarray(a).resize((1280, 720), Image.LANCZOS).filter(
        ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if s.get("sepia"):  # warm tint for grey engravings
        g = out.convert("L")
        out = Image.merge("RGB", [g.point(lambda v: min(255, v + 12)), g.point(lambda v: int(v * .88 + 6)), g.point(lambda v: int(v * .68))])
    out.save(path, quality=95)


def page(s, bg):
    shade = s.get("shade", "left")
    grad = {"left": "linear-gradient(90deg,rgba(14,11,16,.95) 0%,rgba(14,11,16,.8) 32%,rgba(14,11,16,0) 54%)",
            "top": "linear-gradient(180deg,rgba(14,11,16,.94) 0%,rgba(14,11,16,.8) 24%,rgba(14,11,16,0) 46%)",
            "bottom": "linear-gradient(0deg,rgba(14,11,16,.96) 0%,rgba(14,11,16,.9) 34%,rgba(14,11,16,0) 58%)"}[shade]
    def fmt(line):
        if line.startswith("*"):
            return f'<span class=g>{html.escape(line[1:])}</span>'
        if "*" in line:
            a, b = line.split("*", 1)
            return f'{html.escape(a)}<span class=g>{html.escape(b)}</span>'
        return html.escape(line)
    body = "<br>".join(fmt(l) for l in s["lines"])
    size = s.get("size", 120)
    n = len(s["lines"]); block = size * 0.92 * n
    if shade == "left":
        pos = f"left:52px;top:{int(360 - block / 2 - 20)}px"; kpos = f"left:58px;top:{int(360 + block / 2 + 10)}px"
    elif shade == "top":
        pos = "left:0;width:1280px;text-align:center;top:34px"; kpos = f"left:0;width:1280px;text-align:center;top:{int(44 + block)}px"
    else:
        pos = f"left:0;width:1280px;text-align:center;top:{int(690 - block)}px"; kpos = f"left:0;width:1280px;text-align:center;top:{int(640 - block)}px"
    ring = ""
    if s.get("ring"):
        cx, cy, rx, ry = s["ring"]
        e = f'cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none"'
        ring = (f'<svg width="1280" height="720" style="position:absolute;left:0;top:0">'
                f'<ellipse {e} stroke="rgba(0,0,0,0.55)" stroke-width="22"/><ellipse {e} stroke="#FAE846" stroke-width="11"/></svg>')
    kick = f'<div class=k style="{kpos}">{html.escape(s["kicker"])}</div>' if s.get("kicker") else ""
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:M;font-weight:900;src:url(file://{FONT}/montserrat-latin-900-normal.woff2)}}
@font-face{{font-family:M;font-weight:800;src:url(file://{FONT}/montserrat-latin-800-normal.woff2)}}
body{{margin:0}} .t{{width:1280px;height:720px;position:relative;overflow:hidden;font-family:M,sans-serif;background:#0E0B10 url({bg}) center/cover}}
.big{{position:absolute;font-weight:900;color:#fff;line-height:.92;letter-spacing:1px;font-size:{size}px;text-shadow:0 6px 24px rgba(0,0,0,.85),0 0 4px rgba(0,0,0,.9)}}
.g{{color:#FAE846}} .k{{position:absolute;font-weight:800;font-size:30px;letter-spacing:6px;color:#FAE846;text-shadow:0 2px 10px rgba(0,0,0,.9)}}
</style></head><body><div class=t><div style="position:absolute;inset:0;background:{grad}"></div>{ring}
<div class=big style="{pos}">{body}</div>{kick}</div></body></html>"""


async def main(specs):
    from playwright.async_api import async_playwright
    os.makedirs("/tmp/doc_thumb", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        for i, s in enumerate(specs):
            bg = f"/tmp/doc_thumb/bg{i}.jpg"; background(s, bg)
            hp = f"/tmp/doc_thumb/t{i}.html"; open(hp, "w").write(page(s, bg))
            await pg.goto("file://" + hp); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"/tmp/doc_thumb/t{i}.png")
            Image.open(f"/tmp/doc_thumb/t{i}.png").convert("RGB").save(s["out"], quality=90)
            print(s["out"], os.path.getsize(s["out"]))
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(json.load(open(sys.argv[1]))))
