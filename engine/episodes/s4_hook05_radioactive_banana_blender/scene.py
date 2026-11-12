# S4 Hook Shots · "Bananas are radioactive" — bold toy objects on punchy colour backdrops, hard cuts, squash & stretch.
import sys; sys.path.insert(0, '/home/claude/bk')
import bpy, bmesh, math, json, random
from mathutils import Vector
from blib import *
AR = args(); OUT = AR['out']; FPS = 24
VO = json.load(open('/home/claude/s4/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; T = VO['total']
sc = setup(int(AR.get('res', 50)), int(AR.get('spp', 8)), FPS, T, view='AgX - Punchy')
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
M_BG = mat('bg', (1, 0.3, 0.5), 0.6); cyc = mesh_obj('cyc', me, M_BG)
BGC = M_BG.node_tree.nodes['Principled BSDF'].inputs['Base Color']
wbg = world((1, 0.3, 0.5), 0.3)

# ---------- materials ----------
M_BAN = mat('banana', (0.98, 0.78, 0.08), 0.42, sss=0.08, coat=0.3)
M_TIP = mat('tip', (0.16, 0.10, 0.04), 0.6)
M_STEM = mat('stem', (0.45, 0.48, 0.12), 0.55)
M_YEL = mat('yel', (1.0, 0.82, 0.0), 0.3, coat=0.6)
M_BLK = mat('blk', (0.01, 0.01, 0.012), 0.25, coat=1.0)
M_RED = mat('prot', (0.95, 0.15, 0.18), 0.25, coat=0.8)
M_BLU = mat('neut', (0.15, 0.35, 0.98), 0.25, coat=0.8)
M_GLOW, GLOW_E = emission('glow', (0.4, 1.0, 0.4), 0.0)
M_ORG = mat('geiger', (1.0, 0.45, 0.08), 0.35, coat=0.5)
M_WHT = mat('white', (0.95, 0.95, 0.93), 0.35)
M_CHR = mat('chrome', (0.8, 0.8, 0.82), 0.15, metal=1.0)

# ---------- banana mesh ----------
def banana_mesh():
    me = bpy.data.meshes.new('ban'); bm = bmesh.new(); R = 1.25; n = 28; sides = 5; ringsv = []
    for k in range(n+1):
        s = k/n; th = (s-0.5)*1.15
        c = Vector((R*math.sin(th), 0, R*(1-math.cos(th))))
        tng = Vector((math.cos(th), 0, math.sin(th))); nrm = Vector((-math.sin(th), 0, math.cos(th))); bi = Vector((0, 1, 0))
        r = 0.17*(math.sin(math.pi*min(1, max(0, (s*0.94+0.03))))**0.55) + 0.012
        ring = []
        for j in range(sides):
            a = j/sides*2*math.pi
            ring.append(bm.verts.new(c + nrm*math.cos(a)*r + bi*math.sin(a)*r))
        ringsv.append(ring)
    for k in range(n):
        for j in range(sides):
            a, b = ringsv[k][j], ringsv[k][(j+1) % sides]; c_, d = ringsv[k+1][(j+1) % sides], ringsv[k+1][j]
            bm.faces.new((a, b, c_, d))
    bm.faces.new(list(reversed(ringsv[0]))); bm.faces.new(ringsv[-1])
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    me.materials.append(M_BAN); return me
ME_BAN = banana_mesh()
R0 = 1.25; th0 = -0.575
def banana(name, loc, rz=0.0, scale=1.0, tilt=0.0):
    root = empty(name, loc); root.rotation_euler = (tilt, 0, rz); root.scale = (scale,)*3
    b = mesh_obj(name+'_b', ME_BAN, None, (0, 0, 0.19), root); subsurf(b, 2)
    tipp = Vector((R0*math.sin(-th0), 0, R0*(1-math.cos(-th0)) + 0.19))
    tip = prim('uv_sphere', M_TIP, root, radius=0.035, location=tipp)
    stp = Vector((R0*math.sin(th0), 0, R0*(1-math.cos(th0)) + 0.19))
    st = prim('cylinder', M_STEM, root, vertices=10, radius=0.045, depth=0.22, location=stp + Vector((-0.08, 0, 0.05)))
    st.rotation_euler = (0, math.radians(-60), 0)
    return root

# ---------- radiation badge ----------
def badge(name, loc, s=1.0):
    root = empty(name, loc); root.scale = (s,)*3
    d = prim('cylinder', M_YEL, root, vertices=96, radius=1.0, depth=0.16, location=(0, 0, 0)); d.rotation_euler = (math.pi/2, 0, 0)
    me = bpy.data.meshes.new('tre'); bm = bmesh.new()
    for k in range(3):
        a0 = math.radians(90 + k*120 - 30); a1 = math.radians(90 + k*120 + 30); pts = []
        for i in range(13):
            a = a0 + (a1-a0)*i/12; pts.append((0.26*math.cos(a), 0.26*math.sin(a)))
        for i in range(13):
            a = a1 - (a1-a0)*i/12; pts.append((0.82*math.cos(a), 0.82*math.sin(a)))
        vs = [bm.verts.new((x, 0, z)) for x, z in pts]; f = bm.faces.new(vs)
    vs = [bm.verts.new((0.17*math.cos(i/32*2*math.pi), 0, 0.17*math.sin(i/32*2*math.pi))) for i in range(32)]; bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces)); bmesh.ops.translate(bm, vec=(0, -0.06, 0), verts=[v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)])
    bm.to_mesh(me); bm.free(); t = mesh_obj(name+'_t', me, M_BLK, (0, -0.08, 0), root)
    return root

