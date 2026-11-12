# S5 Space Transit · stop 04 Venus — cinematic space: glowing atmospheres, starfield, sun glare (bloom/flare added in post).
import sys; sys.path.insert(0, '/home/claude/bk')
import bpy, bmesh, math, json, random
from mathutils import Vector
from blib import *
AR = args(); OUT = AR['out']; FPS = 24
VO = json.load(open('/home/claude/s5/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; T = VO['total']
sc = setup(int(AR.get('res', 50)), int(AR.get('spp', 8)), FPS, T, view='AgX - High Contrast')
sc.cycles.max_bounces = 3
def K(o, p, t, v, i=None): key(o, p, t, v, FPS, i)

# ---------- world: stars ----------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree
bg = nt.nodes['Background']; tc = nt.nodes.new('ShaderNodeTexCoord'); vor = nt.nodes.new('ShaderNodeTexVoronoi')
vor.feature = 'DISTANCE_TO_EDGE' if False else 'F1'; vor.inputs['Scale'].default_value = 420
nt.links.new(tc.outputs['Generated'], vor.inputs['Vector'])
mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.0; mr.inputs['From Max'].default_value = 0.045
mr.inputs['To Min'].default_value = 7.0; mr.inputs['To Max'].default_value = 0.0
nt.links.new(vor.outputs['Distance'], mr.inputs['Value'])
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 30
nt.links.new(tc.outputs['Generated'], noise.inputs['Vector'])
m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'; nt.links.new(mr.outputs['Result'], m2.inputs[0]); nt.links.new(noise.outputs['Fac'], m2.inputs[1])
p3 = nt.nodes.new('ShaderNodeMath'); p3.operation = 'POWER'; p3.inputs[1].default_value = 3.0; nt.links.new(m2.outputs[0], p3.inputs[0])
nt.links.new(p3.outputs[0], bg.inputs['Strength']); bg.inputs['Color'].default_value = (0.85, 0.9, 1.0, 1)
WORLD_STR = p3

# ---------- planet material builder ----------
def planet_mat(name, cols, scale=3.0, bands=False, rough=0.8):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale
    n.inputs['Detail'].default_value = 12; n.inputs['Roughness'].default_value = 0.62
    if bands:
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.25, 0.25, 6.0)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
        wv = nt.nodes.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.inputs['Scale'].default_value = 0.8
        wv.inputs['Distortion'].default_value = 6; wv.inputs['Detail'].default_value = 6
        nt.links.new(tc.outputs['Object'], wv.inputs['Vector']); src = wv.outputs['Fac']
    else:
        nt.links.new(tc.outputs['Object'], n.inputs['Vector']); src = n.outputs['Fac']
    cr = nt.nodes.new('ShaderNodeValToRGB'); el = cr.color_ramp.elements
    el[0].position = 0.3; el[0].color = (*cols[0], 1); el[1].position = 0.7; el[1].color = (*cols[-1], 1)
    for i, c in enumerate(cols[1:-1]):
        e = el.new(0.3 + 0.4*(i+1)/(len(cols)-1)); e.color = (*c, 1)
    nt.links.new(src, cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough
    return m
def atmo_mat(name, col, strength=2.5, power=4.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for x in list(nt.nodes): nt.nodes.remove(x)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = power
    nt.links.new(lw.outputs['Facing'], pw.inputs[0])
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(pw.outputs[0], mx.inputs[0]); nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs[0])
    m.blend_method = 'BLEND' if hasattr(m, 'blend_method') else None
    return m, e

# ---------- space objects ----------
SUNPOS = Vector((45, 55, 6))
sunm, sune = emission('sun', (1.0, 0.85, 0.6), 40.0)
sunobj = prim('uv_sphere', sunm, None, radius=3.0, location=SUNPOS, segments=48, ring_count=24)
sl = bpy.data.lights.new('sunL', 'SUN'); sl.energy = 2.6; sl.angle = math.radians(0.6); sl.color = (1.0, 0.93, 0.82)
slo = bpy.data.objects.new('sunL', sl); link(slo); slo.location = SUNPOS; point_at(slo, (0, 0, 0))
# Venus
VEN = Vector((0, 0, 0))
vmat = planet_mat('venus', [(0.42, 0.24, 0.07), (0.85, 0.6, 0.25), (0.97, 0.82, 0.5)], 2.2)
venus = prim('uv_sphere', vmat, None, radius=2.0, location=VEN, segments=96, ring_count=48)
vat, vate = atmo_mat('vatmo', (1.0, 0.62, 0.25), 1.8, 3.0)
vatmo = prim('uv_sphere', vat, None, radius=2.12, location=VEN, segments=96, ring_count=48)
# retrograde arrow (torus arc) around Venus
def arc(name, r, a0, a1, m, thick=0.035):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); segs = 64; ring = 10; rows = []
    for i in range(segs+1):
        a = a0 + (a1-a0)*i/segs; c = Vector((r*math.cos(a), r*math.sin(a), 0)); tng = Vector((-math.sin(a), math.cos(a), 0))
        nrm = Vector((math.cos(a), math.sin(a), 0)); up = Vector((0, 0, 1))
        rows.append([bm.verts.new(c + (nrm*math.cos(j/ring*2*math.pi) + up*math.sin(j/ring*2*math.pi))*thick) for j in range(ring)])
    for i in range(segs):
        for j in range(ring):
            bm.faces.new((rows[i][j], rows[i][(j+1) % ring], rows[i+1][(j+1) % ring], rows[i+1][j]))
    # arrow head at a1
    a = a1; c = Vector((r*math.cos(a), r*math.sin(a), 0)); tng = Vector((-math.sin(a), math.cos(a), 0)) * (1 if a1 > a0 else -1)
    nrm = Vector((math.cos(a), math.sin(a), 0)); base = [bm.verts.new(c + (nrm*math.cos(j/ring*2*math.pi) + Vector((0, 0, 1))*math.sin(j/ring*2*math.pi))*thick*3) for j in range(ring)]
    tip = bm.verts.new(c + tng*0.28)
    for j in range(ring): bm.faces.new((base[j], base[(j+1) % ring], tip))
    bm.faces.new(list(reversed(base)))
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return mesh_obj(name, me, m)
arrm, arre = emission('arrow', (0.4, 0.85, 1.0), 0.0)
arrow = arc('arrow', 2.55, math.radians(-20), math.radians(-160), arrm); arrow.rotation_euler = (math.radians(14), 0, 0)
# orbit view: small sun + orbit ring + mini Venus (area O)
O = Vector((0, 120, 0))
osun = prim('uv_sphere', sunm, None, radius=0.9, location=O, segments=32, ring_count=16)
ringm, ringe = emission('ring', (0.5, 0.6, 0.8), 1.2)
orb = arc('orbit', 4.0, 0, 2*math.pi - 0.001, ringm, 0.012); orb.location = O
mven = prim('uv_sphere', vmat, None, radius=0.35, location=O + Vector((4, 0, 0)), segments=48, ring_count=24)
mark = prim('cone', arrm, mven, vertices=16, radius1=0.07, depth=0.3, location=(0, 0.48, 0)); mark.rotation_euler = (-math.pi/2, 0, 0)
ol = bpy.data.lights.new('ol', 'POINT'); ol.energy = 4000; ol.shadow_soft_size = 0.9; olo = bpy.data.objects.new('ol', ol); link(olo); olo.location = O
# Jupiter tease
JUP = Vector((-40, -10, 6))
jm = planet_mat('jupiter', [(0.5, 0.27, 0.14), (0.9, 0.72, 0.5), (0.7, 0.4, 0.2), (0.95, 0.86, 0.7)], bands=True)
jup = prim('uv_sphere', jm, None, radius=6.0, location=JUP, segments=96, ring_count=48); jup.rotation_euler = (math.radians(8), 0, 0)
jat, _ = atmo_mat('jatmo', (0.95, 0.85, 0.7), 1.2, 4.0)
prim('uv_sphere', jat, None, radius=6.25, location=JUP, segments=96, ring_count=48)
# ---------- surface (area V) ----------
V = Vector((0, -300, 0))
gm = planet_mat('ground', [(0.18, 0.1, 0.05), (0.42, 0.22, 0.1), (0.62, 0.36, 0.16)], 1.2, rough=0.9)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=220, y_subdivisions=220, size=80, location=V); gnd = bpy.context.object
gnd.data.materials.append(gm); bpy.ops.object.shade_smooth()
tex = bpy.data.textures.new('dsp', 'CLOUDS'); tex.noise_scale = 3.5; tex.noise_depth = 4
md = gnd.modifiers.new('d', 'DISPLACE'); md.texture = tex; md.strength = 0.5; md.mid_level = 0.5
rnd = random.Random(4); rockm = planet_mat('rock', [(0.12, 0.07, 0.04), (0.35, 0.2, 0.1)], 6, rough=0.85)
for i in range(70):
    p = V + Vector((rnd.uniform(-12, 12), rnd.uniform(-4, 30), -0.1))
    r = prim('ico_sphere', rockm, None, subdivisions=2, radius=rnd.uniform(0.15, 0.7), location=p)
    r.scale = (rnd.uniform(0.8, 1.6), rnd.uniform(0.8, 1.4), rnd.uniform(0.4, 0.8)); r.rotation_euler = (rnd.random(), rnd.random(), rnd.random())
