"""v3 Jonah (Ricks-Clips-style test): backgrounds (3D, rendered once each) + shot list (2D comp) + timeline.
Shared by scene3.py (Blender) and comp3.py (PIL)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
FPS = 24
LINES = json.load(open(os.path.join(D, "audio/lines.json")))

# ---------- timeline ----------
STARTS, t = [], 0.15
for i, (txt, dur) in enumerate(LINES):
    STARTS.append(round(t, 3))
    gap = 0.20 if txt.rstrip().endswith((".", "?", "!")) and not txt.rstrip().endswith("...") else 0.09
    if i in (8, 25, 31, 36): gap += 0.25      # breathing room at section turns
    t += dur + gap
END = round(t + 0.6, 3)

J_DOCK = (-6.0, -0.4, 1.2)
# ---------- backgrounds ----------
# cam, tgt, lens, focus (world point or None), fstop, env, extra; pts = world points to project (feet)
BG = {
 "b_port_low":  dict(cam=(-5.55, -3.3, 1.85), tgt=(-6.0, 0, 2.5), lens=30, focus=(-6.0, -0.4, 2.6), fstop=1.6, env="day", pts=dict(jonah=J_DOCK)),
 "b_nin_dusk":  dict(cam=(300, -12, 2.2), tgt=(300, 16, 6), lens=24, focus=None, fstop=8, env="dusk", pts={}),
 "b_port_side": dict(cam=(-3.6, -3.4, 1.4), tgt=(-6.2, 0, 2.4), lens=30, focus=(-6.0, -0.4, 2.4), fstop=1.6, env="day", pts=dict(jonah=J_DOCK)),
 "b_port_pan":  dict(cam=(-4.5, -6.2, 1.5), tgt=(-4.5, 0, 2.0), lens=22, focus=(-4.5, -0.2, 2.0), fstop=2.4, env="day", pts=dict(ja=(-8.0, -0.2, 1.2), jb=(-1.2, -0.2, 1.2))),
 "b_port_wide": dict(cam=(-10.5, -10.5, 4.0), tgt=(-2.0, 0, 2.6), lens=26, focus=(-5.0, 0, 2.0), fstop=4.0, env="day", pts=dict(jonah=J_DOCK)),
 "b_plank":     dict(cam=(-1.7, -5.0, 2.3), tgt=(-1.6, 0, 2.1), lens=28, focus=(-1.6, 0, 2.0), fstop=2.0, env="day", pts=dict(captain=(-0.6, -0.1, 1.2), jonah=(-2.7, 0.0, 1.25))),
 "b_hatch":     dict(cam=(2.4, -3.1, 3.3), tgt=(1.0, 0, 1.7), lens=30, focus=(1.0, 0, 1.6), fstop=2.0, env="day", pts=dict(jonah=(1.0, 0.0, 1.2))),
 "b_below":     dict(cam=(102.95, -2.2, 1.4), tgt=(100.1, 0.5, 0.65), lens=24, focus=(100.0, 0.5, 0.4), fstop=2.0, env="inside", pts=dict(bed=(100.0, 0.5, 0.08), captain=(101.0, 1.45, 0.0))),
 "b_storm_wide": dict(cam=(49, -12.5, 1.2), tgt=(40, 0, 3.4), lens=24, focus=None, fstop=8, env="storm", anim=True, pts={}),
 "b_storm_sail": dict(cam=(42.3, -3.6, 1.9), tgt=(40.0, 0, 5.2), lens=22, focus=None, fstop=8, env="storm", pts={}),
 "b_deck":      dict(cam=(39.8, -4.3, 2.0), tgt=(39.8, 0, 2.35), lens=28, focus=(39.8, 0.3, 2.2), fstop=1.8, env="storm",
                     pts=dict(s1=(41.0, 0.2, 1.2), s2=(38.6, -0.2, 1.2), jonah=(39.8, 0.4, 1.2), captain=(40.6, 1.0, 1.2))),
 "b_deck_high": dict(cam=(40.0, -3.3, 4.4), tgt=(40.0, 0.2, 1.1), lens=28, focus=(40.0, 0.2, 1.4), fstop=2.2, env="storm",
                     pts=dict(s1=(41.0, 0.4, 1.2), s2=(39.0, 0.5, 1.2), captain=(40.0, 1.2, 1.2), stones=(40.0, -0.3, 1.2))),
 "b_deck_row":  dict(cam=(37.1, -4.3, 1.9), tgt=(39.6, 0, 2.1), lens=28, focus=(39.6, 0, 2.0), fstop=2.0, env="storm", pts=dict(s1=(40.6, 0.6, 1.2), s2=(38.9, -0.4, 1.2))),
 "b_storm_huge": dict(cam=(52, -15, 0.8), tgt=(40, 0, 4.2), lens=22, focus=None, fstop=8, env="storm", waves=1.75, anim=True, pts={}),
 "b_storm_side": dict(cam=(44.6, -7.6, 2.0), tgt=(42.5, 2.0, 2.4), lens=24, focus=(42.5, 1.0, 2.0), fstop=4.0, env="storm", pts=dict(ja=(40.5, 0.0, 2.6), jb=(44.5, 3.5, -0.2))),
 "b_calm":      dict(cam=(49, -12, 2.0), tgt=(40, 0, 3.2), lens=24, focus=None, fstop=8, env="calm", pts=dict(s1=(40.9, 0.3, 1.2), s2=(39.1, -0.3, 1.2))),
 "b_fish":      dict(cam=(-98.0, -2.5, 1.5), tgt=(-100.0, 0, 1.0), lens=26, focus=(-100.0, 0, 0.9), fstop=2.0, env="fish", pts=dict(jonah=(-100.0, 0.0, 0.0))),
 "b_beach":     dict(cam=(201.7, -6.2, 1.5), tgt=(199.6, 2.5, 1.4), lens=26, focus=(199.6, 0, 0.9), fstop=2.4, env="day", pts=dict(jonah=(199.6, 0.0, 0.0), ja=(197.0, 9.0, 3.0))),
 "b_beach_up":  dict(cam=(200.5, -2.3, 0.7), tgt=(200.0, 0, 2.7), lens=26, focus=(200.0, 0, 1.6), fstop=2.0, env="day", pts=dict(jonah=(200.0, 0.0, 0.0))),
 "b_nin_walk":  dict(cam=(295.5, -6.0, 1.8), tgt=(299.5, 6, 3.0), lens=26, focus=(299.0, 2.5, 1.5), fstop=3.0, env="day", pts=dict(ja=(296.6, 1.8, 0.0), jb=(300.6, 4.2, 0.0))),
 "b_nin_kneel": dict(cam=(300.0, -3.6, 1.6), tgt=(300.0, 8, 2.2), lens=28, focus=(300.0, 1.8, 0.8), fstop=2.2, env="golden",
                     pts=dict(n1=(298.7, 1.8, 0.0), n2=(300.2, 2.3, 0.0), n3=(301.6, 1.6, 0.0), n4=(299.4, 4.6, 0.0))),
 "b_nin_gold":  dict(cam=(300, -16, 3.0), tgt=(300, 16, 7), lens=24, focus=None, fstop=8, env="golden", pts={}),
 "b_hill":      dict(cam=(309.6, -5.3, 1.5), tgt=(305.0, 3.0, 2.3), lens=28, focus=(306.0, -1.5, 1.4), fstop=1.8, env="golden", pts=dict(jonah=(306.0, -1.5, 0.0))),
}

# ---------- shots ----------
# (line, f0, f1, bg, move, zoom, chars, fx); zoom = (factor, point_key, head_up_units) ; chars = list of dicts
def C(who, at, view="front", pose="stand", face="calm", flip=False, look=(0, 0), **kw):
    d = dict(who=who, at=at, view=view, pose=pose, face=face, flip=flip, look=look); d.update(kw); return d
SHOTS = [
 (0, 0, 1, "b_port_low", "push", None, [C("jonah", "jonah", face="smug", look=(0.3, 0))], []),
 (1, 0, 1, "b_nin_dusk", "push", None, [], ["vignette_red"]),
 (2, 0, 1, "b_port_low", "punch", (1.9, "jonah", 2.05), [C("jonah", "jonah", face="shocked")], []),
 (3, 0, 1, "b_port_side", "push", None, [C("jonah", "jonah", "side", face="stern")], []),
 (4, 0, 1, "b_port_pan", "pan", None, [C("jonah", ("ja", "jb"), "side", "run", "angry")], ["speedlines", "dust"]),
 (5, 0, 1, "b_port_wide", "push", None, [C("jonah", "jonah", "side", "point", "smug")], []),
 (6, 0, 1, "b_plank", "push", None, [C("captain", "captain", "front", "point", "smug", look=(-0.5, 0)), C("jonah", "jonah", "side", "stand", "worried")], ["coin"]),
 (7, 0, 1, "b_hatch", "push", None, [C("jonah", "jonah", "side", "stand", "tired", sink=1.7)], []),
 (8, 0, 1, "b_below", "push", None, [C("jonah", "bed", face="sleep", lie=True)], ["zzz"]),
 (9, 0, 0.55, "b_storm_wide", "shake", None, [], ["rain", "lightning"]),
 (9, 0.55, 1, "b_storm_sail", "shake", None, [], ["rain", "wind"]),
 (10, 0, 1, "b_deck", "shake", None, [C("s1", "s1", "front", "panic", "scared"), C("s2", "s2", "front", "panic", "scared", True)], ["rain"]),
 (11, 0, 1, "b_deck", "shake", (1.8, "s1", 2.0), [C("s1", "s1", "front", "panic", "yell")], ["rain"]),
 (12, 0, 1, "b_deck", "shake", None, [C("s1", "s1", "front", "panic", "scared"), C("s2", "s2", "front", "throw", "angry")], ["rain", "crates"]),
 (13, 0, 1, "b_below", "punch", (1.25, "bed", 0.4), [C("jonah", "bed", face="sleep", lie=True)], ["zzz"]),
 (14, 0, 1, "b_below", "push", (2.3, "bed", 0.35), [C("jonah", "bed", face="sleep", lie=True)], ["zzz"]),
 (15, 0, 1, "b_below", "shake", None, [C("captain", "captain", "front", "shake", "angry", True), C("jonah", "bed", face="shocked", lie=True)], []),
 (16, 0, 1, "b_below", "punch", (1.9, "captain", 2.05), [C("captain", "captain", "front", "shake", "yell", True, talk=True)], []),
 (17, 0, 1, "b_below", "push", (1.3, "captain", 1.2), [C("captain", "captain", "front", "throw", "yell", True, talk=True), C("jonah", "bed", face="shocked", lie=True)], []),
 (18, 0, 0.55, "b_deck_high", "shake", None, [C("s1", "s1", "front", "stand", "worried", look=(-0.4, 0.7)), C("s2", "s2", "front", "stand", "worried", look=(0.4, 0.7)), C("captain", "captain", "front", "stand", "stern", look=(0, 0.8))], ["rain", "stones"]),
 (18, 0.55, 1, "b_deck_high", "push", (2.2, "stones", 0.1), [], ["rain", "stones"]),
 (19, 0, 1, "b_deck", "punch", None, [C("jonah", "jonah", "front", "stand", "shocked"), C("s1", "s1", "side", "point", "angry", True), C("s2", "s2", "side", "stand", "stern"), C("captain", "captain", "front", "stand", "stern", look=(-0.7, 0.3))], ["rain", "lightning"]),
 (20, 0, 1, "b_deck", "push", (1.9, "jonah", 2.05), [C("jonah", "jonah", "front", "stand", "tired", talk=True)], ["rain"]),
 (21, 0, 1, "b_deck", "shake", (1.5, "s1", 1.4), [C("s1", "s1", "front", "stand", "shocked", look=(-0.6, 0)), C("jonah", "jonah", "front", "stand", "tired", talk=True)], ["rain"]),
 (22, 0, 0.55, "b_deck_row", "shake", None, [C("s1", "s1", "side", "row", "angry"), C("s2", "s2", "side", "row", "angry")], ["rain", "oars"]),
 (22, 0.55, 1, "b_deck_row", "shake", (1.9, "s1", 2.0), [C("s1", "s1", "side", "row", "angry")], ["rain", "oars"]),
 (23, 0, 1, "b_storm_huge", "shake", None, [], ["rain", "lightning"]),
 (24, 0, 1, "b_storm_side", "shake", None, [C("jonah", ("ja", "jb"), "front", "panic", "scared", fly=True)], ["rain", "splash_end"]),
 (25, 0, 1, "b_calm", "push", None, [C("s1", "s1", "front", "stand", "calm"), C("s2", "s2", "front", "stand", "calm", True)], ["rays"]),
 (26, 0, 1, "u_sink", "push", None, [], []),
 (27, 0, 1, "u_fish", "punch", None, [], []),
 (28, 0, 0.5, "b_fish", "push", None, [C("jonah", "jonah", "front", "kneel", "tired")], ["drips"]),
 (28, 0.5, 1, "b_fish", "push", (2.0, "jonah", 1.75), [C("jonah", "jonah", "front", "kneel", "tired")], ["drips"]),
 (29, 0, 1, "b_fish", "push", None, [C("jonah", "jonah", "front", "pray", "tired")], ["glow"]),
 (30, 0, 1, "u_swim", "push", None, [], []),
 (31, 0, 1, "b_beach", "shake", None, [C("jonah", ("ja", "jonah"), "front", "panic", "shocked", fly=True, seaweed=True)], ["splat_end"]),
 (32, 0, 1, "b_beach", "punch", (2.0, "jonah", 2.0), [C("jonah", "jonah", "front", "stand", "tired", seaweed=True)], []),
 (33, 0, 1, "b_beach_up", "push", None, [C("jonah", "jonah", "front", "stand", "worried", look=(0, -0.9), seaweed=True)], []),
 (34, 0, 1, "b_nin_walk", "push", None, [C("jonah", ("ja", "jb"), "side", "walk", "stern")], []),
 (35, 0, 0.5, "b_nin_kneel", "push", None, [C("ninevite", "n4", "front", "kneel", "tired"), C("ninevite", "n1", "front", "kneel", "tired"), C("ninevite", "n3", "front", "pray", "tired"), C("ninevite", "n2", "front", "kneel", "tired")], []),
 (35, 0.5, 1, "b_nin_kneel", "push", (2.0, "n2", 1.75), [C("ninevite", "n2", "front", "pray", "tired")], ["tear"]),
 (36, 0, 1, "b_nin_gold", "push", None, [], ["rays"]),
 (37, 0, 1, "b_hill", "punch", None, [C("jonah", "jonah", "side", "fists", "stern", True)], []),
 (38, 0, 1, "b_hill", "shake", (2.0, "jonah", 2.05), [C("jonah", "jonah", "front", "fists", "angry")], ["steam", "vignette_red"]),
 (39, 0, 0.5, "b_port_pan", "pan", None, [C("jonah", ("ja", "jb"), "side", "run", "angry")], ["speedlines", "flashback"]),
 (39, 0.5, 1, "b_hill", "push", (1.5, "jonah", 1.6), [C("jonah", "jonah", "side", "fists", "angry", True)], ["steam"]),
 (40, 0, 1, "b_nin_gold", "push", None, [], ["rays"]),
 (41, 0, 1, "b_hill", "push", (2.2, "jonah", 2.05), [C("jonah", "jonah", "front", "fists", "angry")], ["steam"]),
]
# who aliases for the toon module
WHO = {"s1": "sailor1", "s2": "sailor2"}

def shot_times():
    out = []
    for k, (li, f0, f1, *_r) in enumerate(SHOTS):
        dur = LINES[li][1]
        a = STARTS[li] + f0 * dur - (0.06 if f0 == 0 else 0)
        out.append(max(0.0, a))
    out[0] = 0.0
    res = []
    for k in range(len(SHOTS)):
        b = out[k + 1] if k + 1 < len(SHOTS) else END
        res.append((round(out[k], 3), round(b, 3)))
    return res
TIMES = shot_times()
ANIM_FRAMES = {}
for k, sh in enumerate(SHOTS):
    bg = sh[3]
    if bg in BG and BG[bg].get("anim"):
        a, b = TIMES[k]; ANIM_FRAMES[bg] = max(ANIM_FRAMES.get(bg, 0), int(round((b - a) * FPS)) + 2)

if __name__ == "__main__":
    print("END", END, "shots", len(SHOTS), "anim", ANIM_FRAMES)
    for k, sh in enumerate(SHOTS):
        print(k, sh[0], sh[3], TIMES[k], round(TIMES[k][1] - TIMES[k][0], 2), LINES[sh[0]][0][:40])
