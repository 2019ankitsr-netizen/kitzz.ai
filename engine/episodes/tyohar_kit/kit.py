"""Reusable Kalamkari-ink kit for festival-date reels (Tyohar series + monthly "इस महीने के त्योहार").
Episode file: set CAPS (list of caption chunks per voice line), SCENES, then kit.init('durs.json', CAPS, SCENES) and kit.main()."""
import sys, json, subprocess, os, math, random, calendar
sys.path.insert(0, '/home/claude/kitzz.ai/engine/episodes/chitragupta')
from eng import *

durs = []; CAPS = []; SCENES = []; D = []; START = []; TOT = 0; NUDGE_AT = None
PAD0, PADE = 0.12, 0.30
def init(durs_path, caps, scenes, nudge_frac=0.4):
    global durs, CAPS, SCENES, D, START, TOT, NUDGE_AT
    durs = json.load(open(durs_path)); CAPS = caps; SCENES = scenes
    D = [d + PAD0 + PADE for d in durs]; D[0] = durs[0] + PAD0 + 0.2; D[-1] += 0.8
    START = [sum(D[:i]) for i in range(len(D))]; TOT = sum(D)
    NUDGE_AT = TOT * nudge_frac if nudge_frac else None

def cap_times(i):
    ch = CAPS[i]; tot = sum(len(x) for x in ch); out = []; t = PAD0
    for x in ch:
        d = durs[i] * len(x) / tot; out.append((t, t + d, x)); t += d
    return out

CAP_BOXES = []
def wrap(txt, size=54, maxw=740):
    words = txt.split(' '); lines = ['']
    for w in words:
        cand = (lines[-1] + ' ' + w).strip()
        if text_w(cand, F_HB, size) > maxw and lines[-1]: lines.append(w)
        else: lines[-1] = cand
    return lines[:2]

def draw_caption(c, i, tau):
    for (a, b, x) in cap_times(i):
        if a - 0.05 <= tau < b + (0.25 if x == CAPS[i][-1] else 0):
            pop = back((tau - a) / 0.18) if tau >= a else 0
            lines = wrap(x)
            ws = [text_w(l, F_HB, 54) for l in lines]
            bw = max(ws) + 60; lh = 70; bh = lh * len(lines) + 24
            cy = 1150 if len(lines) == 1 else 1145
            CAP_BOXES.append((520 - bw / 2, cy - bh / 2, 520 + bw / 2, cy + bh / 2))
            c.save(); c.translate(520, cy); c.scale(0.9 + 0.1 * pop, 0.9 + 0.1 * pop)
            r = skia.Rect(-bw / 2, -bh / 2, bw / 2, bh / 2)
            c.drawRRect(skia.RRect.MakeRectXY(r, 26, 26), skia.Paint(AntiAlias=True, Color=C(INK, 232)))
            for j, l in enumerate(lines):
                draw_text(c, l, 0, -bh / 2 + 12 + lh * j + lh / 2, F_HB, 54, CREAM)
            c.restore()

def headline(c, txt, tau, t0=0.0, y=330, size=70, col=RED):
    a = clamp((tau - t0) / 0.15)
    if a > 0: draw_text(c, txt, 540, y, F_Y, size, col, alpha=a, scale=0.85 + 0.15 * back((tau - t0) / 0.3), stroke=5, sfill=CREAM)

def date_chip(c, txt, tau, t0, y=445, bg=SAF):
    a = clamp((tau - t0) / 0.2)
    if a > 0: chip(c, txt, 540, y, 50, bg, INK, a, scale=0.9 + 0.1 * back((tau - t0) / 0.3), pad=(30, 12))

def label(c, txt, x, y, tau, t0, size=40, bg=CREAM, fg=INK):
    a = clamp((tau - t0) / 0.2)
    if a > 0: chip(c, txt, x, y, size, bg, fg, a, scale=0.9 + 0.1 * back((tau - t0) / 0.3), pad=(20, 9))

def nudge(c, tau, t0, dur=1.7, T=0):
    """soft mid-reel save chip (~40%)"""
    if t0 <= tau < t0 + dur:
        a = clamp((tau - t0) / 0.15) * clamp((t0 + dur - tau) / 0.2)
        bl = 0.85 + 0.15 * (0.5 + 0.5 * math.sin(T * 9))
        chip(c, "सेव कर लो — काम आएगा", 520, 1010, 44, '#FFF6DA', RED, a * bl, scale=(0.92 + 0.08 * back((tau - t0) / 0.3)), outline=RED)

def glow(c, x, y, r, col, a):
    g = skia.Paint(AntiAlias=True, Color=C(col, 255 * a)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.4))
    c.drawCircle(x, y, r, g)

