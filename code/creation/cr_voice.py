"""Creation piece narration (Nov 20, 2026): Kokoro, one wav per beat -> cr/audio/bNN.wav + lines.json"""
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
S = json.load(open("/home/claude/gnf/cr/script.json")); D = "/home/claude/gnf/cr/audio"; os.makedirs(D, exist_ok=True)
k = Kokoro("/home/claude/gnf/models/kokoro-v1.0.onnx", "/home/claude/gnf/models/voices-v1.0.bin")
info = []
for b in S["beats"]:
    t = b["say"].replace("“", "").replace("”", "").replace("LORD", "Lord")
    a, sr = k.create(t, voice=S["voice"], speed=S["speed"], lang="en-us")
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 480): nz[-1] + 1600]
    sf.write(f"{D}/{b['id']}.wav", a, sr); info.append((b["id"], round(len(a) / sr, 3)))
json.dump(info, open(f"{D}/lines.json", "w"))
print(len(info), "beats", round(sum(d for _, d in info), 1), "s speech")
