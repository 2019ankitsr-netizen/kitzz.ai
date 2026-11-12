"""Blender-series kit for @kitzz.ai: voice lines -> vo.wav/vo.json, frame compositor with crisp overlays
(captions with speaker label, mid nudge, end CTA, safe-zone check) and a mux step.
Each reel dir has: lines (list of dicts), scene.py (bpy), extra overlay fn, music fn."""
import json, math, os, subprocess, sys
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/claude/kitzz.ai/engine')
W, H = 1080, 1920
SAFE = (65, 269, 1015, 1248)
CAP_Y = 1345          # captions sit low, under the subject (box ~1270-1420, left of the icon rail)
CAP_MAX = 1440
FD = '/usr/share/fonts/opentype/inter/'
HD = '/home/claude/fonts/'
def fnt(n, s):
    p = HD + n if n.startswith(('Hind', 'Yatra')) else FD + n
    return ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.RAQM)
def ease(x): x = min(1, max(0, x)); return x*x*(3-2*x)
def eout(x): x = min(1, max(0, x)); return 1-(1-x)**3
def eback(x, s=1.6): x = min(1, max(0, x)); x -= 1; return x*x*((s+1)*x+s)+1
def win(t, a, b, fi=0.25, fo=0.25):
    if t < a or t > b: return 0
    return min(eout((t-a)/fi), eout((b-t)/fo))

# ---------------- voice ----------------
def make_voice(d, lines, lead=0.15, tail=0.6):
    """lines: dict(key, voice, say, cap, speed, pitch, tone, lang, gap, pre, who)"""
    import audio as A
    out, meta, t = [np.zeros(int(A.SR*lead), np.float32)], [], lead
    for l in lines:
        if l.get('pre'): out.append(np.zeros(int(A.SR*l['pre']), np.float32)); t += l['pre']
        a = A.say(l['say'], l['voice'], speed=l.get('speed', 1.08), lang=l.get('lang', 'en-us'), pitch=l.get('pitch', 0), tone=l.get('tone', 'warm'))
        meta.append(dict(key=l['key'], text=l.get('cap') or l['say'].replace('|', ''), who=l.get('who'), start=round(t, 3), end=round(t+len(a)/A.SR, 3)))
        g = l.get('gap', 0.28); out += [a, np.zeros(int(A.SR*g), np.float32)]; t += len(a)/A.SR + g
    out.append(np.zeros(int(A.SR*tail), np.float32)); t += tail
    sf.write(f'{d}/vo.wav', np.concatenate(out), A.SR)
    json.dump(dict(lines=meta, total=round(t, 3)), open(f'{d}/vo.json', 'w'), indent=1, ensure_ascii=False)
    for m in meta: print(m['key'], m['start'], m['end'])
    print('total', round(t, 2)); return meta

# ---------------- music helpers ----------------
SR = 44100
def put(buf, x, t, g=1.0):
    i = int(t*SR)
    if i >= len(buf) or i < 0: return
    x = x[:len(buf)-i]; buf[i:i+len(x)] += x*g
def mix_and_master(d, music, sfx, music_gain=0.75, duck=0.42):
    from scipy.signal import resample_poly
    VO = json.load(open(f'{d}/vo.json')); N = len(music)
    v, vsr = sf.read(f'{d}/vo.wav'); v = resample_poly(v, SR, vsr)[:N]; v = np.pad(v, (0, N-len(v)))
    env = np.ones(N)
    for l in VO['lines']:
        a, b = int((l['start']-0.15)*SR), int((l['end']+0.15)*SR); env[max(0, a):b] = duck
    k = int(0.12*SR); env = np.convolve(env, np.ones(k)/k, mode='same')
    mix = v + music*env*music_gain + sfx*0.8
    st = np.stack([mix + music*0.03, mix - music*0.03], 1); st = st/np.max(np.abs(st))*0.9
    sf.write(f'{d}/mix_raw.wav', st, SR)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{d}/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '44100', f'{d}/mix.wav'], check=True)
    import pyloudnorm as pyln
    a, _ = sf.read(f'{d}/mix.wav'); print('LUFS', round(pyln.Meter(SR).integrated_loudness(a), 2))

