# ====================== v3 additions: new sets + per-background stills ======================
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots3 import BG, ANIM_FRAMES

for o in list(bpy.data.objects): o.animation_data_clear()
for l in bpy.data.lights: l.animation_data_clear()
sc.world.node_tree.animation_data_clear()
cam.constraints.clear()
tr = cam.constraints.new("TRACK_TO"); tr.target = tgt; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"

def M2(name, rgb, rough=0.7, emit=None, es=0.0):
    return mat(name, rgb, rough, emit, es)
M.update({
    "flesh": M2("flesh", (0.62, 0.16, 0.20), 0.45), "rib": M2("rib", (0.92, 0.62, 0.58), 0.6), "wet": M2("wet", (0.55, 0.14, 0.20), 0.35),
    "bile": M2("bile", (0.20, 0.45, 0.30), 0.08), "weed": M2("weed", (0.12, 0.45, 0.18), 0.7),
    "sand": M2("sand", (0.86, 0.60, 0.34), 0.95), "seaflat": M2("seaflat", (0.03, 0.38, 0.55), 0.08), "foam": M2("foam", (0.95, 0.97, 1.0), 0.6),
    "rock": M2("rock", (0.45, 0.42, 0.40), 0.9), "palm": M2("palm", (0.45, 0.30, 0.16), 0.9), "leaf": M2("leaf", (0.16, 0.55, 0.20), 0.7),
    "wall": M2("wall", (0.84, 0.58, 0.34), 0.9), "wall2": M2("wall2", (0.72, 0.46, 0.28), 0.9), "gate": M2("gate", (0.08, 0.06, 0.05), 0.9),
    "blue_tile": M2("blue_tile", (0.10, 0.30, 0.70), 0.4), "gold": M2("gold", (0.95, 0.70, 0.25), 0.3), "cloth": M2("cloth", (0.75, 0.15, 0.15), 0.8),
})

# ---- inside the great fish (x = -100) ----
FX = -100.0
bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=3.2, depth=16, location=(FX, 0, 2.0), rotation=(0, math.pi / 2, 0))
bpy.context.object.data.materials.append(M["flesh"])
for cap in (-8.0, 8.0):
    cyl("fcap", (FX + cap, 0, 2.0), 3.4, 0.1, M["flesh"], verts=28, rot=(0, math.pi / 2, 0))
for k in range(10):
    bpy.ops.mesh.primitive_torus_add(major_radius=3.05, minor_radius=0.2, location=(FX - 7 + k * 1.55, 0, 2.0), rotation=(0, math.pi / 2, 0))
    bpy.context.object.data.materials.append(M["rib"])
box("ffloor", (FX, 0, -0.05), (16, 5.6, 0.1), M["wet"], 0.0)
for k, (x, y, r) in enumerate([(FX + 1.5, 0.8, 0.9), (FX - 2.0, -0.6, 0.7), (FX + 3.6, -0.3, 0.6)]):
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=0.02, location=(x, y, 0.01)); bpy.context.object.data.materials.append(M["bile"])
box("f_crate", (FX + 2.4, 1.4, 0.35), (0.7, 0.7, 0.7), M["wood"], 0.04, rot=(0, 0, 0.4))   # the cargo they threw overboard
cyl("f_barrel", (FX - 2.6, 1.3, 0.45), 0.38, 0.9, M["wood_dark"], verts=10)
for k in range(6):
    cyl(f"f_weed{k}", (FX - 3 + k * 1.2, 1.9 - (k % 2) * 3.6, 0.6), 0.05, 1.2, M["weed"], verts=6, rot=(0.3 * (k % 3 - 1), 0.2, 0))
bpy.ops.object.light_add(type="POINT", location=(FX + 1.0, -1.0, 3.6)); fl1 = bpy.context.object; fl1.data.energy = 140; fl1.data.color = (1.0, 0.45, 0.42)
bpy.ops.object.light_add(type="POINT", location=(FX - 3.0, 1.0, 3.0)); fl2 = bpy.context.object; fl2.data.energy = 60; fl2.data.color = (0.6, 0.8, 1.0)
bpy.ops.object.light_add(type="SPOT", location=(FX, 0, 4.9), rotation=(0, 0, 0)); fspot = bpy.context.object
fspot.data.energy = 0; fspot.data.spot_size = math.radians(40); fspot.data.color = (1.0, 0.85, 0.55)

# ---- beach (x = 200) ----
BXc = 200.0
box("sand", (BXc, -12, -0.5), (90, 34, 1.0), M["sand"], 0.0)
box("seaflat", (BXc, 45, -0.06), (200, 90, 0.04), M["seaflat"], 0.0)
box("foam", (BXc, 5.05, -0.02), (90, 0.25, 0.04), M["foam"], 0.0)
random.seed(21)
for k in range(6):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, location=(BXc + random.uniform(-14, 14), random.uniform(-4, 3.5), 0.1))
    r = bpy.context.object; s = random.uniform(0.3, 0.9); r.scale = (s * 1.3, s, s * 0.7); r.data.materials.append(M["rock"])
