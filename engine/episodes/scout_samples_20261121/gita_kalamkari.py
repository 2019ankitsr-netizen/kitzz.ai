"""Scout sample 1 (21 Nov 2026): Gita Jayanti in Kalamkari Ink — payoff first, rewind, self-drawing chariot scene, count-up.
Reuses engine/episodes/chitragupta/eng.py (skia PathMeasure ink + Pillow/raqm Devanagari)."""
import os, sys, math, subprocess, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); ENG = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ENG, 'episodes', 'chitragupta')); sys.path.insert(0, ENG)
from eng import *
import audio as A

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'; os.makedirs(OUT, exist_ok=True)
SAFE = (65, 269, 1015, 1248); RAIL = (930, 900, 1080, 1700)

# ---------------- voice ----------------
VO = [("गीता जयंती, बीस दिसंबर।", ["गीता जयंती · 20 दिसंबर"]),
      ("कुरुक्षेत्र में, श्री कृष्ण ने, अर्जुन को, गीता का ज्ञान दिया।", ["कुरुक्षेत्र में श्री कृष्ण ने", "अर्जुन को गीता का ज्ञान दिया"]),
      ("अठारह अध्याय। सात सौ श्लोक।", ["18 अध्याय, 700 श्लोक"]),
      ("ये रील परिवार को भेजिए, और गीता जयंती पर, फिर देखिए।", ["ये रील परिवार को भेजिए", "और गीता जयंती पर फिर देखिए"])]
GAP = [0.35, 0.3, 0.45, 0.0]
LEAD = [0.15, 0, 0, 0]
voice, T0, T1, t = [], [], [], 0.0
for i, (say, _) in enumerate(VO):
    a = A.say(say, 'hm_omega', 1.0, 'hi'); pre = np.zeros(int(A.SR * LEAD[i]), np.float32)
    t += LEAD[i]; T0.append(t); t += len(a) / A.SR; T1.append(t)
    voice += [pre, a, np.zeros(int(A.SR * GAP[i]), np.float32)]; t += GAP[i]
TOT = t + 0.9
voice = np.concatenate(voice + [np.zeros(int(A.SR * 0.9), np.float32)])
print('VO', [round(x, 2) for x in T0], round(TOT, 2))

# ---------------- music: tanpura + santoor-style plucks + bells (same recipe as the Chitragupta reel) ----------------
SR = A.SR; N = len(voice)
def tt_(d): return np.arange(int(d * SR)) / SR
def add(buf, x, at, g=1.0):
    i = int(at * SR); x = x[:max(0, len(buf) - i)]; buf[i:i + len(x)] += x * g
def tanpura(f, d=2.4):
    t = tt_(d); x = np.zeros_like(t)
    for h in range(1, 12): x += (0.7 ** h) * np.sin(2 * np.pi * f * h * t + 0.3 * np.sin(2 * np.pi * 3 * t) * (h > 3)) * np.exp(-t * (0.8 + 0.25 * h))
    return x * np.minimum(1, t / 0.01)
def pluck(f, d=1.2):
    t = tt_(d); x = np.zeros_like(t)
    for h, a in [(1, 1), (2, .5), (3, .25), (4, .12)]: x += a * np.sin(2 * np.pi * f * h * t * (1 + 0.0007 * h)) * np.exp(-t * (3 + 2 * h))
    return x * np.minimum(1, t / 0.003)
def bell(f=880, d=3.0):
    t = tt_(d); x = np.zeros_like(t)
    for r, a, dc in [(1, 1, 1.0), (2.0, .5, 1.6), (2.76, .4, 2.2), (5.4, .2, 3.5)]: x += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dc)
    return x * np.minimum(1, t / 0.002)
def thump(d=0.5):
    t = tt_(d); f = 70 + 80 * np.exp(-t * 25); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
rng = np.random.default_rng(3)
def scratch(d):
    from scipy.signal import butter, sosfilt
    x = sosfilt(butter(2, [2500, 7000], 'band', fs=SR, output='sos'), rng.normal(0, 1, int(d * SR)))
    tt = tt_(d); return x * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * tt))) * np.minimum(1, tt / 0.03) * np.minimum(1, (d - tt) / 0.05)
def rewind(d=0.4):
    tt = tt_(d); f = 1800 - 1400 * tt / d; return np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 * np.sin(np.pi * tt / d)
