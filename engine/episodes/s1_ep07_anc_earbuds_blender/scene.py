# Blender (bpy 5.x) scene: "How noise-cancelling earbuds work" — S1 cinematic product-macro look.
# Everything is procedural per frame (no keyframes): update(t) moves waves, earbud, engine, camera.
# usage: WORK=/home/claude/anc python3 scene.py <out_dir> [--res 50] [--spp 6] [--stills t1,t2] [--f0 1 --f1 N] [--step 1]
import bpy, bmesh, json, math, sys, os
from mathutils import Vector

A = sys.argv[1:]
OUT = A[0]; os.makedirs(OUT, exist_ok=True)
def opt(k, d): return A[A.index(k)+1] if k in A else d
RES = int(opt('--res', 50)); SPP = int(opt('--spp', 6)); STILLS = opt('--stills', '')
WORK = os.environ.get('WORK', '/home/claude/anc')
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
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.render.use_persistent_data = True
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94

# ---------- helpers ----------
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
    if emit: b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = estr
    return m, b
def emis(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0]); return m, e

M_BUD, _ = principled('bud', (0.90, 0.90, 0.88), 0.18, coat=1.0)
M_TIP, _ = principled('tip', (0.42, 0.43, 0.46), 0.75)
M_MESH, _ = principled('mesh', (0.02, 0.02, 0.025), 0.5, metal=0.6)
M_FLOOR, _ = principled('floor', (0.03, 0.03, 0.034), 0.45)
M_STEEL, _ = principled('steel', (0.6, 0.6, 0.63), 0.3, metal=1.0)
M_NAC, _ = principled('nac', (0.12, 0.125, 0.135), 0.42, metal=1.0)
M_BLADE, _ = principled('blade', (0.55, 0.56, 0.6), 0.25, metal=1.0)
M_DARK, _ = principled('dark', (0.05, 0.05, 0.06), 0.35, metal=0.8)
M_OMIC, OMIC_E = emis('omic', (1.0, 0.55, 0.12), 0.0)     # outer mic glow (amber)
M_IMIC, IMIC_E = emis('imic', (0.2, 0.85, 1.0), 0.0)      # inner mic / tip ring glow (cyan)
AMBER = (1.0, 0.32, 0.02); CYAN = (0.02, 0.55, 1.0); WHITE = (1.0, 1.0, 1.0); RED = (1.0, 0.05, 0.06); GREEN = (0.05, 1.0, 0.3); PINK = (1.0, 0.12, 0.6)
WAVE_MATS = {}
def wave_mat(name, col):
    m, e = emis('w_'+name, col, 1.6); WAVE_MATS[name] = e; return m

# ---------- waves (poly curves with round bevel) ----------
NP = 220
def make_wave(name, col, depth=0.028):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = depth; cu.bevel_resolution = 3; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(NP-1)
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o)
    cu.materials.append(wave_mat(name, col)); return o
def set_wave(o, pts, depth=None, strength=None, col=None):
    sp = o.data.splines[0]
    for i, p in enumerate(pts): sp.points[i].co = (p[0], p[1], p[2], 1)
    if depth is not None: o.data.bevel_depth = depth
    e = WAVE_MATS[o.name]
    if strength is not None: e.inputs[1].default_value = strength
    if col is not None: e.inputs[0].default_value = (*col, 1)
    o.hide_render = (strength is not None and strength <= 0.01) or (depth is not None and depth <= 0.002)

WA = make_wave('A', AMBER)    # outside noise
WC = make_wave('C', CYAN)     # anti-noise
WR = make_wave('R', WHITE)    # the sum (what reaches your ear)
WH = make_wave('H', PINK, 0.022)   # high, sharp sound (voices)

