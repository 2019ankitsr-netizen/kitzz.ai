"""Build one Hanuman Chalisa episode (Din 2..22).
usage: python3 build.py DIN OUTDIR [vo] [render]   (no step flags = all steps)
Voice: Indic Parler-TTS 'Rohit', smooth calm conversational, whole-line takes, checked against assets/ref_hook.wav.
Look: Kalamkari ink (eng.py / art.py / motifs.py). Safe zone and caption rules from the kitzz page manager.
"""
import os, sys, json, math, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, soundfile as sf
from episodes import episode, NUM

DIN = int(sys.argv[1]); OUT = os.path.abspath(sys.argv[2]); STEPS = set(sys.argv[3:]) or {'vo', 'render'}
os.makedirs(f'{OUT}/vo', exist_ok=True)
EP = episode(DIN)
KEYS = ['hook', 'save', 'recite', 'm1', 'm2', 'ins', 'cta']
def spoken(k):
    return {'save': 'इस वीडियो को सेव कर लीजिए, और मैं आपको आराम से बताता हूँ।', 'hook': EP['hook'], 'recite': EP['recite'].replace('॥', '।'), 'm1': EP['m1']['spoken'], 'm2': EP['m2']['spoken'],
            'ins': EP['ins']['spoken'], 'cta': EP['cta']}[k]
MOOD = {'recite': 'chant'}

# ------------------------------------------------------------------ voice
def make_voice():
    import torch, librosa
    from transformers import AutoTokenizer
    from parler_tts import ParlerTTSForConditionalGeneration
    REPO = "RXD03/indic-parler-tts"; torch.set_num_threads(os.cpu_count() or 2)
    m = ParlerTTSForConditionalGeneration.from_pretrained(REPO)
    tok = AutoTokenizer.from_pretrained(REPO); dtok = AutoTokenizer.from_pretrained(m.config.text_encoder._name_or_path)
    SR = m.config.sampling_rate
    BASE = "Rohit speaks in a smooth, calm and friendly conversational voice{p}, warmly explaining with gentle and natural intonation, with a very close recording that has no background noise."
    DESC = {"calm": BASE.format(p=" at a moderate pace"), "chant": BASE.format(p=" at a slow pace, reciting a devotional verse melodiously")}
    def gen(desc, text, seed):
        torch.manual_seed(seed)
        ids = dtok(desc, return_tensors='pt'); pids = tok(text, return_tensors='pt')
        with torch.no_grad():
            a = m.generate(input_ids=ids.input_ids, attention_mask=ids.attention_mask, prompt_input_ids=pids.input_ids,
                           prompt_attention_mask=pids.attention_mask).cpu().numpy().squeeze().astype(np.float32)
        idx = np.where(np.abs(a) > 0.012)[0]
        return a[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.15 * SR)]
    def feats(a, sr):
        f0, _, _ = librosa.pyin(a, fmin=60, fmax=400, sr=sr, frame_length=4096); f = f0[~np.isnan(f0)]
        return (float(np.median(f)) if len(f) else 0.0), librosa.feature.mfcc(y=a, sr=sr, n_mfcc=20).mean(1)
    ra, rsr = sf.read(f'{HERE}/assets/ref_hook.wav', dtype='float32'); ref = feats(ra, rsr)
    score = lambda f: abs(f[0] - ref[0]) / 10 + np.linalg.norm(f[1][1:] - ref[1][1:]) / 20
    rep = {}
    for k in KEYS:
        if k == 'save':
            a, sr = sf.read(f'{HERE}/assets/save.wav', dtype='float32'); sf.write(f'{OUT}/vo/save.wav', a, sr); continue
        if os.path.exists(f'{OUT}/vo/{k}.wav'): continue
        mood = MOOD.get(k, 'calm'); best = None
        for seed in (7, 21, 33):
            a = gen(DESC[mood], spoken(k), seed); f = feats(a, SR); sc = score(f)
            if best is None or sc < best[0]: best = (sc, seed, a, f)
            if abs(f[0] - ref[0]) < 9 and sc < 1.6: break
        sc, seed, a, f = best
        sf.write(f'{OUT}/vo/{k}.wav', a, SR); rep[k] = dict(seed=seed, f0=round(f[0], 1), score=round(float(sc), 2), dur=round(len(a) / SR, 2))
        print(k, rep[k], flush=True)
    json.dump(rep, open(f'{OUT}/vo/report.json', 'w'), indent=1)

if 'vo' in STEPS: make_voice()
if 'render' not in STEPS: sys.exit(0)

