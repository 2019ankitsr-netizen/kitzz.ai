import sys, json, subprocess, os, math
from eng import *

durs = json.load(open('durs.json'))
PAD0, PADE = 0.12, 0.28
D = [d + PAD0 + PADE for d in durs]
D[0] = durs[0] + PAD0 + 0.2
D[-1] += 0.7
START = [sum(D[:i]) for i in range(len(D))]

CAPS = [
    [],
    ["मान्यता है,", "ब्रह्मा जी की काया से प्रकट हुए", "हाथ में कलम-दवात लिए", "भगवान चित्रगुप्त"],
    ["यमराज के दरबार में,", "हर इंसान के कर्मों का", "लेखा-जोखा यही रखते हैं"],
    ["इसीलिए कायस्थ परिवार,", "पूजा होने तक,", "कलम और बही को आराम देते हैं"],
    ["इस साल चित्रगुप्त पूजा है", "बुधवार, 11 नवंबर", "भाई दूज के दिन"],
    ["पूजा में रखिए —", "नई कलम, दवात,", "कोरा कागज़ और बही"],
    ["तिलक लगाइए,", "फूल, अक्षत और दीया चढ़ाइए"],
    ["फिर नई कलम से लिखिए —", "ॐ चित्रगुप्ताय नमः"],
    ["ये रील अपने कायस्थ दोस्त को भेजिए", "और सेव कीजिए", "क्योंकि पूजा के बाद ही", "फिर कलम चलती है"],
]

def cap_times(i):
    ch = CAPS[i]; tot = sum(len(x) for x in ch); out = []; t = PAD0
    for x in ch:
        d = durs[i] * len(x) / tot; out.append((t, t + d, x)); t += d
    return out

def wrap(txt, size=54, maxw=760):
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
            cy = 1150
            c.save(); c.translate(520, cy); c.scale(0.9 + 0.1 * pop, 0.9 + 0.1 * pop)
            r = skia.Rect(-bw / 2, -bh / 2, bw / 2, bh / 2)
            c.drawRRect(skia.RRect.MakeRectXY(r, 26, 26), skia.Paint(AntiAlias=True, Color=C(INK, 230)))
            for j, l in enumerate(lines):
                draw_text(c, l, 0, -bh / 2 + 12 + lh * j + lh / 2, F_HB, 54, CREAM)
            c.restore()

def headline(c, txt, tau, t0=0.0, y=330, size=70, col=RED):
    a = clamp((tau - t0) / 0.15)
    if a > 0: draw_text(c, txt, 540, y, F_Y, size, col, alpha=a, scale=0.85 + 0.15 * back((tau - t0) / 0.3), stroke=5, sfill=CREAM)

# ---------------- scenes ----------------
def s0(c, k, tau, T):
    headline(c, "दिवाली के बाद", tau, 0.0, 330, 92, RED)
    headline(c, "कलम क्यों रख दी जाती है?", tau, 0.12, 445, 72, INK)
    c.save(); c.translate(0, 80)
    # open bahi
    k.shape(P(('M', 540, 640), ('Q', 390, 610, 240, 630), ('L', 240, 920), ('Q', 390, 900, 540, 930), ('Z',)), 0.05, 0.6, fill=CREAM, w=6)
    k.shape(P(('M', 540, 640), ('Q', 690, 610, 840, 630), ('L', 840, 920), ('Q', 690, 900, 540, 930), ('Z',)), 0.1, 0.65, fill=CREAM, w=6)
    k.shape(P(('M', 540, 640), ('L', 540, 930)), 0.1, 0.6, w=6, col=RED)
    for i in range(5):
        y = 690 + i * 48
        k.shape(P(('M', 270, y), ('Q', 400, y - 10, 515, y + 4)), 0.3 + i * 0.05, 0.8, w=3, col='#B9A27A')
    # writing on right page that stops mid-way
    wr = clamp((tau - 0.55) / 1.0)
    stop = 0.62
    wr = min(wr, stop)
    pth = skia.Path(); pth.moveTo(580, 700)
    for j in range(1, 60): pth.lineTo(580 + j * 4, 700 + 6 * math.sin(j * 1.3))
    pp = k.partial(pth, wr / 1.0 if wr > 0 else 0.0001)
    if wr > 0: c.drawPath(pp, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(INK), StrokeCap=skia.Paint.kRound_Cap))
    tipx = 580 + 236 * wr
    lift = 40 * eio((tau - 1.7) / 0.5)
    k2 = Ink(c, tau)
    quill(k2, tipx, 700 - lift, tipx + 160, 700 - lift - 190, 0.0, 0.5)
    inkpot(k, 190, 1000, 0.95, 0.3, 0.9)
    diya(k, 830, 1010, 0.9, 0.35, 0.9, T)
    # question marks bobbing
    for i, (qx, qy) in enumerate([(640, 580), (900, 640), (560, 560)]):
        a = clamp((tau - 1.9 - i * 0.15) / 0.2)
        if a > 0:
            draw_text(c, "?", qx, qy + 10 * math.sin(T * 4 + i), F_Y, 80 - i * 12, SAF, alpha=a, stroke=4, sfill=INK)
    c.restore()

