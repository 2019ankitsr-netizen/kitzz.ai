import sys, math; sys.path.insert(0, '/home/claude/bk')
from kit import *
from PIL import ImageChops
D = '/home/claude/s5'
TH = dict(accent=(255, 176, 72), chip_bg=(8, 10, 20), chip_font=fnt('InterDisplay-ExtraBold.otf', 58), nudge_bg=(255, 176, 72), nudge_ink=(8, 10, 20),
          nudge_font=fnt('InterDisplay-ExtraBold.otf', 52), card_bg=(8, 10, 20), card_ink=(255, 255, 255), cta_font=fnt('InterDisplay-Black.otf', 62),
          cap_font=fnt('Inter-ExtraBold.otf', 54), cap_bg=(8, 10, 20), who_font=fnt('Inter-Bold.otf', 34))
C = Comp(D, 24, TH); S = C.S
SURF = (S['hot']-0.15, S['next']-0.15)
def post(im, t):
    # bloom: blur of the bright parts added back (sun glare, atmosphere glow)
    small = im.resize((270, 480)); hi = small.point(lambda v: max(0, v-170)*3)
    bl = hi.filter(ImageFilter.GaussianBlur(10)).resize(im.size, Image.BILINEAR)
    im = ImageChops.add(im, bl)
    if SURF[0] <= t < SURF[1]:   # thick hazy air: orange fog toward the horizon
        fog = Image.new('RGB', im.size, (226, 140, 70)); m = Image.linear_gradient('L').resize(im.size)
        m = m.point(lambda v: int(150*(1-abs(v-110)/145)) if v < 255 else 0)
        im = Image.composite(fog, im, m)
    return im
C.post = post
def stop_card(c, dr, t, a, b, top, big):
    k = win(t, a, b, 0.15, 0.25)
    if not k: return
    s = eback(min(1, (t-a)/0.35))
    w_, h_ = 640*s, 210*s; x0 = W/2-w_/2; y0 = 330
    dr.rounded_rectangle([x0, y0, x0+w_, y0+h_], int(30*s), fill=(255, 176, 72, int(240*k)))
    if s > 0.6:
        dr.text((W/2, y0+52*s), top, font=fnt('InterDisplay-ExtraBold.otf', int(44*s)), fill=(8, 10, 20, int(255*k)), anchor='mm')
        dr.text((W/2, y0+140*s), big, font=fnt('InterDisplay-Black.otf', int(110*s)), fill=(8, 10, 20, int(255*k)), anchor='mm')
    c.box('stop', (x0, y0, x0+w_, y0+h_))
def extra(c, dr, t):
    stop_card(c, dr, t, 0.0, S['intro']+1.6, 'NEXT STOP', 'VENUS')
    stop_card(c, dr, t, S['next']-0.1, S['cta']-0.1, 'NEXT STOP', 'JUPITER')
    k = win(t, S['day']+2.2, S['west']-0.2)
    if k:
        c.text(dr, (W/2, 360), '1 day = 243 Earth days', fnt('InterDisplay-ExtraBold.otf', 66), (255, 176, 72, int(255*k)), 7)
        c.text(dr, (W/2, 450), '1 year = 225 Earth days', fnt('InterDisplay-ExtraBold.otf', 66), (255, 255, 255, int(255*k)), 7)
    c.chip(dr, t, 'Spins backwards  ↺', S['west']+0.5, S['hot']-0.2, col=(120, 210, 255))
    k = win(t, S['hot']+1.4, S['press']-0.2)
    if k:
        n = int(round(465*eout(min(1, (t-S['hot']-1.4)/1.6))))
        c.text(dr, (W/2, 400), f'{n}°C', fnt('InterDisplay-Black.otf', 190), (255, 176, 72, int(255*k)), 11, label='465')
        if t > S['hot']+4.5: c.text(dr, (W/2, 535), 'lead melts at 327°C', fnt('InterDisplay-ExtraBold.otf', 56), (255, 255, 255, int(255*k)), 6)
    c.chip(dr, t, '≈ 900 m under the sea', S['press']+0.6, S['imagine']-0.2, col=(255, 255, 255))
    c.chip(dr, t, 'Sunrise: WEST', S['imagine']+0.8, S['next']-0.25)
    c.nudge(dr, t, S['west']+0.6, 'Send to a space nerd ↗')
    c.cta(dr, t, S['cta'], [('save', 'SAVE the ride'), ('tag', 'TAG who goes')])
C.extra = extra
src = lambda fi: f'{D}/frames/f_{fi:04d}.jpg'
if sys.argv[1] == 'stills':
    import glob
    st = sorted(glob.glob(f'{D}/st4/still_*.jpg'))
    C.stills([float(x) for x in sys.argv[2].split(',')], lambda fi: st[min(len(st)-1, int(fi/24/9))], f'{D}/comp')
else: C.video(src, sys.argv[2])
