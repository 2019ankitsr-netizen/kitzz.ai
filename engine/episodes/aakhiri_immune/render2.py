import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/claude/ep1')
import render as R
from render import F, W, H, FPS, ease, clamp, finish, phone, SW, SH, wrap

DUR, CHUNKS, VO_OFF = R.DUR, R.CHUNKS, R.VO_OFF
KNOCKS_S1 = [0.15, 0.45, 0.75, 2.6, 2.85]
KNOCKS_S7 = [0.1, 0.35, 0.6]

def subtitle(img, i, t, col=(255, 255, 255), label=None, y=1590):
    for a, b, p in CHUNKS[i]:
        if a <= t < b + 0.15:
            d = ImageDraw.Draw(img); f = F(62, 'ExtraBold')
            if label:
                d.text((W / 2, y - 80), label, font=F(38, 'Bold'), fill=(200, 200, 200), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))
            for k, l in enumerate(wrap(p.replace('...', '…'), f, 900)):
                d.text((W / 2, y + k * 80), l, font=f, fill=col, anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
            break

def knock_shake(t, knocks, amp=14):
    s = 0.0
    for k in knocks:
        if 0 <= t - k < 0.18: s += amp * math.exp(-(t - k) * 18) * math.sin((t - k) * 120)
    return s

# ---------------- door (S1, S7) ----------------
def build_door():
    img = Image.new('RGB', (W, H), (16, 15, 18)); d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=(int(30 - 12 * k), int(28 - 12 * k), int(32 - 12 * k)))
    # floor
    d.rectangle((0, 1560, W, H), fill=(22, 18, 16))
    return img
DOOR_BG = build_door()

def door(t, knocks, shadows=False, light=1.0):
    img = DOOR_BG.copy(); d = ImageDraw.Draw(img, 'RGBA')
    sx = knock_shake(t, knocks)
    x0, y0, x1, y1 = 290 + sx, 330, 790 + sx, 1560
    # light leak under door
    lk = Image.new('L', (W, H), 0); ImageDraw.Draw(lk).rectangle((x0 - 40, 1540, x1 + 40, 1640), fill=int(200 * light))
    img = Image.composite(Image.new('RGB', (W, H), (255, 226, 170)), img, lk.filter(ImageFilter.GaussianBlur(30))); d = ImageDraw.Draw(img, 'RGBA')
    d.rectangle((x0 - 30, y0 - 30, x1 + 30, y1), fill=(40, 30, 24))
    d.rectangle((x0, y0, x1, y1), fill=(74, 52, 38))
    for (a, b, c, e) in [(x0 + 50, y0 + 60, x1 - 50, y0 + 520), (x0 + 50, y0 + 600, x1 - 50, y1 - 80)]:
        d.rectangle((a, b, c, e), outline=(56, 38, 28), width=10)
    d.rectangle((x0, y1 - 6, x1, y1), fill=(255, 220, 160, int(200 * light)))
    # peephole
    d.ellipse((x0 + 230, y0 + 340, x0 + 270, y0 + 380), fill=(30, 24, 20)); d.ellipse((x0 + 240, y0 + 350, x0 + 260, y0 + 370), fill=(255, 230, 190, int(220 * light)))
    # handle + chain
    d.rounded_rectangle((x1 - 110, 960, x1 - 40, 990), 12, fill=(180, 160, 110)); d.ellipse((x1 - 70, 940, x1 - 30, 1010), fill=(150, 130, 90))
    for k in range(7): d.ellipse((x1 - 150 + k * 14 + sx * 0.5, 880 + 6 * math.sin(k + t * 8 * (abs(sx) > 1)), x1 - 136 + k * 14 + sx * 0.5, 896 + 6 * math.sin(k + t * 8 * (abs(sx) > 1))), outline=(170, 160, 140), width=3)
    if shadows:
        for k, ph in enumerate((0, 1.7)):
            cx = x0 + 160 + k * 200 + 18 * math.sin(t * 2 + ph)
            d.rectangle((cx - 40, 1556, cx + 40, 1600), fill=(10, 10, 12, 230))
    return img