# ---------- earbud ----------
def ob(o, mat=None, parent=None, smooth=True):
    if mat: o.data.materials.append(mat)
    if parent: o.parent = parent
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    return o
BUD = bpy.data.objects.new('BUD', None); sc.collection.objects.link(BUD)
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1, location=(0, 0, 0)); body = ob(bpy.context.object, M_BUD, BUD)
body.scale = (0.46, 0.40, 0.44)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.13, depth=1.0, location=(0.02, 0.05, -0.62)); stem = ob(bpy.context.object, M_BUD, BUD)
stem.rotation_euler = (math.radians(8), math.radians(-6), 0)
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.135, location=(0.07, 0.12, -1.11)); ob(bpy.context.object, M_BUD, BUD)
# silicone ear tip (points +x, slightly into depth)
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=(0.48, 0.10, 0.06)); tip = ob(bpy.context.object, M_TIP, BUD)
tip.scale = (0.17, 0.25, 0.25)
bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.022, location=(0.62, 0.10, 0.06), rotation=(0, math.radians(90), 0)); ob(bpy.context.object, M_IMIC, BUD)
# outer mic (faces -x, toward the incoming sound) + mesh grille
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.085, depth=0.03, location=(-0.455, 0, 0.10), rotation=(0, math.radians(90), 0)); ob(bpy.context.object, M_MESH, BUD)
bpy.ops.mesh.primitive_torus_add(major_radius=0.10, minor_radius=0.014, location=(-0.465, 0, 0.10), rotation=(0, math.radians(90), 0)); ob(bpy.context.object, M_OMIC, BUD)
# tiny chip visible through a "window" is overkill: a gold chip floats out during the flip beat
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); chip = ob(bpy.context.object, None, None, False)
M_CHIP, CHIP_B = principled('chip', (0.03, 0.03, 0.035), 0.3, emit=CYAN, estr=0.0)
chip.data.materials.append(M_CHIP); chip.scale = (0.30, 0.30, 0.05)
bpy.ops.object.modifier_add(type='BEVEL'); chip.modifiers[-1].width = 0.02; chip.modifiers[-1].segments = 2
pins = []
for side in range(4):
    for k in range(5):
        bpy.ops.mesh.primitive_cube_add(size=1); p = bpy.context.object; p.data.materials.append(M_STEEL)
        off = (k-2)*0.11
        p.location = [(off, 0.62, 0), (off, -0.62, 0), (0.62, off, 0), (-0.62, off, 0)][side]
        p.scale = (0.05/0.30, 0.16/0.30, 0.4) if side < 2 else (0.16/0.30, 0.05/0.30, 0.4)
        p.parent = chip; pins.append(p)
BUD_HOME = Vector((1.15, 0, 0.35))

# ---------- jet engine (the "engine hum") ----------
ENG = bpy.data.objects.new('ENG', None); sc.collection.objects.link(ENG)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.75, depth=1.4, location=(0, 0, 0), rotation=(0, math.radians(90), 0)); nac = ob(bpy.context.object, M_NAC, ENG)
bpy.ops.object.modifier_add(type='SOLIDIFY'); nac.modifiers[-1].thickness = 0.06
# remove caps so it's a hollow ring
me = nac.data; bm = bmesh.new(); bm.from_mesh(me)
caps = [f for f in bm.faces if len(f.verts) > 4]; bmesh.ops.delete(bm, geom=caps, context='FACES'); bm.to_mesh(me); bm.free()
FAN = bpy.data.objects.new('FAN', None); sc.collection.objects.link(FAN); FAN.parent = ENG
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(0.15, 0, 0)); ob(bpy.context.object, M_DARK, FAN)
for k in range(14):
    a = k/14*2*math.pi
    bpy.ops.mesh.primitive_cube_add(size=1); bl = ob(bpy.context.object, M_BLADE, FAN, False)
    bl.scale = (0.04, 0.12, 0.62); bl.location = (0.1, math.cos(a)*0.38, math.sin(a)*0.38)
    bl.rotation_euler = (a + math.pi/2, math.radians(28), 0)
ENG_HOME = Vector((-3.05, 0.6, 0.35))

# ---------- floor, lights, world ----------
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -1.3)); ob(bpy.context.object, M_FLOOR, None, False)
def area(name, loc, rot, energy, size, col):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = size; ld.color = col
    o = bpy.data.objects.new(name, ld); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot; return o
