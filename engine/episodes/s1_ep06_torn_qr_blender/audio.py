# Original score + SFX for the QR reel: cinematic "product macro" pulse (A minor, 96 bpm),
# sub-bass, glassy plucks, risers, foley-ish ticks. Voice ducking, -14 LUFS.
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, lfilter, resample_poly
SR = 44100
VO = json.load(open('/home/claude/qr/vo.json')); L = {l['key']: l for l in VO['lines']}; S = {k: L[k]['start'] for k in L}
T = VO['total']; N = int(SR*T)
rng = np.random.default_rng(11)
def lp(x, f, o=2): b, a = butter(o, f/(SR/2)); return lfilter(b, a, x)
def hp(x, f, o=2): b, a = butter(o, f/(SR/2), 'high'); return lfilter(b, a, x)
def bp(x, f0, f1): return hp(lp(x, f1), f0)
def put(buf, x, t, g=1.0):
    i = int(t*SR)
    if i >= len(buf): return
    x = x[:len(buf)-i]; buf[i:i+len(x)] += x*g
mf = lambda m: 440*2**((m-69)/12)
def tone(f, d, a=0.01, r=0.3, kind='pluck', det=0.0):
    t = np.arange(int(d*SR))/SR
    if kind == 'pluck':   # glassy FM pluck
        s = np.sin(2*np.pi*f*t + 1.2*np.exp(-t*9)*np.sin(2*np.pi*f*2.0*t))*np.exp(-t*4.5)
    elif kind == 'pad':   # detuned saw-ish, filtered later
        s = sum(np.sin(2*np.pi*f*(1+dv)*t + ph) + 0.3*np.sin(2*np.pi*2*f*(1+dv)*t) for dv, ph in [(0, 0), (0.006, 1.3), (-0.006, 2.1)])/3
    elif kind == 'sub':
        s = np.sin(2*np.pi*f*t)
    env = np.minimum(1, t/a)*np.minimum(1, np.maximum(0, (d-t))/r)
    return s*env

bpm = 96; beat = 60/bpm; bar = beat*4
music = np.zeros(N); pads = np.zeros(N); sub = np.zeros(N); perc = np.zeros(N)
prog = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]   # Am F C G
nb = int(T/bar)+1
for b in range(nb):
    ch = prog[b % 4]; t0 = b*bar
    for m in ch: put(pads, tone(mf(m), bar+0.6, a=0.6, r=0.8, kind='pad'), t0, 0.05)
    put(sub, tone(mf(ch[0]-24), bar, a=0.05, r=0.3, kind='sub'), t0, 0.22)
    intro = t0 < S['finder'] - 0.3
    for k in range(16):    # 16th glassy arp, sparse during hook
        if intro and k % 4: continue
        m = ch[[0, 2, 1, 3][k % 4]] + 12 + (12 if k % 8 == 6 else 0)
        put(music, tone(mf(m), 0.5), t0 + k*beat/4, 0.055 if k % 4 == 0 else 0.03)
    if not intro and t0 < S['cta'] + 2:
        for k in range(4):
            tt = np.arange(int(0.25*SR))/SR
            kick = np.sin(2*np.pi*(48 + 90*np.exp(-tt*30))*tt)*np.exp(-tt*9)
            put(perc, kick, t0 + k*beat, 0.35)
            hat = hp(rng.standard_normal(int(0.05*SR)), 7000)*np.exp(-np.arange(int(0.05*SR))/SR*80)
            put(perc, hat, t0 + k*beat + beat/2, 0.05)
pads = lp(pads, 1800)
music = music + pads + lp(sub, 200) + perc

sfx = np.zeros(N)
def whoosh(d, f0=300, f1=3000, g=1.0):
    n = int(d*SR); x = rng.standard_normal(n); t = np.arange(n)/SR
    env = np.sin(np.pi*t/d)**2
    lo = lp(x, f1)*0.6 + bp(x, f0, f1)*0.4
    return lo*env*g
def tick(f=3200, d=0.03):
    t = np.arange(int(d*SR))/SR; return np.sin(2*np.pi*f*t)*np.exp(-t*160)
def chime(f, d=1.2):
    t = np.arange(int(d*SR))/SR
    return sum(np.sin(2*np.pi*f*h*t)*np.exp(-t*(2.5+h)) / h for h in (1, 2.76, 5.4))
def thunk(f=90):
    t = np.arange(int(0.35*SR))/SR; return np.sin(2*np.pi*(f + 120*np.exp(-t*25))*t)*np.exp(-t*12)
