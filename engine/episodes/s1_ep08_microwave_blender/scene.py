# Blender (bpy 5.x) scene: "How a microwave heats food" — S1 cinematic product-macro look (same family as ep06/ep07).
# Procedural per frame (no keyframes): update(t) drives molecules, waves, turntable, sparks, chocolate and camera.
# usage: WORK=/home/claude/mw python3 scene.py <out_dir> [--res 50] [--spp 6] [--stills t1,t2] [--f0 1 --f1 N] [--step 1]
import bpy, json, math, sys, os, random
from mathutils import Vector, Euler

A = sys.argv[1:]
OUT = A[0]; os.makedirs(OUT, exist_ok=True)
def opt(k, d): return A[A.index(k)+1] if k in A else d
RES = int(opt('--res', 50)); SPP = int(opt('--spp', 6)); STILLS = opt('--stills', '')
WORK = os.environ.get('WORK', '/home/claude/mw')
FPS = 24
VO = json.load(open(f'{WORK}/vo.json')); L = {l['key']: l for l in VO['lines']}
TOTAL = VO['total']; NF = int(math.ceil(TOTAL*FPS))
S = {k: L[k]['start'] for k in L}

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, RES
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP
sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 1
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = float(opt('--thr', 0.05))
sc.render.use_persistent_data = True
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94

def ss(x): x = min(1, max(0, x)); return x*x*(3-2*x)
def ramp(t, a, b): return ss((t-a)/max(1e-6, b-a))
def lerp(a, b, k): return a + (b-a)*k
def vlerp(a, b, k): return Vector(a).lerp(Vector(b), k)

def principled(name, col, rough=0.4, coat=0.0, metal=0.0, emit=None, estr=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if coat: b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.06
    b.inputs['Emission Color'].default_value = (*(emit or (0, 0, 0)), 1); b.inputs['Emission Strength'].default_value = estr
    return m, b
def emis(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0]); return m, e

ORANGE = (1.0, 0.22, 0.0); PURPLE = (0.55, 0.12, 1.0); WHITE = (1, 1, 1); BLUE = (0.1, 0.5, 1.0)
M_O, O_B = principled('oxy', (0.80, 0.06, 0.05), 0.22, coat=1.0, emit=ORANGE, estr=0.0)
M_H, H_B = principled('hyd', (0.92, 0.92, 0.95), 0.2, coat=1.0, emit=ORANGE, estr=0.0)
M_FLOOR, _ = principled('floor', (0.03, 0.03, 0.034), 0.45)
M_STEEL, _ = principled('steel', (0.62, 0.62, 0.65), 0.28, metal=1.0)
M_DARKM, _ = principled('darkm', (0.08, 0.08, 0.09), 0.35, metal=1.0)
M_COPPER, _ = principled('copper', (0.95, 0.55, 0.35), 0.25, metal=1.0)
M_PLATE, _ = principled('plate', (0.55, 0.62, 0.66), 0.12, coat=0.6)
M_PLINTH, _ = principled('plinth', (0.06, 0.06, 0.07), 0.5, metal=0.3)
M_CUP, _ = principled('cup', (0.93, 0.90, 0.84), 0.2, coat=1.0)
M_CHAI, CHAI_B = principled('chai', (0.42, 0.22, 0.10), 0.18, coat=0.5, emit=ORANGE, estr=0.0)
M_CHOC, CHOC_B = principled('choc', (0.20, 0.09, 0.04), 0.35, coat=0.3)
M_WRAP, _ = principled('wrap', (0.75, 0.05, 0.08), 0.35)
M_SLOT, SLOT_E = emis('slot', (1.0, 0.45, 0.1), 0.0)
M_SPARK, SPARK_E = emis('spark', (0.7, 0.85, 1.0), 0.0)
M_HOT, HOT_E = emis('hot', (1.0, 0.3, 0.02), 0.0)
M_COLD, COLD_E = emis('cold', (0.1, 0.45, 1.0), 0.0)
WAVE_E = {}

