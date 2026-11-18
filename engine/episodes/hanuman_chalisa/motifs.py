"""Kalamkari-ink motif library for the Hanuman Chalisa series. Each motif draws itself around (x, y) at scale s over [t0, t1]."""
from art import *

def m_crown(k, x, y, s, t0, t1, T):
    k.shape(poly([(x - 150 * s, y + 70 * s), (x - 130 * s, y - 60 * s), (x - 70 * s, y), (x, y - 110 * s), (x + 70 * s, y), (x + 130 * s, y - 60 * s), (x + 150 * s, y + 70 * s)]), t0, t1, fill=GOLD, w=6)
    k.shape(rrect(x - 155 * s, y + 60 * s, x + 155 * s, y + 100 * s, 8), t0 + 0.2, t1, fill=RED, w=5)
    for dx in (-100, 0, 100): k.shape(circ(x + dx * s, y + 80 * s, 10 * s), t0 + 0.4, t1, fill=IND, w=3)
    k.shape(circ(x, y - 110 * s, 16 * s), t0 + 0.3, t1, fill=RED, w=4)

def m_ocean(k, x, y, s, t0, t1, T):
    for i, dy in enumerate((-80, 0, 80)):
        ph = T * 1.5 + i
        pth = skia.Path(); pth.moveTo(x - 260 * s, y + dy * s)
        for j in range(1, 27): pth.lineTo(x - 260 * s + j * 20 * s, y + dy * s + 22 * s * math.sin(j * 0.6 + ph))
        k.shape(pth, t0 + i * 0.1, t1 + i * 0.1, w=8, col=IND if i != 1 else '#4A7FB5')
    k.shape(circ(x + 150 * s, y - 170 * s, 40 * s), t0 + 0.3, t1, fill=GOLDL, w=4)

def m_gada(k, x, y, s, t0, t1, T):
    k.tube(P(('M', x - 120 * s, y + 200 * s), ('L', x + 40 * s, y - 60 * s)), t0, t0 + (t1 - t0) * 0.5, BROWN, 18 * s)
    k.shape(oval(x + 70 * s, y - 110 * s, 80 * s, 95 * s), t0 + 0.2, t1, fill=GOLD, w=6)
    for dy in (-40, 0, 40): k.shape(P(('M', x - 6 * s, y - 110 * s + dy * s), ('Q', x + 70 * s, y - 95 * s + dy * s, x + 146 * s, y - 110 * s + dy * s)), t0 + 0.4, t1, w=4, col=BROWN)
    k.shape(circ(x + 70 * s, y - 215 * s, 15 * s), t0 + 0.4, t1, fill=GOLD, w=4)

def m_flag(k, x, y, s, t0, t1, T):
    k.tube(P(('M', x - 100 * s, y + 220 * s), ('L', x - 100 * s, y - 220 * s)), t0, t0 + (t1 - t0) * 0.4, BROWN, 12 * s)
    w = 10 * math.sin(T * 3)
    k.shape(P(('M', x - 94 * s, y - 210 * s), ('Q', x + 20 * s, y - 230 * s + w, x + 150 * s, y - 160 * s), ('Q', x + 20 * s, y - 120 * s + w, x - 94 * s, y - 110 * s), ('Z',)), t0 + 0.2, t1, fill=SAF, w=5)
    k.shape(circ(x - 100 * s, y - 232 * s, 12 * s), t0 + 0.3, t1, fill=GOLD, w=3)

def m_sun(k, x, y, s, t0, t1, T):
    a = k.prog(t0, t1)
    if a > 0: rays(k.c, x, y, T, a, n=24, r0=120 * s, r1=230 * s)
    k.shape(circ(x, y, 110 * s), t0, t1, fill=SAF, w=6)
    k.shape(circ(x, y, 75 * s), t0 + 0.2, t1, fill=GOLDL, w=4)

def m_scroll(k, x, y, s, t0, t1, T):
    k.shape(rrect(x - 150 * s, y - 180 * s, x + 150 * s, y + 180 * s, 6), t0, t1, fill=CREAM, w=6)
    for yy in (-180, 180): k.shape(rrect(x - 175 * s, y + yy * s - 18 * s, x + 175 * s, y + yy * s + 18 * s, 14), t0 + 0.1, t1, fill='#E8D7AE', w=5)
    for i in range(6):
        yy = y - 120 * s + i * 48 * s
        k.shape(P(('M', x - 110 * s, yy), ('Q', x, yy - 8 * s, x + 110 * s, yy)), t0 + 0.3 + i * 0.05, t1 + i * 0.05, w=4, col=FADED)
    quill(k, x + 120 * s, y + 120 * s, x + 260 * s, y - 40 * s, t0 + 0.4, t1 + 0.2)