def flame(c, fx, fy, s, a, tt):
    if a <= 0: return
    fl = 1 + 0.08 * math.sin(tt * 19) + 0.05 * math.sin(tt * 31)
    glow(c, fx, fy - 30 * s, 48 * s, '#FFD27A', 0.35 * a)
    f = P(('M', fx, fy), ('Q', fx - 22 * s, fy - 22 * s * fl, fx, fy - 64 * s * fl), ('Q', fx + 22 * s, fy - 22 * s * fl, fx, fy), ('Z',))
    c.drawPath(f, skia.Paint(AntiAlias=True, Color=C('#F2A33A', 255 * a)))
    g = P(('M', fx, fy - 4 * s), ('Q', fx - 9 * s, fy - 18 * s, fx, fy - 38 * s * fl), ('Q', fx + 9 * s, fy - 18 * s, fx, fy - 4 * s), ('Z',))
    c.drawPath(g, skia.Paint(AntiAlias=True, Color=C('#FFF2B0', 255 * a)))

# ---------------- art ----------------
def calendar_page(c, k, tau, T, t0=0.0, year=2026, month=12, title="दिसंबर 2026"):
    x0, x1, y0 = 210, 870, 530
    cw = (x1 - x0 - 40) / 7
    first = (calendar.weekday(year, month, 1) + 1) % 7   # Sunday-first column
    ndays = calendar.monthrange(year, month)[1]; nrows = (first + ndays + 6) // 7
    rh = 62 if nrows <= 5 else 52
    y1 = y0 + 100 + 40 + rh * nrows + 20
    k.shape(rrect(x0, y0, x1, y1, 18), t0, t0 + 0.5, fill=CREAM, w=6)
    k.shape(rrect(x0, y0, x1, y0 + 100, 18), t0 + 0.1, t0 + 0.5, fill=RED, w=6)
    for rx in [330, 540, 750]:
        k.shape(rrect(rx - 10, y0 - 34, rx + 10, y0 + 18, 10), t0 + 0.2, t0 + 0.6, fill=GOLD, w=4)
    a = clamp((tau - t0 - 0.35) / 0.2)
    draw_text(c, title, 540, y0 + 52, F_Y, 62, CREAM, alpha=a, stroke=4, sfill=INK)
    days = ["र", "सो", "मं", "बु", "गु", "शु", "श"]
    for j, d in enumerate(days):
        draw_text(c, d, x0 + 20 + cw * (j + 0.5), y0 + 128, F_HB, 32, RED, alpha=clamp((tau - t0 - 0.4) / 0.2))
    cells = {}
    for n in range(1, ndays + 1):
        idx = first + n - 1; r, col = divmod(idx, 7)
        cx = x0 + 20 + cw * (col + 0.5); cy = y0 + 172 + rh * r
        cells[n] = (cx, cy)
        draw_text(c, str(n), cx, cy, F_HB, 36 if nrows <= 5 else 32, INK, alpha=clamp((tau - t0 - 0.45 - n * 0.008) / 0.15))
    return cells

def ring(k, x, y, r, t0, t1, col=RED, w=7):
    k.shape(P(('M', x + r, y), ('C', x + r, y + r * 1.1, x - r * 1.1, y + r, x - r, y), ('C', x - r, y - r * 1.15, x + r * 1.05, y - r * 1.05, x + r * 1.1, y + r * 0.2)), t0, t1, w=w, col=col)

def trishul(k, x, y, s, t0, t1):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    k.tube(P(('M', x, y + 190 * s), ('L', x, y - 230 * s)), *T(0, 0.35), '#8A5A2B', 16 * s)
    k.shape(P(('M', x, y - 210 * s), ('L', x - 16 * s, y - 300 * s), ('L', x, y - 420 * s), ('L', x + 16 * s, y - 300 * s), ('Z',)), *T(0.25, 0.55), fill=GOLD, w=5)
    for sx in (-1, 1):
        k.shape(P(('M', x, y - 210 * s), ('Q', x + sx * 110 * s, y - 220 * s, x + sx * 100 * s, y - 330 * s),
                  ('L', x + sx * 118 * s, y - 380 * s), ('L', x + sx * 76 * s, y - 330 * s), ('Q', x + sx * 80 * s, y - 250 * s, x, y - 238 * s), ('Z',)), *T(0.3, 0.65), fill=GOLD, w=5)
    k.shape(rrect(x - 34 * s, y - 238 * s, x + 34 * s, y - 206 * s, 8 * s), *T(0.4, 0.7), fill=RED, w=4)

def damru(k, x, y, s, t0, t1, tt):
    k.shape(poly([(x - 60 * s, y - 60 * s), (x + 60 * s, y - 60 * s), (x + 8 * s, y), (x - 8 * s, y)]), t0, t1, fill=RED, w=5)
    k.shape(poly([(x - 60 * s, y + 60 * s), (x + 60 * s, y + 60 * s), (x + 8 * s, y), (x - 8 * s, y)]), t0 + 0.05, t1, fill=RED, w=5)
    k.shape(oval(x, y - 60 * s, 60 * s, 12 * s), t0 + 0.1, t1, fill=CREAM, w=4)
    k.shape(oval(x, y + 60 * s, 60 * s, 12 * s), t0 + 0.1, t1, fill=CREAM, w=4)
    k.shape(rrect(x - 12 * s, y - 8 * s, x + 12 * s, y + 8 * s, 4 * s), t0 + 0.2, t1, fill=GOLD, w=3)
    sw = math.sin(tt * 10) * 0.6
    for sx in (-1, 1):
        bx = x + sx * (60 + 30 * math.cos(sw)) * s; by = y + 40 * math.sin(sw * sx) * s
        k.shape(P(('M', x, y), ('Q', x + sx * 40 * s, y + 10 * s, bx, by)), t0 + 0.3, t1, w=3)
        k.shape(circ(bx, by, 10 * s), t0 + 0.35, t1, fill=GOLD, w=3)

