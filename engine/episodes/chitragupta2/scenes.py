import sys, json, subprocess, os, math
from eng import *

durs = json.load(open('durs.json'))
PAD0, PADE = 0.10, 0.25
D = [d + PAD0 + PADE for d in durs]
D[0] = durs[0] + PAD0 + 0.15
D[-1] += 0.8
START = [sum(D[:i]) for i in range(len(D))]

CAPS = [
    ["पार्ट 2:", "चित्रगुप्त जी ने", "कलम क्यों रख दी थी?"],
    ["रावण पर जीत के बाद,", "अयोध्या में श्री राम के", "राजतिलक की तैयारी थी"],
    ["गुरु वशिष्ठ के शिष्यों ने", "सभी देवताओं को न्योता भेजा", "पर चित्रगुप्त जी का नाम", "छूट गया"],
    ["इस भूल से आहत होकर,", "चित्रगुप्त जी ने", "अपनी कलम रख दी"],
    ["और यमलोक में", "कर्मों का हिसाब रुक गया!", "कौन स्वर्ग जाए, कौन नर्क —", "कोई तय नहीं कर पा रहा था"],
    ["तब श्री राम,", "गुरु वशिष्ठ के साथ", "चित्रगुप्त जी के पास गए", "और भूल की क्षमा माँगी"],
    ["प्रभु के कहने पर,", "चित्रगुप्त जी ने कलम की पूजा की", "और फिर से लिखना शुरू किया"],
    ["मान्यता है, तभी से", "कायस्थ परिवार दिवाली पूजा के बाद", "कलम रख देते हैं", "और यम द्वितीया पर", "कलम-दवात पूजा के बाद ही", "फिर उठाते हैं"],
    ["कल ये पूजा है", "ये कहानी उस दोस्त को भेजिए", "जो कल कलम उठाएगा", "और ऐसी कहानियों के लिए", "फॉलो कीजिए"],
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
            c.save(); c.translate(520, 1150); c.scale(0.9 + 0.1 * pop, 0.9 + 0.1 * pop)
            r = skia.Rect(-bw / 2, -bh / 2, bw / 2, bh / 2)
            c.drawRRect(skia.RRect.MakeRectXY(r, 26, 26), skia.Paint(AntiAlias=True, Color=C(INK, 230)))
            for j, l in enumerate(lines):
                draw_text(c, l, 0, -bh / 2 + 12 + lh * j + lh / 2, F_HB, 54, CREAM)
            c.restore()

def headline(c, txt, tau, t0=0.0, y=330, size=70, col=RED):
    a = clamp((tau - t0) / 0.15)
    if a > 0: draw_text(c, txt, 540, y, F_Y, size, col, alpha=a, scale=0.85 + 0.15 * back((tau - t0) / 0.3), stroke=5, sfill=CREAM)

def figure(c, x, y, s, t0, dur, tau, T, **kw):
    place(c, x - 300 * s, y, s); kk = Ink(c, tau); chitragupta(kk, t0, dur, T, **kw); c.restore()

def palace(k, t0, t1):
    # simple folk palace: base, three domes, pillars, flags
    k.shape(rrect(200, 760, 880, 1000, 6), t0, t1, fill=CREAM, w=6)
    k.shape(rrect(180, 990, 900, 1030, 6), t0, t1, fill=RED, w=5)
    for x in [260, 400, 680, 820]:
        k.shape(rrect(x - 16, 790, x + 16, 990, 6), t0 + 0.1, t1, fill=GOLD, w=4)
    k.shape(P(('M', 470, 990), ('L', 470, 880), ('Q', 540, 800, 610, 880), ('L', 610, 990), ('Z',)), t0 + 0.15, t1, fill=IND, w=5)
    for (x, r, yy) in [(330, 80, 760), (540, 120, 760), (750, 80, 760)]:
        k.shape(P(('M', x - r, yy), ('Q', x - r, yy - r * 1.3, x, yy - r * 1.6), ('Q', x + r, yy - r * 1.3, x + r, yy), ('Z',)), t0 + 0.2, t1, fill=SAF, w=5)
        k.shape(P(('M', x, yy - r * 1.6), ('L', x, yy - r * 1.6 - 50)), t0 + 0.3, t1, w=4)
        k.shape(poly([(x, yy - r * 1.6 - 50), (x + 46, yy - r * 1.6 - 38), (x, yy - r * 1.6 - 26)]), t0 + 0.35, t1, fill=RED, w=3)
    # marigold toran
    for i in range(9):
        x = 230 + i * 77.5; y = 780 + 22 * math.sin(i / 8 * math.pi)
        marigold(k, x, y, 18, t0 + 0.4 + i * 0.03, t1 + 0.2)

def scroll(k, x, y, w, h, t0, t1, fill=CREAM):
    k.shape(rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 4), t0, t1, fill=fill, w=4)
    k.shape(rrect(x - w / 2 - 12, y - h / 2 - 8, x - w / 2 + 8, y + h / 2 + 8, 8), t0, t1, fill='#E8D7AE', w=3)
    k.shape(rrect(x + w / 2 - 8, y - h / 2 - 8, x + w / 2 + 12, y + h / 2 + 8, 8), t0, t1, fill='#E8D7AE', w=3)

