import sys, math, random; sys.path.insert(0, '/home/claude/bk')
from kit import *
from PIL import ImageChops, ImageOps
import numpy as np
D = '/home/claude/s3'
MONO = fnt('Inter-Bold.otf', 40)
TH = dict(accent=(255, 70, 70), chip_bg=(10, 12, 12), chip_font=fnt('InterDisplay-ExtraBold.otf', 56), nudge_bg=(255, 70, 70), nudge_ink=(255, 255, 255),
          nudge_font=fnt('InterDisplay-ExtraBold.otf', 52), card_bg=(10, 12, 12), card_ink=(255, 255, 255), cta_font=fnt('InterDisplay-Black.otf', 62),
          cap_font=fnt('Inter-ExtraBold.otf', 54), cap_bg=(10, 12, 12), who_font=fnt('Inter-Bold.otf', 34))
C = Comp(D, 12, TH); S = C.S
rng = np.random.default_rng(1)
SCAN = Image.new('L', (W, H), 0)
_d = ImageDraw.Draw(SCAN)
for y in range(0, H, 4): _d.line([(0, y), (W, y)], fill=38)
VIG = Image.radial_gradient('L').resize((W, H)).point(lambda v: int(min(255, v*1.1)))
def post(im, t):
    g = ImageOps.grayscale(im); gi = Image.merge('RGB', (g.point(lambda v: v*0.86), g, g.point(lambda v: v*0.9)))   # CCTV green-grey
    im = Image.blend(gi, im, 0.45)   # keep some colour: the red hotel is the clue
    im = Image.blend(im, im.filter(ImageFilter.GaussianBlur(1.2)), 0.35)
    n = Image.fromarray((rng.normal(0, 18, (H//2, W//2))+128).clip(0, 255).astype('uint8')).resize((W, H))
    im = ImageChops.add(im, Image.merge('RGB', (n, n, n)), 1, -128)
    im = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), im, SCAN)
    im = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), im, VIG.point(lambda v: int(v*0.55)))
    if int(t*12) % 37 in (0,):   # tracking glitch
        a = rng.integers(300, 1500); im.paste(im.crop((0, a, W, a+40)).transform((W, 40), Image.AFFINE, (1, 0, -30, 0, 1, 0)), (0, a))
    return im
C.post = post
def extra(c, dr, t):
    # CCTV HUD (inside safe zone)
    cam = 'CAM 03' if S['stop']+0.6 <= t < S['clue'] else 'CAM 02'
    dr.text((95, 300), cam, font=MONO, fill=(235, 235, 235, 230)); c.box('hud', (95, 300, 260, 345))
    ts = f'23:{10 + int(t//60):02d}:{int(t % 60):02d}'
    dr.text((985, 300), ts, font=MONO, fill=(235, 235, 235, 230), anchor='ra'); c.box('ts', (800, 300, 985, 345))
    if int(t*2) % 2 == 0: dr.ellipse([95, 360, 125, 390], fill=(255, 50, 50, 240))
    dr.text((140, 356), 'REC', font=MONO, fill=(235, 235, 235, 230)); c.box('rec', (95, 356, 230, 395))
    # hook title
    k = win(t, 0.0, S['solved']-0.1, 0.1, 0.2)
    if k:
        c.text(dr, (W/2, 520), 'CASE 04', fnt('InterDisplay-Black.otf', 120), (255, 70, 70, int(255*k)), 8)
        c.text(dr, (W/2, 630), 'The Car & the Hotel', fnt('InterDisplay-ExtraBold.otf', 66), (255, 255, 255, int(255*k)), 6)
    # case 03 solved card
    k = win(t, S['solved']-0.05, S['log']-0.1, 0.2, 0.2)
    if k:
        s = eback(min(1, (t-S['solved'])/0.35)); x0, y0, x1, y1 = W/2-400*s, 470, W/2+400*s, 470+300*s
        dr.rounded_rectangle([x0, y0, x1, y1], 26, fill=(238, 232, 214, int(245*k)))
        if s > 0.7:
            dr.text((W/2, y0+60), 'CASE 03 · SOLVED', font=fnt('InterDisplay-Black.otf', 56), fill=(200, 30, 30, int(255*k)), anchor='mm')
            dr.text((W/2, y0+150), 'The surgeon =', font=fnt('InterDisplay-ExtraBold.otf', 60), fill=(20, 20, 20, int(255*k)), anchor='mm')
            dr.text((W/2, y0+230), "the boy's MOTHER", font=fnt('InterDisplay-Black.otf', 66), fill=(20, 20, 20, int(255*k)), anchor='mm')
        c.box('solved', (x0, y0, x1, y1))
    c.chip(dr, t, 'Cam 02 · Hotel car park · 23:10', S['log']+0.2, S['setup']-0.1, col=(255, 255, 255), y=470)
    c.chip(dr, t, '"I\'m bankrupt."', S['stop']+2.4, S['ask']-0.1, y=470)
    k = win(t, S['ask']+0.2, S['clue']-0.1)
    if k:
        for i, (w_, on) in enumerate([('No crash', 0.2), ('No theft', 0.8), ('No one touched it', 1.4)]):
            if t > S['ask']+on: c.text(dr, (W/2, 450+i*80), '× '+w_, fnt('InterDisplay-ExtraBold.otf', 60), (255, 255, 255, int(255*k)), 6)
    k = win(t, S['clue']+0.3, S['cta']+0.2)
    if k:
        c.text(dr, (W/2, 450), 'CLUE', fnt('InterDisplay-Black.otf', 110), (255, 70, 70, int(255*k)), 8)
        c.text(dr, (W/2, 560), 'red hotel · tiny town', fnt('InterDisplay-ExtraBold.otf', 60), (255, 255, 255, int(255*k)), 6)
    c.nudge(dr, t, S['stop']+0.4, 'Send to your smartest friend ↗')
    c.cta(dr, t, S['cta'], [('comment', 'COMMENT it'), ('send', 'SEND it')])
C.extra = extra
src = lambda fi: f'{D}/frames/f_{fi:04d}.jpg'
if sys.argv[1] == 'stills':
    import glob
    st = sorted(glob.glob(f'{D}/st1/still_*.jpg'))
    C.stills([float(x) for x in sys.argv[2].split(',')], lambda fi: st[min(len(st)-1, int(fi/12/9))], f'{D}/comp')
else: C.video(src, sys.argv[2], out_fps=24)
