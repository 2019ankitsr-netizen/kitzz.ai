# S2 AI Ki Kahani · ep04 "Tara sochti kaise hai?" — claymation stop-motion (12 fps, clay "boil", thumbprint bumps).
import sys; sys.path.insert(0, '/home/claude/bk')
import bpy, bmesh, math, json, random
from mathutils import Vector
from blib import *
AR = args(); OUT = AR['out']; FPS = 12
VO = json.load(open('/home/claude/s2/vo.json')); LN = VO['lines']; S = {l['key']: l['start'] for l in LN}; E = {l['key']: l['end'] for l in LN}; T = VO['total']
sc = setup(int(AR.get('res', 50)), int(AR.get('spp', 8)), FPS, T, view='AgX - Medium High Contrast')
def K(o, p, t, v, i=None): key(o, p, t, v, FPS, i)
world((0.95, 0.85, 0.75), 0.25)

# ---------- clay material with per-frame "boil" ----------
BOIL = []
def clay(name, col, rough=0.62, bump=0.35):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    pass
    tc = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.noise_dimensions = '4D'
    n.inputs['Scale'].default_value = 9.0; n.inputs['Detail'].default_value = 4
    nt.links.new(tc.outputs['Object'], n.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.02
    nt.links.new(n.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    BOIL.append(n.inputs['W']); return m
C_SKIN = clay('skin', (0.72, 0.45, 0.3)); C_HAIR = clay('hair', (0.06, 0.04, 0.03)); C_SHIRT = clay('shirt', (0.95, 0.55, 0.1))
C_EYEW = clay('eyew', (0.95, 0.94, 0.9), 0.4, 0.1); C_PUP = clay('pup', (0.03, 0.03, 0.03), 0.3, 0.05)
C_ROBO = clay('robo', (0.45, 0.78, 0.82)); C_SCREEN = clay('screen', (0.06, 0.08, 0.12), 0.3, 0.05)
C_DESK = clay('desk', (0.55, 0.32, 0.18), 0.7, 0.5); C_WALL = clay('wall', (0.96, 0.78, 0.55), 0.8, 0.25)
C_CUP = clay('cup', (0.92, 0.9, 0.85)); C_CHAI = clay('chai', (0.55, 0.32, 0.15), 0.3, 0.1); C_BISC = clay('bisc', (0.85, 0.6, 0.25), 0.7, 0.8)
C_TILE = clay('tile', (0.98, 0.95, 0.86), 0.6, 0.2); C_BAR1 = clay('bar1', (0.25, 0.7, 0.35)); C_BAR2 = clay('bar2', (0.95, 0.6, 0.2)); C_BAR3 = clay('bar3', (0.85, 0.3, 0.3))
C_RED = clay('red', (0.85, 0.15, 0.12)); C_FRAME = clay('frame', (0.35, 0.2, 0.1))
M_EYE, EYE_E = emission('tara_eye', (0.4, 1.0, 0.95), 4.0)
M_Q, Q_E = emission('q', (1.0, 0.85, 0.4), 0.0)

def blob(kind, m, parent=None, ss=2, **kw):
    o = prim(kind, m, parent, **kw); subsurf(o, ss); return o

# ---------- set: desk + wall ----------
desk = mesh_obj('desk', bevel_box('dk', 18, 14, 0.4, 0.15, 4), C_DESK, (0, -3.8, -0.4)); subsurf(desk, 1)
wall = mesh_obj('wall', bevel_box('wl', 22, 0.4, 16, 0.2, 3), C_WALL, (0, 3.2, -0.5)); subsurf(wall, 1)
# chai + biscuit
cup = blob('cylinder', C_CUP, None, vertices=24, radius=0.32, depth=0.55, location=(2.6, 0.2, 0.28))
blob('cylinder', C_CHAI, None, vertices=24, radius=0.27, depth=0.05, location=(2.6, 0.2, 0.54))
hdl = blob('torus', C_CUP, None, major_radius=0.16, minor_radius=0.05, location=(2.95, 0.2, 0.3)); hdl.rotation_euler = (math.pi/2, 0, 0)
bisc = blob('cylinder', C_BISC, None, vertices=24, radius=0.28, depth=0.07, location=(2.1, -0.4, 0.04))

# ---------- Bablu (clay boy) ----------
bab = empty('bablu', (-2.2, 0.4, 0))
blob('cylinder', C_SHIRT, bab, vertices=24, radius=0.55, depth=1.1, location=(0, 0, 0.55))
bhead = empty('bhead', (0, 0, 1.55)); bhead.parent = bab
blob('uv_sphere', C_SKIN, bhead, radius=0.62, location=(0, 0, 0), segments=32, ring_count=16)
hair = blob('uv_sphere', C_HAIR, bhead, radius=0.66, location=(0, 0.06, 0.2), segments=32, ring_count=16); hair.scale = (1.03, 1.03, 0.72)
for x in (-0.22, 0.22):
    blob('uv_sphere', C_EYEW, bhead, radius=0.13, location=(x, -0.54, 0.08), segments=16, ring_count=8)
    blob('uv_sphere', C_PUP, bhead, radius=0.06, location=(x+0.03, -0.65, 0.07), segments=12, ring_count=6)
mouth = blob('uv_sphere', C_PUP, bhead, radius=0.12, location=(0, -0.58, -0.22), segments=16, ring_count=8); mouth.scale = (1.1, 0.4, 0.25)
blob('uv_sphere', C_SKIN, bhead, radius=0.09, location=(0, -0.62, -0.04), segments=12, ring_count=6)   # nose
bab.rotation_euler = (0, 0, math.radians(-18))
# ---------- Tara (clay robot) ----------
tara = empty('tara', (0.4, 0.6, 0))
tbody = mesh_obj('tbody', bevel_box('tb', 1.0, 0.8, 0.9, 0.25, 4), C_ROBO, (0, 0, 0), tara)
thead = empty('thead', (0, 0, 1.45)); thead.parent = tara
mesh_obj('th', bevel_box('thm', 1.5, 1.0, 1.05, 0.35, 5), C_ROBO, (0, 0, -0.5), thead)
mesh_obj('tsc', bevel_box('tsm', 1.15, 0.1, 0.7, 0.18, 4), C_SCREEN, (0, -0.47, -0.32), thead)
eyes = []
for x in (-0.25, 0.25):
    e = prim('uv_sphere', M_EYE, thead, radius=0.11, location=(x, -0.54, 0.05), segments=16, ring_count=8); e.scale = (1, 0.4, 1.3); eyes.append(e)
blob('cylinder', C_ROBO, thead, vertices=12, radius=0.04, depth=0.45, location=(0, 0, 0.75))
ant = blob('uv_sphere', C_RED, thead, radius=0.1, location=(0, 0, 1.0), segments=16, ring_count=8)
tara.rotation_euler = (0, 0, math.radians(14))

# ---------- word tiles (Latin text) ----------
FONT = bpy.data.fonts.load('/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf')
def tile(word, loc, w=None, mat=C_TILE, size=0.38):
    root = empty('tile_'+word, loc); w = w or 0.32 + 0.25*len(word)
    mesh_obj('tb_'+word, bevel_box('tbm_'+word, w, 0.35, 0.7, 0.12, 3), mat, (0, 0, 0), root)
    bpy.ops.object.text_add(location=(0, -0.19, 0.35)); tx = bpy.context.object; tx.data.body = word; tx.data.font = FONT
    tx.data.align_x = 'CENTER'; tx.data.align_y = 'CENTER'; tx.data.size = size; tx.data.extrude = 0.02; tx.rotation_euler = (math.pi/2, 0, 0)
    tx.data.materials.append(C_PUP); tx.parent = root
    root.scale = (0.001,)*3; return root
words = [tile('chai', (-1.9, -1.0, 2.9)), tile('ke', (-0.75, -1.0, 2.9)), tile('saath', (0.55, -1.0, 2.9))]
cand = [('biscuit', 62, C_BAR1), ('samosa', 21, C_BAR2), ('pakode', 9, C_BAR3)]
bars = []
for i, (wd, pct, m) in enumerate(cand):
    t_ = tile(wd, (-1.6, -1.2, 1.75 - i*0.62), 1.9, size=0.32)
    bar = mesh_obj('bar%d' % i, bevel_box('bm%d' % i, 1.0, 0.3, 0.42, 0.1, 3), m, (0, 0, 0)); bar.location = (-0.6, -1.2, 1.89 - i*0.62)
    bars.append((t_, bar, pct))
next_tile = tile('biscuit', (1.95, -1.0, 2.9), mat=clay('tile_g', (0.6, 0.92, 0.6), 0.6, 0.2))
chain = [tile(w, (-2.2 + i*1.45, -1.0, 3.9), size=0.34) for i, w in enumerate(['ek', 'shabd', 'phir', 'agla'])]
wrong = tile('galat?', (0.4, -1.4, 3.2), 2.1, clay('tile_r', (0.98, 0.6, 0.55), 0.6, 0.2))
# photo frame for the cliffhanger
frame = empty('frame', (0.4, -0.6, 2.4))
mesh_obj('fr', bevel_box('frm', 1.9, 0.2, 2.3, 0.12, 3), C_FRAME, (0, 0, -1.15), frame)
mesh_obj('fq', bevel_box('fqm', 1.5, 0.05, 1.9, 0.05, 2), M_Q, (0, -0.12, -1.15), frame)
bpy.ops.object.text_add(location=(0, -0.17, -0.05)); q = bpy.context.object; q.data.body = '?'; q.data.font = FONT; q.data.align_x = 'CENTER'; q.data.align_y = 'CENTER'
q.data.size = 1.2; q.data.extrude = 0.05; q.rotation_euler = (math.pi/2, 0, 0); q.data.materials.append(C_PUP); q.parent = frame
frame.scale = (0.001,)*3

# ---------- lights ----------
key_l = area('key', (-4, -5, 6), (0, 0, 0), 900, 4, (1.0, 0.9, 0.78)); point_at(key_l, (0, 0.5, 1.2))
rim = area('rim', (4, 3, 4), (0, 0, 0), 400, 3, (0.7, 0.85, 1.0)); point_at(rim, (0, 0, 1))
fill = area('fill', (5, -4, 2), (0, 0, 0), 150, 4, (1, 0.9, 0.85)); point_at(fill, (0, 0, 1))

# ---------- camera ----------
cam, cd, tgt = camera(38, 4.0)
def shot(t0, t1, c0, c1, g0, g1, lens=38):
    for t_, c, g in ((t0, c0, g0), (t1-0.002, c1, g1)):
        K(cam, 'location', t_, Vector(c)); K(tgt, 'location', t_, Vector(g)); cd.lens = lens; cd.keyframe_insert('lens', frame=F(t_, FPS))
WIDE = ((0.0, -9.5, 2.8), (0.0, 0.4, 1.7))
shot(0, S['t1']-0.1, (-0.3, -7.2, 2.4), (-0.1, -6.6, 2.3), (-0.6, 0.4, 1.6), (-0.6, 0.4, 1.6), 36)                    # two-shot
shot(S['t1']-0.1, S['b1']-0.05, (1.2, -4.2, 2.2), (1.0, -3.9, 2.2), (0.4, 0.6, 1.5), (0.4, 0.6, 1.5), 45)                # Tara close
shot(S['b1']-0.05, S['chai']-0.05, (-3.0, -4.0, 2.2), (-2.9, -3.7, 2.2), (-2.2, 0.4, 1.6), (-2.2, 0.4, 1.6), 45)          # Bablu close
shot(S['chai']-0.05, S['chain']-0.05, (0.0, -8.6, 2.9), (0.0, -8.0, 2.8), (0.0, -0.6, 2.2), (0.0, -0.6, 2.3), 48)        # tiles + bars
shot(S['chain']-0.05, S['b3']-0.05, (0.0, -9.0, 3.4), (0.3, -8.6, 3.4), (-0.2, -0.6, 3.0), (0.0, -0.6, 3.0), 46)          # chain
shot(S['b3']-0.05, S['t3']-0.05, (-3.0, -4.0, 2.2), (-2.9, -3.7, 2.2), (-2.2, 0.4, 1.6), (-2.2, 0.4, 1.6), 45)            # Bablu
shot(S['t3']-0.05, S['cliff']-0.2, (1.4, -5.2, 2.6), (1.1, -4.7, 2.6), (0.4, 0.0, 2.0), (0.4, 0.0, 2.2), 42)              # Tara + galat
shot(S['cliff']-0.2, S['cta']-0.05, (0.4, -7.5, 2.0), (0.4, -5.2, 1.6), (0.4, -0.6, 1.4), (0.4, -0.6, 1.4), 40)           # frame push-in
shot(S['cta']-0.05, T+0.1, (-0.1, -6.6, 2.3), (-0.3, -7.2, 2.4), (-0.6, 0.4, 1.6), (-0.6, 0.4, 1.6), 36)                 # back to two-shot (loop)

# ---------- animation ----------
def pop(o, t, s=1.0): K(o, 'scale', t-0.01, Vector((0.001,)*3)); K(o, 'scale', t+0.25, Vector((s*1.15,)*3)); K(o, 'scale', t+0.42, Vector((s,)*3))
def hide(o, t): K(o, 'scale', t-0.01, Vector(o.scale)); K(o, 'scale', t+0.2, Vector((0.001,)*3))
# talking: Bablu mouth flaps / Tara eyes pulse + head bob, by line speaker
for l in LN:
    if l.get('who') == 'BABLU':
        n = int((l['end']-l['start'])/0.17)
        for k in range(n+1): K(mouth, 'scale', l['start'] + k*0.17, Vector((1.1, 0.4, 0.25 if k % 2 == 0 else 0.85)))
        K(mouth, 'scale', l['end']+0.05, Vector((1.1, 0.4, 0.25)))
        K(bhead, 'rotation_euler', l['start'], Vector((0, 0, 0))); K(bhead, 'rotation_euler', l['start']+0.4, Vector((math.radians(-8), math.radians(6), 0))); K(bhead, 'rotation_euler', l['end'], Vector((0, 0, 0)))
    if l.get('who') == 'TARA':
        n = int((l['end']-l['start'])/0.2)
        for k in range(n+1):
            for e in eyes: K(e, 'scale', l['start'] + k*0.2, Vector((1, 0.4, 1.3 if k % 2 == 0 else 0.6)))
        for e in eyes: K(e, 'scale', l['end']+0.05, Vector((1, 0.4, 1.3)))
        K(thead, 'rotation_euler', l['start'], Vector((0, 0, 0))); K(thead, 'rotation_euler', l['start']+0.5, Vector((0, math.radians(-6), math.radians(-8)))); K(thead, 'rotation_euler', l['end'], Vector((0, 0, 0)))
# blinks for Bablu
for t_ in (2.0, 7.5, 15.0, 23.0, 30.0, 37.0, 44.0):
    pass
# tiles: chai ke saath
for i, w_ in enumerate(words): pop(w_, S['chai'] + 0.6 + i*0.55)
for i, (t_, bar, pct) in enumerate(bars):
    pop(t_, E['chai'] + 0.1 + i*0.2)
    K(bar, 'scale', E['chai'] + 0.3 + i*0.2, Vector((0.001, 1, 1)))
    K(bar, 'scale', E['chai'] + 1.3 + i*0.2, Vector((pct/62*2.3, 1, 1)))
    K(bar, 'location', E['chai'] + 0.3 + i*0.2, Vector((-0.6, -1.2, 1.89 - i*0.62)))
    K(bar, 'location', E['chai'] + 1.3 + i*0.2, Vector((-0.6 + pct/62*2.3/2, -1.2, 1.89 - i*0.62)))
pop(next_tile, S['b2'] + 0.05)
for i, (t_, bar, pct) in enumerate(bars): hide(t_, S['chain'] - 0.3); hide(bar, S['chain'] - 0.3)
for w_ in words + [next_tile]: hide(w_, S['b3'] - 0.2)
for i, c in enumerate(chain): pop(c, S['chain'] + 0.4 + i*0.8)
for c in chain: hide(c, S['b3'] - 0.2)
pop(wrong, S['t3'] + 0.5, 1.0)
for k in range(8): K(wrong, 'rotation_euler', S['t3'] + 1.0 + k*0.25, Vector((0, math.radians(8 if k % 2 else -8), 0)))
hide(wrong, S['cliff'] - 0.3)
pop(frame, S['cliff'] + 1.2, 1.0)
keyv(Q_E.inputs[1], S['cliff'] + 1.2, 0.0, FPS); keyv(Q_E.inputs[1], S['cliff'] + 3.0, 3.0, FPS); keyv(Q_E.inputs[1], S['cta'] + 0.5, 3.0, FPS)
hide(frame, S['cta'] + 0.4)
# antenna bob + idle sway
for k in range(int(T/1.5)):
    K(ant, 'location', k*1.5, Vector((0, 0, 1.0 + (0.05 if k % 2 else 0))))
    K(bab, 'rotation_euler', k*1.5, Vector((0, 0, math.radians(-18 + (3 if k % 2 else -3)))))

# ---------- stop-motion: clay boil (W changes every 2nd frame) + camera micro jitter ----------
rnd = random.Random(2); nf = int(math.ceil(T*FPS))
for f in range(1, nf+2, 2):
    for w in BOIL: w.default_value = rnd.uniform(0, 100); w.keyframe_insert('default_value', frame=f)
smooth_all()
for ob in (cam, tgt): set_constant(ob)
for fc in all_fcurves(cd): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
for ob in (cam, tgt):
    for fc in all_fcurves(ob):
        kps = fc.keyframe_points
        for i in range(0, len(kps), 2): kps[i].interpolation = 'LINEAR'
for m in bpy.data.materials:
    if m.node_tree:
        for fc in all_fcurves(m.node_tree):
            if 'W' in fc.data_path or 'inputs[4]' in fc.data_path or fc.data_path.endswith('default_value'):
                pass
for m in [x for x in bpy.data.materials if x.node_tree]:
    for fc in all_fcurves(m.node_tree):
        if any(kp.co[0] == 3 for kp in fc.keyframe_points) and len(fc.keyframe_points) > 100:
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
# mouth / eyes snap (stop-motion replacement mouths)
for ob in [mouth] + eyes:
    for fc in all_fcurves(ob): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/s2/s2.blend')
render(OUT, AR, FPS, T)
