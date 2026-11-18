from eng import *

VERM = '#D2693C'; MUZ = '#F4D9B0'; WHITE = '#FFFDF5'; BROWN = '#8A5A2B'; FADED = '#B9A27A'; SKY = '#BFD4E6'

def hanuman(k, t0, dur, tt, gada=True):
    """Original Kalamkari-style seated Hanuman, hands in anjali. Local box 600x760."""
    T = lambda a, b: (t0 + dur * a, t0 + dur * b)
    # halo
    k.shape(circ(300, 250, 225), *T(0.0, 0.16), fill=GOLDL, w=6)
    for i in range(24):
        a = i * math.pi / 12
        k.shape(circ(300 + math.cos(a) * 225, 250 + math.sin(a) * 225, 13), *T(0.04 + i * 0.004, 0.2), fill=SAF, w=3)
    k.shape(circ(300, 250, 192), *T(0.05, 0.2), w=3, col=GOLD)
    # tail (behind body), curling up on the left
    k.tube(P(('M', 215, 640), ('C', 60, 640, 20, 420, 70, 300), ('C', 100, 220, 170, 250, 150, 300), ('Q', 135, 330, 112, 305)), *T(0.12, 0.3), VERM, 26)
    # gada behind right shoulder
    if gada:
        k.tube(P(('M', 430, 640), ('L', 520, 190)), *T(0.14, 0.26), BROWN, 16)
        k.shape(oval(528, 150, 58, 70), *T(0.18, 0.32), fill=GOLD, w=6)
        for dy in (-30, 0, 30):
            k.shape(P(('M', 476, 150 + dy), ('Q', 528, 162 + dy, 580, 150 + dy)), *T(0.24, 0.34), w=4, col=BROWN)
        k.shape(circ(528, 70, 12), *T(0.26, 0.34), fill=GOLD, w=4)
    # lotus seat
    for i, dx in enumerate([-150, -90, -30, 30, 90, 150]):
        k.shape(P(('M', 300 + dx - 48, 700), ('Q', 300 + dx, 610, 300 + dx + 48, 700), ('Z',)), *T(0.2 + i * 0.01, 0.34), fill=PINK, w=4)
    k.shape(oval(300, 708, 220, 26), *T(0.22, 0.34), fill='#C9596A', w=5)
    # dhoti, cross-legged
    k.shape(P(('M', 165, 650), ('Q', 170, 565, 245, 550), ('L', 355, 550), ('Q', 430, 565, 435, 650), ('Q', 300, 684, 165, 650), ('Z',)), *T(0.26, 0.42), fill=SAF, w=5)
    k.shape(P(('M', 180, 638), ('Q', 300, 666, 420, 638)), *T(0.36, 0.44), w=6, col=RED)
    # torso
    k.shape(P(('M', 196, 360), ('Q', 300, 336, 404, 360), ('Q', 402, 455, 365, 552), ('L', 235, 552), ('Q', 198, 455, 196, 360), ('Z',)), *T(0.3, 0.46), fill=VERM, w=5)
    k.shape(P(('M', 250, 455), ('Q', 300, 470, 350, 455)), *T(0.4, 0.48), w=3)  # chest line
    k.shape(rrect(232, 532, 368, 556, 6), *T(0.4, 0.48), fill=GOLD, w=4)  # waist band
    k.shape(P(('M', 214, 360), ('Q', 290, 450, 352, 548)), *T(0.42, 0.5), w=5, col=WHITE)  # janeu
    # necklaces
    k.shape(P(('M', 246, 350), ('Q', 300, 420, 354, 350)), *T(0.44, 0.52), w=7, col=GOLD)
    for j in range(7):
        a = 0.15 + j * 0.115; x = 246 + 108 * a; y = 350 + 70 * 4 * a * (1 - a) * 0.9
        k.shape(circ(x, y, 6), *T(0.46, 0.52), fill=RED, w=2)
    # arms in anjali
    k.tube(P(('M', 210, 375), ('Q', 160, 460, 210, 500), ('Q', 250, 520, 292, 470)), *T(0.46, 0.58), VERM, 40)
    k.tube(P(('M', 390, 375), ('Q', 440, 460, 390, 500), ('Q', 350, 520, 308, 470)), *T(0.48, 0.6), VERM, 40)
    for bx, by in [(168, 470), (432, 470)]:
        k.shape(P(('M', bx - 18, by - 8), ('L', bx + 18, by + 8)), *T(0.56, 0.62), w=8, col=GOLD)
    k.shape(P(('M', 300, 380), ('Q', 330, 430, 312, 482), ('L', 288, 482), ('Q', 270, 430, 300, 380), ('Z',)), *T(0.56, 0.64), fill=VERM, w=5)
    k.shape(P(('M', 300, 392), ('L', 300, 478)), *T(0.6, 0.66), w=3)
    # neck + head
    Th = lambda a, b: T(0.56 + a * 0.44, 0.56 + b * 0.44)
    k.shape(rrect(274, 300, 326, 352, 12), *Th(0.0, 0.1), fill=VERM, w=5)
    for sx in (-1, 1):
        k.shape(circ(300 + sx * 88, 245, 28), *Th(0.02, 0.14), fill=VERM, w=5)
        k.shape(circ(300 + sx * 88, 245, 14), *Th(0.06, 0.16), fill=PINK, w=3)
        k.shape(circ(300 + sx * 90, 282, 9), *Th(0.12, 0.18), fill=GOLD, w=3)
    k.shape(oval(300, 238, 80, 84), *Th(0.04, 0.2), fill=VERM, w=6)
    k.shape(P(('M', 232, 230), ('Q', 240, 196, 276, 200), ('Q', 300, 214, 324, 200), ('Q', 360, 196, 368, 230),
              ('Q', 372, 312, 300, 314), ('Q', 228, 312, 232, 230), ('Z',)), *Th(0.12, 0.3), fill=MUZ, w=5)
    # crown
    k.shape(poly([(228, 170), (238, 112), (262, 126), (274, 72), (300, 30), (326, 72), (338, 126), (362, 112), (372, 170)]), *Th(0.16, 0.34), fill=GOLD, w=5)
    k.shape(rrect(226, 158, 374, 182, 6), *Th(0.22, 0.34), fill=RED, w=4)
    k.shape(circ(300, 118, 12), *Th(0.28, 0.38), fill=RED, w=3)
    for dx in (-42, 42): k.shape(circ(300 + dx, 140, 7), *Th(0.3, 0.38), fill=IND, w=2)
    # eyes / brows / nose / mouth
    blink = 0.15 if (tt % 3.7) < 0.12 else 1.0
    for sx in (-1, 1):
        ex = 300 + sx * 30
        k.shape(P(('M', ex - sx * 20, 232), ('Q', ex, 214 + (1 - blink) * 14, ex + sx * 18, 230), ('Q', ex, 242, ex - sx * 20, 232), ('Z',)), *Th(0.34, 0.5), fill=WHITE, w=4)
        if blink > 0.5: k.shape(circ(ex + sx * 2, 230, 6.5), *Th(0.44, 0.52), fill=INK, w=0)
        k.shape(P(('M', ex - sx * 24, 212), ('Q', ex, 196, ex + sx * 24, 210)), *Th(0.38, 0.52), w=5)
    k.shape(circ(292, 262, 4), *Th(0.48, 0.56), fill=INK, w=0); k.shape(circ(308, 262, 4), *Th(0.48, 0.56), fill=INK, w=0)
    k.shape(P(('M', 270, 284), ('Q', 300, 304, 330, 284)), *Th(0.5, 0.62), w=5, col=RED)
    k.shape(P(('M', 290, 204), ('L', 300, 178), ('L', 310, 204)), *Th(0.5, 0.6), w=6, col=RED)  # tilak
    k.shape(rrect(296, 182, 304, 206, 3), *Th(0.52, 0.6), fill=RED, w=0)