# ---------------- compositor ----------------
class Comp:
    def __init__(self, d, fps, theme):
        self.d = d; self.fps = fps; self.th = theme
        self.VO = json.load(open(f'{d}/vo.json')); self.L = {l['key']: l for l in self.VO['lines']}
        self.S = {k: v['start'] for k, v in self.L.items()}; self.E = {k: v['end'] for k, v in self.L.items()}
        self.T = self.VO['total']; self.NF = int(math.ceil(self.T*fps)); self.BOX = []; self.extra = None; self.post = None
    def box(self, lab, bb): self.BOX.append((lab, bb))
    def text(self, dr, xy, s, f, fill, stroke=6, anchor='mm', sfill=(0, 0, 0), label=None):
        dr.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)
        bb = dr.textbbox(xy, s, font=f, anchor=anchor, stroke_width=stroke); self.box(label or s, bb); return bb
    def chip(self, dr, t, txt, a, b, y=360, col=None, f=None, bg=None):
        th = self.th; col = col or th['accent']; f = f or th['chip_font']; bg = bg or th['chip_bg']
        k = win(t, a, b, 0.2, 0.2)
        if not k: return
        s = 0.85 + 0.15*eback(min(1, (t-a)/0.3)); fz = f.font_variant(size=int(f.size*s))
        tw = dr.textlength(txt, font=fz); pad = 34
        x0 = W/2-tw/2-pad; y0 = y-50*s
        dr.rounded_rectangle([x0, y0, x0+tw+2*pad, y0+100*s], int(30*s), fill=(*bg, int(225*k)), outline=(*col, int(255*k)), width=4)
        dr.text((W/2, y0+50*s), txt, font=fz, fill=(*col, int(255*k)), anchor='mm')
        self.box(txt, (x0, y0, x0+tw+2*pad, y0+100*s))
    def nudge(self, dr, t, a, txt, dur=2.8):
        th = self.th; b = a+dur; k = win(t, a, b, 0.2, 0.25)
        if not k: return
        blink = 0.75+0.25*(0.5+0.5*math.cos((t-a)*2*math.pi*2.2)); s = eback(min(1, (t-a)/0.35))
        bw, bh = int(780*min(s, 1.0)), int(120*s); x0 = 110+(780-bw)/2; y0 = 1110+(120-bh)/2
        dr.rounded_rectangle([x0, y0, x0+bw, y0+bh], int(60*s), fill=(*th['nudge_bg'], int(250*k*blink)))
        if s > 0.6:
            f = th['nudge_font'].font_variant(size=int(th['nudge_font'].size*s))
            dr.text((x0+bw/2, y0+bh/2), txt, font=f, fill=(*th['nudge_ink'], int(255*k)), anchor='mm')
        self.box('nudge', (x0, y0, x0+bw, y0+bh))
    def cta(self, dr, t, a, rows):
        """rows: list of (icon, text) icon in save/send/comment/follow/tag"""
        th = self.th; k = win(t, a, self.T, 0.3, 0.2)
        if not k: return
        s = eback(min(1, (t-a)/0.4)); pulse = 1+0.04*math.sin((t-a)*2*math.pi*1.6)
        rh = 125; cw, ch = 860*s*pulse, (rh*len(rows)+80)*s*pulse; x0 = W/2-cw/2; y0 = 700-ch/2
        dr.rounded_rectangle([x0, y0, x0+cw, y0+ch], int(46*s), fill=(*th['card_bg'], int(232*k)), outline=(*th['accent'], int(255*k)), width=5)
        if s > 0.7:
            blink = int(255*k*(0.6+0.4*(0.5+0.5*math.cos((t-a)*2*math.pi*1.8))))
            for i, (ic, tx) in enumerate(rows):
                cx, cy = x0+105, y0+40*s+rh*s*(i+0.5)
                icon(dr, ic, cx, cy, (*th['accent'], blink))
                dr.text((cx+70, cy), tx, font=th['cta_font'], fill=(*th['card_ink'], int(255*k)), anchor='lm')
        self.box('cta', (x0, y0, x0+cw, y0+ch))
    def captions(self, dr, t):
        th = self.th; F = th['cap_font']
        for l in self.VO['lines']:
            if not (l['start']-0.05 <= t <= l['end']+0.2): continue
            words = l['text'].split(); rows, r = [], []
            for wd in words:
                if len(' '.join(r+[wd])) > th.get('cap_chars', 22) and r: rows.append(r); r = []
                r.append(wd)
            rows.append(r); chunks = [rows[i:i+2] for i in range(0, len(rows), 2)]
            cl = lambda c: sum(len(' '.join(x)) for x in c); tot = sum(cl(c) for c in chunks); dur = l['end']-l['start']; acc = 0
            for c in chunks:
                c0 = l['start']+dur*acc/tot; c1 = l['start']+dur*(acc+cl(c))/tot; acc += cl(c)
                if not (c0-0.05 <= t <= (c1 if c is not chunks[-1] else l['end']+0.2)): continue
                p = (t-c0)/max(0.01, c1-c0); nw = sum(len(w) for x in c for w in x); cut = p*nw
                lh = th.get('cap_lh', 70); ytop = CAP_Y-lh*len(c)/2
                widths = [dr.textlength(' '.join(x), font=F) for x in c]; mw = max(widths)
                bx0 = max(120, W/2-mw/2-34); bx1 = min(920, W/2+mw/2+34)
                dr.rounded_rectangle([bx0, ytop-14, bx1, ytop+lh*len(c)+10], 28, fill=(*th['cap_bg'], 205))
                self.box('caption', (bx0, ytop-14, bx1, ytop+lh*len(c)+10))
                if l.get('who'):
                    wf = th['who_font']; ww = dr.textlength(l['who'], font=wf)
                    col = th.get('who_cols', {}).get(l['who'], th['accent'])
                    dr.rounded_rectangle([bx0+10, ytop-62, bx0+10+ww+36, ytop-14], 16, fill=(*col, 240))
                    dr.text((bx0+28, ytop-38), l['who'], font=wf, fill=(*th['cap_bg'], 255), anchor='lm')
                    self.box('who', (bx0+10, ytop-62, bx0+10+ww+36, ytop-14))
                seen = 0
                for ri, row in enumerate(c):
                    x = W/2-widths[ri]/2; y = ytop+ri*lh+lh/2
                    for wd in row:
                        col = th['accent'] if seen <= cut < seen+len(wd) else (255, 255, 255)
                        dr.text((x, y), wd, font=F, fill=col, anchor='lm'); x += dr.textlength(wd+' ', font=F); seen += len(wd)
                break
    def frame(self, t, src):
        fi = min(self.NF, int(t*self.fps)+1)
        im = Image.open(src(fi)).convert('RGB').resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
        if self.post: im = self.post(im, t)
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
        if self.extra: self.extra(self, dr, t)
        self.captions(dr, t)
        im = im.convert('RGBA'); im.alpha_composite(ov); return im.convert('RGB')
    def check(self):
        bad = []
        for lab, (x0, y0, x1, y1) in self.BOX:
            if lab in ('caption', 'who'):
                if x0 < 119 or x1 > 921 or y1 > CAP_MAX: bad.append(lab)
                continue
            if x0 < SAFE[0]-1 or x1 > SAFE[2]+1 or y0 < SAFE[1]-1 or y1 > SAFE[3]+1: bad.append(lab)
            elif y1 > 900 and x1 > 921: bad.append('rail:'+lab)
        return bad
    def stills(self, ts, src, outdir):
        os.makedirs(outdir, exist_ok=True)
        for t in ts:
            self.BOX.clear(); self.frame(t, src).save(f'{outdir}/c_{t:05.2f}.jpg', quality=90); print(t, self.check())
    def video(self, src, out, out_fps=None):
        r = str(self.fps)
        vf = ['-vf', f'fps={out_fps}'] if out_fps else []
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', r, '-i', '-',
                               '-i', f'{self.d}/mix.wav', *vf, '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                               '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        bad = set()
        for f in range(self.NF):
            self.BOX.clear(); t = f/self.fps; ff.stdin.write(self.frame(t, src).tobytes())
            if f % 4 == 0: bad |= set(self.check())
        ff.stdin.close(); ff.wait(); print('safe-zone issues:', bad or 'none')

