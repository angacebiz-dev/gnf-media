"""mix5 (Nov 19, 2026): soundtrack for a toon Short. python3 mix5.py <sid> -> s5/<sid>/mix.wav (-15 LUFS), voice >= ~12 dB over the bed.
Music styles (code-made): epic (A), night (B), comic (C), gentle (D), bouncy (E). SFX from shots_<sid>.SFX + a whoosh on cuts."""
import sys, os, subprocess
import numpy as np, soundfile as sf
SID = sys.argv[1]; sys.argv = ["engine5.py", SID]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine5 as E
SR = 24000; END = E.END; n = int(SR * (END + 0.3)); t = np.arange(n) / SR
rng = np.random.default_rng(7)
def lp(x, a):
    from scipy.signal import lfilter
    return lfilter([a], [1, -(1 - a)], x)
def add(buf, x, at, g=1.0):
    i0 = int(at * SR); L = min(len(x), n - i0)
    if L > 0 and i0 >= 0: buf[i0:i0 + L] += x[:L] * g
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def note(f, dur, kind="pluck", amp=0.2):
    L = int(dur * SR); tt = np.arange(L) / SR
    if kind == "pluck": env = np.exp(-tt * 9); w = np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(4 * np.pi * f * tt) + 0.15 * np.sin(6 * np.pi * f * tt)
    elif kind == "bass": env = np.exp(-tt * 4); w = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)
    elif kind == "brass": env = np.minimum(1, tt * 25) * np.exp(-tt * 3); w = sum(np.sin(2 * np.pi * f * k * tt) / k for k in range(1, 7))
    elif kind == "pad": env = np.minimum(1, tt / 0.8) * np.minimum(1, (dur - tt) / 0.8); w = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.004 * tt) + 0.25 * np.sin(4 * np.pi * f * tt)
    elif kind == "piano": env = np.exp(-tt * 3.2) * np.minimum(1, tt * 200); w = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 2) + 0.1 * np.sin(6 * np.pi * f * tt)
    elif kind == "harp": env = np.exp(-tt * 4) * np.minimum(1, tt * 300); w = np.sin(2 * np.pi * f * tt) + 0.2 * np.sin(4 * np.pi * f * tt)
    else: env = np.exp(-tt * 6); w = np.sin(2 * np.pi * f * tt)
    return w * env * amp
def drum(kind):
    if kind == "kick":
        L = int(0.3 * SR); tt = np.arange(L) / SR; f = 50 + 90 * np.exp(-tt * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10) * 0.6
    if kind == "tom":
        L = int(0.45 * SR); tt = np.arange(L) / SR; f = 80 + 60 * np.exp(-tt * 12); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 6) * 0.5
    if kind == "snare":
        L = int(0.2 * SR); return (rng.standard_normal(L) * 0.25 + np.sin(2 * np.pi * 190 * np.arange(L) / SR) * 0.2) * np.exp(-np.linspace(0, 9, L))
    L = int(0.06 * SR); return rng.standard_normal(L) * np.exp(-np.linspace(0, 7, L)) * 0.12
music = np.zeros(n)
def loop(bpm, fn):
    beat = 60 / bpm; k = 0; x = 0.25
    while x < END - 0.3: fn(k, x, beat); x += beat / 2; k += 1
