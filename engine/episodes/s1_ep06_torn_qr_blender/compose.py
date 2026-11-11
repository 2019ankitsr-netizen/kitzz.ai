# Composite Blender frames (540x960) -> 1080x1920 with crisp overlays: hook title, paid toast, labels,
# karaoke captions, blinking mid nudge, end CTA card. Safe-zone checked. Pipes to ffmpeg.
# usage: compose.py video | compose.py stills t1,t2,...
import json, math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
VO = json.load(open('/home/claude/qr/vo.json')); LINES = VO['lines']; L = {l['key']: l for l in LINES}; S = {k: L[k]['start'] for k in L}
T = VO['total']; FPS = 24; NF = int(math.ceil(T*FPS))
W, H = 1080, 1920
FD = '/usr/share/fonts/opentype/inter/'
def fnt(n, s): return ImageFont.truetype(FD+n, s)
F_HOOK = fnt('InterDisplay-Black.otf', 132); F_HOOK2 = fnt('InterDisplay-ExtraBold.otf', 92)
F_CAP = fnt('Inter-ExtraBold.otf', 54); F_LAB = fnt('InterDisplay-ExtraBold.otf', 60); F_SMALL = fnt('Inter-Bold.otf', 40)
F_BIG = fnt('InterDisplay-Black.otf', 260); F_CTA = fnt('InterDisplay-Black.otf', 70)
AMBER = (255, 166, 48); WHITE = (255, 255, 255); INK = (12, 13, 18); GREEN = (40, 200, 110)
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
    # ---- hook title (0 -> finder) + loop end (re-shows at the very end)
    for a, b in [(0.0, S['finder']-0.1)]:
        k = win(t, a, b, 0.12, 0.3)
        if k:
            dy = (1-eback(min(1, (t-a)/0.35)))*-60
            al = int(255*k)
            text_c(d, (W/2, 380+dy), 'TORN QR.', F_HOOK, (255, 255, 255, al), 8)
            if t > 0.55:
                k2 = eback(min(1, (t-0.55)/0.3))
                f2 = fnt('InterDisplay-ExtraBold.otf', max(10, int(92*k2)))
                text_c(d, (W/2, 515), 'Still pays.', f2, (*AMBER, al), 7, label='Still pays.')
    # ---- paid toast
    k = win(t, 1.3, S['finder']-0.1, 0.2, 0.25)
    if k:
        y = 640 - (1-eback(min(1, (t-1.3)/0.3)))*40
        bw, bh = 420, 104; x0 = W/2-bw/2
        d.rounded_rectangle([x0, y, x0+bw, y+bh], 52, fill=(*GREEN, int(240*k)))
        cx, cy = x0+60, y+bh/2
        d.ellipse([cx-32, cy-32, cx+32, cy+32], fill=(255, 255, 255, int(255*k)))
        d.line([(cx-15, cy+1), (cx-4, cy+13), (cx+17, cy-12)], fill=(*GREEN, 255), width=9, joint='curve')
        d.text((x0+110, cy), 'Paid  ₹20', font=fnt('InterDisplay-ExtraBold.otf', 56), fill=(255, 255, 255, int(255*k)), anchor='lm')
        BOXES.append(('toast', (x0, y, x0+bw, y+bh)))
    # ---- labels per beat (top band of safe zone)
    def chip(txt, a, b, col=AMBER, y=360, f=F_LAB):
        k = win(t, a, b, 0.2, 0.2)
        if not k: return
        s = 0.85 + 0.15*eback(min(1, (t-a)/0.3))
        tw = d.textlength(txt, font=f)*s; pad = 34
        fz = fnt('InterDisplay-ExtraBold.otf', int(f.size*s))
        x0 = W/2 - tw/2 - pad; y0 = y - 50*s
        d.rounded_rectangle([x0, y0, x0+tw+2*pad, y0+100*s], int(30*s), fill=(*INK, int(215*k)), outline=(*col, int(255*k)), width=4)
        d.text((W/2, y0+50*s), txt, font=fz, fill=(*col, int(255*k)), anchor='mm')
        BOXES.append((txt, (x0, y0, x0+tw+2*pad, y0+100*s)))
    chip('3 corner markers', S['finder']+1.0, S['bits']-0.1)
    # bits legend with drawn squares
    k = win(t, S['bits']+0.3, S['backup']-0.1)
    if k:
        x0, y0 = 250, 310; al = int(255*k)
        d.rounded_rectangle([x0-30, y0-20, W-x0+30, y0+120], 34, fill=(245, 243, 238, int(235*k)))
        d.rounded_rectangle([x0+10, y0+15, x0+80, y0+85], 10, fill=(10, 10, 12, al))
        d.text((x0+100, y0+50), '= 1', font=F_LAB, fill=(*INK, al), anchor='lm')
        d.rounded_rectangle([x0+310, y0+15, x0+380, y0+85], 10, fill=(255, 255, 255, al), outline=(150, 150, 150, al), width=4)
        d.text((x0+400, y0+50), '= 0', font=F_LAB, fill=(*INK, al), anchor='lm')
        BOXES.append(('bits', (x0-30, y0-20, W-x0+30, y0+120)))
    chip('Amber = backup blocks', S['backup']+1.1, S['rs']+0.2)
    chip('Reed–Solomon repair', S['rs']+0.6, S['thirty']-0.1, col=(120, 255, 170))
    # 30% count-up
    k = win(t, S['thirty']+0.3, S['origin']-0.1, 0.2, 0.3)
    if k:
        n = int(round(30*eout(min(1, (t-S['thirty']-0.3)/1.0))))
        txt = f'{n}%'; al = int(255*k)
        text_c(d, (W/2, 450), txt, F_BIG, (*AMBER, al), 10, label='30%')
        text_c(d, (W/2, 615), 'can be missing', F_HOOK2.font_variant(size=64), (*WHITE, al), 6, label='can be missing')
    chip('1994 · Japan · car parts', S['origin']+0.8, S['cta']-0.2, col=WHITE)
    # ---- mid nudge (~40%), big + blinking, 2.6 s
    a = S['backup']+2.2; b = a+2.8; k = win(t, a, b, 0.2, 0.25)
    if k:
        blink = 0.75 + 0.25*(0.5+0.5*math.cos((t-a)*2*math.pi*2.2))
        s = eback(min(1, (t-a)/0.35))
        bw, bh = int(760*s), int(120*s); x0 = 110 + (760-bw)/2; y0 = 905 + (120-bh)/2
        d.rounded_rectangle([x0, y0, x0+bw, y0+bh], int(60*s), fill=(*AMBER, int(250*k*blink)))
        if s > 0.6:
            d.text((x0+bw/2, y0+bh/2), 'Send to your chai-wala ↗', font=fnt('InterDisplay-ExtraBold.otf', int(54*s)), fill=(*INK, int(255*k)), anchor='mm')
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
                    lh = 70; ytop = 1145 - lh*len(rows)/2
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
    p = f'/home/claude/qr/frames/f_{fi:04d}.jpg'
    im = (Image.open(p) if os.path.exists(p) else Image.open('/home/claude/qr/stills/still_06.00.jpg')).convert('RGB').resize((W, H), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if VIG is None:
        v = Image.radial_gradient('L').resize((W, H)); VIG = v.point(lambda x: int(255 - 0.35*x))
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), VIG)
    im.paste(overlay(t), (0, 0), overlay(t)) if False else None
    ov = overlay(t); im = im.convert('RGBA'); im.alpha_composite(ov); return im.convert('RGB')

def check():
    bad = []
    for lab, (x0, y0, x1, y1) in BOXES:
        if x0 < SAFE[0]-1 or x1 > SAFE[2]+1 or y0 < SAFE[1]-1 or y1 > SAFE[3]+1: bad.append((lab, (int(x0), int(y0), int(x1), int(y1))))
        elif y1 > 900 and x1 > 921: bad.append(('rail:'+lab, (int(x0), int(y0), int(x1), int(y1))))
    return bad

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        os.makedirs('/home/claude/qr/comp', exist_ok=True)
        for ts in sys.argv[2].split(','):
            BOXES.clear(); t = float(ts); im = frame(t); im.save(f'/home/claude/qr/comp/c_{t:05.2f}.jpg', quality=90)
            print(t, check())
    else:
        out = sys.argv[2]
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-i', '/home/claude/qr/mix.wav', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                               '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        bad_all = set()
        for f in range(NF):
            BOXES.clear(); t = f/FPS; ff.stdin.write(frame(t).tobytes())
            if f % 6 == 0:
                for b in check(): bad_all.add(b[0])
        ff.stdin.close(); ff.wait(); print('safe-zone issues:', bad_all or 'none')