def palm(x, y, h=5.0, lean=0.2):
    cyl("trunk", (x + lean * h / 2, y, h / 2), 0.16, h, M["palm"], verts=8, rot=(0, lean, 0))
    for k in range(6):
        a = k * math.pi / 3
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.45, depth=2.4, location=(x + lean * h + math.cos(a) * 1.0, y + math.sin(a) * 1.0, h - 0.2),
                                        rotation=(math.sin(a) * 1.25, -math.cos(a) * 1.25, 0))
        bpy.context.object.scale = (1, 0.25, 1); bpy.context.object.data.materials.append(M["leaf"])
for x, y, h in [(BXc - 6, 1.5, 5.5), (BXc - 8.5, -1.0, 4.4), (BXc + 7, 2.2, 5.0), (BXc + 9.5, -2.0, 4.0)]:
    palm(x, y, h, 0.18 if x < BXc else -0.18)

# ---- Nineveh (x = 300) ----
NXc = 300.0
box("ngr", (NXc, 0, -0.5), (140, 90, 1.0), M["sand"], 0.0)
box("nwall", (NXc, 16, 3.5), (70, 2.2, 7.0), M["wall"], 0.05)
for k in range(35):
    if abs(k * 2 - 34) < 3: continue
    box(f"cren{k}", (NXc - 34 + k * 2, 16, 7.35), (1.0, 2.2, 0.7), M["wall"], 0.03)
for side in (-1, 1):
    box(f"gtower{side}", (NXc + side * 3.3, 15.8, 5.0), (3.4, 3.4, 10.0), M["wall2"], 0.05)
    for k in range(3):
        box(f"gtcren{side}{k}", (NXc + side * 3.3 - 1.2 + k * 1.2, 15.8, 10.35), (0.8, 3.4, 0.7), M["wall2"], 0.03)
    box(f"gband{side}", (NXc + side * 3.3, 14.08, 7.5), (3.4, 0.1, 0.5), M["blue_tile"], 0.0)
box("gate_open", (NXc, 14.85, 2.6), (3.2, 0.3, 5.2), M["gate"], 0.0)
box("gate_lintel", (NXc, 14.8, 5.6), (3.8, 0.5, 0.6), M["blue_tile"], 0.02)
box("gate_gold", (NXc, 14.5, 5.6), (1.0, 0.1, 0.35), M["gold"], 0.0)
random.seed(8)
for k in range(16):
    x = NXc + random.uniform(-30, 30); y = random.uniform(20, 42); h = random.uniform(6, 13); w_ = random.uniform(3, 6)
    box(f"nb{k}", (x, y, h / 2), (w_, w_, h), M["wall"] if k % 2 else M["wall2"], 0.05)
for k, (sz, z) in enumerate([(18, 1.75), (13, 5.25), (8.5, 8.75), (4.5, 12.25)]):
    box(f"zig{k}", (NXc + 2, 34, z), (sz, sz, 3.5), M["wall2"] if k % 2 else M["wall"], 0.05)
box("zigtop", (NXc + 2, 34, 14.5), (2.5, 2.5, 1.0), M["blue_tile"], 0.03)
for x in (NXc - 9, NXc + 9, NXc - 15, NXc + 14):
    palm(x, 12.0, 5.5, 0.1 if x < NXc else -0.1)
for k, x in enumerate((NXc - 1.4, NXc + 1.4)):
    box(f"banner{k}", (x, 14.0, 7.2), (0.7, 0.05, 2.2), M["cloth"], 0.0)

# ---- environment presets ----
nt = sc.world.node_tree
ramps = [n for n in nt.nodes if n.type == "VALTORGB"]
day_r = ramps[0]; mixn = [n for n in nt.nodes if n.type == "MIX"][0]
flashn = [n for n in nt.nodes if n.type == "VALUE"][0]
SKY = {
    "day":    [(0.30, (1.0, 0.86, 0.66)), (0.55, (0.52, 0.76, 1.0)), (1.0, (0.14, 0.40, 0.95))],
    "dusk":   [(0.30, (1.0, 0.42, 0.18)), (0.55, (0.70, 0.20, 0.25)), (1.0, (0.12, 0.05, 0.18))],
    "golden": [(0.30, (1.0, 0.82, 0.45)), (0.55, (0.98, 0.66, 0.42)), (1.0, (0.36, 0.52, 0.92))],
}
def set_sky(key):
    els = day_r.color_ramp.elements
    while len(els) > 3: els.remove(els[-1])
    while len(els) < 3: els.new(0.5)
    for e, (p, c) in zip(els, SKY[key]): e.position = p; e.color = (*c, 1)

