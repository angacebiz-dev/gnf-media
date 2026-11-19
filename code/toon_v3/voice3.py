import soundfile as sf, json
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/gnf/models/kokoro-v1.0.onnx", "/home/claude/gnf/models/voices-v1.0.bin")
L = [
 "God gave Jonah one job.",
 "Go to Nineveh,", "and preach against it.",
 "So Jonah got up...", "and ran the exact opposite way.",
 "He found a ship headed for Tarshish,", "paid the fare,",
 "went down into the bottom of the boat...", "and fell fast asleep.",
 "Then the Lord hurled a great wind onto the sea.",
 "The sailors panicked.", "Every man cried out to his own god.",
 "They threw the cargo overboard.",
 "And Jonah?", "Still asleep.",
 "The captain shook him awake.",
 "How can you sleep?", "Get up and call upon your God!",
 "They cast lots to find out who was to blame...", "and the lot fell on Jonah.",
 "Pick me up, he said,", "and throw me into the sea.",
 "The sailors rowed as hard as they could.", "But the sea only got worse.",
 "So they threw him overboard...", "and the sea went perfectly calm.",
 "But God wasn't finished.", "He had a great fish waiting.",
 "Three days and three nights inside a fish.", "And right there, Jonah prayed.",
 "Then the Lord commanded the fish...", "and it threw Jonah up onto dry land.",
 "Second chance.", "Go to Nineveh.", "This time, Jonah went.",
 "And the whole city turned from its evil ways.", "So God spared them.",
 "And Jonah?", "He was furious.",
 "Because that's why he ran in the first place.",
 "He knew God was gracious and compassionate,", "and he didn't want God to spare Nineveh.",
]
info = []
for i, t in enumerate(L):
    a, sr = k.create(t, voice="am_michael", speed=1.12, lang="en-us")
    import numpy as np
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 480): nz[-1] + 1200]
    sf.write(f"l{i:02d}.wav", a, sr); info.append((t, round(len(a) / sr, 3)))
json.dump(info, open("lines.json", "w"), indent=0)
print(len(L), "lines", round(sum(d for _, d in info), 1), "s speech")
