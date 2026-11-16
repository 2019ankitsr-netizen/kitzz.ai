import sys, math; sys.path.insert(0, '/home/claude/bk')
from kit import *
D = '/home/claude/s4'
TH = dict(accent=(255, 196, 0), chip_bg=(20, 18, 30), chip_font=fnt('InterDisplay-ExtraBold.otf', 60), nudge_bg=(255, 196, 0), nudge_ink=(20, 18, 30),
          nudge_font=fnt('InterDisplay-ExtraBold.otf', 54), card_bg=(20, 18, 30), card_ink=(255, 255, 255), cta_font=fnt('InterDisplay-Black.otf', 66),
          cap_font=fnt('Inter-ExtraBold.otf', 56), cap_bg=(20, 18, 30), who_font=fnt('Inter-Bold.otf', 34))
C = Comp(D, 24, TH); S = C.S; E = C.E
GOLD, WHITE = (255, 196, 0), (255, 255, 255)
def slam(c, dr, t, t0, xy, txt, size, col, k):
    if t < t0: return
    s = eback(min(1, (t-t0)/0.18), 2.4); f = fnt('InterDisplay-Black.otf', max(8, int(size*s)))
    c.text(dr, xy, txt, f, (*col, int(255*k)), 9)
def big(c, dr, t, a, b, l1, l2, y=400):
    k = win(t, a, b)
    if not k: return
    s = eback(min(1, (t-a)/0.3))
    c.text(dr, (W/2, y), l1, fnt('InterDisplay-Black.otf', max(8, int(150*s))), (*GOLD, int(255*k)), 10)
    if l2: c.text(dr, (W/2, y+120), l2, fnt('InterDisplay-ExtraBold.otf', 64), (*WHITE, int(255*k)), 7)
def extra(c, dr, t):
    k = win(t, 0, S['tomb'] - 0.12, 0.05, 0.15)
    if k:
        slam(c, dr, t, 0.0, (W/2, 360), 'HONEY', 150, GOLD, k)
        slam(c, dr, t, 0.45, (W/2, 480), 'CAN LAST', 96, WHITE, k)
        slam(c, dr, t, 0.95, (W/2, 590), '3,000 YEARS', 112, GOLD, k)
    # tomb: count-up
    a = S['tomb'] + 0.3; k = win(t, a, S['water'] - 0.25)
    if k:
        n = int(round(3000*eout(min(1, (t-a)/1.8))))
        c.text(dr, (W/2, 400), f'{n:,} yrs', fnt('InterDisplay-Black.otf', 150), (*GOLD, int(255*k)), 10, label='3000')
        c.text(dr, (W/2, 520), 'ancient Egyptian tombs', fnt('InterDisplay-ExtraBold.otf', 60), (*WHITE, int(255*k)), 7)
    c.chip(dr, t, 'Still edible ✓', S['tomb'] + 3.0, S['water'] - 0.25, y=640)
    big(c, dr, t, S['water'] + 0.9, S['water'] + 3.5, '17%', 'water')
    tg = S['water'] + 3.6
    c.chip(dr, t, 'Germs dry out', tg + 1.0, S['acid'] - 0.25)
    big(c, dr, t, S['acid'] + 0.2, S['bee'] - 0.25, 'pH ≈ 3.9', '≈ orange juice')
    big(c, dr, t, S['bee'] + 1.6, S['bee'] + 3.6, 'H₂O₂', 'hydrogen peroxide')
    c.chip(dr, t, 'Built-in germ killer', S['bee'] + 3.7, S['crystal'] - 0.25)
    c.chip(dr, t, 'Cloudy ≠ spoiled', S['crystal'] + 2.2, S['crystal'] + 4.3)
    c.chip(dr, t, 'Warm water bath', S['crystal'] + 4.4, S['cta'] - 0.25)
    c.nudge(dr, t, E['water'] - 0.3, 'Send to a honey lover ↗')
    c.cta(dr, t, S['cta'], [('send', 'SEND it'), ('save', 'SAVE it')])
C.extra = extra
src = lambda fi: f'{D}/frames/f_{fi:04d}.jpg'
if sys.argv[1] == 'stills': C.stills([float(x) for x in sys.argv[2].split(',')], lambda fi: f'{D}/st/still_{sys.argv[3]}.jpg', f'{D}/comp')
else: C.video(src, sys.argv[2])
