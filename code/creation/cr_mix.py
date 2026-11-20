"""Creation score + mix (Nov 20, 2026): code-made cinematic score, voice on top, -14 LUFS."""
import sys, subprocess, numpy as np, soundfile as sf
sys.argv = ["cr_render.py", "plan"]; import cr_render as C
from scipy.signal import lfilter
SR = 24000; END = C.END; n = int(SR * (END + 0.5)); t = np.arange(n) / SR
rng = np.random.default_rng(3)
def lp(x, a): return lfilter([a], [1, -(1 - a)], x)
def add(buf, x, at, g=1.0):
    i0 = int(at * SR); L = min(len(x), n - i0)
    if L > 0 and i0 >= 0: buf[i0:i0 + L] += x[:L] * g
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def pad(f, dur, amp, att=1.5, rel=2.0):
    L = int(dur * SR); tt = np.arange(L) / SR
    env = np.minimum(1, tt / att) * np.clip((dur - tt) / rel, 0, 1)
    w = sum(np.sin(2 * np.pi * f * d * tt + p) for d, p in ((1, 0), (1.003, 1), (0.997, 2))) / 3
    w += 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt)
    return lp(w * env, 0.25) * amp
def choir(f, dur, amp, att=0.6):
    L = int(dur * SR); tt = np.arange(L) / SR; vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * tt)
    env = np.minimum(1, tt / att) * np.clip((dur - tt) / 1.5, 0, 1)
    w = sum(np.sin(2 * np.pi * f * k * vib * tt) * a for k, a in ((1, 1), (2, 0.5), (3, 0.3), (4, 0.15), (5, 0.08)))
    return lp(w * env, 0.18) * amp
def harp(f, amp):
    L = int(2.2 * SR); tt = np.arange(L) / SR; return (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 2.6) * np.minimum(1, tt * 400) * amp
def boom(amp):
    L = int(3.5 * SR); tt = np.arange(L) / SR; f = 38 + 50 * np.exp(-tt * 9)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.6) + lp(rng.standard_normal(L), 0.01) * np.exp(-tt * 2.5) * 1.5) * amp
def timp(amp):
    L = int(1.6 * SR); tt = np.arange(L) / SR; f = 73 + 12 * np.exp(-tt * 20)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3) + lp(rng.standard_normal(L), 0.05) * np.exp(-tt * 18) * 0.4) * amp
def riser(dur, amp):
    L = int(dur * SR); tt = np.arange(L) / SR; x = rng.standard_normal(L); out = np.zeros(L)
    for i in range(0, L, 2400):
        a = 0.01 + 0.25 * (i / L) ** 2; out[i:i + 2400] = lp(x[i:i + 2400], a)
    return out * (tt / dur) ** 2 * amp
def shimmer(dur, amp):
    out = np.zeros(int(dur * SR))
    for k in range(int(dur * 6)):
        m = rng.choice([86, 90, 93, 98, 102]); s = harp(midi(m), 0.6)[: len(out) - int(k / 6 * SR)]; out[int(k / 6 * SR): int(k / 6 * SR) + len(s)] += s
    return out * amp * np.minimum(1, np.arange(len(out)) / SR / 0.5)