def ob(o, mat=None, parent=None, smooth=True):
    if mat: o.data.materials.append(mat)
    if parent: o.parent = parent
    if smooth and hasattr(o.data, 'polygons'):
        for p in o.data.polygons: p.use_smooth = True
    return o
def empty(name, parent=None):
    e = bpy.data.objects.new(name, None); sc.collection.objects.link(e)
    if parent: e.parent = parent
    return e

# ---------- curves (waves, steam) ----------
NP = 160
def make_curve(name, col, depth=0.026, strength=1.6, n=NP):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = depth; cu.bevel_resolution = 3; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(n-1)
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o)
    m, e = emis('c_'+name, col, strength); cu.materials.append(m); WAVE_E[name] = e; return o
def set_curve(o, pts, depth, strength):
    sp = o.data.splines[0]
    for i, p in enumerate(pts): sp.points[i].co = (p[0], p[1], p[2], 1)
    o.data.bevel_depth = max(0.001, depth); WAVE_E[o.name].inputs[1].default_value = strength
    o.hide_render = strength <= 0.01 or depth <= 0.002

# ---------- turntable + cup of chai ----------
PLATE_C = Vector((0.85, 0.35, -1.02))
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.35, depth=0.18, location=PLATE_C - Vector((0, 0, 0.13))); ob(bpy.context.object, M_PLINTH)
TT = empty('TT'); TT.location = PLATE_C
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.15, depth=0.05, location=(0, 0, 0)); plate = ob(bpy.context.object, M_PLATE, TT)
bpy.ops.object.modifier_add(type='BEVEL'); plate.modifiers[-1].width = 0.02; plate.modifiers[-1].segments = 3
CUP = empty('CUP', TT); CUP_OFF = Vector((0.0, -0.5, 0.03)); CUP.location = CUP_OFF
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.30, depth=0.62, location=(0, 0, 0.31)); cupb = ob(bpy.context.object, M_CUP, CUP)
bpy.ops.object.modifier_add(type='SOLIDIFY'); cupb.modifiers[-1].thickness = 0.035
bpy.ops.object.modifier_add(type='BEVEL'); cupb.modifiers[-1].width = 0.012; cupb.modifiers[-1].segments = 2
# open the top: delete top cap
import bmesh
me = cupb.data; bm = bmesh.new(); bm.from_mesh(me)
top = [f for f in bm.faces if len(f.verts) > 4 and f.calc_center_median().z > 0.3]; bmesh.ops.delete(bm, geom=top, context='FACES'); bm.to_mesh(me); bm.free()
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.275, depth=0.02, location=(0, 0, 0.53)); ob(bpy.context.object, M_CHAI, CUP)
bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.035, location=(0.33, 0, 0.32), rotation=(math.radians(90), 0, 0)); ob(bpy.context.object, M_CUP, CUP)
# spoon (only in the metal beat)
SPOON = empty('SPOON', CUP)
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.022, depth=0.75, location=(0, 0, 0.375)); ob(bpy.context.object, M_STEEL, SPOON)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(0, 0, 0.0)); sb = ob(bpy.context.object, M_STEEL, SPOON); sb.scale = (0.07, 0.03, 0.11)
SPOON_TIP = Vector((0, 0, 0.75))
SPARKS = []
for k in range(9):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.008, depth=1, location=(0, 0, 0)); s = ob(bpy.context.object, M_SPARK, None, False); SPARKS.append(s)
bpy.ops.object.light_add(type='POINT', location=(0, 0, 0)); SPARK_L = bpy.context.object; SPARK_L.data.color = (0.6, 0.8, 1.0); SPARK_L.data.shadow_soft_size = 0.05
# hot / cold spots on the plate (fixed in space; the plate turns through them)
SPOTS = []
for i, (x, y, hot) in enumerate([(-0.55, -0.45, 1), (0.5, -0.5, 0), (0.0, 0.05, 1), (-0.6, 0.5, 0), (0.55, 0.5, 1)]):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.26, depth=0.004, location=PLATE_C + Vector((x, y, 0.032))); s = ob(bpy.context.object, M_HOT if hot else M_COLD, None, False)
    SPOTS.append((s, hot))