def clank():
    t = np.arange(int(1.4*SR))/SR
    return sum(np.sin(2*np.pi*f*t)*np.exp(-t*d) for f, d in [(312, 3), (587, 4), (843, 5), (1290, 7)])*0.4 + thunk(60)*0.8 if False else \
        np.concatenate([sum(np.sin(2*np.pi*f*t)*np.exp(-t*d) for f, d in [(312, 3), (587, 4), (843, 5), (1290, 7)])*0.3])
def riser(d):
    n = int(d*SR); t = np.arange(n)/SR; x = rng.standard_normal(n)
    return bp(x, 800, 6000)*(t/d)**2*0.5 + np.sin(2*np.pi*(200 + 600*(t/d)**2)*t)*(t/d)**2*0.15

# hook: scanner beep, sweep, "paid" chime
put(sfx, tone(1800, 0.08, a=0.002, r=0.03, kind='sub'), 0.05, 0.12)
put(sfx, whoosh(1.1, 1500, 8000, 0.25), 0.05)
put(sfx, chime(1318.5, 1.0) + chime(1975.5, 1.0)*0.6, 1.3, 0.22)
# transitions
for t in [S['finder']-0.25, S['bits']-0.3, S['backup']+0.6, S['rs']-0.1, S['thirty']-0.5, S['origin']-0.2, S['cta']-0.4]:
    put(sfx, whoosh(0.9, 200, 2500, 0.35), t)
# finders rise
for k in range(3): put(sfx, thunk(70 + 15*k), S['finder']+1.2 + 0.35*k, 0.55)
# bits ripple ticks
for k in range(28): put(sfx, tick(2600 + 40*k, 0.025), S['bits']+0.95 + k*0.045*2, 0.1)
# backup: glass chimes
for k in range(9): put(sfx, chime(mf(76 + [0, 3, 7, 10, 12, 15, 19, 22, 24][k]), 0.9), S['backup']+1.0 + k*0.1, 0.05)
# rebuild: magnetic clicks
put(sfx, riser(1.2), S['rs']+0.1, 0.6)
for k in range(45): put(sfx, tick(rng.uniform(1800, 4200), 0.02), S['rs']+1.25 + rng.uniform(0, 2.3), 0.12)
put(sfx, chime(1046.5, 1.4), S['rs']+3.6, 0.15)
# thirty: slab lifts
put(sfx, whoosh(1.2, 100, 1200, 0.5), S['thirty']+0.5)
# origin: gear clank
put(sfx, thunk(55), S['origin']+0.3, 0.8); put(sfx, clank()[:int(1.4*SR)], S['origin']+0.3, 0.35)
# nudge + cta pops
for t in [S['backup']+2.2, S['cta']+0.2]: put(sfx, tone(880, 0.12, a=0.003, r=0.08, kind='sub') + tone(1320, 0.12, a=0.003, r=0.08, kind='sub'), t, 0.12)
# end tear crumble (loop back)
for k in range(30): put(sfx, tick(rng.uniform(500, 1500), 0.04), T-1.3 + rng.uniform(0, 0.8), 0.15)

v, vsr = sf.read('/home/claude/qr/vo.wav'); v = resample_poly(v, SR, vsr)[:N]; v = np.pad(v, (0, N-len(v)))
# ducking envelope
env = np.ones(N)
for l in VO['lines']:
    a, b = int((l['start']-0.15)*SR), int((l['end']+0.15)*SR); env[a:b] = 0.42
k = int(0.12*SR); env = np.convolve(env, np.ones(k)/k, mode='same')
music *= env
fade = np.ones(N); fade[:int(0.03*SR)] = np.linspace(0, 1, int(0.03*SR)); fade[-int(0.3*SR):] = np.linspace(1, 0.6, int(0.3*SR))
mix = (v*1.0 + music*0.75 + sfx*0.8)*fade
st = np.stack([mix, mix], 1)
st[:, 0] += music*0.04; st[:, 1] -= music*0.04
sf.write('/home/claude/qr/mix_raw.wav', st/np.max(np.abs(st))*0.9, SR)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/home/claude/qr/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '44100', '/home/claude/qr/mix.wav'], check=True)
import pyloudnorm as pyln
a, _ = sf.read('/home/claude/qr/mix.wav'); print('LUFS', round(pyln.Meter(SR).integrated_loudness(a), 2), 'dur', len(a)/SR)
