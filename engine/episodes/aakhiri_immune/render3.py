import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/claude/ep1')
import render as R
from render import F, W, H, FPS, ease, clamp, finish, wrap

DUR, CHUNKS, VO_OFF = R.DUR, R.CHUNKS, R.VO_OFF
vpx, vpy, gy, road_half = R.STREET_GEO

def subtitle(img, i, t, col=(255, 255, 255), label=None, y=1590):
    for a, b, p in CHUNKS[i]:
        if a <= t < b + 0.15:
            d = ImageDraw.Draw(img); f = F(62, 'ExtraBold')
            if label: d.text((W / 2, y - 80), label, font=F(38, 'Bold'), fill=(200, 200, 200), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))
            for k, l in enumerate(wrap(p.replace('...', '…'), f, 900)):
                d.text((W / 2, y + k * 80), l, font=f, fill=col, anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
            break

def scooter(d, X, Y, k, col=(70, 120, 150), light=False, fallen=False):
    if fallen:
        d.ellipse((X - k * 0.55, Y - k * 0.12, X - k * 0.25, Y + k * 0.06), fill=(20, 20, 22))
        d.polygon([(X - k * 0.5, Y - k * 0.05), (X + k * 0.5, Y - k * 0.12), (X + k * 0.55, Y + k * 0.05), (X - k * 0.45, Y + k * 0.08)], fill=col)
        d.ellipse((X + k * 0.3, Y - k * 0.1, X + k * 0.6, Y + k * 0.08), fill=(20, 20, 22))
        d.line((X - k * 0.2, Y - k * 0.08, X - k * 0.45, Y - k * 0.3), fill=(40, 40, 44), width=max(2, int(k * 0.04)))
        return
    d.ellipse((X - k * 0.45, Y - k * 0.2, X - k * 0.2, Y + k * 0.05), fill=(20, 20, 22)); d.ellipse((X + k * 0.2, Y - k * 0.2, X + k * 0.45, Y + k * 0.05), fill=(20, 20, 22))
    d.polygon([(X - k * 0.4, Y - k * 0.12), (X + k * 0.1, Y - k * 0.12), (X + k * 0.25, Y - k * 0.6), (X + k * 0.35, Y - k * 0.6), (X + k * 0.4, Y - k * 0.12), (X - k * 0.2, Y - k * 0.1)], fill=col)
    d.rounded_rectangle((X - k * 0.42, Y - k * 0.32, X - k * 0.02, Y - k * 0.18), int(k * 0.05), fill=(30, 30, 34))
    d.line((X + k * 0.28, Y - k * 0.62, X + k * 0.45, Y - k * 0.66), fill=(30, 30, 34), width=max(2, int(k * 0.04)))
    if light:
        d.ellipse((X + k * 0.33, Y - k * 0.58, X + k * 0.43, Y - k * 0.48), fill=(255, 245, 200))

# ---------------- S1: empty FC Road ----------------
def s1(t):
    p = t / DUR[0]
    img, M, sc = R.street_view(t, 1.05 + 0.08 * p, R.STREET.width / 2, R.STREET.height / 2 - 40, int(t * 1.5) % 2 == 0)
    d = ImageDraw.Draw(img, 'RGBA')
    X, Y = M(vpx + 40, gy(0.62)); scooter(d, X, Y, 0.62 * 330 * sc, fallen=True)
    # shop shutters signs on left near
    for k, (s_, txt) in enumerate([(0.85, 'चाय'), (0.6, 'मेडिकल'), (0.42, 'मोबाइल')]):
        x = vpx - road_half * s_ * 1.05; y = gy(s_) - 280 * s_
        X, Y = M(x, y); w_ = 170 * s_ * sc
        d.rectangle((X - w_ * 0.2, Y - w_ * 0.35, X + w_ * 0.9, Y), fill=(140, 40, 34, 230))
        d.text((X + w_ * 0.35, Y - w_ * 0.17), txt, font=F(max(14, int(46 * s_ * sc)), 'ExtraBold'), fill=(250, 230, 200), anchor='mm')
    d = ImageDraw.Draw(img)
    d.text((W / 2, 120), 'PART 3', font=F(44, 'ExtraBold'), fill=(235, 60, 60), anchor='mm')
    a = clamp((t - 0.8) / 0.5)
    if a > 0: d.text((W / 2, 205), 'आख़िरी इम्यून · खाली शहर', font=F(64, 'ExtraBold'), fill=tuple(int(c * a) for c in (240, 240, 245)), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))
    subtitle(img, 0, t)
    return finish(img, t, grade=(0.95, 0.96, 1.0))

