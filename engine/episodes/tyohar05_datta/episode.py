"""Tyohar 05: एक भगवान, 24 गुरु — Datta Jayanti (Wed 23 Dec 2026, Margashirsha Purnima). Post 21 Dec. Idea from a viewer comment."""
import sys
sys.path.insert(0, '/home/claude/kitzz.ai/engine/episodes/tyohar_kit')
import kit
from kit import *

LINES = [
    "एक भगवान, जिनके चौबीस गुरु थे! और उनमें, एक अजगर, एक मधुमक्खी, और एक कबूतर भी!",
    "ये हैं भगवान दत्तात्रेय। ब्रह्मा, विष्णु और महेश, तीनों का एक रूप। ऋषि अत्रि, और माता अनसूया के पुत्र।",
    "तीन मुख, छह हाथ, साथ में एक गाय, और चार कुत्ते, जिन्हें चार वेदों का प्रतीक माना जाता है।",
    "उन्होंने प्रकृति को ही गुरु बना लिया। अजगर से सीखा संतोष। जो मिल जाए, उसी में ख़ुश रहना।",
    "मधुमक्खी से सीखा, हर फूल से थोड़ा-थोड़ा लो, किसी एक पर बोझ मत बनो।",
    "और कबूतर से सीखा, कि ज़रूरत से ज़्यादा मोह, दुख ही देता है।",
    "इनकी जयंती है, दत्त जयंती, मार्गशीर्ष पूर्णिमा पर। इस बार, बुधवार, तेईस दिसंबर।",
    "महाराष्ट्र, कर्नाटक और गुजरात में, ये बड़ा पर्व है। गाणगापुर और गिरनार जैसे, दत्त धामों पर, भारी भीड़ जुटती है।",
    "ये रील, उस दोस्त को भेजो, जो हर चीज़ से सीखता है। कमेंट में बताओ, आपका गुरु कौन? क्योंकि, एक भगवान के, चौबीस गुरु थे!",
]
CAPS = [
    ["एक भगवान,", "जिनके 24 गुरु थे!", "एक अजगर, एक मधुमक्खी", "और एक कबूतर भी!"],
    ["ये हैं भगवान दत्तात्रेय", "ब्रह्मा, विष्णु और महेश", "तीनों का एक रूप", "ऋषि अत्रि और", "माता अनसूया के पुत्र"],
    ["तीन मुख, छह हाथ", "साथ में एक गाय", "और चार कुत्ते", "चार वेदों का प्रतीक"],
    ["प्रकृति को ही", "गुरु बना लिया", "अजगर से सीखा — संतोष", "जो मिल जाए,", "उसी में ख़ुश रहना"],
    ["मधुमक्खी से सीखा", "हर फूल से थोड़ा-थोड़ा लो", "किसी एक पर", "बोझ मत बनो"],
    ["और कबूतर से सीखा", "ज़रूरत से ज़्यादा मोह", "दुख ही देता है"],
    ["इनकी जयंती — दत्त जयंती", "मार्गशीर्ष पूर्णिमा पर", "इस बार:", "बुधवार, 23 दिसंबर"],
    ["महाराष्ट्र, कर्नाटक", "और गुजरात में बड़ा पर्व", "गाणगापुर और गिरनार", "जैसे दत्त धामों पर", "भारी भीड़ जुटती है"],
    ["ये रील उस दोस्त को भेजो", "जो हर चीज़ से सीखता है", "कमेंट में बताओ —", "आपका गुरु कौन?", "क्योंकि एक भगवान के", "24 गुरु थे!"],
]
BELLS = [1, 6]
SNAKE = '#5E8A3A'; PIGEON = '#8E9BB0'; BEE = '#F2C230'

