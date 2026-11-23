# Blender (bpy 5.x) scene: "How a touchscreen feels your finger" — S1 cinematic product-macro look (ep06–ep08 family).
# A glossy phone tilted back; its sensing grid lifts out above the glass (exploded view). Every crossing is a glowing node
# whose brightness = stored charge. A finger (then a glove, then a sausage) pulls charge away; a scan bar finds the dip.
# Procedural per frame: update(t). usage: WORK=/home/claude/ts python3 scene.py <out_dir> [--res 45] [--spp 6] [--thr 0.08] [--stills ..]
import bpy, bmesh, json, math, sys, os, random
from mathutils import Vector, Euler

A = sys.argv[1:]
OUT = A[0]; os.makedirs(OUT, exist_ok=True)
def opt(k, d): return A[A.index(k)+1] if k in A else d
RES = int(opt('--res', 45)); SPP = int(opt('--spp', 6)); STILLS = opt('--stills', '')
WORK = os.environ.get('WORK', '/home/claude/ts')
FPS = 24
VO = json.load(open(f'{WORK}/vo.json')); L = {l['key']: l for l in VO['lines']}
TOTAL = VO['total']; NF = int(math.ceil(TOTAL*FPS))
S = {k: L[k]['start'] for k in L}; E = {k: L[k]['end'] for k in L}

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, RES
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP
sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 1
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = float(opt('--thr', 0.08))
sc.render.use_persistent_data = True
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94

def ss(x): x = min(1, max(0, x)); return x*x*(3-2*x)
def ramp(t, a, b): return ss((t-a)/max(1e-6, b-a))
def lerp(a, b, k): return a + (b-a)*k
def vlerp(a, b, k): return Vector(a).lerp(Vector(b), k)

def principled(name, col, rough=0.4, coat=0.0, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if coat: b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.05
    return m, b
def emis(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0]); return m, e
def objcolor_emis(name, strength):
    # emission colour taken from each object's .color, so 100+ nodes share one material
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); oi = nt.nodes.new('ShaderNodeObjectInfo')
    e.inputs[1].default_value = strength; nt.links.new(oi.outputs['Color'], e.inputs[0]); nt.links.new(e.outputs[0], o.inputs[0]); return m

M_BODY, _ = principled('body', (0.025, 0.025, 0.03), 0.25, coat=1.0, metal=0.2)
M_FRAME, _ = principled('frame', (0.55, 0.56, 0.6), 0.22, metal=1.0)
M_SCREEN, _ = principled('screen', (0.004, 0.005, 0.008), 0.32, coat=0.25)
M_SKIN, _ = principled('skin', (0.78, 0.52, 0.40), 0.45)
M_NAIL, _ = principled('nail', (0.93, 0.74, 0.70), 0.18, coat=1.0)
M_GLOVE, _ = principled('glove', (0.08, 0.22, 0.75), 0.75)
M_SAUS, _ = principled('saus', (0.62, 0.20, 0.12), 0.32, coat=0.8)
M_FLOOR, _ = principled('floor', (0.03, 0.03, 0.034), 0.45)
M_SCOPE, _ = principled('scope', (0.01, 0.04, 0.02), 0.12, coat=1.0)
M_ROW, ROW_E = emis('row', (0.05, 0.6, 1.0), 1.4)
M_COL, COL_E = emis('col', (0.55, 0.15, 1.0), 1.4)
M_NODE = objcolor_emis('node', 7.0)
M_SPARK, SPARK_E = emis('spark', (1.0, 0.85, 0.35), 6.0)
M_RING, RING_E = emis('ring', (0.1, 1.0, 0.35), 0.0)
M_SCAN, SCAN_E = emis('scan', (1.0, 1.0, 1.0), 0.0)
M_SWEEP, SWEEP_E = emis('sweep', (0.2, 1.0, 0.35), 0.0)
M_BLIP, BLIP_E = emis('blip', (0.4, 1.0, 0.5), 0.0)

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