# lead ingot that melts
leadm = mat('lead', (0.55, 0.57, 0.6), 0.25, metal=1.0)
ingot = mesh_obj('ingot', bevel_box('ing', 0.9, 0.45, 0.32, 0.06, 4), leadm, V + Vector((0.3, 3.0, 0.35)))
# surface sun (low, in the west) + haze sky: big emission dome
skym, skye = emission('sky', (0.85, 0.42, 0.14), 0.0)
sky = prim('uv_sphere', skym, None, radius=70, location=V, segments=48, ring_count=24); sky.scale = (1, 1, 0.5)
for p in sky.data.polygons: p.flip() if False else None
ssun = prim('uv_sphere', sunm, None, radius=2.6, location=V + Vector((-26, 50, 6)), segments=32, ring_count=16)
gl = bpy.data.lights.new('glow', 'AREA'); gl.energy = 0.0; gl.size = 40; gl.color = (1.0, 0.6, 0.3)
glo = bpy.data.objects.new('glow', gl); link(glo); glo.location = V + Vector((-10, 20, 25)); point_at(glo, V)

for o_ in (sunobj, vatmo, sky, ssun, osun):
    o_.visible_shadow = False
for o_ in bpy.data.objects:
    if o_.active_material and o_.active_material.name.startswith(('jatmo', 'vatmo', 'sky', 'sun')): o_.visible_shadow = False
