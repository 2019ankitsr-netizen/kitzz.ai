import sys, math, random
sys.path.insert(0, '/home/claude')
from common45 import *

def dam_bg(night=0.0):
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img)
    hz = 1000
    for y in range(hz):
        k = y / hz
        c1 = (int(70 + 170 * k), int(60 + 90 * k), int(100 - 20 * k)); c2 = (int(14 + 30 * k), int(16 + 26 * k), int(34 + 30 * k))
        d.line((0, y, W, y), fill=tuple(int(a * (1 - night) + b * night) for a, b in zip(c1, c2)))
    if night < 0.5: d.ellipse((W / 2 - 110, hz - 170, W / 2 + 110, hz + 50), fill=(255, 190, 110))
    else:
        rnd = random.Random(3)
        for _ in range(80): x, y = rnd.uniform(0, W), rnd.uniform(0, hz * 0.7); d.ellipse((x, y, x + 3, y + 3), fill=(220, 220, 240))
    hill = (60, 50, 70) if night < 0.5 else (20, 20, 30)
    d.polygon([(0, hz), (0, 760), (260, 700), (520, 820), (760, 720), (W, 780), (W, hz)], fill=hill)
    damc = (110, 104, 110) if night < 0.5 else (46, 46, 56)
    d.polygon([(140, hz), (200, 860), (880, 860), (940, hz)], fill=damc)
    for x in range(220, 880, 60): d.rectangle((x, 870, x + 30, 960), fill=tuple(c - 20 for c in damc))
    d.rectangle((0, hz, W, H), fill=(40, 40, 44) if night < 0.5 else (18, 18, 22))
    return img
DUSK = dam_bg(0.0); NIGHT = dam_bg(1.0)

def s1(t):
    p = clamp(t / (DUR[0] - 0.5))
    img = DUSK.copy(); d = ImageDraw.Draw(img, 'RGBA')
    person(d, 760, 1560, 560, c=(18, 16, 20), ponytail=True, gun='aim', jacket=(46, 56, 40))
    person(d, 240, 1230, 230, c=(18, 16, 20))  # him far
    title(img, 'PART 4', 'आख़िरी इम्यून · मीरा', t)
    subtitle(img, 0, t)
    return finish(img, t, grade=(1.02, 0.96, 0.95))

def s2(t):
    img = DUSK.copy(); d = ImageDraw.Draw(img, 'RGBA')
    z = 1.35; cw, ch = W / z, H / z
    img = img.crop((int(W / 2 - cw / 2), int(H * 0.45 - ch / 2), int(W / 2 + cw / 2), int(H * 0.45 + ch / 2))).resize((W, H)); d = ImageDraw.Draw(img, 'RGBA')
    person(d, 700, 1820, 1000, c=(16, 14, 18), ponytail=True, gun='aim', jacket=(46, 56, 40))
    subtitle(img, 1, t, col=MEERA_COL, label='मीरा')
    return finish(img, t, grade=(1.0, 0.95, 0.95))

def arm(d, yb, t, glow_on=True):
    sk = (176, 128, 98); sk2 = (160, 114, 86)
    d.polygon([(-40, yb - 150), (690, yb - 105), (700, yb + 105), (-40, yb + 170)], fill=sk)
    d.ellipse((640, yb - 135, 900, yb + 130), fill=sk)
    for k, (dy, ln) in enumerate([(-95, 170), (-35, 200), (25, 190), (80, 150)]): d.rounded_rectangle((850, yb + dy - 24, 850 + ln, yb + dy + 24), 24, fill=sk)
    d.rounded_rectangle((700, yb - 175, 830, yb - 125), 25, fill=sk)
    if glow_on:
        g = 0.5 + 0.5 * math.sin(t * 3)
        for v in [[(-40, yb - 20), (250, yb - 30), (480, yb - 5), (690, yb - 25)], [(-40, yb + 60), (220, yb + 40), (430, yb + 50), (690, yb + 30)]]:
            d.line(v, fill=(60, 140, 255, int(80 + 120 * g)), width=20, joint='curve'); d.line(v, fill=(150, 215, 255, int(150 + 100 * g)), width=6, joint='curve')