def tick(c, x, y, a, col=GRN):
    if a <= 0: return
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, Color=C(col), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    pth = P(('M', x - 18, y), ('L', x - 4, y + 16), ('L', x + 22, y - 18))
    c.drawPath(Ink(c, 0).partial(pth, ease(a)), p)

def cross(c, x, y, a, col=RED):
    if a <= 0: return
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, Color=C(col), StrokeCap=skia.Paint.kRound_Cap)
    k = Ink(c, 0)
    c.drawPath(k.partial(P(('M', x - 18, y - 18), ('L', x + 18, y + 18)), ease(a * 2)), p)
    if a > 0.5: c.drawPath(k.partial(P(('M', x + 18, y - 18), ('L', x - 18, y + 18)), ease(a * 2 - 1)), p)

def send_chip(c, tau, t0, T, txt="दोस्त को भेजो"):
    a = clamp((tau - t0) / 0.2) * (1 - clamp((tau - t0 - 1.6) / 0.25))
    if a > 0:
        bl = 0.85 + 0.15 * (0.5 + 0.5 * math.sin(T * 9))
        chip(c, txt, 540, 1035, 46, SAF, INK, a * bl, scale=0.9 + 0.1 * back((tau - t0) / 0.3))

# ---------------- scenes ----------------
def s0(c, k, tau, T):
    chip(c, "पार्ट 2", 540, 320, 52, RED, CREAM, clamp(tau / 0.12), scale=0.8 + 0.2 * back(tau / 0.3), outline=INK)
    headline(c, "चित्रगुप्त जी ने", tau, 0.05, 440, 80, INK)
    headline(c, "कलम क्यों रख दी?", tau, 0.15, 545, 86, RED)
    # quill lying down + inkpot + question marks
    quill(k, 330, 900, 760, 830, 0.1, 0.9)
    inkpot(k, 810, 900, 1.0, 0.2, 0.9)
    k.shape(P(('M', 220, 935), ('L', 880, 935)), 0.05, 0.6, w=5, col='#8A6A44')
    for i, (qx, qy) in enumerate([(300, 720), (560, 690), (760, 740)]):
        a = clamp((tau - 0.6 - i * 0.12) / 0.2)
        if a > 0: draw_text(c, "?", qx, qy + 10 * math.sin(T * 4 + i), F_Y, 96 - i * 10, SAF, alpha=a, stroke=4, sfill=INK)

def s1(c, k, tau, T):
    headline(c, "अयोध्या — राजतिलक", tau, 0.0, 330, 76, RED)
    palace(k, 0.0, 1.4)
    ra = clamp((tau - 1.2) / 0.8)
    if ra > 0:
        g = skia.Paint(AntiAlias=True, Color=C('#FFE7A8', 120 * ra)); g.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 50))
        c.drawCircle(540, 560, 130, g)
    for i, x in enumerate([250, 420, 660, 830]):
        diya(k, x, 1060 - 0 * i, 0.55, 1.0 + i * 0.12, 1.5 + i * 0.12, T + i)

