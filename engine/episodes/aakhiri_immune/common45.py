import os, sys, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/claude/ep1')
import render as R
from render import F, W, H, FPS, ease, clamp, finish, wrap

DUR, CHUNKS, VO_OFF = R.DUR, R.CHUNKS, R.VO_OFF

def subtitle(img, i, t, col=(255, 255, 255), label=None, y=1590):
    for a, b, p in CHUNKS[i]:
        if a <= t < b + 0.15:
            d = ImageDraw.Draw(img); f = F(62, 'ExtraBold')
            if label: d.text((W / 2, y - 80), label, font=F(38, 'Bold'), fill=(210, 210, 210), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))
            for k, l in enumerate(wrap(p.replace('...', '…'), f, 900)):
                d.text((W / 2, y + k * 80), l, font=f, fill=col, anchor='mm', stroke_width=5, stroke_fill=(0, 0, 0))
            break

MEERA_COL = (255, 170, 190)

def person(d, X, Y, k, c=(22, 22, 26), ponytail=False, gun=None, sitting=False, jacket=None):
    """standing silhouette, feet at (X,Y), height ~k*1.2"""
    body = jacket or c
    if sitting:
        d.rounded_rectangle((X - k * 0.2, Y - k * 0.62, X + k * 0.2, Y - k * 0.12), int(k * 0.08), fill=body)
        d.polygon([(X - k * 0.18, Y - k * 0.14), (X + k * 0.35, Y - k * 0.14), (X + k * 0.38, Y), (X + k * 0.26, Y), (X + k * 0.22, Y - k * 0.04), (X - k * 0.18, Y - k * 0.02)], fill=c)
        hy = Y - k * 0.75
    else:
        d.polygon([(X - k * 0.13, Y), (X - k * 0.06, Y), (X - k * 0.02, Y - k * 0.5), (X - k * 0.14, Y - k * 0.5)], fill=c)
        d.polygon([(X + k * 0.13, Y), (X + k * 0.06, Y), (X + k * 0.02, Y - k * 0.5), (X + k * 0.14, Y - k * 0.5)], fill=c)
        d.polygon([(X - k * 0.15, Y - k * 0.48), (X + k * 0.15, Y - k * 0.48), (X + k * 0.19, Y - k * 0.9), (X - k * 0.19, Y - k * 0.9)], fill=body)
        hy = Y - k * 1.0
    d.ellipse((X - k * 0.09, hy - k * 0.11, X + k * 0.09, hy + k * 0.08), fill=c)
    if ponytail:
        d.polygon([(X + k * 0.06, hy - k * 0.08), (X + k * 0.2, hy + k * 0.05), (X + k * 0.16, hy + k * 0.14), (X + k * 0.05, hy)], fill=c)
    if gun is not None and not sitting:
        # gun: 'aim' (arms forward to the left) or 'down'
        if gun == 'aim':
            d.polygon([(X - k * 0.15, Y - k * 0.85), (X - k * 0.55, Y - k * 0.8), (X - k * 0.55, Y - k * 0.74), (X - k * 0.15, Y - k * 0.76)], fill=body)
            d.rectangle((X - k * 0.72, Y - k * 0.83, X - k * 0.5, Y - k * 0.77), fill=(10, 10, 12)); d.rectangle((X - k * 0.56, Y - k * 0.79, X - k * 0.52, Y - k * 0.7), fill=(10, 10, 12))
        else:
            d.polygon([(X - k * 0.19, Y - k * 0.88), (X - k * 0.24, Y - k * 0.5), (X - k * 0.18, Y - k * 0.5), (X - k * 0.14, Y - k * 0.86)], fill=body)
            d.rectangle((X - k * 0.25, Y - k * 0.5, X - k * 0.2, Y - k * 0.36), fill=(10, 10, 12))

def end_card(t, te, big, small, sub):
    card = Image.new('RGB', (W, H), (6, 6, 8)); cd = ImageDraw.Draw(card)
    a = clamp((te - 0.4) / 0.5); a2 = clamp((te - 1.0) / 0.5)
    cd.text((W / 2, 860), big, font=F(140, 'ExtraBold'), fill=tuple(int(c * a) for c in (240, 240, 245)), anchor='mm')
    cd.text((W / 2, 1020), small, font=F(70, 'ExtraBold'), fill=tuple(int(c * a2) for c in (230, 50, 50)), anchor='mm')
    cd.text((W / 2, 1110), sub, font=F(40, 'Bold'), fill=tuple(int(c * a2) for c in (170, 170, 180)), anchor='mm')
    return finish(card, t, grade=(1, 1, 1))

def title(img, part, name, t):
    d = ImageDraw.Draw(img)
    d.text((W / 2, 120), part, font=F(44, 'ExtraBold'), fill=(235, 60, 60), anchor='mm', stroke_width=3, stroke_fill=(0, 0, 0))
    a = clamp((t - 0.8) / 0.5)
    if a > 0: d.text((W / 2, 205), name, font=F(64, 'ExtraBold'), fill=tuple(int(c * a) for c in (240, 240, 245)), anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))

def fire(img, cx, cy, t, s=1.0):
    gl = Image.new('L', (W, H), 0); ImageDraw.Draw(gl).ellipse((cx - 420 * s, cy - 380 * s, cx + 420 * s, cy + 200 * s), fill=150)
    img = Image.composite(Image.new('RGB', (W, H), (255, 150, 60)), img, gl.filter(ImageFilter.GaussianBlur(70)))
    d = ImageDraw.Draw(img, 'RGBA')
    for k in range(5):
        h = (90 + 40 * math.sin(t * 7 + k * 1.7)) * s; x = cx + (k - 2) * 22 * s
        d.polygon([(x - 26 * s, cy), (x + 3 * math.sin(t * 9 + k) * s * 5, cy - h), (x + 26 * s, cy)], fill=(255, 140 + k * 20, 40, 220))
    d.polygon([(cx - 14 * s, cy), (cx, cy - 60 * s - 10 * math.sin(t * 11) * s), (cx + 14 * s, cy)], fill=(255, 240, 160))
    d.rectangle((cx - 70 * s, cy - 8 * s, cx + 70 * s, cy + 12 * s), fill=(60, 36, 24))
    return img

def write_scenes(SCENES, still=None, idx=None):
    if still is not None:
        Image.fromarray(SCENES[idx](still)).save(f'still_{idx + 1}_{still:.1f}.jpg', quality=88); return
    os.makedirs('scenes', exist_ok=True)
    i = idx; f = SCENES[i]; n = int(round(DUR[i] * FPS)); tmp = f'scenes/s{i + 1}.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(f(k / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f'scenes/s{i + 1}.mp4')

def main(SCENES):
    if sys.argv[1] == 'still': write_scenes(SCENES, float(sys.argv[3]), int(sys.argv[2]) - 1)
    elif sys.argv[1] == 'info': print([round(x, 2) for x in DUR], sum(DUR))
    else: write_scenes(SCENES, idx=int(sys.argv[1]) - 1)