def crescent(k, x, y, r, t0, t1):
    k.shape(P(('M', x, y - r), ('C', x - r * 1.35, y - r * 0.8, x - r * 1.35, y + r * 0.8, x, y + r),
              ('C', x - r * 0.6, y + r * 0.5, x - r * 0.6, y - r * 0.5, x, y - r), ('Z',)), t0, t1, fill='#FFF6DA', w=4)

def temple(k, x, base, s, t0, t1, tt):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    top = base - 300 * s
    k.shape(rrect(x - 110 * s, base - 40 * s, x + 110 * s, base + 10 * s, 6), *T(0, 0.3), fill=RED, w=5)
    k.shape(P(('M', x - 90 * s, base - 40 * s), ('Q', x - 100 * s, top + 120 * s, x, top), ('Q', x + 100 * s, top + 120 * s, x + 90 * s, base - 40 * s), ('Z',)), *T(0.1, 0.55), fill=SAF, w=5)
    for i in range(1, 5):
        yy = base - 40 * s - i * 50 * s; hw = 90 * s * (1 - (i / 6) ** 1.6)
        k.shape(P(('M', x - hw, yy), ('Q', x, yy + 12 * s, x + hw, yy)), *T(0.4 + i * 0.04, 0.7), w=3, col=INK)
    k.shape(rrect(x - 26 * s, base - 110 * s, x + 26 * s, base - 40 * s, 22 * s), *T(0.45, 0.7), fill=INK, w=4)
    k.shape(circ(x, top - 14 * s, 16 * s), *T(0.5, 0.75), fill=GOLD, w=4)
    k.tube(P(('M', x, top - 26 * s), ('L', x, top - 110 * s)), *T(0.55, 0.75), '#8A5A2B', 6)
    w = math.sin(tt * 5) * 10 * s
    k.shape(P(('M', x, top - 110 * s), ('Q', x + 40 * s, top - 100 * s + w, x + 80 * s, top - 86 * s + w), ('L', x, top - 66 * s), ('Z',)), *T(0.6, 0.8), fill=RED, w=4)

def ghats(k, t0, t1, y=870):
    for i in range(4):
        yy = y + i * 26; hw = 260 + i * 60
        k.shape(rrect(540 - hw, yy, 540 + hw, yy + 26, 3), t0 + i * 0.06, t1, fill='#D8C29A' if i % 2 else '#C9AE82', w=4)
    for i in range(3):
        yy = y + 112 + i * 22
        pth = skia.Path(); pth.moveTo(150, yy)
        for j in range(1, 40): pth.lineTo(150 + j * 20, yy + 6 * math.sin(j * 0.9 + i))
        k.shape(pth, t0 + 0.2 + i * 0.06, t1, w=4, col=IND)

def garland(k, x0, y0, x1, y1, sag, t0, t1, n=9, r=20):
    for j in range(n):
        u = j / (n - 1)
        x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u + sag * 4 * u * (1 - u)
        marigold(k, x, y, r if j % 2 == 0 else r * 0.85, t0 + (t1 - t0) * 0.6 * u, t0 + (t1 - t0) * (0.4 + 0.6 * u))

def kalash(k, x, y, s, t0, t1):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    for i, ang in enumerate([-60, -30, 0, 30, 60]):
        a = math.radians(ang - 90); L = 110 * s
        tx, ty = x + math.cos(a) * L, y - 110 * s + math.sin(a) * L
        nx, ny = -math.sin(a) * 24 * s, math.cos(a) * 24 * s
        mx, my = (x + tx) / 2, (y - 110 * s + ty) / 2
        k.shape(P(('M', x, y - 110 * s), ('Q', mx + nx, my + ny, tx, ty), ('Q', mx - nx, my - ny, x, y - 110 * s), ('Z',)), *T(0.35 + i * 0.03, 0.7), fill=GRN, w=4)
    k.shape(circ(x, y - 150 * s, 44 * s), *T(0.5, 0.8), fill='#8A5A2B', w=5)
    k.shape(P(('M', x - 30 * s, y - 175 * s), ('L', x, y - 200 * s), ('L', x + 30 * s, y - 175 * s)), *T(0.6, 0.85), w=4, col=GOLDL)
    k.shape(P(('M', x - 70 * s, y - 70 * s), ('Q', x - 140 * s, y + 20 * s, x - 70 * s, y + 90 * s), ('Q', x, y + 120 * s, x + 70 * s, y + 90 * s),
              ('Q', x + 140 * s, y + 20 * s, x + 70 * s, y - 70 * s), ('Z',)), *T(0, 0.45), fill='#B5562B', w=6)
    k.shape(rrect(x - 56 * s, y - 112 * s, x + 56 * s, y - 70 * s, 8 * s), *T(0.2, 0.5), fill=GOLD, w=5)
    k.shape(P(('M', x - 100 * s, y), ('Q', x, y + 26 * s, x + 100 * s, y)), *T(0.4, 0.7), w=6, col=RED)
    k.shape(P(('M', x - 92 * s, y + 30 * s), ('Q', x, y + 56 * s, x + 92 * s, y + 30 * s)), *T(0.45, 0.75), w=4, col=GOLDL)