def s1(t):
    img = door(t, KNOCKS_S1)
    d = ImageDraw.Draw(img)
    d.text((W / 2, 120), 'PART 2', font=F(44, 'ExtraBold'), fill=(235, 60, 60), anchor='mm')
    a = clamp((t - 1.2) / 0.5)
    if a > 0:
        d.text((W / 2, 205), 'आख़िरी इम्यून · दस्तक', font=F(64, 'ExtraBold'), fill=tuple(int(c * a) for c in (230, 230, 235)), anchor='mm')
    subtitle(img, 0, t)
    fl = max([clamp(1 - abs(t - k) / 0.08) for k in KNOCKS_S1])
    return finish(img, t, grade=(1.0, 0.95, 0.92), flash=0.08 * fl)

# ---------------- S2: emergency alert ----------------
def alert_screen(t):
    s = R.MAP.copy().convert('RGBA'); d = ImageDraw.Draw(s)
    d.rectangle((0, 0, SW, SH), fill=(0, 0, 0, 150))
    p = ease((t - 0.3) / 0.4)
    if p > 0:
        a = int(255 * p)
        blink = (int(t * 2.5) % 2 == 0)
        y0 = 230 + int(40 * (1 - p))
        d.rounded_rectangle((26, y0, SW - 26, y0 + 640), 30, fill=(250, 246, 240, a))
        d.rounded_rectangle((26, y0, SW - 26, y0 + 110), 30, fill=((220, 40, 40) if blink else (240, 140, 30)) + (a,))
        d.rectangle((26, y0 + 70, SW - 26, y0 + 110), fill=((220, 40, 40) if blink else (240, 140, 30)) + (a,))
        d.text((SW / 2, y0 + 58), '⚠  आपातकालीन अलर्ट'.replace('⚠  ', ''), font=F(42, 'ExtraBold'), fill=(255, 255, 255, a), anchor='mm')
        lines = ['राष्ट्रीय स्वास्थ्य आपातकाल', '', 'जो नागरिक संक्रमित नहीं हैं,', 'तुरंत नज़दीकी मेडिकल', 'कैंप में रिपोर्ट करें।', '', 'घर से बाहर अकेले न निकलें।']
        for k, l in enumerate(lines):
            d.text((60, y0 + 160 + k * 52), l, font=F(36 if k else 38, 'ExtraBold' if k == 0 else 'Bold'), fill=(30, 30, 34, a) if k else (190, 20, 30, a), anchor='lm')
        d.rounded_rectangle((60, y0 + 560, SW - 60, y0 + 620), 20, fill=(30, 30, 34, a))
        d.text((SW / 2, y0 + 590), 'ठीक है', font=F(32, 'Bold'), fill=(255, 255, 255, a), anchor='mm')
    return s.convert('RGB')

def s2(t):
    sh = (int(10 * math.sin(t * 70)), 0) if 0.3 < t < 0.9 else (0, 0)
    img = phone(alert_screen(t), y0=330, shake=sh)
    # red pulse glow
    subtitle(img, 1, t)
    pulse = 0.5 + 0.5 * math.sin(t * 2.5 * 2 * math.pi / 2)
    return finish(img, t, grade=(1.0 + 0.08 * pulse, 0.95, 0.95))

