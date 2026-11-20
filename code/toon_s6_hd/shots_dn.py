"""Daniel in the lions' den - look B: night, silhouette toons with warm rim light, slow push-ins, glowing captions, British narrator."""
STYLE = dict(toon=dict(out=(24, 16, 14), lw=1.3, grain=True, pastel=0.0), char="hd", post="warm", cap="pop", capmax=12, capy=0.70, gap=0.12, vig=0.35, tail=0.9)
PAUSE = {6: 0.2, 12: 0.3, 13: 0.4, 16: 0.4, 18: 0.2}
def C(w, x, y=0.8, s=0.13, **k): return dict(w=w, x=x, y=y, s=s, **k)
def CU(c, z0, z1, at=0.40, dx=0.0):
    hy = c["y"] - 2.05 * c["s"] * 1080 / 1920
    return (z0, z1, (c["x"] + dx, hy + (0.5 - at) / z0), (c["x"] + dx, hy + (0.5 - at) / z1))
SLOW = dict()
d_pray = C("daniel", 0.5, 0.86, 0.17, p="kneel", f="calm", look=(0.3, -0.6))
dar = C("darius", 0.5, 0.86, 0.17, f="worried")
SHOTS = [
 dict(l=0, bg="palace", cam=(1.3, 1.45, (0.5, 0.6), (0.5, 0.62)), chars=[C("official", 0.3, 0.86, 0.12, p="point", f="smug", talk=True), C("darius", 0.6, 0.86, 0.13, f="calm"), C("official", 0.82, 0.87, 0.12, f="smug", flip=True)], fx=[("glow", 0.5, 0.5, 0.3, (255, 170, 80), 70)]),
 dict(l=0, f=0.55, bg="den", cam=(1.5, 1.7, (0.5, 0.6), (0.5, 0.62)), props=[dict(k="lion", x=0.3, y=0.80, s=0.12, mouth=1.0, roar=True), dict(k="lion", x=0.72, y=0.81, s=0.13, mouth=1.0, roar=True, flip=True, dt=0.5)], fx=[("glow", 0.5, 0.3, 0.2, (150, 170, 255), 60)]),
 dict(l=1, bg="city", cam=(1.7, 1.9, (0.42, 0.6), (0.52, 0.6)), chars=[C("daniel", 0.34, 0.76, 0.13, p="walk", ph=0.9, mx=0.2, v="side", f="worried")]),
 dict(l=2, bg="room", cam=CU(C("daniel", 0.5, 0.86, 0.17), 1.3, 1.45, at=0.5), chars=[C("daniel", 0.5, 0.86, 0.17, f="calm", look=(0, -0.7), p="reach")], fx=[("rays", 0.6, 0.2, (160, 180, 255))]),
 dict(l=3, bg="room", cam=CU(d_pray, 1.9, 2.15), chars=[d_pray], fx=[("glow", 0.5, 0.6, 0.2, (255, 170, 80), 80)]),
 dict(l=4, bg="room", cam=CU(C("daniel", 0.5, 0.86, 0.19), 1.35, 1.5, at=0.48), chars=[C("daniel", 0.5, 0.86, 0.19, p="kneel", f="calm", look=(0.3, -0.6))], fx=[("rays", 0.6, 0.22, (160, 180, 255))]),
 dict(l=5, bg="city", cam=(2.0, 2.2, (0.45, 0.6), (0.5, 0.6)), chars=[C("official", 0.38, 0.76, 0.11, f="smug", look=(0.8, 0)), C("official", 0.58, 0.765, 0.11, f="smug", look=(0.8, 0), dt=0.6)]),
 dict(l=6, bg="palace", cam=CU(dar, 1.8, 2.0), chars=[dar], fx=[("glow", 0.3, 0.45, 0.2, (255, 170, 80), 80)]),
 dict(l=6, f=0.55, bg="palace", cam=(1.6, 1.75, (0.5, 0.6), (0.5, 0.6)), chars=[C("official", 0.4, 0.86, 0.13, f="smug", p="fists"), C("official", 0.62, 0.86, 0.13, f="smug", dt=0.4)]),
 dict(l=7, bg="den", cam=(1.5, 1.7, (0.5, 0.58), (0.5, 0.6)), shake=0.5, chars=[C("daniel", 0.5, 0.80, 0.14, f="worried", look=(0, -0.5))], props=[dict(k="lion", x=0.2, y=0.80, s=0.11, mouth=0.8, roar=True), dict(k="lion", x=0.82, y=0.81, s=0.12, mouth=0.8, roar=True, flip=True, dt=0.4)]),
 dict(l=8, bg="dentop", cam=CU(C("darius", 0.5, 0.81, 0.12), 1.7, 1.9), chars=[C("darius", 0.5, 0.81, 0.12, f="worried", talk=True, p="reach")]),
 dict(l=9, bg="dentop", cam=(2.0, 2.3, (0.5, 0.7), (0.5, 0.7)), punch=True, props=[dict(k="seal", x=0.5, y=0.687, s=0.022)], fx=[("glow", 0.5, 0.69, 0.06, (255, 80, 60), 120)]),
 dict(l=10, bg="palace", cam=CU(C("darius", 0.5, 0.86, 0.17), 1.6, 1.8), chars=[C("darius", 0.5, 0.86, 0.17, p="sit", f="tired")], fx=[("glow", 0.25, 0.5, 0.2, (255, 170, 80), 60)]),
 dict(l=11, bg="dentop_dawn", cam=(1.2, 1.35, (0.4, 0.6), (0.5, 0.62)), chars=[C("darius", 0.15, 0.81, 0.09, p="run", ph=2.2, mx=0.3, v="side", f="worried")], fx=[("glow", 0.6, 0.45, 0.35, (255, 200, 150), 70)]),
 dict(l=12, bg="dentop_dawn", cam=CU(C("darius", 0.5, 0.81, 0.13), 1.8, 2.1), shake=0.3, chars=[C("darius", 0.5, 0.81, 0.13, f="scared", talk=True, p="panic")]),
 dict(l=13, bg="den", cam=(1.0, 1.25, (0.5, 0.55), (0.5, 0.62)), nocap=False, fx=[("glow", 0.5, 0.65, 0.12, (220, 230, 255), 90)]),
 dict(l=14, bg="den", cam=(1.5, 1.65, (0.5, 0.58), (0.5, 0.58)), chars=[C("daniel", 0.5, 0.80, 0.14, f="calm", talk=True)], props=[dict(k="lion", x=0.22, y=0.80, s=0.11, sleepy=True), dict(k="lion", x=0.8, y=0.81, s=0.11, sleepy=True, flip=True)], fx=[("rays", 0.5, 0.05, (220, 230, 255)), ("glow", 0.5, 0.6, 0.3, (220, 230, 255), 90)]),
 dict(l=15, bg="dentop_dawn", cam=(1.4, 1.55, (0.5, 0.6), (0.5, 0.6)), chars=[C("daniel", 0.42, 0.81, 0.11, f="calm", p="arms_up"), C("darius", 0.64, 0.81, 0.11, f="shocked", flip=True)], fx=[("glow", 0.5, 0.4, 0.4, (255, 210, 160), 80)]),
 dict(l=16, bg="dentop_dawn", cam=CU(C("daniel", 0.5, 0.81, 0.13), 1.9, 2.2), chars=[C("daniel", 0.5, 0.81, 0.13, f="calm", look=(0, -0.4))], fx=[("rays", 0.5, 0.1, (255, 220, 170))]),
 dict(l=17, bg="room", cam=CU(d_pray, 1.7, 1.9), chars=[d_pray], fx=[("rays", 0.6, 0.2, (160, 180, 255))]),
 dict(l=18, bg="room", cam=(1.15, 1.25, (0.5, 0.52), (0.5, 0.54)), chars=[C("daniel", 0.5, 0.84, 0.15, p="kneel", f="calm", look=(0.3, -0.6))], fx=[("rays", 0.6, 0.2, (160, 180, 255))]),
 dict(l=19, bg="den", cam=CU(C("daniel", 0.5, 0.84, 0.15), 1.9, 2.2), chars=[C("daniel", 0.5, 0.84, 0.15, f="calm", look=(0, 0.1))], props=[dict(k="lion", x=0.12, y=0.83, s=0.10, sleepy=True)], fx=[("glow", 0.5, 0.5, 0.35, (220, 230, 255), 80)]),
]
SFX = [(0, 0.55, "roar"), (7, 0.0, "roar"), (9, 0.0, "stone"), (12, 0.0, "boom"), (14, 0.0, "choir"), (16, 0.0, "choir")]
MUSIC = "epic"