music = np.zeros(N); sfx = np.zeros(N); SA = 146.83; beat = 60 / 92
cyc = [SA * 0.75, SA, SA, SA / 2]; x = 0; i = 0
while x < TOT: add(music, tanpura(cyc[i % 4] * 2), x, 0.22); x += beat; i += 1
scale = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2, 9 / 4, 5 / 2]; pat = [0, 2, 3, 4, 5, 4, 3, 2, 0, 3, 5, 7, 6, 5, 3, 4]
x = beat * 2; i = 0
while x < TOT - 1:
    if i % 8 not in (3, 7): add(music, pluck(SA * 2 * scale[pat[i % 16]]), x, 0.16)
    x += beat / 2; i += 1
x = 0; i = 0
while x < TOT: add(music, thump(), x, 0.3 if i % 4 == 0 else 0.15); x += beat; i += 1
add(sfx, bell(1046), 0.02, 0.16); add(sfx, rewind(), 0.8, 0.5); add(sfx, scratch(1.0), 1.3, 0.10)
add(sfx, bell(880, 3.5), T0[2], 0.2); add(sfx, bell(1174), T0[3], 0.12)
env = np.convolve(np.abs(voice), np.ones(int(.08 * SR)) / int(.08 * SR), 'same'); duck = 1 - 0.55 * np.minimum(1, env / 0.05)
mix = voice + music * duck * 0.5 + sfx; mix /= np.max(np.abs(mix)) * 1.05
sf.write(f'{OUT}/_gita_raw.wav', np.stack([mix, mix], 1), SR); A.loudnorm(f'{OUT}/_gita_raw.wav', f'{OUT}/_gita.wav')

# ---------------- art ----------------
KBLUE = '#4A78C2'; PIT = '#E8B730'; HORSE = '#FBF6E6'; HORSE2 = '#EADCB8'
DRAW_END = 6.6          # art-clock seconds to draw everything

def face(k, cx, cy, r, skin, T, crown_col=GOLD, feather=False, tilak=RED):
    s = r / 64.0
    def X(x): return cx + x * s
    def Y(y): return cy + y * s
    k.shape(oval(X(-62), Y(8), 12 * s, 22 * s), *T(0.02, 0.1), fill=skin, w=4)
    k.shape(oval(X(62), Y(8), 12 * s, 22 * s), *T(0.02, 0.1), fill=skin, w=4)
    k.shape(oval(cx, cy, 64 * s, 78 * s), *T(0.0, 0.14), fill=skin, w=5)
    for ex in [-62, 62]: k.shape(circ(X(ex), Y(40), 9 * s), *T(0.1, 0.16), fill=GOLD, w=3)
    # crown (mukut)
    k.shape(poly([(X(-66), Y(-60)), (X(-56), Y(-116)), (X(-34), Y(-104)), (X(-24), Y(-154)), (cx, Y(-194)), (X(24), Y(-154)),
                  (X(34), Y(-104)), (X(56), Y(-116)), (X(66), Y(-60))]), *T(0.1, 0.3), fill=crown_col, w=5)
    k.shape(rrect(X(-68), Y(-70), X(68), Y(-48), 6 * s), *T(0.16, 0.3), fill=RED, w=4)
    k.shape(circ(cx, Y(-108), 11 * s), *T(0.2, 0.32), fill=RED, w=3)
    if feather:   # peacock feather
        k.shape(P(('M', X(20), Y(-150)), ('Q', X(50), Y(-200), X(80), Y(-226))), *T(0.26, 0.4), w=4, col=GRN)
        k.shape(oval(X(84), Y(-236), 22 * s, 30 * s), *T(0.3, 0.44), fill=GRN, w=4)
        k.shape(oval(X(85), Y(-233), 12 * s, 17 * s), *T(0.34, 0.46), fill=GOLD, w=3)
        k.shape(oval(X(86), Y(-231), 6 * s, 8 * s), *T(0.36, 0.48), fill=IND, w=2)
    for sx in [-1, 1]:
        ex = 27 * sx
        k.shape(P(('M', X(ex - sx * 22), Y(-6)), ('Q', X(ex), Y(-22), X(ex + sx * 20), Y(-8)), ('Q', X(ex), Y(4), X(ex - sx * 22), Y(-6)), ('Z',)),
                *T(0.3, 0.4), fill='#FFFDF5', w=4)
        k.shape(circ(X(ex + sx * 2), Y(-8), 6.5 * s), *T(0.36, 0.42), fill=INK, w=0)
        k.shape(P(('M', X(ex - sx * 24), Y(-24)), ('Q', X(ex), Y(-38), X(ex + sx * 24), Y(-26))), *T(0.32, 0.42), w=5)
    k.shape(P(('M', cx, Y(-6)), ('Q', X(-7), Y(20), cx, Y(28)), ('Q', X(6), Y(30), X(10), Y(24))), *T(0.36, 0.44), w=4)
    k.shape(P(('M', X(-14), Y(48)), ('Q', cx, Y(58), X(14), Y(48))), *T(0.4, 0.46), w=4, col=RED)
    k.shape(P(('M', X(-8), Y(-32)), ('L', cx, Y(-60)), ('L', X(8), Y(-32))), *T(0.38, 0.46), w=5, col=tilak)