def s2(c, k, tau, T):
    headline(c, "देवताओं को न्योता", tau, 0.0, 330, 76, RED)
    names = ["इंद्र देव", "अग्नि देव", "वरुण देव", "यमराज", "चित्रगुप्त जी"]
    ct = cap_times(2)
    tmiss = ct[2][0]
    for j, nm in enumerate(names):
        y = 470 + j * 120; t0 = 0.3 + j * 0.35
        scroll(k, 470, y, 460, 84, t0, t0 + 0.4, fill=CREAM if j < 4 else '#F6DCCB')
        draw_text(c, nm, 470, y, F_HB, 52, INK if j < 4 else RED, alpha=clamp((k.t - t0 - 0.3) / 0.2))
        if j < 4: tick(c, 770, y, clamp((k.t - t0 - 0.5) / 0.3))
        else: cross(c, 770, y, clamp((k.t - tmiss) / 0.5))
    a = clamp((tau - ct[3][0]) / 0.2)
    if a > 0: chip(c, "नाम छूट गया!", 540, 1040 - 20, 50, RED, CREAM, a, scale=0.8 + 0.2 * back((tau - ct[3][0]) / 0.3))

def s3(c, k, tau, T):
    headline(c, "कलम रख दी", tau, 0.0, 330, 84, RED)
    figure(c, 540, 400, 0.8, -10, 0.01, tau, T, show_pen_write=False, pen=False)
    # quill drops from top and lands flat beside him
    d = ease((tau - 0.6) / 0.8)
    y = 520 + 470 * d; ang = -60 + 60 * d
    c.save(); c.translate(300, y); c.rotate(ang)
    kk = Ink(c, 9); quill(kk, -150, 0, 150, 0, 0, 0.01)
    c.restore()
    if d >= 1:
        a = clamp((tau - 1.4) / 0.3)
        for i in range(5):
            ang2 = i * 0.6 + 0.3
            pt = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(INK, 255 * a), StrokeCap=skia.Paint.kRound_Cap)
            c.drawLine(300 + math.cos(ang2 + 3.4) * 170, 990 + math.sin(ang2 + 3.4) * 40, 300 + math.cos(ang2 + 3.4) * 200, 990 + math.sin(ang2 + 3.4) * 60, pt)

def s4(c, k, tau, T):
    headline(c, "हिसाब रुक गया!", tau, 0.0, 330, 84, RED)
    # open ledger with writing that stops
    k.shape(rrect(170, 420, 910, 720, 12), 0.0, 0.5, fill=CREAM, w=6)
    k.shape(P(('M', 540, 420), ('L', 540, 720)), 0.1, 0.5, w=5, col=RED)
    for i in range(5):
        y = 465 + i * 50
        L = 1.0 if i < 3 else (0.45 if i == 3 else 0.0)
        for (x0, x1) in [(200, 510), (570, 880)]:
            pth = skia.Path(); pth.moveTo(x0, y)
            for j in range(1, 40): pth.lineTo(x0 + (x1 - x0) * j / 39, y + 4 * math.sin(j * 1.5 + i))
            p = clamp((tau - 0.3 - i * 0.12) / 0.4) * (L if x0 == 570 else (1.0 if i < 4 else 0.0))
            if p > 0: c.drawPath(k.partial(pth, p), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C(INK), StrokeCap=skia.Paint.kRound_Cap))
    a = clamp((tau - 1.0) / 0.2)
    if a > 0: chip(c, "रुका!", 760, 660, 46, RED, CREAM, a, scale=0.8 + 0.2 * back((tau - 1.0) / 0.3))
    # two doors
    ct = cap_times(4); td = ct[2][0] - 0.1
    for j, (x, lab, col) in enumerate([(340, "स्वर्ग", GOLD), (740, "नर्क", '#6E3B2E')]):
        t0 = td + j * 0.2
        k.shape(P(('M', x - 110, 960), ('L', x - 110, 840), ('Q', x, 750, x + 110, 840), ('L', x + 110, 960), ('Z',)), t0, t0 + 0.5, fill=col, w=5)
        draw_text(c, lab, x, 905, F_Y, 52, CREAM, alpha=clamp((tau - t0 - 0.4) / 0.2), stroke=4, sfill=INK)
    qa = clamp((tau - td - 0.8) / 0.2)
    if qa > 0: draw_text(c, "?", 540, 860 + 8 * math.sin(T * 5), F_Y, 120, SAF, alpha=qa, stroke=5, sfill=INK)
    send_chip(c, tau, ct[3][0], T)  # ~40% soft nudge

