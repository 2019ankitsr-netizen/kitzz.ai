import skia, numpy as np, math, json, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
F_HB = '/home/claude/fonts/Hind-Bold.ttf'
F_HS = '/home/claude/fonts/Hind-SemiBold.ttf'
F_Y = '/home/claude/fonts/YatraOne-Regular.ttf'

def C(h, a=255):
    h = h.lstrip('#'); return skia.ColorSetARGB(int(a), int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

INK = '#2B1B12'; RED = '#A8322A'; SAF = '#E08A1E'; GOLD = '#D9A43A'; GOLDL = '#F0CF7A'
IND = '#2F4A7A'; GRN = '#4F7A3A'; SKIN = '#E7B98A'; CREAM = '#FBF3DC'; PINK = '#E58C8C'; PAPER = '#F3E6C8'

def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

# ---------- background ----------
def make_bg():
    rng = np.random.default_rng(7)
    base = np.array([243, 230, 200], np.float32)
    img = np.ones((H, W, 3), np.float32) * base
    n = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    n = np.array(Image.fromarray(((n * 20) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
    img += n[..., None] * 0.35
    img += rng.normal(0, 3, (H, W, 1))
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2)
    img *= (1 - 0.22 * np.clip(d - 0.35, 0, 1))[..., None]
    pil = Image.fromarray(img.clip(0, 255).astype(np.uint8)).convert('RGBA')
    dr = ImageDraw.Draw(pil)
    for _ in range(260):  # paper fibres
        x, y = rng.uniform(0, W), rng.uniform(0, H); a = rng.uniform(0, 6.28); l = rng.uniform(8, 30)
        dr.line([(x, y), (x + l * math.cos(a), y + l * math.sin(a))], fill=(180, 150, 110, 60), width=1)
    arr = np.array(pil)
    return arr

def border_layer():
    # kalamkari-style borders, top and bottom (outside safe zone -> decoration only)
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    p = skia.Paint(AntiAlias=True)
    for (y0, flip) in [(60, 1), (1860, -1)]:
        p.setStyle(skia.Paint.kFill_Style); p.setColor(C(RED)); c.drawRect(skia.Rect(0, y0 - 18 * flip if flip > 0 else y0 - 18, W, y0 + 18), p)
        p.setColor(C(GOLD))
        for i in range(0, W + 60, 60):
            c.drawCircle(i, y0, 9, p)
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(3); p.setColor(C(INK))
        c.drawLine(0, y0 - 18, W, y0 - 18, p); c.drawLine(0, y0 + 18, W, y0 + 18, p)
        # scallops
        yb = y0 + 18 * flip
        for i in range(0, W + 60, 60):
            path = skia.Path(); path.moveTo(i - 30, yb); path.quadTo(i, yb + 46 * flip, i + 30, yb)
            p.setStyle(skia.Paint.kFill_Style); p.setColor(C(SAF, 200)); c.drawPath(path, p)
            p.setStyle(skia.Paint.kStroke_Style); p.setColor(C(INK)); c.drawPath(path, p)
            p.setStyle(skia.Paint.kFill_Style); p.setColor(C(RED)); c.drawCircle(i, yb + 18 * flip, 5, p)
    return s.makeImageSnapshot()

# ---------- text ----------
_tc = {}
def text_img(txt, font=F_HB, size=60, fill=INK, stroke=0, sfill=CREAM):
    k = (txt, font, size, fill, stroke, sfill)
    if k in _tc: return _tc[k]
    f = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM)
    bb = f.getbbox(txt, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 8, bb[3] - bb[1] + 8
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hx = lambda c: tuple(int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    d.text((4 - bb[0], 4 - bb[1]), txt, font=f, fill=hx(fill), stroke_width=stroke, stroke_fill=hx(sfill))
    arr = np.array(im)
    si = skia.Image.fromarray(arr)
    _tc[k] = (si, w, h, (4 - bb[0], 4 - bb[1]), bb)
    return _tc[k]

def text_w(txt, font=F_HB, size=60): return text_img(txt, font, size)[1]

def draw_text(c, txt, cx, cy, font=F_HB, size=60, fill=INK, alpha=1, scale=1, stroke=0, sfill=CREAM, anchor='c', reveal=1.0):
    si, w, h, _, _ = text_img(txt, font, size, fill, stroke, sfill)
    if alpha <= 0 or scale <= 0: return w, h
    c.save(); c.translate(cx, cy); c.scale(scale, scale)
    x = -w / 2 if anchor == 'c' else (0 if anchor == 'l' else -w)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(clamp(alpha))
    if reveal < 1:
        c.clipRect(skia.Rect(x, -h, x + w * clamp(reveal), h))
    c.drawImage(si, x, -h / 2, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore(); return w, h

# ---------- self-drawing ink ----------
class Ink:
    def __init__(s, c, t): s.c = c; s.t = t
    def prog(s, t0, t1): return clamp((s.t - t0) / max(1e-3, t1 - t0))
    def partial(s, path, p):
        if p >= 1: return path
        out = skia.Path()
        pm = skia.PathMeasure(path, False); Ls = []
        while True:
            Ls.append(pm.getLength())
            if not pm.nextContour(): break
        want = sum(Ls) * p
        pm = skia.PathMeasure(path, False)
        for L in Ls:
            if want <= 0: break
            pm.getSegment(0, min(L, want), out, True); want -= L
            pm.nextContour()
        return out
    def shape(s, path, t0, t1, fill=None, w=5, col=INK, falpha=1.0):
        p = s.prog(t0, t1)
        if p <= 0: return
        if fill:
            fa = clamp((p - 0.45) / 0.55) * falpha
            if fa > 0:
                pt = skia.Paint(AntiAlias=True, Style=skia.Paint.kFill_Style, Color=C(fill, 255 * fa)); s.c.drawPath(path, pt)
        if w > 0:
            pt = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col),
                            StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
            s.c.drawPath(s.partial(path, ease(p)), pt)
    def tube(s, path, t0, t1, col, w):
        p = s.prog(t0, t1)
        if p <= 0: return
        pp = s.partial(path, ease(p))
        for ww, cc in [(w + 9, INK), (w, col)]:
            pt = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=ww, Color=C(cc),
                            StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
            s.c.drawPath(pp, pt)

def P(*cmds):
    """tiny path DSL: ('M',x,y) ('L',x,y) ('Q',x1,y1,x,y) ('C',..) ('Z',)"""
    p = skia.Path()
    for cmd in cmds:
        k = cmd[0]
        if k == 'M': p.moveTo(*cmd[1:])
        elif k == 'L': p.lineTo(*cmd[1:])
        elif k == 'Q': p.quadTo(*cmd[1:])
        elif k == 'C': p.cubicTo(*cmd[1:])
        elif k == 'Z': p.close()
    return p
def circ(x, y, r):
    p = skia.Path(); p.moveTo(x + r, y); p.addCircle(x, y, r); return p
def oval(x, y, rx, ry):
    p = skia.Path(); p.addOval(skia.Rect(x - rx, y - ry, x + rx, y + ry)); return p
def poly(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p
def rrect(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)); return p

# ---------- reusable art ----------
def quill(k, x0, y0, x1, y1, t0, t1, vane=SAF):
    """reed/quill pen from nib (x0,y0) to top (x1,y1)"""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    k.tube(P(('M', x0, y0), ('L', x1, y1)), t0, t0 + (t1 - t0) * 0.5, '#8A5A2B', 10)
    # feather vane over upper 60%
    a = 0.35
    sx, sy = x0 + dx * a, y0 + dy * a
    pts = []
    vane_path = P(('M', sx, sy), ('Q', sx + dx * 0.3 + nx * 70, sy + dy * 0.3 + ny * 70, x1 + ux * 30, y1 + uy * 30),
                  ('Q', sx + dx * 0.35 - nx * 45, sy + dy * 0.35 - ny * 45, sx, sy), ('Z',))
    k.shape(vane_path, t0 + (t1 - t0) * 0.3, t1, fill=vane, w=5)
    for i in range(1, 6):
        f = 0.35 + i * 0.11; bx, by = x0 + dx * f, y0 + dy * f
        k.shape(P(('M', bx, by), ('L', bx + nx * 38 + ux * 22, by + ny * 38 + uy * 22)), t0 + (t1 - t0) * 0.6, t1, w=3)
    # nib
    k.shape(poly([(x0, y0), (x0 + ux * 26 + nx * 7, y0 + uy * 26 + ny * 7), (x0 + ux * 26 - nx * 7, y0 + uy * 26 - ny * 7)]), t0, t0 + (t1 - t0) * 0.3, fill=INK, w=3)

def inkpot(k, x, y, s, t0, t1):
    k.shape(oval(x, y + 46 * s, 70 * s, 14 * s), t0, t1, fill='#C9B48A', w=0)
    body = P(('M', x - 34 * s, y - 20 * s), ('Q', x - 78 * s, y + 10 * s, x - 56 * s, y + 40 * s), ('Q', x, y + 62 * s, x + 56 * s, y + 40 * s),
             ('Q', x + 78 * s, y + 10 * s, x + 34 * s, y - 20 * s), ('Z',))
    k.shape(body, t0, t1, fill=IND, w=5)
    k.shape(rrect(x - 30 * s, y - 40 * s, x + 30 * s, y - 18 * s, 6 * s), t0 + 0.1, t1, fill=GOLD, w=5)
    k.shape(oval(x, y - 40 * s, 30 * s, 8 * s), t0 + 0.2, t1, fill=INK, w=4)
    k.shape(P(('M', x - 40 * s, y + 8 * s), ('Q', x, y + 26 * s, x + 40 * s, y + 8 * s)), t0 + 0.3, t1, w=4, col=GOLDL)

def diya(k, x, y, s, t0, t1, tt):
    k.shape(P(('M', x - 70 * s, y), ('Q', x, y + 70 * s, x + 70 * s, y), ('Q', x + 90 * s, y - 6 * s, x + 96 * s, y - 16 * s),
              ('Q', x, y + 6 * s, x - 70 * s, y), ('Z',)), t0, t1, fill='#B5562B', w=5)
    k.shape(P(('M', x - 50 * s, y + 18 * s), ('Q', x, y + 46 * s, x + 50 * s, y + 18 * s)), t0 + 0.2, t1, w=3, col=GOLDL)
    a = clamp((k.t - t1) / 0.3)
    if a > 0:
        fl = 1 + 0.08 * math.sin(tt * 19) + 0.05 * math.sin(tt * 31)
        fx, fy = x + 80 * s, y - 20 * s
        g = skia.Paint(AntiAlias=True, Color=C('#FFD27A', 90 * a)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22 * s))
        k.c.drawCircle(fx, fy - 30 * s, 48 * s, g)
        flame = P(('M', fx, fy), ('Q', fx - 22 * s, fy - 22 * s * fl, fx, fy - 64 * s * fl), ('Q', fx + 22 * s, fy - 22 * s * fl, fx, fy), ('Z',))
        pt = skia.Paint(AntiAlias=True, Color=C('#F2A33A', 255 * a)); k.c.drawPath(flame, pt)
        inner = P(('M', fx, fy - 4 * s), ('Q', fx - 9 * s, fy - 18 * s, fx, fy - 38 * s * fl), ('Q', fx + 9 * s, fy - 18 * s, fx, fy - 4 * s), ('Z',))
        pt.setColor(C('#FFF2B0', 255 * a)); k.c.drawPath(inner, pt)

def marigold(k, x, y, r, t0, t1):
    k.shape(circ(x, y, r), t0, t1, fill=SAF, w=4)
    for i in range(10):
        a = i * math.pi / 5
        k.shape(circ(x + math.cos(a) * r * 0.62, y + math.sin(a) * r * 0.62, r * 0.36), t0 + 0.1, t1, fill='#F2A33A', w=2.5)
    k.shape(circ(x, y, r * 0.35), t0 + 0.2, t1, fill='#C8641E', w=3)

def bahi(k, x, y, w, h, t0, t1, open_=False):
    """red-cloth bahi-khata (closed) with swastik-free simple motif"""
    k.shape(rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 10), t0, t1, fill=RED, w=5)
    k.shape(rrect(x - w / 2 + 14, y - h / 2 + 14, x + w / 2 - 14, y + h / 2 - 14, 6), t0 + 0.15, t1, w=3, col=GOLDL)
    k.shape(P(('M', x - w / 2 + 30, y), ('L', x + w / 2 - 30, y)), t0 + 0.25, t1, w=6, col=GOLD)  # tie string
    k.shape(circ(x, y, 14), t0 + 0.3, t1, fill=GOLD, w=3)

def chitragupta(k, t0, dur, tt, show_pen_write=True):
    """original folk-style figure in local box 600x740; draws over [t0, t0+dur]"""
    T = lambda a, b: (t0 + dur * a, t0 + dur * b)
    # halo
    k.shape(circ(300, 260, 220), *T(0.0, 0.18), fill=GOLDL, w=6)
    for i in range(24):
        a = i * math.pi / 12
        k.shape(circ(300 + math.cos(a) * 220, 260 + math.sin(a) * 220, 13), *T(0.05 + i * 0.004, 0.22), fill=SAF, w=3)
    k.shape(circ(300, 260, 188), *T(0.06, 0.22), w=3, col=GOLD)
    Tb = lambda a, b: T(0.36 + (a - 0.12) * 0.9, 0.36 + (b - 0.12) * 0.9)
    Th = lambda a, b: T(a - 0.22, b - 0.22)
    Ts = lambda a, b: T(a + 0.08, b + 0.08)
    # neck + head
    k.shape(rrect(276, 290, 324, 345, 12), *Th(0.4, 0.5), fill=SKIN, w=5)
    k.shape(oval(236, 236, 13, 24), *Th(0.44, 0.52), fill=SKIN, w=4)
    k.shape(oval(364, 236, 13, 24), *Th(0.44, 0.52), fill=SKIN, w=4)
    k.shape(oval(300, 228, 64, 78), *Th(0.42, 0.54), fill=SKIN, w=6)
    for ex in [236, 364]:
        k.shape(circ(ex, 270, 10), *Th(0.5, 0.56), fill=GOLD, w=3)
    # crown (mukut)
    k.shape(poly([(234, 168), (244, 112), (266, 124), (276, 74), (300, 34), (324, 74), (334, 124), (356, 112), (366, 168)]), *Th(0.48, 0.62), fill=GOLD, w=5)
    k.shape(rrect(232, 158, 368, 180, 6), *Th(0.52, 0.62), fill=RED, w=4)
    k.shape(circ(300, 120, 12), *Th(0.56, 0.64), fill=RED, w=3)
    for dx in [-40, 40]:
        k.shape(circ(300 + dx, 140, 7), *Th(0.58, 0.64), fill=IND, w=2)
    # face features
    for sx in [-1, 1]:
        ex = 300 + sx * 27
        k.shape(P(('M', ex - sx * 22, 222), ('Q', ex, 206, ex + sx * 20, 220), ('Q', ex, 232, ex - sx * 22, 222), ('Z',)), *Th(0.6, 0.68), fill='#FFFDF5', w=4)
        k.shape(circ(ex + sx * 2, 220, 6.5), *Th(0.64, 0.7), fill=INK, w=0)
        k.shape(P(('M', ex - sx * 24, 204), ('Q', ex, 190, ex + sx * 24, 202)), *Th(0.62, 0.7), w=5)
        k.shape(P(('M', ex + sx * 20, 220), ('L', ex + sx * 34, 214)), *Th(0.64, 0.7), w=3)
    k.shape(P(('M', 300, 222), ('Q', 293, 248, 300, 256), ('Q', 306, 258, 310, 252)), *Th(0.64, 0.72), w=4)
    k.shape(P(('M', 268, 272), ('Q', 286, 260, 300, 268), ('Q', 314, 260, 332, 272), ('Q', 314, 266, 300, 274), ('Q', 286, 266, 268, 272), ('Z',)), *Th(0.66, 0.74), fill=INK, w=3)
    k.shape(P(('M', 288, 284), ('Q', 300, 292, 312, 284)), *Th(0.68, 0.74), w=4, col=RED)
    k.shape(P(('M', 292, 196), ('L', 300, 168), ('L', 308, 196)), *Th(0.6, 0.68), w=5, col=RED)
    k.shape(circ(300, 200, 4), *Th(0.66, 0.7), fill=SAF, w=0)
    # lotus seat
    for i, dx in enumerate([-150, -90, -30, 30, 90, 150]):
        k.shape(P(('M', 300 + dx - 48, 690), ('Q', 300 + dx, 600, 300 + dx + 48, 690), ('Z',)), *Tb(0.12 + i * 0.01, 0.3), fill=PINK, w=4)
    k.shape(oval(300, 698, 220, 26), *Tb(0.14, 0.3), fill='#C9596A', w=5)
    # legs / dhoti (cross-legged)
    k.shape(P(('M', 170, 640), ('Q', 175, 560, 245, 545), ('L', 355, 545), ('Q', 425, 560, 430, 640), ('Q', 300, 672, 170, 640), ('Z',)), *Tb(0.18, 0.36), fill=RED, w=5)
    k.shape(P(('M', 185, 628), ('Q', 300, 655, 415, 628)), *Tb(0.3, 0.4), w=5, col=GOLD)
    # torso
    k.shape(P(('M', 200, 352), ('Q', 300, 330, 400, 352), ('Q', 395, 450, 362, 548), ('L', 238, 548), ('Q', 205, 450, 200, 352), ('Z',)), *Tb(0.22, 0.4), fill=SKIN, w=5)
    k.shape(P(('M', 205, 360), ('Q', 260, 470, 345, 548), ('L', 395, 548), ('Q', 330, 450, 258, 345), ('Z',)), *Tb(0.28, 0.44), fill=SAF, w=4)  # angvastra
    k.shape(P(('M', 252, 345), ('Q', 300, 420, 348, 345)), *Tb(0.34, 0.46), w=6, col=GOLD)
    k.shape(P(('M', 238, 342), ('Q', 300, 450, 362, 342)), *Tb(0.36, 0.48), w=5, col=RED)
    k.shape(circ(300, 418, 11), *Tb(0.4, 0.5), fill=RED, w=3)
    # arms (tubes)
    k.tube(P(('M', 212, 368), ('Q', 150, 440, 168, 500), ('Q', 190, 540, 240, 548)), *Tb(0.36, 0.5), SKIN, 42)
    k.tube(P(('M', 388, 368), ('Q', 450, 440, 432, 500), ('Q', 410, 540, 362, 548)), *Tb(0.38, 0.52), SKIN, 42)
    for bx, by in [(176, 512), (424, 512)]:
        k.shape(P(('M', bx - 18, by - 8), ('L', bx + 18, by + 8)), *Tb(0.5, 0.56), w=7, col=GOLD)
    # scroll (patra) on lap
    k.shape(rrect(212, 500, 388, 598, 4), *Ts(0.6, 0.74), fill=CREAM, w=5)
    k.shape(rrect(198, 494, 222, 604, 10), *Ts(0.62, 0.74), fill='#E8D7AE', w=4)
    k.shape(rrect(378, 494, 402, 604, 10), *Ts(0.62, 0.74), fill='#E8D7AE', w=4)
    for i in range(4):
        y = 520 + i * 20
        wr = clamp((k.t - (t0 + dur * (0.82 + i * 0.03))) / (dur * 0.06)) if show_pen_write else 1
        if wr > 0:
            k.c.save(); k.c.clipRect(skia.Rect(232, y - 8, 232 + 136 * wr, y + 8))
            pt = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C(INK), StrokeCap=skia.Paint.kRound_Cap)
            pth = skia.Path(); pth.moveTo(234, y)
            for j in range(1, 34): pth.lineTo(234 + j * 4, y + 3 * math.sin(j * 1.7 + i))
            k.c.drawPath(pth, pt); k.c.restore()
    # quill in hand (writing wiggle)
    wig = 6 * math.sin(tt * 9) if show_pen_write else 0
    quill(k, 300 + wig, 560, 170 + wig, 420, *Ts(0.7, 0.86))
    k.tube(P(('M', 240, 548), ('L', 300 + wig * 0.5, 560)), *Ts(0.7, 0.76), SKIN, 30)
    # inkpot
    inkpot(k, 500, 600, 0.85, *T(0.86, 1.0))

def place(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)

def rays(c, x, y, t, a, n=28, r0=80, r1=520):
    pt = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap)
    for i in range(n):
        ang = i * 2 * math.pi / n + t * 0.15
        L = r0 + (r1 - r0) * ease(a)
        pt.setColor(C(SAF if i % 2 else GOLD, 170 * clamp(a * 2)))
        c.drawLine(x + math.cos(ang) * r0, y + math.sin(ang) * r0, x + math.cos(ang) * L, y + math.sin(ang) * L, pt)

def chip(c, txt, cx, cy, size, bg, fg, alpha, scale=1, pad=(34, 18), font=F_HB, outline=INK):
    si, w, h, _, _ = text_img(txt, font, size, fg)
    if alpha <= 0: return
    c.save(); c.translate(cx, cy); c.scale(scale, scale)
    r = skia.Rect(-w / 2 - pad[0], -h / 2 - pad[1], w / 2 + pad[0], h / 2 + pad[1])
    p = skia.Paint(AntiAlias=True, Color=C(bg, 255 * alpha)); c.drawRRect(skia.RRect.MakeRectXY(r, 30, 30), p)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(outline, 255 * alpha)); c.drawRRect(skia.RRect.MakeRectXY(r, 30, 30), p)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(alpha)
    c.drawImage(si, -w / 2, -h / 2, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()
    return r