def mirror(k, x, y, s, t0, t1, dust=0.0, tt=0, glint=0.0):
    k.shape(rrect(x - 16 * s, y + 140 * s, x + 16 * s, y + 300 * s, 10 * s), t0, t1, fill=GOLD, w=5)
    k.shape(circ(x, y + 306 * s, 22 * s), t0, t1, fill=GOLD, w=5)
    k.shape(oval(x, y, 150 * s, 185 * s), t0, t1, fill=GOLD, w=6)
    k.shape(oval(x, y, 122 * s, 157 * s), t0 + 0.1, t1, fill=SKY, w=5)
    for i in range(12):
        a = i * math.pi / 6
        k.shape(circ(x + math.cos(a) * 136 * s, y + math.sin(a) * 171 * s, 6 * s), t0 + 0.2, t1, fill=RED, w=0)
    a = k.prog(t0 + 0.1, t1)
    if dust > 0 and a > 0:
        rng = random.Random(4)
        c = k.c; c.save()
        pth = skia.Path(); pth.addOval(skia.Rect(x - 122 * s, y - 157 * s, x + 122 * s, y + 157 * s)); c.clipPath(pth, doAntiAlias=True)
        p = skia.Paint(AntiAlias=True); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9 * s))
        for _ in range(26):
            px, py, r = x + rng.uniform(-120, 120) * s, y + rng.uniform(-150, 150) * s, rng.uniform(18, 46) * s
            p.setColor(C('#8C7A5A', 150 * dust * a)); c.drawCircle(px, py, r, p)
        c.restore()
    if glint > 0:
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=14 * s, Color=C(WHITE, 200 * glint), StrokeCap=skia.Paint.kRound_Cap)
        k.c.drawLine(x - 60 * s, y - 70 * s, x + 10 * s, y - 130 * s, p)
        p.setStrokeWidth(8 * s); k.c.drawLine(x - 40 * s, y - 20 * s, x + 30 * s, y - 85 * s, p)