# ---------- magnetron ----------
MAG = empty('MAG'); MAG_HOME = Vector((-2.55, 0.35, 0.25)); MAG.location = MAG_HOME
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); mb = ob(bpy.context.object, M_DARKM, MAG, False); mb.scale = (0.62, 0.62, 0.62)
bpy.ops.object.modifier_add(type='BEVEL'); mb.modifiers[-1].width = 0.04; mb.modifiers[-1].segments = 3
for k in range(7):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.05, 0, -0.27 + k*0.09)); f = ob(bpy.context.object, M_STEEL, MAG, False); f.scale = (0.78, 0.78, 0.018)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.13, depth=0.22, location=(0.38, 0, 0.0), rotation=(0, math.radians(90), 0)); ob(bpy.context.object, M_COPPER, MAG)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.1, location=(0.5, 0, 0.0)); ob(bpy.context.object, M_COPPER, MAG)
bpy.ops.mesh.primitive_torus_add(major_radius=0.2, minor_radius=0.02, location=(0.32, 0, 0), rotation=(0, math.radians(90), 0)); ob(bpy.context.object, M_SLOT, MAG)
# chocolate bar (origin beat)
CHOC = empty('CHOC'); CHOC_HOME = Vector((-1.95, -0.45, -0.12)); CHOC.location = CHOC_HOME
bpy.ops.mesh.primitive_cube_add(size=1); wrap = ob(bpy.context.object, M_WRAP, CHOC, False); wrap.scale = (0.58, 0.30, 0.07); wrap.location = (0.32, 0, 0)
CHOC_SQ = []
for i in range(3):
    for j in range(2):
        bpy.ops.mesh.primitive_cube_add(size=1); q = ob(bpy.context.object, M_CHOC, CHOC, False); q.scale = (0.17, 0.13, 0.07)
        bpy.ops.object.modifier_add(type='BEVEL'); q.modifiers[-1].width = 0.02; q.modifiers[-1].segments = 2
        q.location = (-0.30 + i*0.19, -0.07 + j*0.15, 0.0); CHOC_SQ.append((q, Vector(q.location)))

# ---------- water molecules ----------
MOLS = []
random.seed(7)
GRID = [(-0.62, 0.62), (0.0, 0.62), (0.62, 0.62), (-0.62, 0.0), (0.0, 0.0), (0.62, 0.0), (-0.62, -0.62), (0.0, -0.62), (0.62, -0.62)]
CL = empty('CLUSTER')
for i, (gx, gz) in enumerate(GRID):
    m = empty(f'mol{i}', CL)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, radius=0.16, location=(0, 0, 0)); ob(bpy.context.object, M_O, m)
    for s in (-1, 1):
        a = math.radians(52.25)*s
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.105, location=(0.19*math.sin(a), 0, 0.19*math.cos(a))); ob(bpy.context.object, M_H, m)
    MOLS.append(dict(o=m, home=Vector((gx + random.uniform(-0.08, 0.08), random.uniform(-0.1, 0.1), gz + random.uniform(-0.08, 0.08))),
                     ph=random.uniform(0, 6.28), base=random.uniform(-0.6, 0.6), yaw=random.uniform(-0.6, 0.6)))
CL_BIG = (Vector((0.15, 0.0, 0.3)), 1.0)        # big cluster in mid-air
CL_CUP = (PLATE_C + CUP_OFF + Vector((0, 0, 1.0)), 0.34)  # tiny cluster floating over the chai

# waves: three rows from the magnetron horn to the cluster
WV = [make_curve(f'W{i}', PURPLE, 0.024) for i in range(3)]
STEAM = [make_curve(f'S{i}', (1.0, 0.85, 0.7), 0.02, 0.0, 60) for i in range(3)]