def mandap(k, t0, t1, tt):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    for px in [250, 830]:
        k.tube(P(('M', px, 990), ('L', px, 640)), *T(0, 0.3), GOLD, 18)
    k.shape(P(('M', 200, 650), ('L', 540, 520), ('L', 880, 650), ('Z',)), *T(0.15, 0.45), fill=RED, w=6)
    k.shape(P(('M', 260, 640), ('L', 540, 540), ('L', 820, 640)), *T(0.3, 0.55), w=4, col=GOLD)
    for i in range(12):
        x = 230 + i * 56
        k.shape(P(('M', x, 652), ('Q', x + 28, 700, x + 56, 652), ('Z',)), *T(0.35 + i * 0.01, 0.6), fill=SAF if i % 2 else GOLDL, w=3)
    # havan kund
    k.shape(poly([(420, 930), (660, 930), (620, 990), (460, 990)]), *T(0.5, 0.7), fill='#8A5A2B', w=5)
    k.shape(P(('M', 440, 950), ('L', 640, 950)), *T(0.6, 0.75), w=3, col=GOLDL)
    a = clamp((k.t - T(0.7, 1)[0]) / 0.3)
    for dx, sc in [(-40, 0.8), (0, 1.15), (40, 0.85)]:
        flame(k.c, 540 + dx, 930, sc, a, tt + dx)

def book(k, x, y, t0, t1, tau):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    k.tube(P(('M', x - 230, y + 230), ('L', x + 170, y + 40)), *T(0, 0.3), '#8A5A2B', 18)
    k.tube(P(('M', x + 230, y + 230), ('L', x - 170, y + 40)), *T(0.05, 0.3), '#8A5A2B', 18)
    k.shape(P(('M', x, y + 10), ('Q', x - 140, y - 40, x - 290, y - 10), ('L', x - 290, y + 160), ('Q', x - 140, y + 130, x, y + 180), ('Z',)), *T(0.2, 0.55), fill='#FFFDF6', w=6)
    k.shape(P(('M', x, y + 10), ('Q', x + 140, y - 40, x + 290, y - 10), ('L', x + 290, y + 160), ('Q', x + 140, y + 130, x, y + 180), ('Z',)), *T(0.25, 0.6), fill='#FFFDF6', w=6)
    k.shape(P(('M', x, y + 10), ('L', x, y + 180)), *T(0.3, 0.6), w=6, col=RED)
    rv = clamp((tau - T(0.6, 1)[0]) / ((t1 - t0) * 0.4))
    draw_text(k.c, "गीता", x - 145, y + 75, F_Y, 84, RED, reveal=rv)
    for i in range(4):
        yy = y + 30 + i * 32
        k.shape(P(('M', x + 40, yy + 4), ('Q', x + 150, yy - 8, x + 250, yy)), *T(0.65 + i * 0.06, 0.95), w=3, col='#B9A27A')
    if 0 < rv < 1:
        tx = x - 145 - 85 + 170 * rv
        quill(Ink(k.c, 10), tx, y + 100, tx + 120, y - 100, 0, 1)

def peacock_feather(k, x, y, s, t0, t1, tt):
    sway = math.sin(tt * 2) * 6 * s
    tipx, tipy = x + 60 * s + sway, y - 330 * s
    k.shape(P(('M', x, y), ('Q', x + 10 * s, y - 180 * s, tipx, tipy)), t0, t0 + (t1 - t0) * 0.4, w=5, col='#6B4A2B')
    for i in range(14):
        u = 0.25 + i * 0.05; bx = x + (tipx - x) * u + 5 * s * math.sin(u * 3); by = y + (tipy - y) * u
        for sx in (-1, 1):
            k.shape(P(('M', bx, by), ('Q', bx + sx * 40 * s, by - 10 * s, bx + sx * 56 * s, by - 34 * s)), t0 + (t1 - t0) * (0.3 + i * 0.02), t1, w=3, col=GRN)
    ex, ey = tipx - 4 * s, tipy + 60 * s
    k.shape(oval(ex, ey, 52 * s, 70 * s), t0 + (t1 - t0) * 0.6, t1, fill=GRN, w=4)
    k.shape(oval(ex, ey + 6 * s, 36 * s, 48 * s), t0 + (t1 - t0) * 0.68, t1, fill=GOLD, w=3)
    k.shape(oval(ex, ey + 10 * s, 22 * s, 30 * s), t0 + (t1 - t0) * 0.75, t1, fill='#1F4E8C', w=3)
    k.shape(oval(ex, ey + 14 * s, 10 * s, 14 * s), t0 + (t1 - t0) * 0.82, t1, fill=INK, w=0)

