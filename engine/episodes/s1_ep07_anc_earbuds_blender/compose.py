# S1 ep07 noise-cancelling earbuds. Composite Blender frames (540x960) -> 1080x1920 with crisp overlays: hook title, paid toast, labels,
# karaoke captions, blinking mid nudge, end CTA card. Safe-zone checked. Pipes to ffmpeg.
# usage: compose.py video | compose.py stills t1,t2,...
import json, math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
WORK = os.environ.get('WORK', '/home/claude/anc')
VO = json.load(open(f'{WORK}/vo.json')); LINES = VO['lines']; L = {l['key']: l for l in LINES}; S = {k: L[k]['start'] for k in L}
T = VO['total']; FPS = 24; NF = int(math.ceil(T*FPS))
W, H = 1080, 1920
FD = '/usr/share/fonts/opentype/inter/'
def fnt(n, s): return ImageFont.truetype(FD+n, s)
F_HOOK = fnt('InterDisplay-Black.otf', 132); F_HOOK2 = fnt('InterDisplay-ExtraBold.otf', 92)
F_CAP = fnt('Inter-ExtraBold.otf', 54); F_LAB = fnt('InterDisplay-ExtraBold.otf', 60); F_SMALL = fnt('Inter-Bold.otf', 40)
F_BIG = fnt('InterDisplay-Black.otf', 260); F_CTA = fnt('InterDisplay-Black.otf', 70)
AMBER = (255, 150, 40); WHITE = (255, 255, 255); INK = (12, 13, 18); GREEN = (40, 220, 110); CYAN = (60, 190, 255); RED = (255, 80, 80); PINK = (255, 100, 190)
SAFE = (65, 269, 1015, 1248)
BOXES = []
def ease(x): x = min(1, max(0, x)); return x*x*(3-2*x)
def eout(x): x = min(1, max(0, x)); return 1-(1-x)**3
def eback(x, s=1.6): x = min(1, max(0, x)); x -= 1; return x*x*((s+1)*x+s)+1
def win(t, a, b, fi=0.25, fo=0.25):
    if t < a or t > b: return 0
    return min(eout((t-a)/fi), eout((b-t)/fo))

def text_c(d, xy, s, f, fill, stroke=6, anchor='mm', label=None):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
    bb = d.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke); BOXES.append((label or s, bb)); return bb