sc.view_settings.look = "AgX - Punchy"
bgsn = [n for n in nt.nodes if n.type == "MATH"][0]
for nm in ("stone", "stone2", "wood"):
    bsdf = M[nm].node_tree.nodes["Principled BSDF"]; c0 = bsdf.inputs["Base Color"].default_value
    bsdf.inputs["Base Color"].default_value = (c0[0] * 0.92, c0[1] * 0.80, c0[2] * 0.70, 1)
def set_env(env, waves=None, tt=0.0, flash=0.0):
    storm_v = {"storm": 1.0, "calm": 0.2}.get(env, 0.0)
    set_sky({"dusk": "dusk", "golden": "golden", "calm": "golden"}.get(env, "day"))
    mixn.inputs[0].default_value = storm_v
    flashn.outputs[0].default_value = flash
    bgsn.inputs[0].default_value = {"storm": 1.0, "dusk": 0.8}.get(env, 0.55)
    if env == "storm":
        sun.data.energy = 1.6; sun.data.color = (0.60, 0.68, 0.85)
    elif env == "dusk":
        sun.data.energy = 3.0; sun.data.color = (1.0, 0.45, 0.25); sun.rotation_euler = (math.radians(84), 0, math.radians(-30))
    elif env in ("golden", "calm"):
        sun.data.energy = 4.2; sun.data.color = (1.0, 0.74, 0.42); sun.rotation_euler = (math.radians(74), 0, math.radians(-45))
    else:
        sun.data.energy = 4.0; sun.data.color = (1.0, 0.84, 0.62); sun.rotation_euler = (math.radians(66), 0, math.radians(-60))
    bolt.data.energy = flash * 1.6
    oc.wave_scale = waves if waves else (1.25 if env == "storm" else 0.35)
    oc.time = tt

def place_ship(bgname, f=0):
    sea_bg = bgname.startswith(("b_storm", "b_deck", "b_calm"))
    if sea_bg:
        s = 1.0 if BG[bgname]["env"] == "storm" else 0.0
        roll = math.sin(f / 7.0) * 0.12 * s; pitch = math.sin(f / 11.0 + 1) * 0.07 * s; heave = math.sin(f / 9.0) * 0.3 * s
        if not BG[bgname].get("anim"): roll = pitch = heave = 0.0
        ship.location = (40.0, 0, heave); ship.rotation_euler = (roll, pitch, 0)
    else:
        ship.location = (0, 0, 0); ship.rotation_euler = (0, 0, 0)
    plank.hide_render = sea_bg

def setup_bg(name, f=0):
    b = BG[name]
    flash = 0.0
    if b.get("anim") and b["env"] == "storm":
        for c0 in (10, 30):
            dd = f - c0
            if 0 <= dd <= 3: flash = max(flash, [3.0, 0.6, 2.2, 0.3][dd])
    set_env(b["env"], b.get("waves"), (f + 120) / FPS, flash)
    place_ship(name, f)
    fspot.data.energy = 0
    cam.location = b["cam"]; tgt.location = b["tgt"]; cam_d.lens = b["lens"]
    cam_d.dof.use_dof = b.get("focus") is not None
    if b.get("focus") is not None:
        from mathutils import Vector
        cam_d.dof.focus_distance = (Vector(b["focus"]) - Vector(b["cam"])).length
        cam_d.dof.aperture_fstop = b["fstop"]
    bpy.context.view_layer.update()

def anchors(name):
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    setup_bg(name)
    out = {}
    for k, p in BG[name]["pts"].items():
        a = world_to_camera_view(sc, cam, Vector(p)); b = world_to_camera_view(sc, cam, Vector(p) + Vector((0, 0, 1)))
        out[k] = [a.x, 1 - a.y, a.z, abs(b.y - a.y)]
    return out

OUTD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg3")
os.makedirs(OUTD, exist_ok=True)
names = [n for n in BG] if "--only" not in args else args[args.index("--only") + 1].split(",")
if "--anchors" in args:
    json.dump({n: anchors(n) for n in BG}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "anchors3.json"), "w"))
    print("ANCHORS OK"); sys.exit(0)
for name in names:
    b = BG[name]
    if b.get("anim"):
        sc.render.resolution_x, sc.render.resolution_y = 540, 960; sc.cycles.samples = arg("--asamples", 8)
        for f in range(ANIM_FRAMES[name]):
            p = os.path.join(OUTD, f"{name}_{f:03d}.png")
            if os.path.exists(p): continue
            setup_bg(name, f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
    else:
        p = os.path.join(OUTD, f"{name}.png")
        if os.path.exists(p): continue
        sc.render.resolution_x, sc.render.resolution_y = 720, 1280; sc.cycles.samples = arg("--samples", 24)
        setup_bg(name); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
    print("BG DONE", name, flush=True)