# ---------- phone (local: x across, y up the screen, z out of the screen) ----------
PHONE = empty('PHONE'); PHONE.location = (0, 0, -0.35); PHONE.rotation_euler = (math.radians(58), 0, 0)
PW, PH = 1.55, 3.15
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.06)); body = ob(bpy.context.object, M_FRAME, PHONE, False); body.scale = (PW, PH, 0.12)
bpy.ops.object.modifier_add(type='BEVEL'); body.modifiers[-1].width = 0.14; body.modifiers[-1].segments = 6
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.0)); scr = ob(bpy.context.object, M_SCREEN, PHONE, False); scr.scale = (PW-0.08, PH-0.08, 0.02)
bpy.ops.object.modifier_add(type='BEVEL'); scr.modifiers[-1].width = 0.12; scr.modifiers[-1].segments = 6
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.05, depth=0.01, location=(0, PH/2-0.16, 0.015)); ob(bpy.context.object, M_BODY, PHONE)

# sensing grid (lifts out of the screen)
GRID = empty('GRID', PHONE)
NX, NY = 7, 13
XS = [-0.6 + 1.2*i/(NX-1) for i in range(NX)]; YS = [-1.32 + 2.64*j/(NY-1) for j in range(NY)]
ROWS, COLS, NODES = [], [], {}
for j, y in enumerate(YS):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.009, depth=1.36, location=(0, y, 0), rotation=(0, math.radians(90), 0)); ROWS.append(ob(bpy.context.object, M_ROW, GRID))
for i, x in enumerate(XS):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.009, depth=2.84, location=(x, 0, 0.012), rotation=(math.radians(90), 0, 0)); COLS.append(ob(bpy.context.object, M_COL, GRID))
for i, x in enumerate(XS):
    for j, y in enumerate(YS):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.034, location=(x, y, 0.006)); NODES[(i, j)] = ob(bpy.context.object, M_NODE, GRID)
bpy.ops.mesh.primitive_torus_add(major_radius=0.11, minor_radius=0.012, location=(0, 0, 0.01)); RING = ob(bpy.context.object, M_RING, GRID)
bpy.ops.mesh.primitive_cube_add(size=1); SCAN = ob(bpy.context.object, M_SCAN, GRID, False); SCAN.scale = (1.42, 0.05, 0.004)

# charge particles flying from the grid into the touching object
PARTS = []
for k in range(20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.034); PARTS.append(ob(bpy.context.object, M_SPARK, PHONE))

# ---------- fingers / glove / sausage (built along +Z from the tip) ----------
def capsule(name, r, length, mat, nail=False, tie=False, cuff=None):
    root = empty(name, PHONE)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r, location=(0, 0, r)); ob(bpy.context.object, mat, root)
    bpy.ops.mesh.primitive_cone_add(vertices=40, radius1=r, radius2=r*1.13, depth=length, location=(0, 0, r + length/2)); ob(bpy.context.object, mat, root)
    if nail:
        for zz in (0.62, 1.25):
            bpy.ops.mesh.primitive_torus_add(major_radius=r*(1.0 + 0.13*zz/length), minor_radius=r*0.07, location=(0, 0, r + zz)); ob(bpy.context.object, mat, root)
    if nail:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=(0, r*0.82, r*1.7)); n = ob(bpy.context.object, M_NAIL, root); n.scale = (r*0.72, r*0.25, r*0.95)
    if tie:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=r*0.35, location=(0, 0, -r*0.05)); ob(bpy.context.object, M_SAUS, root)
    if cuff:
        bpy.ops.mesh.primitive_torus_add(major_radius=r*1.05, minor_radius=r*0.18, location=(0, 0, cuff)); ob(bpy.context.object, mat, root)
    root.scale = (0.001,)*3
    return root
FING = capsule('FING', 0.16, 2.0, M_SKIN, nail=True)
FING2 = capsule('FING2', 0.15, 2.0, M_SKIN, nail=True)
GLOVE = capsule('GLOVE', 0.18, 2.0, M_GLOVE, cuff=1.7)
SAUS = capsule('SAUS', 0.19, 1.5, M_SAUS, tie=True)
FDIR = Vector((0.45, -0.75, 1.0)).normalized()     # body leans toward the viewer's lower right
FDIR2 = Vector((-0.45, -0.75, 1.0)).normalized()

