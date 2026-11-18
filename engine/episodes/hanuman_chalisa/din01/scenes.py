import sys, json, os, math
from art import *
from lines import LINES

KEYS = [l[0] for l in LINES]
durs = json.load(open('durs.json'))
PAD0, PADE = 0.10, 0.30
D = []
for i, k_ in enumerate(KEYS):
    d = durs[k_] + PAD0 + PADE
    if LINES[i][2] == 'chant': d += 0.5
    D.append(d)
D[0] = durs[KEYS[0]] + PAD0 + 0.6
D[-1] += 1.2
START = [sum(D[:i]) for i in range(len(D))]
TOT = sum(D)
NUDGE = (-9, -8)  # save ask is spoken in the 'save' scene  # mid-reel save chip (~40%)

# on-screen caption chunks (spoken text split for display)
CAPS = {
 'hook': ["क्या आप जानते हैं,", "हनुमान चालीसा के पहले दोहे का", "असली मतलब क्या है?"],
 'save': ["इस वीडियो को सेव कर लीजिए", "और मैं आपको आराम से बताता हूँ"],
 'm1': ["देखिए, तुलसीदास जी कहते हैं", "गुरु के चरण कमल जैसे हैं", "और उनकी धूल से", "मैं अपने मन का शीशा साफ़ करता हूँ"],
 'm2': ["क्योंकि जब मन का शीशा साफ़ होगा", "तभी उसमें राम का निर्मल यश दिखेगा", "वो यश, जो चारों फल देता है", "अब दूसरा दोहा सुनिए"],
 'm4': ["इतने बड़े कवि,", "ख़ुद को बुद्धिहीन कहते हैं", "और हनुमान जी से माँगते हैं", "बल, बुद्धि और विद्या"],
 'm6': ["और ध्यान दीजिए,", "उन्होंने धन नहीं माँगा", "माँगी समझ, और मन की शांति"],
 'cta': ["अगर आप भी रोज़ चालीसा पढ़ते हैं", "तो फॉलो कीजिए", "कल मैं आपको", "पहली 2 चौपाई का मतलब बताऊँगा"],
}
DOHA = {
 'd1': ["श्रीगुरु चरन सरोज रज,", "निज मनु मुकुरु सुधारि।", "बरनउँ रघुबर बिमल जसु,", "जो दायकु फल चारि॥"],
 'd2': ["बुद्धिहीन तनु जानिके,", "सुमिरौं पवन-कुमार।", "बल बुधि बिद्या देहु मोहिं,", "हरहु कलेस बिकार॥"],
}

import numpy as _np, soundfile as _sf
_GAPS = {}
def gaps(key):
    if key not in _GAPS:
        a, sr = _sf.read(f'vo/{key}.wav', dtype='float32'); hop = int(sr * 0.02)
        e = _np.array([_np.abs(a[i:i + hop]).max() for i in range(0, len(a) - hop, hop)]) < 0.015
        g = []; i = 0
        while i < len(e):
            if e[i]:
                j = i
                while j < len(e) and e[j]: j += 1
                if (j - i) * 0.02 >= 0.18: g.append((i + j) / 2 * 0.02)
                i = j
            else: i += 1
        _GAPS[key] = g
    return _GAPS[key]
_CH = {}
def chunks(key, parts):
    k_ = (key, tuple(parts))
    if k_ in _CH: return _CH[k_]
    d = durs[key]; tot = sum(len(x) for x in parts); b = [0.0]; t = 0
    for x in parts[:-1]:
        t += d * len(x) / tot
        g = [q for q in gaps(key) if abs(q - t) < 0.9 and q > b[-1] + 0.3]
        b.append(min(g, key=lambda q: abs(q - t)) if g else t)
    b.append(d)
    _CH[k_] = [(PAD0 + b[i], PAD0 + b[i + 1], parts[i]) for i in range(len(parts))]
    return _CH[k_]

def wrap(txt, size=54, maxw=720):
    words = txt.split(' '); lines = ['']
    for w in words:
        cand = (lines[-1] + ' ' + w).strip()
        if text_w(cand, F_HB, size) > maxw and lines[-1]: lines.append(w)
        else: lines[-1] = cand
    return lines[:2]

BOXES = []  # (x0,y0,x1,y1,label) recorded for safe-zone checks
def rec(x0, y0, x1, y1, lab): BOXES.append((x0, y0, x1, y1, lab))