# ---------------- S3: leaked video ----------------
def camp_frame(t):
    s = Image.new('RGB', (SW, 760), (20, 26, 24)); d = ImageDraw.Draw(s)
    # tent interior
    d.polygon([(0, 0), (SW, 0), (SW, 300), (0, 300)], fill=(40, 52, 48))
    d.polygon([(0, 0), (SW / 2, 120), (SW, 0)], fill=(48, 62, 56))
    d.rectangle((0, 300, SW, 760), fill=(30, 36, 34))
    # bed + body silhouette
    d.rectangle((80, 430, 420, 470), fill=(170, 180, 176)); d.rectangle((90, 470, 110, 560), fill=(90, 96, 94)); d.rectangle((390, 470, 410, 560), fill=(90, 96, 94))
    d.ellipse((100, 390, 160, 440), fill=(30, 34, 34)); d.rounded_rectangle((150, 400, 400, 440), 18, fill=(150, 160, 156))
    # IV stand
    d.line((60, 220, 60, 560), fill=(140, 140, 140), width=6); d.rounded_rectangle((40, 220, 80, 290), 10, fill=(170, 210, 220))
    d.line((60, 290, 140, 420), fill=(170, 210, 220), width=3)
    # hazmat figure
    d.ellipse((440, 250, 520, 330), fill=(220, 224, 214)); d.rounded_rectangle((425, 320, 535, 560), 30, fill=(220, 224, 214)); d.rectangle((455, 270, 505, 300), fill=(40, 50, 60))
    # monitor
    d.rectangle((300, 120, 520, 250), fill=(10, 14, 12), outline=(90, 90, 90), width=4)
    flat = t > 4.2
    pts = []
    for x in range(310, 510, 3):
        ph = (x - 310) / 200 * 3 + t * 1.6
        y = 185
        if not flat:
            f = ph % 1.0
            if 0.45 < f < 0.5: y -= 45
            elif 0.5 <= f < 0.55: y += 25
        pts.append((x, y))
    d.line(pts, fill=(255, 70, 70) if flat else (80, 255, 120), width=3)
    d.text((510, 235), '0' if flat else str(70 + int(10 * math.sin(t))), font=F(26, 'Bold'), fill=(255, 70, 70) if flat else (80, 255, 120), anchor='rm')
    # noise, scanlines
    a = np.asarray(s).astype(np.float32)
    a = a * 0.9 + np.random.default_rng(int(t * 30)).normal(0, 14, a.shape[:2])[..., None]
    a[::4] *= 0.75
    if flat: a[..., 0] *= 1.25
    s = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(s)
    d.text((24, 30), '● REC', font=F(30, 'ExtraBold'), fill=(255, 50, 50) if int(t * 2) % 2 == 0 else (120, 30, 30), anchor='lm')
    d.text((SW - 24, 30), 'CAMP-07  03:12:44', font=F(24, 'Bold'), fill=(220, 220, 220), anchor='rm')
    return s

def s3(t):
    sc = Image.new('RGB', (SW, SH), (8, 8, 10)); d = ImageDraw.Draw(sc)
    d.rectangle((0, 0, SW, 150), fill=(16, 16, 20))
    d.text((40, 95), 'फ़ॉरवर्ड किया गया वीडियो', font=F(34, 'Bold'), fill=(220, 220, 225), anchor='lm')
    d.rounded_rectangle((SW - 170, 70, SW - 30, 120), 14, fill=(200, 30, 30)); d.text((SW - 100, 95), 'LEAKED', font=F(28, 'ExtraBold'), fill=(255, 255, 255), anchor='mm')
    sc.paste(camp_frame(t), (0, 230))
    # progress bar
    d.rectangle((30, 1030, SW - 30, 1036), fill=(70, 70, 70)); d.rectangle((30, 1030, 30 + (SW - 60) * clamp(t / DUR[2]), 1036), fill=(230, 50, 50))
    img = phone(sc, y0=330)
    subtitle(img, 2, t)
    glitch = 0.3 if (4.2 < t < 4.35) else 0
    return finish(img, t, grade=(0.95, 1.0, 0.98), flash=glitch)

# ---------------- S4: subject list ----------------
def s4(t):
    img = Image.new('RGB', (W, H), (10, 12, 16)); d = ImageDraw.Draw(img)
    d.rectangle((90, 300, 990, 1440), fill=(232, 228, 216))
    d.rectangle((90, 300, 990, 420), fill=(40, 46, 58))
    d.text((130, 360), 'गोपनीय · IMMUNE SUBJECTS', font=F(48, 'ExtraBold'), fill=(240, 240, 240), anchor='lm')
    rows = [('#09', 'मुंबई'), ('#10', 'दिल्ली'), ('#11', 'नागपुर'), ('#12', 'इंदौर'), ('#13', 'नाशिक'), ('#14', 'पुणे')]
    for k, (n, city) in enumerate(rows):
        ts = 0.4 + k * 0.75
        if t < ts: break
        y = 500 + k * 130
        d.text((140, y), f'Subject {n}', font=F(50, 'Bold'), fill=(30, 30, 36), anchor='lm')
        d.text((480, y), city, font=F(50, 'Bold'), fill=(30, 30, 36), anchor='lm')
        if t > ts + 0.35:
            d.text((940, y), 'मृत', font=F(54, 'ExtraBold'), fill=(190, 20, 30), anchor='rm')
        d.line((130, y + 55, 950, y + 55), fill=(190, 186, 176), width=2)
    if t > 0.4 + 6 * 0.75 + 0.2:
        y = 500 + 6 * 130
        a = clamp((t - 5.1) / 0.4)
        d.text((140, y), 'Subject #15', font=F(50, 'Bold'), fill=(30, 30, 36), anchor='lm')
        d.text((480, y), 'पुणे', font=F(50, 'Bold'), fill=(30, 30, 36), anchor='lm')
        if int(t * 3) % 2 == 0: d.text((940, y), 'तलाश जारी', font=F(48, 'ExtraBold'), fill=(220, 120, 20), anchor='rm')
    subtitle(img, 3, t)
    z = 1 + 0.05 * t / DUR[3]
    return finish(img, t, grade=(0.95, 0.97, 1.02))