mus = np.zeros(n)
S0 = {s[0]: s[1] for s in C.SEG}; S0.update({s[3]: s[1] for s in C.SEG if s[3] in ("m1", "m2")})
LT = C.LIGHT_T
# hook: glory chord
for m in (50, 57, 62, 66, 69): add(mus, choir(midi(m), 2.2, 0.05), 0.0)
add(mus, boom(0.5), 0.02)
# darkness: low drone + rumble until the light
d0, d1 = S0["b00"], LT
for m in (38, 45): add(mus, pad(midi(m), d1 - d0 + 1.5, 0.11, att=3, rel=1.0), d0)
add(mus, lp(rng.standard_normal(int((d1 - d0) * SR)), 0.004) * 1.6 * np.minimum(1, np.arange(int((d1 - d0) * SR)) / SR / 3), d0)
for k, m in enumerate((62, 65, 60, 62, 57)): add(mus, harp(midi(m), 0.05), d0 + 2.5 + k * 3.2)
add(mus, riser(LT - S0["m1"] + 0.6, 0.55), S0["m1"] - 0.6)
# LET THERE BE LIGHT
add(mus, boom(0.9), LT - 0.02); add(mus, timp(0.6), LT)
for m in (50, 57, 62, 66, 69, 74, 78): add(mus, choir(midi(m), 6.0, 0.045, att=0.08), LT)
add(mus, shimmer(6.0, 0.6), LT)
# days: warm progression D A Bm G, building
prog = [(50, 54, 57), (45, 49, 52), (47, 50, 54), (43, 47, 50)]
a0, a1 = LT + 4.0, S0["b17"]
x = a0; k = 0
while x < a1 - 0.5:
    dur = min(4.0, a1 - x + 1.0); ch = prog[k % 4]; inten = min(1, 0.45 + (x - a0) / (S0["b15"] - a0 + 0.01) * 0.55) if x < S0["b16"] else 0.4
    for m in ch: add(mus, pad(midi(m), dur + 1.2, 0.05 * inten, att=1.2, rel=1.4), x)
    add(mus, pad(midi(ch[0] - 12), dur + 1.0, 0.09 * inten), x)
    for j in range(8): add(mus, harp(midi(ch[j % 3] + 24 + (12 if j % 4 == 3 else 0)), 0.03 * inten), x + j * 0.5)
    if x < S0["b16"] and k % 2 == 0: add(mus, timp(0.35 * inten), x)
    x += 4.0; k += 1
for b in ("b06", "b07", "b09", "b11", "b12"): add(mus, timp(0.4), S0[b] + 0.25)
add(mus, boom(0.45), S0["b15"] + 0.2)
for m in (50, 57, 62, 66, 69): add(mus, choir(midi(m), 5.0, 0.035), S0["b15"] + 0.2)
# darkness again (b17), riser into dawn (m2), resolution at b19
for m in (38, 45, 53): add(mus, pad(midi(m), S0["b19"] - S0["b17"] + 1.0, 0.07, att=1.5, rel=1.0), S0["b17"])
add(mus, riser(S0["b19"] - S0["m2"] + 0.4, 0.5), S0["m2"] - 0.4)
add(mus, boom(0.75), S0["b19"]); add(mus, timp(0.5), S0["b19"])
for m in (50, 57, 62, 66, 69, 74): add(mus, choir(midi(m), END - S0["b19"] + 0.4, 0.04, att=0.4), S0["b19"])
for m in (38, 50): add(mus, pad(midi(m), END - S0["b19"] + 0.4, 0.09, att=0.5, rel=2.5), S0["b19"])
add(mus, shimmer(END - S0["b19"] - 1.0, 0.45), S0["b19"])
# voice
vo = np.zeros(n)
for b in C.S["beats"]:
    a, sr = sf.read(f"{C.R}/audio/{b['id']}.wav"); add(vo, a, C.T[b["id"]][0])
env = np.clip(lp(np.abs(vo), 0.003) * 12, 0, 1)
bed = mus * (1 - 0.55 * env)
mix = vo * 1.0 + bed * 0.36; mix *= np.clip((END + 0.4 - t) / 0.8, 0, 1); mix /= np.max(np.abs(mix)) / 0.9
sf.write(f"{C.R}/mix_raw.wav", mix, SR)
sp = env > 0.5; print("voice over bed: %.1f dB" % (20 * np.log10(np.sqrt(np.mean(vo[sp] ** 2)) / np.sqrt(np.mean((bed[sp] * 0.36) ** 2)))))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{C.R}/mix_raw.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", f"{C.R}/mix.wav"], check=True)
print("MIX OK", round(END, 2))
