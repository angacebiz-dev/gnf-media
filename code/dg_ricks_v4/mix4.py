"""mix4 (Nov 22, 2026): ElevenLabs dialogue + code-made epic score + SFX for David & Goliath v4 -> mix.wav (-14 LUFS)"""
import sys, os, math, subprocess, numpy as np, soundfile as sf
from scipy.signal import lfilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots4 import SHOTS, TIMES, STARTS, DUR, END
SR = 44100; n = int(SR * (END + 0.5)); rng = np.random.default_rng(9)
def lp(x, a): return lfilter([a], [1, -(1 - a)], x)
def add(buf, x, at, g=1.0):
    i0 = int(at * SR); L = min(len(x), n - i0)
    if L > 0 and i0 >= 0: buf[i0:i0 + L] += x[:L] * g
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def tone(f, dur, kind, amp):
    L = int(dur * SR); tt = np.arange(L) / SR
    if kind == "pad": env = np.minimum(1, tt / 0.6) * np.clip((dur - tt) / 0.8, 0, 1); w = sum(np.sin(2 * np.pi * f * dd * tt) for dd in (1, 1.004, 0.996)) / 3 + 0.3 * np.sin(4 * np.pi * f * tt); w = lp(w, 0.3)
    elif kind == "brass": env = np.minimum(1, tt * 20) * np.exp(-tt * 2.2); w = lp(sum(np.sin(2 * np.pi * f * k * tt) / k for k in range(1, 8)), 0.35)
    elif kind == "bass": env = np.exp(-tt * 2.5); w = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)
    elif kind == "choir": env = np.minimum(1, tt / 0.3) * np.clip((dur - tt) / 1.0, 0, 1); vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * tt); w = lp(sum(np.sin(2 * np.pi * f * k * vib * tt) * a for k, a in ((1, 1), (2, .5), (3, .3), (4, .15))), 0.2)
    else: env = np.exp(-tt * 6); w = np.sin(2 * np.pi * f * tt)
    return w * env * amp
def drum(kind, g=1.0):
    if kind == "kick": L = int(.4 * SR); tt = np.arange(L) / SR; f = 45 + 80 * np.exp(-tt * 28); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 8) * g
    if kind == "tom": L = int(.5 * SR); tt = np.arange(L) / SR; f = 75 + 50 * np.exp(-tt * 12); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 6) * g
    if kind == "snare": L = int(.25 * SR); return (rng.standard_normal(L) * .3 + np.sin(2 * np.pi * 190 * np.arange(L) / SR) * .2) * np.exp(-np.linspace(0, 9, L)) * g
    L = int(.06 * SR); return rng.standard_normal(L) * np.exp(-np.linspace(0, 7, L)) * .12 * g