def s5(c, k, tau, T):
    headline(c, "भूल की क्षमा", tau, 0.0, 330, 84, RED)
    # puja thali with diya, marigolds and folded-hands symbol (namaste in Devanagari 'प्रणाम')
    k.shape(oval(540, 840, 320, 90), 0.0, 0.6, fill=GOLD, w=6)
    k.shape(oval(540, 830, 270, 66), 0.1, 0.6, fill=GOLDL, w=4)
    diya(k, 520, 815, 0.95, 0.3, 0.9, T)
    for i, x in enumerate([330, 420, 660, 750]):
        marigold(k, x, 838 + (8 if i % 2 else -6), 30, 0.5 + i * 0.08, 1.0 + i * 0.08)
    k.shape(circ(540, 560, 150), 0.2, 0.9, fill=CREAM, w=5)
    draw_text(c, "प्रणाम", 540, 560, F_Y, 90, RED, alpha=clamp((tau - 0.8) / 0.3), stroke=4, sfill=CREAM)
    for i in range(16):
        a = i * math.pi / 8
        k.shape(circ(540 + math.cos(a) * 172, 560 + math.sin(a) * 172, 10), 0.4 + i * 0.02, 1.0, fill=SAF, w=2.5)

def s6(c, k, tau, T):
    ra = clamp(tau / 1.0)
    rays(c, 540, 640, T, ra, r0=120, r1=480)
    headline(c, "कलम फिर चली", tau, 0.0, 330, 84, RED)
    figure(c, 540, 410, 0.85, -10, 0.01, tau, T, show_pen_write=True)
    a = clamp((tau - 0.6) / 0.3)

def s7(c, k, tau, T):
    headline(c, "तभी से ये परंपरा", tau, 0.0, 330, 78, RED)
    ct = cap_times(7)
    for j, (top, sub, t0, col) in enumerate([("दिवाली पूजा", "कलम रखी", 0.2, IND), ("यम द्वितीया", "कलम उठी", ct[3][0], GRN)]):
        y = 520 + j * 290
        k.shape(rrect(150, y - 110, 930, y + 110, 24), t0, t0 + 0.5, fill=CREAM, w=6)
        k.shape(rrect(150, y - 110, 420, y + 110, 24), t0 + 0.1, t0 + 0.5, fill=col, w=6)
        draw_text(c, top, 285, y, F_Y, 46, CREAM, alpha=clamp((tau - t0 - 0.3) / 0.2), stroke=3, sfill=INK)
        draw_text(c, sub, 600, y, F_HB, 56, INK, alpha=clamp((tau - t0 - 0.5) / 0.2))
        kk = Ink(c, tau)
        if j == 0: quill(kk, 760, y + 40, 890, y + 30, t0 + 0.5, t0 + 1.0)
        else: quill(kk, 790, y + 60, 880, y - 70, t0 + 0.5, t0 + 1.0)
    a = clamp((tau - ct[4][0]) / 0.2)
    if a > 0: chip(c, "11 नवंबर · बुधवार", 540, 1000, 46, SAF, INK, a, scale=0.85 + 0.15 * back((tau - ct[4][0]) / 0.3))

def s8(c, k, tau, T):
    figure(c, 540, 285, 0.5, -10, 0.01, tau, T, show_pen_write=True)
    ct = cap_times(8)
    bl = 0.82 + 0.18 * (0.5 + 0.5 * math.sin(T * 8))
    a1 = clamp((tau - ct[1][0]) / 0.2)
    chip(c, "कल कलम उठाने वाले दोस्त को भेजो", 520, 825, 46, SAF, INK, a1 * bl, scale=(0.92 + 0.08 * back((tau - ct[1][0]) / 0.3)))
    a0 = clamp(tau / 0.2)
    chip(c, "कल है चित्रगुप्त पूजा", 540, 725, 40, CREAM, RED, a0, outline=RED)
    t2 = ct[3][0] - 0.1
    chip(c, "फॉलो करो — और कहानियाँ", 520, 965, 54, RED, CREAM, clamp((tau - t2) / 0.2) * bl, scale=(0.9 + 0.1 * back((tau - t2) / 0.3)) * (1 + 0.03 * math.sin(T * 8)))

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