# ---------- AREA A / H: hook ----------
A = Vector((0, 0, 0))
bA = [banana('bA%d' % i, A + Vector(p), rz) for i, (p, rz) in enumerate([((-0.9, -0.3, 0), 0.5), ((0.35, -0.8, 0), -0.3), ((0.6, 0.35, 0), 2.6)])]
bdA = badge('badgeA', A + Vector((0, 2.2, 1.9)), 1.25)
# ---------- AREA B/C: hero banana + nucleus ----------
B = Vector((12, 0, 0))
hero = banana('hero', B, 0.2, 1.3)
nuc = empty('nuc', B + Vector((0.1, -0.2, 1.4)))
pts = []
rnd = random.Random(3)
for i in range(19):
    y = 1 - 2*(i+0.5)/19; r = math.sqrt(1-y*y); ph = i*2.399963
    pts.append(Vector((math.cos(ph)*r, y, math.sin(ph)*r))*0.22*(0.6 + 0.4*rnd.random()))
for i, p in enumerate(pts):
    prim('uv_sphere', M_RED if i % 2 else M_BLU, nuc, radius=0.13, location=p, segments=24, ring_count=12)
part = prim('uv_sphere', M_GLOW, None, radius=0.12, location=nuc.location)
pl = bpy.data.lights.new('pl', 'POINT'); pl.color = (0.4, 1, 0.4); pl.energy = 0; plo = bpy.data.objects.new('plo', pl); link(plo); plo.parent = part
# ---------- AREA D: Geiger counter ----------
D = Vector((24, 0, 0))
ban_d = banana('banD', D + Vector((-0.9, -0.3, 0)), 0.3)
gc = empty('geiger', D + Vector((0.75, 0.3, 0)))
mesh_obj('gbody', bevel_box('gb', 1.3, 0.8, 0.9, 0.12, 4), M_ORG, (0, 0, 0), gc)
face = prim('cylinder', M_WHT, gc, vertices=64, radius=0.32, depth=0.04, location=(-0.15, -0.41, 0.5)); face.rotation_euler = (math.pi/2, 0, 0)
needle = empty('needle', (-0.15, -0.44, 0.38)); needle.parent = gc
nd = mesh_obj('nd', bevel_box('ndm', 0.025, 0.02, 0.36, 0.005, 1), M_BLK, (0, 0, 0), needle)
prim('cylinder', M_BLK, gc, vertices=32, radius=0.06, depth=0.05, location=(-0.15, -0.44, 0.38)).rotation_euler = (math.pi/2, 0, 0)
spk = prim('cylinder', M_BLK, gc, vertices=48, radius=0.13, depth=0.03, location=(0.38, -0.41, 0.55)); spk.rotation_euler = (math.pi/2, 0, 0)
hdl = prim('torus', M_CHR, gc, major_radius=0.35, minor_radius=0.05, location=(0, 0, 0.95)); hdl.rotation_euler = (math.pi/2, 0, 0)
# ---------- AREA E: pile of 50 ----------
E_ = Vector((36, 0, 0))
pile = []
rnd = random.Random(7)
for i in range(50):
    layer = 0 if i < 22 else 1 if i < 36 else 2 if i < 45 else 3
    rad = [1.7, 1.25, 0.8, 0.35][layer]; a = rnd.uniform(0, 2*math.pi); r = rad*math.sqrt(rnd.random())
    p = E_ + Vector((math.cos(a)*r, math.sin(a)*r, layer*0.3))
    b = banana('p%d' % i, p, rnd.uniform(0, 2*math.pi), 0.9, tilt=rnd.uniform(-0.25, 0.25))
    pile.append((b, Vector(p), 13.45 + i*0.034))
