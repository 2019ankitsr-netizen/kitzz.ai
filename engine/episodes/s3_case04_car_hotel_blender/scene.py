# S3 CCTV Riddles · case 04 "Pushed his car to a hotel" — miniature night street set seen through CCTV (12 fps, grain added in post).
import sys; sys.path.insert(0, '/home/claude/bk')
import bpy, bmesh, math, json, random
from mathutils import Vector
from blib import *
AR = args(); OUT = AR['out']; FPS = 12
VO = json.load(open('/home/claude/s3/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; T = VO['total']
sc = setup(int(AR.get('res', 50)), int(AR.get('spp', 8)), FPS, T, view='AgX - Base Contrast')
def K(o, p, t, v, i=None): key(o, p, t, v, FPS, i)
world((0.02, 0.025, 0.04), 1.0)

# ---------- set ----------
M_ASP = mat('asphalt', (0.05, 0.05, 0.055), 0.75)
M_PAVE = mat('pave', (0.22, 0.22, 0.21), 0.8)
M_LINE = mat('line', (0.85, 0.8, 0.55), 0.6)
M_RED = mat('hotelred', (0.62, 0.05, 0.05), 0.45, coat=0.3)
M_GRN = mat('housegreen', (0.06, 0.38, 0.12), 0.45, coat=0.3)
M_WIN, WIN_E = emission('win', (1.0, 0.78, 0.45), 3.0)
M_ROOF = mat('roof', (0.12, 0.1, 0.1), 0.6)
M_CAR = mat('car', (0.08, 0.22, 0.55), 0.25, coat=1.0)
M_TYRE = mat('tyre', (0.02, 0.02, 0.02), 0.7)
M_GLASS = mat('glass', (0.05, 0.07, 0.09), 0.1, coat=1.0)
M_SKIN = mat('skin', (0.62, 0.42, 0.3), 0.6)
M_SHIRT = mat('shirt', (0.75, 0.72, 0.62), 0.6)
M_SUIT = mat('suit', (0.12, 0.12, 0.14), 0.6)
M_POLE = mat('pole', (0.3, 0.3, 0.32), 0.4, metal=1.0)
M_LAMP, LAMP_E = emission('lamp', (1.0, 0.62, 0.25), 18.0)
M_SIGN, SIGN_E = emission('sign', (1.0, 0.92, 0.85), 6.0)
M_TABLE = mat('table', (0.3, 0.17, 0.08), 0.5)

prim('plane', M_TABLE, None, size=120, location=(0, 0, -0.16))
M_BOARD = mat('board', (0.72, 0.8, 0.66), 0.6)
mesh_obj('board', bevel_box('bdm', 25, 25, 0.1, 0.03, 2), M_BOARD, (0, 0, -0.1))
road = prim('plane', M_ASP, None, size=1, location=(0, 0, 0)); road.scale = (24, 3.2, 1)
for side in (-1, 1):
    pv = mesh_obj('pave%d' % side, bevel_box('pv%d' % side, 24, 2.2, 0.12, 0.02, 2), M_PAVE, (0, side*2.7, 0))
for i in range(-7, 8):
    d = prim('plane', M_LINE, None, size=1, location=(i*1.6, 0, 0.002)); d.scale = (0.7, 0.07, 1)
# hotel (red block, lit windows, sign)
hotel = empty('hotel', (0.4, 5.0, 0.12))
mesh_obj('hbody', bevel_box('hb', 4.4, 2.6, 3.2, 0.06, 3), M_RED, (0, 0, 0), hotel)
mesh_obj('hroof', bevel_box('hr', 4.7, 2.9, 0.25, 0.05, 2), M_ROOF, (0, 0, 3.2), hotel)
for r in range(3):
    for c in range(4):
        if r == 0 and c in (1, 2): continue
        w_ = mesh_obj('w%d%d' % (r, c), bevel_box('wb', 0.55, 0.06, 0.55, 0.01, 1), M_WIN, (-1.5+c*1.0, -1.31, 0.5+r*0.95), hotel)
door = mesh_obj('door', bevel_box('db', 1.1, 0.08, 1.2, 0.02, 1), M_WIN, (0, -1.32, 0.0), hotel)
bpy.ops.object.text_add(location=(0, -1.36, 2.95)); sign = bpy.context.object; sign.data.body = 'HOTEL'; sign.data.align_x = 'CENTER'
sign.data.size = 0.55; sign.data.extrude = 0.03; sign.rotation_euler = (math.pi/2, 0, 0); sign.data.materials.append(M_SIGN); sign.parent = hotel
# green houses along the street
rnd = random.Random(3)
def house(name, loc, s=1.0, m=M_GRN):
    h = empty(name, loc); h.scale = (s,)*3
    mesh_obj(name+'b', bevel_box(name+'bm', 1.2, 1.2, 0.9, 0.05, 2), m, (0, 0, 0), h)
    me = bpy.data.meshes.new(name+'r'); bm = bmesh.new()
    v = [bm.verts.new(p) for p in [(-0.66, -0.66, 0.9), (0.66, -0.66, 0.9), (0.66, 0.66, 0.9), (-0.66, 0.66, 0.9), (0, -0.66, 1.5), (0, 0.66, 1.5)]]
    for f in [(0, 1, 4), (2, 3, 5), (0, 4, 5, 3), (1, 2, 5, 4)]: bm.faces.new([v[i] for i in f])
    bm.to_mesh(me); bm.free(); mesh_obj(name+'rf', me, m, (0, 0, 0), h)
    mesh_obj(name+'w', bevel_box(name+'wm', 0.35, 0.04, 0.32, 0.01, 1), M_WIN, (0.2, -0.61, 0.35), h)
    return h
for i, x in enumerate([-9, -7.2, -5.4, 6.0, 7.8, 9.6]):
    house('h%d' % i, (x, 4.6, 0.12), 1.1)
for i, x in enumerate([-8, -5.5, -3, 3.5, 6.2, 8.8]):
    house('s%d' % i, (x, -4.6, 0.12), 1.1).rotation_euler = (0, 0, math.pi)
# street lamps
def lamp(x, y):
    mesh_obj('pole', bevel_box('pl', 0.08, 0.08, 2.8, 0.01, 1), M_POLE, (x, y, 0.12))
    prim('uv_sphere', M_LAMP, None, radius=0.16, location=(x, y - 0.0, 2.95), segments=16, ring_count=8)
    pl = bpy.data.lights.new('pl', 'POINT'); pl.energy = 260; pl.color = (1.0, 0.62, 0.3); pl.shadow_soft_size = 0.2
    o = bpy.data.objects.new('pl', pl); link(o); o.location = (x, y, 2.8)
for x, y in [(-4.2, 2.0), (3.6, 2.0), (-0.6, -2.0), (8, -2.0), (-9, 2.0)]: lamp(x, y)
moon = bpy.data.lights.new('moon', 'SUN'); moon.energy = 0.25; moon.color = (0.55, 0.65, 1.0); mo = bpy.data.objects.new('moon', moon); link(mo); mo.rotation_euler = (0.7, 0.3, 0.6)

# ---------- toy car ----------
car = empty('car', (-11, -0.9, 0))
mesh_obj('cbody', bevel_box('cb', 1.6, 0.75, 0.38, 0.12, 4), M_CAR, (0, 0, 0.14), car)
mesh_obj('ctop', bevel_box('ct', 0.85, 0.66, 0.3, 0.1, 3), M_GLASS, (-0.08, 0, 0.5), car)
for x in (-0.5, 0.5):
    for y in (-0.38, 0.38):
        w = prim('cylinder', M_TYRE, car, vertices=24, radius=0.16, depth=0.12, location=(x, y, 0.16)); w.rotation_euler = (math.pi/2, 0, 0)
hl = prim('uv_sphere', M_LAMP, car, radius=0.05, location=(0.8, 0.25, 0.32), segments=12, ring_count=6)
prim('uv_sphere', M_LAMP, car, radius=0.05, location=(0.8, -0.25, 0.32), segments=12, ring_count=6)
# ---------- people (simple figurines) ----------
def person(name, loc, top=M_SHIRT, s=1.0):
    p = empty(name, loc); p.scale = (s,)*3
    prim('cylinder', M_SUIT, p, vertices=16, radius=0.07, depth=0.5, location=(0.0, -0.06, 0.25))
    prim('cylinder', M_SUIT, p, vertices=16, radius=0.07, depth=0.5, location=(0.0, 0.06, 0.25))
    body = mesh_obj(name+'body', bevel_box(name+'bm', 0.26, 0.38, 0.55, 0.08, 3), top, (0, 0, 0.5), p)
    head = empty(name+'neck', (0, 0, 1.08)); head.parent = p
    prim('uv_sphere', M_SKIN, head, radius=0.15, location=(0, 0, 0.12), segments=24, ring_count=12)
    return p, head
man, man_neck = person('man', (-11.95, -0.9, 0.0))
owner, own_neck = person('owner', (0.3, 3.55, 0.12), M_SUIT); owner.rotation_euler = (0, 0, -math.pi/2)
man.rotation_euler = (0, math.radians(14), 0)   # leaning in to push

# ---------- motion ----------
t0, t1 = S['setup'] - 0.3, S['stop'] + 0.3
x_end = -0.6
for tt, x in [(0, -11), (t0, -11), (t1, x_end)]:
    K(car, 'location', tt, Vector((x, -0.9, 0))); K(man, 'location', tt, Vector((x - 0.95, -0.9, 0)))
# little push rhythm (bob)
n = int((t1 - t0)/0.5)
for k in range(n):
    tt = t0 + k*0.5
    K(man, 'rotation_euler', tt, Vector((0, math.radians(14 + (6 if k % 2 else 0)), 0)))
K(man, 'rotation_euler', t1 + 0.2, Vector((0, 0, 0)))
K(man, 'rotation_euler', S['stop'] + 1.2, Vector((0, 0, math.radians(70))))    # turns to the owner
K(man_neck, 'rotation_euler', S['stop'] + 2.4, Vector((0, 0, 0))); K(man_neck, 'rotation_euler', S['stop'] + 3.0, Vector((math.radians(28), 0, 0)))   # head drops
# window flicker (CCTV mood)
for k in range(12):
    keyv(WIN_E.inputs[1], k*3.4, 3.0 + (0.6 if k % 3 == 0 else 0), FPS)

# ---------- CCTV cameras (fixed, high angle) ----------
cam, cd, tgt = camera(24, 22); cd.dof.use_dof = True
cuts = []
def shot(t0_, t1_, c0, c1, g0, g1, lens=24, fstop=1.4):
    for t_, c, g in ((t0_, c0, g0), (t1_ - 0.002, c1, g1)):
        K(cam, 'location', t_, Vector(c)); K(tgt, 'location', t_, Vector(g))
        cd.lens = lens; cd.keyframe_insert('lens', frame=F(t_, FPS)); cd.dof.aperture_fstop = fstop; cd.dof.keyframe_insert('aperture_fstop', frame=F(t_, FPS))
# hook: wide CAM 02 with the car already at the hotel (end state preview) -> we show it from a high corner
# (the hook frames show the street; the push itself plays during setup)
CAM02 = Vector((-7.5, -9.0, 8.5)); CAM03 = Vector((3.2, -4.2, 3.2))
shot(0, S['log'], CAM02, CAM02 + Vector((0.6, 0.6, -0.4)), Vector((-1, 1.2, 0.4)), Vector((-1, 1.2, 0.4)), 24, 1.6)
shot(S['log'], S['stop'] + 0.6, CAM02, CAM02 + Vector((1.0, 1.2, -0.6)), Vector((-3, 0.5, 0.4)), Vector((-0.6, 1.5, 0.5)), 24, 1.6)
shot(S['stop'] + 0.6, S['clue'], CAM03, CAM03 + Vector((-0.3, 0.4, -0.2)), Vector((-0.6, 1.2, 0.7)), Vector((-0.4, 1.6, 0.8)), 30, 1.2)
# clue: pull way up — the whole "town" is a little board on a wooden table
shot(S['clue'], S['cta'] + 0.3, Vector((-2, -16, 15)), Vector((-2, -22, 22)), Vector((0, 0, 0)), Vector((0, 0, 0)), 24, 2.4)
shot(S['cta'] + 0.3, T + 0.1, CAM02, CAM02 + Vector((0.6, 0.6, -0.4)), Vector((-1, 1.2, 0.4)), Vector((-1, 1.2, 0.4)), 24, 1.6)

smooth_all()
for ob in (cam, tgt): set_constant(ob)
for fc in all_fcurves(cd): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
for ob in (cam, tgt):
    for fc in all_fcurves(ob):
        kps = fc.keyframe_points
        for i in range(0, len(kps), 2): kps[i].interpolation = 'LINEAR'
for fc in all_fcurves(car) + all_fcurves(man):
    if fc.data_path == 'location':
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/s3/s3.blend')
render(OUT, AR, FPS, T)