def horse(k, ox, oy, fill, T, saddle=RED):
    def Q(x, y): return (ox + x, oy + y)
    def PP(*pts): return poly([Q(*p) for p in pts])
    # legs (galloping)
    for (x0, y0, x1, y1, x2, y2) in [(-70, 30, -120, 80, -150, 120), (-40, 35, -60, 100, -50, 140), (60, 30, 90, 90, 70, 135), (90, 25, 140, 70, 170, 100)]:
        k.tube(P(('M', *Q(x0, y0)), ('Q', *Q(x1, y1), *Q(x2, y2))), *T(0.3, 0.5), fill, 16)
    k.shape(oval(ox, oy, 120, 50), *T(0.0, 0.25), fill=fill, w=5)
    k.shape(PP((-70, -20), (-150, -120), (-110, -140), (-40, -30)), *T(0.1, 0.3), fill=fill, w=5)
    k.shape(PP((-150, -130), (-222, -98), (-232, -74), (-206, -66), (-140, -92)), *T(0.15, 0.35), fill=fill, w=5)
    k.shape(PP((-138, -134), (-130, -166), (-118, -132)), *T(0.2, 0.36), fill=fill, w=4)
    k.shape(circ(*Q(-170, -106), 6), *T(0.3, 0.4), fill=INK, w=0)
    for j in range(6):   # mane
        mx, my = -150 + j * 20, -128 + j * 18
        k.shape(P(('M', *Q(mx, my)), ('Q', *Q(mx + 22, my - 18), *Q(mx + 26, my + 6))), *T(0.3 + j * 0.02, 0.5), fill=SAF, w=4)
    k.shape(P(('M', *Q(112, -18)), ('Q', *Q(176, -40), *Q(170, 50))), *T(0.35, 0.55), w=10, col=INK)
    # saddle cloth with gold dots
    k.shape(P(('M', *Q(-30, -46)), ('L', *Q(60, -46)), ('Q', *Q(70, 10), *Q(50, 36)), ('L', *Q(-20, 36)), ('Q', *Q(-40, 0), *Q(-30, -46)), ('Z',)), *T(0.4, 0.6), fill=saddle, w=4)
    for j in range(4): k.shape(circ(*Q(-10 + j * 20, 20), 5), *T(0.5, 0.64), fill=GOLDL, w=2)
    k.shape(P(('M', *Q(-205, -82)), ('L', *Q(-150, -96))), *T(0.4, 0.6), w=4, col=RED)   # bridle