def overlay(t):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    # ---- hook (payoff first)
    k = win(t, 0.0, S['mic']-0.1, 0.12, 0.3)
    if k:
        dy = (1-eback(min(1, t/0.35)))*-60; al = int(255*k)
        text_c(d, (W/2, 360+dy), 'Earbuds make', F_HOOK2, (255, 255, 255, al), 7)
        text_c(d, (W/2, 480+dy), 'NOISE', F_HOOK, (*AMBER, al), 9)
        if t > 0.9:
            k2 = eback(min(1, (t-0.9)/0.3))
            f2 = fnt('InterDisplay-ExtraBold.otf', max(10, int(76*k2)))
            text_c(d, (W/2, 590), 'to make silence.', f2, (*CYAN, al), 7, label='to make silence.')
    def chip(txt, a, b, col=AMBER, y=360, f=F_LAB):
        k = win(t, a, b, 0.2, 0.2)
        if not k: return
        s = 0.85 + 0.15*eback(min(1, (t-a)/0.3))
        fz = fnt('InterDisplay-ExtraBold.otf', int(f.size*s))
        tw = d.textlength(txt, font=fz); pad = 34
        x0 = W/2 - tw/2 - pad; y0 = y - 50*s
        d.rounded_rectangle([x0, y0, x0+tw+2*pad, y0+100*s], int(30*s), fill=(*INK, int(215*k)), outline=(*col, int(255*k)), width=4)
        d.text((W/2, y0+50*s), txt, font=fz, fill=(*col, int(255*k)), anchor='mm')
        BOXES.append((txt, (x0, y0, x0+tw+2*pad, y0+100*s)))
    chip('Outer mic hears the hum', S['mic']+2.4, S['flip']-0.1)
    # flip: legend noise / anti-noise
    k = win(t, S['flip']+0.5, S['cancel']+2.0)
    if k:
        al = int(255*k); x0, y0, x1 = 170, 300, W-170
        d.rounded_rectangle([x0, y0, x1, y0+120], 34, fill=(*INK, int(215*k)))
        d.line([(x0+40, y0+60), (x0+120, y0+60)], fill=(*AMBER, al), width=14)
        d.text((x0+140, y0+60), 'noise', font=F_LAB, fill=(*WHITE, al), anchor='lm')
        d.line([(x0+390, y0+60), (x0+470, y0+60)], fill=(*CYAN, al), width=14)
        d.text((x0+490, y0+60), 'flipped', font=F_LAB, fill=(*WHITE, al), anchor='lm')
        BOXES.append(('legend', (x0, y0, x1, y0+120)))
    chip('Peak  →  dip', S['flip']+2.2, S['cancel']-0.1, col=CYAN, y=490)
    # cancel: big SILENCE
    k = win(t, S['cancel']+2.6, S['fast']-0.05, 0.15, 0.25)
    if k:
        s = eback(min(1, (t-S['cancel']-2.6)/0.35)); al = int(255*k)
        text_c(d, (W/2, 500), 'SILENCE', F_HOOK.font_variant(size=max(10, int(150*s))), (255, 255, 255, al), 9, label='SILENCE')
    # fast: late vs on time
    chip('1000s of times a second', S['fast']+0.2, S['fast']+1.2, col=WHITE)
    chip('A bit late = noise leaks', S['fast']+1.2, S['fast']+3.0, col=RED)
    chip('On time = flat', S['fast']+3.6, S['inside']-0.1, col=GREEN)
    chip('Inner mic fixes the rest', S['inside']+0.4, S['low']-0.1, col=CYAN)
    chip('Low hum → cancelled', S['low']+0.6, S['origin']-0.1, col=AMBER, y=330)
    chip('Voices → blocked by tip', S['low']+2.6, S['origin']-0.1, col=PINK, y=455)
    # origin: 1936 count-up
    k = win(t, S['origin']+0.2, S['cta']-0.1, 0.2, 0.3)
    if k:
        n = int(round(1900 + 36*eout(min(1, (t-S['origin']-0.2)/1.0)))); al = int(255*k)
        text_c(d, (W/2, 440), str(n), F_BIG, (*AMBER, al), 10, label='1936')
        if t > S['origin']+3.0:
            text_c(d, (W/2, 610), "patent → pilots' headsets", F_HOOK2.font_variant(size=58), (*WHITE, al), 6, label='pilots')
    # ---- mid nudge (~40%), big + blinking, 2.6 s
    a = S['fast']+0.3; b = a+2.8; k = win(t, a, b, 0.2, 0.25)
    if k:
        blink = 0.75 + 0.25*(0.5+0.5*math.cos((t-a)*2*math.pi*2.2))
        s = eback(min(1, (t-a)/0.35))
        bw, bh = int(760*s), int(120*s); x0 = 110 + (760-bw)/2; y0 = 1110 + (120-bh)/2
        d.rounded_rectangle([x0, y0, x0+bw, y0+bh], int(60*s), fill=(*AMBER, int(250*k*blink)))
        if s > 0.6:
            d.text((x0+bw/2, y0+bh/2), 'Send to an earbud addict ↗', font=fnt('InterDisplay-ExtraBold.otf', int(54*s)), fill=(*INK, int(255*k)), anchor='mm')
        BOXES.append(('nudge', (x0, y0, x0+bw, y0+bh)))
    # ---- end CTA card (last ~5 s)
    a = S['cta']; k = win(t, a, T, 0.3, 0.2)
    if k:
        s = eback(min(1, (t-a)/0.4))
        pulse = 1 + 0.04*math.sin((t-a)*2*math.pi*1.6)
        cw, ch = 820*s*pulse, 330*s*pulse; x0 = W/2-cw/2; y0 = 640-ch/2+60
        d.rounded_rectangle([x0, y0, x0+cw, y0+ch], int(46*s), fill=(*INK, int(230*k)), outline=(*AMBER, int(255*k)), width=5)
        if s > 0.7:
            blink = int(255*k*(0.6+0.4*(0.5+0.5*math.cos((t-a)*2*math.pi*1.8))))
            # save icon (bookmark) + send icon (paper plane) drawn
            bx, by = x0+120, y0+105
            d.polygon([(bx-30, by-45), (bx+30, by-45), (bx+30, by+45), (bx, by+20), (bx-30, by+45)], fill=(*AMBER, blink))
            d.text((bx+70, by), 'SAVE it', font=F_CTA, fill=(*WHITE, int(255*k)), anchor='lm')
            px, py = x0+120, y0+235
            d.polygon([(px-40, py+5), (px+40, py-38), (px+12, py+40), (px+2, py+12)], fill=(*AMBER, blink))
            d.text((px+70, py), 'SEND it', font=F_CTA, fill=(*WHITE, int(255*k)), anchor='lm')
        BOXES.append(('cta', (x0, y0, x0+cw, y0+ch)))
    # ---- karaoke captions
    for l in LINES:
        if l['start']-0.05 <= t <= l['end']+0.2:
            words = l['text'].split(); allrows, r = [], []
            for wd in words:
                if len(' '.join(r+[wd])) > 22 and r: allrows.append(r); r = []
                r.append(wd)
            allrows.append(r)
            chunks = [allrows[i:i+2] for i in range(0, len(allrows), 2)]
            clen = lambda c: sum(len(' '.join(x)) for x in c)
            tot = sum(clen(c) for c in chunks); dur = l['end']-l['start']; acc = 0
            for c in chunks:
                cl = clen(c); c0 = l['start'] + dur*acc/tot; c1 = l['start'] + dur*(acc+cl)/tot; acc += cl
                if c0-0.05 <= t <= (c1 if c is not chunks[-1] else l['end']+0.2):
                    rows = c
                    p = (t-c0)/max(0.01, c1-c0); nw = sum(len(x) for x in rows); cut = p*nw
                    lh = 70; ytop = 1345 - lh*len(rows)/2
                    widths = [d.textlength(' '.join(x), font=F_CAP) for x in rows]
                    mw = max(widths); bx0 = max(120, W/2-mw/2-34) - 0; bx1 = min(920, W/2+mw/2+34)
                    d.rounded_rectangle([bx0, ytop-14, bx1, ytop+lh*len(rows)+10], 28, fill=(*INK, 200))
                    BOXES.append(('caption', (bx0, ytop-14, bx1, ytop+lh*len(rows)+10)))
                    seen = 0
                    for ri, row in enumerate(rows):
                        x = W/2 - widths[ri]/2; y = ytop + ri*lh + lh/2
                        for wd in row:
                            col = AMBER if seen <= cut < seen+len(wd) else WHITE
                            d.text((x, y), wd, font=F_CAP, fill=col, anchor='lm'); x += d.textlength(wd+' ', font=F_CAP); seen += len(wd)
                    break
    return ov