# ---------- floor, lights, world ----------
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -1.3)); ob(bpy.context.object, M_FLOOR, None, False)
def area(name, loc, rot, energy, size, col):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = size; ld.color = col
    o = bpy.data.objects.new(name, ld); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot; return o
area('key', (-2.5, -4.0, 3.6), (math.radians(50), math.radians(-25), math.radians(-20)), 520, 3.5, (1.0, 0.9, 0.8))
area('rim', (3.6, 3.5, 2.2), (math.radians(-60), math.radians(45), 0), 650, 2.0, (1.0, 0.62, 0.4))
area('fill', (2.0, -5.0, 3.0), (math.radians(55), math.radians(20), 0), 70, 4, (0.85, 0.9, 1.0))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.006, 0.005, 0.009, 1)

# ---------- camera ----------
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.lens = 40; cd.sensor_width = 36; cd.sensor_fit = 'HORIZONTAL'
cd.dof.use_dof = True; cd.dof.aperture_fstop = 3.0
tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt); cd.dof.focus_object = tgt
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
CUPW = PLATE_C + CUP_OFF
HERO = ((0.95, -3.6, 0.6), (CUPW.x, CUPW.y, CUPW.z + 0.27), 3.0, 46)
SHOTS = [
 (0.0,               *HERO),
 (S['mol']-0.2,      (0.95, -3.3, 0.7), (CUPW.x, CUPW.y, CUPW.z + 0.35), 3.0, 48),
 (S['mol']+1.6,      (0.15, -4.6, 0.9), (0.15, 0, 0.0), 4.0, 42),            # big molecules
 (S['mag']+0.2,      (-2.0, -4.0, 1.1), (-1.85, 0.2, -0.1), 3.5, 40),         # magnetron
 (S['flip']+0.6,     (-0.9, -6.4, 1.6), (-0.8, 0, -0.35), 5.0, 38),           # wide: waves + molecules
 (S['heat']+0.4,     (0.25, -4.4, 0.9), (0.1, 0, 0.0), 4.0, 42),
 (S['spin']+0.3,     (0.85, -3.4, 3.3), (PLATE_C.x, PLATE_C.y - 0.35, PLATE_C.z - 0.3), 4.5, 36),   # high angle on the plate
 (S['metal']+0.2,    (1.25, -2.9, 0.5), (CUPW.x, CUPW.y, CUPW.z + 0.16), 2.8, 46),
 (S['origin']+0.3,   (-2.1, -3.4, 0.9), (-2.05, 0.1, -0.2), 3.2, 44),        # magnetron + chocolate
 (S['cta']-0.2,      (-0.4, -5.6, 1.4), (0.0, 0.2, -0.65), 4.5, 40),
 (S['cta']+2.4,      *HERO),
 (TOTAL,             *HERO),
]
# hold each beat's shot (with a slow push-in) until just before the next beat, then glide
_X = []
for i in range(len(SHOTS)-1):
    a, b = SHOTS[i], SHOTS[i+1]
    _X.append(a)
    if b[0] - a[0] > 1.6:
        _X.append((b[0]-0.45, a[1], a[2], a[3], a[4]*1.06))
_X.append(SHOTS[-1]); SHOTS = _X
def camera(t):
    for i in range(len(SHOTS)-1):
        a, b = SHOTS[i], SHOTS[i+1]
        if a[0] <= t <= b[0]:
            k = ss((t-a[0])/max(1e-6, b[0]-a[0]))
            cam.location = vlerp(a[1], b[1], k); tgt.location = vlerp(a[2], b[2], k)
            cd.dof.aperture_fstop = lerp(a[3], b[3], k); cd.lens = lerp(a[4], b[4], k); return
    cam.location = SHOTS[-1][1]; tgt.location = SHOTS[-1][2]