# ---------------- S2: down the pipe, scooter starts ----------------
def build_wall():
    w, h = W, H * 3
    img = Image.new('RGB', (w, h), (56, 58, 66)); d = ImageDraw.Draw(img)
    for fl in range(6):
        y = fl * (h - 500) / 5
        d.rectangle((0, y, w, y + 24), fill=(44, 46, 52))
        for j in range(3):
            if j == 1: continue
            wx = 120 + j * 320
            d.rectangle((wx, y + 140, wx + 220, y + 460), fill=(30, 32, 38)); d.rectangle((wx + 10, y + 150, wx + 210, y + 450), fill=(46, 54, 66))
    d.rectangle((w / 2 - 22, 0, w / 2 + 22, h - 420), fill=(116, 108, 94))
    for y in range(0, h - 420, 360): d.rectangle((w / 2 - 34, y, w / 2 + 34, y + 26), fill=(96, 90, 78))
    d.rectangle((0, h - 420, w, h), fill=(42, 42, 46))
    for x in range(0, w, 260): d.line((x, h - 420, x + 120, h), fill=(230, 220, 150), width=8)
    return img
WALL = build_wall()
def s2(t):
    vd = DUR[1] - 0.55
    p = ease(clamp(t / (vd * 0.55)))
    y0 = int((WALL.height - H) * p)
    img = WALL.crop((0, y0, W, y0 + H)); d = ImageDraw.Draw(img, 'RGBA')
    # climbing hands on pipe until bottom
    if p < 0.98:
        hy = H * 0.35 + 30 * math.sin(t * 6)
        for s in (-1, 1):
            d.ellipse((W / 2 + s * 60 - 34, hy - 30 + s * 20, W / 2 + s * 60 + 34, hy + 30 + s * 20), fill=(176, 128, 98))
    else:
        light = t > vd - 0.7
        scooter(d, W / 2 - 40, H - 260, 640, light=light)
        if light:
            beam = Image.new('L', (W, H), 0); ImageDraw.Draw(beam).polygon([(W / 2 + 230, H - 600), (W + 300, H - 900), (W + 300, H - 200)], fill=110)
            img = Image.composite(Image.new('RGB', (W, H), (255, 240, 190)), img, beam.filter(ImageFilter.GaussianBlur(40))); d = ImageDraw.Draw(img)
        # key
        d.ellipse((W / 2 - 40 + 30, H - 560, W / 2 - 40 + 60, H - 530), fill=(210, 190, 120))
    subtitle(img, 1, t)
    return finish(img, t, grade=(0.85, 0.88, 0.98))