# ---------------- art ----------------
def head(k, x, y, s, t0, t1, crown=GOLD):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    k.shape(oval(x - 60 * s, y + 8 * s, 12 * s, 22 * s), *T(0.0, 0.3), fill=SKIN, w=4 * s)
    k.shape(oval(x + 60 * s, y + 8 * s, 12 * s, 22 * s), *T(0.0, 0.3), fill=SKIN, w=4 * s)
    k.shape(oval(x, y, 60 * s, 74 * s), *T(0.0, 0.4), fill=SKIN, w=5 * s)
    # jata-mukut
    k.shape(P(('M', x - 58 * s, y - 50 * s), ('Q', x - 60 * s, y - 120 * s, x - 20 * s, y - 150 * s), ('Q', x, y - 190 * s, x + 20 * s, y - 150 * s),
              ('Q', x + 60 * s, y - 120 * s, x + 58 * s, y - 50 * s), ('Z',)), *T(0.25, 0.6), fill=crown, w=5 * s)
    k.shape(rrect(x - 60 * s, y - 64 * s, x + 60 * s, y - 44 * s, 6 * s), *T(0.35, 0.6), fill=RED, w=4 * s)
    k.shape(circ(x, y - 108 * s, 11 * s), *T(0.45, 0.65), fill=RED, w=3 * s)
    for sx in (-1, 1):
        ex = x + sx * 25 * s
        k.shape(P(('M', ex - sx * 20 * s, y - 4 * s), ('Q', ex, y - 18 * s, ex + sx * 18 * s, y - 6 * s), ('Q', ex, y + 6 * s, ex - sx * 20 * s, y - 4 * s), ('Z',)), *T(0.5, 0.75), fill='#FFFDF5', w=3.5 * s)
        k.shape(circ(ex + sx * 2 * s, y - 6 * s, 6 * s), *T(0.6, 0.8), fill=INK, w=0)
        k.shape(P(('M', ex - sx * 22 * s, y - 24 * s), ('Q', ex, y - 36 * s, ex + sx * 22 * s, y - 26 * s)), *T(0.55, 0.8), w=4.5 * s)
    k.shape(P(('M', x, y - 2 * s), ('Q', x - 7 * s, y + 22 * s, x, y + 28 * s), ('Q', x + 6 * s, y + 30 * s, x + 9 * s, y + 25 * s)), *T(0.6, 0.85), w=3.5 * s)
    k.shape(P(('M', x - 16 * s, y + 46 * s), ('Q', x, y + 56 * s, x + 16 * s, y + 46 * s)), *T(0.65, 0.9), w=4 * s, col=RED)
    k.shape(P(('M', x - 8 * s, y - 32 * s), ('L', x, y - 52 * s), ('L', x + 8 * s, y - 32 * s)), *T(0.6, 0.85), w=4 * s, col=RED)

def mala(k, x, y, r, t0, t1):
    for i in range(14):
        a = i * 2 * math.pi / 14
        k.shape(circ(x + math.cos(a) * r, y + math.sin(a) * r * 1.3, 7), t0 + (t1 - t0) * i / 20, t1, fill='#8A5A2B', w=2)

def kamandalu(k, x, y, s, t0, t1):
    k.shape(P(('M', x - 40 * s, y - 30 * s), ('Q', x - 70 * s, y + 40 * s, x, y + 50 * s), ('Q', x + 70 * s, y + 40 * s, x + 40 * s, y - 30 * s), ('Z',)), t0, t1, fill='#B5562B', w=4)
    k.shape(P(('M', x + 40 * s, y - 20 * s), ('Q', x + 80 * s, y - 30 * s, x + 90 * s, y - 60 * s)), t0 + 0.1, t1, w=6, col=INK)
    k.shape(P(('M', x - 30 * s, y - 30 * s), ('Q', x, y - 80 * s, x + 30 * s, y - 30 * s)), t0 + 0.15, t1, w=5, col=GOLD)

