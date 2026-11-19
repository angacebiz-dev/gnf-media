"""v3 Jonah soundtrack: voice on top (>= ~10 dB over the bed), code-made music by section + timed SFX."""
import sys, os, json
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shots3 import LINES, STARTS, END, TIMES
SR = 24000
n = int(SR * (END + 0.3)); t = np.arange(n) / SR
rng = np.random.default_rng(12)
def lp(x, a):
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x): acc += a * (v - acc); y[i] = acc
    return y
def gate(a, b, fade=0.25): return np.clip((t - a) / fade, 0, 1) * np.clip((b - t) / fade, 0, 1)
def add(buf, x, at, g=1.0):
    i0 = int(at * SR); L = min(len(x), n - i0)
    if L > 0: buf[i0:i0 + L] += x[:L] * g
def note(f, dur, kind="pluck", amp=0.2):
    L = int(dur * SR); tt = np.arange(L) / SR
    if kind == "pluck": env = np.exp(-tt * 9); w = np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(4 * np.pi * f * tt) + 0.15 * np.sin(6 * np.pi * f * tt)
    elif kind == "bass": env = np.exp(-tt * 4); w = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)
    elif kind == "bassoon": env = np.minimum(1, tt * 30) * np.exp(-tt * 2.5); w = np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + 0.5 * np.sin(2 * np.pi * f * tt)
    elif kind == "pad": env = np.minimum(1, tt / 0.6) * np.minimum(1, (dur - tt) / 0.6); w = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.005 * tt)
    else: env = np.exp(-tt * 6); w = np.sin(2 * np.pi * f * tt)
    return w * env * amp
def drum(kind):
    if kind == "kick":
        L = int(0.3 * SR); tt = np.arange(L) / SR; f = 50 + 90 * np.exp(-tt * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10) * 0.6
    if kind == "tom":
        L = int(0.45 * SR); tt = np.arange(L) / SR; f = 80 + 60 * np.exp(-tt * 12)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 6) * 0.5
    L = int(0.06 * SR); return rng.standard_normal(L) * np.exp(-np.linspace(0, 7, L)) * 0.12   # hat