def wheel(k, x, y, r, t0, t1, tt):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    k.shape(circ(x, y, r), *T(0, 0.4), w=0, fill='#E8D7AE')
    k.tube(P(('M', x + r, y), ('A',)) if False else circ(x, y, r), *T(0, 0.45), '#8A5A2B', 22)
    rot = tt * 0.6
    for i in range(12):
        a = rot + i * math.pi / 6
        k.tube(P(('M', x + math.cos(a) * 34, y + math.sin(a) * 34), ('L', x + math.cos(a) * (r - 14), y + math.sin(a) * (r - 14))), *T(0.3 + i * 0.02, 0.75), '#A87442', 9)
    k.shape(circ(x, y, 40), *T(0.6, 0.85), fill=GOLD, w=5)
    k.shape(circ(x, y, 14), *T(0.7, 0.9), fill=RED, w=3)

def shankh(k, x, y, s, t0, t1):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    body = P(('M', x - 110 * s, y + 10 * s), ('Q', x - 60 * s, y - 80 * s, x + 40 * s, y - 70 * s), ('Q', x + 120 * s, y - 50 * s, x + 130 * s, y + 10 * s),
             ('Q', x + 90 * s, y + 70 * s, x - 10 * s, y + 60 * s), ('Q', x - 80 * s, y + 50 * s, x - 110 * s, y + 10 * s), ('Z',))
    k.shape(body, *T(0, 0.5), fill='#FFFBEF', w=5)
    for i in range(3):
        cx = x + 70 * s - i * 6 * s; rr = (40 - i * 12) * s
        k.shape(P(('M', cx - rr, y), ('Q', cx, y - rr * 1.2, cx + rr, y), ('Q', cx, y + rr, cx - rr * 0.6, y)), *T(0.4 + i * 0.1, 0.9), w=3, col=SAF)
    k.shape(P(('M', x - 90 * s, y + 10 * s), ('Q', x - 20 * s, y + 30 * s, x + 50 * s, y + 20 * s)), *T(0.6, 0.95), w=3, col=PINK)

def flag(k, x, y, t0, t1, tt):
    k.tube(P(('M', x, y), ('L', x, y - 300)), t0, t0 + (t1 - t0) * 0.5, '#8A5A2B', 10)
    w = math.sin(tt * 5) * 12
    k.shape(P(('M', x, y - 300), ('Q', x + 70, y - 290 + w, x + 140, y - 270 + w), ('L', x, y - 210), ('Z',)), t0 + (t1 - t0) * 0.4, t1, fill=SAF, w=4)

def mini_card(c, k, tau, x, y, num, l1, l2, col, t0, hdr="दिसंबर"):
    k.shape(rrect(x - 140, y - 150, x + 140, y + 150, 18), t0, t0 + 0.4, fill=CREAM, w=6)
    k.shape(rrect(x - 140, y - 150, x + 140, y - 82, 18), t0 + 0.05, t0 + 0.4, fill=col, w=6)
    a = clamp((tau - t0 - 0.25) / 0.2)
    draw_text(c, hdr, x, y - 116, F_HB, 40, CREAM, alpha=a)
    draw_text(c, num, x, y - 10, F_Y, 120, col, alpha=a, scale=0.8 + 0.2 * back((tau - t0 - 0.25) / 0.3), stroke=4, sfill=INK)
    draw_text(c, l1, x, y + 80, F_HB, 38, INK, alpha=a)
    draw_text(c, l2, x, y + 122, F_HB, 38, INK, alpha=a)


# ---------- winter / Sankranti / Purnima art ----------
def sun(k, x, y, r, t0, t1, tt, face=True):
    c = k.c; a = clamp((k.t - t0) / max(1e-3, (t1 - t0) * 0.6))
    if a > 0:
        glow(c, x, y, r * 1.6, '#FFD27A', 0.35 * a)
        rot = tt * 0.25
        for i in range(16):
            an = rot + i * math.pi / 8; r1 = r * (1.25 if i % 2 else 1.45)
            pth = poly([(x + math.cos(an - 0.12) * r * 1.02, y + math.sin(an - 0.12) * r * 1.02), (x + math.cos(an) * r1, y + math.sin(an) * r1),
                        (x + math.cos(an + 0.12) * r * 1.02, y + math.sin(an + 0.12) * r * 1.02)])
            c.drawPath(pth, skia.Paint(AntiAlias=True, Color=C(SAF if i % 2 else GOLD, 255 * a)))
            c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C(INK, 255 * a)))
    k.shape(circ(x, y, r), t0, t1, fill=GOLDL, w=6)
    k.shape(circ(x, y, r * 0.78), t0 + 0.1, t1, w=3, col=SAF)
    if face:
        for sx in (-1, 1):
            k.shape(P(('M', x + sx * r * 0.42 - 14, y - r * 0.1), ('Q', x + sx * r * 0.42, y - r * 0.2, x + sx * r * 0.42 + 14, y - r * 0.1)), t0 + 0.3, t1, w=5)
        k.shape(P(('M', x - r * 0.3, y + r * 0.25), ('Q', x, y + r * 0.45, x + r * 0.3, y + r * 0.25)), t0 + 0.35, t1, w=5, col=RED)

