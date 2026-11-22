"""David & Goliath v4 (Nov 22, 2026) — toy-diorama 3D sets for the Ricks-Clips-style toon Short.
Valley of Elah (two camps on two hills, brook in the middle), Saul's tent interior. Renders one still per camera.
python3 scene4.py [--only a,b] [--samples N]"""
import bpy, math, sys, os, random
from mathutils import Vector
args = sys.argv[1:]
def arg(n, d): return type(d)(args[args.index(n) + 1]) if n in args else d
R = random.Random(4)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = arg("--samples", 20)
sc.cycles.use_denoising = True; sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 1; sc.cycles.transmission_bounces = 0
sc.render.resolution_x, sc.render.resolution_y = 720, 1280; sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = "PNG"
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"

def mat(name, rgb, rough=0.8, emit=None, es=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = es
    return m
def noisy(name, c1, c2, scale=6.0, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    tx = nt.nodes.new("ShaderNodeTexNoise"); tx.inputs["Scale"].default_value = scale; tx.inputs["Detail"].default_value = 6
    cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (*c1, 1); cr.color_ramp.elements[1].color = (*c2, 1)
    cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[1].position = 0.65
    nt.links.new(tx.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    return m
M = {
 "ground": noisy("ground", (0.62, 0.46, 0.22), (0.50, 0.40, 0.16), 3.0),
 "hill": noisy("hill", (0.55, 0.42, 0.20), (0.40, 0.36, 0.14), 2.0),
 "rock": noisy("rock", (0.55, 0.50, 0.44), (0.40, 0.36, 0.32), 8.0),
 "water": mat("water", (0.10, 0.42, 0.55), 0.08),
 "pebble": mat("pebble", (0.72, 0.70, 0.66), 0.5),
 "tent_w": mat("tent_w", (0.86, 0.80, 0.66), 0.9),
 "tent_r": mat("tent_r", (0.62, 0.16, 0.12), 0.9),
 "pole": mat("pole", (0.30, 0.18, 0.08), 0.8),
 "flag_b": mat("flag_b", (0.15, 0.30, 0.65), 0.9),
 "flag_r": mat("flag_r", (0.70, 0.12, 0.10), 0.9),
 "bush": noisy("bush", (0.28, 0.36, 0.12), (0.20, 0.28, 0.08), 10.0),
 "olive": noisy("olive", (0.32, 0.40, 0.18), (0.24, 0.30, 0.12), 12.0),
 "trunk": mat("trunk", (0.30, 0.20, 0.12), 0.9),
 "fabric": noisy("fabric", (0.55, 0.20, 0.14), (0.46, 0.15, 0.10), 30.0),
 "fabric2": noisy("fabric2", (0.80, 0.68, 0.50), (0.70, 0.58, 0.42), 30.0),
 "rug": noisy("rug", (0.42, 0.12, 0.30), (0.30, 0.08, 0.22), 50.0),
 "gold": mat("gold", (0.85, 0.62, 0.20), 0.3),
 "lamp": mat("lamp", (1.0, 0.7, 0.3), 0.5, emit=(1.0, 0.55, 0.2), es=8.0),
 "shield": mat("shield", (0.55, 0.36, 0.18), 0.6),
}
def obj_add(o, m, loc=None, rot=None, scale=None, bevel=0.0, smooth=False):
    if loc: o.location = loc
    if rot: o.rotation_euler = rot
    if scale: o.scale = scale
    if bevel:
        bv = o.modifiers.new("bv", "BEVEL"); bv.width = bevel; bv.segments = 2
    o.data.materials.append(m)
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    return o
def box(loc, dims, m, bevel=0.05, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = dims
    bpy.ops.object.transform_apply(scale=True); return obj_add(o, m, bevel=bevel)
def cone(loc, r, d, m, verts=4, rot=(0, 0, 0), r2=0.0):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=d, location=loc, rotation=rot); return obj_add(bpy.context.object, m, bevel=0.03)
def cyl(loc, r, d, m, verts=8, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d, location=loc, rotation=rot); return obj_add(bpy.context.object, m)
def ico(loc, r, m, sub=1, sc_=(1, 1, 1), smooth=False):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r, location=loc); o = bpy.context.object; o.scale = sc_
    return obj_add(o, m, smooth=smooth)
# ---------- terrain: valley along Y, Israel hill at -X, Philistine hill at +X ----------
bpy.ops.mesh.primitive_grid_add(x_subdivisions=160, y_subdivisions=160, size=160, location=(0, 30, 0))
g = bpy.context.object
for v in g.data.vertices:
    x, y = v.co.x, v.co.y + 30
    h = 0.0
    h += 7.5 * math.exp(-((x + 26) / 13) ** 2) + 7.5 * math.exp(-((x - 26) / 13) ** 2)      # two hills
    h += 9.0 * math.exp(-((y - 75) / 18) ** 2) * (0.6 + 0.4 * math.cos(x / 9))               # far ridge
    h += 0.35 * math.sin(x * 0.7 + y * 0.3) + 0.25 * math.sin(y * 0.9 - x * 0.2)
    h -= 0.45 * math.exp(-((x - 1.2 * math.sin(y / 6)) / 1.6) ** 2)                          # brook bed
    v.co.z = max(h, -0.6)
for p in g.data.polygons: p.use_smooth = True
obj_add(g, M["ground"])
def hz(x, y):
    yy = y
    h = 7.5 * math.exp(-((x + 26) / 13) ** 2) + 7.5 * math.exp(-((x - 26) / 13) ** 2)
    h += 9.0 * math.exp(-((yy - 75) / 18) ** 2) * (0.6 + 0.4 * math.cos(x / 9))
    h += 0.35 * math.sin(x * 0.7 + yy * 0.3) + 0.25 * math.sin(yy * 0.9 - x * 0.2)
    h -= 0.45 * math.exp(-((x - 1.2 * math.sin(yy / 6)) / 1.6) ** 2)
    return max(h, -0.6)
# brook water ribbon
bpy.ops.mesh.primitive_grid_add(x_subdivisions=4, y_subdivisions=200, size=1, location=(0, 0, 0))
br = bpy.context.object
for v in br.data.vertices:
    y = (v.co.y + 0.5) * 140 - 40; x = 1.2 * math.sin(y / 6) + v.co.x * 1.3
    v.co.x, v.co.y, v.co.z = x, y, hz(1.2 * math.sin(y / 6), y) + 0.10
obj_add(br, M["water"])
for k in range(120):                                  # smooth stones in and along the brook
    y = R.uniform(-30, 40); x = 1.2 * math.sin(y / 6) + R.uniform(-1.9, 1.9)
    r = R.uniform(0.08, 0.22); ico((x, y, hz(x, y) + r * 0.3), r, M["pebble"], 2, (1, 0.8, 0.55), True)
# tents
def tent(x, y, m, flagm, s=1.0, rot=0.0):
    z = hz(x, y)
    cone((x, y, z + 1.0 * s), 1.6 * s, 2.0 * s, m, 4, (0, 0, rot))
    cyl((x, y, z + 2.2 * s), 0.05, 0.8 * s, M["pole"])
    box((x + 0.3 * s, y, z + 2.45 * s), (0.6 * s, 0.03, 0.32 * s), flagm, 0.0)
for i in range(18):
    tent(-26 + R.uniform(-9, 9), R.uniform(2, 40), M["tent_w"], M["flag_b"], R.uniform(0.8, 1.2), R.uniform(0, 1))
    tent(26 + R.uniform(-9, 9), R.uniform(2, 40), M["tent_r"], M["flag_r"], R.uniform(0.8, 1.2), R.uniform(0, 1))
# rocks, bushes, olive trees
for k in range(260):
    x, y = R.uniform(-45, 45), R.uniform(-25, 60)
    if abs(x) < 3 and R.random() < 0.7: continue
    z = hz(x, y)
    if R.random() < 0.45: ico((x, y, z + 0.1), R.uniform(0.25, 0.9), M["rock"], 1, (1, R.uniform(0.7, 1.2), R.uniform(0.5, 0.8)))
    elif R.random() < 0.7: ico((x, y, z + 0.2), R.uniform(0.3, 0.6), M["bush"], 2, (1, 1, 0.7), True)
    else:
        cyl((x, y, z + 0.6), 0.09, 1.2, M["trunk"]); ico((x, y, z + 1.5), R.uniform(0.6, 0.9), M["olive"], 2, (1.2, 1.2, 0.8), True)
# camp edge props: shields + spears at the Israelite line (x ~ -9)
for k in range(10):
    y = 2 + k * 1.6; x = -9.5 + R.uniform(-0.6, 0.6); z = hz(x, y)
    cyl((x, y, z + 0.5), 0.55, 0.08, M["shield"], 12, (math.radians(80), 0, math.radians(90)))
    cyl((x - 0.4, y + 0.3, z + 1.3), 0.03, 2.6, M["pole"], 6, (0.15, 0, 0))
# ---------- Saul's tent interior (far away at x=300) ----------
IX = 300.0
box((IX, 0, -0.05), (10, 10, 0.1), M["fabric2"], 0)
box((IX, 0, 0.01), (4.0, 3.0, 0.02), M["rug"], 0)
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=5, depth=6, location=(IX, 0, 3)); wall = bpy.context.object
obj_add(wall, M["fabric"]); wall.modifiers.new("sol", "SOLIDIFY").thickness = 0.1
for n in wall.data.polygons:
    if abs(n.normal.z) > 0.9: n.select = True
cone((IX, 0, 7.0), 5.2, 2.4, M["fabric"], 16)
cyl((IX, 0, 3.5), 0.12, 7.0, M["pole"], 8)
box((IX + 0.0, 2.6, 0.5), (1.4, 0.8, 1.0), M["gold"], 0.08)                     # throne seat
box((IX + 0.0, 3.0, 1.6), (1.4, 0.2, 2.2), M["gold"], 0.08)
for dx in (-2.6, 2.6):
    cyl((IX + dx, 2.2, 0.9), 0.08, 1.8, M["pole"]); ico((IX + dx, 2.2, 1.9), 0.18, M["lamp"], 2)
    bpy.ops.object.light_add(type="POINT", location=(IX + dx, 2.0, 2.0)); l = bpy.context.object; l.data.energy = 250; l.data.color = (1.0, 0.62, 0.3)
for k in range(5):
    box((IX - 3.2 + k * 0.3, -2.5 + k * 0.4, 0.35), (0.6, 0.6, 0.7), M["shield"], 0.06)
# ---------- sky + sun ----------
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; nt = w.node_tree
for n in list(nt.nodes):
    if n.type != "OUTPUT_WORLD": nt.nodes.remove(n)
out = [n for n in nt.nodes if n.type == "OUTPUT_WORLD"][0]
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Window"], sep.inputs[0])
rmp = nt.nodes.new("ShaderNodeValToRGB"); E = rmp.color_ramp.elements
E[0].position, E[0].color = 0.40, (1.0, 0.70, 0.38, 1); E[1].position, E[1].color = 1.0, (0.22, 0.45, 0.92, 1)
e = E.new(0.62); e.color = (0.98, 0.60, 0.45, 1)
nt.links.new(sep.outputs["Y"], rmp.inputs["Fac"])
bgn = nt.nodes.new("ShaderNodeBackground"); bgn.inputs["Strength"].default_value = 1.0
nt.links.new(rmp.outputs["Color"], bgn.inputs["Color"]); nt.links.new(bgn.outputs[0], out.inputs[0])
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(70), 0, math.radians(-40))); sun = bpy.context.object
sun.data.energy = 4.2; sun.data.color = (1.0, 0.80, 0.55); sun.data.angle = math.radians(4)
# ---------- camera ----------
cam_d = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
tgt = bpy.data.objects.new("tgt", None); sc.collection.objects.link(tgt)
tc_ = cam.constraints.new("TRACK_TO"); tc_.target = tgt; tc_.track_axis = "TRACK_NEGATIVE_Z"; tc_.up_axis = "UP_Y"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bgs4 import BG
OUTD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg")
names = list(BG) if "--only" not in args else args[args.index("--only") + 1].split(",")
for name in names:
    b = BG[name]; p = os.path.join(OUTD, f"{name}.png")
    if os.path.exists(p) and "--force" not in args: continue
    cx, cy, cz = b["cam"]; tx, ty, tz = b["tgt"]
    if b.get("ground"):                         # heights relative to terrain
        cz += hz(cx, cy); tz += hz(tx, ty)
    cam.location = (cx, cy, cz); tgt.location = (tx, ty, tz); cam_d.lens = b["lens"]
    cam_d.dof.use_dof = b.get("fstop") is not None
    if cam_d.dof.use_dof:
        cam_d.dof.focus_distance = b.get("focus", (Vector((tx, ty, tz)) - Vector((cx, cy, cz))).length); cam_d.dof.aperture_fstop = b["fstop"]
    sun.data.energy = b.get("sun", 4.2); sun.rotation_euler = (math.radians(b.get("sun_el", 70)), 0, math.radians(b.get("sun_az", -40)))
    sc.render.filepath = p; bpy.ops.render.render(write_still=True); print("BG DONE", name, flush=True)
