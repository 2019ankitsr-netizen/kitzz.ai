import sys, math; sys.path.insert(0, '/home/claude/bk')
from kit import *
D = '/home/claude/s2'
TH = dict(accent=(255, 150, 40), chip_bg=(60, 35, 25), chip_font=fnt('InterDisplay-ExtraBold.otf', 56), nudge_bg=(255, 150, 40), nudge_ink=(60, 35, 25),
          nudge_font=fnt('InterDisplay-ExtraBold.otf', 52), card_bg=(60, 35, 25), card_ink=(255, 248, 235), cta_font=fnt('InterDisplay-Black.otf', 62),
          cap_font=fnt('Inter-ExtraBold.otf', 52), cap_bg=(60, 35, 25), who_font=fnt('Inter-Black.otf', 32),
          who_cols={'TARA': (110, 220, 225), 'BABLU': (255, 170, 60)})
C = Comp(D, 12, TH); S = C.S; E = C.E
def extra(c, dr, t):
    k = win(t, 0.0, S['t1'] - 0.1, 0.1, 0.2)
    if k:
        c.text(dr, (W/2, 340), 'AI KI KAHANI · PART 4', fnt('InterDisplay-ExtraBold.otf', 44), (255, 248, 235, int(255*k)), 5)
        s = eback(min(1, t/0.3))
        c.text(dr, (W/2, 450), '"Tara, tum sochti', fnt('InterDisplay-Black.otf', max(8, int(84*s))), (255, 150, 40, int(255*k)), 8, label='h1')
        c.text(dr, (W/2, 550), 'kaise ho?"', fnt('InterDisplay-Black.otf', max(8, int(84*s))), (255, 150, 40, int(255*k)), 8, label='h2')
    c.chip(dr, t, 'Agla shabd = andaaza', S['t1'] + 1.2, S['b1'] - 0.05)
    c.chip(dr, t, 'Agla shabd?', S['chai'] + 2.2, E['chai'] + 0.1, y=330)
    k = win(t, E['chai'] + 0.4, S['chain'] - 0.3)
    if k:
        c.text(dr, (W/2, 330), 'Sabse zyada aane wala', fnt('InterDisplay-ExtraBold.otf', 56), (255, 248, 235, int(255*k)), 7, label='win1')
        c.text(dr, (W/2, 400), 'shabd jeet-ta hai', fnt('InterDisplay-ExtraBold.otf', 56), (255, 150, 40, int(255*k)), 7, label='win2')
    k = win(t, E['chai'] + 0.4, S['chain'] - 0.3)
    if k: c.text(dr, (W/2, 460), '(example numbers)', fnt('Inter-Bold.otf', 32), (255, 248, 235, int(200*k)), 4, label='ex')
    c.chip(dr, t, 'Shabd → shabd → jawaab', S['chain'] + 1.0, S['b3'] - 0.1, y=330)
    c.chip(dr, t, 'Zaroori baatein? JAANCH lo', S['t3'] + 2.4, S['cliff'] - 0.2, col=(255, 110, 90), y=330)
    k = win(t, S['cliff'] + 2.5, S['cta'] - 0.05)
    if k: c.text(dr, (W/2, 350), 'Ek tasveer jo kabhi kheenchi hi nahi gayi…', fnt('InterDisplay-ExtraBold.otf', 44), (255, 248, 235, int(255*k)), 6, label='cliff')
    c.nudge(dr, t, S['t2'] + 2.0, 'Send to your chai-biscuit dost ↗')
    c.cta(dr, t, S['cta'], [('follow', 'FOLLOW for Part 5'), ('send', 'SEND to that dost')])
C.extra = extra
src = lambda fi: f'{D}/frames/f_{fi:04d}.jpg'
if sys.argv[1] == 'stills':
    import glob
    st = sorted(glob.glob(f'{D}/st1/still_*.jpg'))
    C.stills([float(x) for x in sys.argv[2].split(',')], lambda fi: st[min(len(st)-1, int(fi/12/6))], f'{D}/comp')
else: C.video(src, sys.argv[2], out_fps=24)