def datta(k, t0, dur, tt, hi=None):
    """original folk-style Dattatreya in local box ~ x 0..600, y -40..720 (3 heads, 6 arms, lotus seat)."""
    T = lambda a, b: (t0 + dur * a, t0 + dur * b)
    k.shape(circ(300, 240, 250), *T(0.0, 0.15), fill=GOLDL, w=6)
    for i in range(28):
        a = i * math.pi / 14
        k.shape(circ(300 + math.cos(a) * 250, 240 + math.sin(a) * 250, 12), *T(0.04 + i * 0.003, 0.18), fill=SAF, w=3)
    # lotus seat
    for i, dx in enumerate([-160, -96, -32, 32, 96, 160]):
        k.shape(P(('M', 300 + dx - 50, 700), ('Q', 300 + dx, 606, 300 + dx + 50, 700), ('Z',)), *T(0.1 + i * 0.01, 0.26), fill=PINK, w=4)
    k.shape(oval(300, 706, 230, 26), *T(0.12, 0.26), fill='#C9596A', w=5)
    k.shape(P(('M', 160, 650), ('Q', 165, 568, 240, 552), ('L', 360, 552), ('Q', 435, 568, 440, 650), ('Q', 300, 684, 160, 650), ('Z',)), *T(0.14, 0.3), fill=SAF, w=5)
    k.shape(P(('M', 175, 638), ('Q', 300, 666, 425, 638)), *T(0.26, 0.34), w=5, col=RED)
    # torso + robe
    k.shape(P(('M', 205, 362), ('Q', 300, 340, 395, 362), ('Q', 392, 460, 362, 556), ('L', 238, 556), ('Q', 208, 460, 205, 362), ('Z',)), *T(0.18, 0.34), fill=SKIN, w=5)
    k.shape(P(('M', 210, 370), ('Q', 262, 480, 348, 556), ('L', 392, 556), ('Q', 332, 460, 262, 355), ('Z',)), *T(0.24, 0.38), fill=SAF, w=4)
    mala(k, 300, 410, 36, *T(0.3, 0.42))
    # six arms: upper (raised), middle (out), lower (lap)
    arms = [((212, 380), (120, 300), (96, 210)), ((388, 380), (480, 300), (504, 210)),
            ((210, 400), (110, 420), (60, 470)), ((390, 400), (490, 420), (540, 470)),
            ((214, 420), (170, 520), (236, 556)), ((386, 420), (430, 520), (364, 556))]
    for j, (a, b, e) in enumerate(arms):
        k.tube(P(('M', *a), ('Q', *b, *e)), *T(0.32 + j * 0.025, 0.46 + j * 0.025), SKIN, 30)
        k.shape(P(('M', b[0] - 14, b[1] - 6), ('L', b[0] + 14, b[1] + 6)), *T(0.46 + j * 0.02, 0.56), w=6, col=GOLD)
    # attributes
    trishul(k, 96, 330, 0.42, *T(0.52, 0.66))
    wheel(k, 504, 190, 52, *T(0.52, 0.68), tt)
    shankh(k, 60, 470, 0.42, *T(0.56, 0.7))
    damru(k, 540, 470, 0.55, *T(0.56, 0.7), tt)
    kamandalu(k, 236, 566, 0.55, *T(0.6, 0.72))
    # three heads (side heads behind, slightly smaller)
    head(k, 178, 260, 0.78, *T(0.62, 0.8), crown=GOLD)
    head(k, 422, 260, 0.78, *T(0.66, 0.84), crown=GOLD)
    head(k, 300, 236, 1.0, *T(0.7, 0.92), crown=GOLD)
    return {'L': (178, 110), 'C': (300, 40), 'R': (422, 110)}