def draw_caption(c, key, tau):
    if key not in CAPS: return
    ch = chunks(key, CAPS[key])
    for j, (a, b, x) in enumerate(ch):
        if a - 0.05 <= tau < b + (0.35 if j == len(ch) - 1 else 0):
            pop = back((tau - a) / 0.18) if tau >= a else 0
            lines = wrap(x); ws = [text_w(l, F_HB, 54) for l in lines]
            bw = max(ws) + 60; lh = 70; bh = lh * len(lines) + 24; cx, cy = 510, 1150
            c.save(); c.translate(cx, cy); c.scale(0.9 + 0.1 * pop, 0.9 + 0.1 * pop)
            r = skia.Rect(-bw / 2, -bh / 2, bw / 2, bh / 2)
            c.drawRRect(skia.RRect.MakeRectXY(r, 26, 26), skia.Paint(AntiAlias=True, Color=C(INK, 232)))
            for i, l in enumerate(lines): draw_text(c, l, 0, -bh / 2 + 12 + lh * i + lh / 2, F_HB, 54, CREAM)
            c.restore(); rec(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2, 'caption')

def headline(c, txt, tau, t0=0.0, y=345, size=72, col=RED, out=None):
    a = clamp((tau - t0) / 0.15)
    if out is not None: a *= 1 - clamp((tau - out) / 0.2)
    if a > 0:
        w, h = draw_text(c, txt, 540, y, F_Y, size, col, alpha=a, scale=0.85 + 0.15 * back((tau - t0) / 0.3), stroke=5, sfill=CREAM)
        rec(540 - w / 2, y - h / 2, 540 + w / 2, y + h / 2, 'headline:' + txt)

def tag(c, txt, cx, cy, tau, t0, size=48, bg=CREAM, fg=INK, out=None):
    a = clamp((tau - t0) / 0.15)
    if out is not None: a *= 1 - clamp((tau - out) / 0.2)
    if a <= 0: return
    r = chip(c, txt, cx, cy, size, bg, fg, a, scale=0.8 + 0.2 * back((tau - t0) / 0.3))
    rec(cx + r.left(), cy + r.top(), cx + r.right(), cy + r.bottom(), 'chip:' + txt)

def doha_card(c, k, key, tau, num):
    d = durs[key]; lines = DOHA[key]
    k.shape(rrect(110, 470, 970, 900, 30), 0.0, 0.45, fill=CREAM, w=6)
    k.shape(rrect(130, 490, 950, 880, 22), 0.1, 0.5, w=4, col=RED)
    draw_text(c, f"हनुमान चालीसा · दोहा {num}", 540, 540, F_HB, 40, RED, alpha=clamp((tau - 0.3) / 0.3))
    ch = [(a + 0.25, b + 0.25, x) for a, b, x in chunks(key, lines)]
    for j, (a, b, x) in enumerate(ch):
        y = 610 + j * 78
        if tau >= a - 0.1: col = RED if tau < b else INK
        else: col = FADED
        draw_text(c, x, 540, y, F_Y, 60, col, alpha=clamp((tau - 0.2 - j * 0.08) / 0.3), scale=1 + 0.04 * (a <= tau < b))
    rec(110, 470, 970, 900, 'doha card')