# ---------------- S3: riding, green signals, smoke ----------------
def s3(t):
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img, 'RGBA')
    hz = 760
    for y in range(hz):
        k = y / hz; d.line((0, y, W, y), fill=(int(150 + 60 * k), int(110 + 40 * k), int(90 + 20 * k)))
    # smoke columns
    for k, x in enumerate((230, 760, 900)):
        for j in range(16):
            yy_ = hz - j * 45; r = 30 + j * 9
            xx_ = x + 30 * math.sin(j * 0.5 + t * 0.8 + k) + j * 6
            d.ellipse((xx_ - r, yy_ - r, xx_ + r, yy_ + r), fill=(60, 56, 58, 70))
    # skyline
    rnd = random.Random(2); x = 0
    while x < W:
        bw = rnd.randint(60, 140); bh = rnd.randint(80, 260); d.rectangle((x, hz - bh, x + bw, hz), fill=(70, 62, 66)); x += bw
    d.rectangle((0, hz, W, H), fill=(84, 80, 78))
    # road
    d.polygon([(0, H), (W, H), (W / 2 + 30, hz), (W / 2 - 30, hz)], fill=(58, 58, 62))
    d.polygon([(0, H), (-300, H), (W / 2 - 30, hz)], fill=(84, 80, 78)); d.polygon([(W, H), (W + 300, H), (W / 2 + 30, hz)], fill=(84, 80, 78))
    speed = 2.2
    for k in range(12):
        s0 = ((k / 12 + t * speed * 0.25) % 1.0)
        s1_ = s0 ** 2.2; s2_ = min(1, (s0 + 0.035)) ** 2.2
        y1 = hz + (H - hz) * s1_; y2 = hz + (H - hz) * s2_
        w1 = 4 + 18 * s1_; w2 = 4 + 18 * s2_
        d.polygon([(W / 2 - w1, y1), (W / 2 + w1, y1), (W / 2 + w2, y2), (W / 2 - w2, y2)], fill=(230, 226, 210))
    # signal poles passing
    for k in range(3):
        s0 = ((k / 3 + t * 0.3) % 1.0) ** 2.0
        for side in (-1, 1):
            x = W / 2 + side * (40 + 900 * s0); y = hz + (H - hz) * s0
            hgt = 40 + 900 * s0
            d.rectangle((x - 3 - 8 * s0, y - hgt, x + 3 + 8 * s0, y), fill=(30, 30, 34))
            r = 6 + 34 * s0
            d.rounded_rectangle((x - r * 1.2, y - hgt - r * 3.4, x + r * 1.2, y - hgt), int(r * 0.4), fill=(20, 20, 22))
            d.ellipse((x - r * 2.5, y - hgt - r * 3.0, x + r * 2.5, y - hgt + r * 2.0), fill=(60, 255, 120, 40))
            d.ellipse((x - r * 0.8, y - hgt - r * 1.1, x + r * 0.8, y - hgt + r * 0.5), fill=(70, 255, 130))
    # handlebar foreground
    d.rounded_rectangle((60, H - 150, W - 60, H - 100), 25, fill=(26, 26, 30))
    d.rounded_rectangle((W / 2 - 170, H - 190, W / 2 + 170, H + 40), 40, fill=(70, 120, 150))
    d.rounded_rectangle((W / 2 - 100, H - 175, W / 2 + 100, H - 105), 14, fill=(20, 22, 26))
    d.text((W / 2, H - 140), f'{int(52 + 6 * math.sin(t))}', font=F(44, 'ExtraBold'), fill=(120, 230, 255), anchor='mm')
    sh = int(4 * math.sin(t * 40))
    img = img.transform(img.size, Image.AFFINE, (1, 0, 0, 0, 1, sh))
    subtitle(img, 2, t)
    return finish(img, t, grade=(1.02, 0.96, 0.92))