def cow(k, x, y, s, t0, t1):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    for lx in (-90, -55, 55, 90):
        k.tube(P(('M', x + lx * s, y + 30 * s), ('L', x + lx * s, y + 120 * s)), *T(0.2, 0.5), '#FFFBEF', 14 * s)
    k.shape(oval(x, y, 130 * s, 62 * s), *T(0, 0.45), fill='#FFFBEF', w=5)
    k.shape(oval(x - 30 * s, y - 10 * s, 30 * s, 22 * s), *T(0.3, 0.55), fill='#C9AE82', w=3)
    k.shape(P(('M', x + 120 * s, y - 30 * s), ('Q', x + 170 * s, y - 70 * s, x + 200 * s, y - 40 * s), ('Q', x + 215 * s, y + 10 * s, x + 180 * s, y + 20 * s),
              ('Q', x + 150 * s, y + 10 * s, x + 120 * s, y + 10 * s), ('Z',)), *T(0.35, 0.6), fill='#FFFBEF', w=5)
    k.shape(P(('M', x + 165 * s, y - 60 * s), ('Q', x + 160 * s, y - 100 * s, x + 140 * s, y - 108 * s)), *T(0.5, 0.7), w=6, col='#8A5A2B')
    k.shape(P(('M', x + 190 * s, y - 52 * s), ('Q', x + 205 * s, y - 92 * s, x + 225 * s, y - 100 * s)), *T(0.5, 0.7), w=6, col='#8A5A2B')
    k.shape(circ(x + 182 * s, y - 26 * s, 6 * s), *T(0.6, 0.75), fill=INK, w=0)
    k.shape(P(('M', x - 128 * s, y - 10 * s), ('Q', x - 170 * s, y + 30 * s, x - 150 * s, y + 90 * s)), *T(0.6, 0.8), w=4)
    k.shape(rrect(x + 150 * s, y + 18 * s, x + 185 * s, y + 32 * s, 6), *T(0.6, 0.8), fill=RED, w=3)

def dog(k, x, y, s, t0, t1, col='#C98A4B', flip=1, tt=0):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    f = flip
    k.shape(oval(x, y, 54 * s, 30 * s), *T(0, 0.45), fill=col, w=4)
    for lx in (-34, -14, 18, 36):
        k.tube(P(('M', x + lx * s, y + 18 * s), ('L', x + lx * s, y + 60 * s)), *T(0.2, 0.5), col, 9 * s)
    hx = x + f * 58 * s; hy = y - 32 * s
    k.shape(circ(hx, hy, 26 * s), *T(0.3, 0.6), fill=col, w=4)
    k.shape(P(('M', hx + f * 18 * s, hy + 2 * s), ('L', hx + f * 44 * s, hy + 10 * s), ('L', hx + f * 20 * s, hy + 20 * s), ('Z',)), *T(0.4, 0.65), fill=col, w=4)
    k.shape(P(('M', hx - f * 12 * s, hy - 18 * s), ('Q', hx - f * 30 * s, hy, hx - f * 18 * s, hy + 18 * s)), *T(0.45, 0.7), fill=INK, w=3)
    k.shape(circ(hx + f * 8 * s, hy - 6 * s, 4 * s), *T(0.5, 0.7), fill=INK, w=0)
    wag = math.sin(tt * 12) * 14 * s
    k.shape(P(('M', x - f * 52 * s, y - 8 * s), ('Q', x - f * 80 * s, y - 30 * s, x - f * 78 * s, y - 56 * s + wag)), *T(0.5, 0.8), w=6, col=INK)

def python_(k, x, y, s, t0, t1, tt):
    pth = skia.Path(); n = 120; pts = []
    for i in range(n + 1):
        u = i / n; a = u * 2.6 * 2 * math.pi; r = (40 + 150 * u) * s
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r * 0.55))
    pts = pts[::-1]
    pth.moveTo(*pts[0])
    for q in pts[1:]: pth.lineTo(*q)
    k.tube(pth, t0, t0 + (t1 - t0) * 0.6, SNAKE, 34 * s)
    p = clamp((k.t - t0 - (t1 - t0) * 0.5) / ((t1 - t0) * 0.3))
    for j in range(0, n, 6):
        if j / n < p: k.c.drawCircle(*pts[j], 6 * s, skia.Paint(AntiAlias=True, Color=C('#E8D47A', 230)))
    # head rising from centre (end of spiral)
    hx, hy = pts[-1][0] + 10 * s, pts[-1][1] - 60 * s
    k.tube(P(('M', *pts[-1]), ('Q', pts[-1][0] - 30 * s, pts[-1][1] - 40 * s, hx, hy)), t0 + (t1 - t0) * 0.55, t0 + (t1 - t0) * 0.75, SNAKE, 34 * s)
    k.shape(oval(hx + 20 * s, hy - 8 * s, 42 * s, 26 * s), t0 + (t1 - t0) * 0.7, t1, fill=SNAKE, w=4)
    k.shape(circ(hx + 30 * s, hy - 16 * s, 6 * s), t0 + (t1 - t0) * 0.8, t1, fill='#FFF6DA', w=2)
    k.shape(circ(hx + 31 * s, hy - 16 * s, 3 * s), t0 + (t1 - t0) * 0.85, t1, fill=INK, w=0)
    if k.t > t1 and math.sin(tt * 6) > 0.2:
        k.shape(P(('M', hx + 60 * s, hy - 4 * s), ('L', hx + 86 * s, hy - 2 * s), ('L', hx + 98 * s, hy - 12 * s), ('M', hx + 86 * s, hy - 2 * s), ('L', hx + 98 * s, hy + 8 * s)), 0, 0.01, w=3, col=RED)