VIG = None
def frame(t):
    global VIG
    fi = min(NF, int(t*FPS)+1)
    p = f'{WORK}/frames/f_{fi:04d}.jpg'
    im = (Image.open(p) if os.path.exists(p) else Image.open(sorted(__import__('glob').glob(f'{WORK}/stills/*.jpg'))[0])).convert('RGB').resize((W, H), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if VIG is None:
        v = Image.radial_gradient('L').resize((W, H)); VIG = v.point(lambda x: int(255 - 0.35*x))
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), VIG)
    im.paste(overlay(t), (0, 0), overlay(t)) if False else None
    ov = overlay(t); im = im.convert('RGBA'); im.alpha_composite(ov); return im.convert('RGB')

def check():
    bad = []
    for lab, (x0, y0, x1, y1) in BOXES:
        if lab == 'caption':
            if x0 < 119 or x1 > 921 or y1 > 1440: bad.append((lab, (int(x0), int(y0), int(x1), int(y1))))
            continue
        if x0 < SAFE[0]-1 or x1 > SAFE[2]+1 or y0 < SAFE[1]-1 or y1 > SAFE[3]+1: bad.append((lab, (int(x0), int(y0), int(x1), int(y1))))
        elif y1 > 900 and x1 > 921: bad.append(('rail:'+lab, (int(x0), int(y0), int(x1), int(y1))))
    return bad

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        os.makedirs(f'{WORK}/comp', exist_ok=True)
        for ts in sys.argv[2].split(','):
            BOXES.clear(); t = float(ts); im = frame(t); im.save(f'{WORK}/comp/c_{t:05.2f}.jpg', quality=90)
            print(t, check())
    else:
        out = sys.argv[2]
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-i', f'{WORK}/mix.wav', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                               '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        bad_all = set()
        for f in range(NF):
            BOXES.clear(); t = f/FPS; ff.stdin.write(frame(t).tobytes())
            if f % 6 == 0:
                for b in check(): bad_all.add(b[0])
        ff.stdin.close(); ff.wait(); print('safe-zone issues:', bad_all or 'none')