# ---------------- S4: Shaniwar Wada crowd ----------------
def build_fort():
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=(int(110 - 50 * k), int(100 - 50 * k), int(110 - 50 * k)))
    base = 1050
    d.rectangle((0, 520, W, base), fill=(92, 70, 58))
    for x in range(0, W, 80): d.polygon([(x, 520), (x + 40, 470), (x + 80, 520)], fill=(92, 70, 58))
    for bx in (170, W - 170):
        d.rectangle((bx - 130, 430, bx + 130, base), fill=(104, 80, 66)); d.ellipse((bx - 130, 390, bx + 130, 480), fill=(104, 80, 66))
        for x in range(bx - 130, bx + 130, 52): d.polygon([(x, 400), (x + 26, 360), (x + 52, 400)], fill=(104, 80, 66))
    d.rectangle((W / 2 - 170, 560, W / 2 + 170, base), fill=(70, 52, 42))
    d.pieslice((W / 2 - 170, 460, W / 2 + 170, 760), 180, 360, fill=(70, 52, 42))
    d.rectangle((W / 2 - 120, 640, W / 2 + 120, base), fill=(44, 30, 24)); d.pieslice((W / 2 - 120, 560, W / 2 + 120, 760), 180, 360, fill=(44, 30, 24))
    for y in range(680, base, 70):
        for x in range(int(W / 2 - 100), int(W / 2 + 100), 50): d.ellipse((x, y, x + 14, y + 14), fill=(150, 120, 80))
    d.rectangle((0, base, W, H), fill=(70, 66, 64))
    return img
FORT = build_fort()
CROWD = [(random.Random(i).uniform(40, W - 40), random.Random(i * 7).uniform(1080, 1420)) for i in range(48)]
def s4(t):
    vd = DUR[3] - 0.55
    turn_t = vd - 1.6
    img = FORT.copy(); d = ImageDraw.Draw(img, 'RGBA')
    for i, (x, y) in sorted(enumerate(CROWD), key=lambda e: e[1][1]):
        s = 0.5 + (y - 1080) / 340 * 0.6
        k = 120 * s; sway = 3 * math.sin(t * 1.1 + i)
        turned = t > turn_t + (i % 7) * 0.08
        X = x + sway; Y = y
        c = (24, 22, 24)
        d.rounded_rectangle((X - k * 0.2, Y - k * 0.95, X + k * 0.2, Y), int(k * 0.1), fill=c)
        tilt = k * 0.06 * (1 if i % 2 else -1)
        d.ellipse((X - k * 0.13 + tilt, Y - k * 1.2, X + k * 0.13 + tilt, Y - k * 0.92), fill=c)
        if turned:
            er = max(1.5, k * 0.025); a = int(255 * clamp((t - turn_t - (i % 7) * 0.08) / 0.3))
            d.ellipse((X - k * 0.05 + tilt - er, Y - k * 1.07 - er, X - k * 0.05 + tilt + er, Y - k * 1.07 + er), fill=(255, 230, 230, a))
            d.ellipse((X + k * 0.05 + tilt - er, Y - k * 1.07 - er, X + k * 0.05 + tilt + er, Y - k * 1.07 + er), fill=(255, 230, 230, a))
    z = 1 + 0.08 * clamp(t / vd) + (0.06 * ease(clamp((t - turn_t) / 0.4)))
    cw, ch = W / z, H / z
    img = img.crop((int(W / 2 - cw / 2), int(H / 2 - ch / 2 + 80 * (z - 1)), int(W / 2 + cw / 2), int(H / 2 + ch / 2 + 80 * (z - 1)))).resize((W, H), Image.BILINEAR)
    subtitle(img, 3, t)
    return finish(img, t, grade=(0.95, 0.92, 0.95), red=0.3 * clamp((t - turn_t) / 0.5))