def flower(k, x, y, s, t0, t1, col=PINK):
    k.tube(P(('M', x, y), ('Q', x - 10 * s, y + 90 * s, x, y + 180 * s)), t0, t0 + (t1 - t0) * 0.4, GRN, 8 * s)
    k.shape(P(('M', x, y + 100 * s), ('Q', x + 50 * s, y + 70 * s, x + 60 * s, y + 110 * s), ('Q', x + 30 * s, y + 120 * s, x, y + 100 * s), ('Z',)), t0 + 0.1, t1, fill=GRN, w=3)
    for i in range(6):
        a = i * math.pi / 3
        k.shape(circ(x + math.cos(a) * 30 * s, y + math.sin(a) * 30 * s, 24 * s), t0 + (t1 - t0) * (0.3 + i * 0.05), t1, fill=col, w=3)
    k.shape(circ(x, y, 18 * s), t0 + (t1 - t0) * 0.7, t1, fill=GOLD, w=3)

def bee(c, x, y, s, ang, tt, a=1):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    k = Ink(c, 99)
    flap = 0.6 + 0.4 * abs(math.sin(tt * 40))
    for sx in (-1, 1):
        c.drawOval(skia.Rect(-10 + sx * 2, -40 * flap - 6, 22, -6), skia.Paint(AntiAlias=True, Color=C('#DDEFFF', 200 * a)))
    k.shape(oval(0, 0, 34, 22), 0, 0.01, fill=BEE, w=4)
    for dx in (-10, 6):
        k.shape(P(('M', dx, -20), ('Q', dx + 5, 0, dx, 20)), 0, 0.01, w=7, col=INK)
    k.shape(circ(34, -2, 12), 0, 0.01, fill=INK, w=0)
    c.restore()

def pigeon(k, x, y, s, t0, t1, flip=1, col=PIGEON):
    T = lambda a, b: (t0 + (t1 - t0) * a, t0 + (t1 - t0) * b)
    f = flip
    k.shape(P(('M', x - f * 70 * s, y), ('Q', x - f * 60 * s, y - 50 * s, x + f * 10 * s, y - 46 * s), ('Q', x + f * 60 * s, y - 40 * s, x + f * 60 * s, y),
              ('Q', x + f * 40 * s, y + 40 * s, x - f * 20 * s, y + 36 * s), ('L', x - f * 110 * s, y + 20 * s), ('Z',)), *T(0, 0.5), fill=col, w=4)
    k.shape(P(('M', x - f * 40 * s, y - 20 * s), ('Q', x + f * 10 * s, y - 34 * s, x + f * 30 * s, y)), *T(0.3, 0.6), w=3, col='#5E6B80')
    k.shape(circ(x + f * 62 * s, y - 52 * s, 26 * s), *T(0.3, 0.6), fill=col, w=4)
    k.shape(P(('M', x + f * 48 * s, y - 30 * s), ('Q', x + f * 66 * s, y - 20 * s, x + f * 60 * s, y - 6 * s)), *T(0.4, 0.65), w=8, col='#6FA88F')
    k.shape(poly([(x + f * 86 * s, y - 56 * s), (x + f * 104 * s, y - 50 * s), (x + f * 86 * s, y - 46 * s)]), *T(0.45, 0.7), fill=SAF, w=2)
    k.shape(circ(x + f * 70 * s, y - 58 * s, 5 * s), *T(0.5, 0.7), fill=INK, w=0)
    for lx in (-6, 12):
        k.shape(P(('M', x + f * lx * s, y + 34 * s), ('L', x + f * lx * s, y + 56 * s)), *T(0.5, 0.75), w=4, col=RED)

