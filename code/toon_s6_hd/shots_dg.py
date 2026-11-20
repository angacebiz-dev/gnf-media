"""David & Goliath toon Short - look A: warm golden 2.5D (layered painted sets with depth blur), big-eye toons, fast cuts, pop captions."""
STYLE = dict(toon=dict(out=(24, 16, 14), lw=1.3, grain=True, pastel=0.0), char="hd", post="warm", cap="pop", capmax=12, capy=0.70, gap=0.12, vig=0.35, tail=0.9)
PAUSE = {3: 0.15, 12: 0.1, 18: 0.2, 22: 0.35, 24: 0.2}
G = 0.80   # ground line
def C(w, x, y=G, s=0.13, **k): return dict(w=w, x=x, y=y, s=s, **k)
def CU(c, z0, z1, at=0.40, dx=0.0):
    """camera that puts character c's head at `at` of the frame height (world 1080x1920)"""
    hy = c["y"] - 2.05 * c["s"] * 1080 / 1920
    return (z0, z1, (c["x"] + dx, hy + (0.5 - at) / z0), (c["x"] + dx, hy + (0.5 - at) / z1))
SHOTS = [
 dict(l=0, bg="valley", cam=(1.0, 1.25, (0.5, 0.55), (0.5, 0.62)), chars=[C("goliath", 0.62, 0.70, 0.05, p="walk", ph=0.8, mx=-0.12, f="smug", v="side", flip=True)], fx=[("dust",)]),
 dict(l=1, bg="lowsky", cam=(1.0, 1.12, (0.5, 0.55), (0.5, 0.45)), punch=True, chars=[C("goliath", 0.5, 0.95, 0.36, f="angry", look=(0, -0.3)), C("soldier", 0.86, 0.95, 0.07, f="scared", p="panic")]),
 dict(l=2, bg="valley", cam=(1.6, 1.8, (0.6, 0.62), (0.58, 0.64)), chars=[C("goliath", 0.6, 0.74, 0.08, p="fists", f="angry"), C("soldier", 0.2, 0.62, 0.035, f="scared"), C("soldier", 0.26, 0.625, 0.035, f="scared", dt=0.4)]),
 dict(l=3, bg="lowsky", cam=CU(C("goliath", 0.5, 0.95, 0.30, p="fists", f="yell", talk=True), 1.8, 2.1), shake=1.0, punch=True, chars=[C("goliath", 0.5, 0.95, 0.30, p="fists", f="yell", talk=True)], fx=[("dust",)]),
 dict(l=4, bg="camp", cam=(1.15, 1.3, (0.35, 0.62), (0.6, 0.62)), chars=[C("soldier", 0.25, 0.82, 0.10, f="worried"), C("soldier", 0.45, 0.83, 0.10, f="worried", dt=0.7), C("soldier", 0.68, 0.82, 0.10, f="tired", dt=1.3), C("israelite", 0.85, 0.84, 0.10, f="worried")]),
 dict(l=5, bg="camp", cam=CU(C("saul", 0.5, 0.84, 0.16, f="scared", p="panic"), 2.0, 2.2), punch=True, chars=[C("saul", 0.5, 0.84, 0.16, f="scared", p="panic")]),
 dict(l=5, f=0.5, bg="camp", cam=CU(C("soldier", 0.2, 0.84, 0.11, f="scared", p="panic"), 1.3, 1.4), shake=0.6, chars=[C("soldier", 0.2, 0.84, 0.11, f="scared", p="panic"), C("soldier", 0.42, 0.85, 0.11, f="shocked", p="panic", dt=0.3), C("soldier", 0.64, 0.84, 0.11, f="scared", p="panic", dt=0.6), C("soldier", 0.84, 0.85, 0.11, f="scared", p="panic", dt=0.9)]),
 dict(l=6, bg="camp", cam=(1.25, 1.35, (0.4, 0.62), (0.55, 0.62)), chars=[C("david", 0.15, 0.84, 0.11, p="walk", ph=1.6, mx=0.42, v="side", f="calm")], props=[dict(k="sheep", x=0.05, y=0.86, s=0.07, mx=0.38)]),
 dict(l=7, bg="camp", cam=CU(C("david", 0.5, 0.84, 0.16, f="calm", look=(0.2, 0)), 2.3, 2.5), punch=True, chars=[C("david", 0.5, 0.84, 0.16, f="calm", look=(0.2, 0))], fx=[("glow", 0.5, 0.5, 0.2, (255, 240, 200), 90)]),
 dict(l=8, bg="valley", cam=(1.7, 1.9, (0.35, 0.63), (0.42, 0.62)), chars=[C("david", 0.3, 0.74, 0.07, f="worried", look=(0.8, 0)), C("goliath", 0.66, 0.73, 0.07, p="fists", f="yell")]),
 dict(l=9, bg="camp", cam=CU(C("david", 0.45, 0.84, 0.15, p="point", f="stern", talk=True), 1.8, 2.0), chars=[C("david", 0.45, 0.84, 0.15, p="point", f="stern", talk=True), C("soldier", 0.78, 0.86, 0.13, f="shocked")]),
 dict(l=10, bg="camp", cam=CU(C("saul", 0.36, 0.86, 0.16, f="stern", p="point", talk=True), 1.6, 1.7), chars=[C("saul", 0.36, 0.86, 0.16, f="stern", p="point", talk=True), C("david", 0.72, 0.86, 0.11, f="calm", flip=True)]),
 dict(l=11, bg="brook", cam=(1.3, 1.5, (0.5, 0.6), (0.5, 0.6)), chars=[C("david", 0.62, 0.80, 0.14, f="smug", p="fists", talk=True)], props=[dict(k="lion", x=0.25, y=0.80, s=0.11, mouth=0.0, sleepy=True), dict(k="sheep", x=0.85, y=0.83, s=0.06, flip=True)], fx=[("dust",)]),
 dict(l=12, bg="lowsky", cam=CU(C("david", 0.5, 0.95, 0.24, f="stern", p="fists"), 2.0, 2.2), punch=True, chars=[C("david", 0.5, 0.95, 0.24, f="stern", p="fists")], fx=[("sparks",), ("rays", 0.5, 0.2, (255, 240, 190))]),
 dict(l=13, bg="camp", cam=CU(C("soldier", 0.5, 0.86, 0.15, f="worried", p="stand"), 2.0, 2.1), chars=[C("soldier", 0.5, 0.86, 0.15, f="worried", p="stand")]),
 dict(l=13, f=0.55, bg="camp", cam=CU(C("david", 0.5, 0.86, 0.15, f="smug", p="arms_up"), 2.0, 2.1), punch=True, chars=[C("david", 0.5, 0.86, 0.15, f="smug", p="arms_up")]),
 dict(l=14, bg="brook", cam=(1.2, 1.35, (0.5, 0.62), (0.55, 0.62)), chars=[C("david", 0.2, 0.74, 0.10, p="walk", ph=1.6, mx=0.35, v="side")]),
 dict(l=15, bg="brook", cam=CU(C("david", 0.38, 0.86, 0.14, p="kneel", f="calm", look=(0.6, 0.6)), 2.4, 2.6), punch=True, chars=[C("david", 0.38, 0.86, 0.14, p="kneel", f="calm", look=(0.6, 0.6))], props=[dict(k="stone", x=0.48 + i * 0.045, y=0.85, s=0.016) for i in range(5)]),
 dict(l=16, bg="lowsky", cam=CU(C("goliath", 0.5, 0.95, 0.30, f="smug", talk=True, p="point"), 1.6, 1.8), chars=[C("goliath", 0.5, 0.95, 0.30, f="smug", talk=True, p="point")]),
 dict(l=17, bg="valley", cam=CU(C("david", 0.3, 0.76, 0.08, f="yell", talk=True, p="point"), 2.4, 2.6), punch=True, chars=[C("david", 0.3, 0.76, 0.08, f="yell", talk=True, p="point")]),
 dict(l=18, bg="lowsky", cam=CU(C("david", 0.5, 0.95, 0.26, p="arms_up", f="yell", talk=True), 1.6, 1.8), punch=True, chars=[C("david", 0.5, 0.95, 0.26, p="arms_up", f="yell", talk=True)], fx=[("rays", 0.5, 0.15, (255, 236, 170)), ("sparks",)]),
 dict(l=19, bg="valley", cam=(1.5, 1.7, (0.35, 0.66), (0.55, 0.64)), chars=[C("david", 0.18, 0.77, 0.06, p="run", ph=2.6, mx=0.4, v="side", f="stern"), C("goliath", 0.72, 0.74, 0.08, p="fists", f="smug")], fx=[("dust",)]),
 dict(l=20, bg="lowsky", cam=CU(C("david", 0.5, 0.95, 0.24, p="sling", f="stern"), 2.2, 2.4), punch=True, chars=[C("david", 0.5, 0.95, 0.24, p="sling", f="stern")]),
 dict(l=21, bg="lowsky", cam=CU(C("goliath", 0.6, 0.95, 0.28, f="shocked"), 1.4, 1.5), chars=[C("goliath", 0.6, 0.95, 0.28, f="shocked")], fx=[("projectile", 0.0, 0.55, 0.6, 0.36, 0.45, 0.02), ("flash", 0.5)]),
 dict(l=22, bg="valley", cam=(2.0, 2.2, (0.6, 0.68), (0.6, 0.69)), shake=1.4, props=[dict(k="giantfall", x=0.6, y=0.76, s=0.13, delay=0.2)], fx=[("dust",)]),
 dict(l=23, bg="valley", cam=(2.3, 2.5, (0.36, 0.66), (0.36, 0.66)), chars=[C("david", 0.36, 0.77, 0.08, f="calm", p="stand", look=(0.6, 0.2))]),
 dict(l=24, bg="valley", cam=(1.55, 1.75, (0.52, 0.66), (0.52, 0.68)), chars=[C("david", 0.42, 0.77, 0.07, p="arms_up", f="calm")], props=[dict(k="giantfall", x=0.64, y=0.76, s=0.075, delay=-5)], fx=[("rays", 0.6, 0.18, (255, 240, 200)), ("dust",)]),
 dict(l=25, bg="camp", cam=CU(C("david", 0.5, 0.86, 0.16, f="calm", look=(0, 0.1), talk=True), 2.3, 2.5), chars=[C("david", 0.5, 0.86, 0.16, f="calm", look=(0, 0.1), talk=True)], fx=[("glow", 0.5, 0.45, 0.25, (255, 236, 190), 80)]),
]
SFX = [(0, 0.0, "boom"), (1, 0.0, "boom"), (3, 0.0, "roar"), (5, 0.5, "panic"), (7, 0.0, "ting"), (12, 0.0, "whoosh"), (15, 0.0, "clack"), (18, 0.0, "boom"), (20, 0.1, "swing"), (21, 0.0, "whiz"), (21, 0.55, "thud"), (22, 0.2, "bigthud"), (24, 0.0, "choir")]
MUSIC = "epic"