# ---------- story ----------
WX0, WX1 = -1.95, -0.55
def wave_pts(t, z, amp, lead=None, lam=0.55):
    pts = []; kx = 2*math.pi/lam
    for i in range(NP):
        x = WX0 + (WX1-WX0)*i/(NP-1)
        env = ss((x-WX0)/0.2) * (1 - ss((x-(WX1-0.15))/0.15))
        if lead is not None: env *= ss((lead-x)/0.3)
        pts.append((x, 0.0, z + amp*env*math.sin(kx*x - 2*math.pi*1.4*t)))
    return pts
def steam_pts(t, i, h):
    base = CUP.matrix_world @ Vector((-0.12 + i*0.12, 0, 0.56))
    return [(base.x + 0.05*math.sin(3*u + t*2.2 + i*2), base.y + 0.03*math.cos(2*u + t*1.7 + i), base.z + u*h) for u in [j/59 for j in range(60)]]

def update(t):
    camera(t)
    # turntable: still except during the spin beat
    spin = ramp(t, S['spin']+0.3, S['metal']-0.1)
    TT.rotation_euler = (0, 0, spin*2*math.pi)
    # cluster: big (mid-air) from mol to heat, tiny over the cup otherwise
    big = ramp(t, S['mol']+0.1, S['mol']+1.2) * (1 - ramp(t, S['spin']-0.2, S['spin']+0.6))
    loc = vlerp(CL_CUP[0], CL_BIG[0], big); scl = lerp(CL_CUP[1], CL_BIG[1], big)
    cupvis = 1 - ramp(t, S['spin']+0.6, S['spin']+1.0)          # tiny cluster hides when the plate starts spinning
    cupvis = max(cupvis, ramp(t, TOTAL-2.2, TOTAL-1.2)) if t > S['spin'] else 1.0
    if t > S['spin'] and big < 0.01: scl *= max(0.001, cupvis)
    CL.location = loc; CL.scale = Vector((1, 1, 1))*max(0.001, scl)
    # heat level 0..1 (glow + jitter)
    heat = 1 - ramp(t, S['mol']-0.2, S['mol']+0.8)                     # hook: hot
    heat = max(heat, ramp(t, S['heat']+0.2, S['heat']+2.0) * (1 - ramp(t, S['spin']+0.3, S['spin']+1.0)))
    heat = max(heat, ramp(t, TOTAL-2.4, TOTAL-0.6))                   # loop back into the hook
    # field drive (flip beat onward): molecules swing to follow the flipping field
    drive = ramp(t, S['flip']+0.3, S['flip']+1.0) * (1 - ramp(t, S['spin']-0.2, S['spin']+0.4))
    drive = max(drive, heat*0.7)
    fld = math.sin(2*math.pi*1.4*t)
    for i, m in enumerate(MOLS):
        calm = 0.25*math.sin(t*0.9 + m['ph'])
        jit = heat*0.07
        m['o'].location = m['home'] + Vector((jit*math.sin(t*23 + i*3.1), jit*math.cos(t*19 + i*1.7), jit*math.sin(t*29 + i)))
        rot = lerp(m['base'] + calm, math.radians(80)*fld + 0.25*m['base'], drive)
        m['o'].rotation_euler = Euler((0, rot, m['yaw']*(1-drive)), 'XYZ')
    O_B.inputs['Emission Strength'].default_value = 0.9*heat
    H_B.inputs['Emission Strength'].default_value = 0.35*heat
    CHAI_B.inputs['Emission Strength'].default_value = 0.6*heat
    # waves
    won = ramp(t, S['mag']+0.8, S['mag']+1.4) * (1 - ramp(t, S['spin']-0.3, S['spin']+0.3))
    won = max(won, 0.0)
    lead = lerp(WX0, WX1+0.4, ramp(t, S['mag']+0.8, S['mag']+3.0))
    for i, o in enumerate(WV):
        set_curve(o, wave_pts(t, -0.15 + i*0.4, 0.16, lead=lead), 0.024*max(won, 0.06), 1.8*won)
    SLOT_E.inputs[1].default_value = 6*max(won, ramp(t, S['mag']+0.1, S['mag']+0.8)*(1-ramp(t, S['spin']-0.3, S['spin']+0.3)),
                                         ramp(t, S['origin']+0.2, S['origin']+0.8)*(1-ramp(t, S['cta']+0.5, S['cta']+1.5))) * (0.8 + 0.2*math.sin(t*15))
    # steam
    st = max(heat, ramp(t, S['spin']+1.5, S['spin']+3.0)*(1-ramp(t, S['metal']-0.2, S['metal']+0.3)))
    for i, o in enumerate(STEAM):
        set_curve(o, steam_pts(t, i, 0.55 + 0.1*i), 0.02*max(st, 0.06), 0.9*st)
    # hot / cold spots
    sp = ramp(t, S['spin']-0.1, S['spin']+0.6) * (1 - ramp(t, S['metal']-0.3, S['metal']+0.2))
    HOT_E.inputs[1].default_value = 3.0*sp*(0.85 + 0.15*math.sin(t*6)); COLD_E.inputs[1].default_value = 2.0*sp
    for s, hot in SPOTS: s.hide_render = sp < 0.02
    # spoon + sparks
    sv = ramp(t, S['metal']-0.1, S['metal']+0.5) * (1 - ramp(t, S['origin']-0.4, S['origin']+0.1))
    SPOON.scale = Vector((1, 1, 1))*max(0.001, sv); SPOON.location = Vector((0.08, 0.02, 0.15)); SPOON.rotation_euler = (math.radians(-12), math.radians(14), 0)
    bpy.context.view_layer.update()
    tipw = SPOON.matrix_world @ SPOON_TIP
    fl = ramp(t, S['metal']+1.6, S['metal']+2.0) * (1 - ramp(t, S['metal']+3.8, S['metal']+4.3))
    rnd = random.Random(int(t*24))
    flick = fl * (0.4 + 0.6*rnd.random())
    for k, s in enumerate(SPARKS):
        a = k/len(SPARKS)*2*math.pi + rnd.uniform(-0.3, 0.3); el = rnd.uniform(-0.6, 0.9); ln = rnd.uniform(0.08, 0.26)*flick
        d = Vector((math.cos(a)*math.cos(el), math.sin(a)*math.cos(el), math.sin(el)))
        s.location = tipw + d*ln/2; s.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); s.scale = (1, 1, max(0.001, ln))
        s.hide_render = flick < 0.05 or rnd.random() < 0.25
    SPARK_E.inputs[1].default_value = 30*flick; SPARK_L.location = tipw; SPARK_L.data.energy = 60*flick
    # chocolate melts next to the magnetron
    cv = ramp(t, S['origin']+0.2, S['origin']+0.8) * (1 - ramp(t, S['cta']+0.6, S['cta']+1.4))
    CHOC.scale = Vector((1, 1, 1))*max(0.001, cv)
    melt = ramp(t, S['origin']+4.2, S['origin']+7.5)
    for q, home in CHOC_SQ:
        q.scale = (0.17*(1 + 0.25*melt), 0.13*(1 + 0.25*melt), 0.07*(1 - 0.65*melt))
        q.location = (home.x*(1 + 0.15*melt), home.y*(1 + 0.2*melt), home.z - 0.03*melt)
    CHOC_B.inputs['Roughness'].default_value = lerp(0.35, 0.08, melt)
    MAG.location = MAG_HOME + Vector((0, 0, 0.03*math.sin(t*1.1)))

if STILLS:
    for ts in STILLS.split(','):
        t = float(ts); update(t); sc.render.filepath = f'{OUT}/still_{t:05.2f}.jpg'
        bpy.ops.render.render(write_still=True)
else:
    f0 = int(opt('--f0', 1)); f1 = int(opt('--f1', NF)); step = int(opt('--step', 1))
    for f in range(f0, f1+1, step):
        p = f'{OUT}/f_{f:04d}.jpg'
        if os.path.exists(p): continue
        update((f-1)/FPS); sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
print('NF', NF)