def heart(k, x, y, s, t0, t1, crack=None):
    k.shape(P(('M', x, y + 50 * s), ('C', x - 90 * s, y - 10 * s, x - 50 * s, y - 70 * s, x, y - 30 * s),
              ('C', x + 50 * s, y - 70 * s, x + 90 * s, y - 10 * s, x, y + 50 * s), ('Z',)), t0, t1, fill=RED, w=5)
    if crack is not None:
        k.shape(P(('M', x + 4 * s, y - 30 * s), ('L', x - 10 * s, y - 6 * s), ('L', x + 10 * s, y + 10 * s), ('L', x - 4 * s, y + 40 * s)), crack, crack + 0.35, w=6, col=CREAM)

def branch(k, t0, t1, y=900):
    k.tube(P(('M', 120, y + 20), ('Q', 540, y - 30, 960, y + 10)), t0, t1, '#8A5A2B', 18)
    for x, d in [(260, -1), (480, 1), (760, -1)]:
        k.shape(P(('M', x, y), ('Q', x + 30, y - 40 * d, x + 80, y - 30 * d), ('Q', x + 40, y - 6 * d, x, y), ('Z',)), t0 + 0.2, t1, fill=GRN, w=3)

def badge24(c, tau, t0, x, y, sc=1.0, T=0):
    a = clamp((tau - t0) / 0.2)
    if a <= 0: return
    c.save(); c.translate(x, y); c.scale(sc * (0.85 + 0.15 * back((tau - t0) / 0.35)), sc * (0.85 + 0.15 * back((tau - t0) / 0.35)))
    c.drawCircle(0, 0, 92, skia.Paint(AntiAlias=True, Color=C(RED, 255 * a)))
    c.drawCircle(0, 0, 92, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C(GOLD, 255 * a)))
    draw_text(c, "24", 0, -12, F_Y, 92, CREAM, alpha=a, stroke=4, sfill=INK)
    draw_text(c, "गुरु", 0, 52, F_HB, 38, GOLDL, alpha=a)
    c.restore()

# ---------------- scenes ----------------
def s0(c, k, tau, T):
    headline(c, "1 भगवान…", tau, 0.0, 330, 96, INK)
    badge24(c, tau, 0.15, 540, 500, 1.15)
    ct = cap_times(0); t2 = ct[2][0]
    c.save(); c.translate(250, 840); c.scale(0.72, 0.72); python_(Ink(c, tau), 0, 0, 1.0, t2 - 0.1, t2 + 0.7, T); c.restore()
    c.save(); c.translate(540, 720); c.scale(0.72, 0.72); kk = Ink(c, tau); flower(kk, 0, 0, 1.0, t2 + 0.2, t2 + 0.8); c.restore()
    bee(c, 540 + 80 * math.cos(T * 3), 650 + 30 * math.sin(T * 5), 1.4, 0, T, clamp((tau - t2 - 0.5) / 0.2))
    pigeon(k, 830, 860, 1.2, ct[3][0] - 0.1, ct[3][0] + 0.5, flip=-1)
    map_chip(c, "अजगर", 260, 1000, tau, t2 + 0.3, 40, '#DDEBC8', INK)
    map_chip(c, "मधुमक्खी", 540, 1000, tau, t2 + 0.7, 40, '#FBE7A1', INK)
    map_chip(c, "कबूतर", 820, 1000, tau, ct[3][0] + 0.2, 40, '#DCE3EE', INK)

