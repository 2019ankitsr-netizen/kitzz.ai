# Blender (bpy 5.x) scene: "How a torn QR code still works" — cinematic macro look.
# usage: python3 scene.py <out_dir> [f0 f1] [--res 50] [--spp 8] [--stills t1,t2]
import bpy, bmesh, json, math, random, sys, os
from mathutils import Vector
import qrcode

A = sys.argv[1:]
OUT = A[0]; os.makedirs(OUT, exist_ok=True)
def opt(k, d):
    return A[A.index(k)+1] if k in A else d
RES = int(opt('--res', 50)); SPP = int(opt('--spp', 8)); STILLS = opt('--stills', '')
FPS = 24
VO = json.load(open('/home/claude/qr/vo.json')); L = {l['key']: l for l in VO['lines']}
TOTAL = VO['total']; NF = int(math.ceil(TOTAL*FPS))
def F(t): return t*FPS + 1
S = {k: L[k]['start'] for k in L}

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = NF
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, RES
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP
sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
sc.render.use_persistent_data = True
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94

# ---------- materials ----------
def principled(name, col, rough=0.4, coat=0.0, metal=0.0, objcol_emit=None, objcol_mix=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if coat: b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.08
    if objcol_emit or objcol_mix:
        oi = nt.nodes.new('ShaderNodeObjectInfo'); sep = nt.nodes.new('ShaderNodeSeparateColor')
        nt.links.new(oi.outputs['Color'], sep.inputs[0])
        if objcol_mix:   # R channel mixes base colour to objcol_mix
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'
            mx.inputs['A'].default_value = (*col, 1); mx.inputs['B'].default_value = (*objcol_mix, 1)
            nt.links.new(sep.outputs['Red'], mx.inputs['Factor']); nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
        if objcol_emit:  # G channel = emission strength of objcol_emit, B channel = green glow
            b.inputs['Emission Color'].default_value = (*objcol_emit, 1)
            mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.inputs[1].default_value = 6.0
            nt.links.new(sep.outputs['Green'], mul.inputs[0]); nt.links.new(mul.outputs[0], b.inputs['Emission Strength'])
    return m
M_BLACK = principled('black', (0.012, 0.013, 0.016), 0.22, coat=1.0, objcol_emit=(1.0, 0.45, 0.08), objcol_mix=(0.95, 0.42, 0.06))
M_WHITE = principled('white', (0.86, 0.85, 0.82), 0.38, objcol_emit=(0.15, 1.0, 0.45), objcol_mix=(0.86, 0.85, 0.82))
M_FLOOR = principled('floor', (0.035, 0.033, 0.035), 0.55)
M_ALU = principled('alu', (0.18, 0.19, 0.21), 0.28, metal=1.0)
M_STEEL = principled('steel', (0.62, 0.62, 0.64), 0.32, metal=1.0)
def emis(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0]); return m, e
M_BEAM, BEAM_E = emis('beam', (1.0, 0.12, 0.1), 0.0)
# phone screen: mix of two image emissions
M_SCR = bpy.data.materials.new('screen'); M_SCR.use_nodes = True; nt = M_SCR.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)
o = nt.nodes.new('ShaderNodeOutputMaterial'); mixs = nt.nodes.new('ShaderNodeMixShader')
tc = nt.nodes.new('ShaderNodeTexCoord')
for i, p in enumerate(['screen_scan.png', 'screen_paid.png']):
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load('/home/claude/qr/'+p)
    nt.links.new(tc.outputs['UV'], t.inputs[0])
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs[1].default_value = 1.6
    nt.links.new(t.outputs[0], e.inputs[0]); nt.links.new(e.outputs[0], mixs.inputs[1+i])
nt.links.new(mixs.outputs[0], o.inputs[0]); SCR_MIX = mixs.inputs[0]

# ---------- meshes ----------
def bevel_box(name, sx, sy, sz, w=0.012, seg=3):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x*sx, v.co.y*sy, v.co.z*sz + sz/2))
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=w, segments=seg, affect='EDGES', profile=0.5)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me
C = 0.1
ME_TILE = bevel_box('tile', C*0.93, C*0.93, 0.03, 0.01, 2)
ME_CUBE = bevel_box('cube', C*0.93, C*0.93, 0.085, 0.014, 3)