area('key', (-2.5, -4.0, 3.6), (math.radians(50), math.radians(-25), math.radians(-20)), 520, 3.5, (1.0, 0.9, 0.8))
area('rim', (3.6, 3.5, 2.2), (math.radians(-60), math.radians(45), 0), 600, 2.0, (0.55, 0.72, 1.0))
area('fill', (2.0, -5.0, 3.0), (math.radians(55), math.radians(20), 0), 60, 4, (1, 0.95, 0.9))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.005, 0.006, 0.009, 1)

# ---------- camera ----------
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.lens = 40; cd.sensor_width = 36; cd.sensor_fit = 'HORIZONTAL'
cd.dof.use_dof = True; cd.dof.aperture_fstop = 3.0
tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt); cd.dof.focus_object = tgt
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'

# shots: (time, cam pos, target, fstop, lens). The frame centre sits ~0.9 above the subject so the
# lower third (captions) stays over empty floor.
HERO = ((0.0, -6.6, 1.0), (-0.3, 0, -0.35), 4.5, 40)
SHOTS = [
 (0.0,               *HERO),
 (S['mic']-0.3,      (0.1, -6.0, 1.1), (-0.3, 0, -0.5), 4.5, 44),
 (S['mic']+1.4,      (-2.6, -4.6, 0.9), (-1.30, 0.2, -0.45), 3.2, 40),     # engine + wave arriving
 (S['mic']+3.6,      (-0.6, -2.9, 0.9), (0.4, 0, -0.25), 2.4, 46),       # outer mic close-up
 (S['flip']+0.6,     (-0.6, -6.6, 1.4), (-0.60, 0, -0.75), 4.5, 39),      # wide for the flip
 (S['cancel']+1.0,   (-0.2, -6.2, 1.6), (-0.60, 0, -0.55), 4.5, 39),
 (S['fast']+0.4,     (1.8, -6.0, 2.0), (-0.30, 0, -0.75), 4.5, 39),
 (S['inside']+0.2,   (3.4, -3.4, 1.6), (1.9, 0.1, -0.2), 2.6, 44),       # ear-tip side
 (S['low']+0.4,      (0.6, -6.6, 1.5), (-0.40, 0, -0.65), 4.5, 39),
 (S['origin']+0.2,   (0.4, -7.4, 2.6), (-0.60, 0, -0.8), 5.0, 40),
 (S['cta']-0.2,      (-1.4, -6.8, 2.4), (-0.30, 0, -0.7), 5.0, 40),
 (S['cta']+2.0,      *HERO),
 (TOTAL,             *HERO),
]
def camera(t):
    for i in range(len(SHOTS)-1):
        a, b = SHOTS[i], SHOTS[i+1]
        if a[0] <= t <= b[0]:
            k = ss((t-a[0])/max(1e-6, b[0]-a[0]))
            cam.location = vlerp(a[1], b[1], k); tgt.location = vlerp(a[2], b[2], k)
            cd.dof.aperture_fstop = lerp(a[3], b[3], k); cd.lens = lerp(a[4], b[4], k); return
    cam.location = SHOTS[-1][1]; tgt.location = SHOTS[-1][2]

# ---------- the story ----------
X0, X1 = -2.45, 0.62       # waves run from the engine to the outer mic
LAMBDA = 0.95; AMP = 0.36
def wave_pts(t, z0, amp, phase=0.0, flip_theta=0.0, lam=LAMBDA, x0=X0, x1=X1, lead=None, y=0.0, jag=0.0, tail_block=None):
    pts = []; kx = 2*math.pi/lam; speed = 1.1
    for i in range(NP):
        x = x0 + (x1-x0)*i/(NP-1)
        env = 1.0
        if lead is not None: env *= ss((lead - x)/0.35)                  # leading edge (wave arriving)
        if tail_block is not None: env *= 1 - ss((x - tail_block)/0.12)  # blocked by the ear tip
        env *= ss((x - x0)/0.25)                                          # soft start at the engine
        v = math.sin(kx*x - speed*kx*t + phase)
        if jag: v = 0.55*v + 0.45*math.sin(3.7*kx*x - 3.7*speed*kx*t)
        a = amp*env*v
        pts.append((x, y + a*math.sin(flip_theta), z0 + a*math.cos(flip_theta)))
    return pts