def scene(c, i, tau, T):
    key = KEYS[i]; k = Ink(c, tau)
    if key == 'hook':
        headline(c, "पहले दोहे का", tau, 0.0, 345, 84, RED)
        headline(c, "असली मतलब?", tau, 0.2, 455, 80, INK)
        mirror(k, 540, 720, 1.0, 0.0, 0.9, dust=1.0, tt=T)
    elif key == 'save':
        hanuman_at(c, tau, T, 0.0, 2.4, y=470, s=0.78)
        bl = 1 + 0.06 * math.sin(T * 9)
        a = clamp(tau / 0.2)
        r = chip(c, "सेव कर लीजिए", 540, 360, 64, SAF, INK, a, scale=(0.8 + 0.2 * back(tau / 0.3)) * bl)
        rec(540 + r.left() * 1.1, 360 + r.top() * 1.1, 540 + r.right() * 1.1, 360 + r.bottom() * 1.1, 'save chip')
    elif key == 'intro':
        tag(c, "रोज़ 2 पंक्तियाँ · अर्थ सहित", 540, 360, tau, 0.1)
    elif key in DOHA:
        doha_card(c, k, key, tau, 1 if key == 'd1' else 2)
        if key == 'd1': tag(c, "दिन 1 / 22 · रोज़ 2 पंक्तियाँ", 560, 390, tau, 0.1, size=44, bg=GOLDL)
        diya(k, 520, 1040, 0.9, 0.2, 0.7, T)
    elif key == 'm1':
        ch = chunks(key, CAPS[key]); t_dust = ch[2][0]; t_wipe = ch[3][0] + 0.3
        tag(c, "गुरु के चरण = कमल", 540, 345, tau, ch[1][0])
        tag(c, "रज = चरणों की धूल", 540, 450, tau, t_dust, size=44, bg=GOLDL)
        lotus(k, 300, 720, 1.0, 0.0, 0.8)
        clean = clamp((tau - t_wipe) / 1.0)
        mirror(k, 760, 700, 0.85, 0.3, 1.0, dust=1 - clean, tt=T, glint=clean)
        # golden pollen drifting from lotus to mirror
        if tau > t_dust:
            p = skia.Paint(AntiAlias=True)
            for n in range(14):
                f = ((tau - t_dust) * 0.6 + n / 14) % 1.0
                x = 330 + (760 - 330) * f; y = 650 - 120 * math.sin(math.pi * f) + 20 * math.sin(n * 2.1)
                p.setColor(C(GOLD, 230 * (1 - clean * 0.7))); c.drawCircle(x, y, 7 + 3 * math.sin(n), p)
        if t_wipe <= tau < t_wipe + 1.0:  # cloth wiping
            f = (tau - t_wipe); cx = 680 + 160 * f; cy = 640 + 40 * math.sin(f * 12)
            k2 = Ink(c, 9); k2.shape(rrect(cx - 46, cy - 30, cx + 46, cy + 30, 12), 0, 1, fill='#F2E2BE', w=4)
        tag(c, "मुकुर = शीशा", 300, 930, tau, ch[3][0], size=42, bg=CREAM)
    elif key == 'm2':
        ch = chunks(key, CAPS[key]); tt2 = ch[2][0]
        if tau < tt2 + 0.2:
            c.saveLayerAlpha(None, int(255 * (1 - clamp((tau - tt2) / 0.2))))
            headline(c, "रघुबर का बिमल जसु", tau, ch[1][0] - 0.1, 345, 70, RED)
            mirror(k, 540, 680, 1.0, 0.0, 0.5, dust=0, tt=T, glint=0.6 + 0.4 * math.sin(T * 3))
            bow(k, 520, 680, 1.0, ch[1][0], ch[1][0] + 1.0)
            c.restore()
        else:
            tau2 = tau - tt2
            headline(c, "चारों फल", tau2, 0.0, 345, 84, RED)
            names = ["धर्म", "अर्थ", "काम", "मोक्ष"]
            for j in range(4):
                cx = 340 + (j % 2) * 400; cy = 560 + (j // 2) * 320; t0 = 0.1 + j * 0.3
                Ink(c, tau2).shape(rrect(cx - 170, cy - 130, cx + 170, cy + 130, 26), t0, t0 + 0.4, fill=CREAM, w=6)
                a = clamp((tau2 - t0 - 0.2) / 0.3)
                if a > 0:
                    ic = Ink(c, 9)
                    if j == 0:
                        ic.shape(circ(cx, cy - 35, 50), 0, 1, w=7, col=SAF)
                        for q in range(8):
                            ang = q * math.pi / 4; ic.shape(P(('M', cx, cy - 35), ('L', cx + 50 * math.cos(ang), cy - 35 + 50 * math.sin(ang))), 0, 1, w=4, col=SAF)
                    elif j == 1: coin(ic, cx, cy - 35, 50, 0, 1); draw_text(c, "₹", cx, cy - 37, F_HB, 56, BROWN, alpha=a)
                    elif j == 2:
                        ic.shape(P(('M', cx, cy + 5), ('C', cx - 80, cy - 45, cx - 40, cy - 105, cx, cy - 65), ('C', cx + 40, cy - 105, cx + 80, cy - 45, cx, cy + 5), ('Z',)), 0, 1, fill=PINK, w=5)
                    else: draw_text(c, "ॐ", cx, cy - 40, F_HB, 96, IND, alpha=a)
                    draw_text(c, names[j], cx, cy + 70, F_Y, 58, INK, alpha=a)
                rec(cx - 170, cy - 130, cx + 170, cy + 130, 'tile')
    elif key == 'm4':
        ch = chunks(key, CAPS[key]); last = ch[3]
        hanuman_at(c, tau, T, -3, 0.1, y=470, s=0.78)
        tag(c, "\"मैं बुद्धिहीन हूँ\" — तुलसीदास", 540, 345, tau, 0.2, size=44, out=last[0] - 0.2)
        L = last[1] - last[0]
        for j, (w_, f) in enumerate([("बल", 0.05), ("बुद्धि", 0.35), ("विद्या", 0.75)]):
            tag(c, w_, 300 + j * 240, 345, tau, last[0] + L * f, size=56, bg=GOLDL)
    elif key == 'm5':
        ch = chunks(key, CAPS[key])
        tag(c, "क्लेश = दुख", 540, 345, tau, 0.1, size=50)
        tag(c, "विकार = मन के बुरे भाव", 540, 450, tau, ch[1][0], size=46, bg=GOLDL)
        blow = clamp((tau - ch[2][0] - 0.4) / 1.4)
        c.save(); c.translate(700 * ease(blow), -60 * blow)
        cloud(k, 420, 680, 1.1, 0.0, 0.5); cloud(k, 650, 820, 0.9, ch[1][0], ch[1][0] + 0.5, col='#3F3A4A')
        c.restore()
        if blow > 0:
            wind(Ink(c, tau), 300, 760, 1.2, ch[2][0], ch[2][0] + 0.8)
            draw_text(c, "पवन-कुमार", 300, 930, F_Y, 52, IND, alpha=clamp((tau - ch[2][0]) / 0.3))
            rec(170, 900, 430, 960, 'pavan')
    elif key == 'm6':
        ch = chunks(key, CAPS[key])
        headline(c, "धन नहीं माँगा", tau, ch[1][0] - 0.1, 345, 80, RED)
        for j, (dx, dy) in enumerate([(-60, 40), (60, 40), (0, -40)]):
            coin(k, 540 + dx, 640 + dy, 70, 0.0 + j * 0.1, 0.5 + j * 0.1)
            draw_text(c, "₹", 540 + dx, 638 + dy, F_HB, 70, BROWN, alpha=clamp((tau - 0.4 - j * 0.1) / 0.3))
        Ink(c, tau).shape(P(('M', 400, 520), ('L', 680, 800)), ch[1][0] + 0.3, ch[1][0] + 0.7, w=18, col=RED)
        Ink(c, tau).shape(P(('M', 680, 520), ('L', 400, 800)), ch[1][0] + 0.5, ch[1][0] + 0.9, w=18, col=RED)
        L = ch[2][1] - ch[2][0]
        for j, (w_, f) in enumerate([("समझ", 0.2), ("मन की शांति", 0.6)]):
            tag(c, w_, 360 + j * 330, 960, tau, ch[2][0] + L * f, size=56, bg=GOLDL)
    elif key == 'cta':
        ch = chunks(key, CAPS[key])
        hanuman_at(c, tau, T, -3, 0.1, y=470, s=0.78)
        tag(c, "फॉलो करो · रोज़ 2 पंक्तियाँ", 540, 345, tau, ch[1][0] - 0.1, size=54, bg=RED, fg=CREAM, out=ch[2][0])
        tag(c, "कल: चौपाई 1 और 2", 540, 345, tau, ch[2][0], size=56, bg=GOLDL)

def hanuman_at(c, tau, T, t0, dur, y=420, s=0.9):
    c.save(); c.translate(540 - 300 * s, y); c.scale(s, s)
    hanuman(Ink(c, tau), t0, dur, T); c.restore()
    rec(540 - 300 * s, y, 540 + 300 * s, y + 740 * s, 'hanuman')

def overlay(c, T, i, tau):
    # day badge after intro
    if i >= 1:
        a = clamp((T - START[1] - 0.1) / 0.3)
        if True:
            badge(c, "दिन 1", None, 126, 324, 50, alpha=1)
            rec(76, 274, 176, 374, 'badge')
    # mid-reel save nudge
    if NUDGE[0] <= T < NUDGE[1]:
        f = (T - NUDGE[0]) / (NUDGE[1] - NUDGE[0])
        a = clamp(f / 0.1) * (1 - clamp((f - 0.88) / 0.12)); bl = 1 + 0.07 * math.sin(T * 12)
        r = chip(c, "सेव करो · रोज़ काम आएगा", 510, 1150, 46, SAF, INK, a, scale=bl)
        rec(510 + r.left() * bl, 1150 + r.top() * bl, 510 + r.right() * bl, 1150 + r.bottom() * bl, 'nudge')

BG = None; BORD = None
def frame(T):
    global BG, BORD
    if BG is None: BG = skia.Image.fromarray(make_bg()); BORD = border_layer()
    s = skia.Surface(W, H); c = s.getCanvas(); c.drawImage(BG, 0, 0); c.drawImage(BORD, 0, 0)
    i = max(j for j in range(len(START)) if START[j] <= T); tau = T - START[i]
    # scene cross-fade in
    c.saveLayerAlpha(None, int(255 * clamp(tau / 0.18)) if i > 0 else 255)
    scene(c, i, tau, T); c.restore()
    nudge_on = NUDGE[0] <= T < NUDGE[1]
    if not nudge_on: draw_caption(c, KEYS[i], tau)
    overlay(c, T, i, tau)
    return s.makeImageSnapshot().toarray()[:, :, [2, 1, 0]]