# ---------------- S5: hiding behind wall ----------------
def s5(t):
    img = Image.new('RGB', (W, H), (40, 38, 42)); d = ImageDraw.Draw(img, 'RGBA')
    # background street (blurred crowd moving past)
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=(int(70 - 30 * k), int(66 - 30 * k), int(72 - 30 * k)))
    d.rectangle((0, 1150, W, H), fill=(52, 50, 50))
    bg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bg)
    for i in range(10):
        x = (i * 230 + t * 70) % (W + 400) - 200; y = 1180 + (i % 3) * 30; k = 260
        bd.rounded_rectangle((x - k * 0.2, y - k * 0.95, x + k * 0.2, y), 20, fill=(20, 18, 20, 230)); bd.ellipse((x - k * 0.13, y - k * 1.2, x + k * 0.13, y - k * 0.92), fill=(20, 18, 20, 230))
        bd.ellipse((x - 10, y - k * 1.08 - 3, x - 4, y - k * 1.08 + 3), fill=(255, 220, 220, 200)); bd.ellipse((x + 4, y - k * 1.08 - 3, x + 10, y - k * 1.08 + 3), fill=(255, 220, 220, 200))
    img.paste(bg.filter(ImageFilter.GaussianBlur(6)), (0, 0), bg.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(img, 'RGBA')
    # wall foreground left with bricks
    wx = 560 + 8 * math.sin(t * 0.7)
    d.rectangle((0, 0, wx, H), fill=(110, 70, 56))
    for row in range(0, H, 60):
        off = 0 if (row // 60) % 2 == 0 else 60
        for x in range(-off, int(wx), 120): d.rectangle((x + 3, row + 3, x + 117, row + 57), outline=(90, 56, 44), width=4)
    d.rectangle((wx - 20, 0, wx, H), fill=(80, 50, 40))
    # hand on wall edge, trembling
    hy = 900 + 6 * math.sin(t * 22)
    d.ellipse((wx - 70, hy - 40, wx + 30, hy + 40), fill=(176, 128, 98))
    for k in range(4): d.rounded_rectangle((wx - 10, hy - 40 + k * 22, wx + 40, hy - 24 + k * 22), 8, fill=(176, 128, 98))
    # clock-like seconds tick (top)
    sec = int(t)
    d.text((W - 70, 330), f'00:0{min(9, sec)}', font=F(56, 'ExtraBold'), fill=(255, 255, 255, 180), anchor='rm')
    subtitle(img, 4, t)
    breathe = 0.04 * math.sin(t * 5)
    return finish(img, t, grade=(0.9 + breathe, 0.86, 0.9))

# ---------------- S6: drone scanning ----------------
def s6(t):
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img, 'RGBA')
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=(int(40 + 30 * k), int(40 + 20 * k), int(52 + 10 * k)))
    # rooftops/edges (looking up between buildings)
    d.polygon([(0, 0), (260, 0), (360, H), (0, H)], fill=(26, 26, 30)); d.polygon([(W, 0), (W - 260, 0), (W - 360, H), (W, H)], fill=(26, 26, 30))
    for y in range(80, H, 160):
        d.rectangle((40, y, 200 + y * 0.06, y + 70), fill=(36, 36, 42)); d.rectangle((W - 200 - y * 0.06, y, W - 40, y + 70), fill=(36, 36, 42))
    dx = W / 2 + 220 * math.sin(t * 0.6); dy = 520 + 40 * math.sin(t * 1.1)
    # red scan cone
    sweep = math.sin(t * 1.4) * 0.5
    cone = Image.new('L', (W, H), 0); ImageDraw.Draw(cone).polygon([(dx, dy), (dx - 380 + sweep * 600, H), (dx + 380 + sweep * 600, H)], fill=120)
    img = Image.composite(Image.new('RGB', (W, H), (255, 40, 40)), img, cone.filter(ImageFilter.GaussianBlur(30))); d = ImageDraw.Draw(img, 'RGBA')
    # drone body
    d.rounded_rectangle((dx - 90, dy - 30, dx + 90, dy + 30), 20, fill=(16, 16, 18))
    for sx in (-1, 1):
        d.line((dx + sx * 60, dy - 10, dx + sx * 180, dy - 60), fill=(16, 16, 18), width=12)
        rot = abs(math.sin(t * 40 + sx)) * 90 + 20
        d.ellipse((dx + sx * 180 - rot, dy - 70, dx + sx * 180 + rot, dy - 50), fill=(60, 60, 64, 160))
    d.ellipse((dx - 16, dy + 4, dx + 16, dy + 36), fill=(255, 40, 40) if int(t * 4) % 2 == 0 else (120, 20, 20))
    # HUD text
    d.text((W / 2, 330), 'SCANNING…', font=F(40, 'ExtraBold'), fill=(255, 90, 90, 200 if int(t * 2) % 2 == 0 else 90), anchor='mm')
    subtitle(img, 5, t)
    return finish(img, t, grade=(0.95, 0.9, 0.95))