# ---------- 1965 radar scope (origin beat) ----------
SCOPE = empty('SCOPE'); SCOPE_HOME = Vector((3.2, 0.6, -0.35)); SCOPE.location = SCOPE_HOME; SCOPE.rotation_euler = (math.radians(70), 0, math.radians(-12))
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.95, depth=0.12, location=(0, 0, 0)); ob(bpy.context.object, M_SCOPE, SCOPE)
bpy.ops.mesh.primitive_torus_add(major_radius=0.98, minor_radius=0.07, location=(0, 0, 0.04)); ob(bpy.context.object, M_FRAME, SCOPE)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.12, depth=0.5, location=(0, 0, -0.3)); ob(bpy.context.object, M_BODY, SCOPE)
for r in (0.35, 0.65):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.006, location=(0, 0, 0.065)); ob(bpy.context.object, M_BLIP, SCOPE)
SWEEP = empty('SWEEP', SCOPE)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.45, 0, 0.068)); sw = ob(bpy.context.object, M_SWEEP, SWEEP, False); sw.scale = (0.9, 0.018, 0.004)
BLIPS = []
for (x, y) in [(0.4, 0.3), (-0.5, 0.2), (0.1, -0.6)]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.04, location=(x, y, 0.07)); BLIPS.append(ob(bpy.context.object, M_BLIP, SCOPE))

# ---------- floor, lights, world ----------
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -1.75)); ob(bpy.context.object, M_FLOOR, None, False)
def area(name, loc, rot, energy, size, col):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = size; ld.color = col
    o = bpy.data.objects.new(name, ld); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot; return o
area('key', (-2.8, -3.6, 3.8), (math.radians(45), math.radians(-30), math.radians(-25)), 480, 3.5, (1.0, 0.9, 0.8))
area('rim', (3.4, 3.2, 2.6), (math.radians(-60), math.radians(45), 0), 700, 2.0, (0.5, 0.7, 1.0))
area('fill', (2.2, -5.0, 2.0), (math.radians(70), math.radians(20), 0), 60, 4, (1, 0.95, 0.9))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.004, 0.005, 0.009, 1)

# ---------- camera ----------
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.lens = 40; cd.sensor_width = 36; cd.sensor_fit = 'HORIZONTAL'
cd.dof.use_dof = True; cd.dof.aperture_fstop = 3.0
tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt); cd.dof.focus_object = tgt
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
bpy.context.view_layer.update()
def P(x, y, z=0.0): return PHONE.matrix_world @ Vector((x, y, z))     # phone-local -> world
C = P(0, 0)
HERO = ((0.3, -4.9, 1.9), (C.x, C.y, C.z - 0.35), 4.0, 40)
SHOTS = [
 (0.0,               *HERO),
 (S['grid']+0.2,     (-0.4, -5.2, 2.6), (C.x, C.y, C.z - 0.3), 4.5, 40),
 (S['field']+0.1,    (0.6, -4.0, 1.6), (P(0.2, -0.3).x, P(0.2, -0.3).y, P(0.2, -0.3).z - 0.3), 2.8, 46),   # closer on nodes
 (S['touch']+0.2,    (1.2, -4.4, 1.4), (P(0.25, -0.2).x, P(0.25, -0.2).y, P(0.25, -0.2).z - 0.25), 3.0, 44),
 (S['scan']+0.2,     (0.0, -5.6, 2.4), (C.x, C.y, C.z - 0.35), 4.5, 40),
 (S['swipe']+0.2,    (-0.8, -5.0, 1.9), (C.x, C.y, C.z - 0.35), 4.0, 40),
 (S['glove']+0.2,    (0.9, -4.4, 1.7), (P(0, 0).x, P(0, 0).y, P(0, 0).z - 0.3), 3.2, 42),
 (S['origin']+0.2,   (2.6, -3.6, 1.0), (SCOPE_HOME.x, SCOPE_HOME.y, SCOPE_HOME.z - 0.25), 3.5, 42),
 (S['cta']-0.1,      (0.0, -6.0, 2.4), (C.x, C.y, C.z - 0.4), 4.5, 40),
 (S['cta']+2.4,      *HERO),
 (TOTAL,             *HERO),
]
_X = []
for i in range(len(SHOTS)-1):
    a, b = SHOTS[i], SHOTS[i+1]; _X.append(a)
    if b[0] - a[0] > 1.6: _X.append((b[0]-0.45, a[1], a[2], a[3], a[4]*1.06))
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
GZ = 0.32   # grid lift above the glass
def place(o, xy, hover, d, vis):
    # tip at grid height + hover, body along d
    o.location = Vector((xy[0], xy[1], GZ + 0.012 + hover)) - Vector((0, 0, 0))
    o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    o.scale = Vector((1, 1, 1))*max(0.001, vis)