def obj(name, me, mat, loc=(0, 0, 0)):
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o)
    if mat and not me.materials: me.materials.append(mat)
    o.location = loc; return o

def key(o, path, t, val, idx=None, interp='BEZIER'):
    if idx is None:
        setattr(o, path, val); o.keyframe_insert(path, frame=F(t))
    else:
        getattr(o, path)[idx] = val; o.keyframe_insert(path, index=idx, frame=F(t))

# ---------- the QR code ----------
qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, border=2)
qr.add_data('kitzz.ai'); qr.make(fit=False)
MAT = qr.get_matrix(); N = len(MAT)   # 29 with border
mid = (N-1)/2
def is_finder(i, j):
    b = 2; ii, jj = i-b, j-b; n = N-2*b
    return (ii < 7 and jj < 7) or (ii < 7 and jj >= n-7) or (ii >= n-7 and jj < 7)
random.seed(4)
# torn corner region (bottom-right), ragged edge
def torn(i, j):
    u = (i + j) - (N-1)*1.28 + random.Random(i*131+j).uniform(-1.6, 1.6)
    return u > 0
# 30% region (a diagonal slab through the middle-right), avoiding finders
def slab(i, j):
    return (j - i*0.45) > 12.5 and not is_finder(i, j)

BOARD = bpy.data.objects.new('board', None); sc.collection.objects.link(BOARD)
cells = []
for i in range(N):
    for j in range(N):
        black = MAT[i][j]
        o = obj(f'c{i}_{j}', ME_CUBE if black else ME_TILE, M_BLACK if black else M_WHITE)
        o.data.materials.clear() if False else None
        o.location = ((j-mid)*C, (mid-i)*C, 0)
        o.color = (0, 0, 0, 1); o.parent = BOARD
        cells.append(dict(o=o, i=i, j=j, black=black, finder=is_finder(i, j) and black, torn=torn(i, j),
                          slab=slab(i, j), ecc=black and not is_finder(i, j) and random.random() < 0.62,
                          home=Vector(o.location)))
# floor
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.001)); fl = bpy.context.object; fl.data.materials.append(M_FLOOR)

# ---------- phone ----------
ME_PH = bevel_box('phone', 0.78, 1.62, 0.07, 0.06, 6)
phone = obj('phone', ME_PH, M_ALU)
for bx, by in [(-0.22, 0.6), (-0.22, 0.38)]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.085, depth=0.03, location=(bx, by, 0.08)); lb = bpy.context.object
    lb.data.materials.append(M_BLACK); lb.parent = phone
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.035, depth=0.01, location=(0.0, 0.62, 0.075)); fl_ = bpy.context.object; fl_.data.materials.append(M_WHITE); fl_.parent = phone
bpy.ops.mesh.primitive_plane_add(size=1); scr = bpy.context.object; scr.scale = (0.72, 1.52, 1)
scr.data.materials.append(M_SCR); scr.parent = phone; scr.location = (0, 0, -0.002); scr.rotation_euler = (math.pi, 0, 0)
# screen faces down toward the code; image would mirror -> flip U
for lp in scr.data.uv_layers.active.data: lp.uv = (1-lp.uv[0], lp.uv[1])
bpy.ops.mesh.primitive_plane_add(size=1); beam = bpy.context.object; beam.scale = (3.2, 0.012, 1)
beam.data.materials.append(M_BEAM); beam.location = (0, 1.5, 0.12)

