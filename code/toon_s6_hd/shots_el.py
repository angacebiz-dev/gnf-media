"""Elijah on Mount Carmel - look C: comic book. Black ink outlines, halftone dots, yellow caption boxes, burst words, speed lines, fastest cuts."""
STYLE = dict(toon=dict(out=(24, 16, 14), lw=1.3, grain=True, pastel=0.0), char="hd", post="warm", cap="pop", capmax=12, capy=0.70, gap=0.12, vig=0.35, tail=0.9)
PAUSE = {7: 0.25, 10: 0.2, 18: 0.3, 22: 0.25}
def C(w, x, y=0.82, s=0.12, **k): return dict(w=w, x=x, y=y, s=s, **k)
def CU(c, z0, z1, at=0.40, dx=0.0):
    hy = c["y"] - 2.05 * c["s"] * 1080 / 1920
    return (z0, z1, (c["x"] + dx, hy + (0.5 - at) / z0), (c["x"] + dx, hy + (0.5 - at) / z1))
def crowd(n, x0, x1, y, s, **k): return [C("baalp", x0 + (x1 - x0) * i / max(1, n - 1), y + (i % 2) * 0.012, s, dt=i * 0.37, **k) for i in range(n)]
EL = lambda **k: C("elijah", 0.5, 0.86, 0.17, **k)
AL, AR = dict(k="altar", x=0.28, y=0.84, s=0.06), dict(k="altar", x=0.72, y=0.84, s=0.06)
SHOTS = [
 dict(l=0, bg="carmel", cam=(1.25, 1.35, (0.5, 0.66), (0.5, 0.67)), punch=True, chars=crowd(7, 0.1, 0.9, 0.80, 0.085, f="smug")),
 dict(l=0, f=0.6, bg="burst", cam=CU(EL(), 1.6, 1.75), punch=True, chars=[EL(f="stern")], fx=[("speed",)]),
 dict(l=1, bg="carmel", cam=CU(EL(), 1.5, 1.6), chars=[EL(p="point", f="smug", talk=True)]),
 dict(l=2, bg="carmel", cam=(1.4, 1.5, (0.5, 0.71), (0.5, 0.72)), props=[AL, AR], fx=[("word", "NO FIRE?", 0.5, 0.3, 54)]),
 dict(l=3, bg="burst", cam=CU(EL(), 1.6, 1.8), punch=True, chars=[EL(p="arms_up", f="yell", talk=True)], fx=[("speed",)]),
 dict(l=4, bg="carmel", cam=(1.5, 1.6, (0.32, 0.74), (0.3, 0.75)), props=[AL], chars=crowd(4, 0.12, 0.48, 0.86, 0.07, f="smug")),
 dict(l=5, bg="carmel", cam=(1.6, 1.7, (0.3, 0.75), (0.34, 0.75)), shake=0.8, props=[AL], chars=crowd(4, 0.12, 0.48, 0.86, 0.07, f="yell", p="arms_up", hop=3.0), fx=[("word", "!!!", 0.75, 0.25, 50)]),
 dict(l=6, bg="burst", cam=CU(C("baalp", 0.5, 0.86, 0.17), 1.7, 1.9), punch=True, shake=0.6, chars=[C("baalp", 0.5, 0.86, 0.17, p="arms_up", f="yell", talk=True)], fx=[("speed",)]),
 dict(l=7, bg="carmel", cam=(1.6, 1.7, (0.3, 0.75), (0.3, 0.75)), props=[AL], chars=crowd(3, 0.16, 0.44, 0.86, 0.07, f="worried"), fx=[("word", "...", 0.5, 0.3, 50)]),
 dict(l=8, bg="carmel", cam=CU(EL(), 1.6, 1.75), chars=[EL(f="smug", look=(-0.6, 0))]),
 dict(l=9, bg="burst", cam=CU(EL(), 1.7, 1.9), punch=True, chars=[EL(p="point", f="smug", talk=True, flip=True)], fx=[("word", "ZZZ?", 0.72, 0.22, 48)]),
 dict(l=10, bg="carmel", cam=CU(C("baalp", 0.5, 0.86, 0.15), 1.6, 1.7), chars=[C("baalp", 0.5, 0.86, 0.15, f="tired")]),
 dict(l=11, bg="carmel", cam=(1.6, 1.75, (0.66, 0.75), (0.7, 0.75)), props=[AR], chars=[C("elijah", 0.55, 0.86, 0.11, p="kneel", f="calm", look=(0.8, 0.2))]),
 dict(l=12, bg="carmel", cam=(2.6, 2.8, (0.72, 0.8), (0.72, 0.8)), punch=True, props=[AR], fx=[("word", "12", 0.75, 0.25, 60)]),
 dict(l=13, bg="burst", cam=CU(EL(), 1.8, 2.0), punch=True, chars=[EL(f="smug")], fx=[("speed",)]),
 dict(l=14, bg="carmel", cam=(2.0, 2.1, (0.72, 0.76), (0.72, 0.76)), props=[dict(AR, wet=1.0, wetgrow=True)], fx=[("splash", 0.72, 0.8), ("word", "SPLASH!", 0.5, 0.3, 50)]),
 dict(l=15, bg="carmel", cam=(2.4, 2.6, (0.72, 0.8), (0.72, 0.8)), props=[dict(AR, wet=1.0)]),
 dict(l=16, bg="crowd", cam=CU(C("elijah", 0.5, 0.86, 0.15), 1.5, 1.6), chars=[C("elijah", 0.5, 0.86, 0.15, p="kneel", f="calm", look=(0, -0.6))]),
 dict(l=17, bg="sky_fire", cam=CU(EL(), 1.6, 1.85), shake=0.3, chars=[EL(p="arms_up", f="yell", talk=True, look=(0, -0.8))]),
 dict(l=18, bg="carmel_dark", cam=(1.6, 1.7, (0.72, 0.7), (0.72, 0.7)), shake=1.5, props=[dict(AR, wet=1.0, fire=1.0)], fx=[("firefall", 0.72, 0.78), ("flash", 0.4), ("word", "FWOOSH!", 0.4, 0.22, 56)]),
 dict(l=19, bg="carmel_dark", cam=(2.0, 2.2, (0.72, 0.74), (0.72, 0.72)), shake=0.6, props=[dict(AR, fire=1.6)], fx=[("sparks",)]),
 dict(l=20, bg="carmel_dark", cam=(2.4, 2.6, (0.72, 0.8), (0.72, 0.8)), props=[dict(AR, fire=1.0)], fx=[("sparks",)]),
 dict(l=21, bg="crowd", cam=(1.25, 1.35, (0.5, 0.74), (0.5, 0.75)), chars=[C("israelite", 0.2 + i * 0.15, 0.9, 0.1, p="kneel", f="shocked", dt=i * 0.3) for i in range(5)]),
 dict(l=22, bg="burst", cam=CU(C("israelite", 0.5, 0.86, 0.16), 1.6, 1.8), punch=True, chars=[C("israelite", 0.5, 0.86, 0.16, p="arms_up", f="yell", talk=True)], fx=[("speed",), ("sparks",)]),
 dict(l=23, bg="carmel", cam=CU(C("baalp", 0.5, 0.86, 0.15), 1.6, 1.7), chars=[C("baalp", 0.5, 0.86, 0.15, f="shocked")]),
 dict(l=24, bg="carmel", cam=CU(EL(), 1.5, 1.65), chars=[EL(f="calm", p="arms_up")], fx=[("rays", 0.5, 0.1, (255, 240, 170))]),
 dict(l=25, bg="burst", cam=CU(EL(), 1.9, 2.1), chars=[EL(f="calm", look=(0, 0.1), p="point")]),
]
SFX = [(0, 0.0, "boom"), (0, 0.6, "whoosh"), (3, 0.0, "boom"), (5, 0.0, "panic"), (6, 0.0, "boom"), (7, 0.0, "crickets"), (9, 0.0, "whoosh"), (12, 0.0, "clack"), (14, 0.0, "splash"), (17, 0.0, "rumble"), (18, 0.0, "fire"), (18, 0.0, "bigthud"), (22, 0.0, "choir")]
MUSIC = "epic"