# ---------------- S7: radio ----------------
def s7(t):
    img = Image.new('RGB', (W, H), (14, 14, 18)); d = ImageDraw.Draw(img, 'RGBA')
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse((150, 400, 930, 1300), fill=110)
    img = Image.composite(Image.new('RGB', (W, H), (60, 120, 130)), img, glow.filter(ImageFilter.GaussianBlur(120))); d = ImageDraw.Draw(img, 'RGBA')
    x0, y0, x1, y1 = 230, 480, 850, 1240
    d.rounded_rectangle((x0, y0, x1, y1), 60, fill=(48, 44, 40), outline=(90, 84, 76), width=6)
    d.line((x1 - 90, y0, x1 - 30, 260), fill=(160, 160, 165), width=10); d.ellipse((x1 - 44, 246, x1 - 16, 274), fill=(180, 180, 185))
    # speaker grille
    for yy_ in range(y0 + 60, y0 + 360, 26):
        for xx_ in range(x0 + 60, x1 - 60, 26): d.ellipse((xx_, yy_, xx_ + 12, yy_ + 12), fill=(28, 26, 24))
    # frequency window
    d.rounded_rectangle((x0 + 50, y0 + 400, x1 - 50, y0 + 520), 18, fill=(230, 200, 120))
    for k in range(20):
        xx_ = x0 + 70 + k * 24; d.line((xx_, y0 + 410, xx_, y0 + (450 if k % 5 == 0 else 430)), fill=(60, 50, 30), width=3)
    nx = x0 + 120 + 300 * clamp(t / 1.2) + 4 * math.sin(t * 9)
    d.line((nx, y0 + 405, nx, y0 + 515), fill=(200, 30, 30), width=5)
    d.text((W / 2, y0 + 485), '104.2 MHz', font=F(36, 'ExtraBold'), fill=(60, 50, 30), anchor='mm')
    # waveform from mix envelope (fake)
    for k in range(40):
        xx_ = x0 + 70 + k * 12
        amp = (12 + 50 * abs(math.sin(k * 0.7 + t * 9) * math.sin(t * 3 + k * 0.2))) * (t > 0.6)
        d.line((xx_, y0 + 620 - amp, xx_, y0 + 620 + amp), fill=(120, 230, 240), width=6)
    d.ellipse((x0 + 70, y1 - 110, x0 + 140, y1 - 40), fill=(30, 28, 26)); d.ellipse((x1 - 140, y1 - 110, x1 - 70, y1 - 40), fill=(30, 28, 26))
    sh = int(3 * math.sin(t * 50)) if t < 0.6 else 0
    img = img.transform(img.size, Image.AFFINE, (1, 0, sh, 0, 1, 0))
    subtitle(img, 6, t, col=(140, 235, 245), label='रेडियो पर एक लड़की की आवाज़')
    return finish(img, t, grade=(0.95, 1.0, 1.02))