def s1(c, k, tau, T):
    ra = clamp(tau / 1.6) * (1 - clamp((tau - 3.0) / 1.2))
    if ra > 0:
        rays(c, 540, 700, T, ra)
        g = skia.Paint(AntiAlias=True, Color=C('#FFE7A8', 200 * ra)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
        c.drawCircle(540, 700, 150, g)
    if tau < 4.7: headline(c, "ब्रह्मा जी की काया से…", tau, 0.1, 330, 66, RED)
    else: headline(c, "भगवान चित्रगुप्त", tau, 4.7, 330, 84, RED)
    place(c, 540 - 300 * 0.9, 410, 0.9)
    kk = Ink(c, tau); chitragupta(kk, 1.1, 4.4, T)
    c.restore()

def s2(c, k, tau, T):
    headline(c, "कर्मों का लेखा-जोखा", tau, 0.0, 330, 76, RED)
    un = ease(tau / 0.9); ybot = 440 + 590 * un
    p = skia.Paint(AntiAlias=True, Color=C(CREAM)); c.drawRect(skia.Rect(200, 450, 880, ybot), p)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(INK)); c.drawRect(skia.Rect(200, 450, 880, ybot), p)
    for yy in [440, ybot]:
        r = skia.Rect(170, yy - 20, 910, yy + 20)
        c.drawRRect(skia.RRect.MakeRectXY(r, 18, 18), skia.Paint(AntiAlias=True, Color=C('#8A5A2B')))
        c.drawRRect(skia.RRect.MakeRectXY(r, 18, 18), p)
    c.save(); c.clipRect(skia.Rect(200, 460, 880, ybot - 20))
    draw_text(c, "अच्छे कर्म", 370, 520, F_HB, 48, GRN, alpha=clamp((tau - 0.7) / 0.2))
    draw_text(c, "बुरे कर्म", 710, 520, F_HB, 48, RED, alpha=clamp((tau - 0.8) / 0.2))
    k.shape(P(('M', 540, 490), ('L', 540, 1000)), 0.8, 1.3, w=4)
    k.shape(P(('M', 220, 565), ('L', 860, 565)), 0.8, 1.3, w=4)
    tip = None
    rows = 4
    for i in range(rows):
        y = 640 + i * 95
        for side in (0, 1):
            t0 = 1.2 + (i * 2 + side) * 0.5; t1 = t0 + 0.45
            x0 = 230 if side == 0 else 570
            if side == 0:
                k.shape(P(('M', x0 + 8, y), ('L', x0 + 24, y + 18), ('L', x0 + 52, y - 20)), t0, t0 + 0.15, w=7, col=GRN)
            else:
                k.shape(P(('M', x0 + 8, y - 16), ('L', x0 + 40, y + 16), ('M', x0 + 40, y - 16), ('L', x0 + 8, y + 16)), t0, t0 + 0.15, w=7, col=RED)
            pr = clamp((tau - t0 - 0.12) / 0.33)
            if pr > 0:
                pth = skia.Path(); pth.moveTo(x0 + 75, y)
                n = 40 if side == 0 else 36
                for j in range(1, n): pth.lineTo(x0 + 75 + j * 5, y + 5 * math.sin(j * 1.5 + i + side))
                c.drawPath(k.partial(pth, pr), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C(INK), StrokeCap=skia.Paint.kRound_Cap))
                if pr < 1: tip = (x0 + 75 + pr * (n - 1) * 5, y)
    c.restore()
    if tip:
        k2 = Ink(c, 10); quill(k2, tip[0], tip[1], tip[0] + 130, tip[1] - 210, 0, 1)