# ------------------------------------------------------------------ timeline
from motifs import *   # noqa  (eng/art/motifs: skia drawing)
def trimmed(k):
    v, sr = sf.read(f'{OUT}/vo/{k}.wav', dtype='float32'); idx = np.where(np.abs(v) > 0.01)[0]
    return v[max(0, idx[0] - 400): idx[-1] + 4000], sr
durs = {}
for k in KEYS:
    v, sr = trimmed(k); durs[k] = len(v) / sr
PAD0, PADE = 0.10, 0.30
D = [durs[k] + PAD0 + PADE + (0.5 if k == 'recite' else 0) for k in KEYS]
D[0] = durs['hook'] + PAD0 + 0.6; D[-1] += 1.2
START = [sum(D[:i]) for i in range(len(D))]; TOT = sum(D)

def split_caps(text, maxc=26):
    parts = [p.strip(' ,।?') for p in re.split(r'(?<=[,।?])\s+', text) if p.strip(' ,।?')]
    out = []
    for p in parts:
        if out and len(out[-1]) + len(p) + 1 <= maxc and not out[-1].endswith(('।', '?')): out[-1] += ', ' + p
        else: out.append(p)
    return out
CAPS = {k: split_caps(spoken(k)) for k in KEYS if k != 'recite'}
CAPS['save'] = ["इस वीडियो को सेव कर लीजिए", "और मैं आपको आराम से बताता हूँ"]

_G = {}
def gaps(k):
    if k not in _G:
        a, sr = trimmed(k); hop = int(sr * 0.02)
        e = np.array([np.abs(a[i:i + hop]).max() for i in range(0, len(a) - hop, hop)]) < 0.015
        g = []; i = 0
        while i < len(e):
            if e[i]:
                j = i
                while j < len(e) and e[j]: j += 1
                if (j - i) * 0.02 >= 0.16: g.append((i + j) / 2 * 0.02)
                i = j
            else: i += 1
        _G[k] = g
    return _G[k]
_CH = {}
def chunks(k, parts):
    key = (k, tuple(parts))
    if key in _CH: return _CH[key]
    d = durs[k]; tot = sum(len(x) for x in parts); b = [0.0]; t = 0
    for x in parts[:-1]:
        t += d * len(x) / tot
        g = [q for q in gaps(k) if abs(q - t) < 0.9 and q > b[-1] + 0.3]
        b.append(min(g, key=lambda q: abs(q - t)) if g else t)
    b.append(d)
    _CH[key] = [(PAD0 + b[i], PAD0 + b[i + 1], parts[i]) for i in range(len(parts))]
    return _CH[key]
def cue(k, word):
    """time (scene-local) at which `word` is spoken, by character position"""
    s = spoken(k); i = s.find(word)
    if i < 0: return 0.3
    return PAD0 + durs[k] * i / max(1, len(s)) - 0.1

BOXES = []
def rec(x0, y0, x1, y1, lab): BOXES.append((x0, y0, x1, y1, lab))

def fit_size(txt, font, size, maxw):
    while size > 30 and text_w(txt, font, size) > maxw: size -= 2
    return size

def wrap(txt, size=54, maxw=720):
    words = txt.split(' '); lines = ['']
    for w in words:
        cand = (lines[-1] + ' ' + w).strip()
        if text_w(cand, F_HB, size) > maxw and lines[-1]: lines.append(w)
        else: lines[-1] = cand
    return lines[:2]

def draw_caption(c, k, tau):
    if k not in CAPS: return
    ch = chunks(k, CAPS[k])
    for j, (a, b, x) in enumerate(ch):
        if a - 0.05 <= tau < b + (0.35 if j == len(ch) - 1 else 0):
            pop = back((tau - a) / 0.18) if tau >= a else 0
            lines = wrap(x); bw = max(text_w(l, F_HB, 54) for l in lines) + 60; lh = 70; bh = lh * len(lines) + 24; cx, cy = 510, 1150
            c.save(); c.translate(cx, cy); c.scale(0.9 + 0.1 * pop, 0.9 + 0.1 * pop)
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(-bw / 2, -bh / 2, bw / 2, bh / 2), 26, 26), skia.Paint(AntiAlias=True, Color=C(INK, 232)))
            for i, l in enumerate(lines): draw_text(c, l, 0, -bh / 2 + 12 + lh * i + lh / 2, F_HB, 54, CREAM)
            c.restore(); rec(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2, 'caption')