def kite(k, x, y, s, col, t0, t1, tt, string_to=None, ph=0):
    bx = x + 10 * s * math.sin(tt * 1.7 + ph); by = y + 8 * s * math.sin(tt * 2.3 + ph)
    pts = [(bx, by - 90 * s), (bx + 70 * s, by), (bx, by + 90 * s), (bx - 70 * s, by)]
    k.shape(poly(pts), t0, t1, fill=col, w=5)
    k.shape(poly([(bx, by - 90 * s), (bx + 70 * s, by), (bx, by)]), t0 + 0.1, t1, fill=CREAM, w=3, falpha=0.55)
    k.shape(P(('M', bx, by - 90 * s), ('L', bx, by + 90 * s)), t0 + 0.15, t1, w=3)
    k.shape(P(('M', bx - 70 * s, by), ('Q', bx, by - 30 * s, bx + 70 * s, by)), t0 + 0.15, t1, w=3)
    tail = P(('M', bx, by + 90 * s), ('Q', bx - 20 * s + 10 * math.sin(tt * 4 + ph), by + 130 * s, bx + 6 * s, by + 170 * s))
    k.shape(tail, t0 + 0.2, t1, w=3)
    for j in range(2):
        tx, ty = bx - 6 * s + 8 * j * s, by + 120 * s + 30 * j * s
        k.shape(poly([(tx - 14 * s, ty - 8 * s), (tx + 14 * s, ty + 8 * s), (tx + 14 * s, ty - 8 * s), (tx - 14 * s, ty + 8 * s)]), t0 + 0.25, t1, fill=RED if j else GOLD, w=2)
    if string_to:
        sx, sy = string_to
        k.shape(P(('M', bx, by + 20 * s), ('Q', (bx + sx) / 2 + 60, (by + sy) / 2, sx, sy)), t0 + 0.2, t1, w=2, col='#6B4A2B')

def laddoos(k, x, y, s, t0, t1):
    k.shape(oval(x, y + 40 * s, 150 * s, 30 * s), t0, t1, fill=GOLD, w=5)
    k.shape(oval(x, y + 40 * s, 120 * s, 20 * s), t0 + 0.1, t1, w=3, col=RED)
    rng = random.Random(5)
    for j, (dx, dy) in enumerate([(-70, 10), (0, 14), (70, 10), (-35, -40), (35, -40), (0, -90)]):
        cx, cy = x + dx * s, y + dy * s
        k.shape(circ(cx, cy, 36 * s), t0 + 0.15 + j * 0.05, t1, fill='#C8893A', w=4)
        for q in range(6):
            a = rng.uniform(0, 6.28); rr = rng.uniform(0, 24) * s
            k.shape(oval(cx + math.cos(a) * rr, cy + math.sin(a) * rr, 4 * s, 2.5 * s), t0 + 0.3 + j * 0.05, t1, fill='#FFF6DA', w=0)

def bonfire(k, x, y, s, t0, t1, tt):
    for a in (-0.5, 0.5, -0.15, 0.15):
        L = 150 * s
        k.tube(P(('M', x - math.sin(a) * L - 40 * a * s, y + 20 * s), ('L', x + math.sin(a) * L * 0.2, y - L * 0.55)), t0, t0 + (t1 - t0) * 0.5, '#7A4A22', 22 * s)
    a = clamp((k.t - t0 - (t1 - t0) * 0.5) / 0.4)
    if a > 0:
        glow(k.c, x, y - 90 * s, 170 * s, '#FFB347', 0.35 * a)
        for dx, sc, ph in [(-50, 1.7, 0), (0, 2.6, 1.3), (50, 1.8, 2.1), (-20, 1.3, 3.1), (28, 1.2, 4.2)]:
            flame(k.c, x + dx * s, y - 10 * s, sc * s, a, tt + ph)
        rng = random.Random(9)
        for j in range(10):
            ph = (tt * 0.6 + j / 10) % 1
            sx = x + rng.uniform(-80, 80) * s + 20 * math.sin(tt * 3 + j); sy = y - 120 * s - ph * 260 * s
            k.c.drawCircle(sx, sy, 4 * s, skia.Paint(AntiAlias=True, Color=C('#FFD27A', 255 * a * (1 - ph))))