def s1(c, k, tau, T):
    headline(c, "भगवान दत्तात्रेय", tau, 0.0, 320, 84, RED)
    c.save(); c.translate(540 - 300 * 0.95, 450); c.scale(0.95, 0.95)
    kk = Ink(c, tau); datta(kk, 0.1, 2.4, T)
    c.restore()
    ct = cap_times(1); t1 = ct[1][0]
    for j, (n, x, y, col) in enumerate([("ब्रह्मा", 290, 470, '#F6D28A'), ("विष्णु", 540, 412, '#AFC4E8'), ("महेश", 790, 470, '#F2B9A6')]):
        map_chip(c, n, x, y, tau, t1 + j * 0.35, 40, col, INK)
    label(c, "ऋषि अत्रि + माता अनसूया", 540, 1000, tau, ct[3][0], 42, '#FFF6DA', RED)

def s2(c, k, tau, T):
    headline(c, "3 मुख · 6 हाथ", tau, 0.0, 320, 88, RED)
    ct = cap_times(2)
    cow(k, 560, 640, 0.85, ct[1][0] - 0.2, ct[1][0] + 0.6)
    c.save(); c.translate(270 - 300 * 0.55, 380); c.scale(0.55, 0.55); kk = Ink(c, 10); datta(kk, 0, 1, T); c.restore()
    for j, x in enumerate([170, 390, 610, 830]):
        dog(k, x, 900, 0.85, ct[2][0] - 0.1 + j * 0.15, ct[2][0] + 0.5 + j * 0.15, ['#C98A4B', '#F3E6C8', '#6B4A2B', '#B9A27A'][j], 1 if j % 2 else -1, T + j)
    for j, (x, v) in enumerate(zip([170, 390, 610, 830], ["ऋग्", "यजु", "साम", "अथर्व"])):
        label(c, v, x, 1010, tau, ct[3][0] + j * 0.12, 36, '#FFF6DA', IND)

def s3(c, k, tau, T):
    headline(c, "गुरु: अजगर", tau, 0.0, 320, 92, RED)
    ct = cap_times(3)
    c.save(); c.translate(540, 700); kk = Ink(c, tau); python_(kk, 0, 0, 1.2, 0.2, 1.6, T); c.restore()
    label(c, "सीख: संतोष", 540, 450, tau, ct[2][0], 52, '#FFF6DA', GRN)
    label(c, "जो मिले, उसी में ख़ुश", 540, 900, tau, ct[3][0], 42, CREAM, INK)

def s4(c, k, tau, T):
    headline(c, "गुरु: मधुमक्खी", tau, 0.0, 320, 88, RED)
    xs = [(220, 640, PINK), (420, 560, SAF), (640, 640, '#B98ADB'), (850, 580, PINK)]
    for j, (x, y, col) in enumerate(xs):
        c.save(); c.translate(x, y); c.scale(0.8, 0.8); flower(Ink(c, tau), 0, 0, 1.0, 0.1 + j * 0.2, 0.7 + j * 0.2, col); c.restore()
    # bee hops flower to flower
    u = (tau * 0.55) % len(xs); i0 = int(u); fr = eio(u - i0); i1 = (i0 + 1) % len(xs)
    bx = xs[i0][0] + (xs[i1][0] - xs[i0][0]) * fr; by = xs[i0][1] - 60 + (xs[i1][1] - xs[i0][1]) * fr - 70 * math.sin(math.pi * fr)
    bee(c, bx, by, 1.2, 0 if xs[i1][0] >= xs[i0][0] else 180, T, clamp((tau - 0.6) / 0.2))
    ct = cap_times(4)
    label(c, "थोड़ा-थोड़ा लो", 540, 860, tau, ct[1][0], 52, '#FBE7A1', INK)
    label(c, "बोझ मत बनो", 540, 1000, tau, ct[3][0], 46, '#FFF6DA', RED)