# ---------------- S8: ride to the dam ----------------
def s8(t):
    vo_end = DUR[7] - 2.6
    if t >= vo_end:
        te = t - vo_end
        card = Image.new('RGB', (W, H), (6, 6, 8)); cd = ImageDraw.Draw(card)
        a = clamp((te - 0.4) / 0.5); a2 = clamp((te - 1.0) / 0.5)
        cd.text((W / 2, 860), 'Part 4?', font=F(150, 'ExtraBold'), fill=tuple(int(c * a) for c in (240, 240, 245)), anchor='mm')
        cd.text((W / 2, 1020), 'आख़िरी इम्यून', font=F(70, 'ExtraBold'), fill=tuple(int(c * a2) for c in (230, 50, 50)), anchor='mm')
        cd.text((W / 2, 1110), 'Follow करो, अगला एपिसोड परसों', font=F(40, 'Bold'), fill=tuple(int(c * a2) for c in (170, 170, 180)), anchor='mm')
        return finish(card, t, grade=(1, 1, 1))
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img, 'RGBA')
    hz = 980
    for y in range(hz):
        k = y / hz; d.line((0, y, W, y), fill=(int(70 + 170 * k), int(60 + 90 * k), int(100 - 20 * k)))
    d.ellipse((W / 2 - 110, hz - 170, W / 2 + 110, hz + 50), fill=(255, 190, 110))
    # hills + dam wall
    d.polygon([(0, hz), (0, 760), (260, 700), (520, 820), (760, 720), (W, 780), (W, hz)], fill=(60, 50, 70))
    d.polygon([(140, hz), (200, 860), (880, 860), (940, hz)], fill=(110, 104, 110))
    for x in range(220, 880, 60): d.rectangle((x, 870, x + 30, 960), fill=(90, 84, 92))
    # water glint
    d.rectangle((0, hz, W, hz + 60), fill=(80, 70, 100))
    # road
    d.polygon([(W / 2 - 20, hz + 60), (W / 2 + 20, hz + 60), (W + 100, H), (-100, H)], fill=(46, 42, 48))
    d.rectangle((0, hz + 60, W / 2 - 20, H), fill=(36, 44, 34)); d.polygon([(W / 2 + 20, hz + 60), (W, hz + 60), (W, H), (W + 100, H)], fill=(36, 44, 34))
    d.polygon([(W / 2 + 20, hz + 60), (W, hz + 60), (W, H), (W + 100, H)], fill=(36, 44, 34))
    # scooter riding away
    p = clamp(t / vo_end)
    s = 1.0 - 0.75 * ease(p)
    sy = hz + 60 + (H - hz - 200) * s; sx = W / 2 + 10 * math.sin(t * 2)
    k = 420 * s
    d.rounded_rectangle((sx - k * 0.22, sy - k * 0.6, sx + k * 0.22, sy), int(k * 0.08), fill=(30, 30, 34))
    d.ellipse((sx - k * 0.12, sy - k * 0.85, sx + k * 0.12, sy - k * 0.6), fill=(30, 30, 34))
    d.ellipse((sx - k * 0.08, sy - k * 0.12, sx + k * 0.08, sy - k * 0.02), fill=(255, 60, 60))
    tl = Image.new('L', (W, H), 0); ImageDraw.Draw(tl).ellipse((sx - k * 0.3, sy - k * 0.3, sx + k * 0.3, sy + k * 0.15), fill=90)
    img = Image.composite(Image.new('RGB', (W, H), (255, 70, 60)), img, tl.filter(ImageFilter.GaussianBlur(25)))
    subtitle(img, 7, t)
    return finish(img, t, grade=(1.02, 0.97, 0.95))

SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]

def render(i, still=None):
    f = SCENES[i]
    if still is not None:
        Image.fromarray(f(still)).save(f'still_{i + 1}_{still:.1f}.jpg', quality=88); return
    n = int(round(DUR[i] * FPS)); tmp = f'scenes/s{i + 1}.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(f(k / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f'scenes/s{i + 1}.mp4')

if __name__ == '__main__':
    os.makedirs('scenes', exist_ok=True)
    if sys.argv[1] == 'still': render(int(sys.argv[2]) - 1, float(sys.argv[3]))
    elif sys.argv[1] == 'info': print([round(x, 2) for x in DUR], sum(DUR))
    else: render(int(sys.argv[1]) - 1)