# ---------- camera ----------
cam, cd, tgt = camera(50, 8.0); cd.clip_end = 1000; cd.dof.use_dof = False
def shot(t, c, g, lens=None):
    K(cam, 'location', t, Vector(c)); K(tgt, 'location', t, Vector(g))
    if lens: cd.lens = lens; cd.keyframe_insert('lens', frame=F(t, FPS))
cuts = []
def cut(t0, t1, c0, c1, g0, g1, l0=50, l1=None):
    shot(t0, c0, g0, l0); shot(t1-0.002, c1, g1, l1 or l0); cuts.append(t1-0.002)
s_intro = S['intro']; s_day = S['day']; s_west = S['west']; s_hot = S['hot']; s_press = S['press']; s_im = S['imagine']; s_next = S['next']; s_cta = S['cta']
# hook: fly in toward crescent Venus
cut(0, s_intro+2.0, (-3.0, -26, 3.0), (-2.2, -11.5, 1.6), (0.6, 0, 0.0), (0.4, 0, 0.0), 50, 42)
# intro tail: slow orbit, sun flare at frame edge
cut(s_intro+2.0, s_day+1.6, (6.5, -9.0, 2.2), (8.5, -6.0, 2.6), (0, 0, 0), (0, 0, 0), 40)
# day: orbit diagram from above
cut(s_day+1.6, s_west-0.15, O+Vector((0, -6.5, 9.5)), O+Vector((0, -5.6, 8.6)), O, O, 38)
# west: Venus + backwards arrow
cut(s_west-0.15, s_hot-0.15, (0.0, -8.4, 2.4), (-0.8, -7.6, 1.8), (0, 0, 0.1), (0, 0, 0.1), 45)
# hot: descend to surface, ingot melting
cut(s_hot-0.15, s_press-0.15, V+Vector((-0.4, 0.4, 1.2)), V+Vector((0.0, 1.4, 0.8)), V+Vector((0.3, 3.0, 0.4)), V+Vector((0.3, 3.0, 0.3)), 35)
# press: low wide over the plain
cut(s_press-0.15, s_im-0.15, V+Vector((2.0, -4.0, 0.9)), V+Vector((1.0, -2.0, 0.8)), V+Vector((-4, 20, 1.5)), V+Vector((-6, 22, 2.0)), 28)
# imagine: sunrise in the west
cut(s_im-0.15, s_next-0.15, V+Vector((4.0, -6.0, 1.2)), V+Vector((3.0, -5.0, 1.3)), V+Vector((-26, 50, 5)), V+Vector((-26, 50, 6)), 40)
# next: Jupiter tease
cut(s_next-0.15, s_cta-0.1, (-26, -48, 8), (-28, -40, 8), JUP, JUP, 50)
# cta: back to the hook framing (loop)
cut(s_cta-0.1, T+0.1, (-2.2, -11.5, 1.6), (-3.0, -26, 3.0), (0.4, 0, 0), (0.6, 0, 0), 42, 50)