def s3(c, k, tau, T):
    headline(c, "पूजा तक, कलम को आराम", tau, 0.0, 330, 70, RED)
    # chowki
    k.shape(rrect(200, 880, 880, 920, 8), 0.0, 0.5, fill='#8A5A2B', w=5)
    for x in [240, 820]:
        k.shape(rrect(x - 16, 918, x + 16, 1010, 4), 0.1, 0.6, fill='#6E4420', w=5)
    k.shape(P(('M', 200, 900), ('L', 880, 900)), 0.3, 0.6, w=3, col=GOLD)
    bahi(k, 430, 830, 360, 90, 0.2, 0.8)
    bahi(k, 430, 740, 330, 90, 0.35, 0.95)
    # red mauli thread around stack
    k.shape(P(('M', 330, 690), ('Q', 320, 790, 335, 872)), 0.8, 1.2, w=7, col='#C0262B')
    k.shape(P(('M', 525, 690), ('Q', 535, 790, 522, 872)), 0.85, 1.25, w=7, col='#C0262B')
    # pen lying on top
    k2 = Ink(c, tau)
    quill(k2, 260, 668, 610, 640, 0.6, 1.2)
    inkpot(k, 740, 820, 0.95, 0.5, 1.0)
    k.shape(P(('M', 712, 784), ('Q', 740, 760, 768, 784), ('Z',)), 1.0, 1.3, fill=GOLD, w=4)  # lid
    # sleepy z's
    for i in range(3):
        ph = (T * 0.6 + i / 3) % 1
        a = clamp((tau - 1.3) / 0.3) * math.sin(ph * math.pi)
        if a > 0: draw_text(c, "z", 620 + 40 * i + 30 * ph, 600 - 160 * ph, F_HB, 48 + 16 * i, IND, alpha=a)
    # mid-reel save nudge (bigger, blinking, longer)
    a = clamp((tau - 2.0) / 0.2) * (1 - clamp((tau - 4.9) / 0.3))
    if a > 0:
        bl = 0.85 + 0.15 * math.sin(T * 9)
        chip(c, "सेव करो — पूजा के दिन काम आएगा", 520, 1000, 46, '#FFF6DA', RED, a * bl, scale=0.9 + 0.1 * back((tau - 2.0) / 0.3), outline=RED)

def s4(c, k, tau, T):
    headline(c, "कब है पूजा?", tau, 0.0, 330, 76, RED)
    k.shape(rrect(200, 430, 880, 1030, 26), 0.0, 0.6, fill=CREAM, w=6)
    k.shape(P(('M', 226, 430), ('L', 854, 430), ('Q', 880, 430, 880, 456), ('L', 880, 540), ('L', 200, 540), ('L', 200, 456), ('Q', 200, 430, 226, 430), ('Z',)), 0.1, 0.6, fill=RED, w=6)
    for x in [330, 750]:
        k.shape(circ(x, 430, 16), 0.3, 0.6, fill=GOLD, w=4)
    draw_text(c, "कार्तिक शुक्ल द्वितीया", 540, 487, F_HB, 46, CREAM, alpha=clamp((tau - 0.5) / 0.2))
    a = clamp((tau - 0.9) / 0.15)
    draw_text(c, "11", 540, 670, F_Y, 250, RED, alpha=a, scale=0.7 + 0.3 * back((tau - 0.9) / 0.35), stroke=6, sfill=INK)
    draw_text(c, "नवंबर 2026 · बुधवार", 540, 805, F_HB, 56, INK, alpha=clamp((tau - 1.8) / 0.2))
    chip(c, "भाई दूज के दिन", 540, 888, 46, SAF, INK, clamp((tau - 3.3) / 0.2), scale=0.8 + 0.2 * back((tau - 3.3) / 0.3))
    draw_text(c, "अपराह्न मुहूर्त 1:10 – 3:20 PM", 540, 978, F_HS, 34, INK, alpha=clamp((tau - 4.0) / 0.25))
    draw_text(c, "समय: नई दिल्ली, द्रिक पंचांग · अपने शहर का देखें", 540, 1062, F_HS, 30, '#6B5236', alpha=clamp((tau - 4.2) / 0.25))
    marigold(k, 205, 435, 34, 0.5, 0.9); marigold(k, 875, 435, 34, 0.55, 0.95)