# ---------------- S5: wrist / veins ----------------
def s5(t):
    img = Image.new('RGB', (W, H), (12, 12, 16)); d = ImageDraw.Draw(img, 'RGBA')
    # arm from bottom-left
    p = t / DUR[4]
    sk = (176, 128, 98); sk2 = (160, 114, 86)
    yb = 1000 + 6 * math.sin(t * 1.2)
    # forearm from left edge, palm up, wrist at x~690
    d.polygon([(-40, yb - 150), (690, yb - 105), (700, yb + 105), (-40, yb + 170)], fill=sk)
    d.polygon([(-40, yb + 110), (700, yb + 70), (700, yb + 105), (-40, yb + 170)], fill=sk2)
    # palm
    d.ellipse((640, yb - 135, 900, yb + 130), fill=sk)
    for k, (dy, ln) in enumerate([(-95, 170), (-35, 200), (25, 190), (80, 150)]):
        d.rounded_rectangle((850, yb + dy - 24, 850 + ln, yb + dy + 24), 24, fill=sk)
    d.rounded_rectangle((700, yb - 175, 830, yb - 125), 25, fill=sk)  # thumb
    d.arc((560, yb - 60, 760, yb + 60), 70, 110, fill=sk2, width=6)  # wrist crease
    glow = 0.5 + 0.5 * math.sin(t * 3)
    veins = [[(-40, yb - 20), (250, yb - 30), (480, yb - 5), (690, yb - 25)], [(-40, yb + 60), (220, yb + 40), (430, yb + 50), (690, yb + 30)], [(250, yb - 30), (360, yb + 15), (430, yb + 50)]]
    for v in veins:
        d.line(v, fill=(60, 140, 255, int(80 + 120 * glow)), width=20, joint='curve')
        d.line(v, fill=(150, 215, 255, int(150 + 100 * glow)), width=6, joint='curve')
    # DNA helix faint
    for k in range(40):
        y = 300 + k * 13; ph = k * 0.45 + t * 2
        x1 = W / 2 + 160 * math.sin(ph); x2 = W / 2 - 160 * math.sin(ph)
        al = int(70 * clamp(t / 1.5))
        d.ellipse((x1 - 6, y - 6, x1 + 6, y + 6), fill=(120, 200, 255, al)); d.ellipse((x2 - 6, y - 6, x2 + 6, y + 6), fill=(255, 110, 110, al))
        if k % 2 == 0: d.line((x1, y, x2, y), fill=(200, 200, 220, al // 2), width=2)
    subtitle(img, 4, t)
    redp = clamp((t - (DUR[4] * 0.62)) / 1.5) * 0.5
    return finish(img, t, grade=(0.95, 0.98, 1.05), red=redp)

# ---------------- S6: vans arriving (street view, darker) ----------------
def s6(t):
    p = t / DUR[5]
    z = 1.0 + 0.10 * p
    vpx, vpy, gy, road_half = R.STREET_GEO
    img, M, sc = R.street_view(t, z, R.STREET.width / 2, R.STREET.height / 2 - 40, False)
    d = ImageDraw.Draw(img, 'RGBA')
    # vans: drive in from far to near, stop
    for k in range(2):
        s_ = 0.12 + (0.55 - 0.12) * ease(clamp((t - 0.2 - k * 0.6) / 2.4)) - k * 0.12
        if s_ <= 0.1: continue
        x = vpx + (-1 if k == 0 else 1) * road_half * s_ * 0.45; y = gy(s_)
        X, Y = M(x, y); k_ = s_ * 520 * sc
        d.rounded_rectangle((X - k_ * 0.5, Y - k_ * 0.62, X + k_ * 0.5, Y), int(k_ * 0.08), fill=(14, 14, 16))
        d.rectangle((X - k_ * 0.42, Y - k_ * 0.55, X + k_ * 0.42, Y - k_ * 0.38), fill=(40, 48, 60))
        d.ellipse((X - k_ * 0.45, Y - k_ * 0.2, X - k_ * 0.33, Y - k_ * 0.1), fill=(255, 250, 220)); d.ellipse((X + k_ * 0.33, Y - k_ * 0.2, X + k_ * 0.45, Y - k_ * 0.1), fill=(255, 250, 220))
        # beam lights
        if int(t * 4 + k) % 2 == 0: d.rectangle((X - k_ * 0.2, Y - k_ * 0.7, X + k_ * 0.2, Y - k_ * 0.62), fill=(255, 60, 60))
        else: d.rectangle((X - k_ * 0.2, Y - k_ * 0.7, X + k_ * 0.2, Y - k_ * 0.62), fill=(70, 120, 255))
    # hazmat figures walking toward camera (building)
    if t > 3.0:
        for j in range(4):
            s_ = 0.42 + 0.2 * clamp((t - 3.0 - j * 0.15) / (DUR[5] - 3.0)) + j * 0.015
            x = vpx + (j - 1.5) * road_half * 0.18 * s_; y = gy(s_)
            X, Y = M(x, y); k_ = s_ * 240 * sc
            bob = 3 * math.sin(t * 9 + j)
            d.rounded_rectangle((X - k_ * 0.16, Y - k_ * 0.85 + bob, X + k_ * 0.16, Y), int(k_ * 0.08), fill=(225, 228, 220))
            d.ellipse((X - k_ * 0.12, Y - k_ * 1.08 + bob, X + k_ * 0.12, Y - k_ * 0.84 + bob), fill=(225, 228, 220))
            d.rectangle((X - k_ * 0.08, Y - k_ * 1.0 + bob, X + k_ * 0.08, Y - k_ * 0.93 + bob), fill=(30, 40, 50))
    subtitle(img, 5, t)
    return finish(img, t, grade=(0.62, 0.66, 0.80))

# ---------------- S7: knocking + voice ----------------
def s7(t):
    img = door(t, KNOCKS_S7, shadows=True)
    subtitle(img, 6, t, col=(255, 214, 90), label='दरवाज़े के बाहर से')
    fl = max([clamp(1 - abs(t - k) / 0.08) for k in KNOCKS_S7])
    return finish(img, t, grade=(0.98, 0.95, 0.95), flash=0.08 * fl)

# ---------------- S8: back window, the drop ----------------
def build_drop():
    w, h = int(W * 1.6), int(H * 1.6)
    img = Image.new('RGB', (w, h), (20, 22, 28)); d = ImageDraw.Draw(img)
    # looking down a building wall: perspective converging to ground at center-bottom
    gx, gy_ = w * 0.5, h * 0.82
    # wall
    d.polygon([(0, 0), (w * 0.62, 0), (gx + w * 0.06, gy_), (0, gy_ + 80)], fill=(58, 60, 68))
    for k in range(6):  # floors lines
        s = (k + 1) / 7
        y = s ** 1.6 * gy_
        x2 = w * 0.62 + (gx + w * 0.06 - w * 0.62) * (y / gy_)
        d.line((0, y, x2, y), fill=(44, 46, 52), width=int(16 * (1 - s) + 4))
        # windows
        for j in range(3):
            wx = 60 + j * (x2 - 120) / 3; ww = (x2 - 120) / 3 * 0.55
            d.rectangle((wx, y + 20 * (1 - s), wx + ww, y + (110 * (1 - s) + 20)), fill=(34, 36, 42))
    # pipe
    d.polygon([(w * 0.5, 0), (w * 0.54, 0), (gx + 6, gy_), (gx - 6, gy_)], fill=(110, 104, 92))
    # ground
    d.rectangle((0, gy_, w, h), fill=(40, 40, 44))
    pool = Image.new('L', (w, h), 0); ImageDraw.Draw(pool).ellipse((gx - 700, gy_ - 120, gx + 700, gy_ + 380), fill=170)
    img = Image.composite(Image.new('RGB', (w, h), (210, 160, 90)), img, pool.filter(ImageFilter.GaussianBlur(80)))
    d = ImageDraw.Draw(img); d.line((gx - 900, gy_ + 30, gx + 900, gy_ + 30), fill=(90, 80, 60), width=6)
    return img, (gx, gy_)
DROP, DROP_G = build_drop()

def s8(t):
    vo_end = DUR[7] - 2.6
    if t >= vo_end:
        te = t - vo_end
        if te < 0.12: return finish(Image.new('RGB', (W, H), (40, 0, 0)), t, flash=0.5)
        card = Image.new('RGB', (W, H), (6, 6, 8)); cd = ImageDraw.Draw(card)
        a = clamp((te - 0.5) / 0.5); a2 = clamp((te - 1.1) / 0.5)
        cd.text((W / 2, 860), 'Part 3?', font=F(150, 'ExtraBold'), fill=tuple(int(c * a) for c in (240, 240, 245)), anchor='mm')
        cd.text((W / 2, 1020), 'आख़िरी इम्यून', font=F(70, 'ExtraBold'), fill=tuple(int(c * a2) for c in (230, 50, 50)), anchor='mm')
        cd.text((W / 2, 1110), 'Follow करो, अगला एपिसोड परसों', font=F(40, 'Bold'), fill=tuple(int(c * a2) for c in (170, 170, 180)), anchor='mm')
        return finish(card, t, grade=(1, 1, 1))
    p = clamp(t / vo_end)
    z = 1.0 + 0.5 * ease(p)
    gx, gy_ = DROP_G
    cw, ch = W * 1.6 / z, H * 1.6 / z
    cx = DROP.width / 2 + (gx - DROP.width / 2) * ease(p) * 0.6; cy = DROP.height / 2 + (gy_ - 300 - DROP.height / 2) * ease(p) * 0.7
    img = DROP.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(img, 'RGBA')
    def M(x, y): return ((x - (cx - cw / 2)) * W / cw, (y - (cy - ch / 2)) * H / ch)
    sc = W / cw
    # crowd of infected (top-down-ish blobs with heads), shuffling, looking up
    rnd = random.Random(9)
    for j in range(26):
        bx = gx + rnd.uniform(-560, 560); by = gy_ + rnd.uniform(40, 300)
        bx += 8 * math.sin(t * 1.3 + j)
        X, Y = M(bx, by); r = 34 * sc
        d.ellipse((X - r * 1.4, Y - r * 0.6, X + r * 1.4, Y + r * 0.9), fill=(16, 14, 14))
        d.ellipse((X - r * 0.7 + 4 * math.sin(j), Y - r * 1.3, X + r * 0.7 + 4 * math.sin(j), Y + r * 0.1), fill=(24, 22, 24))
        if t > vo_end * 0.55 and j % 2 == 0:
            er = max(1.2, r * 0.12); a = int(255 * clamp((t - vo_end * 0.55) / 0.8))
            d.ellipse((X - r * 0.3 - er, Y - r * 0.6 - er, X - r * 0.3 + er, Y - r * 0.6 + er), fill=(255, 230, 230, a)); d.ellipse((X + r * 0.3 - er, Y - r * 0.6 - er, X + r * 0.3 + er, Y - r * 0.6 + er), fill=(255, 230, 230, a))
    # window frame + curtain flapping (foreground)
    fa = int(255 * (1 - clamp(p * 2.5)))
    d.rectangle((0, 0, 70, H), fill=(14, 14, 16, fa)); d.rectangle((W - 70, 0, W, H), fill=(14, 14, 16, fa))
    d.rectangle((0, 1280, W, 1340), fill=(14, 14, 16, fa))
    cur = [(W - 70, 0)] + [(W - 70 - 120 - 40 * math.sin(t * 3 + y / 200), y) for y in range(0, 1290, 60)] + [(W - 70, 1280)]
    d.polygon(cur, fill=(80, 54, 58, fa))
    out = Image.fromarray(finish(img, t, grade=(0.8, 0.82, 0.95), red=0.1 + 0.35 * p))
    subtitle(out, 7, t)
    return np.asarray(out)

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
