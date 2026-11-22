"""David & Goliath v4 shot list (Ricks-Clips style): ~31 shots, characters speak their own lines.
Positions are in BACKGROUND coordinates (0..1 of the 720x1280 render); s = character height unit as a fraction of frame height."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open("/home/claude/gnf/dg3/script.json")); DUR = json.load(open("/home/claude/gnf/dg3/audio/durs.json"))
LINES = S["lines"]; FPS = 24
STARTS, t = [], 0.35
for i, l in enumerate(LINES):
    STARTS.append(round(t, 3))
    gap = 0.34 if l["text"].rstrip().endswith(("?", "!")) else 0.24
    if i in (3, 7, 11, 14): gap += 0.25
    if i == 13: gap = 0.05
    t += DUR[i] + gap
END = round(t + 1.4, 3)
# ---------------- pose library (angles in degrees from straight down; a=(shoulder, elbow)) ----------------
P = {
 "stand": {},
 "hips":   dict(aL=(35, 95), aR=(35, 95)),
 "point":  dict(aR=(95, 0)),
 "point_up": dict(aR=(165, 0), aL=(15, 10)),
 "fist_up": dict(aR=(170, -20), aL=(30, 20), lean=-3),
 "arms_up": dict(aL=(160, 10), aR=(160, 10), bob=0.03),
 "yell":   dict(aL=(60, 50), aR=(150, -10), lean=-8),
 "spear_up": dict(aR=(150, -30), aL=(40, 30), spear_ang=-15, lean=-6),
 "shake_fist": dict(aR=(120, 60), lean=-5),
 "chest":  dict(aR=(30, 140), aL=(15, 10)),
 "facepalm": dict(aL=(150, 125), tilt=-10),
 "laugh":  dict(aL=(35, 95), aR=(35, 95), lean=-10, tilt=-14),
 "laugh2": dict(aL=(35, 95), aR=(35, 95), lean=-6, tilt=-6, bob=0.02),
 "cower":  dict(aL=(120, 80), aR=(120, 80), sq=0.9, tilt=6),
 "carry":  dict(aR=(40, 80), aL=(20, 10)),
 "give":   dict(aR=(80, 10), aL=(20, 10)),
 "take":   dict(aL=(75, 15), aR=(75, 15)),
 "kneel":  dict(lL=(70, 100), lR=(-20, 90), bob=-0.22, aR=(55, 10), lean=10),
 "kneel_up": dict(lL=(70, 100), lR=(-20, 90), bob=-0.22, aR=(110, 30), lean=4),
 "spin":   dict(aR=(170, 0), aL=(30, 20), lean=-4),
 "release": dict(aR=(95, -10), aL=(-30, 10), lean=10, lL=(-15, 0), lR=(25, 5)),
 "brace":  dict(aL=(60, 20), aR=(60, 20), lL=(15, 5), lR=(15, 5), sq=0.93),
 "stagger": dict(aL=(100, 20), aR=(120, 30), lean=-14, tilt=-15),
 "down":   dict(lean=88, aL=(170, 0), aR=(170, 0), sq=0.95),
}
def C(who, x, y, s, keys, face="calm", view="front", flip=False, talk=None, look=(0, 0), **kw):
    d = dict(who=who, x=x, y=y, s=s, keys=keys if isinstance(keys, list) else [(0, keys)], face=face, view=view, flip=flip, talk=talk, look=look); d.update(kw); return d
L = lambda i: i
SHOTS = [
 # L0 Every morning, a giant walked into the valley.
 dict(l=0, f=(0, .5), bg="wide", cam=((1.05, .5, .55), (1.25, .55, .6)), chars=[C("goliath", .74, .70, .035, "stand", "smug", "side", True, walk=1.0, move=((.80, .69), (.62, .70)), itemR="spear")], fx=["dust_walk"]),
 dict(l=0, f=(.5, 1), bg="gol_low", cam=((1.15, .5, .62), (1.05, .5, .55)), chars=[C("goliath", .5, .97, .17, "stand", "angry", "front", walk=0.9, stomp=True, itemR="spear")], fx=["stomp_shake", "dust_walk"]),
 # L1 Over nine feet tall. Covered in bronze.
 dict(l=1, f=(0, .5), bg="gol_low", cam=((2.2, .5, .88), (1.3, .5, .5)), chars=[C("goliath", .5, .97, .17, "hips", "smug", "front", itemR=None)], fx=[]),
 dict(l=1, f=(.5, 1), bg="gol_med", cam=((2.3, .52, .43), (2.6, .52, .40)), chars=[C("goliath", .52, .86, .16, [(0, "hips"), (.5, dict(P["hips"], tilt=8))], "smug", "front", look=(.4, 0))], fx=["shine"]),
 # L2 GOLIATH: I defy the ranks of Israel this day! Give me a man to fight!
 dict(l=2, f=(0, .45), bg="gol_med", cam=((1.25, .52, .55), (1.45, .52, .52)), chars=[C("goliath", .52, .86, .16, [(0, "stand"), (.15, "spear_up"), (.9, dict(P["spear_up"], lean=-10))], "yell", "front", talk=2, itemR="spear")], fx=["shake_s"]),
 dict(l=2, f=(.45, 1), bg="gol_low", cam=((1.75, .5, .36), (2.0, .5, .35)), chars=[C("goliath", .5, .97, .17, [(0, "yell"), (.5, dict(P["yell"], lean=-12))], "yell", "front", talk=2)], fx=["shake_m", "spit"]),
 # L3 And Israel's whole army? Terrified.
 dict(l=3, f=(0, .55), bg="israel", cam=((1.2, .45, .6), (1.3, .42, .6)), chars=[C("soldier", .26, .80, .085, "cower", "scared", itemL="shield", tremble=1), C("soldier", .44, .79, .08, "cower", "scared", flip=True, itemR="shield", tremble=1), C("soldier", .62, .78, .075, "cower", "worried", itemL="shield", tremble=1)], fx=[]),
 dict(l=3, f=(.55, 1), bg="israel", cam=((2.6, .44, .52), (2.9, .44, .52)), chars=[C("soldier", .44, .79, .08, "cower", "shocked", flip=True, itemR="shield", tremble=2)], fx=["gulp"]),
 # L4 Then a shepherd boy showed up, bringing bread for his brothers.
 dict(l=4, f=(0, .55), bg="camp", cam=((1.15, .40, .58), (1.15, .56, .58)), chars=[C("david", .2, .84, .11, "carry", "happy", "side", walk=1.6, move=((.16, .84), (.55, .84)), itemR="basket")], fx=["dust_walk"]),
 dict(l=4, f=(.55, 1), bg="camp", cam=((1.6, .55, .6), (1.75, .56, .6)), chars=[C("brother", .70, .82, .09, [(0, "stand"), (.4, "take")], "shocked", flip=True, look=(-.5, 0)), C("david", .48, .83, .085, [(0, "carry"), (.35, "give")], "happy", itemR="basket")], fx=[]),
 # L5 DAVID: Who is this uncircumcised Philistine, that he should defy the armies of the living God?
 dict(l=5, f=(0, .42), bg="israel", cam=((1.3, .42, .6), (1.4, .45, .58)), chars=[C("soldier", .25, .80, .085, "stand", "shocked", look=(.6, 0), itemL="shield"), C("david", .50, .80, .08, [(0, "stand"), (.3, "point")], "angry", talk=5, look=(.6, 0)), C("soldier", .70, .78, .075, "stand", "shocked", flip=True, look=(-.6, 0), itemR="shield")], fx=[]),
 dict(l=5, f=(.42, 1), bg="david_med", cam=((1.9, .5, .66), (2.2, .5, .63)), chars=[C("david", .5, .88, .15, [(0, "shake_fist"), (.5, dict(P["shake_fist"], aR=(140, 40))), (1, "shake_fist")], "angry", talk=5, gest=1)], fx=[]),
 # L6 SAUL: You are just a boy.
 dict(l=6, f=(0, 1), bg="tent_cu", cam=((1.5, .5, .52), (1.7, .5, .52)), chars=[C("saul", .5, .92, .17, [(0, "stand"), (.35, "facepalm")], "sad", talk=6, headshake=1)], fx=[]),
 # L7 DAVID: The LORD, who delivered me from the claws of the lion and the bear, will deliver me from the hand of this Philistine.
 dict(l=7, f=(0, .38), bg="tent_in", cam=((1.25, .5, .6), (1.35, .5, .6)), chars=[C("saul", .64, .80, .10, "stand", "worried", flip=True, look=(-.6, .5)), C("david", .38, .82, .085, [(0, "stand"), (.25, "chest")], "determined", talk=7, look=(.6, -.3))], fx=[]),
 dict(l=7, f=(.38, .7), bg="david_med", cam=((1.9, .5, .66), (2.0, .5, .64)), chars=[C("david", .5, .88, .15, [(0, "chest"), (.5, dict(P["shake_fist"], aR=(110, 60))), (.9, "point_up")], "determined", talk=7, gest=1)], fx=["flash_claw"]),
 dict(l=7, f=(.7, 1), bg="tent_cu", cam=((1.6, .5, .52), (1.8, .5, .5)), chars=[C("saul", .5, .92, .17, [(0, "stand"), (.6, dict(tilt=6))], "amazed")], fx=[]),
 # L8 No armor. Just a sling, and five smooth stones.
 dict(l=8, f=(0, .4), bg="david_med", cam=((1.5, .5, .72), (1.6, .5, .70)), chars=[C("david", .5, .88, .15, [(0, "spin")], "determined", itemR="sling", sling=1.2)], fx=[]),
 dict(l=8, f=(.4, 1), bg="brook_cu", cam=((1.2, .5, .6), (1.4, .5, .62)), chars=[C("david", .42, .80, .11, [(0, "kneel"), (.5, "kneel_up"), (.7, "kneel")], "determined", itemR="stone")], fx=["stones5"]),
 # L9 GOLIATH: Am I a dog, that you come at me with sticks?
 dict(l=9, f=(0, .55), bg="gol_med", cam=((1.5, .52, .5), (1.6, .52, .48)), chars=[C("goliath", .52, .86, .16, [(0, "laugh"), (.3, "laugh2"), (.6, "laugh"), (1, "laugh2")], "laugh", talk=9, itemR=None)], fx=["shake_s"]),
 dict(l=9, f=(.55, 1), bg="ots", cam=((1.3, .55, .55), (1.45, .58, .55)), chars=[C("goliath", .72, .70, .07, [(0, "point")], "laugh", flip=True, talk=9), C("david", .18, .98, .22, "stand", "determined", "side")], fx=[]),
 # L10 DAVID: You come against me with sword and spear and javelin, but I come against you in the name of the LORD of Hosts!
 dict(l=10, f=(0, .36), bg="david_med", cam=((1.5, .5, .72), (1.7, .5, .68)), chars=[C("david", .5, .88, .15, [(0, "stand"), (.2, "point")], "determined", talk=10, gest=1)], fx=[]),
 dict(l=10, f=(.36, .6), bg="gol_med", cam=((2.0, .52, .45), (2.2, .52, .45)), chars=[C("goliath", .52, .86, .16, [(0, "laugh2"), (.4, "stand"), (.8, "shake_fist")], "angry", itemR=None, face2=(.35, "angry"))], fx=[]),
 dict(l=10, f=(.6, 1), bg="david_med", cam=((2.2, .5, .64), (2.6, .5, .62)), chars=[C("david", .5, .88, .15, [(0, "point"), (.6, "fist_up")], "yell", talk=10)], fx=["wind_hair", "punch_in"]),
 # L11 DAVID: The battle is the LORD's!
 dict(l=11, f=(0, 1), bg="victory", cam=((1.35, .5, .70), (1.55, .5, .67)), chars=[C("david", .5, .90, .16, [(0, "point"), (.25, "fist_up")], "yell", talk=11)], fx=["rays", "shake_m"]),
 # L12 David ran toward him.
 dict(l=12, f=(0, 1), bg="run_side", cam=((1.2, .30, .6), (1.2, .70, .6)), chars=[C("david", .1, .84, .12, "stand", "determined", "side", run=2.6, move=((.14, .84), (.86, .84)), itemR="sling")], fx=["speedlines", "dust_run"]),
 # L13 One stone.
 dict(l=13, f=(0, 1), bg="david_med", cam=((1.7, .5, .68), (1.9, .5, .66)), chars=[C("david", .5, .88, .15, [(0, "spin"), (.75, "spin"), (.86, "release")], "determined", itemR="sling", sling=3.2)], fx=["whoosh_lines"]),
 # L14 And he fell facedown on the ground.
 dict(l=14, f=(0, .3), bg="sky_up", cam=((1.1, .5, .5), (1.2, .5, .45)), chars=[C("goliath", .56, .66, .11, "stagger", "shocked", flip=True)], fx=["stone_streak", "impact_star"]),
 dict(l=14, f=(.3, 1), bg="fall", cam=((1.05, .5, .6), (1.12, .48, .62)), chars=[C("goliath", .74, .90, .16, [(0, "stagger"), (.2, "stagger"), (.75, "down")], "shocked", flip=True, fall=(.2, .75))], fx=["fall_dust", "impact_shake"]),
 # L15 Not by sword or spear. By God.
 dict(l=15, f=(0, .45), bg="fall", cam=((1.15, .46, .63), (1.22, .46, .64)), chars=[C("goliath", .74, .90, .16, "down", "sleep", flip=True)], fx=["settle_dust"]),
 dict(l=15, f=(.45, 1), bg="victory", cam=((1.25, .5, .72), (1.4, .5, .69)), chars=[C("david", .5, .90, .16, [(0, "stand"), (.2, "arms_up")], "happy")], fx=["rays", "confetti_dust"]),
 # L16 So what giant are you facing today?
 dict(l=16, f=(0, 1), bg="end_cu", cam=((1.8, .5, .64), (2.05, .5, .62)), chars=[C("david", .5, .90, .17, "stand", "happy", look=(0, .1))], fx=["end_card"], hold=1.4),
]
def shot_times():
    tt = []
    for k, sh in enumerate(SHOTS):
        li = sh["l"]; a = STARTS[li] + sh["f"][0] * DUR[li] - (0.12 if sh["f"][0] == 0 else 0)
        tt.append(max(0.0, a))
    tt[0] = 0.0
    return [(round(tt[k], 3), round(tt[k + 1] if k + 1 < len(tt) else END, 3)) for k in range(len(tt))]
TIMES = shot_times()
if __name__ == "__main__":
    print("END", END, "shots", len(SHOTS))
    for k, sh in enumerate(SHOTS): print(k, sh["l"], sh["bg"], TIMES[k], round(TIMES[k][1] - TIMES[k][0], 2))
