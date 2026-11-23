# Original score + SFX for the touchscreen reel (S1 ep09): cinematic "product macro" pulse (A minor, 96 bpm),
# sub-bass, glassy plucks, risers, foley-ish ticks. Voice ducking, -14 LUFS.
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, lfilter, resample_poly
SR = 44100
import os
WORK = os.environ.get('WORK', '/home/claude/ts')
VO = json.load(open(f'{WORK}/vo.json')); L = {l['key']: l for l in VO['lines']}; S = {k: L[k]['start'] for k in L}
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
    intro = t0 < S['grid'] - 0.3
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

sfx = np.zeros(N)
def zap(d=0.25, f=900):
    n = int(d*SR); t = np.arange(n)/SR
    return (np.sin(2*np.pi*(f + 600*np.exp(-t*30))*t)*0.5 + 0.5*bp(rng.standard_normal(n), 2000, 7000))*np.exp(-t*14)
def tap():
    n = int(0.06*SR); t = np.arange(n)/SR; return (np.sin(2*np.pi*1800*t) + 0.4*hp(rng.standard_normal(n), 4000))*np.exp(-t*90)
# hook: tap + charge zap
put(sfx, tap(), 0.45, 0.3); put(sfx, zap(0.5), 0.5, 0.25)
for t in [S['grid']-0.25, S['field']-0.2, S['touch']-0.2, S['scan']-0.3, S['swipe']-0.3, S['glove']-0.3, S['origin']-0.2, S['cta']-0.4]:
    put(sfx, whoosh(0.9, 200, 2500, 0.3), t)
# grid drawing on: rising ticks per row, then per column
for j in range(13): put(sfx, tick(1800 + 90*j, 0.025), S['grid']+0.2 + j*0.1, 0.12)
for i in range(7): put(sfx, tick(2400 + 150*i, 0.025), S['grid']+2.4 + i*0.16, 0.12)
# field: soft electric shimmer
n = int(3.0*SR); tt = np.arange(n)/SR; put(sfx, bp(rng.standard_normal(n), 3000, 9000)*np.sin(np.pi*tt/3.0)*0.6, S['field']+0.2, 0.06)
# touch: tap + charge being pulled
put(sfx, tap(), S['touch']+3.2, 0.3); put(sfx, zap(0.6, 700), S['touch']+3.25, 0.22)
# scan: two fast sweeps of ticks, then a found "blip"
for rep in range(2):
    for k in range(13): put(sfx, tick(3000, 0.012), S['scan']+0.3 + rep*2.0 + k*0.15, 0.08)
put(sfx, tone(1320, 0.2, a=0.003, r=0.12, kind='sub') + tone(1760, 0.2, a=0.003, r=0.12, kind='sub'), S['scan']+2.7, 0.15)
put(sfx, riser(1.2), S['scan']+1.4, 0.2)
# swipe: whoosh along the glass, pinch: two taps
put(sfx, whoosh(1.2, 600, 5000, 0.35), S['swipe']+0.3)
put(sfx, tap(), S['swipe']+2.2, 0.25); put(sfx, tap(), S['swipe']+2.26, 0.25)
# glove: dull thud, nothing happens; sausage: squish + zap (it works)
put(sfx, thunk(160), S['glove']+0.9, 0.35)
put(sfx, tone(220, 0.25, a=0.005, r=0.15, kind='sub'), S['glove']+1.1, 0.12)
put(sfx, thunk(120)*0.6, S['glove']+3.0, 0.3); put(sfx, zap(0.5, 600)*0.6, S['glove']+3.0, 0.3)
put(sfx, chime(1568, 1.0)*0.6, S['glove']+3.2, 0.1)
# origin: count-up ticks + radar ping
for k in range(12): put(sfx, tick(2400 + 60*k, 0.03), S['origin']+0.2 + k*0.08, 0.12)
for k in range(3): put(sfx, chime(1046, 1.4)*0.5, S['origin']+1.4 + k*2.6, 0.12)
for t in [S['scan']+0.3, S['cta']+0.2]: put(sfx, tone(880, 0.12, a=0.003, r=0.08, kind='sub') + tone(1320, 0.12, a=0.003, r=0.08, kind='sub'), t, 0.12)
put(sfx, tap(), T-0.15, 0.25)   # loops into the hook's tap

v, vsr = sf.read(f'{WORK}/vo.wav'); v = resample_poly(v, SR, vsr)[:N]; v = np.pad(v, (0, N-len(v)))
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
sf.write(f'{WORK}/mix_raw.wav', st/np.max(np.abs(st))*0.9, SR)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{WORK}/mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '44100', f'{WORK}/mix.wav'], check=True)
import pyloudnorm as pyln
a, _ = sf.read(f'{WORK}/mix.wav'); print('LUFS', round(pyln.Meter(SR).integrated_loudness(a), 2), 'dur', len(a)/SR)
# second pass: land exactly on -14 LUFS (loudnorm's one-pass mode can undershoot), keep peaks under -1 dBFS
g = 10**((-14 - pyln.Meter(SR).integrated_loudness(a))/20); a2 = a*g
pk = np.max(np.abs(a2))
if pk > 0.89:   # soft-knee limiter above 0.7 only
    sg = np.sign(a2); m = np.abs(a2); over = m > 0.7
    m[over] = 0.7 + 0.19*np.tanh((m[over]-0.7)/0.19); a2 = sg*m
sf.write(f'{WORK}/mix.wav', a2, SR); print('LUFS final', round(pyln.Meter(SR).integrated_loudness(a2), 2))
