"""Print YouTube chapter lines from <dir>/beats.json (Nov 19, 2026). python3 doc_chapters.py <dir>"""
import json, sys
b = json.load(open(f"{sys.argv[1]}/beats.json")); out, prev = [], None
for x in b:
    if x["sec"] != prev:
        t = 0 if not out else int(max(0, x["t"] - 0.25)); name = x["sec"].split(". ", 1)[-1] if x["sec"][0].isdigit() else x["sec"]
        name = {"Opening": "Intro", "Close": "Subscribe"}.get(name, name); out.append(f"{t // 60}:{t % 60:02d} {name}")
    prev = x["sec"]
print("\n".join(out))