def s5(c, k, tau, T):
    headline(c, "गुरु: कबूतर", tau, 0.0, 320, 92, RED)
    branch(k, 0.1, 0.8, 760)
    pigeon(k, 400, 700, 1.0, 0.3, 1.0, 1)
    pigeon(k, 690, 700, 1.0, 0.5, 1.2, -1)
    ct = cap_times(5)
    heart(k, 545, 510, 0.9, ct[1][0] - 0.1, ct[1][0] + 0.4, crack=ct[2][0])
    label(c, "ज़्यादा मोह = दुख", 540, 1000, tau, ct[2][0] + 0.1, 50, '#FFF6DA', RED)

def s6(c, k, tau, T):
    headline(c, "दत्त जयंती", tau, 0.0, 320, 100, RED)
    full_moon(k, 820, 520, 90, 0.2, 0.9)
    label(c, "मार्गशीर्ष पूर्णिमा", 540, 440, tau, cap_times(6)[1][0], 44, '#FFF6DA', IND)
    c.save(); c.translate(430, 720); c.scale(1.35, 1.35); c.translate(-430, -720)
    mini_card(c, k, tau, 430, 720, "23", "2026", "", RED, 0.3, hdr="दिसंबर")
    c.restore()
    date_chip(c, "बुधवार", tau, cap_times(6)[3][0], 1000, SAF)
    diya(k, 830, 860, 0.8, 0.6, 1.0, T)

def s7(c, k, tau, T):
    headline(c, "दत्त धाम", tau, 0.0, 320, 100, RED)
    ct = cap_times(7)
    for j, (n, x) in enumerate([("महाराष्ट्र", 230), ("कर्नाटक", 540), ("गुजरात", 850)]):
        map_chip(c, n, x, 440, tau, 0.15 + j * 0.3, 40, [SAF, GOLDL, '#9FC08A'][j], INK)
    temple(k, 300, 900, 1.0, ct[2][0] - 0.3, ct[2][0] + 0.8, T)
    temple(k, 780, 900, 1.0, ct[2][0] + 0.1, ct[2][0] + 1.2, T)
    label(c, "गाणगापुर", 300, 1000, tau, ct[2][0] + 0.2, 42, '#FFF6DA', RED)
    label(c, "गिरनार", 780, 1000, tau, ct[2][0] + 0.6, 42, '#FFF6DA', RED)
    garland(k, 140, 520, 940, 520, 70, 0.3, 1.4, n=11, r=18)

def s8(c, k, tau, T):
    headline(c, "आपका गुरु कौन?", tau, 0.0, 320, 84, RED)
    badge24(c, tau, 0.1, 540, 520, 0.95)
    bee(c, 300 + 40 * math.cos(T * 3), 520 + 20 * math.sin(T * 4), 0.9, 0, T, clamp((tau - 0.3) / 0.2))
    pigeon(k, 800, 560, 0.6, 0.3, 0.8, -1)
    bl = 0.82 + 0.18 * (0.5 + 0.5 * math.sin(T * 8))
    a1 = clamp((tau - 0.2) / 0.2)
    chip(c, "उस दोस्त को भेजो 📲".replace(" 📲", ""), 510, 770, 58, SAF, INK, a1 * (bl if tau > 0.7 else 1),
         scale=(0.92 + 0.08 * back((tau - 0.2) / 0.3)) * (1 + 0.03 * math.sin(T * 8)))
    draw_text(c, "जो हर चीज़ से सीखता है", 510, 862, F_HB, 44, INK, alpha=clamp((tau - 0.5) / 0.2))
    ct = cap_times(8); t3 = ct[2][0]
    chip(c, "कमेंट: आपका गुरु कौन?", 510, 990, 46, '#FFF6DA', RED, clamp((tau - t3) / 0.2) * bl, scale=0.9 + 0.1 * back((tau - t3) / 0.3), outline=RED)

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8]
SCRATCH = []

if __name__ == '__main__':
    kit.init('durs.json', CAPS, SCENES); kit.main()