def headline(c, txt, tau, t0, y, size, col, maxw=860):
    a = clamp((tau - t0) / 0.15)
    if a > 0:
        size = fit_size(txt, F_Y, size, maxw)
        w, h = draw_text(c, txt, 540, y, F_Y, size, col, alpha=a, scale=0.85 + 0.15 * back((tau - t0) / 0.3), stroke=5, sfill=CREAM)
        rec(540 - w / 2, y - h / 2, 540 + w / 2, y + h / 2, 'headline')

def tag(c, txt, cx, cy, tau, t0, size=48, bg=CREAM, fg=INK, out=None, maxw=640):
    a = clamp((tau - t0) / 0.15)
    if out is not None: a *= 1 - clamp((tau - out) / 0.2)
    if a <= 0: return
    size = fit_size(txt, F_HB, size, maxw)
    sc = 0.8 + 0.2 * back((tau - t0) / 0.3)
    r = chip(c, txt, cx, cy, size, bg, fg, a, scale=sc)
    rec(cx + r.left() * max(1, sc), cy + r.top() * max(1, sc), cx + r.right() * max(1, sc), cy + r.bottom() * max(1, sc), 'chip:' + txt)

def chips_row(c, k, chips, tau, y=990, size=44):
    shown = [(t, cue(k, w)) for t, w in chips]; shown = [(t, t0) for t, t0 in shown if tau >= t0 - 0.05]
    if not shown: return
    while True:  # keep the newest chips that fit inside x 100..900
        ws = [text_w(t, F_HB, size) + 68 for t, _ in shown]; tot = sum(ws) + 18 * (len(ws) - 1)
        if tot <= 800 or len(shown) == 1: break
        shown = shown[1:]
    x = 500 - tot / 2
    for (t, t0), w in zip(shown, ws):
        tag(c, t, x + w / 2, y, tau, t0, size=size, bg=GOLDL, maxw=780); x += w + 18

def card(c, k, tau):
    lines = EP['verses']; Ink(c, tau).shape(rrect(110, 470, 970, 900, 30), 0.0, 0.45, fill=CREAM, w=6)
    Ink(c, tau).shape(rrect(130, 490, 950, 880, 22), 0.1, 0.5, w=4, col=RED)
    draw_text(c, EP['card_title'], 540, 540, F_HB, 40, RED, alpha=clamp((tau - 0.3) / 0.3))
    size = min(fit_size(l, F_Y, 60, 780) for l in lines)
    ch = [(a + 0.25, b + 0.25, x) for a, b, x in chunks(k, list(lines))]
    for j, (a, b, x) in enumerate(ch):
        col = (RED if tau < b else INK) if tau >= a - 0.1 else FADED
        draw_text(c, x, 540, 610 + j * 78, F_Y, size, col, alpha=clamp((tau - 0.2 - j * 0.08) / 0.3), scale=1 + 0.04 * (a <= tau < b))
    rec(110, 470, 970, 900, 'card')

def hanuman_at(c, tau, T, y=470, s=0.78, draw=(-3, 0.1)):
    c.save(); c.translate(540 - 300 * s, y); c.scale(s, s); hanuman(Ink(c, tau), draw[0], draw[1], T); c.restore()
    rec(540 - 300 * s, y, 540 + 300 * s, y + 740 * s, 'hanuman')

def motif(c, name, tau, T, y=700, s=0.9, t0=0.0, t1=0.9):
    MOTIFS[name](Ink(c, tau), 540, y, s if name != 'hanuman' else 0.68, t0, t1, T)

