"""Tyohar 03: दिसंबर के 3 बड़े त्योहार — Kalamkari ink style (reuses chitragupta/eng.py)."""
import sys, json, subprocess, os, math, random, calendar
sys.path.insert(0, '/home/claude/kitzz.ai/engine/episodes/chitragupta')
from eng import *

durs = json.load(open('durs.json'))
PAD0, PADE = 0.12, 0.30
D = [d + PAD0 + PADE for d in durs]
D[0] = durs[0] + PAD0 + 0.2
D[-1] += 0.8
START = [sum(D[:i]) for i in range(len(D))]
TOT = sum(D)

CAPS = [
    ["दिसंबर में,", "तीन बड़े त्योहार आ रहे हैं!", "तारीख़ें नोट कर लो"],
    ["पहला — काल भैरव जयंती", "मंगलवार, 1 दिसंबर"],
    ["मान्यता है, इसी दिन", "शिव जी ने काल भैरव का", "रूप लिया था", "काशी के कोतवाल,", "और समय के स्वामी"],
    ["दूसरा — विवाह पंचमी", "सोमवार, 14 दिसंबर"],
    ["इसी दिन, जनकपुर में", "श्री राम और माता सीता का", "विवाह हुआ था", "अयोध्या और जनकपुर में", "आज भी बारात निकलती है"],
    ["तीसरा — गीता जयंती", "रविवार, 20 दिसंबर"],
    ["कुरुक्षेत्र में, श्री कृष्ण ने", "अर्जुन को गीता का", "ज्ञान दिया था", "और इसी दिन", "मोक्षदा एकादशी भी है"],
    ["ये रील फ़ैमिली ग्रुप में भेजो", "और सेव कर लो", "क्योंकि दिसंबर में", "तीन बड़े त्योहार आ रहे हैं!"],
]

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
def calendar_page(c, k, tau, T, t0=0.0):
    x0, x1, y0 = 210, 870, 530
    cw = (x1 - x0 - 40) / 7; rh = 62
    y1 = y0 + 100 + 40 + rh * 5 + 20
    k.shape(rrect(x0, y0, x1, y1, 18), t0, t0 + 0.5, fill=CREAM, w=6)
    k.shape(rrect(x0, y0, x1, y0 + 100, 18), t0 + 0.1, t0 + 0.5, fill=RED, w=6)
    for rx in [330, 540, 750]:
        k.shape(rrect(rx - 10, y0 - 34, rx + 10, y0 + 18, 10), t0 + 0.2, t0 + 0.6, fill=GOLD, w=4)
    a = clamp((tau - t0 - 0.35) / 0.2)
    draw_text(c, "दिसंबर 2026", 540, y0 + 52, F_Y, 62, CREAM, alpha=a, stroke=4, sfill=INK)
    days = ["र", "सो", "मं", "बु", "गु", "शु", "श"]
    for j, d in enumerate(days):
        draw_text(c, d, x0 + 20 + cw * (j + 0.5), y0 + 128, F_HB, 32, RED, alpha=clamp((tau - t0 - 0.4) / 0.2))
    first = (calendar.weekday(2026, 12, 1) + 1) % 7   # Sunday-first column
    cells = {}
    for n in range(1, 32):
        idx = first + n - 1; r, col = divmod(idx, 7)
        if r > 4: r = 4; col = col  # 31 lands in row 5 when needed
        cx = x0 + 20 + cw * (col + 0.5); cy = y0 + 172 + rh * r
        cells[n] = (cx, cy)
        draw_text(c, str(n), cx, cy, F_HB, 36, INK, alpha=clamp((tau - t0 - 0.45 - n * 0.008) / 0.15))
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

def mini_card(c, k, tau, x, y, num, l1, l2, col, t0):
    k.shape(rrect(x - 140, y - 150, x + 140, y + 150, 18), t0, t0 + 0.4, fill=CREAM, w=6)
    k.shape(rrect(x - 140, y - 150, x + 140, y - 82, 18), t0 + 0.05, t0 + 0.4, fill=col, w=6)
    a = clamp((tau - t0 - 0.25) / 0.2)
    draw_text(c, "दिसंबर", x, y - 116, F_HB, 40, CREAM, alpha=a)
    draw_text(c, num, x, y - 10, F_Y, 120, col, alpha=a, scale=0.8 + 0.2 * back((tau - t0 - 0.25) / 0.3), stroke=4, sfill=INK)
    draw_text(c, l1, x, y + 80, F_HB, 38, INK, alpha=a)
    draw_text(c, l2, x, y + 122, F_HB, 38, INK, alpha=a)

# ---------------- scenes ----------------
def s0(c, k, tau, T):
    headline(c, "दिसंबर में…", tau, 0.0, 320, 82, INK)
    headline(c, "3 बड़े त्योहार!", tau, 0.1, 425, 96, RED)
    cells = calendar_page(c, k, tau, T, 0.05)
    for j, (n, col) in enumerate([(1, RED), (14, SAF), (20, IND)]):
        x, y = cells[n]; t1 = 1.1 + j * 0.45
        ring(k, x, y - 2, 34, t1, t1 + 0.35, col)
        a = clamp((tau - t1 - 0.3) / 0.2)
        if a > 0: glow(c, x, y, 40, GOLDL, 0.25 * a)
    for j, (mx, my) in enumerate([(160, 520), (920, 520)]):
        marigold(k, mx, my, 34, 0.4 + j * 0.1, 0.9 + j * 0.1)

