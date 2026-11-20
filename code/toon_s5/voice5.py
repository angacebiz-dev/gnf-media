"""Voice the 5 toon Shorts (Nov 19, 2026): one wav per line -> s5/<id>/audio/lNN.wav + lines.json. python3 s5/voice5.py <id>"""
import sys, json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
S = json.load(open("/home/claude/gnf/s5/scripts.json")); sid = sys.argv[1]; s = S[sid]
D = f"/home/claude/gnf/s5/{sid}/audio"; os.makedirs(D, exist_ok=True)
k = Kokoro("/home/claude/gnf/models/kokoro-v1.0.onnx", "/home/claude/gnf/models/voices-v1.0.bin")
SUBS = [("LORD", "Lord"), ("Baal", "Bay-ul"), ("Philistine", "Phil-ih-steen"), ("Goliath", "Guh-lie-uth")]
info = []
for i, t in enumerate(s["lines"]):
    tt = t
    for a_, b_ in SUBS: tt = tt.replace(a_, b_)
    a, sr = k.create(tt, voice=s["voice"], speed=s["speed"], lang="en-gb" if s["voice"].startswith("b") else "en-us")
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 480): nz[-1] + 1200]
    sf.write(f"{D}/l{i:02d}.wav", a, sr); info.append((t, round(len(a) / sr, 3)))
json.dump(info, open(f"{D}/lines.json", "w"), indent=0)
print(sid, len(info), "lines", round(sum(d for _, d in info), 1), "s speech")