def s5(c, k, tau, T):
    headline(c, "पूजा में क्या रखें?", tau, 0.0, 330, 76, RED)
    ct = cap_times(5)
    b1 = ct[1][0]; b2 = ct[2][0]; dd = ct[1][1] - ct[1][0]; d2 = ct[2][1] - ct[2][0]
    times = [b1, b1 + dd * 0.5, b2, b2 + d2 * 0.6]
    cells = [(330, 620), (750, 620), (330, 900), (750, 900)]
    labels = ["नई कलम", "दवात", "कोरा कागज़", "बही-खाता"]
    for i, ((x, y), t0) in enumerate(zip(cells, times)):
        t0 -= 0.25
        k.shape(rrect(x - 180, y - 130, x + 180, y + 120, 24), t0 - 0.3, t0 + 0.2, fill='#FFF8E6', w=4, col='#B9A27A')
        if i == 0: quill(k, x - 70, y + 50, x + 80, y - 100, t0, t0 + 0.6)
        if i == 1: inkpot(k, x, y - 10, 1.1, t0, t0 + 0.6)
        if i == 2:
            k.shape(P(('M', x - 70, y - 90), ('L', x + 40, y - 90), ('L', x + 70, y - 60), ('L', x + 70, y + 50), ('L', x - 70, y + 50), ('Z',)), t0, t0 + 0.6, fill='#FFFFFF', w=5)
            k.shape(P(('M', x + 40, y - 90), ('L', x + 40, y - 60), ('L', x + 70, y - 60)), t0 + 0.3, t0 + 0.6, w=4)
        if i == 3: bahi(k, x, y - 20, 200, 130, t0, t0 + 0.6)
        draw_text(c, labels[i], x, y + 88, F_HB, 44, INK, alpha=clamp((tau - t0 - 0.3) / 0.2))
        a = clamp((tau - t0) / 0.2)
        if a > 0:
            k.c.drawCircle(x - 150, y - 100, 24, skia.Paint(AntiAlias=True, Color=C(RED, 255 * a)))
            draw_text(c, str(i + 1), x - 150, y - 98, F_HB, 34, CREAM, alpha=a)

def s6(c, k, tau, T):
    headline(c, "फिर चढ़ाइए", tau, 0.0, 330, 80, RED)
    k.shape(circ(540, 740, 290), 0.0, 0.5, fill=GOLD, w=6)
    k.shape(circ(540, 740, 250), 0.1, 0.55, fill=GOLDL, w=4)
    for i in range(36):
        a = i * math.pi / 18
        k.shape(circ(540 + math.cos(a) * 270, 740 + math.sin(a) * 270, 6), 0.2, 0.5, fill=RED, w=0)
    ct = cap_times(6)
    t_til = ct[0][0]; t2 = ct[1][0]; d2 = ct[1][1] - ct[1][0]
    times = [t_til, t2, t2 + d2 * 0.3, t2 + d2 * 0.6]
    # roli/chandan bowl
    t0 = times[0] - 0.1
    k.shape(P(('M', 330, 620), ('Q', 410, 720, 490, 620), ('Z',)), t0, t0 + 0.5, fill='#7A3B1E', w=5)
    k.shape(oval(410, 620, 80, 20), t0 + 0.1, t0 + 0.5, fill='#D2232A', w=4)
    k.shape(oval(360, 700, 34, 12), t0 + 0.2, t0 + 0.6, fill='#F1D9A0', w=3)
    chip(c, "तिलक", 410, 755, 36, CREAM, INK, clamp((tau - t0 - 0.4) / 0.2), pad=(18, 8))
    # marigolds
    t0 = times[1] - 0.1
    for j, (mx, my, r) in enumerate([(640, 610, 46), (720, 650, 40), (660, 690, 36)]):
        marigold(k, mx, my, r, t0 + j * 0.08, t0 + 0.5 + j * 0.08)
    chip(c, "फूल", 680, 755, 36, CREAM, INK, clamp((tau - t0 - 0.4) / 0.2), pad=(18, 8))
    # akshat heap
    t0 = times[2] - 0.1
    k.shape(P(('M', 320, 880), ('Q', 400, 790, 480, 880), ('Z',)), t0, t0 + 0.4, fill='#FFFBEF', w=4)
    rng = random.Random(3)
    for j in range(24):
        rx, ry = 400 + rng.uniform(-60, 60), 862 + rng.uniform(-30, 12)
        if abs(rx - 400) < (880 - ry) * 0.9:
            k.shape(oval(rx, ry, 6, 3), t0 + 0.2, t0 + 0.4, fill='#E9DFC4', w=1.5)
    chip(c, "अक्षत", 400, 925, 36, CREAM, INK, clamp((tau - t0 - 0.3) / 0.2), pad=(18, 8))
    t0 = times[3] - 0.1
    diya(k, 650, 880, 0.95, t0, t0 + 0.4, T)
    chip(c, "दीया", 680, 945, 36, CREAM, INK, clamp((tau - t0 - 0.3) / 0.2), pad=(18, 8))

