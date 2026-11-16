# S4 Hook Shots · "Honey can last 3,000 years" — bold toy objects on punchy colour backdrops, hard cuts, squash & stretch.
import sys; sys.path.insert(0, '/home/claude/bk')
import bpy, bmesh, math, json, random
from mathutils import Vector
from blib import *
AR = args(); OUT = AR['out']; FPS = 24
VO = json.load(open('/home/claude/s4/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; E = {l['key']: l['end'] for l in VO['lines']}; T = VO['total']
sc = setup(int(AR.get('res', 50)), int(AR.get('spp', 8)), FPS, T)
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'Medium High Contrast'; sc.view_settings.exposure = -0.25
def K(o, p, t, v, i=None): key(o, p, t, v, FPS, i)

# ---------- backdrop (cyc) ----------
prof = [(y, 0.0) for y in [-14, -6, 2, 4]]
for k in range(1, 13):
    a = k/12*math.pi/2; prof.append((4 + 4*math.sin(a), 4 - 4*math.cos(a)))
prof.append((8, 40))
me = bpy.data.meshes.new('cyc'); bm = bmesh.new(); rows = []
for x in (-8, 100):
    rows.append([bm.verts.new((x, y, z)) for y, z in prof])
for i in range(len(prof)-1):
    bm.faces.new((rows[0][i], rows[0][i+1], rows[1][i+1], rows[1][i]))
bm.to_mesh(me); bm.free()
for p in me.polygons: p.use_smooth = True
M_BG = mat('bg', (0.55, 0.32, 0.98), 0.6); cyc = mesh_obj('cyc', me, M_BG)
BGC = M_BG.node_tree.nodes['Principled BSDF'].inputs['Base Color']
wbg = world((0.55, 0.32, 0.98), 0.3)

# ---------- materials ----------
M_HON = mat('honey', (1.0, 0.55, 0.02), 0.18, coat=0.9, sss=0.15)
M_HONC = mat('honeyc', (1.0, 0.55, 0.02), 0.18, coat=0.9, sss=0.15)   # crystallising jar
HC = M_HONC.node_tree.nodes['Principled BSDF'].inputs['Base Color']; HR = M_HONC.node_tree.nodes['Principled BSDF'].inputs['Roughness']
M_LID = mat('lid', (0.95, 0.15, 0.2), 0.3, coat=0.8)
M_LAB = mat('label', (0.97, 0.95, 0.9), 0.45)
M_WAX = mat('wax', (1.0, 0.8, 0.1), 0.35, coat=0.5)
M_WOOD = mat('wood', (0.62, 0.36, 0.16), 0.5)
M_SAND = mat('sand', (0.98, 0.76, 0.42), 0.7)
M_DARK = mat('dark', (0.18, 0.1, 0.05), 0.6)
M_WAT = mat('water', (0.25, 0.6, 1.0), 0.12, coat=1.0)
M_GERM, GERM_C = None, None
M_GERM = mat('germ', (0.35, 0.92, 0.25), 0.3, coat=0.6); GERM_C = M_GERM.node_tree.nodes['Principled BSDF'].inputs['Base Color']
M_WHT = mat('white', (0.97, 0.97, 0.95), 0.35)
M_BLK = mat('blk', (0.02, 0.02, 0.02), 0.25, coat=1.0)
M_ORA = mat('orange', (1.0, 0.42, 0.02), 0.4, coat=0.3)
M_PULP = mat('pulp', (1.0, 0.68, 0.15), 0.35, sss=0.1)
M_BEE = mat('bee', (1.0, 0.8, 0.0), 0.3, coat=0.6)
M_WING = mat('wing', (0.92, 0.97, 1.0), 0.1, coat=1.0, alpha=0.55)
M_BOWL = mat('bowl', (0.95, 0.95, 0.97), 0.25, coat=0.6)

def jar(name, loc, s=1.0, hm=M_HON):
    root = empty(name, loc); root.scale = (s,)*3
    h = prim('cylinder', hm, root, vertices=64, radius=0.5, depth=1.0, location=(0, 0, 0.5)); bevel(h, 0.08)
    prim('cylinder', M_LAB, root, vertices=64, radius=0.515, depth=0.38, location=(0, 0, 0.45))
    lid = prim('cylinder', M_LID, root, vertices=64, radius=0.53, depth=0.18, location=(0, 0, 1.08)); bevel(lid, 0.05)
    prim('cylinder', M_LID, root, vertices=64, radius=0.42, depth=0.06, location=(0, 0, 0.98))
    hx = prim('cylinder', M_WAX, root, vertices=6, radius=0.12, depth=0.03, location=(0, -0.52, 0.47)); hx.rotation_euler = (math.pi/2, 0, math.pi/6)
    return root
def bevel(o, w):
    m = o.modifiers.new('bv', 'BEVEL'); m.width = w; m.segments = 3; m.limit_method = 'ANGLE'
def hexes(c, n, rnd, z=0.0, r0=2.6):
    out = []
    for i in range(n):
        a = rnd.uniform(0, 2*math.pi); r = rnd.uniform(1.4, r0)
        h = prim('cylinder', M_WAX, None, vertices=6, radius=0.32, depth=0.14, location=c + Vector((math.cos(a)*r, math.sin(a)*r*0.8 + 0.6, z + 0.07)))
        h.rotation_euler = (0, 0, rnd.uniform(0, 1)); bevel(h, 0.03); out.append(h)
    return out
def dipper(name, loc, rot):
    root = empty(name, loc); root.rotation_euler = rot
    prim('cylinder', M_WOOD, root, vertices=24, radius=0.045, depth=1.5, location=(0, 0, 0.75))
    for i in range(4):
        prim('torus', M_WOOD, root, major_radius=0.12 - 0.012*abs(i-1.5), minor_radius=0.045, location=(0, 0, 0.05 + i*0.08))
    prim('uv_sphere', M_WOOD, root, radius=0.08, location=(0, 0, 0.17))
    return root

rnd = random.Random(4)
# ---------- AREA A: hook (3 jars + hex tiles + dipper) ----------
A = Vector((0, 0, 0))
jA = [jar('jA%d' % i, A + Vector(p), s) for i, (p, s) in enumerate([((-1.05, 0.2, 0), 0.95), ((0.0, -0.4, 0), 1.15), ((1.1, 0.25, 0), 0.9)])]
hxA = hexes(A, 9, rnd)
dpA = dipper('dpA', A + Vector((0.35, -0.55, 1.25)), (0.5, 0.4, 0))
# ---------- AREA B: tomb ----------
B = Vector((12, 0, 0))
pyr = prim('cone', M_SAND, None, vertices=4, radius1=2.6, radius2=0, depth=2.6, location=B + Vector((0.6, 2.2, 1.3)), smooth=False); pyr.rotation_euler = (0, 0, math.pi/4)
pyr2 = prim('cone', M_SAND, None, vertices=4, radius1=1.5, radius2=0, depth=1.5, location=B + Vector((-2.2, 3.2, 0.75)), smooth=False); pyr2.rotation_euler = (0, 0, math.pi/4)
pot = jar('pot', B + Vector((-0.5, -0.8, 0)), 1.0)
# ---------- AREA C: water + germ ----------
C = Vector((24, 0, 0))
jC = jar('jC', C, 1.25)
drop = empty('drop', C + Vector((-1.5, -0.3, 0.0)))
prim('uv_sphere', M_WAT, drop, radius=0.42, location=(0, 0, 0.42))
dc = prim('cone', M_WAT, drop, vertices=32, radius1=0.36, radius2=0.0, depth=0.55, location=(0, 0, 0.92))
germ = empty('germ', C + Vector((0, -0.1, 1.55)))
prim('uv_sphere', M_GERM, germ, radius=0.2, location=(0, 0, 0))
for i in range(14):
    y = 1 - 2*(i+0.5)/14; r = math.sqrt(1-y*y); ph = i*2.399963; d = Vector((math.cos(ph)*r, y, math.sin(ph)*r))
    sp = prim('cone', M_GERM, germ, vertices=8, radius1=0.05, radius2=0.0, depth=0.16, location=d*0.24)
    sp.rotation_mode = 'QUATERNION'; sp.rotation_quaternion = d.to_track_quat('Z', 'Y')
for sx in (-0.07, 0.07):
    prim('uv_sphere', M_WHT, germ, radius=0.06, location=(sx, -0.17, 0.05)); prim('uv_sphere', M_BLK, germ, radius=0.03, location=(sx, -0.22, 0.05))
# ---------- AREA D: acid (jar + orange) ----------
D = Vector((36, 0, 0))
jD = jar('jD', D + Vector((0.8, 0, 0)), 1.1)
orng = prim('uv_sphere', M_ORA, None, radius=0.55, location=D + Vector((-0.75, 0.25, 0.55)), segments=48, ring_count=24)
half = empty('half', D + Vector((-0.55, -0.75, 0.0)))
hh = prim('cylinder', M_ORA, half, vertices=48, radius=0.5, depth=0.3, location=(0, 0, 0.15))
pp = prim('cylinder', M_PULP, half, vertices=48, radius=0.44, depth=0.02, location=(0, 0, 0.31))
for k in range(8):
    a = k/8*2*math.pi
    s = prim('cube', M_WHT, half, size=1, location=(math.cos(a)*0.22, math.sin(a)*0.22, 0.322)); s.scale = (0.42, 0.015, 0.004); s.rotation_euler = (0, 0, a)
half.rotation_euler = (math.radians(62), 0, 0)
# ---------- AREA E: bee ----------
Ev = Vector((48, 0, 0))
jE = jar('jE', Ev + Vector((0, 0.3, 0)), 1.15)
bee = empty('bee', Ev + Vector((-0.55, -0.6, 1.9)))
bb = prim('uv_sphere', M_BEE, bee, radius=0.3, location=(0, 0, 0)); bb.scale = (1.35, 0.95, 0.95)
for x in (-0.12, 0.12):
    st = prim('torus', M_BLK, bee, major_radius=0.28, minor_radius=0.05, location=(x, 0, 0)); st.rotation_euler = (0, math.pi/2, 0)
prim('uv_sphere', M_BLK, bee, radius=0.2, location=(0.42, 0, 0.04))
for sy in (-0.09, 0.09):
    prim('uv_sphere', M_WHT, bee, radius=0.06, location=(0.52, sy*1.2 - 0.1, 0.1)); prim('uv_sphere', M_BLK, bee, radius=0.03, location=(0.56, sy*1.2 - 0.15, 0.1))
wings = []
for sy in (-1, 1):
    wp = empty('wp%d' % sy, (0, 0, 0)); wp.parent = bee; wp.location = (-0.02, sy*0.1, 0.22)
    w = prim('uv_sphere', M_WING, wp, radius=0.25, location=(0, sy*0.18, 0.12)); w.scale = (0.6, 1.0, 0.12); wings.append((wp, sy))
bubbles = []
for i in range(12):
    b = prim('uv_sphere', M_WHT, None, radius=0.06 + 0.04*rnd.random(), location=Ev + Vector((rnd.uniform(-0.3, 0.3), 0.3 + rnd.uniform(-0.3, 0.1), 1.2)))
    bubbles.append(b)
# ---------- AREA F: crystal + hot water bowl ----------
Fv = Vector((60, 0, 0))
jF = jar('jF', Fv, 1.2, M_HONC)
bowl = empty('bowl', Fv + Vector((0, 0, 0)))
bw = prim('cylinder', M_BOWL, bowl, vertices=64, radius=1.15, depth=0.5, location=(0, 0, 0.25)); bevel(bw, 0.1)
prim('cylinder', M_WAT, bowl, vertices=64, radius=1.05, depth=0.05, location=(0, 0, 0.48))
steam = [prim('uv_sphere', M_WHT, None, radius=0.14, location=Fv + Vector((x, -0.3, 0.6))) for x in (-0.75, 0.0, 0.75)]

# ---------- light ----------
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.6; sun.angle = math.radians(14)
so = bpy.data.objects.new('sun', sun); link(so); so.rotation_euler = (math.radians(42), math.radians(18), math.radians(-28))

# ---------- camera shots (hard cuts) ----------
cam, cd, tgt = camera(42, 5.6)
def shot(t0, t1, c0, c1, g0, g1, bg, lens=42, fstop=5.6):
    for t, c, g in ((t0, c0, g0), (t1-0.002, c1, g1)):
        K(cam, 'location', t, Vector(c)); K(tgt, 'location', t, Vector(g))
        cd.lens = lens; cd.keyframe_insert('lens', frame=F(t, FPS)); cd.dof.aperture_fstop = fstop; cd.dof.keyframe_insert('aperture_fstop', frame=F(t, FPS))
        keyv(BGC, t, (*bg, 1), FPS); keyv(wbg.inputs[0], t, (*bg, 1), FPS)
PINK, CYAN, MINT, PURP, BLUE, CORAL = (1, 0.3, 0.5), (0.15, 0.72, 0.95), (0.3, 0.9, 0.62), (0.55, 0.32, 0.98), (0.22, 0.38, 1.0), (1.0, 0.38, 0.33)
tB = S['tomb'] - 0.1; tC = S['water'] - 0.15; tD = S['acid'] - 0.15; tE = S['bee'] - 0.15; tF = S['crystal'] - 0.15; tH = S['cta'] - 0.15
shot(0, tB, A+Vector((0.2, -5.4, 2.3)), A+Vector((0.1, -4.8, 2.1)), A+Vector((0, 0.3, 0.75)), A+Vector((0, 0.3, 0.75)), PURP, 40, 8)
shot(tB, tC, B+Vector((-1.2, -4.6, 1.3)), B+Vector((-0.7, -4.0, 1.2)), B+Vector((-0.3, 0.2, 0.9)), B+Vector((-0.2, 0.2, 0.9)), CYAN, 36, 8)
shot(tC, tD, C+Vector((-0.6, -4.6, 1.8)), C+Vector((-0.3, -4.0, 1.7)), C+Vector((-0.5, 0, 0.75)), C+Vector((-0.2, 0, 0.8)), BLUE, 44, 5)
shot(tD, tE, D+Vector((0.0, -4.4, 1.9)), D+Vector((0.2, -3.9, 1.7)), D+Vector((0.0, 0, 0.6)), D+Vector((0.1, 0, 0.6)), MINT, 44, 5)
shot(tE, tF, Ev+Vector((-0.4, -4.6, 2.0)), Ev+Vector((0.0, -4.1, 1.9)), Ev+Vector((-0.2, 0, 0.95)), Ev+Vector((0, 0, 0.95)), PINK, 42, 5)
shot(tF, tH, Fv+Vector((0, -4.6, 2.0)), Fv+Vector((0, -4.0, 1.8)), Fv+Vector((0, 0, 0.7)), Fv+Vector((0, 0, 0.7)), CORAL, 42, 5)
shot(tH, T+0.1, A+Vector((0.1, -4.8, 2.1)), A+Vector((0.2, -5.4, 2.3)), A+Vector((0, 0.3, 0.75)), A+Vector((0, 0.3, 0.75)), PURP, 40, 8)

# ---------- object animation ----------
def drop_in(root, t0, home, h=3.5, dur=0.42):
    s = root.scale.x
    K(root, 'location', t0-0.01, home + Vector((0, 0, h))); K(root, 'location', t0+dur, home)
    K(root, 'location', t0+dur+0.12, home + Vector((0, 0, 0.18))); K(root, 'location', t0+dur+0.26, home)
    K(root, 'scale', t0+dur-0.02, Vector((s, s, s))); K(root, 'scale', t0+dur+0.05, Vector((s*1.18, s*1.18, s*0.72))); K(root, 'scale', t0+dur+0.2, Vector((s, s, s)))
def pop(o, t, s=1.0, d=0.35):
    K(o, 'scale', t-0.01, Vector((0.001,)*3)); K(o, 'scale', t+d*0.7, Vector((s*1.15,)*3)); K(o, 'scale', t+d, Vector((s,)*3))
for i, j in enumerate(jA):
    home = Vector(j.location); drop_in(j, 0.0 + i*0.12, home)
    K(j, 'location', T-0.45 + i*0.05, home); K(j, 'location', T+0.05 + i*0.05, home + Vector((0, 0, 4)))
for i, h in enumerate(hxA): pop(h, 0.5 + i*0.05, 1.0, 0.25)
pop(dpA, 0.8, 1.0, 0.3); K(dpA, 'rotation_euler', 0.8, Vector((0.5, 0.4, 0))); K(dpA, 'rotation_euler', tB, Vector((0.35, 0.2, 0.4)))
K(dpA, 'rotation_euler', tH, Vector((0.35, 0.2, 0.4))); K(dpA, 'rotation_euler', T, Vector((0.5, 0.4, 0)))
# tomb: pot slides out of the door
K(pot, 'location', tB+0.3, B + Vector((0.6, 0.6, 0))); K(pot, 'location', tB+1.2, B + Vector((-0.5, -0.8, 0)))
K(pot, 'scale', tB+0.3, Vector((0.4,)*3)); K(pot, 'scale', tB+1.2, Vector((1.0,)*3))
K(pot, 'rotation_euler', S['tomb']+3.2, Vector((0, 0, 0))); K(pot, 'rotation_euler', S['tomb']+3.45, Vector((0, 0, 0.35))); K(pot, 'rotation_euler', S['tomb']+3.7, Vector((0, 0, 0)))
# water drop shrinks (17% water)
K(drop, 'scale', S['water']+1.0, Vector((1, 1, 1))); K(drop, 'scale', S['water']+2.9, Vector((0.42, 0.42, 0.42)))
# germ falls onto the honey, shrivels and greys
tg = S['water'] + 3.6
K(germ, 'location', tg-0.01, C + Vector((0, -0.1, 7.5))); K(germ, 'location', tg+0.45, C + Vector((0, -0.1, 1.55)))
K(germ, 'scale', tg+0.45, Vector((1.6, 1.6, 1.6))); K(germ, 'scale', tg+0.6, Vector((1.9, 1.9, 1.2))); K(germ, 'scale', tg+0.8, Vector((1.6, 1.6, 1.6)))
K(germ, 'scale', tg+1.4, Vector((1.6, 1.6, 1.6))); K(germ, 'scale', tD-0.1, Vector((0.55, 0.55, 0.4)))
keyv(GERM_C, tg+1.4, (0.35, 0.92, 0.25, 1), FPS); keyv(GERM_C, tD-0.1, (0.42, 0.4, 0.36, 1), FPS)
K(germ, 'rotation_euler', tg+0.45, Vector((0, 0, 0))); K(germ, 'rotation_euler', tD, Vector((0, 0, 1.2)))
# acid: orange pops in, half wobbles
pop(orng, tD+0.5, 1.0); pop(half, tD+0.7, 1.0)
K(jD, 'rotation_euler', S['acid']+1.4, Vector((0, 0, 0))); K(jD, 'rotation_euler', S['acid']+1.6, Vector((0, 0.12, 0))); K(jD, 'rotation_euler', S['acid']+1.8, Vector((0, -0.08, 0))); K(jD, 'rotation_euler', S['acid']+2.0, Vector((0, 0, 0)))
# bee hovers in a loop, wings flap, bubbles rise
for k in range(int((tF-tE)/0.25)+2):
    t = tE + k*0.25; a = k*0.55
    K(bee, 'location', t, Ev + Vector((-0.55 + 0.3*math.sin(a*0.7), -0.6 + 0.25*math.cos(a*0.7), 1.9 + 0.12*math.sin(a*2))))
    K(bee, 'rotation_euler', t, Vector((0.08*math.sin(a), 0.1, -0.5 + 0.15*math.sin(a*0.7))))
for wp, sy in wings:
    n = int((tF-tE)/0.042)+2
    for k in range(n):
        K(wp, 'rotation_euler', tE + k*0.042, Vector((sy*(0.7 if k % 2 else -0.2), 0, 0)))
    for fc in all_fcurves(wp): [setattr(kp, 'interpolation', 'LINEAR') for kp in fc.keyframe_points]
for i, b in enumerate(bubbles):
    t0 = S['bee'] + 2.0 + i*0.22; home = Vector(b.location)
    K(b, 'scale', tE, Vector((0.001,)*3)); K(b, 'scale', t0, Vector((0.001,)*3)); K(b, 'scale', t0+0.15, Vector((1, 1, 1)))
    K(b, 'location', t0, home); K(b, 'location', t0+1.6, home + Vector((rnd.uniform(-0.4, 0.4), 0, 1.6)))
    K(b, 'scale', t0+1.45, Vector((1, 1, 1))); K(b, 'scale', t0+1.6, Vector((0.001,)*3))
# crystallise: honey turns cloudy pale, then bowl of hot water, back to golden
tc0 = S['crystal'] + 0.4; tc1 = S['crystal'] + 2.0; tw = S['crystal'] + 4.4
keyv(HC, tF, (1.0, 0.55, 0.02, 1), FPS); keyv(HC, tc0, (1.0, 0.55, 0.02, 1), FPS); keyv(HC, tc1, (1.0, 0.86, 0.55, 1), FPS)
keyv(HR, tF, 0.18, FPS); keyv(HR, tc0, 0.18, FPS); keyv(HR, tc1, 0.85, FPS)
keyv(HC, tw+0.4, (1.0, 0.86, 0.55, 1), FPS); keyv(HC, tw+1.8, (1.0, 0.55, 0.02, 1), FPS)
keyv(HR, tw+0.4, 0.85, FPS); keyv(HR, tw+1.8, 0.18, FPS)
pop(bowl, tw-0.05, 1.0, 0.35); K(jF, 'location', tw+0.05, Fv + Vector((0, 0, 0.9))); K(jF, 'location', tw+0.4, Fv + Vector((0, 0, 0.3)))
K(jF, 'location', tw-0.06, Fv); K(jF, 'location', tF, Fv)
for i, s in enumerate(steam):
    t0 = tw + 0.4 + i*0.3; home = Vector(s.location)
    K(s, 'scale', tF, Vector((0.001,)*3)); K(s, 'scale', t0, Vector((0.001,)*3)); K(s, 'scale', t0+0.3, Vector((1, 1, 1)))
    K(s, 'location', t0, home); K(s, 'location', t0+1.6, home + Vector((0, 0, 1.4))); K(s, 'scale', t0+1.6, Vector((0.001,)*3))

smooth_all()
for ob in (cam, tgt): set_constant(ob)
for fc in all_fcurves(cd): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
for tree in (M_BG.node_tree, sc.world.node_tree):
    for fc in all_fcurves(tree): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
for ob in (cam, tgt):
    for fc in all_fcurves(ob):
        kps = fc.keyframe_points
        for i in range(0, len(kps), 2): kps[i].interpolation = 'LINEAR'
for wp, sy in wings:
    for fc in all_fcurves(wp): [setattr(kp, 'interpolation', 'LINEAR') for kp in fc.keyframe_points]
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/s4/s4.blend')
render(OUT, AR, FPS, T)