kind = E.SH.MUSIC
if kind == "epic":      # A: D minor, toms + brass stabs + string pad, building
    ch = [[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 49, 52]]
    def f(k, x, b):
        if k % 2 == 0: add(music, drum("tom"), x, 0.35 if k % 8 == 0 else 0.18)
        if k % 8 == 4: add(music, drum("snare"), x, 0.5)
        if k % 16 == 0:
            for m in ch[(k // 16) % 4]: add(music, note(midi(m), b * 8, "pad", 0.05), x); add(music, note(midi(m + 12), b * 0.9, "brass", 0.035), x)
            add(music, note(midi(ch[(k // 16) % 4][0] - 12), b * 8, "bass", 0.14), x)
    loop(104, f)
elif kind == "night":   # B: low drone + sparse minor piano
    for m in (38, 45, 50): music += np.sin(2 * np.pi * midi(m) * t) * 0.025 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.1 * t))
    mel = [62, 65, 69, 67, 65, 62, 60, 62, 57, 60, 62, 65]
    def f(k, x, b):
        if k % 3 == 0: add(music, note(midi(mel[(k // 3) % 12]), 2.0, "piano", 0.07), x)
        if k % 12 == 0: add(music, note(midi(38), 3.0, "bass", 0.10), x)
    loop(70, f)
elif kind == "comic":   # C: fast drums + brass hits, major
    prog = [55, 60, 62, 60]
    def f(k, x, b):
        add(music, drum("kick" if k % 4 == 0 else "hat"), x, 0.45 if k % 4 == 0 else 1.0)
        if k % 4 == 2: add(music, drum("snare"), x, 0.45)
        if k % 8 == 0: add(music, note(midi(prog[(k // 8) % 4]), b * 0.8, "brass", 0.05), x); add(music, note(midi(prog[(k // 8) % 4] + 4), b * 0.8, "brass", 0.035), x); add(music, note(midi(prog[(k // 8) % 4] - 24), b * 3.5, "bass", 0.14), x)
        if k % 2 == 1: add(music, note(midi(prog[(k // 8) % 4] + 12 + (k % 3) * 2), b * 0.4, "pluck", 0.04), x)
    loop(132, f)
elif kind == "gentle":  # D: harp arpeggios + warm pad, C major
    ch = [[48, 55, 60, 64, 67], [45, 52, 57, 60, 64], [41, 48, 53, 57, 60], [43, 50, 55, 59, 62]]
    def f(k, x, b):
        c = ch[(k // 16) % 4]
        add(music, note(midi(c[1 + k % 4] + 12), 1.4, "harp", 0.05), x)
        if k % 16 == 0:
            for m in c[:3]: add(music, note(midi(m), b * 8, "pad", 0.04), x)
    loop(80, f)
else:                   # E: bouncy pluck + bass, G major
    mel = [67, 71, 74, 71, 72, 76, 74, 71, 69, 72, 71, 67, 66, 69, 67, 0]
    bass = [43, 43, 48, 48, 50, 50, 43, 43]
    def f(k, x, b):
        m = mel[k % 16]
        if m: add(music, note(midi(m), b * 0.45, "pluck", 0.07), x)
        if k % 2 == 0: add(music, note(midi(bass[(k // 2) % 8] - 12), b * 0.9, "bass", 0.13), x); add(music, drum("kick"), x, 0.3)
        else: add(music, drum("hat"), x, 0.8)
    loop(116, f)
add(music, np.zeros(1), 0)
# ---------- SFX
sfx = np.zeros(n)
def nb(dur, a, decay, g): L = int(dur * SR); return lp(rng.standard_normal(L), a) * np.exp(-np.linspace(0, decay, L)) * g
def sweep(f0, f1, dur, g):
    L = int(dur * SR); return np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, L)) / SR) * np.exp(-np.linspace(0, 3, L)) * g
def mx(*a):
    L = max(len(x) for x in a); o = np.zeros(L)
    for x in a: o[:len(x)] += x
    return o
SFXF = {
 "boom": lambda: mx(drum("kick") * 0.9, nb(1.2, 0.01, 4, 1.2)),
 "roar": lambda: lp(rng.standard_normal(int(1.3 * SR)), 0.04) * np.sin(np.linspace(0, np.pi, int(1.3 * SR))) * (0.7 + 0.3 * np.sin(2 * np.pi * 34 * np.arange(int(1.3 * SR)) / SR)) * 1.4,
 "panic": lambda: np.concatenate([note(midi(m), 0.09, "pluck", 0.07) for m in (79, 83, 79, 83, 79, 83)]),
 "ting": lambda: note(2600, 0.6, "sine", 0.12),
 "whoosh": lambda: lp(rng.standard_normal(int(0.35 * SR)), 0.25) * np.hanning(int(0.35 * SR)) * 0.25,
 "clack": lambda: note(1800, 0.06, "sine", 0.12),
 "swing": lambda: lp(rng.standard_normal(int(0.6 * SR)), 0.3) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * np.arange(int(0.6 * SR)) / SR)) * 0.15,
 "whiz": lambda: sweep(1400, 500, 0.4, 0.12),
 "thud": lambda: drum("tom") * 0.9,
 "bigthud": lambda: mx(drum("kick") * 1.0, nb(0.9, 0.02, 4, 1.0)),
 "choir": lambda: sum(note(midi(m), 2.4, "pad", 0.05) for m in (62, 66, 69, 74)),
 "stone": lambda: nb(0.9, 0.03, 3, 0.9),
 "crickets": lambda: np.concatenate([note(4200, 0.05, "sine", 0.05) for _ in range(6)] + [np.zeros(int(0.2 * SR))]),
 "splash": lambda: nb(1.0, 0.15, 4, 0.8),
 "rumble": lambda: lp(rng.standard_normal(int(1.6 * SR)), 0.006) * np.sin(np.linspace(0, np.pi, int(1.6 * SR))) * 3.0,
 "fire": lambda: mx(lp(rng.standard_normal(int(1.8 * SR)), 0.2) * np.exp(-np.linspace(0, 2, int(1.8 * SR))) * 0.6, nb(1.0, 0.01, 3, 1.4)),
 "wind": lambda: lp(rng.standard_normal(int(2.5 * SR)), 0.02) * np.sin(np.linspace(0, np.pi, int(2.5 * SR))) * 0.9,
 "party": lambda: np.concatenate([note(midi(m), 0.12, "pluck", 0.08) for m in (72, 76, 79, 84)]),
 "oink": lambda: sweep(500, 300, 0.25, 0.18),
}
for li, fr, k in E.SH.SFX: add(sfx, SFXF[k](), E.STARTS[li] + fr * E.DUR[li] - 0.03)
CUTS = [float(x) for x in os.environ["CUTS"].split(",")] if os.environ.get("CUTS") else [s["t0"] for s in E.SHOTS[1:]]
OUTN = os.environ.get("MIXOUT", "mix")
for c in CUTS:
    w = lp(rng.standard_normal(int(0.18 * SR)), 0.3) * np.hanning(int(0.18 * SR)) * (0.10 if kind in ("comic", "epic", "bouncy") else 0.04); add(sfx, w, c - 0.1)
if any(f[0] == "rain" for s in E.SHOTS for f in s.get("fx", [])):
    rg = np.zeros(n)
    for s in E.SHOTS:
        if any(f[0] == "rain" for f in s.get("fx", [])): rg[int(s["t0"] * SR):int(s["t1"] * SR)] = 1
    sfx += lp(rng.standard_normal(n), 0.3) * 0.03 * lp(rg, 0.001)
# ---------- voice + mix
vo = np.zeros(n)
for i, s0 in enumerate(E.STARTS):
    a, sr = sf.read(f"{E.D}/audio/l{i:02d}.wav"); add(vo, a, s0)
env_v = np.clip(lp(np.abs(vo), 0.003) * 14, 0, 1)
bed = (music * 0.85 + sfx * 0.75) * (1 - 0.72 * env_v)
mix = vo + bed; mix *= np.clip((END + 0.3 - t) / 0.5, 0, 1); mix /= np.max(np.abs(mix)) / 0.9
sf.write(f"{E.D}/mix_raw.wav", mix, SR)
sp = env_v > 0.5
print("%s voice over bed while speaking: %.1f dB" % (SID, 20 * np.log10(np.sqrt(np.mean(vo[sp] ** 2)) / np.sqrt(np.mean(bed[sp] ** 2) + 1e-12))))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{E.D}/mix_raw.wav", "-af", "loudnorm=I=-15:TP=-1.5:LRA=9", "-ar", "48000", f"{E.D}/{OUTN}.wav"], check=True)
print("MIX OK", E.D + "/mix.wav", round(END, 2), "s")