def scene(c, i, tau, T):
    k = KEYS[i]
    if k == 'hook':
        headline(c, EP['title'][0], tau, 0.0, 345, 84, RED); headline(c, EP['title'][1], tau, 0.2, 455, 78, INK)
        motif(c, EP['hook_motif'], tau, T, y=770, s=1.1)
    elif k == 'save':
        hanuman_at(c, tau, T, draw=(0.0, 2.4)); bl = 1 + 0.06 * math.sin(T * 9)
        r = chip(c, "सेव कर लीजिए", 540, 360, 64, SAF, INK, clamp(tau / 0.2), scale=(0.8 + 0.2 * back(tau / 0.3)) * bl)
        rec(540 + r.left() * 1.1, 360 + r.top() * 1.1, 540 + r.right() * 1.1, 360 + r.bottom() * 1.1, 'save')
    elif k == 'recite':
        card(c, k, tau); diya(Ink(c, tau), 520, 1040, 0.9, 0.2, 0.7, T)
        tag(c, f"दिन {DIN} / 22 · {EP['ref']}", 560, 395, tau, 0.1, size=42, bg=GOLDL, out=2.6)
    elif k in ('m1', 'm2', 'ins'):
        d = EP[k]
        tag(c, d['head'], 560, 345, tau, 0.15, size=52, bg=CREAM if k != 'ins' else RED, fg=INK if k != 'ins' else CREAM)
        motif(c, d['motif'], tau, T, y=690, s=1.0, t0=0.05, t1=0.95)
        chips_row(c, k, d['chips'], tau)
    elif k == 'cta':
        hanuman_at(c, tau, T)
        ch = chunks(k, CAPS[k]); a, b = EP['cta_chips']
        mid = ch[len(ch) // 2][0] if len(ch) > 1 else durs[k] * 0.5
        tag(c, a, 560, 345, tau, 0.4, size=54, bg=RED, fg=CREAM, out=mid)
        tag(c, b, 560, 345, tau, mid, size=56, bg=GOLDL)

BG = BORD = None
def frame(T):
    global BG, BORD
    if BG is None: BG = skia.Image.fromarray(make_bg()); BORD = border_layer()
    s = skia.Surface(W, H); c = s.getCanvas(); c.drawImage(BG, 0, 0); c.drawImage(BORD, 0, 0)
    i = max(j for j in range(len(START)) if START[j] <= T); tau = T - START[i]
    c.saveLayerAlpha(None, int(255 * clamp(tau / 0.18)) if i > 0 else 255); scene(c, i, tau, T); c.restore()
    draw_caption(c, KEYS[i], tau)
    if i >= 1: badge(c, f"दिन {DIN}", None, 126, 324, 50, alpha=1); rec(76, 274, 176, 374, 'badge')
    return s.makeImageSnapshot().toarray()[:, :, [2, 1, 0]]

# ------------------------------------------------------------------ audio
def mix():
    import pyloudnorm as pyln
    from scipy.signal import butter, sosfilt, resample_poly
    SR = 44100; N = int(TOT * SR) + SR; rng = np.random.default_rng(1)
    t_ = lambda d: np.arange(int(d * SR)) / SR
    def add(buf, x, at, g=1.0):
        i = int(at * SR); x = x[:max(0, len(buf) - i)]; buf[i:i + len(x)] += x * g
    bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
    music = np.zeros(N); sfx = np.zeros(N); voice = np.zeros(N); SA = 138.59
    def tanpura(f, d=2.6):
        t = t_(d); x = sum((0.7 ** h) * np.sin(2 * np.pi * f * h * t + 0.3 * np.sin(2 * np.pi * 3 * t) * (h > 3)) * np.exp(-t * (0.7 + 0.22 * h)) for h in range(1, 12))
        return x * np.minimum(1, t / 0.01)
    def pluck(f, d=2.2):
        t = t_(d); x = sum(a * np.sin(2 * np.pi * f * h * t * (1 + 0.0007 * h)) * np.exp(-t * (2.5 + 2 * h)) for h, a in [(1, 1), (2, .5), (3, .25), (4, .12)])
        return x * np.minimum(1, t / 0.003)
    def bell(f=880, d=4.0):
        t = t_(d); x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dc) for r, a, dc in [(1, 1, 1.0), (2.0, .5, 1.6), (2.76, .4, 2.2), (5.4, .2, 3.5), (8.9, .1, 5)])
        return x * np.minimum(1, t / 0.002)
    def manjira(d=1.2):
        t = t_(d); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 4) for f in (3150, 4420, 5870, 7310)) * 0.25 * np.minimum(1, t / 0.001)
    def whoosh(d=0.35): return bp(rng.normal(0, 1, int(d * SR)), 400, 3000) * np.sin(np.pi * t_(d) / d) ** 2
    beat = 60 / 66; cyc = [SA * 0.75, SA, SA, SA / 2]; t = 0; i = 0
    while t < TOT: add(music, tanpura(cyc[i % 4] * 2), t, 0.22); t += beat; i += 1
    scale = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2, 9 / 4, 5 / 2]; pat = [0, 2, 3, 4, 5, 4, 3, 2, 0, 3, 5, 7, 6, 5, 3, 4]
    r = KEYS.index('recite'); t = beat * 2; i = 0
    while t < TOT - 1:
        if i % 8 not in (3, 7) and not (START[r] <= t < START[r] + D[r]): add(music, pluck(SA * 2 * scale[pat[i % 16]]), t, 0.09)
        if i % 8 == 0: add(music, manjira(), t, 0.035)
        t += beat / 2; i += 1
    add(sfx, bell(1108, 3.5), 0.02, 0.2)
    for i in range(1, len(KEYS)): add(sfx, whoosh(), START[i] - 0.15, 0.08)
    add(sfx, bell(880, 4.5), START[r] + 0.02, 0.24); add(sfx, bell(1318, 3), START[1] + 0.05, 0.10); add(sfx, bell(988, 4), TOT - 2.2, 0.14)
    for i, k in enumerate(KEYS):
        v, sr = trimmed(k)
        if sr != SR: v = resample_poly(v, SR, sr)
        add(voice, v, START[i] + PAD0 + (0.25 if k == 'recite' else 0))
    env = np.minimum(1, np.convolve(np.abs(voice), np.ones(int(0.08 * SR)) / int(0.08 * SR), 'same') / 0.04)
    m = (voice + music * (1 - 0.55 * env) * 0.42 + sfx)[:int(TOT * SR)]; m[-SR:] *= np.linspace(1, 0, SR)
    meter = pyln.Meter(SR)
    def soft(x, th=0.6):
        y = x.copy(); o = np.abs(x) > th; y[o] = np.sign(x[o]) * (th + (1 - th) * np.tanh((np.abs(x[o]) - th) / (1 - th))); return y
    for _ in range(4): m = soft(pyln.normalize.loudness(m, meter.integrated_loudness(m), -14)) * 0.97
    sf.write(f'{OUT}/mix.wav', np.stack([m, m], 1), SR); return meter.integrated_loudness(m)