def art(c, kt, tt):
    k = Ink(c, kt)
    T = lambda a, b: (a * DRAW_END, b * DRAW_END)
    Tr = lambda a0, a1: (lambda x, y: (DRAW_END * (a0 + (a1 - a0) * x), DRAW_END * (a0 + (a1 - a0) * y)))
    c.save(); c.translate(0, 10)
    # ground + distant battlefield flags
    k.shape(P(('M', 70, 1050), ('Q', 540, 1030, 1010, 1050)), *T(0.0, 0.08), w=6)
    for j, x in enumerate([110, 210, 870, 960]):
        k.shape(P(('M', x, 1040), ('L', x, 960)), *T(0.03 + j * .01, 0.1), w=4)
        k.shape(poly([(x, 962), (x + 40, 974), (x, 986)]), *T(0.05 + j * .01, 0.12), fill=[SAF, RED, GOLD, IND][j], w=3)
    # horses (back one first)
    horse(k, 345, 850, HORSE2, Tr(0.06, 0.26), saddle=IND)
    horse(k, 250, 905, HORSE, Tr(0.1, 0.3))
    # yoke pole
    k.shape(P(('M', 400, 880), ('Q', 300, 860, 190, 850)), *T(0.28, 0.34), w=9, col='#8A5A2B')
    # Arjuna (behind, right)
    k.shape(P(('M', 590, 790), ('Q', 600, 700, 650, 690), ('Q', 700, 700, 712, 790), ('Z',)), *T(0.34, 0.42), fill=RED, w=5)
    k.shape(P(('M', 612, 720), ('Q', 650, 750, 690, 720)), *T(0.38, 0.44), w=5, col=GOLD)
    k.shape(P(('M', 606, 750), ('Q', 650, 780, 698, 750)), *T(0.4, 0.46), w=4, col=GOLD)
    face(k, 650, 625, 44, SKIN, Tr(0.36, 0.58))
    # bow (gandiva) held upright
    k.shape(P(('M', 735, 560), ('Q', 795, 680, 735, 800)), *T(0.5, 0.58), w=9, col='#8A5A2B')
    k.shape(P(('M', 735, 560), ('L', 735, 800)), *T(0.54, 0.6), w=2.5, col=INK)
    k.tube(P(('M', 700, 708), ('Q', 722, 690, 738, 660)), *T(0.52, 0.6), SKIN, 22)
    # Krishna (charioteer, front)
    k.shape(P(('M', 400, 800), ('Q', 410, 715, 455, 705), ('Q', 500, 715, 512, 800), ('Z',)), *T(0.42, 0.5), fill=PIT, w=5)
    k.shape(P(('M', 418, 730), ('Q', 455, 770, 494, 730)), *T(0.46, 0.52), w=5, col=RED)
    face(k, 456, 640, 46, KBLUE, Tr(0.44, 0.7), feather=True)
    k.tube(P(('M', 418, 728), ('Q', 380, 760, 360, 800)), *T(0.6, 0.68), KBLUE, 22)
    for dy in (0, 14):   # reins to both bridles
        k.shape(P(('M', 360, 800 + dy), ('Q', 200, 740 + dy, 66, 804 + dy * 2)), *T(0.66, 0.74), w=3, col=RED)
    # chariot body + wheel
    k.shape(poly([(380, 790), (790, 790), (810, 920), (360, 920)]), *T(0.5, 0.64), fill=RED, w=6)
    k.shape(P(('M', 372, 840), ('L', 798, 840)), *T(0.56, 0.66), w=8, col=GOLD)
    for j in range(7): k.shape(circ(410 + j * 60, 880, 9), *T(0.58 + j * .005, 0.68), fill=GOLDL, w=3)
    cx, cy, R = 585, 950, 112
    k.shape(circ(cx, cy, R), *T(0.62, 0.76), fill=GOLD, w=7)
    k.shape(circ(cx, cy, R - 22), *T(0.64, 0.78), fill=PAPER, w=5)
    rot = tt * 0.0 if kt >= DRAW_END else 0
    for j in range(8):
        a = j * math.pi / 4 + rot
        k.shape(P(('M', cx, cy), ('L', cx + math.cos(a) * (R - 22), cy + math.sin(a) * (R - 22))), *T(0.68 + j * .006, 0.8), w=6)
    k.shape(circ(cx, cy, 20), *T(0.74, 0.82), fill=RED, w=5)
    # flag
    k.shape(P(('M', 800, 790), ('L', 800, 600)), *T(0.76, 0.82), w=7, col='#8A5A2B')
    wav = 6 * math.sin(tt * 4) if kt >= DRAW_END * .9 else 0
    k.shape(P(('M', 800, 606), ('Q', 860, 612 + wav, 930, 640), ('Q', 860, 662 - wav, 800, 680), ('Z',)), *T(0.8, 0.9), fill=SAF, w=5)
    k.shape(circ(842, 641, 10), *T(0.86, 0.92), fill=RED, w=3)
    c.restore()

# ---------------- frames ----------------
BG = skia.Image.fromarray(make_bg()); BORDER = border_layer()
def countup(n, p): return int(round(n * ease(p)))
def nib(c, x, y):
    k = Ink(c, 99); quill(k, x, y, x + 120, y - 150, 0, 1)

boxes_bad = []
def chk(label, cx, cy, w, h, t):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    out = x0 < SAFE[0] or y0 < SAFE[1] or x1 > SAFE[2] or y1 > SAFE[3]
    rail = x1 > RAIL[0] and y1 > RAIL[1] and y0 < RAIL[3]
    if out or rail: boxes_bad.append((round(t, 2), label, [int(v) for v in (x0, y0, x1, y1)]))

def caption(c, t):
    for i, (_, rows) in enumerate(VO):
        if T0[i] - 0.05 <= t <= T1[i] + 0.25:
            n = len(rows); seg = (T1[i] - T0[i]) / n
            j = min(n - 1, int((t - T0[i]) / seg)) if t >= T0[i] else 0
            txt = rows[j]; a0 = T0[i] + j * seg
            pop = back((t - a0) / 0.18)
            w = text_w(txt, F_HB, 54) + 60; h = 94; cy = 1150
            c.save(); c.translate(520, cy); s = 0.9 + 0.1 * pop; c.scale(s, s)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 26, 26), skia.Paint(AntiAlias=True, Color=C(INK, 230)))
            draw_text(c, txt, 0, 0, F_HB, 54, CREAM); c.restore()
            chk('caption', 520, cy, w, h, t)