def s1(c, k, tau, T):
    headline(c, "काल भैरव जयंती", tau, 0.0, 330, 84, RED)
    date_chip(c, "मंगलवार, 1 दिसंबर", tau, 0.35, 445, SAF)
    a = clamp(tau / 1.2)
    rays(c, 540, 760, T, a, n=24, r0=90, r1=360)
    crescent(k, 700, 590, 50, 0.3, 0.9)
    trishul(k, 540, 860, 0.9, 0.1, 1.6)
    damru(k, 540, 690, 0.8, 0.9, 1.6, T)

def s2(c, k, tau, T):
    ct = cap_times(2)
    headline(c, "काशी के कोतवाल", tau, ct[3][0], 330, 84, RED) if tau >= ct[3][0] else headline(c, "शिव का रूप", tau, 0.0, 330, 84, RED)
    temple(k, 540, 880, 1.0, 0.1, 1.8, T)
    ghats(k, 0.5, 1.4, 868)
    flame(c, 300, 960, 0.5, clamp((tau - 1.4) / 0.3), T)
    flame(c, 780, 975, 0.5, clamp((tau - 1.6) / 0.3), T + 1)
    label(c, "काशी", 260, 640, tau, 1.2)
    label(c, "समय के स्वामी", 790, 520, tau, ct[4][0], 40, '#FFF6DA', RED)

def s3(c, k, tau, T):
    headline(c, "विवाह पंचमी", tau, 0.0, 330, 92, RED)
    date_chip(c, "सोमवार, 14 दिसंबर", tau, 0.35, 445, SAF)
    garland(k, 170, 560, 470, 560, 230, 0.2, 1.4)
    garland(k, 610, 560, 910, 560, 230, 0.35, 1.55)
    kalash(k, 540, 830, 0.95, 0.6, 1.8)
    nudge(c, tau, 1.5, 1.7, T)

def s4(c, k, tau, T):
    ct = cap_times(4)
    headline(c, "श्री राम – माता सीता", tau, 0.0, 330, 76, RED)
    mandap(k, 0.1, 2.0, T)
    garland(k, 330, 760, 470, 760, 90, 1.2, 2.0, n=6, r=16)
    garland(k, 610, 760, 750, 760, 90, 1.3, 2.1, n=6, r=16)
    label(c, "जनकपुर", 540, 460, tau, ct[0][0] + 0.6, 44, CREAM, INK)
    if tau >= ct[3][0]:
        label(c, "अयोध्या", 400, 1025, tau, ct[3][0], 40, '#FFF6DA', RED)
        label(c, "जनकपुर", 680, 1025, tau, ct[3][0] + 0.4, 40, '#FFF6DA', RED)

def s5(c, k, tau, T):
    headline(c, "गीता जयंती", tau, 0.0, 330, 92, RED)
    date_chip(c, "रविवार, 20 दिसंबर", tau, 0.35, 445, SAF)
    book(k, 540, 700, 0.2, 2.2, tau)
    peacock_feather(k, 840, 990, 0.85, 0.8, 2.0, T)

def s6(c, k, tau, T):
    ct = cap_times(6)
    headline(c, "कुरुक्षेत्र", tau, 0.0, 330, 92, RED)
    wheel(k, 430, 760, 200, 0.1, 1.6, T)
    flag(k, 760, 930, 0.6, 1.5, T)
    shankh(k, 790, 990, 0.8, 1.0, 2.0)
    if tau >= ct[3][0]:
        label(c, "मोक्षदा एकादशी भी", 540, 460, tau, ct[3][0], 48, '#FFF6DA', RED)

def s7(c, k, tau, T):
    headline(c, "तारीख़ें नोट कर लो", tau, 0.0, 320, 76, RED)
    mini_card(c, k, tau, 230, 590, "1", "काल भैरव", "जयंती", RED, 0.0)
    mini_card(c, k, tau, 540, 590, "14", "विवाह", "पंचमी", SAF, 0.15)
    mini_card(c, k, tau, 850, 590, "20", "गीता", "जयंती", IND, 0.3)
    ct = cap_times(7)
    bl = 0.82 + 0.18 * (0.5 + 0.5 * math.sin(T * 8))
    a1 = clamp((tau - 0.1) / 0.2)
    chip(c, "फ़ैमिली ग्रुप में भेजो", 510, 865, 58, SAF, INK, a1 * (bl if tau > 0.6 else 1), scale=(0.92 + 0.08 * back((tau - 0.1) / 0.3)) * (1 + 0.03 * math.sin(T * 8)))
    t2 = ct[1][0] - 0.1
    chip(c, "सेव कर लो", 510, 990, 48, '#FFF6DA', RED, clamp((tau - t2) / 0.2) * bl, scale=0.9 + 0.1 * back((tau - t2) / 0.3), outline=RED)
    if tau > 0.3:
        ph = ((tau - 0.3) * 0.6) % 1
        px, py = 150 + 700 * ph, 790 - 50 * math.sin(ph * math.pi)
        pl = poly([(px, py), (px - 46, py - 14), (px - 30, py + 4)])
        c.drawPath(pl, skia.Paint(AntiAlias=True, Color=C('#FFFFFF', 230)))
        c.drawPath(pl, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C(INK)))

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7]

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

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        from PIL import Image
        for spec in sys.argv[2:]:
            i, tau = spec.split(':'); i = int(i); tau = float(tau)
            Image.fromarray(frame(i, tau)).convert('RGB').save(f'still_{i}_{tau}.png')
    else:
        for i in map(int, sys.argv[2:]): print(i, render(i))