if __name__ == '__main__' and len(sys.argv) > 4 and sys.argv[4].startswith('part'):
    pass
NAME = f"HanumanChalisa_Din{DIN:02d}"
def render_part(p, n):
    nf = int(TOT * 30); a, b = nf * p // n, nf * (p + 1) // n
    pr = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30', '-i', '-', '-c:v', 'libx264',
                           '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', f'{OUT}/part{p}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b): pr.stdin.write(np.ascontiguousarray(frame(f / 30)).tobytes())
    pr.stdin.close(); pr.wait()

if os.environ.get('HC_PART'):
    p, n = map(int, os.environ['HC_PART'].split('/')); render_part(p, n); sys.exit(0)

if os.environ.get('HC_STILLS'):
    from PIL import Image, ImageDraw
    ts = [START[i] + D[i] * f for i in range(len(D)) for f in (0.4, 0.92)]; ims = []
    for t in ts:
        im = Image.fromarray(np.ascontiguousarray(frame(t))); d = ImageDraw.Draw(im, 'RGBA')
        for box in ([0, 0, W, 269], [0, 1248, W, H], [0, 0, 65, H], [W - 65, 0, W, H]): d.rectangle(box, fill=(255, 0, 0, 50))
        d.rectangle([930, 900, W, 1700], fill=(255, 180, 0, 60)); ims.append(im.resize((270, 480)))
    sh = Image.new('RGB', (270 * 7, 480 * 2), 'white')
    for j, im in enumerate(ims): sh.paste(im, ((j % 7) * 270, (j // 7) * 480))
    sh.save(f'{OUT}/{NAME}_contact_safezone.png'); print('stills', round(TOT, 1)); sys.exit(0)

# full render: 2 processes, mix, mux, safe-zone check, caption
env = dict(os.environ)
procs = [subprocess.Popen([sys.executable, '-W', 'ignore', __file__, str(DIN), OUT, 'render'], env={**env, 'HC_PART': f'{p}/2'}) for p in range(2)]
lufs = mix()
for p in procs: p.wait()
open(f'{OUT}/l.txt', 'w').write("file part0.mp4\nfile part1.mp4\n")
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', f'{OUT}/l.txt', '-i', f'{OUT}/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', f'{OUT}/{NAME}.mp4'], check=True)
bad = []
for f in range(0, int(TOT * 30), 6):
    BOXES.clear(); frame(f / 30)
    for x0, y0, x1, y1, l in BOXES:
        if x0 < 65 or x1 > 1015 or y0 < 269 or y1 > 1248 or (y1 > 900 and x1 > 930): bad.append((round(f / 30, 1), l, int(x0), int(y0), int(x1), int(y1)))
for p in range(2): os.remove(f'{OUT}/part{p}.mp4')
print(json.dumps(dict(name=NAME, dur=round(TOT, 2), lufs=round(lufs, 2), safe_zone_violations=len(bad), first=bad[:5]), ensure_ascii=False))