def s7(c, k, tau, T):
    headline(c, "नई कलम से पहली लाइन", tau, 0.0, 330, 70, RED)
    c.save(); c.rotate(-2, 540, 740)
    k.shape(P(('M', 170, 470), ('L', 910, 470), ('L', 910, 990), ('L', 170, 990), ('Z',)), 0.0, 0.5, fill='#FFFDF6', w=5)
    for i in range(6):
        k.shape(P(('M', 210, 560 + i * 75), ('L', 870, 560 + i * 75)), 0.2, 0.6, w=2, col='#E3C9C0')
    ct = cap_times(7); r0 = ct[1][0] - 0.2; r1 = ct[1][1] + 0.2
    rv = clamp((tau - r0) / (r1 - r0))
    w, h = draw_text(c, "ॐ चित्रगुप्ताय नमः", 540, 640, F_Y, 92, RED, reveal=rv)
    c.restore()
    if 0 < rv < 1:
        tx = 540 - w / 2 + w * rv
        k2 = Ink(c, 10); quill(k2, tx, 665, tx + 130, 455, 0, 1)
    elif rv <= 0:
        k2 = Ink(c, 10); quill(k2, 300, 665, 430, 455, 0, 1)
    a = clamp((tau - r1) / 0.25)
    draw_text(c, "कई परिवार साल भर का", 540, 800, F_HB, 46, INK, alpha=a)
    draw_text(c, "आय-व्यय भी लिखते हैं", 540, 865, F_HB, 46, INK, alpha=a)

def s8(c, k, tau, T):
    place(c, 540 - 300 * 0.58, 285, 0.58)
    kk = Ink(c, 99); chitragupta(kk, 0, 0.01, T, show_pen_write=True)
    c.restore()
    ct = cap_times(8)
    a1 = clamp((tau - 0.1) / 0.2)
    bl = 0.82 + 0.18 * (0.5 + 0.5 * math.sin(T * 8))
    chip(c, "अपने कायस्थ दोस्त को भेजो", 520, 800, 54, SAF, INK, a1 * (bl if tau > 0.6 else 1), scale=(0.92 + 0.08 * back((tau - 0.1) / 0.3)) * (1 + 0.03 * math.sin(T * 8)))
    # paper plane icon flying
    if tau > 0.3:
        ph = ((tau - 0.3) * 0.7) % 1
        px, py = 160 + 720 * ph, 720 - 60 * math.sin(ph * math.pi)
        pl = poly([(px, py), (px - 46, py - 14), (px - 30, py + 4)])
        c.drawPath(pl, skia.Paint(AntiAlias=True, Color=C('#FFFFFF', 230)))
        c.drawPath(pl, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C(INK)))
    t2 = ct[1][0] - 0.1
    chip(c, "सेव करो — पूजा के दिन काम आएगा", 520, 945, 44, '#FFF6DA', RED, clamp((tau - t2) / 0.2) * bl, scale=0.9 + 0.1 * back((tau - t2) / 0.3), outline=RED)

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8]

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