def lotus(k, x, y, s, t0, t1):
    k.shape(oval(x, y + 70 * s, 150 * s, 28 * s), t0, t1, fill=GRN, w=5)
    for ang, col in [(-60, '#F2B8C0'), (60, '#F2B8C0'), (-30, PINK), (30, PINK), (0, '#F7CDD3')]:
        k.c.save(); k.c.translate(x, y + 60 * s); k.c.rotate(ang)
        k.shape(P(('M', 0, 0), ('Q', -48 * s, -80 * s, 0, -150 * s), ('Q', 48 * s, -80 * s, 0, 0), ('Z',)), t0 + 0.1, t1, fill=col, w=5)
        k.c.restore()
    k.shape(circ(x, y + 30 * s, 16 * s), t0 + 0.3, t1, fill=GOLD, w=3)

def bow(k, x, y, s, t0, t1):
    k.shape(P(('M', x - 30 * s, y - 120 * s), ('Q', x + 80 * s, y, x - 30 * s, y + 120 * s)), t0, t1, w=11 * s, col=BROWN)
    k.shape(P(('M', x - 30 * s, y - 120 * s), ('L', x - 30 * s, y + 120 * s)), t0 + 0.15, t1, w=3)
    k.shape(P(('M', x - 70 * s, y), ('L', x + 90 * s, y)), t0 + 0.3, t1, w=5)
    k.shape(poly([(x + 110 * s, y), (x + 84 * s, y - 13 * s), (x + 84 * s, y + 13 * s)]), t0 + 0.4, t1, fill=GOLD, w=3)
    k.shape(P(('M', x - 70 * s, y), ('L', x - 86 * s, y - 14 * s), ('M', x - 70 * s, y), ('L', x - 86 * s, y + 14 * s)), t0 + 0.4, t1, w=4, col=RED)

def coin(k, x, y, r, t0, t1):
    k.shape(circ(x, y, r), t0, t1, fill=GOLD, w=5)
    k.shape(circ(x, y, r * 0.75), t0 + 0.1, t1, w=3, col=BROWN)

def cloud(k, x, y, s, t0, t1, col='#5A5468'):
    path = skia.Path()
    for dx, dy, r in [(-70, 10, 55), (0, -25, 70), (75, 5, 55), (-20, 30, 50), (40, 30, 50)]:
        path.addCircle(x + dx * s, y + dy * s, r * s)
    path.setFillType(skia.PathFillType.kWinding)
    k.shape(path, t0, t1, fill=col, w=0)

def wind(k, x, y, s, t0, t1):
    for i, dy in enumerate((-60, 0, 60)):
        k.shape(P(('M', x - 160 * s, y + dy * s), ('Q', x, y + (dy - 30) * s, x + 90 * s, y + dy * s), ('Q', x + 140 * s, y + (dy + 30) * s, x + 110 * s, y + (dy + 50) * s)),
                t0 + i * 0.08, t1 + i * 0.08, w=7, col=IND)

def badge(c, txt, sub, cx, cy, r, alpha=1, scale=1):
    if alpha <= 0: return
    c.save(); c.translate(cx, cy); c.scale(scale, scale)
    p = skia.Paint(AntiAlias=True, Color=C(RED, 255 * alpha)); c.drawCircle(0, 0, r, p)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(3, r * 0.08), Color=C(GOLD, 255 * alpha)); c.drawCircle(0, 0, r * 0.86, p)
    p.setColor(C(INK, 255 * alpha)); p.setStrokeWidth(4); c.drawCircle(0, 0, r, p)
    draw_text(c, txt, 0, -r * 0.12, F_Y, int(r * 0.62), CREAM, alpha=alpha)
    if sub: draw_text(c, sub, 0, r * 0.45, F_HB, int(r * 0.28), GOLDL, alpha=alpha)
    c.restore()