def bowl(k, x, y, s, t0, t1, item='#D9A066', n=7):
    k.shape(P(('M', x - 90 * s, y), ('Q', x, y + 90 * s, x + 90 * s, y), ('Z',)), t0, t1, fill='#B5562B', w=5)
    rng = random.Random(int(x))
    for j in range(n):
        k.shape(oval(x + rng.uniform(-60, 60) * s, y - rng.uniform(0, 18) * s, 14 * s, 9 * s), t0 + 0.2, t1, fill=item, w=2)

def pongal_pot(k, x, y, s, t0, t1, tt):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    for dx in (-110, 110):
        k.shape(rrect(x + dx * s - 40 * s, y + 70 * s, x + dx * s + 40 * s, y + 150 * s, 6), *T(0, 0.3), fill='#A8322A', w=5)
    a = clamp((k.t - T(0.3, 1)[0]) / 0.3)
    for dx in (-40, 0, 40): flame(k.c, x + dx * s, y + 140 * s, 0.9 * s, a, tt + dx)
    body = P(('M', x - 70 * s, y - 80 * s), ('Q', x - 150 * s, y, x - 80 * s, y + 80 * s), ('Q', x, y + 110 * s, x + 80 * s, y + 80 * s),
             ('Q', x + 150 * s, y, x + 70 * s, y - 80 * s), ('Z',))
    k.shape(body, *T(0.1, 0.5), fill='#B5562B', w=6)
    k.shape(P(('M', x - 120 * s, y), ('Q', x, y + 30 * s, x + 120 * s, y)), *T(0.3, 0.6), w=6, col=GOLD)
    for j in range(3):
        k.shape(P(('M', x - 20 * s + j * 20 * s, y - 70 * s), ('Q', x - 60 * s + j * 40 * s, y - 20 * s, x - 40 * s + j * 40 * s, y + 30 * s)), *T(0.4 + j * 0.05, 0.7), w=8, col=GRN)
    k.shape(rrect(x - 75 * s, y - 105 * s, x + 75 * s, y - 75 * s, 10 * s), *T(0.3, 0.55), fill='#8A3B1E', w=5)
    a = clamp((k.t - T(0.6, 1)[0]) / 0.5)
    if a > 0:
        rng = random.Random(4)
        for j in range(14):
            bx = x + rng.uniform(-80, 80) * s; by = y - 110 * s - rng.uniform(0, 50) * s - 6 * s * math.sin(tt * 4 + j)
            k.c.drawCircle(bx, by, (16 + rng.uniform(0, 14)) * s * a, skia.Paint(AntiAlias=True, Color=C('#FFFDF6')))
            k.c.drawCircle(bx, by, (16 + rng.uniform(0, 14)) * s * a, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=C(INK)))
        for sx in (-1, 1):
            dr = P(('M', x + sx * 70 * s, y - 95 * s), ('Q', x + sx * 105 * s, y - 70 * s, x + sx * 98 * s, y - 20 * s * a - 30 * s))
            k.c.drawPath(dr, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=16 * s, Color=C('#FFFDF6'), StrokeCap=skia.Paint.kRound_Cap))

def sugarcane(k, x, y0, y1, t0, t1, lean=0):
    k.tube(P(('M', x, y0), ('L', x + lean, y1)), t0, t0 + (t1 - t0) * 0.6, '#6E8F3A', 20)
    n = 6
    for j in range(1, n):
        u = j / n; px = x + lean * u; py = y0 + (y1 - y0) * u
        k.shape(P(('M', px - 12, py), ('L', px + 12, py)), t0 + (t1 - t0) * 0.4, t1, w=4)
    for sx in (-1, 1):
        k.shape(P(('M', x + lean, y1), ('Q', x + lean + sx * 60, y1 - 40, x + lean + sx * 110, y1 + 10)), t0 + (t1 - t0) * 0.5, t1, w=7, col=GRN)

def kolam(k, x, y, r, t0, t1):
    for i in range(-2, 3):
        for j in range(-1, 2):
            k.shape(circ(x + i * r, y + j * r * 0.6, 4), t0, t1, fill=INK, w=0)
    for i in range(-2, 2):
        k.shape(P(('M', x + i * r, y), ('Q', x + i * r + r / 2, y - r * 0.6, x + (i + 1) * r, y), ('Q', x + i * r + r / 2, y + r * 0.6, x + i * r, y)), t0 + 0.1, t1, w=3, col='#FFFDF6')

def full_moon(k, x, y, r, t0, t1):
    a = clamp((k.t - t0) / 0.6)
    if a > 0: glow(k.c, x, y, r * 1.7, '#FFF2B0', 0.45 * a)
    k.shape(circ(x, y, r), t0, t1, fill='#FFF8E1', w=5)
    for dx, dy, rr in [(-0.3, -0.2, 0.16), (0.25, 0.1, 0.12), (-0.05, 0.35, 0.09)]:
        k.shape(circ(x + dx * r, y + dy * r, rr * r), t0 + 0.2, t1, fill='#EFE3BE', w=2)

