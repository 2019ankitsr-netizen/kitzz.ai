import os, sys, math, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FD = '/home/claude/fonts/'
_fc = {}
def F(size, w='Bold'):
    k = (size, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + f'Mukta-{w}.ttf', size, layout_engine=ImageFont.Layout.RAQM)
    return _fc[k]

LINES = [l.strip() for l in open('lines.txt', encoding='utf-8') if l.strip()]
def vodur(i):
    w = wave.open(f'vo2/{i}_48.wav'); return w.getnframes() / w.getframerate()
VO_OFF = 0.25
DUR = [vodur(i + 1) + 0.55 for i in range(8)]
DUR[7] += 2.6  # end card
START = np.concatenate([[0], np.cumsum(DUR)])[:8]

# event times (local to scene)
CANCEL_T = [VO_OFF + 1.65, VO_OFF + 4.6, VO_OFF + 6.75]
S5_USER, S5_TYPING, S5_REPLY = 0.4, 4.5, 6.2
S6_ASK = 0.35
S6_OFF = [4.1 + i * 0.6 for i in range(6)]

rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 9, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = np.clip(1.15 - 0.75 * (((xx - W / 2) / (W * 0.72)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2), 0.25, 1.0)[..., None]

def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def clamp(x, a=0, b=1): return min(max(x, a), b)

def finish(img, t, grade=(0.92, 1.0, 1.06), red=0.0, flash=0.0):
    a = np.asarray(img.convert('RGB'), dtype=np.float32)
    g = np.array(grade, np.float32)
    if red > 0:
        lum = a.mean(2, keepdims=True)
        a = a * (1 - red) + lum * np.array([1.25, 0.45, 0.42], np.float32) * red
    a = a * g
    gi = GRAIN[int(t * FPS) % 6]
    a = a * VIG + np.repeat(np.repeat(gi, 2, 0), 2, 1)[..., None]
    if flash: a = a + flash * 255
    return np.clip(a, 0, 255).astype(np.uint8)

def wrap(text, font, maxw):
    words = text.split(' '); lines = []; cur = ''
    for w_ in words:
        tr = (cur + ' ' + w_).strip()
        if font.getlength(tr) <= maxw: cur = tr
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def chunks(i):
    """subtitle chunks with times proportional to char count"""
    line = LINES[i]
    parts, cur = [], ''
    for ch in line:
        cur += ch
        if ch in '।?' or cur.endswith('...'):
            parts.append(cur.strip()); cur = ''
    if cur.strip(): parts.append(cur.strip())
    # merge tiny parts
    m = []
    for p in parts:
        if m and len(m[-1]) < 14: m[-1] += ' ' + p
        else: m.append(p)
    tot = sum(len(p) for p in m); d = vodur(i + 1) - 0.2; t = VO_OFF; out = []
    for p in m:
        dd = d * len(p) / tot; out.append((t, t + dd, p)); t += dd
    return out
CHUNKS = [chunks(i) for i in range(8)]

def subtitle(img, i, t, y=1590):
    for a, b, p in CHUNKS[i]:
        if a <= t < b + 0.15:
            d = ImageDraw.Draw(img); f = F(62, 'ExtraBold')
            ls = wrap(p.replace('...', '…'), f, 900)
            for k, l in enumerate(ls):
                d.text((W / 2, y + k * 80), l, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
            break

# ---------------- shared drawings ----------------
def phone(screen, bg=(14, 16, 20), y0=300, shake=(0, 0)):
    img = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(img)
    # soft glow
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).rounded_rectangle((200, y0 - 20, 880, y0 + 1220), 80, fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.composite(Image.new('RGB', (W, H), (60, 90, 110)), img, glow)
    d = ImageDraw.Draw(img)
    x0 = 230 + shake[0]; yb = y0 + shake[1]
    d.rounded_rectangle((x0, yb, x0 + 620, yb + 1180), 70, fill=(28, 30, 34), outline=(70, 74, 80), width=4)
    img.paste(screen, (x0 + 20, yb + 20), rounded_mask(screen.size, 52))
    d.rounded_rectangle((x0 + 240, yb + 34, x0 + 380, yb + 66), 16, fill=(8, 8, 10))
    return img

_masks = {}
def rounded_mask(size, r):
    if (size, r) not in _masks:
        m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255); _masks[(size, r)] = m
    return _masks[(size, r)]

SW, SH = 580, 1140
def map_screen(seed=3):
    rnd = random.Random(seed)
    s = Image.new('RGB', (SW, SH), (24, 30, 38)); d = ImageDraw.Draw(s)
    for _ in range(14):
        if rnd.random() < 0.5:
            x = rnd.randint(0, SW); d.line((x, 0, x + rnd.randint(-200, 200), SH), fill=(44, 52, 62), width=rnd.choice([6, 10, 18]))
        else:
            y = rnd.randint(0, SH); d.line((0, y, SW, y + rnd.randint(-200, 200)), fill=(44, 52, 62), width=rnd.choice([6, 10, 18]))
    for _ in range(25):
        x, y = rnd.randint(0, SW), rnd.randint(0, SH); d.rectangle((x, y, x + rnd.randint(30, 90), y + rnd.randint(30, 90)), fill=(30, 37, 46))
    d.line((120, 900, 200, 640, 380, 520, 430, 300), fill=(80, 170, 255), width=10, joint='curve')
    d.ellipse((105, 885, 135, 915), fill=(80, 170, 255));
    d.ellipse((410, 270, 450, 310), fill=(240, 240, 240))
    # top bar
    d.rectangle((0, 0, SW, 150), fill=(16, 18, 22))
    d.text((40, 95), 'RideGo', font=F(44, 'ExtraBold'), fill=(255, 255, 255), anchor='lm')
    d.text((SW - 40, 95), '8:10', font=F(36, 'Medium'), fill=(200, 200, 200), anchor='rm')
    # bottom sheet
    d.rounded_rectangle((0, 820, SW, SH + 40), 40, fill=(18, 20, 24))
    d.text((40, 880), 'हिंजेवाड़ी फ़ेज़ 2', font=F(40, 'Bold'), fill=(255, 255, 255), anchor='lm')
    d.text((40, 935), 'ऑफ़िस · 14 किमी', font=F(32, 'Medium'), fill=(150, 156, 166), anchor='lm')
    return s

MAP = map_screen()

def notif(sw, title, body, alpha=1.0):
    n = Image.new('RGBA', (sw - 40, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(n)
    d.rounded_rectangle((0, 0, sw - 41, 149), 30, fill=(245, 245, 247, int(245 * alpha)))
    d.ellipse((24, 37, 100, 113), fill=(225, 50, 55, int(255 * alpha)))
    d.line((48, 61, 76, 89), fill=(255, 255, 255, int(255 * alpha)), width=8); d.line((76, 61, 48, 89), fill=(255, 255, 255, int(255 * alpha)), width=8)
    d.text((124, 52), title, font=F(36, 'ExtraBold'), fill=(20, 20, 24, int(255 * alpha)), anchor='lm')
    d.text((124, 100), body, font=F(29, 'Medium'), fill=(80, 80, 90, int(255 * alpha)), anchor='lm')
    return n

# ---------------- scene 1: hook ----------------
def s1(t):
    sc = MAP.copy().convert('RGBA')
    p = ease((t - 0.35) / 0.45)
    if p > 0:
        n = notif(SW, 'राइड कैंसिल हो गई', 'ड्राइवर ने आपकी राइड कैंसिल कर दी')
        sc.alpha_composite(n, (20, int(-160 + p * 210)))
    sh = (0, 0)
    if 0.75 < t < 1.1: sh = (int(10 * math.sin(t * 90)), 0)
    img = phone(sc.convert('RGB'), shake=sh, y0=330)
    d = ImageDraw.Draw(img)
    a = clamp((t - 3.6) / 0.6)
    if a > 0:
        col = tuple(int(c * a + 14 * (1 - a)) for c in (235, 60, 60))
        d.text((W / 2, 150), 'आख़िरी इम्यून', font=F(110, 'ExtraBold'), fill=col, anchor='mm')
        col2 = tuple(int(c * a + 14 * (1 - a)) for c in (210, 210, 215))
        d.text((W / 2, 255), 'EPISODE 1  ·  नॉर्मल सुबह', font=F(40, 'Bold'), fill=col2, anchor='mm')
    subtitle(img, 0, t)
    return finish(img, t, flash=0.35 * clamp(1 - abs(t - 0.8) / 0.12))

# ---------------- scene 2: morning room ----------------
def build_room():
    S = 1.15; w, h = int(W * S), int(H * S)
    img = Image.new('RGB', (w, h), (30, 32, 38)); d = ImageDraw.Draw(img)
    # wall
    for y in range(h):
        k = y / h; d.line((0, y, w, y), fill=(int(46 - 16 * k), int(48 - 16 * k), int(56 - 14 * k)))
    # window
    wx0, wy0, wx1, wy1 = 170, 230, w - 170, 1180
    for y in range(wy0, wy1):
        k = (y - wy0) / (wy1 - wy0)
        c = (int(150 + 90 * k), int(165 + 50 * k), int(190 - 10 * k))
        d.line((wx0, y, wx1, y), fill=c)
    sun = Image.new('L', (w, h), 0); ImageDraw.Draw(sun).ellipse((w * 0.62 - 60, 860, w * 0.62 + 190, 1110), fill=150)
    img = Image.composite(Image.new('RGB', (w, h), (255, 200, 140)), img, sun.filter(ImageFilter.GaussianBlur(50))); d = ImageDraw.Draw(img)
    d.ellipse((w * 0.62, 920, w * 0.62 + 130, 1050), fill=(255, 214, 150))
    rnd = random.Random(4); x = wx0
    while x < wx1:
        bw = rnd.randint(40, 110); bh = rnd.randint(120, 430)
        d.rectangle((x, wy1 - bh, x + bw, wy1), fill=(96, 104, 122)); x += bw + rnd.randint(0, 12)
    x = wx0
    while x < wx1:
        bw = rnd.randint(60, 150); bh = rnd.randint(60, 260)
        d.rectangle((x, wy1 - bh, x + bw, wy1), fill=(70, 76, 92)); x += bw
    # frame & bars
    d.rectangle((wx0 - 26, wy0 - 26, wx1 + 26, wy1 + 26), outline=(22, 22, 26), width=34)
    d.line(((wx0 + wx1) / 2, wy0, (wx0 + wx1) / 2, wy1), fill=(22, 22, 26), width=22)
    d.line((wx0, (wy0 + wy1) / 2, wx1, (wy0 + wy1) / 2), fill=(22, 22, 26), width=16)
    # curtains
    d.polygon([(0, 150), (300, 150), (230, 1500), (0, 1560)], fill=(60, 40, 44))
    d.polygon([(w, 150), (w - 300, 150), (w - 230, 1500), (w, 1560)], fill=(60, 40, 44))
    d.rectangle((0, 130, w, 165), fill=(20, 20, 22))
    # desk
    d.rectangle((0, 1430, w, h), fill=(52, 38, 30)); d.rectangle((0, 1430, w, 1460), fill=(78, 58, 44))
    # light from window on desk
    ov = Image.new('L', (w, h), 0); ImageDraw.Draw(ov).polygon([(wx0, 1460), (wx1, 1460), (wx1 + 200, h), (wx0 - 200, h)], fill=60)
    img = Image.composite(Image.new('RGB', (w, h), (255, 220, 170)), img, ov.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(img)
    # clock
    d.rounded_rectangle((170, 1270, 560, 1450), 26, fill=(18, 18, 20), outline=(50, 50, 54), width=4)
    # bag
    d.rounded_rectangle((w - 470, 1240, w - 170, 1450), 40, fill=(34, 40, 48)); d.arc((w - 400, 1170, w - 240, 1300), 180, 360, fill=(34, 40, 48), width=18)
    # cup
    d.rounded_rectangle((640, 1330, 760, 1450), 16, fill=(225, 225, 230)); d.arc((735, 1355, 800, 1420), 270, 90, fill=(225, 225, 230), width=12)
    return img
ROOM = build_room()

def s2(t):
    S = 1.15; z = 1.0 + 0.07 * (t / DUR[1])
    cw, ch = int(W * S / z), int(H * S / z)
    cx, cy = ROOM.width / 2, ROOM.height / 2 + 60 * (t / DUR[1])
    img = ROOM.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(img, 'RGBA')
    # mapping helper from room coords to screen
    def m(x, y): return ((x - (cx - cw / 2)) * W / cw, (y - (cy - ch / 2)) * H / ch)
    sc = W / cw
    # clock digits
    x, y = m(365, 1360); blink = (int(t * 2) % 2 == 0)
    d.text((x, y), '08:10' if blink else '08 10', font=F(int(110 * sc), 'ExtraBold'), fill=(255, 80, 70), anchor='mm')
    # steam
    for k in range(3):
        pts = []
        for j in range(30):
            yy_ = 1320 - j * 9
            xx_ = 690 + k * 22 + 14 * math.sin(j * 0.35 + t * 2.2 + k * 2)
            pts.append(m(xx_, yy_))
        d.line(pts, fill=(255, 255, 255, 60), width=max(2, int(6 * sc)))
    subtitle(img, 1, t)
    return finish(img, t, grade=(1.0, 0.98, 0.98))

# ---------------- scene 3: cancels ----------------
def spinner(d, cx, cy, t):
    for k in range(8):
        a = k / 8 * 2 * math.pi + t * 6
        al = int(255 * (k + 1) / 8)
        d.ellipse((cx + 30 * math.cos(a) - 6, cy + 30 * math.sin(a) - 6, cx + 30 * math.cos(a) + 6, cy + 30 * math.sin(a) + 6), fill=(80, 170, 255, al))

def s3(t):
    sc = MAP.copy().convert('RGBA'); d = ImageDraw.Draw(sc)
    # searching state in sheet
    d.rounded_rectangle((0, 820, SW, SH + 40), 40, fill=(18, 20, 24))
    n_c = sum(1 for c in CANCEL_T if t >= c)
    d.text((40, 880), 'ड्राइवर ढूंढ रहे हैं…' if n_c < 3 else 'कोई ड्राइवर उपलब्ध नहीं', font=F(40, 'Bold'), fill=(255, 255, 255) if n_c < 3 else (255, 90, 90), anchor='lm')
    d.text((40, 935), f'कोशिश {min(n_c + 1, 3)} / 3', font=F(32, 'Medium'), fill=(150, 156, 166), anchor='lm')
    if n_c < 3: spinner(d, SW / 2, 1040, t)
    shake = (0, 0)
    for k, c in enumerate(CANCEL_T):
        p = ease((t - c) / 0.35)
        if p > 0:
            n = notif(SW, 'राइड कैंसिल हो गई' + ('' if k == 0 else f' ({k + 1})'), 'ड्राइवर ने आपकी राइड कैंसिल कर दी')
            sc.alpha_composite(n, (20, int(-160 + p * (170 + 170 * (len([c2 for c2 in CANCEL_T if c2 <= t]) - 1 - k)) + 40)))
        if 0 < t - c < 0.3: shake = (int(12 * math.sin((t - c) * 80)), 0)
    img = phone(sc.convert('RGB'), shake=shake, y0=330)
    subtitle(img, 2, t)
    fl = max([clamp(1 - abs(t - c - 0.05) / 0.1) for c in CANCEL_T])
    return finish(img, t, flash=0.25 * fl)

# ---------------- scene 4 & 8: empty street ----------------
def build_street(night=False):
    S = 1.3; w, h = int(W * S), int(H * S)
    img = Image.new('RGB', (w, h)); d = ImageDraw.Draw(img)
    vpx, vpy = w / 2, h * 0.40
    for y in range(h):
        k = clamp(y / (vpy + 80))
        c = (int(120 + 85 * k), int(130 + 75 * k), int(146 + 60 * k))
        d.line((0, y, w, y), fill=c)
    ground = h * 1.02
    def gy(s): return vpy + s * (ground - vpy)
    road_half = w * 0.42; side = w * 0.62
    d.polygon([(vpx, vpy), (vpx - side, gy(1)), (vpx + side, gy(1))], fill=(105, 108, 114))
    d.polygon([(vpx, vpy), (vpx - road_half, gy(1)), (vpx + road_half, gy(1))], fill=(62, 64, 70))
    # lane dashes
    s = 0.05
    while s < 1:
        s2_ = s * 1.18
        d.polygon([(vpx - 6 * s, gy(s)), (vpx + 6 * s, gy(s)), (vpx + 6 * s2_, gy(s2_)), (vpx - 6 * s2_, gy(s2_))], fill=(210, 210, 200)); s = s2_ * 1.25
    rnd = random.Random(11)
    for sign in (-1, 1):
        s = 1.0; blocks = []
        while s > 0.04:
            s_far = s * rnd.uniform(0.62, 0.78); hgt = rnd.uniform(0.9, 1.9) * h * 0.55
            blocks.append((s, s_far, hgt)); s = s_far
        for s_near, s_far, hgt in reversed(blocks):
            xn = vpx + sign * s_near * side; xf = vpx + sign * s_far * side
            tn = vpy - s_near * hgt * 0.62; tf = vpy - s_far * hgt * 0.62
            shade = rnd.randint(70, 100)
            col = (shade, shade + 4, shade + 12)
            d.polygon([(xn, gy(s_near)), (xn, tn), (xf, tf), (xf, gy(s_far))], fill=col)
            # windows
            rows = 8; cols = 4
            for r in range(rows):
                for cidx in range(cols):
                    u0, u1 = (cidx + 0.2) / cols, (cidx + 0.75) / cols
                    v0, v1 = (r + 0.25) / rows * 0.85, (r + 0.75) / rows * 0.85
                    def P(u, v):
                        x = xn + (xf - xn) * u; top = tn + (tf - tn) * u; bot = gy(s_near) + (gy(s_far) - gy(s_near)) * u
                        return (x, top + (bot - top) * v)
                    lit = rnd.random() < (0.06 if not night else 0.03)
                    wc = (255, 214, 150) if lit else (max(0, shade - 28), max(0, shade - 24), shade - 12)
                    d.polygon([P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)], fill=wc)
            # front face edge
            d.line((xn, gy(s_near), xn, tn), fill=(shade - 20, shade - 18, shade - 10), width=3)
    # abandoned rickshaw on left lane
    rs = 0.42; rx = vpx - road_half * rs * 0.55; ry = gy(rs)
    k = rs * 260
    d.rounded_rectangle((rx - k * 0.5, ry - k * 0.9, rx + k * 0.5, ry), int(k * 0.2), fill=(30, 34, 30))
    d.rectangle((rx - k * 0.42, ry - k * 0.5, rx + k * 0.42, ry - k * 0.12), fill=(196, 170, 40))
    d.ellipse((rx - k * 0.45, ry - k * 0.12, rx - k * 0.2, ry + k * 0.1), fill=(20, 20, 20)); d.ellipse((rx + k * 0.2, ry - k * 0.12, rx + k * 0.45, ry + k * 0.1), fill=(20, 20, 20))
    # traffic signal pole right
    ps = 0.55; px = vpx + road_half * ps * 1.05; py = gy(ps)
    d.rectangle((px - 6, py - 520 * ps, px + 6, py), fill=(30, 30, 34))
    d.rounded_rectangle((px - 36 * ps * 1.6, py - 620 * ps, px + 36 * ps * 1.6, py - 400 * ps), 10, fill=(24, 24, 26))
    # fog
    fog = Image.new('L', (w, h), 0); fd = ImageDraw.Draw(fog)
    for y in range(h):
        a = math.exp(-((y - vpy) / (h * 0.18)) ** 2) * 200; fd.line((0, y, w, y), fill=int(a))
    img = Image.composite(Image.new('RGB', (w, h), (190, 196, 204)), img, fog)
    # scattered paper
    d = ImageDraw.Draw(img)
    for _ in range(30):
        s = rnd.uniform(0.3, 1.0); x = vpx + rnd.uniform(-1, 1) * road_half * s; y = gy(s); r = 10 * s
        d.polygon([(x - r, y), (x + r, y - r * 0.4), (x + r * 0.8, y + r * 0.5)], fill=(200, 200, 196))
    sigpos = (px, py - 510 * ps, 22 * ps * 1.6)
    return img, (vpx, vpy, gy, road_half), sigpos

STREET, STREET_GEO, SIG = build_street()

def railing(img, alpha=255):
    d = ImageDraw.Draw(img, 'RGBA')
    d.rectangle((0, 1380, W, 1410), fill=(18, 18, 20, alpha))
    for x in range(-20, W + 40, 95): d.rectangle((x, 1410, x + 16, H), fill=(18, 18, 20, alpha))
    d.rectangle((0, H - 120, W, H), fill=(14, 14, 16, alpha))
    # plant
    d.ellipse((60, 1250, 260, 1420), fill=(28, 46, 30, alpha)); d.ellipse((140, 1200, 300, 1380), fill=(34, 56, 36, alpha))

def street_view(t, z, cx, cy, sig_on):
    S = STREET; cw, ch = W * 1.3 / z, H * 1.3 / z
    img = S.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(img, 'RGBA')
    sx, sy, sr = SIG
    X = (sx - (cx - cw / 2)) * W / cw; Y = (sy - (cy - ch / 2)) * H / ch; R = sr * W / cw
    if sig_on:
        d.ellipse((X - R * 3, Y - R * 3, X + R * 3, Y + R * 3), fill=(255, 170, 40, 50)); d.ellipse((X - R, Y - R, X + R, Y + R), fill=(255, 180, 50))
    else:
        d.ellipse((X - R, Y - R, X + R, Y + R), fill=(70, 50, 20))
    return img, (lambda x, y: ((x - (cx - cw / 2)) * W / cw, (y - (cy - ch / 2)) * H / ch)), W / cw

def s4(t):
    p = t / DUR[3]
    z = 1.0 + 0.06 * p
    img, _, _ = street_view(t, z, STREET.width / 2 - 60 + 120 * p, STREET.height / 2 - 60, int(t * 1.5) % 2 == 0)
    railing(img)
    # birds
    d = ImageDraw.Draw(img)
    for k in range(4):
        bx = 200 + k * 70 + t * 60; by = 380 + 30 * math.sin(k * 2.1) - t * 8
        wv = 10 * math.sin(t * 9 + k)
        d.line((bx - 18, by - wv, bx, by, bx + 18, by - wv), fill=(40, 44, 50), width=4)
    subtitle(img, 3, t)
    return finish(img, t, grade=(0.9, 0.98, 1.06))

# ---------------- scene 5/6: chat ----------------
NAMES = ['राहुल', 'प्रिया', 'अमित', 'स्नेहा', 'विक्रम', 'नेहा']
COLS = [(220, 110, 60), (120, 90, 200), (60, 150, 110), (200, 80, 130), (70, 130, 200), (190, 150, 50)]

def chat_base():
    s = Image.new('RGBA', (SW, SH), (32, 33, 44, 255)); d = ImageDraw.Draw(s)
    d.rectangle((0, 0, SW, 170), fill=(46, 46, 66))
    d.text((40, 85), 'Pune Data Team', font=F(40, 'ExtraBold'), fill=(255, 255, 255), anchor='lm')
    d.text((40, 135), '6 सदस्य', font=F(28, 'Medium'), fill=(170, 170, 190), anchor='lm')
    d.rounded_rectangle((24, SH - 110, SW - 24, SH - 30), 40, fill=(48, 49, 62))
    d.text((60, SH - 70), 'मैसेज लिखें…', font=F(30, 'Medium'), fill=(130, 130, 150), anchor='lm')
    return s

def bubble(s, text, mine, y, alpha=1.0, name=None, col=(0, 0, 0)):
    d = ImageDraw.Draw(s); f = F(34, 'Bold')
    ls = wrap(text, f, 380); bw = max(f.getlength(l) for l in ls) + 56; bh = len(ls) * 48 + 36 + (40 if name else 0)
    x = SW - 30 - bw if mine else 100
    fill = (98, 100, 200) if mine else (60, 62, 78)
    d.rounded_rectangle((x, y, x + bw, y + bh), 28, fill=fill + (int(255 * alpha),))
    yy_ = y + 22
    if name:
        d.text((x + 28, yy_ + 14), name, font=F(28, 'ExtraBold'), fill=col + (int(255 * alpha),), anchor='lm'); yy_ += 40
    for l in ls:
        d.text((x + 28, yy_ + 22), l, font=f, fill=(255, 255, 255, int(255 * alpha)), anchor='lm'); yy_ += 48
    if not mine:
        d.ellipse((24, y + bh - 64, 84, y + bh - 4), fill=col + (int(255 * alpha),))
        d.text((54, y + bh - 34), name[0] if name else 'R', font=F(30, 'ExtraBold'), fill=(255, 255, 255, int(255 * alpha)), anchor='mm')
    return bh

def s5(t):
    s = chat_base(); d = ImageDraw.Draw(s)
    d.text((SW / 2, 220), 'आज, 8:14 AM', font=F(26, 'Medium'), fill=(140, 140, 160), anchor='mm')
    y = 270
    a = ease((t - S5_USER) / 0.3)
    if a > 0:
        y += bubble(s, 'Guys कैब नहीं मिल रही 😅 आज WFH कर लूं?'.replace('😅', ''), True, y + int(30 * (1 - a)), a) + 30
    if S5_TYPING <= t < S5_REPLY:
        d.rounded_rectangle((100, y, 220, y + 70), 30, fill=(60, 62, 78))
        for k in range(3):
            o = 8 * math.sin(t * 10 - k * 0.8)
            d.ellipse((125 + k * 30, y + 28 - o, 141 + k * 30, y + 44 - o), fill=(200, 200, 210))
        d.text((240, y + 35), 'राहुल लिख रहा है…', font=F(26, 'Medium'), fill=(150, 150, 170), anchor='lm')
    a2 = ease((t - S5_REPLY) / 0.3)
    if a2 > 0:
        bubble(s, 'भाई आज ऑफिस मत आना। बाहर बिल्कुल मत निकलना।', False, y + int(30 * (1 - a2)), a2, 'राहुल', COLS[0])
    img = phone(s.convert('RGB'), y0=330)
    subtitle(img, 4, t)
    return finish(img, t)

def s6(t):
    s = chat_base(); d = ImageDraw.Draw(s)
    y = 210
    bubble(s, 'भाई आज ऑफिस मत आना। बाहर बिल्कुल मत निकलना।', False, y, 1, 'राहुल', COLS[0])
    a = ease((t - S6_ASK) / 0.3)
    if a > 0: bubble(s, 'क्यों? क्या हुआ??', True, 430 + int(20 * (1 - a)), a)
    # members panel
    d.rounded_rectangle((20, 560, SW - 20, 1010), 30, fill=(42, 43, 58))
    d.text((44, 600), 'सदस्य', font=F(30, 'ExtraBold'), fill=(200, 200, 215), anchor='lm')
    for k, nm in enumerate(NAMES):
        yy_ = 660 + k * 60; off = t >= S6_OFF[k]
        d.ellipse((44, yy_ - 24, 92, yy_ + 24), fill=COLS[k] if not off else (90, 90, 100))
        d.text((68, yy_), nm[0], font=F(26, 'ExtraBold'), fill=(255, 255, 255), anchor='mm')
        d.ellipse((80, yy_ + 8, 98, yy_ + 26), fill=(70, 200, 90) if not off else (120, 120, 130), outline=(42, 43, 58), width=3)
        d.text((116, yy_), nm, font=F(32, 'Bold'), fill=(235, 235, 245) if not off else (130, 130, 145), anchor='lm')
        d.text((SW - 44, yy_), 'ऑनलाइन' if not off else 'ऑफ़लाइन', font=F(26, 'Medium'), fill=(70, 200, 90) if not off else (130, 130, 145), anchor='rm')
    if t > S6_OFF[-1] + 0.4:
        d.text((SW - 40, 545), 'Delivered · किसी ने नहीं देखा', font=F(24, 'Medium'), fill=(150, 150, 170), anchor='rm')
    img = phone(s.convert('RGB'), y0=330)
    subtitle(img, 5, t)
    dim = clamp((t - S6_OFF[-1]) / 1.0) * 0.25
    return finish(img, t, grade=(0.92 * (1 - dim), 1.0 * (1 - dim), 1.06 * (1 - dim)))

# ---------------- scene 7: TV news ----------------
CONT = {
 'na': [(0.05, 0.22), (0.18, 0.12), (0.30, 0.13), (0.33, 0.22), (0.27, 0.32), (0.22, 0.45), (0.17, 0.40), (0.10, 0.30)],
 'sa': [(0.25, 0.50), (0.32, 0.53), (0.36, 0.62), (0.31, 0.80), (0.28, 0.86), (0.26, 0.68)],
 'eu': [(0.45, 0.16), (0.55, 0.12), (0.58, 0.20), (0.53, 0.30), (0.46, 0.30)],
 'af': [(0.45, 0.34), (0.57, 0.33), (0.62, 0.45), (0.58, 0.70), (0.52, 0.72), (0.47, 0.50)],
 'as': [(0.57, 0.12), (0.80, 0.10), (0.92, 0.20), (0.86, 0.35), (0.78, 0.42), (0.70, 0.38), (0.62, 0.32), (0.58, 0.24)],
 'in': [(0.66, 0.35), (0.72, 0.35), (0.69, 0.48)],
 'au': [(0.80, 0.62), (0.90, 0.60), (0.92, 0.72), (0.83, 0.75)],
}
MW, MH = 860, 430
def map_dots():
    m = Image.new('L', (MW, MH), 0); d = ImageDraw.Draw(m)
    for poly in CONT.values(): d.polygon([(x * MW, y * MH) for x, y in poly], fill=255)
    a = np.asarray(m); pts = []
    r2 = random.Random(5)
    for y in range(8, MH, 16):
        for x in range(8, MW, 16):
            if a[y, x]:
                dist = math.hypot(x - 0.69 * MW, (y - 0.40 * MH) * 1.2) / MW
                pts.append((x, y, 0.4 + dist * 7.5 + r2.uniform(0, 0.9)))
    return pts
DOTS = map_dots()

def s7(t):
    img = Image.new('RGB', (W, H), (8, 9, 12)); d = ImageDraw.Draw(img, 'RGBA')
    tx0, ty0, tx1, ty1 = 60, 420, 1020, 1000
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).rectangle((tx0, ty0, tx1, ty1 + 500), fill=90)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(Image.new('RGB', (W, H), (150, 40, 40)), img, glow); d = ImageDraw.Draw(img, 'RGBA')
    # tv stand + body
    d.rectangle((tx0 - 22, ty0 - 22, tx1 + 22, ty1 + 22), fill=(16, 16, 18))
    d.rectangle((W / 2 - 140, ty1 + 22, W / 2 + 140, ty1 + 60), fill=(20, 20, 22))
    d.rectangle((60, ty1 + 60, W - 60, ty1 + 90), fill=(34, 26, 22))
    scr = Image.new('RGB', (tx1 - tx0, ty1 - ty0), (14, 18, 34)); sd = ImageDraw.Draw(scr)
    sw_, sh_ = scr.size
    if t < 0.7:
        n = (np.random.default_rng(int(t * 30)).random((sh_ // 4, sw_ // 4)) * 255).astype(np.uint8)
        scr = Image.fromarray(n).resize((sw_, sh_), Image.NEAREST).convert('RGB')
    else:
        tt = t - 0.7
        for (x, y, th) in DOTS:
            inf = tt * 1.0 > th
            c = (235, 50, 50) if inf else (60, 80, 110)
            r = 5 if inf else 4
            sd.ellipse((50 + x - r, 30 + y - r, 50 + x + r, 30 + y + r), fill=c)
        # pulse at Pune
        pr = 10 + (tt * 40) % 60
        sd.ellipse((50 + 0.69 * MW - pr, 30 + 0.40 * MH - pr, 50 + 0.69 * MW + pr, 30 + 0.40 * MH + pr), outline=(255, 90, 90), width=3)
        sd.rectangle((0, 0, 240, 56), fill=(200, 20, 30)); sd.text((120, 28), 'ब्रेकिंग न्यूज़', font=F(34, 'ExtraBold'), fill=(255, 255, 255), anchor='mm')
        sd.rectangle((sw_ - 130, 10, sw_ - 20, 50), fill=(220, 30, 30)); sd.text((sw_ - 75, 30), 'LIVE', font=F(26, 'ExtraBold'), fill=(255, 255, 255), anchor='mm')
        pct = int(min(99, 4 + tt * 16))
        sd.rounded_rectangle((20, 300, 230, 440), 14, fill=(10, 12, 24))
        sd.text((40, 352), f'{pct}%', font=F(72, 'ExtraBold'), fill=(255, 70, 70), anchor='lm')
        sd.text((42, 412), 'संक्रमित', font=F(28, 'Bold'), fill=(255, 200, 200), anchor='lm')
        sd.rectangle((0, sh_ - 120, sw_, sh_ - 50), fill=(250, 250, 250))
        sd.text((24, sh_ - 85), 'अनजानी बीमारी: एक रात में पूरी दुनिया संक्रमित', font=F(38, 'ExtraBold'), fill=(160, 10, 20), anchor='lm')
        sd.rectangle((0, sh_ - 50, sw_, sh_), fill=(170, 15, 25))
        tick = '   |   घर से बाहर न निकलें   |   सभी उड़ानें रद्द   |   अस्पतालों में जगह नहीं   |   सरकार ने इमरजेंसी घोषित की'
        ox = int(sw_ - (tt * 180) % (sw_ + 1500))
        sd.text((ox, sh_ - 25), tick, font=F(28, 'Bold'), fill=(255, 255, 255), anchor='lm')
        sd.text((24, sh_ - 140), 'भारत 24', font=F(26, 'ExtraBold'), fill=(255, 255, 255), anchor='lm')
        # scanlines
    sa = np.asarray(scr).astype(np.float32); sa[::3] *= 0.82
    img.paste(Image.fromarray(sa.astype(np.uint8)), (tx0, ty0))
    # silhouette of viewer (head & shoulders) bottom
    d = ImageDraw.Draw(img)
    d.ellipse((W / 2 - 120, 1150, W / 2 + 120, 1420), fill=(6, 6, 8)); d.rounded_rectangle((W / 2 - 330, 1380, W / 2 + 330, H + 100), 200, fill=(6, 6, 8))
    subtitle(img, 6, t)
    flick = 0.04 * math.sin(t * 37) * (t > 0.7)
    return finish(img, t, grade=(1.0 + flick, 0.95, 1.0), flash=0.15 * clamp(1 - t / 0.7) * (t < 0.7))

# ---------------- scene 8: figure ----------------
def s8(t):
    vo_end = DUR[7] - 2.6
    vpx, vpy, gy, road_half = STREET_GEO
    fs = 0.5; fx, fy = vpx + 30, gy(fs)
    p = clamp(t / vo_end)
    z = 1.0 + 1.5 * ease(p * 0.9) ** 1.4
    cx = STREET.width / 2 + (fx - STREET.width / 2) * ease(p); cy = STREET.height / 2 - 60 + (fy - 180 - STREET.height / 2 + 60) * ease(p)
    img, M, sc = street_view(t, z, cx, cy, int(t * 1.5) % 2 == 0)
    d = ImageDraw.Draw(img, 'RGBA')
    # figure
    k = fs * 300 * sc
    X, Y = M(fx, fy)
    d.ellipse((X - k * 0.5, Y - k * 0.08, X + k * 0.9, Y + k * 0.1), fill=(20, 20, 24, 120))  # shadow
    c = (20, 20, 24)
    d.polygon([(X - k * 0.13, Y), (X - k * 0.07, Y), (X - k * 0.02, Y - k * 0.5), (X - k * 0.14, Y - k * 0.5)], fill=c)  # left leg
    d.polygon([(X + k * 0.13, Y), (X + k * 0.07, Y), (X + k * 0.02, Y - k * 0.5), (X + k * 0.14, Y - k * 0.5)], fill=c)  # right leg
    d.polygon([(X - k * 0.15, Y - k * 0.48), (X + k * 0.15, Y - k * 0.48), (X + k * 0.19, Y - k * 0.9), (X - k * 0.19, Y - k * 0.9)], fill=c)  # torso
    d.polygon([(X - k * 0.19, Y - k * 0.9), (X - k * 0.26, Y - k * 0.62), (X - k * 0.24, Y - k * 0.40), (X - k * 0.19, Y - k * 0.41), (X - k * 0.19, Y - k * 0.62), (X - k * 0.14, Y - k * 0.86)], fill=c)
    d.polygon([(X + k * 0.19, Y - k * 0.9), (X + k * 0.25, Y - k * 0.6), (X + k * 0.27, Y - k * 0.36), (X + k * 0.22, Y - k * 0.36), (X + k * 0.19, Y - k * 0.6), (X + k * 0.14, Y - k * 0.86)], fill=c)
    hx, hy = X + k * 0.07, Y - k * 1.0  # tilted head
    d.line((X, Y - k * 0.9, hx, hy + k * 0.04), fill=c, width=max(2, int(k * 0.08)))
    d.ellipse((hx - k * 0.085, hy - k * 0.11, hx + k * 0.085, hy + k * 0.08), fill=c)
    if t > vo_end - 1.6:
        ea = int(255 * clamp((t - (vo_end - 1.6)) / 0.4))
        er = max(1.5, k * 0.022)
        for ex in (-0.035, 0.035):
            d.ellipse((hx + k * ex - er, hy - er, hx + k * ex + er, hy + er), fill=(255, 235, 235, ea))
    railing(img, alpha=int(255 * (1 - clamp(p * 3))))
    red = 0.15 + 0.6 * p
    if t < vo_end:
        out = Image.fromarray(finish(img, t, grade=(0.95, 0.92, 0.95), red=red))
        subtitle(out, 7, t)
        return np.asarray(out)
    # end card
    te = t - vo_end
    if te < 0.12:
        return finish(img, t, red=1.0, flash=0.6)
    card = Image.new('RGB', (W, H), (6, 6, 8)); cd = ImageDraw.Draw(card)
    a = clamp((te - 0.5) / 0.5)
    cd.text((W / 2, 860), 'Part 2?', font=F(150, 'ExtraBold'), fill=tuple(int(c * a) for c in (240, 240, 245)), anchor='mm')
    a2 = clamp((te - 1.1) / 0.5)
    cd.text((W / 2, 1020), 'आख़िरी इम्यून', font=F(70, 'ExtraBold'), fill=tuple(int(c * a2) for c in (230, 50, 50)), anchor='mm')
    cd.text((W / 2, 1110), 'Follow करो, अगला एपिसोड जल्द', font=F(40, 'Bold'), fill=tuple(int(c * a2) for c in (170, 170, 180)), anchor='mm')
    return finish(card, t, grade=(1, 1, 1))

SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]

def render(i, still=None):
    f = SCENES[i]
    if still is not None:
        Image.fromarray(f(still)).save(f'still_{i + 1}_{still:.1f}.jpg', quality=88); return
    n = int(round(DUR[i] * FPS)); tmp = f'scenes/s{i + 1}.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(f(k / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f'scenes/s{i + 1}.mp4')

if __name__ == '__main__':
    os.makedirs('scenes', exist_ok=True)
    if sys.argv[1] == 'still':
        render(int(sys.argv[2]) - 1, float(sys.argv[3]))
    elif sys.argv[1] == 'info':
        print('DUR', [round(x, 2) for x in DUR], 'START', [round(x, 2) for x in START], 'TOTAL', sum(DUR))
    else:
        render(int(sys.argv[1]) - 1)