def m_heart(k, x, y, s, t0, t1, T):
    b = 1 + 0.04 * math.sin(T * 5)
    s2 = s * b
    k.shape(P(('M', x, y + 150 * s2), ('C', x - 230 * s2, y - 10 * s2, x - 110 * s2, y - 200 * s2, x, y - 90 * s2), ('C', x + 110 * s2, y - 200 * s2, x + 230 * s2, y - 10 * s2, x, y + 150 * s2), ('Z',)), t0, t1, fill=RED, w=6)
    k.shape(P(('M', x - 90 * s2, y - 100 * s2), ('Q', x - 120 * s2, y - 60 * s2, x - 100 * s2, y - 20 * s2)), t0 + 0.4, t1, w=6, col=PINK)

def m_ring(k, x, y, s, t0, t1, T):
    k.shape(oval(x, y + 30 * s, 120 * s, 100 * s), t0, t1, w=26 * s, col=GOLD)
    k.shape(oval(x, y + 30 * s, 120 * s, 100 * s), t0, t1, w=4)
    k.shape(rrect(x - 50 * s, y - 120 * s, x + 50 * s, y - 50 * s, 10), t0 + 0.2, t1, fill=GOLD, w=5)
    k.shape(oval(x, y - 86 * s, 28 * s, 22 * s), t0 + 0.3, t1, fill=RED, w=3)

def m_flame(k, x, y, s, t0, t1, T):
    a = k.prog(t0, t1)
    if a <= 0: return
    for i, (dx, sc, col) in enumerate([(-110, 0.7, RED), (110, 0.75, RED), (0, 1.0, SAF), (0, 0.6, GOLDL)]):
        fl = 1 + 0.08 * math.sin(T * 9 + i)
        h = 260 * s * sc * fl * ease(a); w_ = 90 * s * sc
        pth = P(('M', x + dx * s, y + 150 * s), ('Q', x + dx * s - w_ * 1.4, y + 40 * s, x + dx * s, y + 150 * s - h), ('Q', x + dx * s + w_ * 1.4, y + 40 * s, x + dx * s, y + 150 * s), ('Z',))
        k.c.drawPath(pth, skia.Paint(AntiAlias=True, Color=C(col, 255 * clamp(a * 2))))
        k.c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C(INK, 255 * clamp(a * 2))))
    k.shape(rrect(x - 200 * s, y + 150 * s, x + 200 * s, y + 175 * s, 6), t0, t1, fill=BROWN, w=4)

