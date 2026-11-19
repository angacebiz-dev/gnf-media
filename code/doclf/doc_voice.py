"""Generic documentary long-form voice (Nov 19, 2026; from rs_voice.py): python3 doc_voice.py <dir> -> <dir>/voice.wav + beats.json.
Kokoro am_michael, one script line = one beat. Lines "@key fx,fy [ring=x,y]" set the image for the following beats."""
import re, json, sys, numpy as np, soundfile as sf, subprocess
DIR = sys.argv[1]
from kokoro_onnx import Kokoro
src = open(f"{DIR}/script.md", encoding="utf-8").read().split("## Opening", 1)[1]
src = "## Opening" + src
VOICE, SPEED, GAP, SEC_GAP = "am_michael", 0.95, 0.5, 1.3
beats, sec, IMG = [], None, None
for l in src.splitlines():
    l = l.strip()
    if l.startswith("## "): sec = re.sub(r"\s*\[.*?\]", "", l[3:]).split(" — ")[0].strip(); continue
    if l.startswith("@"):
        p = l[1:].split(); fx, fy = (float(v) for v in p[1].split(",")) if len(p) > 1 else (0.5, 0.5)
        ring = [float(v) for v in p[2][5:].split(",")] if len(p) > 2 and p[2].startswith("ring=") else None
        IMG = dict(key=p[0], focus=[fx, fy], ring=ring, new=True); continue
    if not l or l.startswith("#") or l.startswith("**") or l == "---": continue
    m = re.match(r'^"(.*)" — (.+)$', l)
    if m: beats.append(dict(sec=sec, raw=m.group(1), ref=m.group(2).strip(), kind="verse"))
    else: beats.append(dict(sec=sec, raw=l, ref=None, kind="line"))
    beats[-1]["img"] = dict(IMG); IMG["new"] = False; IMG["ring"] = None
SUBS = [("Nineveh", "Nin-uh-vuh"), ("Ninevites", "Nin-uh-vites"), ("Tarshish", "Tar-shish"), ("Amittai", "Uh-mit-eye"), ("Gath-hepher", "Gath hee-fer"), ("Sheol", "Shee-ole"), ("Nahum", "Nay-um"), ("120,000", "one hundred twenty thousand"), ("Jeroboam", "Jair-uh-boe-um"), ("Ezekiel", "Ee-zeek-ee-ul"), ("Uz", "Ooz"), ("Eliphaz", "El-ih-faz"), ("Bildad", "Bil-dad"), ("Zophar", "Zoe-far"), ("Elihu", "Ee-lie-hew"), ("Behemoth", "Beh-hee-moth"), ("Leviathan", "Luh-vie-uh-thun"), ("cubits", "cue-bits"), ("gopher", "go-fer"), ("Ararat", "Air-uh-rat"), ("Methuselah", "Meth-oo-zuh-luh"), ("Lamech", "Lay-mek"), ("Shem", "Shem"), ("Japheth", "Jay-feth"), ("Yam Suph", "Yahm Soof"), ("Pi-hahiroth", "Pie ha-hee-roth"), ("Weiqing", "Way-ching"), ("600", "six hundred"), ("2010", "twenty ten"), ("Horeb", "Hor-eb"), ("Visoki Dečani", "Visoki Dechani"), ("Scrovegni", "Skrovaynee"), ("Aert", "Art"), ("1974", "nineteen seventy-four"), ("1305", "thirteen oh five"), ("LORD", "Lord"), ("RaptureTok", "Rapture Tock"), ("1840s", "eighteen forties"), ("1843", "eighteen forty-three"), ("1844", "eighteen forty-four"), ("2011", "twenty eleven"), ("2025", "twenty twenty-five"), ("22nd", "twenty-second"), ("21st", "twenty-first"), ("23rd", "twenty-third"), ("24th", "twenty-fourth"), ("Nuremberg", "Nyurumberg"), ("Glaser", "Glahzer"), ("1561", "fifteen sixty-one"), ("1535", "fifteen thirty-five"), ("14th", "fourteenth"), ("UFO ", "U F O "), ("Giotto", "Jotto"), ("1301", "thirteen oh one"), ("1986", "nineteen eighty-six"), ("Shechem", "Sheh-kem"), ("Dothan", "Doe-thun"), ("Potiphar", "Pot-ih-far"), ("Gilead", "Gil-ee-ad"),
        ("Reuben", "Roo-ben"), ("Jezebel", "Jez-uh-bel"), ("Baal", "Bay-ul"), ("Elah", "Ee-lah"), ("Eliab", "Ee-lie-ab"), ("ephah", "ee-fah"),
        ("Pharaoh", "Fair-oh"), ("Midian", "Mid-ee-an"), ("Horeb", "Hor-eb"), ("Jethro", "Jeth-roe"), ("Lazarus", "Laz-uh-rus"),
        ("Bethany", "Beth-uh-nee"), ("Naomi", "Nay-oh-mee"), ("Orpah", "Or-pah"), ("Moab", "Moe-ab"), ("Obed", "Oh-bed"),
        ("Ishmaelites", "Ish-may-uh-lites"), ("cupbearer", "cup-bearer"),
        ("UFOs", "U F Os"), ("1486", "fourteen eighty-six"), ("1400s", "fourteen hundreds"), ("1710", "seventeen ten"), ("1350", "thirteen fifty"), ("Kebar", "Kee-bar"), ("Blumrich", "Bloom-rick"), ("Saturn V", "Saturn Five"), ("2,600", "twenty-six hundred"), ("1970s", "nineteen seventies"), ("Josef", "Yo-sef")]
def spoken(t):
    for a, b in SUBS: t = t.replace(a, b)
    t = t.replace(" — ", ", ").replace("—", ", ").replace("...", ".")
    t = t.replace("‘", "").replace("…", "."); t = re.sub(r"’(?=\s|$|[.,!?;:])", "", t)
    t = re.sub(r"[\"“”]", "", t); t = re.sub(r"(^|\s)'", r"\1", t); t = re.sub(r"([.,?!])'", r"\1", t)
    return t
k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
out, t, prev = [], 0.0, None
for b in beats:
    if prev is not None:
        g = SEC_GAP if b["sec"] != prev else GAP
        if b["kind"] == "verse": g += 0.25
        out.append(np.zeros(int(24000 * g), np.float32)); t += g
    a, sr = k.create(spoken(b["raw"]), voice=VOICE, speed=SPEED, lang="en-us"); a = a.astype(np.float32)
    nz = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, nz[0] - 720): nz[-1] + 1920] if len(nz) else a
    b["t"], b["end"] = round(t, 3), round(t + len(a) / sr, 3)
    out.append(a); t += len(a) / sr; prev = b["sec"]
    if b["kind"] == "verse": out.append(np.zeros(int(24000 * 0.35), np.float32)); t += 0.35
    print(f"{len(out):4d} {b['t']:7.2f} {b['sec'][:14]:14} {b['raw'][:60]}", flush=True)
out.append(np.zeros(int(24000 * 1.5), np.float32))
sf.write(f"{DIR}/voice_raw.wav", np.concatenate(out), 24000)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{DIR}/voice_raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-ar", "44100", f"{DIR}/voice.wav"], check=True)
for b in beats: b["text"] = b.pop("raw")
json.dump(beats, open(f"{DIR}/beats.json", "w"), ensure_ascii=False, indent=1)
print("VOICE OK", round(t, 1), "s", len(beats), "beats")