# ---------- gear (car part) ----------
gear = bpy.data.objects.new('gear', None); sc.collection.objects.link(gear)
bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=3.2, depth=0.5, location=(0, 0, -0.255)); g0 = bpy.context.object
bpy.ops.object.shade_smooth(); g0.data.materials.append(M_STEEL); g0.parent = gear
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.7, depth=0.6, location=(0, 0, -0.32)); hub = bpy.context.object
hub.data.materials.append(M_ALU); hub.parent = gear
for k in range(34):
    a = k/34*2*math.pi
    tooth = obj(f'tooth{k}', bevel_box(f'tme{k}', 0.42, 0.55, 0.5, 0.05, 2), M_STEEL, (math.cos(a)*3.38, math.sin(a)*3.38, -0.505))
    tooth.rotation_euler = (0, 0, a + math.pi/2); tooth.parent = gear
gear.location = (0, 0, -0.6); gear.scale = (1, 1, 1)

# ---------- lights ----------
def area(name, loc, rot, energy, size, col):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = size; ld.color = col
    o = bpy.data.objects.new(name, ld); sc.collection.objects.link(o); o.location = loc; o.rotation_euler = rot; return o
key_l = area('key', (-3.2, 2.2, 4.2), (math.radians(-35), math.radians(-38), 0), 650, 3.5, (1.0, 0.9, 0.8))
rim_l = area('rim', (3.5, 4.0, 1.4), (math.radians(-72), math.radians(40), 0), 520, 2.0, (0.55, 0.7, 1.0))
fill_l = area('fill', (2.5, -4, 2.5), (math.radians(55), math.radians(25), 0), 90, 4, (1, 0.95, 0.9))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.006, 0.007, 0.01, 1)

# ---------- camera ----------
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.lens = 40; cd.sensor_width = 36; cd.sensor_fit = 'HORIZONTAL'
cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2
tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt); cd.dof.focus_object = tgt
tc_ = cam.constraints.new('TRACK_TO'); tc_.target = tgt; tc_.track_axis = 'TRACK_NEGATIVE_Z'; tc_.up_axis = 'UP_Y'
def shot(t, cpos, tpos, fstop=None, lens=None):
    key(cam, 'location', t, Vector(cpos)); key(tgt, 'location', t, Vector(tpos))
    if fstop: cd.dof.aperture_fstop = fstop; cd.dof.keyframe_insert('aperture_fstop', frame=F(t))
    if lens: cd.lens = lens; cd.keyframe_insert('lens', frame=F(t))

E = 0.0
# HOOK: hero, slightly tilted, phone above; push in
shot(0.0, (0.9, -4.6, 4.7), (0.05, 0.0, 0.0), 4.0, 40)
shot(S['finder']-0.2, (0.55, -3.9, 3.9), (0.15, -0.1, 0.0), 4.0, 40)
# FINDER: low orbit to top-left finder, then sweep to see all three
shot(S['finder']+1.6, (-2.6, -2.2, 1.35), (-0.85, 0.85, 0.15), 2.0, 45)
shot(S['finder']+4.2, (2.7, -2.6, 1.9), (0.0, 0.25, 0.12), 2.4, 40)
# BITS: macro slide along the surface
shot(S['bits'], (1.6, -1.6, 0.75), (0.4, 0.0, 0.05), 1.6, 55)
shot(S['backup']-0.2, (-1.2, -1.75, 0.8), (-0.2, 0.2, 0.05), 1.6, 55)
# BACKUP: rise to 3/4 view
shot(S['backup']+1.2, (0.4, -3.4, 3.0), (0.0, 0.0, 0.0), 3.2, 40)
# RS: rebuild of torn corner, camera close to corner
shot(S['rs']+0.4, (2.9, -2.9, 2.2), (0.85, -0.85, 0.05), 2.2, 45)
shot(S['thirty']-0.3, (0.1, -0.9, 5.6), (0.0, 0.0, 0.0), 5.6, 38)
# THIRTY: top-down
shot(S['thirty']+2.5, (0.05, -0.6, 5.2), (0.0, 0.05, 0.0), 5.6, 38)
# ORIGIN: pull back, gear rises
shot(S['origin']+0.6, (0.0, -7.8, 5.6), (0.0, 0.0, -0.3), 5.0, 40)
shot(S['cta']-0.4, (-1.6, -7.0, 4.4), (0.0, 0.2, -0.3), 5.0, 40)
# CTA: back to hero (matches hook for the loop)
shot(S['cta']+1.6, (0.9, -4.7, 4.8), (0.05, 0.0, 0.0), 4.0, 40)
shot(TOTAL, (0.9, -4.6, 4.7), (0.05, 0.0, 0.0), 4.0, 40)