music = np.zeros(n)
def midi(m): return 440 * 2 ** ((m - 69) / 12)
# --- section A (bouncy, D major) 0-14.1 and 52.3-62.8 ---
def bouncy(a, b, bpm=112):
    beat = 60 / bpm; mel = [74, 76, 78, 81, 78, 76, 74, 69, 71, 74, 76, 74, 71, 69, 66, 69]
    bass = [50, 50, 45, 45, 47, 47, 43, 45]
    k = 0; x = a
    while x < b - beat / 2:
        add(music, note(midi(mel[k % 16]), beat * 0.9, "pluck", 0.10), x)
        if k % 2 == 0: add(music, note(midi(bass[(k // 2) % 8] - 12), beat * 1.8, "bass", 0.16), x); add(music, drum("kick"), x, 0.5)
        else: add(music, drum("hat"), x)
        k += 1; x += beat / 2 * 2 if k % 4 else beat / 2 * 2
bouncy(0.0, 14.1); bouncy(52.3, 62.8)
# --- storm (D minor, toms + tremolo) 14.1-41.1 ---
beat = 60 / 120; x = 14.1; k = 0
while x < 41.0:
    add(music, drum("tom"), x, 0.32 if k % 4 == 0 else 0.16)
    if k % 4 == 2: add(music, drum("kick"), x, 0.4)
    x += beat / 2; k += 1
for a, b, ch in [(14.1, 20.0, [50, 53, 57]), (20.0, 28.7, [46, 50, 53]), (28.7, 35.4, [48, 52, 55]), (35.4, 41.1, [45, 49, 52])]:
    for m in ch:
        tt = np.arange(int((b - a) * SR)) / SR
        trem = (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt)) * np.minimum(1, tt / 0.3) * np.minimum(1, (b - a - tt) / 0.3)
        add(music, np.sin(2 * np.pi * midi(m) * tt) * trem * 0.03, a)
# --- calm + underwater pads 41.1-52.3 ---
for a, b, ch in [(41.1, 43.2, [62, 66, 69]), (43.2, 47.5, [50, 57, 60]), (47.5, 52.3, [53, 57, 62])]:
    for m in ch: add(music, note(midi(m), b - a, "pad", 0.05), a)
for k in range(14): add(music, note(midi(84 + (k * 5) % 12), 0.3, "sine", 0.05), 43.4 + k * 0.62)
# --- grumpy ending 62.8-72 ---
beat = 60 / 96; seq = [38, 38, 41, 38, 36, 38, 33, 0]; x = 62.8; k = 0
while x < END - 0.6:
    m = seq[k % 8]
    if m: add(music, note(midi(m), beat * 0.8, "bassoon", 0.10), x)
    if k % 2 == 0: add(music, drum("kick"), x, 0.35)
    x += beat; k += 1
add(music, note(midi(45), 0.5, "bassoon", 0.18), END - 0.75); add(music, note(midi(38), 0.9, "bassoon", 0.2), END - 0.45)  # end sting
# ---------- SFX ----------
sfx = np.zeros(n)
def noise_burst(dur, a_lp, decay, g): L = int(dur * SR); return lp(rng.standard_normal(L), a_lp) * np.exp(-np.linspace(0, decay, L)) * g
for a, b in TIMES[1:]:   # soft whoosh on every cut
    L = int(0.2 * SR); w = lp(rng.standard_normal(L), 0.3) * np.hanning(L) * 0.10; add(sfx, w, a - 0.12)
for tc in (14.58, 31.74, 38.2):
    add(sfx, noise_burst(1.8, 0.012, 4.5, 1.5), tc + 0.08)
rain = lp(rng.standard_normal(n), 0.35) * 0.03 + lp(rng.standard_normal(n), 0.04) * 0.08
storm_g = gate(14.15, 41.1) * (1 - 0.75 * gate(22.0, 28.7, 0.05))
sfx += rain * storm_g
sfx += lp(rng.standard_normal(n), 0.03) * 0.5 * gate(15.5, 16.7)           # wind gust
for tc in (21.0, 21.35, 21.7): add(sfx, noise_burst(0.5, 0.08, 6, 0.6), tc)  # crate splashes
add(sfx, np.sin(2 * np.pi * np.cumsum(np.linspace(900, 200, int(0.35 * SR))) / SR) * np.exp(-np.linspace(0, 3, int(0.35 * SR))) * 0.22, 22.03)  # record scratch-ish
for a in (12.6, 13.3, 22.4, 23.2):   # snores
    L = int(0.55 * SR); tt = np.arange(L) / SR
    add(sfx, lp(rng.standard_normal(L), 0.04) * np.sin(np.pi * tt / 0.55) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * tt)) * 0.5, a)
for tc in (29.3, 29.6, 30.4, 30.6):   # stones clack
    add(sfx, note(1800, 0.06, "sine", 0.12) + noise_burst(0.06, 0.6, 8, 0.15)[:int(0.06 * SR)], tc)
add(sfx, note(midi(38), 0.5, "bass", 0.35), 31.28); add(sfx, note(midi(37), 0.9, "bass", 0.35), 31.75)   # dun-dun
add(sfx, note(2400, 0.4, "sine", 0.10), 9.9)    # coin ting
add(sfx, noise_burst(1.1, 0.12, 4, 1.0), 40.9)   # big splash
for k in range(10): add(sfx, note(600 + k * 70, 0.08, "sine", 0.05), 43.3 + k * 0.4)   # bubbles
gl = np.arange(int(0.5 * SR)) / SR; add(sfx, np.sin(2 * np.pi * (180 - 120 * gl) * gl) * np.exp(-gl * 5) * 0.4, 46.0)   # gulp
add(sfx, noise_burst(0.4, 0.2, 5, 0.5), 54.45)   # sand splat
for a in (63.8, 66.0, 69.6): add(sfx, lp(rng.standard_normal(int(0.9 * SR)), 0.5) * np.hanning(int(0.9 * SR)) * 0.10, a)   # steam hiss
# ---------- voice + mix ----------
vo = np.zeros(n)
for i, s0 in enumerate(STARTS):
    a, sr = sf.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"l{i:02d}.wav")); add(vo, a, s0)
env_v = np.clip(lp(np.abs(vo), 0.003) * 14, 0, 1)
bed = (music * 0.6 + sfx * 0.7) * (1 - 0.7 * env_v)
mix = vo + bed
mix *= np.clip((END + 0.3 - t) / 0.3, 0, 1)
mix = mix / np.max(np.abs(mix)) * 0.9
sf.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mix3_raw.wav"), mix, SR)
sp = env_v > 0.5
print("voice over bed while speaking: %.1f dB" % (20 * np.log10(np.sqrt(np.mean(vo[sp] ** 2)) / np.sqrt(np.mean(bed[sp] ** 2)))))
ss = sp & (storm_g > 0.5)
print("in storm shots: %.1f dB" % (20 * np.log10(np.sqrt(np.mean(vo[ss] ** 2)) / np.sqrt(np.mean(bed[ss] ** 2)))))
