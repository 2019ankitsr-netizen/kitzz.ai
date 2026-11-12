"""Shared bpy helpers for the Blender series."""
import bpy, bmesh, math, json, sys
from mathutils import Vector

def setup(res, spp, fps, total, view='AgX - Medium High Contrast', bounces=4):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = fps; sc.frame_start = 1; sc.frame_end = int(math.ceil(total*fps))
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, res
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = spp
    sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.max_bounces = bounces; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 4
    sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.05
    sc.render.use_persistent_data = True
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = view
    sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94
    return sc

def F(t, fps): return t*fps + 1

def mat(name, col, rough=0.4, metal=0.0, coat=0.0, emit=None, estr=0.0, sss=0.0, trans=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if coat: b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.06
    if emit: b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = estr
    if sss: b.inputs['Subsurface Weight'].default_value = sss; b.inputs['Subsurface Radius'].default_value = (0.3, 0.15, 0.08)
    if trans: b.inputs['Transmission Weight'].default_value = trans; b.inputs['IOR'].default_value = 1.45
    if alpha < 1: b.inputs['Alpha'].default_value = alpha
    return m

def emission(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0]); return m, e

def link(o):
    bpy.context.scene.collection.objects.link(o); return o

def empty(name, loc=(0, 0, 0)):
    o = bpy.data.objects.new(name, None); link(o); o.location = loc; return o

def mesh_obj(name, me, m=None, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, me); link(o)
    if m is not None and not me.materials: me.materials.append(m)
    o.location = loc
    if parent: o.parent = parent
    return o

def bevel_box(name, sx, sy, sz, w=0.02, seg=3, zbase=True):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x*sx, v.co.y*sy, v.co.z*sz + (sz/2 if zbase else 0)))
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=w, segments=seg, affect='EDGES', profile=0.5)
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me

def prim(kind, m=None, parent=None, smooth=True, **kw):
    getattr(bpy.ops.mesh, 'primitive_'+kind+'_add')(**kw); o = bpy.context.object
    if smooth and kind not in ('plane', 'cube'): bpy.ops.object.shade_smooth()
    if m is not None: o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def subsurf(o, lv=2):
    md = o.modifiers.new('ss', 'SUBSURF'); md.levels = lv; md.render_levels = lv; return md

def key(o, path, t, val, fps, idx=None):
    if idx is None: setattr(o, path, val); o.keyframe_insert(path, frame=F(t, fps))
    else: getattr(o, path)[idx] = val; o.keyframe_insert(path, index=idx, frame=F(t, fps))

def keyv(sock, t, val, fps):
    sock.default_value = val; sock.keyframe_insert('default_value', frame=F(t, fps))

def all_fcurves(idblock):
    ad = getattr(idblock, 'animation_data', None)
    if not ad or not ad.action: return []
    try: return list(ad.action.fcurves)
    except AttributeError:
        return [fc for layer in ad.action.layers for strip in layer.strips for cb in strip.channelbags for fc in cb.fcurves]

def smooth_all(interp='BEZIER'):
    blocks = list(bpy.data.objects) + list(bpy.data.materials) + list(bpy.data.cameras) + list(bpy.data.worlds) + list(bpy.data.lights)
    trees = [b.node_tree for b in bpy.data.materials if b.node_tree] + [w.node_tree for w in bpy.data.worlds if w.node_tree]
    for b in blocks + trees:
        for fc in all_fcurves(b):
            for kp in fc.keyframe_points:
                if kp.interpolation != 'CONSTANT':
                    kp.interpolation = interp; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'

def set_constant(o, path=None):
    for fc in all_fcurves(o):
        if path is None or fc.data_path == path:
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'

def camera(lens=40, fstop=2.8):
    cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); link(cam); bpy.context.scene.camera = cam
    cd.lens = lens; cd.sensor_width = 36; cd.sensor_fit = 'HORIZONTAL'; cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    tgt = empty('tgt'); cd.dof.focus_object = tgt
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    return cam, cd, tgt

def area(name, loc, rot, energy, size, col=(1, 1, 1)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = size; ld.color = col
    o = bpy.data.objects.new(name, ld); link(o); o.location = loc; o.rotation_euler = rot; return o

def point_at(o, target):
    d = Vector(target) - o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def world(col, strength=1.0):
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (*col, 1); bg.inputs[1].default_value = strength; return bg

def render(out, args, fps, total, F_=None):
    sc = bpy.context.scene
    st = args.get('stills')
    if st:
        for t in st.split(','):
            sc.frame_set(int(F(float(t), fps))); sc.render.filepath = f'{out}/still_{float(t):05.2f}.jpg'
            bpy.ops.render.render(write_still=True)
    else:
        sc.render.filepath = f'{out}/f_'
        if args.get('f0'): sc.frame_start = int(args['f0'])
        if args.get('f1'): sc.frame_end = int(args['f1'])
        bpy.ops.render.render(animation=True)

def args():
    A = sys.argv[1:]; d = {'out': A[0]}
    for k in ('res', 'spp', 'stills', 'f0', 'f1'):
        if '--'+k in A: d[k] = A[A.index('--'+k)+1]
    return d