# ---------- phone + beam + screen ----------
key(phone, 'location', 0.0, Vector((0.2, 0.1, 1.25))); key(phone, 'rotation_euler', 0.0, Vector((math.radians(-8), math.radians(4), math.radians(12))))
key(phone, 'location', 2.6, Vector((0.2, 0.05, 1.3)))
key(phone, 'location', S['finder']+0.9, Vector((-6.0, -2.0, 6.0)))
key(phone, 'location', S['cta']+0.8, Vector((-6.0, -2.0, 6.0)))
key(phone, 'location', S['cta']+2.2, Vector((0.2, 0.1, 1.25)))
key(phone, 'location', TOTAL, Vector((0.2, 0.1, 1.25)))
key(beam, 'location', 0.05, Vector((0, 1.5, 0.12))); key(beam, 'location', 1.15, Vector((0, -1.45, 0.12)))
BEAM_E.inputs[1].default_value = 0; BEAM_E.inputs[1].keyframe_insert('default_value', frame=F(0.0))
BEAM_E.inputs[1].default_value = 25; BEAM_E.inputs[1].keyframe_insert('default_value', frame=F(0.1))
BEAM_E.inputs[1].keyframe_insert('default_value', frame=F(1.1))
BEAM_E.inputs[1].default_value = 0; BEAM_E.inputs[1].keyframe_insert('default_value', frame=F(1.25))
for t, v in [(0, 0), (1.15, 0), (1.35, 1), (S['finder']+1.0, 1), (S['finder']+1.1, 0), (S['cta']+1.9, 0), (S['cta']+2.3, 1), (TOTAL, 1)]:
    SCR_MIX.default_value = v; SCR_MIX.keyframe_insert('default_value', frame=F(t))

# ---------- per-cell animation ----------
rng = random.Random(9)
def scatter(c):
    a = rng.uniform(0, 2*math.pi); r = rng.uniform(1.2, 2.6)
    return c['home'] + Vector((math.cos(a)*r*0.6 + 0.9, math.sin(a)*r*0.6 - 0.9, rng.uniform(0.6, 1.8)))
for c in cells:
    o, h = c['o'], c['home']
    col = lambda t, r=0.0, g=0.0: key(o, 'color', t, (r, g, 0, 1))
    if c['torn']:
        off = scatter(c); off.z = -0.6   # hidden below the floor while torn
        key(o, 'location', 0.0, off); key(o, 'scale', 0.0, Vector((0.001,)*3))
        # rebuild during RS
        d = S['rs'] + 1.2 + rng.uniform(0, 1.6)
        fly = scatter(c)
        key(o, 'location', d-0.05, fly); key(o, 'scale', d-0.05, Vector((0.001,)*3))
        key(o, 'scale', d, Vector((1, 1, 1))); key(o, 'location', d+0.75, h)
        col(d+0.7, 0, 0); col(d+0.85, 0, 0.9 if not c['black'] else 0.5); col(d+1.6, 0, 0)
        # tear again at the very end (loop)
        e = TOTAL - 1.3 + rng.uniform(0, 0.5)
        key(o, 'location', e, h); key(o, 'scale', e, Vector((1, 1, 1)))
        key(o, 'location', e+0.45, h + Vector((0.3, -0.3, -0.5))); key(o, 'scale', e+0.45, Vector((0.001,)*3))
    else:
        key(o, 'location', 0.0, h)
    # FINDER: rise + saffron glow
    if c['finder']:
        d = S['finder'] + 0.9 + (0 if c['j'] < 12 and c['i'] < 12 else 0.35 if c['i'] < 12 else 0.7)
        key(o, 'location', d-0.01, h); key(o, 'location', d+0.4, h + Vector((0, 0, 0.32)))
        col(d-0.01); col(d+0.35, 0, 0.55)
        key(o, 'location', S['bits']+0.2, h + Vector((0, 0, 0.32))); key(o, 'location', S['bits']+0.9, h)
        col(S['bits']+0.2, 0, 0.55); col(S['bits']+0.9, 0, 0)
    # BITS: travelling wave bounce
    if not c['torn']:
        d = S['bits'] + 0.9 + (c['i'] + c['j'])*0.045
        key(o, 'location', d, h); key(o, 'location', d+0.18, h + Vector((0, 0, 0.12))); key(o, 'location', d+0.42, h)
    # BACKUP: ECC blocks turn amber
    if c['ecc']:
        d = S['backup'] + 1.0 + rng.uniform(0, 0.9)
        col(d, 0, 0); col(d+0.3, 1.0, 0.12)
        col(S['origin']+0.5, 1.0, 0.12); col(S['origin']+1.3, 0, 0)
    # THIRTY: slab lifts away and floats, then returns
    if c['slab']:
        d = S['thirty'] + 0.5 + (c['j']-12)*0.03
        key(o, 'location', d, h); key(o, 'location', d+0.9, h + Vector((0.55, 0.15, 0.9)))
        key(o, 'location', S['origin']-0.1, h + Vector((0.62, 0.18, 1.0))); key(o, 'location', S['origin']+0.6, h)
    if not c['slab'] and not c['torn'] and not c['black']:
        # the remaining code glows green = still readable
        col(S['thirty']+1.6, 0, 0); col(S['thirty']+2.0, 0, 0.35); col(S['origin']-0.1, 0, 0.35); col(S['origin']+0.4, 0, 0)