def floating_diyas(k, xs, y, tt, t0):
    for j, x in enumerate(xs):
        yy = y + 6 * math.sin(tt * 2 + j)
        k.shape(P(('M', x - 34, yy), ('Q', x, yy + 30, x + 34, yy), ('Z',)), t0 + j * 0.1, t0 + 0.4 + j * 0.1, fill='#B5562B', w=4)
        flame(k.c, x, yy - 4, 0.5, clamp((k.t - t0 - 0.4 - j * 0.1) / 0.3), tt + j)

def lota(k, x, y, s, t0, t1, tt, pour_to=None):
    body = P(('M', x - 40 * s, y - 60 * s), ('Q', x - 110 * s, y, x - 50 * s, y + 70 * s), ('L', x + 50 * s, y + 70 * s), ('Q', x + 110 * s, y, x + 40 * s, y - 60 * s), ('Z',))
    k.c.save(); k.c.rotate(-28, x, y)
    k.shape(body, t0, t1, fill='#C27A2C', w=5)
    k.shape(rrect(x - 52 * s, y - 80 * s, x + 52 * s, y - 56 * s, 8 * s), t0 + 0.1, t1, fill=GOLD, w=4)
    k.shape(P(('M', x - 80 * s, y), ('Q', x, y + 20 * s, x + 80 * s, y)), t0 + 0.2, t1, w=4, col=GOLDL)
    k.c.restore()
    if pour_to:
        a = clamp((k.t - t1) / 0.4)
        if a > 0:
            sx, sy = x + 60 * s, y - 70 * s; ex, ey = pour_to
            for j in range(3):
                off = 8 * j
                pth = P(('M', sx + off, sy), ('Q', (sx + ex) / 2 + 40, sy - 60 + off, ex + off, ey))
                pt = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C('#6FA8DC', 200 * a), StrokeCap=skia.Paint.kRound_Cap)
                pt.setPathEffect(skia.DashPathEffect.Make([18, 14], -(tt * 60 + j * 10) % 32)); k.c.drawPath(pth, pt)

def modak_thali(k, x, y, s, t0, t1):
    k.shape(oval(x, y, 170 * s, 44 * s), t0, t1, fill=GOLD, w=5)
    k.shape(oval(x, y, 140 * s, 32 * s), t0 + 0.1, t1, w=3, col=RED)
    for j, dx in enumerate([-80, -27, 27, 80, -53, 0, 53]):
        dy = -20 if j < 4 else -62
        mx, my = x + dx * s, y + dy * s
        m = P(('M', mx, my - 46 * s), ('Q', mx - 10 * s, my - 20 * s, mx - 34 * s, my + 10 * s), ('Q', mx, my + 30 * s, mx + 34 * s, my + 10 * s), ('Q', mx + 10 * s, my - 20 * s, mx, my - 46 * s), ('Z',))
        k.shape(m, t0 + 0.15 + j * 0.05, t1, fill='#FFF6DA', w=4)
        k.shape(P(('M', mx, my - 40 * s), ('Q', mx - 6 * s, my, mx - 18 * s, my + 14 * s)), t0 + 0.3 + j * 0.05, t1, w=2, col='#B9A27A')

def map_chip(c, txt, x, y, tau, t0, size=44, bg=SAF, fg=INK):
    a = clamp((tau - t0) / 0.2)
    if a > 0: chip(c, txt, x, y, size, bg, fg, a, scale=0.85 + 0.15 * back((tau - t0) / 0.35), pad=(24, 10))

BG = None; BORDER = None
def frame(i, tau):
    global BG, BORDER
    if BG is None:
        BG = skia.Image.fromarray(make_bg()); BORDER = border_layer()
    s = skia.Surface(W, H); c = s.getCanvas()
    c.drawImage(BG, 0, 0); c.drawImage(BORDER, 0, 0)
    T = START[i] + tau
    k = Ink(c, tau)
    SCENES[i](c, k, tau, T)
    if NUDGE_AT is not None: nudge(c, T, NUDGE_AT, 1.7, T)
    draw_caption(c, i, tau)
    return s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)

def render(i):
    n = int(round(D[i] * FPS)); tmp = f'sc{i}.tmp.mp4'
    pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for f in range(n):
        pr.stdin.write(frame(i, f / FPS).tobytes())
    pr.stdin.close(); pr.wait()
    if pr.returncode == 0: os.rename(tmp, f'sc{i}.mp4')
    return n

def main():
    if sys.argv[1] == 'still':
        from PIL import Image
        for spec in sys.argv[2:]:
            i, tau = spec.split(':'); i = int(i); tau = float(tau)
            Image.fromarray(frame(i, tau)).convert('RGB').save(f'still_{i}_{tau}.png')
    else:
        for i in map(int, sys.argv[2:]): print(i, render(i))
