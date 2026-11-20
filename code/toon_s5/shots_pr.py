"""The prodigal son - look E: paper cut-out. Flat bright colours, white paper edges + drop shadows, stop-motion on twos, paper-strip captions."""
STYLE = dict(toon=dict(out=(40, 30, 30), lw=1.0, grain=False, pastel=0.0), char="sticker", post="paper2", cap="strip", capmax=16, capy=0.80, gap=0.14, vig=0.2, twos=True, tail=1.0)
PAUSE = {0: 0.2, 12: 0.2, 17: 0.3}
def C(w, x, y=0.80, s=0.13, **k): return dict(w=w, x=x, y=y, s=s, **k)
def CU(c, z0, z1, at=0.40, dx=0.0):
    hy = c["y"] - 2.05 * c["s"] * 1080 / 1920
    return (z0, z1, (c["x"] + dx, hy + (0.5 - at) / z0), (c["x"] + dx, hy + (0.5 - at) / z1))
F = lambda **k: C("father", k.pop("x", 0.5), k.pop("y", 0.82), k.pop("s", 0.15), **k)
SON = lambda w="son", **k: C(w, k.pop("x", 0.5), k.pop("y", 0.82), k.pop("s", 0.15), **k)
SHOTS = [
 dict(l=0, bg="farm", cam=(1.5, 1.6, (0.45, 0.64), (0.45, 0.64)), chars=[SON(x=0.32, s=0.11, p="reach", f="smug", talk=True), F(x=0.6, s=0.11, f="worried", flip=True)]),
 dict(l=0, f=0.75, bg="farm", cam=CU(F(), 1.8, 2.0), punch=True, chars=[F(f="shocked")]),
 dict(l=1, bg="road", cam=(1.2, 1.3, (0.5, 0.62), (0.5, 0.64)), chars=[SON(x=0.45, y=0.9, s=0.09, p="walk", ph=1.2, mx=0.05, my=-0.2, f="smug"), F(x=0.86, y=0.6, s=0.03, p="arms_up", f="worried")]),
 dict(l=2, bg="city", cam=(1.4, 1.5, (0.5, 0.62), (0.5, 0.62)), chars=[SON(x=0.5, y=0.8, s=0.12, p="arms_up", f="smug", hop=2.0), C("servant", 0.25, 0.8, 0.09, p="arms_up", f="smug", hop=2.0, dt=0.3), C("official", 0.75, 0.8, 0.09, p="arms_up", f="smug", hop=2.0, dt=0.6)], fx=[("confetti",)]),
 dict(l=3, bg="pigpen", cam=CU(SON(), 1.6, 1.8), punch=True, shake=0.4, chars=[SON(f="shocked")]),
 dict(l=4, bg="pigpen", cam=(1.4, 1.5, (0.5, 0.64), (0.5, 0.64)), chars=[SON("son_rag", x=0.4, s=0.11, f="tired")], props=[dict(k="pig", x=0.62, y=0.84, s=0.07, ph=1.0), dict(k="pig", x=0.78, y=0.86, s=0.06, flip=True, dt=0.5)]),
 dict(l=5, bg="pigpen", cam=(1.9, 2.0, (0.5, 0.66), (0.5, 0.66)), chars=[SON("son_rag", x=0.4, s=0.12, p="sit", f="tired", look=(0.8, 0.4))], props=[dict(k="pig", x=0.64, y=0.84, s=0.07)]),
 dict(l=6, bg="pigpen", cam=CU(SON("son_rag"), 1.8, 2.0), chars=[SON("son_rag", f="shocked", look=(0, -0.6))], fx=[("rays", 0.5, 0.2, (255, 250, 200))]),
 dict(l=7, bg="pigpen", cam=CU(SON("son_rag"), 1.7, 1.85), chars=[SON("son_rag", f="worried", talk=True, p="point")]),
 dict(l=7, f=0.55, bg="farm", cam=(1.5, 1.6, (0.4, 0.64), (0.42, 0.64)), chars=[C("servant", 0.3, 0.8, 0.1, f="calm", hop=1.0), C("servant", 0.5, 0.81, 0.1, f="smug", dt=0.4)]),
 dict(l=8, bg="road", cam=(1.4, 1.5, (0.5, 0.64), (0.5, 0.64)), chars=[SON("son_rag", x=0.45, y=0.84, s=0.11, p="walk", ph=0.8, v="side", mx=0.08, talk=True, f="worried")]),
 dict(l=9, bg="road", cam=CU(SON("son_rag"), 1.7, 1.85), chars=[SON("son_rag", f="worried", talk=True, p="pray")]),
 dict(l=10, bg="road", cam=CU(SON("son_rag"), 1.9, 2.05), chars=[SON("son_rag", f="tired", talk=True)]),
 dict(l=11, bg="feast", cam=CU(F(), 1.6, 1.8), chars=[F(f="shocked", look=(-0.6, -0.2))]),
 dict(l=11, f=0.6, bg="road", cam=(1.0, 1.1, (0.5, 0.5), (0.5, 0.52)), chars=[SON("son_rag", x=0.5, y=0.66, s=0.04, f="tired"), F(x=0.83, y=0.6, s=0.03, f="shocked")]),
 dict(l=12, bg="road", cam=CU(F(s=0.15), 1.7, 1.9), punch=True, chars=[F(p="run", ph=2.6, v="side", flip=True, f="shocked")], fx=[("dust",)]),
 dict(l=13, bg="road", cam=(1.2, 1.35, (0.55, 0.6), (0.5, 0.66)), chars=[F(x=0.78, y=0.64, s=0.08, p="run", ph=2.6, mx=-0.25, my=0.22, v="side", flip=True, f="shocked")], fx=[("dust",)]),
 dict(l=14, bg="road", cam=CU(F(x=0.55), 1.7, 1.85, dx=-0.05), chars=[SON("son_rag", x=0.42, f="shocked"), F(x=0.58, p="hug", f="calm", flip=True)], fx=[("hearts",)]),
 dict(l=15, bg="farm", cam=(1.4, 1.5, (0.45, 0.64), (0.5, 0.64)), chars=[F(x=0.35, s=0.11, p="point", f="smug", talk=True), C("servant", 0.62, 0.81, 0.09, p="run", ph=2.0, v="side", mx=0.2), C("servant", 0.75, 0.82, 0.09, p="run", ph=2.2, v="side", mx=0.2, dt=0.3)]),
 dict(l=16, bg="feast", cam=(1.6, 1.7, (0.5, 0.6), (0.5, 0.6)), chars=[SON("son_robe", x=0.42, s=0.12, f="shocked"), F(x=0.6, s=0.12, p="arms_up", f="yell", talk=True, hop=1.5)], fx=[("confetti",)]),
 dict(l=17, bg="feast", cam=(1.2, 1.3, (0.5, 0.62), (0.5, 0.62)), chars=[C("servant", 0.18, 0.8, 0.08, p="arms_up", hop=2.0), SON("son_robe", x=0.4, s=0.09, p="arms_up", f="calm", hop=2.0), F(x=0.58, s=0.09, p="arms_up", f="calm", hop=2.0), C("servant", 0.8, 0.8, 0.08, p="arms_up", hop=2.0, dt=0.4)], fx=[("confetti",)]),
 dict(l=18, bg="road", cam=(1.1, 1.2, (0.5, 0.56), (0.5, 0.58)), chars=[SON("son_robe", x=0.5, y=0.78, s=0.06, p="walk", ph=0.7, my=-0.08, mx=0.06), F(x=0.56, y=0.78, s=0.06, p="walk", ph=0.7, my=-0.08, mx=0.06)]),
 dict(l=19, bg="road", cam=CU(F(), 1.6, 1.8), chars=[F(f="calm", look=(-0.5, 0.2))], fx=[("glow", 0.5, 0.45, 0.3, (255, 230, 170), 90)]),
]
SFX = [(0, 0.75, "boom"), (2, 0.0, "party"), (3, 0.0, "thud"), (4, 0.0, "oink"), (12, 0.0, "whoosh"), (14, 0.0, "choir"), (16, 0.0, "party"), (17, 0.0, "party")]
MUSIC = "bouncy"