def nb(dur, a, decay, g): L = int(dur * SR); return lp(rng.standard_normal(L), a) * np.exp(-np.linspace(0, decay, L)) * g
def sweep(f0, f1, dur, g): L = int(dur * SR); return np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, L)) / SR) * np.exp(-np.linspace(0, 3, L)) * g
mus = np.zeros(n)
T0 = lambda k: TIMES[k][0]
# section A (0 -> shot 24 start): D minor epic pulse, building
ch = [[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 49, 52]]
bpm = 96; beat = 60 / bpm; x = 0.0; k = 0; endA = T0(25) - 0.1
while x < endA:
    inten = min(1, 0.45 + x / endA * 0.6)
    if k % 2 == 0: add(mus, drum("tom", 0.35 * inten), x)
    if k % 8 == 4: add(mus, drum("snare", 0.45 * inten), x)
    if k % 16 == 0:
        c = ch[(k // 16) % 4]
        for m in c: add(mus, tone(midi(m), beat * 8.5, "pad", 0.05), x)
        add(mus, tone(midi(c[0] - 12), beat * 8, "bass", 0.16 * inten), x)
        if inten > 0.6:
            for m in c: add(mus, tone(midi(m + 12), beat * 1.2, "brass", 0.03 * inten), x)
    x += beat / 2; k += 1
# tension: "One stone" -> silence + heartbeat
for j in range(3): add(mus, drum("kick", 0.5), T0(25) + j * 0.42)
# fall hit + triumphant D major
fall_t = TIMES[27][0] + 0.75 * (TIMES[27][1] - TIMES[27][0])
for m in (50, 57, 62, 66, 69): add(mus, tone(midi(m), END - fall_t, "choir", 0.04), fall_t + 0.3)
add(mus, tone(midi(38), END - fall_t, "pad", 0.12), fall_t + 0.2)
x = fall_t + 0.8; k = 0
while x < END - 1.0:
    if k % 2 == 0: add(mus, drum("tom", 0.25), x)
    if k % 8 == 0:
        for m in ((50, 54, 57), (55, 59, 62), (57, 61, 64), (50, 54, 57))[(k // 8) % 4]: add(mus, tone(midi(m + 12), beat * 1.4, "brass", 0.035), x)
    x += beat / 2; k += 1
# ---------- SFX ----------
sfx = np.zeros(n)
for a, b in TIMES[1:]: add(sfx, lp(rng.standard_normal(int(.22 * SR)), .3) * np.hanning(int(.22 * SR)) * .12, a - 0.11)
a, b = TIMES[1]                                                   # giant stomps
st = 0.0
while a + st < b:
    add(sfx, drum("kick", 0.9), a + st); add(sfx, nb(.4, .02, 4, .6), a + st); st += 1 / 1.8
add(sfx, nb(1.6, .01, 2.5, 1.2), TIMES[4][0] + 0.2)                # roar rumble under the shout
add(sfx, sweep(900, 300, .25, .15), TIMES[7][0] + 0.6)            # gulp
add(sfx, tone(1200, .25, "x", .12), TIMES[9][0] + 0.35 * (TIMES[9][1] - TIMES[9][0]))
for k_ in (16, 25):                                               # sling whirr
    a, b = TIMES[k_]; L = int((b - a) * SR); tt = np.arange(L) / SR
    sp = 1.2 if k_ == 16 else 3.2
    add(sfx, lp(rng.standard_normal(L), .2) * (0.5 + 0.5 * np.sin(2 * np.pi * sp * (1 + tt * .8) * tt)) * .12, a)
rel = TIMES[25][0] + 0.86 * (TIMES[25][1] - TIMES[25][0])
add(sfx, sweep(1600, 400, .5, .2), rel)                            # release whiz
add(sfx, sweep(1400, 600, .7, .14), TIMES[26][0])
hit = TIMES[26][0] + 0.86 * (TIMES[26][1] - TIMES[26][0])
add(sfx, tone(2400, .4, "x", .25), hit); add(sfx, drum("snare", .8), hit)   # bonk
add(sfx, drum("kick", 1.3), fall_t); add(sfx, nb(2.2, .008, 3, 2.0), fall_t)                # body hits ground
add(sfx, lp(rng.standard_normal(int(2.5 * SR)), .05) * np.linspace(0, 1, int(2.5 * SR)) ** 2 * np.linspace(1, 0, int(2.5 * SR)) * .25, TIMES[29][0])  # cheer wash
# ---------- voice ----------
vo = np.zeros(n)
for i in range(len(STARTS)):
    v, sr = sf.read(f"/home/claude/gnf/dg3/audio/l{i:02d}.wav"); add(vo, v, STARTS[i])
env = np.clip(lp(np.abs(vo), 0.002) * 10, 0, 1)
bed = mus * 0.55 + sfx * 0.9
mix = vo + bed * (1 - 0.7 * env)
mix *= np.clip((END + 0.4 - np.arange(n) / SR) / 0.6, 0, 1); mix /= np.max(np.abs(mix)) / 0.92
sf.write("/home/claude/gnf/dg4/mix_raw.wav", mix, SR)
sp_ = env > 0.5; print("voice over bed %.1f dB" % (20 * np.log10(np.sqrt(np.mean(vo[sp_] ** 2)) / np.sqrt(np.mean((bed[sp_] * (1 - 0.7 * env[sp_])) ** 2)))))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/home/claude/gnf/dg4/mix_raw.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000", "/home/claude/gnf/dg4/mix.wav"], check=True)
print("MIX OK", END)