# ---------- AREA F: turntable ----------
Fv = Vector((48, 0, 0))
tt = prim('cylinder', M_WHT, None, vertices=96, radius=1.4, depth=0.18, location=Fv + Vector((0, 0, 0.09)))
spin = empty('spin', Fv + Vector((0, 0, 0.18)))
banF = banana('banF', (0, 0, 0), 0.0, 1.2); banF.parent = spin; banF.location = (0, 0.15, 0); banF.rotation_euler = (0, 0, 0)
glowF = prim('uv_sphere', M_GLOW, spin, radius=0.12, location=(0, 0, 0.9))
# ---------- AREA G: giant banana + badge ----------
G = Vector((60, 0, 0))
giant = banana('giant', G + Vector((-1.6, -0.2, 0)), 0.0, 2.6)
bdG = badge('badgeG', G + Vector((1.8, 1.5, 1.5)), 0.9)

# ---------- light ----------
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.6; sun.angle = math.radians(14)
so = bpy.data.objects.new('sun', sun); link(so); so.rotation_euler = (math.radians(42), math.radians(18), math.radians(-28))
fill = area('fill', (0, -9, 6), (0, 0, 0), 0, 1)   # unused placeholder

# ---------- camera shots (hard cuts) ----------
cam, cd, tgt = camera(42, 5.6)
cuts = []
def shot(t0, t1, c0, c1, g0, g1, bg, lens=42, fstop=5.6):
    for t, c, g in ((t0, c0, g0), (t1-0.002, c1, g1)):
        K(cam, 'location', t, Vector(c)); K(tgt, 'location', t, Vector(g))
        cd.lens = lens; cd.keyframe_insert('lens', frame=F(t, FPS)); cd.dof.aperture_fstop = fstop; cd.dof.keyframe_insert('aperture_fstop', frame=F(t, FPS))
        keyv(BGC, t, (*bg, 1), FPS); keyv(wbg.inputs[0], t, (*bg, 1), FPS)
    cuts.append(t1-0.002)
PINK, CYAN, MINT, PURP, BLUE, CORAL = (1, 0.3, 0.5), (0.15, 0.72, 0.95), (0.3, 0.9, 0.62), (0.55, 0.32, 0.98), (0.22, 0.38, 1.0), (1.0, 0.38, 0.33)
tB = S['why'] - 0.1; tC = S['why'] + 3.4; tD = S['dose'] - 0.15; tE = S['xray'] - 0.15; tF = S['safe'] - 0.15; tG = S['unit'] - 0.15; tH = S['cta'] - 0.15
shot(0, tB, A+Vector((0.2, -4.9, 2.1)), A+Vector((0.1, -4.3, 1.9)), A+Vector((0, 0.4, 0.9)), A+Vector((0, 0.4, 0.9)), PINK, 40, 8)
shot(tB, tC, B+Vector((-2.2, -3.4, 1.0)), B+Vector((-1.4, -2.7, 1.3)), B+Vector((0, 0, 0.5)), B+Vector((0.1, -0.1, 0.9)), CYAN, 50, 3.2)
shot(tC, tD, B+Vector((1.2, -2.4, 1.9)), B+Vector((0.7, -2.0, 1.7)), nuc.location + Vector((0, 0, -0.1)), nuc.location, CYAN, 60, 2.8)
shot(tD, tE, D+Vector((-0.4, -3.7, 1.6)), D+Vector((-0.1, -3.2, 1.45)), D+Vector((0.0, 0, 0.55)), D+Vector((0.2, 0, 0.55)), MINT, 45, 5)
shot(tE, tF, E_+Vector((0, -5.8, 2.7)), E_+Vector((0, -5.0, 2.4)), E_+Vector((0, 0, 0.7)), E_+Vector((0, 0, 0.6)), PURP, 40, 8)
shot(tF, tG, Fv+Vector((0, -3.6, 2.0)), Fv+Vector((0, -3.2, 1.8)), Fv+Vector((0, 0, 0.6)), Fv+Vector((0, 0, 0.6)), BLUE, 42, 5)
shot(tG, tH, G+Vector((-3.0, -5.8, 0.7)), G+Vector((-1.4, -6.4, 1.2)), G+Vector((-0.4, 0, 1.4)), G+Vector((0.2, 0, 1.4)), CORAL, 32, 7)
shot(tH, T+0.1, A+Vector((0.1, -4.3, 1.9)), A+Vector((0.2, -4.9, 2.1)), A+Vector((0, 0.4, 0.9)), A+Vector((0, 0.4, 0.9)), PINK, 40, 8)

