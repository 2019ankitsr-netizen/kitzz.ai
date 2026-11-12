import sys, math; sys.path.insert(0, '/home/claude/bk')
from kit import *
D = '/home/claude/s4'
TH = dict(accent=(255, 214, 0), chip_bg=(20, 18, 30), chip_font=fnt('InterDisplay-ExtraBold.otf', 60), nudge_bg=(255, 214, 0), nudge_ink=(20, 18, 30),
          nudge_font=fnt('InterDisplay-ExtraBold.otf', 54), card_bg=(20, 18, 30), card_ink=(255, 255, 255), cta_font=fnt('InterDisplay-Black.otf', 66),
          cap_font=fnt('Inter-ExtraBold.otf', 56), cap_bg=(20, 18, 30), who_font=fnt('Inter-Bold.otf', 34))
C = Comp(D, 24, TH); S = C.S
def extra(c, dr, t):
    # kinetic hook: words slam in
    k = win(t, 0, S['why'] - 0.12, 0.05, 0.15)
    if k:
        words = [('EVERY', 0.0, (255, 255, 255)), ('BANANA', 0.35, (255, 214, 0)), ('IS', 0.75, (255, 255, 255)), ('RADIOACTIVE', 1.0, (255, 255, 255))]
        ys = [360, 470, 580, 580]
        for (w, t0, col), y in zip(words, ys):
            if t < t0: continue
            s = eback(min(1, (t-t0)/0.18), 2.4); f = fnt('InterDisplay-Black.otf', max(8, int((150 if w == 'BANANA' else 112)*s)))
            if w == 'IS': c.text(dr, (W/2 - 320, y), w, f.font_variant(size=max(8, int(84*s))), (*col, int(255*k)), 9, 'lm')
            elif w == 'RADIOACTIVE': c.text(dr, (W/2 - 175, y), w, f.font_variant(size=max(8, int(84*s))), (*col, int(255*k)), 9, 'lm')
            else: c.text(dr, (W/2, y), w, f, (*col, int(255*k)), 9)
    c.chip(dr, t, 'Potassium-40', S['why'] + 2.3, S['dose'] - 0.2)
    # dose counter
    k = win(t, S['dose'] + 0.3, S['xray'] - 0.2)
    if k:
        c.text(dr, (W/2, 400), '0.1 µSv', fnt('InterDisplay-Black.otf', 150), (255, 214, 0, int(255*k)), 10)
        c.text(dr, (W/2, 520), 'per banana', fnt('InterDisplay-ExtraBold.otf', 64), (255, 255, 255, int(255*k)), 7)
    # 50 count-up
    k = win(t, S['xray'] + 0.1, S['safe'] - 0.2)
    if k:
        n = int(round(50*eout(min(1, (t - S['xray'] - 0.1)/1.9))))
        c.text(dr, (W/2, 400), f'{n} 🍌'.replace(' 🍌', ''), fnt('InterDisplay-Black.otf', 190), (255, 214, 0, int(255*k)), 11, label='50')
        c.text(dr, (W/2, 540), '= 1 dental X-ray', fnt('InterDisplay-ExtraBold.otf', 66), (255, 255, 255, int(255*k)), 7)
    c.chip(dr, t, "Doesn't build up", S['safe'] + 0.6, S['unit'] - 0.2)
    k = win(t, S['unit'] + 2.0, S['cta'] - 0.2)
    if k:
        s = eback(min(1, (t - S['unit'] - 2.0)/0.3))
        f = fnt('InterDisplay-Black.otf', max(8, int(84*s)))
        c.text(dr, (W/2, 360), 'BANANA', f, (255, 214, 0, int(255*k)), 9)
        c.text(dr, (W/2, 455), 'EQUIVALENT DOSE', f.font_variant(size=max(8, int(72*s))), (255, 255, 255, int(255*k)), 8)
    c.nudge(dr, t, S['xray'] + 2.4, 'Send to a banana lover ↗')
    c.cta(dr, t, S['cta'], [('send', 'SEND it'), ('save', 'SAVE it')])
C.extra = extra
src = lambda fi: f'{D}/frames/f_{fi:04d}.jpg'
if sys.argv[1] == 'stills': C.stills([float(x) for x in sys.argv[2].split(',')], lambda fi: f'{D}/frames/f_{min(fi, 14):04d}.jpg', f'{D}/comp')
else: C.video(src, sys.argv[2])