def m_mountain(k, x, y, s, t0, t1, T):
    k.shape(poly([(x - 230 * s, y + 160 * s), (x - 60 * s, y - 170 * s), (x + 20 * s, y - 40 * s), (x + 90 * s, y - 120 * s), (x + 230 * s, y + 160 * s)]), t0, t1, fill=GRN, w=6)
    for i in range(7):
        bx = x - 120 * s + i * 40 * s; by = y + 60 * s - (i % 3) * 40 * s
        k.shape(circ(bx, by, 11 * s), t0 + 0.3 + i * 0.03, t1, fill='#F7E27A', w=3)  # glowing herbs
    a = k.prog(t1, t1 + 0.6)
    if a > 0:
        g = skia.Paint(AntiAlias=True, Color=C('#FFF2B0', 70 * a)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
        k.c.drawCircle(x - 20 * s, y + 30 * s, 120 * s, g)

def m_earth(k, x, y, s, t0, t1, T):
    for i, (dy, col, lab) in enumerate([(-170, GOLDL, "स्वर्ग"), (0, GRN, "धरती"), (170, IND, "पाताल")]):
        k.shape(rrect(x - 210 * s, y + dy * s - 62 * s, x + 210 * s, y + dy * s + 62 * s, 30), t0 + i * 0.12, t1 + i * 0.12, fill=col, w=5)
        a = clamp((k.t - t1 - i * 0.12) / 0.3)
        if a > 0: draw_text(k.c, lab, x, y + dy * s, F_Y, int(54 * s), CREAM if i else INK, alpha=a)

def m_gate(k, x, y, s, t0, t1, T):
    k.shape(P(('M', x - 190 * s, y + 200 * s), ('L', x - 190 * s, y - 80 * s), ('Q', x, y - 260 * s, x + 190 * s, y - 80 * s), ('L', x + 190 * s, y + 200 * s)), t0, t1, w=40 * s, col=RED)
    k.shape(P(('M', x - 190 * s, y + 200 * s), ('L', x - 190 * s, y - 80 * s), ('Q', x, y - 260 * s, x + 190 * s, y - 80 * s), ('L', x + 190 * s, y + 200 * s)), t0, t1, w=4)
    k.shape(rrect(x - 140 * s, y - 40 * s, x + 140 * s, y + 200 * s, 10), t0 + 0.2, t1, fill='#B5562B', w=5)
    k.shape(P(('M', x, y - 40 * s), ('L', x, y + 200 * s)), t0 + 0.3, t1, w=5)
    for dx in (-30, 30): k.shape(circ(x + dx * s, y + 80 * s, 10 * s), t0 + 0.4, t1, fill=GOLD, w=3)
    k.shape(circ(x, y - 150 * s, 22 * s), t0 + 0.4, t1, fill=GOLD, w=4)

def m_shield(k, x, y, s, t0, t1, T):
    k.shape(P(('M', x, y - 200 * s), ('Q', x + 140 * s, y - 150 * s, x + 190 * s, y - 160 * s), ('Q', x + 200 * s, y + 80 * s, x, y + 210 * s), ('Q', x - 200 * s, y + 80 * s, x - 190 * s, y - 160 * s), ('Q', x - 140 * s, y - 150 * s, x, y - 200 * s), ('Z',)), t0, t1, fill=RED, w=6)
    k.shape(P(('M', x, y - 150 * s), ('Q', x + 110 * s, y - 115 * s, x + 145 * s, y - 120 * s), ('Q', x + 150 * s, y + 60 * s, x, y + 160 * s), ('Q', x - 150 * s, y + 60 * s, x - 145 * s, y - 120 * s), ('Q', x - 110 * s, y - 115 * s, x, y - 150 * s), ('Z',)), t0 + 0.2, t1, w=5, col=GOLD)
    draw_text(k.c, "राम", x, y, F_Y, int(84 * s), GOLDL, alpha=clamp((k.t - t1) / 0.3))

def m_chain(k, x, y, s, t0, t1, T):
    br = clamp((k.t - t1 - 1.2) / 0.6)
    for i in range(5):
        dx = (i - 2) * 95 * s + (1 if i > 2 else -1 if i < 2 else 0) * 70 * s * ease(br)
        dy = (30 if i % 2 else -30) * s * ease(br) if i != 2 else 0
        if i == 2 and br > 0.5: continue  # broken link
        k.shape(oval(x + dx, y + dy, 62 * s, 38 * s), t0 + i * 0.06, t1, w=16 * s, col='#7A7A84')
        k.shape(oval(x + dx, y + dy, 62 * s, 38 * s), t0 + i * 0.06, t1, w=3)

def m_om(k, x, y, s, t0, t1, T):
    k.shape(circ(x, y, 190 * s), t0, t1, fill=GOLDL, w=6)
    draw_text(k.c, "ॐ", x, y - 10 * s, F_HB, int(230 * s), RED, alpha=clamp((k.t - t0 - 0.3) / 0.4))

def m_hanuman(k, x, y, s, t0, t1, T):
    c = k.c; c.save(); c.translate(x - 300 * s, y - 370 * s); c.scale(s, s)
    hanuman(Ink(c, k.t), t0 - 3, 0.1, T); c.restore()

def m_lotus(k, x, y, s, t0, t1, T): lotus(k, x, y, s * 1.3, t0, t1)
def m_bow(k, x, y, s, t0, t1, T): bow(k, x, y, s * 1.4, t0, t1)
def m_wind(k, x, y, s, t0, t1, T): wind(k, x, y, s * 1.2, t0, t1)
def m_mirror(k, x, y, s, t0, t1, T): mirror(k, x, y - 60 * s, s, t0, t1, dust=0, tt=T, glint=0.7)
def m_diya(k, x, y, s, t0, t1, T): diya(k, x - 20 * s, y, s * 1.8, t0, t1, T)
def m_coin(k, x, y, s, t0, t1, T):
    for j, (dx, dy) in enumerate([(-70, 40), (70, 40), (0, -50)]):
        coin(k, x + dx * s, y + dy * s, 80 * s, t0 + j * 0.1, t1 + j * 0.1)

MOTIFS = {n[2:]: f for n, f in globals().items() if n.startswith('m_') and callable(f)}