def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas()
    c.drawImage(BG, 0, 0); c.drawImage(BORDER, 0, 0)
    if t < 0.8: kt = 99
    elif t < 1.2: kt = DRAW_END * (1 - eio((t - 0.8) / 0.4))
    else: kt = t - 1.2
    art(c, kt, t)
    # headline (on from frame 0: hook inside 1.5 s)
    w, h = draw_text(c, "गीता जयंती", 540, 330, F_Y, 104, RED, stroke=6, sfill=CREAM); chk('headline', 540, 330, w, h, t)
    # date line written by the quill (payoff shows it complete)
    rv = 1 if t < 0.8 else clamp((t - 1.3) / 1.0)
    w, h = draw_text(c, "रविवार, 20 दिसंबर", 540, 412, F_HB, 52, INK, reveal=rv); chk('date', 540, 412, w, h, t)
    if 0.8 < t and 0 < rv < 1: nib(c, 540 - w / 2 + w * rv, 428)
    # count-up during line 2
    if t >= T0[2] - 0.1:
        p = (t - T0[2]) / max(0.6, (T1[2] - T0[2]) * 0.45); p2 = (t - (T0[2] + (T1[2] - T0[2]) * 0.5)) / 0.7
        for (n, lab, x, pp) in [(18, "अध्याय", 245, p), (700, "श्लोक", 835, p2)]:
            if pp <= 0: continue
            sc = 0.8 + 0.2 * back(pp / 0.4)
            c.save(); c.translate(x, 520); c.scale(sc, sc)
            r = skia.Rect(-125, -52, 125, 52)
            c.drawRRect(skia.RRect.MakeRectXY(r, 22, 22), skia.Paint(AntiAlias=True, Color=C(CREAM, 245)))
            c.drawRRect(skia.RRect.MakeRectXY(r, 22, 22), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(INK)))
            draw_text(c, f"{countup(n, pp)} {lab}", 0, 4, F_Y, 52, RED, stroke=3, sfill=CREAM); c.restore()
            chk('count', x, 520, 250 * sc, 104 * sc, t)
    caption(c, t)
    # mid nudge (~40%) and end ask: big blinking send chip under the captions
    for (a, d) in [(TOT * 0.4, 1.6), (T0[3], TOT - T0[3])]:
        if a <= t <= a + d:
            on = int((t - a) / 0.45) % 2 == 0
            bg, fg = (RED, CREAM) if on else (CREAM, RED)
            r = chip(c, "परिवार को भेजिए", 470, 1325, 58, bg, fg, 1, scale=0.9 + 0.1 * back((t - a) / 0.3))
    return s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]

n = int(TOT * FPS); vid = f'{OUT}/_gita_v.mp4'
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
stills = [0.4, 1.0, 2.0, 3.5, 5.0, 6.5, T0[2] + 1.2, TOT - 0.4]; sheet = []
for i in range(n):
    t = i / FPS; arr = frame(t)
    if any(abs(t - s) < 0.5 / FPS for s in stills): sheet.append((t, Image.fromarray(np.ascontiguousarray(arr))))
    p.stdin.write(np.ascontiguousarray(arr).tobytes())
p.stdin.close(); p.wait()
final = f'{OUT}/Scout1_GitaJayanti_Kalamkari_HI.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', f'{OUT}/_gita.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final], check=True)
os.remove(vid)
# contact sheet with safe-zone overlay
tw, th = 270, 480; sh = Image.new('RGB', (len(sheet) * (tw + 8) + 8, th + 16), (250, 250, 250))
for j, (t, im) in enumerate(sheet):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for r in [(0, 0, W, 269), (0, 1248, W, H), (0, 269, 65, 1248), (1015, 269, W, 1248)]: od.rectangle(r, fill=(230, 40, 40, 85))
    od.rectangle(RAIL, fill=(255, 170, 0, 85))
    sh.paste(Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').resize((tw, th)), (8 + j * (tw + 8), 8))
sh.save(f'{OUT}/Scout1_GitaJayanti_contact_safezone.png')
print(final, round(TOT, 1), 's; safe-zone violations:', len(boxes_bad), boxes_bad[:5])