def icon(dr, kind, cx, cy, col):
    if kind == 'save':
        dr.polygon([(cx-30, cy-45), (cx+30, cy-45), (cx+30, cy+45), (cx, cy+20), (cx-30, cy+45)], fill=col)
    elif kind == 'send':
        dr.polygon([(cx-40, cy+5), (cx+40, cy-38), (cx+12, cy+40), (cx+2, cy+12)], fill=col)
    elif kind == 'comment':
        dr.rounded_rectangle([cx-42, cy-36, cx+42, cy+26], 18, fill=col); dr.polygon([(cx-20, cy+20), (cx-30, cy+44), (cx+2, cy+24)], fill=col)
    elif kind == 'follow':
        dr.ellipse([cx-18, cy-44, cx+18, cy-8], fill=col); dr.pieslice([cx-38, cy-4, cx+38, cy+66], 180, 360, fill=col)
    elif kind == 'tag':
        dr.text((cx, cy), '@', font=fnt('InterDisplay-Black.otf', 84), fill=col, anchor='mm')

def contact(video, out, n=12):
    tmp = out + '_d'; os.makedirs(tmp, exist_ok=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video], capture_output=True, text=True).stdout)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', video, '-vf', f'fps={n/dur},scale=360:640', f'{tmp}/c_%02d.png'], check=True)
    import glob
    fs = sorted(glob.glob(f'{tmp}/c_*.png'))[:n]; s = 1/3
    S = Image.new('RGB', (360*6, 640*((len(fs)+5)//6)))
    for k, f in enumerate(fs):
        im = Image.open(f).convert('RGBA'); o = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(o)
        d.rectangle([0, 0, 360, 269*s], fill=(255, 0, 0, 60)); d.rectangle([0, 1248*s, 360, 640], fill=(255, 0, 0, 60))
        d.rectangle([0, 0, 65*s, 640], fill=(255, 0, 0, 60)); d.rectangle([1015*s, 0, 360, 640], fill=(255, 0, 0, 60))
        d.rectangle([930*s, 900*s, 360, 1700*s], fill=(255, 170, 0, 70))
        im.alpha_composite(o); S.paste(im.convert('RGB'), ((k % 6)*360, (k//6)*640))
    S.save(out, quality=88)