def hover_of(t, a, b, far=2.4):     # approach at a, leave at b
    return far*(1 - ramp(t, a, a+0.8)) + far*ramp(t, b, b+0.7)

def update(t):
    camera(t)
    touches = []          # (x, y, strength) of conductive touches
    # --- primary finger
    fx, fy, fh, fv = 0.0, 0.25, 2.4, 0.0
    if t < S['grid']:
        fh = 2.0*(1 - ramp(t, 0.0, 0.55)) + 2.4*ramp(t, S['grid']-0.6, S['grid']+0.2); fv = 1
    elif S['touch'] <= t < S['glove']:
        fv = 1
        p0 = (0.3, -0.25)
        if t < S['swipe']:
            fx, fy = p0; fh = 2.4*(1 - ramp(t, S['touch']+1.4, S['touch']+3.2)) + 0.03*(1-ramp(t, S['touch']+3.2, S['touch']+3.4))
        else:
            k = ramp(t, S['swipe']+0.3, S['swipe']+1.6)
            fx, fy = lerp(p0[0], -0.3, k), lerp(p0[1], 0.75, k)
            # pinch: return to centre, then move apart
            kp = ramp(t, S['swipe']+1.9, S['swipe']+2.3)
            fx, fy = lerp(fx, 0.08, kp), lerp(fy, 0.1, kp)
            ka = ramp(t, S['swipe']+2.5, E['swipe']+0.2)
            fx, fy = fx + 0.32*ka, fy - 0.5*ka
            fh = 2.4*ramp(t, S['glove']-0.5, S['glove'])
    elif t >= S['cta']:
        fv = 1; fh = 2.4*(1 - ramp(t, TOTAL-1.6, TOTAL-0.5)); fx, fy = 0.0, 0.25
    place(FING, (fx, fy), fh, FDIR, fv)
    if fv: touches.append((fx, fy, 1 - ramp(fh, 0.02, 0.5)))
    # --- second finger for the pinch
    p2 = ramp(t, S['swipe']+1.9, S['swipe']+2.3) * (1 - ramp(t, S['glove']-0.6, S['glove']-0.1))
    if p2 > 0:
        ka = ramp(t, S['swipe']+2.5, E['swipe']+0.2)
        gx, gy = -0.08 - 0.32*ka, -0.1 + 0.5*ka; gh = 2.4*(1-p2)
        place(FING2, (gx, gy), gh, FDIR2, 1); touches.append((gx, gy, 1 - ramp(gh, 0.02, 0.5)))
    else: place(FING2, (0, 0), 3, FDIR2, 0)
    # --- glove then sausage
    g0 = S['glove']; gmid = g0 + 2.2
    if g0 - 0.3 <= t < gmid + 0.8:
        gh = hover_of(t, g0 + 0.1, gmid - 0.2); place(GLOVE, (0.0, 0.1), gh, FDIR, 1)
    else: place(GLOVE, (0, 0), 3, FDIR, 0)
    if gmid <= t < S['origin'] + 0.3:
        sh = hover_of(t, gmid + 0.2, S['origin'] - 0.4); place(SAUS, (0.0, 0.1), sh, Vector((0.6, -0.5, 1)).normalized(), 1)
        touches.append((0.0, 0.1, 1 - ramp(sh, 0.02, 0.5)))
    else: place(SAUS, (0, 0), 3, FDIR, 0)

    # --- grid draw-on during the "grid" beat (rows, then columns)
    gr = ramp(t, S['grid']+0.2, S['grid']+1.6); gc = ramp(t, S['grid']+2.4, S['grid']+3.6)
    if t < S['grid']: gr = gc = 1
    for j, o in enumerate(ROWS):
        k = ramp(gr, j/NY*0.7, j/NY*0.7 + 0.3); o.scale = (1, 1, max(0.001, k))
    for i, o in enumerate(COLS):
        k = ramp(gc, i/NX*0.7, i/NX*0.7 + 0.3); o.scale = (1, 1, max(0.001, k))
    # lift: grid rises out of the glass at the start of the grid beat
    lift = 1 if t < S['grid'] else ramp(t, S['grid']+0.0, S['grid']+1.0)
    GRID.location = (0, 0, GZ*lift)
    # --- node charge
    nodes_on = 1.0 if t < S['grid'] else ramp(t, S['grid']+3.4, S['field']+0.6)
    pulse = 0.5 + 0.5*math.sin(t*5)
    fieldglow = ramp(t, S['field'], S['field']+0.6)*(1 - ramp(t, S['touch'], S['touch']+0.8))
    # scan bar: sweeps the rows top->bottom twice during "scan"
    sk = (t - S['scan'] - 0.3)/2.0
    scanning = 0 <= sk < 2
    scan_y = YS[-1] - (YS[-1]-YS[0])*(sk % 1) if scanning else None
    SCAN_E.inputs[1].default_value = 2.5 if scanning else 0.0
    SCAN.location = (0, scan_y if scanning else 0, 0.03); SCAN.hide_render = not scanning
    best, bestv = None, 0
    for (i, j), o in NODES.items():
        x, y = XS[i], YS[j]
        dip = 0.0
        for (tx, ty, st) in touches:
            dip = max(dip, st*math.exp(-((x-tx)**2 + (y-ty)**2)/0.06))
        lvl = (0.55 + 0.12*pulse + 0.35*fieldglow)*nodes_on
        lvl *= (1 - 0.9*dip)
        col = tuple(lerp(c*lvl, o2, min(1, dip*1.1)) for c, o2 in zip((0.55, 0.85, 1.0), (0.35, 0.08, 0.0)))
        if dip > bestv: best, bestv = (x, y), dip
        if scanning and abs(y - scan_y) < 0.12:
            col = tuple(min(1, c + 0.35) if dip < 0.4 else c for c in col)
        o.color = (*col, 1)
        o.scale = (1, 1, 1)
    # detected ring (after the scan, while a touch is down)
    rk = ramp(t, S['scan']+2.6, S['scan']+3.0) * (1 - ramp(t, S['swipe']-0.2, S['swipe']+0.1))
    rk = max(rk, ramp(t, S['swipe']+0.2, S['swipe']+0.5)*(1-ramp(t, S['glove']-0.3, S['glove'])))
    rk = max(rk, ramp(t, S['glove']+2.9, S['glove']+3.3)*(1-ramp(t, S['origin']-0.5, S['origin'])))
    if best and bestv > 0.5 and rk > 0:
        RING.location = (best[0], best[1], 0.02); RING.scale = Vector((1, 1, 1))*(0.8 + 0.2*math.sin(t*10))*rk; RING_E.inputs[1].default_value = 6*rk
    else: RING.scale = (0.001,)*3; RING_E.inputs[1].default_value = 0
    # charge particles: stream from nodes near a touch up into the tip
    rnd = random.Random(3)
    act = [tc for tc in touches if tc[2] > 0.6]
    for k, pp in enumerate(PARTS):
        if not act: pp.scale = (0.001,)*3; continue
        tx, ty, st = act[k % len(act)]
        ang = rnd.uniform(0, 6.28); rad = rnd.uniform(0.15, 0.4); ph = (t*1.6 + rnd.random()) % 1
        sx, sy = tx + rad*math.cos(ang), ty + rad*math.sin(ang)
        pp.location = (lerp(sx, tx, ss(ph)), lerp(sy, ty, ss(ph)), GZ + 0.02 + 0.12*ph)
        pp.scale = Vector((1, 1, 1))*max(0.001, st*(1-ph)*1.2)
    # radar scope
    sv = ramp(t, S['origin']-0.2, S['origin']+0.5)*(1 - ramp(t, S['cta']+0.3, S['cta']+1.0))
    SCOPE.scale = Vector((1, 1, 1))*max(0.001, sv)
    SWEEP.rotation_euler = (0, 0, -t*2.2); SWEEP_E.inputs[1].default_value = 6*sv
    BLIP_E.inputs[1].default_value = 3*sv
    PHONE.location = Vector((0, 0, -0.35 + 0.025*math.sin(t*1.1)))

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
