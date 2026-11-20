"""Peter walks on water - look D: storybook watercolour on paper, pastel toons with soft edges, gentle slow camera, serif captions, female narrator."""
STYLE = dict(toon=dict(out=(24, 16, 14), lw=1.3, grain=True, pastel=0.0), char="hd", post="warm", cap="pop", capmax=12, capy=0.70, gap=0.12, vig=0.35, tail=0.9)
PAUSE = {0: 0.3, 9: 0.5, 14: 0.3, 16: 0.3, 19: 0.4}
def C(w, x, y=0.62, s=0.12, **k): return dict(w=w, x=x, y=y, s=s, **k)
def CU(c, z0, z1, at=0.40, dx=0.0):
    hy = c["y"] - 2.05 * c["s"] * 1080 / 1920
    return (z0, z1, (c["x"] + dx, hy + (0.5 - at) / z0), (c["x"] + dx, hy + (0.5 - at) / z1))
WAT = 0.62
BOAT = lambda x=0.5, s=0.09: dict(k="boat", x=x, y=WAT + 0.04, s=s, z=99999)
JESUS = lambda **k: C("jesus", k.pop("x", 0.5), k.pop("y", WAT), k.pop("s", 0.13), **k)
PETER = lambda **k: C("peter", k.pop("x", 0.5), k.pop("y", WAT), k.pop("s", 0.13), **k)
GL = lambda x=0.5, y=0.5, r=0.25: ("glow", x, y, r, (255, 246, 214), 110)
SHOTS = [
 dict(l=0, bg="sea_night", cam=(1.1, 1.25, (0.5, 0.5), (0.5, 0.55)), props=[BOAT(0.5, 0.07)], chars=[C("disciple", 0.47, WAT + 0.02, 0.045, p="row"), C("peter", 0.54, WAT + 0.02, 0.045, f="calm")]),
 dict(l=0, f=0.6, bg="deck", cam=CU(PETER(y=0.66, s=0.16), 1.6, 1.75), chars=[PETER(y=0.66, s=0.16, p="sink", f="scared")], fx=[("wavefront", 0.64)]),
 dict(l=1, bg="sea_night", cam=(1.55, 1.75, (0.5, 0.56), (0.5, 0.58)), props=[BOAT(0.5, 0.06)], chars=[C("disciple", 0.48, WAT + 0.02, 0.035, p="row")], fx=[GL(0.7, 0.15, 0.12)]),
 dict(l=2, bg="deck", cam=(1.6, 1.75, (0.5, 0.56), (0.5, 0.57)), shake=0.3, props=[BOAT(0.5, 0.16)], chars=[C("disciple", 0.38, WAT + 0.0, 0.08, p="row", f="worried"), C("peter", 0.5, WAT - 0.005, 0.08, p="row", f="tired", dt=0.4), C("disciple", 0.63, WAT + 0.0, 0.08, p="row", f="worried", dt=0.8)], fx=[("rain",)]),
 dict(l=3, bg="sea_night", cam=(1.5, 1.7, (0.56, 0.54), (0.56, 0.55)), chars=[JESUS(x=0.6, s=0.09, p="walk", ph=0.5, v="side", flip=True, mx=-0.05, alpha=0.85)], fx=[GL(0.62, 0.56, 0.08)]),
 dict(l=4, bg="deck", cam=(1.8, 1.95, (0.5, 0.5), (0.5, 0.5)), shake=0.6, props=[BOAT(0.5, 0.16)], chars=[C("disciple", 0.4, WAT, 0.09, p="panic", f="scared"), C("peter", 0.58, WAT - 0.005, 0.09, p="panic", f="shocked", dt=0.3)]),
 dict(l=5, bg="sea_night", cam=CU(JESUS(), 1.5, 1.65), chars=[JESUS(f="calm")], fx=[GL(0.5, 0.48, 0.2)]),
 dict(l=6, bg="sea_night", cam=CU(JESUS(), 1.8, 2.0), chars=[JESUS(f="calm", talk=True, p="reach")], fx=[GL(0.5, 0.46, 0.22), ("rays", 0.5, 0.42, (255, 240, 210))]),
 dict(l=7, bg="deck", cam=(1.8, 1.95, (0.5, 0.5), (0.5, 0.5)), props=[BOAT(0.5, 0.16)], chars=[C("peter", 0.37, WAT - 0.005, 0.10, p="reach", f="worried", talk=True)]),
 dict(l=8, bg="sea_night", cam=CU(JESUS(), 1.4, 1.5), chars=[JESUS(f="calm")], fx=[GL(0.5, 0.48, 0.2)]),
 dict(l=9, bg="sea_night", cam=CU(JESUS(), 2.1, 2.3), chars=[JESUS(f="calm", talk=True, p="reach")], fx=[GL(0.5, 0.45, 0.25), ("rays", 0.5, 0.4, (255, 240, 210))]),
 dict(l=10, bg="deck", cam=(1.5, 1.6, (0.5, 0.52), (0.55, 0.52)), props=[BOAT(0.42, 0.14)], chars=[C("peter", 0.5, WAT - 0.01, 0.09, p="walk", ph=0.8, mx=0.14, v="side", f="worried")]),
 dict(l=11, bg="sea_night", cam=(1.35, 1.5, (0.45, 0.55), (0.55, 0.55)), chars=[PETER(x=0.3, s=0.08, p="walk", ph=0.9, mx=0.18, v="side", f="calm"), JESUS(x=0.74, s=0.08, f="calm", p="reach", flip=True)], fx=[GL(0.74, 0.55, 0.1), ("dust",)]),
 dict(l=12, bg="sea_night", cam=CU(PETER(), 1.6, 1.75), shake=0.6, chars=[PETER(f="scared", look=(-0.8, 0))], fx=[("rain",)]),
 dict(l=13, bg="sea_night", cam=CU(PETER(), 1.5, 1.6), shake=0.4, chars=[PETER(f="scared", p="sink", sink=0.35)], fx=[("wavefront", 0.60), ("rain",)]),
 dict(l=14, bg="deck", cam=CU(PETER(y=0.66, s=0.17), 1.8, 2.0), shake=0.5, chars=[PETER(y=0.66, s=0.17, p="sink", f="yell", talk=True)], fx=[("wavefront", 0.62), ("rain",)]),
 dict(l=15, bg="sea_night", cam=(1.6, 1.7, (0.5, 0.52), (0.5, 0.52)), chars=[PETER(x=0.42, s=0.12, p="sink", f="scared", y=0.64), JESUS(x=0.6, s=0.12, p="reach", f="calm", flip=True)], fx=[GL(0.55, 0.5, 0.25), ("wavefront", 0.635)]),
 dict(l=16, bg="sea_night", cam=CU(JESUS(), 1.8, 2.0), chars=[JESUS(f="calm", p="reach")], fx=[GL(0.5, 0.45, 0.25)]),
 dict(l=17, bg="deck", cam=(1.4, 1.5, (0.5, 0.52), (0.5, 0.52)), props=[BOAT(0.32, 0.13)], chars=[C("disciple", 0.26, WAT - 0.0, 0.07, f="shocked"), C("disciple", 0.38, WAT, 0.07, f="worried", dt=0.4), PETER(x=0.66, s=0.08, f="calm"), JESUS(x=0.78, s=0.08, f="calm")]),
 dict(l=18, bg="sea_calm", cam=(1.4, 1.5, (0.5, 0.54), (0.5, 0.54)), chars=[PETER(x=0.42, s=0.11, f="calm"), JESUS(x=0.6, s=0.11, f="calm", p="hug", flip=True)], fx=[GL(0.5, 0.5, 0.3)]),
 dict(l=19, bg="sea_calm", cam=(1.45, 1.65, (0.5, 0.57), (0.5, 0.59)), props=[BOAT(0.5, 0.06)], fx=[GL(0.6, 0.3, 0.2)]),
 dict(l=20, bg="sea_calm", cam=CU(JESUS(), 1.8, 2.05), chars=[JESUS(f="calm", p="reach", look=(0, 0.1))], fx=[GL(0.5, 0.45, 0.3), ("rays", 0.5, 0.35, (255, 236, 200))]),
]
SFX = [(2, 0.0, "wind"), (4, 0.0, "panic"), (6, 0.0, "choir"), (9, 0.0, "choir"), (13, 0.0, "splash"), (15, 0.0, "choir")]
MUSIC = "epic"
