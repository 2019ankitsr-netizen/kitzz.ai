import sys, math, random
sys.path.insert(0, '/home/claude')
from common45 import *

def lab_bg():
    img = Image.new('RGB', (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H; d.line((0, y, W, y), fill=(int(200 - 90 * k), int(214 - 90 * k), int(222 - 80 * k)))
    d.rectangle((0, 1300, W, H), fill=(150, 160, 166))
    for x in range(0, W, 180): d.line((x, 1300, x - 200, H), fill=(136, 146, 152), width=4)
    for x in (140, 540, 940): d.rectangle((x - 90, 110, x + 90, 140), fill=(250, 255, 255))
    # monitors
    for k, x in enumerate((90, 760)):
        d.rectangle((x, 520, x + 230, 680), fill=(20, 26, 30), outline=(80, 90, 96), width=6)
    # tiles
    for y in range(160, 1300, 140): d.line((0, y, W, y), fill=(180, 192, 198), width=2)
    return img
LAB = lab_bg()

def chair(d, X, Y, k, strapped=True, c=(26, 28, 32)):
    d.rounded_rectangle((X - k * 0.32, Y - k * 1.15, X + k * 0.32, Y - k * 0.45), int(k * 0.06), fill=(70, 76, 84))
    d.rectangle((X - k * 0.38, Y - k * 0.5, X + k * 0.38, Y - k * 0.4), fill=(70, 76, 84))
    d.rectangle((X - k * 0.3, Y - k * 0.4, X - k * 0.25, Y), fill=(60, 66, 72)); d.rectangle((X + k * 0.25, Y - k * 0.4, X + k * 0.3, Y), fill=(60, 66, 72))
    person(d, X, Y - k * 0.05, k * 0.95, c=c, sitting=True)
    if strapped:
        for yy_ in (Y - k * 0.62, Y - k * 0.4):
            d.rectangle((X - k * 0.36, yy_, X + k * 0.36, yy_ + k * 0.05), fill=(120, 80, 40))

def monitors(d, t, flat=False):
    for k, x in enumerate((90, 760)):
        pts = []
        for xx_ in range(x + 10, x + 220, 3):
            f = ((xx_ - x) / 210 * 3 + t * 1.8 + k) % 1.0; y = 600
            if 0.45 < f < 0.5: y -= 40
            elif 0.5 <= f < 0.55: y += 22
            pts.append((xx_, y))
        d.line(pts, fill=(80, 255, 120), width=3)

def s1(t):
    img = LAB.copy(); d = ImageDraw.Draw(img, 'RGBA')
    p = clamp(t / (DUR[0] - 0.5))
    monitors(d, t)
    chair(d, W / 2, 1340, 640)
    z = 1 + 0.1 * p; cw, ch = W / z, H / z
    img = img.crop((int(W / 2 - cw / 2), int(H / 2 - ch / 2), int(W / 2 + cw / 2), int(H / 2 + ch / 2))).resize((W, H), Image.BILINEAR)
    title(img, 'PART 5 · FINALE', 'आख़िरी इम्यून · फ़ैसला', t)
    subtitle(img, 0, t)
    return finish(img, t, grade=(0.9, 0.98, 1.08))

def s2(t):
    img = LAB.copy(); d = ImageDraw.Draw(img, 'RGBA')
    monitors(d, t)
    # door on right wall opening
    op = ease(clamp(t / 1.2))
    dx0, dx1 = 640, 1000
    d.rectangle((dx0, 600, dx1, 1300), fill=(250, 250, 240))
    d.rectangle((dx0, 600, dx0 + (dx1 - dx0) * (1 - op), 1300), fill=(110, 120, 128))
    for k in range(3):
        a = clamp((t - 1.0 - k * 0.4) / 0.6)
        if a > 0:
            x = dx1 - 40 - k * 175 - 60 * a
            if k == 1: person(d, x, 1300 + 20 * a, 600, c=(20, 20, 24), ponytail=True, jacket=(240, 242, 236))
            else:
                person(d, x, 1300 + 20 * a, 620, c=(225, 228, 220))
                d.rectangle((x - 30, 1300 + 20 * a - 640, x + 30, 1300 + 20 * a - 610), fill=(30, 40, 50))
    chair(d, 280, 1400, 560)
    subtitle(img, 1, t)
    return finish(img, t, grade=(0.9, 0.98, 1.06))

def s3(t):
    img = LAB.copy(); d = ImageDraw.Draw(img, 'RGBA')
    z = 1.6; cw, ch = W / z, H / z
    img = img.crop((int(W / 2 - cw / 2), 200, int(W / 2 + cw / 2), int(200 + ch))).resize((W, H)); d = ImageDraw.Draw(img, 'RGBA')
    chair(d, 330, 1900, 1100)
    person(d, 780, 1900, 1150, c=(22, 20, 24), ponytail=True, jacket=(240, 242, 236))
    subtitle(img, 2, t, col=MEERA_COL, label='मीरा, धीमी आवाज़ में')
    return finish(img, t, grade=(0.9, 0.96, 1.05))

def s4(t):
    img = Image.new('RGB', (W, H), (190, 198, 204)); d = ImageDraw.Draw(img, 'RGBA')
    # close-up strap unbuckling on the armrest
    d.rectangle((0, 760, W, 1160), fill=(70, 76, 84))
    d.polygon([(-40, 860), (W + 40, 820), (W + 40, 1040), (-40, 1080)], fill=(176, 128, 98))
    p = ease(clamp((t - 1.0) / 2.0))
    sx = 520 - 260 * p
    d.rectangle((sx - 60, 760, sx + 60, 1160), fill=(120, 80, 40))
    d.rectangle((sx - 80, 920 - 40, sx + 80, 920 + 40), outline=(200, 190, 150), width=10)
    # her hand (gloved white)
    d.ellipse((sx + 40, 840, sx + 260, 1000), fill=(236, 238, 232)); d.rounded_rectangle((sx + 200, 860, sx + 520, 960), 40, fill=(236, 238, 232))
    subtitle(img, 3, t)
    return finish(img, t, grade=(0.95, 0.98, 1.04))

def s5(t):
    img = LAB.copy(); d = ImageDraw.Draw(img, 'RGBA')
    chair(d, W / 2, 1340, 640, strapped=False)
    img = Image.blend(img, Image.new('RGB', (W, H), (0, 0, 0)), 0.82)
    on = int(t * 3) % 2 == 0
    if on:
        red = Image.new('L', (W, H), 0); ImageDraw.Draw(red).ellipse((W / 2 - 600, -200, W / 2 + 600, 900), fill=140)
        img = Image.composite(Image.new('RGB', (W, H), (255, 20, 20)), img, red.filter(ImageFilter.GaussianBlur(80)))
    d = ImageDraw.Draw(img, 'RGBA')
    d.rounded_rectangle((W / 2 - 60, 160, W / 2 + 60, 260), 20, fill=(255, 40, 40) if on else (80, 10, 10))
    rnd = random.Random(int(t * 10))
    for _ in range(6 if rnd.random() < 0.5 else 0):
        x, y = rnd.uniform(100, W - 100), rnd.uniform(400, 1200)
        for k in range(5): d.line((x, y, x + rnd.uniform(-60, 60), y + rnd.uniform(-60, 60)), fill=(255, 220, 120), width=3)
    for k in range(4):
        x = (t * 500 + k * 300) % (W + 300) - 150
        person(d, x, 1500, 520, c=(8, 8, 10))
    subtitle(img, 4, t)
    return finish(img, t, grade=(1.0, 0.9, 0.9), flash=0.2 if (int(t * 8) % 7 == 0) else 0)

def syringe(d, cx, cy, s, t, glow=1.0):
    d.rounded_rectangle((cx - 260 * s, cy - 45 * s, cx + 200 * s, cy + 45 * s), int(20 * s), fill=(220, 236, 240, 230), outline=(160, 180, 190), width=4)
    lvl = 0.75
    d.rounded_rectangle((cx - 240 * s, cy - 30 * s, cx - 240 * s + 420 * s * lvl, cy + 30 * s), int(12 * s), fill=(60, 140, 255, int(220 * glow)))
    d.rectangle((cx + 200 * s, cy - 8 * s, cx + 330 * s, cy + 8 * s), fill=(200, 200, 210))
    d.line((cx + 330 * s, cy, cx + 440 * s, cy), fill=(200, 200, 210), width=max(2, int(4 * s)))
    d.rectangle((cx - 330 * s, cy - 70 * s, cx - 260 * s, cy + 70 * s), fill=(200, 200, 210))

def s6(t):
    img = Image.new('RGB', (W, H), (10, 10, 16)); d = ImageDraw.Draw(img, 'RGBA')
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((150, 650, 930, 1150), fill=160)
    img = Image.composite(Image.new('RGB', (W, H), (60, 130, 255)), img, g.filter(ImageFilter.GaussianBlur(90))); d = ImageDraw.Draw(img, 'RGBA')
    p = ease(clamp(t / 2.0))
    syringe(d, 480 - 120 * (1 - p), 900, 1.0, t)
    subtitle(img, 5, t)
    return finish(img, t, grade=(0.92, 0.98, 1.1))

def s7(t):
    img = Image.new('RGB', (W, H), (14, 14, 20)); d = ImageDraw.Draw(img, 'RGBA')
    yb = 980; sk = (176, 128, 98)
    up = ease(clamp(t / 2.0))
    d.polygon([(-40, yb - 150), (690, yb - 105), (700, yb + 105), (-40, yb + 170)], fill=sk)
    d.ellipse((640, yb - 135, 900, yb + 130), fill=sk)
    for (dy, ln) in [(-95, 170), (-35, 200), (25, 190), (80, 150)]: d.rounded_rectangle((850, yb + dy - 24, 850 + ln, yb + dy + 24), 24, fill=sk)
    # sleeve moving left
    sx = 640 - 560 * up
    d.polygon([(-60, yb - 200), (sx, yb - 170), (sx + 20, yb + 180), (-60, yb + 220)], fill=(60, 66, 90))
    gl = 0.5 + 0.5 * math.sin(t * 4)
    for v in [[(sx, yb - 20), (480, yb - 5), (690, yb - 25)], [(sx, yb + 50), (430, yb + 50), (690, yb + 30)]]:
        d.line(v, fill=(60, 140, 255, int(80 + 120 * gl)), width=20, joint='curve')
    if t > 2.6:
        q = ease(clamp((t - 2.6) / 1.5)); syringe(d, 620, 760 - 60 * q, 0.6, t)
    bluef = clamp((t - (DUR[6] - 1.4)) / 0.8)
    subtitle(img, 6, t)
    return finish(img, t, grade=(0.95, 0.97, 1.05), flash=0.0) if bluef == 0 else np.clip(finish(img, t) * (1 - bluef) + np.array([60, 140, 255]) * bluef, 0, 255).astype(np.uint8)

def phone_end(t):
    s = Image.new('RGBA', (R.SW, R.SH), (32, 33, 44, 255)); d = ImageDraw.Draw(s)
    d.rectangle((0, 0, R.SW, 150), fill=(16, 18, 22)); d.text((40, 95), 'RideGo', font=F(44, 'ExtraBold'), fill=(255, 255, 255), anchor='lm'); d.text((R.SW - 40, 95), '8:10', font=F(36, 'Medium'), fill=(200, 200, 200), anchor='rm')
    d.rounded_rectangle((20, 190, R.SW - 20, 340), 30, fill=(240, 250, 242)); d.ellipse((44, 227, 120, 303), fill=(40, 170, 80))
    d.line((62, 265, 78, 282, 104, 248), fill=(255, 255, 255), width=8)
    d.text((144, 242), 'राइड कन्फ़र्म', font=F(36, 'ExtraBold'), fill=(20, 20, 24), anchor='lm'); d.text((144, 290), 'ड्राइवर 3 मिनट में आ रहा है', font=F(29, 'Medium'), fill=(80, 80, 90), anchor='lm')
    if t > 1.6:
        d.rounded_rectangle((20, 370, R.SW - 20, 560), 30, fill=(46, 46, 66))
        d.ellipse((44, 400, 104, 460), fill=(220, 110, 60)); d.text((74, 430), 'र', font=F(30, 'ExtraBold'), fill=(255, 255, 255), anchor='mm')
        d.ellipse((92, 446, 110, 464), fill=(70, 200, 90))
        d.text((130, 420), 'राहुल · ऑनलाइन', font=F(30, 'ExtraBold'), fill=(255, 255, 255), anchor='lm')
        d.text((130, 480), 'भाई... ऑफिस आ रहा है? 😄'.replace(' 😄', ''), font=F(32, 'Bold'), fill=(220, 220, 235), anchor='lm')
    return s.convert('RGB')

def s8(t):
    vo_end = DUR[7] - 2.6
    if t >= vo_end: return end_card(t, t - vo_end, 'समाप्त', 'आख़िरी इम्यून', 'Season 2 चाहिए? Comment करो')
    seg = vo_end * 0.55
    if t < seg:
        # world map turns from red to blue (callback to Ep1)
        img = Image.new('RGB', (W, H), (8, 10, 18)); d = ImageDraw.Draw(img)
        tt = t / seg * 5.0
        for (x, y, th) in R.DOTS:
            cured = tt > (th - 0.4) * 0.6
            c = (70, 150, 255) if cured else (235, 50, 50)
            d.ellipse((110 + x - 5, 650 + y - 5, 110 + x + 5, 650 + y + 5), fill=c)
        pr = 10 + (t * 60) % 80
        d.ellipse((110 + 0.69 * R.MW - pr, 650 + 0.40 * R.MH - pr, 110 + 0.69 * R.MW + pr, 650 + 0.40 * R.MH + pr), outline=(120, 190, 255), width=3)
        pct = max(0, int(99 - t / seg * 99))
        d.text((W / 2, 1220), f'संक्रमित: {pct}%', font=F(70, 'ExtraBold'), fill=(120, 190, 255), anchor='mm')
        subtitle(img, 7, t)
        return finish(img, t, grade=(0.95, 1.0, 1.05))
    img = R.phone(phone_end(t - seg), y0=330)
    subtitle(img, 7, t)
    return finish(img, t, grade=(1.0, 1.0, 1.0))

SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
if __name__ == '__main__': main(SCENES)