def s3(t):
    vd = DUR[2] - 0.55
    img = Image.new('RGB', (W, H), (14, 14, 20)); d = ImageDraw.Draw(img, 'RGBA')
    if t < vd * 0.55:
        # torch beam on his wrist
        bm = Image.new('L', (W, H), 0); ImageDraw.Draw(bm).ellipse((150, 650, 900, 1250), fill=150)
        img = Image.composite(Image.new('RGB', (W, H), (255, 245, 210)), img, bm.filter(ImageFilter.GaussianBlur(60))); d = ImageDraw.Draw(img, 'RGBA')
        arm(d, 950, t)
    else:
        img = DUSK.copy(); d = ImageDraw.Draw(img, 'RGBA')
        person(d, 720, 1560, 560, c=(18, 16, 20), ponytail=True, gun='down', jacket=(46, 56, 40))
        a = clamp((t - vd * 0.75) / 0.4)
        if a > 0:
            d.text((W / 2, 520), 'मीरा', font=F(150, 'ExtraBold'), fill=MEERA_COL + (int(255 * a),), anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
    subtitle(img, 2, t)
    return finish(img, t, grade=(1.0, 0.97, 0.96))

def campfire(t):
    img = NIGHT.copy()
    img = fire(img, W / 2, 1300, t, 1.0)
    d = ImageDraw.Draw(img, 'RGBA')
    person(d, 300, 1330, 380, c=(14, 12, 14), sitting=True)
    person(d, 790, 1330, 380, c=(14, 12, 14), ponytail=True, sitting=True, jacket=(30, 36, 26))
    return img

def s4(t):
    img = campfire(t); d = ImageDraw.Draw(img, 'RGBA')
    vd = DUR[3] - 0.55
    p = ease(clamp((t - vd * 0.25) / 0.6))
    if p > 0:
        x0, y0 = 170, 360 + int(140 * (1 - p))
        d.rounded_rectangle((x0, y0, x0 + 740, y0 + 440), 30, fill=(240, 240, 236, int(255 * p)))
        d.rectangle((x0, y0, x0 + 740, y0 + 100), fill=(30, 70, 120, int(255 * p)))
        d.text((x0 + 370, y0 + 52), 'राष्ट्रीय विषाणु शोध केंद्र · पुणे', font=F(38, 'ExtraBold'), fill=(255, 255, 255, int(255 * p)), anchor='mm')
        d.rounded_rectangle((x0 + 40, y0 + 140, x0 + 240, y0 + 380), 16, fill=(170, 176, 186, int(255 * p)))
        person(d, x0 + 140, y0 + 400, 260, c=(60, 62, 70), ponytail=True)
        for k, (lab, val) in enumerate([('नाम', 'डॉ. मीरा'), ('पद', 'रिसर्च साइंटिस्ट'), ('विभाग', 'इम्यून प्रोजेक्ट')]):
            d.text((x0 + 280, y0 + 170 + k * 75), f'{lab}:', font=F(32, 'Bold'), fill=(90, 90, 100, int(255 * p)), anchor='lm')
            d.text((x0 + 400, y0 + 170 + k * 75), val, font=F(36, 'ExtraBold'), fill=(20, 20, 26, int(255 * p)), anchor='lm')
    subtitle(img, 3, t)
    return finish(img, t, grade=(1.0, 0.95, 0.92))

def s5(t):
    img = NIGHT.copy(); img = fire(img, W / 2 + 120, 1300, t, 1.0)
    d = ImageDraw.Draw(img, 'RGBA')
    back = ease(clamp(t / 3.0))
    shake = 5 * math.sin(t * 30)
    person(d, 300 - 160 * back + shake, 1360 + 40 * back, 560 + 120 * back, c=(12, 10, 12))
    person(d, 860, 1330, 380, c=(14, 12, 14), ponytail=True, sitting=True, jacket=(30, 36, 26))
    subtitle(img, 4, t)
    return finish(img, t, grade=(1.0, 0.92, 0.92), red=0.2 * back)

def s6(t):
    img = Image.new('RGB', (W, H), (30, 20, 16))
    d = ImageDraw.Draw(img, 'RGBA')
    # notebook
    d.rounded_rectangle((120, 330, 960, 1320), 24, fill=(232, 224, 200))
    for y in range(420, 1300, 52): d.line((150, y, 930, y), fill=(190, 200, 220), width=2)
    d.line((220, 340, 220, 1310), fill=(220, 120, 120), width=3)
    d.text((540, 390), 'Protocol M', font=F(64, 'ExtraBold'), fill=(40, 40, 80), anchor='mm')
    # dna sketch draws itself
    p = clamp(t / 4.0)
    for k in range(int(30 * p)):
        y = 500 + k * 16; ph = k * 0.45
        x1 = 360 + 90 * math.sin(ph); x2 = 360 - 90 * math.sin(ph)
        d.ellipse((x1 - 6, y - 6, x1 + 6, y + 6), fill=(40, 60, 140)); d.ellipse((x2 - 6, y - 6, x2 + 6, y + 6), fill=(160, 40, 40))
        if k % 2 == 0: d.line((x1, y, x2, y), fill=(80, 80, 90), width=2)
    eqs = ['ब्लड सैंपल: 50 ml / दिन', 'कोई मौत नहीं', 'वैक्सीन: 14 दिन', '✓ संभव'.replace('✓ ', '')]
    for k, e in enumerate(eqs):
        if t > 1.0 + k * 1.2: d.text((520, 560 + k * 140), e, font=F(44, 'Bold'), fill=(40, 40, 80), anchor='lm')
    if t > 1.0 + 3 * 1.2 + 0.3:
        d.ellipse((490, 920, 760, 1040), outline=(200, 30, 30), width=6)
    subtitle(img, 5, t, col=MEERA_COL, label='मीरा')
    return finish(img, t, grade=(1.0, 0.97, 0.94))

def spot(t, strength=1.0):
    img = campfire(t)
    dark = Image.new('RGB', (W, H), (4, 4, 8))
    m = Image.new('L', (W, H), int(255 * 0.75 * strength)); md = ImageDraw.Draw(m)
    for k, cx in enumerate((300 + 40 * math.sin(t * 1.3), 790 + 40 * math.sin(t * 1.1 + 1))):
        md.ellipse((cx - 260, 900, cx + 260, 1420), fill=0)
    img = Image.composite(dark, img, m.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(img, 'RGBA')
    for k, cx in enumerate((300 + 40 * math.sin(t * 1.3), 790 + 40 * math.sin(t * 1.1 + 1))):
        d.polygon([(cx - 30 + (k * 2 - 1) * 200, 0), (cx + 30 + (k * 2 - 1) * 200, 0), (cx + 230, 1350), (cx - 230, 1350)], fill=(255, 255, 240, int(35 * strength)))
    return img

def s7(t):
    img = spot(t, clamp(t / 0.6))
    subtitle(img, 6, t, col=(255, 214, 90), label='लाउडस्पीकर पर')
    return finish(img, t, grade=(0.95, 0.95, 1.0), flash=0.25 * clamp(1 - t / 0.25))

def s8(t):
    vo_end = DUR[7] - 2.6
    if t >= vo_end: return end_card(t, t - vo_end, 'Part 5?', 'आख़िरी इम्यून', 'फ़िनाले परसों · Follow करो')
    p = clamp(t / vo_end)
    img = spot(t + 3)
    z = 1 + 0.6 * ease(p); cw, ch = W / z, H / z; cx, cy = 550, 1150
    img = img.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR)
    subtitle(img, 7, t)
    return finish(img, t, grade=(0.95, 0.93, 1.0), red=0.25 * p)

SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
if __name__ == '__main__': main(SCENES)
