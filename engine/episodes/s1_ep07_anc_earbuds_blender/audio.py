# Original score + SFX for the noise-cancelling reel (S1 ep07): cinematic "product macro" pulse (A minor, 96 bpm),
# sub-bass, glassy plucks, risers, foley-ish ticks. Voice ducking, -14 LUFS.
import json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, lfilter, resample_poly
SR = 44100
import os
WORK = os.environ.get('WORK', '/home/claude/anc')
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
    intro = t0 < S['mic'] - 0.3
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

# engine hum (the "noise"): low rumble that the reel literally cancels on screen
def hum(d, f=82):
    n = int(d*SR); t = np.arange(n)/SR
    x = sum(np.sin(2*np.pi*f*h*t + h)/h for h in (1, 2, 3, 4.02)) + 0.4*lp(rng.standard_normal(n), 400)
    return x
H = np.zeros(N); hv = np.zeros(N)
H[:] = hum(T)
def seg(a, b, g, fi=0.3, fo=0.3):
    t = np.arange(N)/SR
    return g*np.clip(np.minimum((t-a)/fi, (b-t)/fo), 0, 1)
tt = np.arange(N)/SR
hv += seg(0.0, 1.9, 0.10, 0.02, 0.5)                                  # hook: hum, then silence
hv += seg(S['mic']+0.4, S['cancel']+2.0, 0.09, 0.8, 0.9)              # mic/flip/cancel: hum, cancelled
hv += seg(S['fast']+1.2, S['fast']+3.2, 0.05, 0.3, 0.5)               # late = leaks
hv += seg(S['low']+0.2, S['low']+2.2, 0.08, 0.5, 0.8)                 # low hum cancelled
sfx = H*hv
# silence hits: a soft "air" pop when the line goes flat
for t in [1.9, S['cancel']+2.4, S['inside']+2.5, S['low']+2.3]:
    put(sfx, chime(1568, 1.2)*0.6 + chime(2349, 1.2)*0.3, t, 0.12)
# transitions
for t in [S['mic']-0.25, S['flip']-0.2, S['cancel']-0.2, S['fast']-0.3, S['inside']-0.3, S['low']-0.3, S['origin']-0.2, S['cta']-0.4]:
    put(sfx, whoosh(0.9, 200, 2500, 0.3), t)
# mic picks up: blip
put(sfx, tone(1400, 0.1, a=0.002, r=0.05, kind='sub'), S['mic']+2.4, 0.12)
# flip: riser + turn whoosh, chip blips
put(sfx, riser(1.4), S['flip']+1.6, 0.4)
for k in range(6): put(sfx, tick(3000 + 200*k, 0.03), S['flip']+0.3 + k*0.08, 0.12)
# fast: rapid ticks (thousands per second impression)
for k in range(40): put(sfx, tick(4200, 0.015), S['fast']+0.2 + k*0.025, 0.06)
# voices blocked by tip: muffled thud
put(sfx, thunk(140), S['low']+4.2, 0.4)
# origin: count-up ticks + clank
for k in range(12): put(sfx, tick(2400 + 60*k, 0.03), S['origin']+0.2 + k*0.08, 0.12)
put(sfx, clank()[:int(1.4*SR)], S['origin']+1.25, 0.3)
# nudge + cta pops
for t in [S['fast']+0.3, S['cta']+0.2]: put(sfx, tone(880, 0.12, a=0.003, r=0.08, kind='sub') + tone(1320, 0.12, a=0.003, r=0.08, kind='sub'), t, 0.12)
# loop: hum fades back in under the last second so the hook's hum continues it
put(sfx, H[:int(1.2*SR)]*np.linspace(0, 0.08, int(1.2*SR)), T-1.2)

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