# ---------- animation ----------
K(venus, 'rotation_euler', 0, Vector((0, 0, 0))); K(venus, 'rotation_euler', T, Vector((0, 0, math.radians(-25))))
K(vatmo, 'rotation_euler', 0, Vector((0, 0, 0))); K(vatmo, 'rotation_euler', T, Vector((0, 0, math.radians(-25))))
# orbit: mini venus goes ~1 full orbit (year) but its marker turns < 1 full (day longer than year)
t0, t1 = s_day+1.6, s_west-0.15
for k in range(25):
    tt = t0 + (t1-t0)*k/24; a = 2*math.pi*0.95*k/24
    K(mven, 'location', tt, O + Vector((4*math.cos(a), 4*math.sin(a), 0)))
    K(mven, 'rotation_euler', tt, Vector((0, 0, -2*math.pi*0.95*(225/243)*k/24*0.9)))
K(arrow, 'scale', 0, Vector((0.001,)*3)); K(arrow, 'scale', s_west-0.2, Vector((0.001,)*3)); K(arrow, 'scale', s_west+0.3, Vector((1, 1, 1))); K(arrow, 'scale', s_hot-0.3, Vector((1, 1, 1))); K(arrow, 'scale', s_hot-0.2, Vector((0.001,)*3))
keyv(arre.inputs[1], s_west-0.2, 0.0, FPS); keyv(arre.inputs[1], s_west+0.4, 6.0, FPS); keyv(arre.inputs[1], s_hot-0.2, 6.0, FPS); keyv(arre.inputs[1], s_hot, 0.0, FPS)
K(venus, 'rotation_euler', s_west-0.15, None) if False else None
# lead melts: z squashes, xy spreads
K(ingot, 'scale', s_hot+3.0, Vector((1, 1, 1))); K(ingot, 'scale', s_press-0.3, Vector((1.9, 2.1, 0.12)))
K(ingot, 'location', s_hot+3.0, V + Vector((0.3, 3.0, 0.35))); K(ingot, 'location', s_press-0.3, V + Vector((0.3, 3.0, 0.22)))
# surface glow on during surface shots only
for t, e in [(s_hot-0.2, 0), (s_hot-0.1, 1), (s_next-0.2, 1), (s_next-0.1, 0)]:
    K(gl, 'energy', t, 9000.0*e); keyv(skye.inputs[1], t, 0.9*e, FPS)
# sunrise: sun climbs slowly
K(ssun, 'location', s_im-0.2, V + Vector((-26, 50, 2.5))); K(ssun, 'location', s_next, V + Vector((-26, 50, 6.5)))
K(jup, 'rotation_euler', s_next-0.2, Vector((math.radians(8), 0, 0))); K(jup, 'rotation_euler', s_cta, Vector((math.radians(8), 0, 0.25)))

smooth_all()
for ob in (cam, tgt): set_constant(ob)
for fc in all_fcurves(cd): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
for ob in (cam, tgt):
    for fc in all_fcurves(ob):
        kps = fc.keyframe_points
        for i in range(0, len(kps), 2): kps[i].interpolation = 'BEZIER'; kps[i].easing = 'EASE_IN_OUT' if False else 'AUTO'
for k in (gl,):
    for fc in all_fcurves(k): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
for fc in all_fcurves(skym.node_tree): [setattr(kp, 'interpolation', 'CONSTANT') for kp in fc.keyframe_points]
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/s5/s5.blend')
render(OUT, AR, FPS, T)