def update(t):
    camera(t)
    # earbud: gentle float + slow turn; engine fan spins
    BUD.location = BUD_HOME + Vector((0, 0, 0.04*math.sin(t*1.3)))
    turn = 0.0
    if t > S['origin']: turn = ramp(t, S['origin']+0.2, S['cta']+0.6)*2*math.pi
    BUD.rotation_euler = (0, 0, math.radians(-14) + 0.06*math.sin(t*0.7) + turn)
    ENG.location = ENG_HOME
    eng_in = ramp(t, S['mic']-0.2, S['mic']+0.8) * (1 - ramp(t, S['inside']-0.3, S['inside']+0.3)) + \
             ramp(t, S['low']-0.2, S['low']+0.5) * (1 - ramp(t, S['cta']+1.0, S['cta']+1.8))
    ENG.scale = Vector((1, 1, 1))*max(0.001, eng_in)
    FAN.rotation_euler = (t*14.0, 0, 0)

    zA = 0.35; mic = OMIC_E.inputs[1]; inner = IMIC_E.inputs[1]
    mic.default_value = 0.0; inner.default_value = 0.6
    chip.scale = Vector((0.001, 0.001, 0.001)); CHIP_B.inputs['Emission Strength'].default_value = 0.0
    a_amp, c_amp, r_amp = AMP, AMP, 0.0
    A_on = C_on = R_on = H_on = 0.0
    zC = zA; thC = 0.0; phC = 0.0; zR = zA; rcol = WHITE; lead = None
    if t < S['mic']:
        # HOOK (payoff first): amber + cyan slide together and flatten into silence
        k = ramp(t, 0.35, 1.8)
        A_on = C_on = 1.0; zA_ = lerp(zA+0.75, zA, k); zC = lerp(zA-0.75, zA, k); thC = math.pi
        a_amp = c_amp = AMP*(1 - ramp(t, 1.5, 2.3))
        R_on = ramp(t, 1.6, 2.2); r_amp = 0.0; zR = zA
        inner.default_value = 0.6 + 5*ramp(t, 1.8, 2.3)
        wa = wave_pts(t, zA_, a_amp); wc = wave_pts(t, zC, c_amp, flip_theta=thC); wr = wave_pts(t, zR, 0)
    elif t < S['flip']:
        # MIC: noise wave flows out of the engine into the outer mic
        lead = lerp(X0, X1+0.4, ramp(t, S['mic']+0.3, S['mic']+2.6))
        A_on = 1.0; mic.default_value = 7*ramp(t, S['mic']+2.2, S['mic']+2.7)*(0.75+0.25*math.sin(t*12))
        wa = wave_pts(t, zA, AMP, lead=lead); wc = wa; wr = wa
    elif t < S['cancel']:
        # FLIP: a cyan copy rises out, the chip pops up, and the copy flips 180 degrees
        A_on = 1.0; C_on = ramp(t, S['flip']+0.2, S['flip']+0.6); mic.default_value = 4.0
        zC = zA - 0.95*ramp(t, S['flip']+0.3, S['flip']+1.2)
        thC = math.pi*ramp(t, S['flip']+1.6, S['flip']+3.0)
        ck = ramp(t, S['flip']+0.2, S['flip']+0.8)*(1-ramp(t, S['cancel']-0.4, S['cancel']))
        chip.scale = Vector((0.55, 0.55, 0.09))*max(0.001, ck)
        chip.location = BUD.location + Vector((-0.95, -0.45, 0.8)); chip.rotation_euler = (math.radians(60), 0, t*0.8)
        CHIP_B.inputs['Emission Strength'].default_value = 2.5*(0.5+0.5*math.sin(t*10))
        wa = wave_pts(t, zA, AMP); wc = wave_pts(t, zC, AMP, flip_theta=thC); wr = wa
    elif t < S['fast']:
        # CANCEL: cyan slides up onto amber; both flatten into one white line = silence
        A_on = C_on = 1.0; thC = math.pi; mic.default_value = 4.0
        k = ramp(t, S['cancel']+0.3, S['cancel']+1.6)
        zC = lerp(zA-0.95, zA, k)
        f = ramp(t, S['cancel']+1.6, S['cancel']+2.6)
        a_amp = c_amp = AMP*(1-f); R_on = f; zR = zA
        inner.default_value = 0.6 + 6*f
        wa = wave_pts(t, zA, a_amp); wc = wave_pts(t, zC, c_amp, flip_theta=thC); wr = wave_pts(t, zR, 0)
    elif t < S['inside']:
        # FAST: stacked view; when the anti-wave is late, the sum (red) wobbles; on time it goes flat (green)
        A_on = C_on = R_on = ramp(t, S['fast'], S['fast']+0.5); thC = math.pi; mic.default_value = 4.0
        zAa = zA + 0.85; zC = zA; zR = zA - 0.85
        lag = 1.3*(ramp(t, S['fast']+0.6, S['fast']+1.3) - ramp(t, S['fast']+3.0, S['fast']+3.8))
        wa = wave_pts(t, zAa, AMP); wc = wave_pts(t, zC, AMP, flip_theta=thC, phase=lag)
        # sum of the two: sin(x) - sin(x+lag)
        wr = []
        for (x, _, za), (_, _, zc) in zip(wa, wc):
            wr.append((x, 0, zR + (za - zAa) + (zc - zC)))
        rcol = tuple(lerp(g, r, min(1, lag/0.6)) for g, r in zip(GREEN, RED))
    elif t < S['low']:
        # INSIDE: tiny leftover wobble between the tip and the ear canal gets fixed by the inner mic
        R_on = 1.0; inner.default_value = 3 + 4*(0.5+0.5*math.sin(t*9))
        res = 0.12*(1 - ramp(t, S['inside']+1.4, S['inside']+2.6))
        wr = wave_pts(t, BUD_HOME.z+0.06, res, lam=0.35, x0=BUD_HOME.x+0.62, x1=BUD_HOME.x+2.6, y=0.1)
        rcol = tuple(lerp(g, r, min(1, res/0.12)) for g, r in zip(GREEN, RED))
        wa = wc = wr
    elif t < S['origin']:
        # LOW vs HIGH: the low hum is cancelled; the sharp high sound is stopped by the ear tip
        A_on = 1.0; H_on = 1.0; C_on = ramp(t, S['low']+0.6, S['low']+1.2); thC = math.pi; mic.default_value = 4
        f = ramp(t, S['low']+1.4, S['low']+2.4)
        wa = wave_pts(t, zA+0.55, AMP*(1-f), lam=1.4); wc = wave_pts(t, zA+0.55, AMP*(1-f), lam=1.4, flip_theta=thC)
        hl = lerp(X0, BUD_HOME.x+0.5, ramp(t, S['low']+2.0, S['low']+4.2))
        wh = wave_pts(t, zA-0.45, 0.22, lam=0.6, jag=1, lead=hl, x1=BUD_HOME.x+0.7, tail_block=BUD_HOME.x+0.35)
        R_on = f; wr = wave_pts(t, zA+0.55, 0, lam=1.4)
        set_wave(WH, wh, depth=0.022, strength=1.6*H_on)
    else:
        # ORIGIN + CTA: earbud turns, then everything resets to the hook's start (loop)
        R_on = 1 - ramp(t, S['cta']+1.6, S['cta']+2.4)
        A_on = C_on = ramp(t, TOTAL-1.6, TOTAL-0.9); thC = math.pi
        k = 1 - ramp(t, TOTAL-1.2, TOTAL-0.05)
        inner.default_value = 4*R_on + 0.6
        wa = wave_pts(t, lerp(zA+0.75, zA, k), AMP*(1-k)); wc = wave_pts(t, lerp(zA-0.75, zA, k), AMP*(1-k), flip_theta=thC); wr = wave_pts(t, zA, 0)
    if not (S['low'] <= t < S['origin']): set_wave(WH, wave_pts(t, 0, 0), depth=0.001, strength=0)
    set_wave(WA, wa, depth=0.03*max(A_on, 0.06), strength=1.6*A_on)
    set_wave(WC, wc, depth=0.03*max(C_on, 0.06), strength=1.6*C_on)
    set_wave(WR, wr, depth=0.032*max(R_on, 0.06), strength=2.2*R_on, col=rcol)

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