# ORIGIN: the gear rises from below, the code sits on it like a sticker
key(gear, 'location', S['origin']-0.2, Vector((0, 0, -0.6)))
key(gear, 'location', S['origin']+0.3, Vector((0, 0, 0.0)))
key(gear, 'location', S['origin']+1.0, Vector((0, 0, 0.55)))
key(BOARD, 'location', S['origin']+0.3, Vector((0, 0, 0)))
key(BOARD, 'location', S['origin']+1.0, Vector((0, 0, 0.55)))
key(BOARD, 'location', S['cta']+0.2, Vector((0, 0, 0.55)))
key(BOARD, 'location', S['cta']+0.9, Vector((0, 0, 0)))
key(BOARD, 'rotation_euler', S['origin']-0.2, Vector((0, 0, 0))); key(BOARD, 'rotation_euler', S['cta']+0.2, Vector((0, 0, math.radians(40)))); key(BOARD, 'rotation_euler', S['cta']+1.4, Vector((0, 0, 0)))
key(gear, 'rotation_euler', S['origin']-0.2, Vector((0, 0, 0))); key(gear, 'rotation_euler', S['cta']+0.2, Vector((0, 0, math.radians(40))))
key(gear, 'location', S['cta']+0.2, Vector((0, 0, 0.55))); key(gear, 'location', S['cta']+0.9, Vector((0, 0, 0.0))); key(gear, 'location', S['cta']+1.4, Vector((0, 0, -0.6)))

# smooth all keyframes
for ob in bpy.data.objects:
    ad = ob.animation_data
    if ad and ad.action:
        try:
            fcs = ad.action.fcurves
        except AttributeError:
            fcs = [fc for layer in ad.action.layers for strip in layer.strips for cb in strip.channelbags for fc in cb.fcurves]
        for fc in fcs:
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'; kp.easing = 'AUTO'
                kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'

bpy.ops.wm.save_as_mainfile(filepath='/home/claude/qr/qr.blend')
if STILLS:
    for t in STILLS.split(','):
        sc.frame_set(int(F(float(t)))); sc.render.filepath = f'{OUT}/still_{float(t):05.2f}.jpg'
        bpy.ops.render.render(write_still=True)
else:
    f0 = int(opt('--f0', 1)); f1 = int(opt('--f1', NF))
    sc.frame_start, sc.frame_end = f0, f1
    sc.render.filepath = f'{OUT}/f_'
    bpy.ops.render.render(animation=True)
print('NF', NF)