# ---------- object animation ----------
def drop(root, t0, home, h=3.5, dur=0.42):
    K(root, 'location', t0-0.01, home + Vector((0, 0, h))); K(root, 'location', t0+dur, home)
    K(root, 'location', t0+dur+0.12, home + Vector((0, 0, 0.18))); K(root, 'location', t0+dur+0.26, home)
    K(root, 'scale', t0+dur-0.02, Vector((1, 1, 1))*root.scale.x); s = root.scale.x
    K(root, 'scale', t0+dur+0.05, Vector((s*1.18, s*1.18, s*0.72))); K(root, 'scale', t0+dur+0.2, Vector((s, s, s)))
for i, b in enumerate(bA):
    home = Vector(b.location); drop(b, 0.0 + i*0.12, home)
    # loop: zip back up at the very end
    K(b, 'location', T-0.45 + i*0.05, home); K(b, 'location', T+0.05 + i*0.05, home + Vector((0, 0, 4)))
def pop(o, t, s=1.0, d=0.35):
    K(o, 'scale', t-0.01, Vector((0.001,)*3)); K(o, 'scale', t+d*0.7, Vector((s*1.15,)*3)); K(o, 'scale', t+d, Vector((s,)*3))
pop(bdA, 0.45, 1.25); K(bdA, 'rotation_euler', 0.45, Vector((0, 0, -0.5))); K(bdA, 'rotation_euler', 2.6, Vector((0, 0, 0.15)))
K(bdA, 'rotation_euler', tH, Vector((0, 0, 0.15))); K(bdA, 'rotation_euler', T, Vector((0, 0, -0.2)))
# hero + nucleus
pop(nuc, S['why'] + 2.2, 1.0, 0.4)
for k in range(10):
    t = S['why'] + 2.7 + k*0.6
    K(nuc, 'rotation_euler', t, Vector((0.3*k, 0.5*k, 0.2*k)))
tp = S['why'] + 4.8
K(part, 'location', tp-0.01, nuc.location); K(part, 'location', tp+0.7, nuc.location + Vector((2.4, -1.0, 2.6)))
pop(part, tp, 1.0, 0.15)
keyv(GLOW_E.inputs[1], tp-0.02, 0.0, FPS); keyv(GLOW_E.inputs[1], tp+0.05, 60.0, FPS); keyv(GLOW_E.inputs[1], tD, 30.0, FPS)
K(pl, 'energy', tp-0.02, 0.0); K(pl, 'energy', tp+0.05, 60.0); K(pl, 'energy', tp+0.8, 6.0)
# geiger needle twitch
rnd = random.Random(5)
for k in range(int((tE-tD)/0.12)):
    t = tD + k*0.12; K(needle, 'rotation_euler', t, Vector((0, math.radians(rnd.uniform(-35, 5) if k > 3 else -40), 0)))
K(gc, 'location', tD+0.2, Vector(gc.location));
# pile rain
for b, home, t0 in pile:
    s = b.scale.x; drop(b, t0, home, 4.5, 0.36)
# turntable spin + glow fades (doesn't build up)
K(spin, 'rotation_euler', tF, Vector((0, 0, math.radians(-30)))); K(spin, 'rotation_euler', tG, Vector((0, 0, math.radians(60))))
pop(glowF, tF+0.4, 1.0, 0.2); K(glowF, 'location', tF+0.4, Vector((0, 0, 0.9))); K(glowF, 'location', tF+2.6, Vector((2.2, -0.6, 2.6)))
K(glowF, 'scale', tF+2.4, Vector((1, 1, 1))); K(glowF, 'scale', tF+2.7, Vector((0.001,)*3))
# giant banana slow spin + badge pop
K(giant, 'rotation_euler', tG, Vector((0, 0, 0.3))); K(giant, 'rotation_euler', tH, Vector((0, 0, -0.25)))
pop(bdG, S['unit'] + 1.6, 0.9); K(bdG, 'rotation_euler', S['unit']+1.6, Vector((0, 0, 0.4))); K(bdG, 'rotation_euler', tH, Vector((0, 0, -0.1)))

smooth_all()
# hard cuts: camera / tgt / lens / bg keys at shot ends hold until the next shot
for ob in (cam, tgt): set_constant(ob)
for fc in all_fcurves(cd): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
for tree in (M_BG.node_tree, sc.world.node_tree):
    for fc in all_fcurves(tree): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
# but keep the slow drift inside each shot: linear between a shot's two keys
for ob in (cam, tgt):
    for fc in all_fcurves(ob):
        kps = fc.keyframe_points
        for i in range(0, len(kps), 2): kps[i].interpolation = 'LINEAR'
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/s4/s4.blend')
render(OUT, AR, FPS, T)
