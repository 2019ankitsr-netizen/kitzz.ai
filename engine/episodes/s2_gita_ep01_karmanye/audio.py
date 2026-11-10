import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, lfilter, resample_poly
SR = 44100; T = 46.9; N = int(SR*T)
rng = np.random.default_rng(3)
def lp(x, f, o=2): b, a = butter(o, f/(SR/2)); return lfilter(b, a, x)
def hp(x, f, o=2): b, a = butter(o, f/(SR/2), 'high'); return lfilter(b, a, x)
def put(buf, x, t, g=1.0):
    i = int(t*SR); x = x[:max(0, len(buf)-i)]; buf[i:i+len(x)] += x*g
def note(f, d, a=0.005, r=0.3, kind='pluck'):
    t = np.arange(int(d*SR))/SR
    if kind == 'pluck':
        s = np.sin(2*np.pi*f*t)*np.exp(-t*5) + 0.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*8) + 0.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*12)
    else:
        s = sum(np.sin(2*np.pi*f*(1+dv)*t + ph) for dv, ph in [(0, 0), (0.004, 1), (-0.004, 2)])/3 + 0.25*np.sin(2*np.pi*2*f*t)
    env = np.minimum(1, t/a)*np.minimum(1, (d-t)/r)
    return s*env
mf = lambda m: 440*2**((m-69)/12)
import json
VO=json.load(open('/home/claude/gita/vo.json')); L={l['key']:l for l in VO['lines']}
tDrop=1.0; tFear=L['fear']['start']-0.2; tK=L['krishna']['start']; tSh=L['sh1']['start']-0.35; tM1=L['mean1']['start']-0.2; tM2=L['mean2']['start']-0.1; tStand=L['mean2']['start']+2.7
tToday=L['today']['start']-0.25; tShoot=L['shoot']['start']-0.15; tFire=L['shoot']['start']+0.95; tCta=L['cta']['start']-0.2
tt = np.arange(N)/SR
music = np.zeros(N)
# tanpura drone on D: Pa Sa' Sa' Sa cycle
cyc = 2.6
for i in range(int(T/cyc)+1):
    for j, m in enumerate([57, 62, 62, 50]):
        t_ = np.arange(int(2.4*SR))/SR; f = mf(m)
        s = sum(np.sin(2*np.pi*f*h*t_)*np.exp(-t_*(0.6+0.25*h))/h**0.7 for h in range(1, 9))*np.minimum(1, t_/0.02)
        put(music, s, i*cyc+j*cyc/4, 0.035)
scale = [62, 64, 66, 69, 71, 74, 76, 78, 81]   # Bhoopali on D
BARS = 20; bar = T/BARS; beat = bar/4
pat = [0, 2, 3, 5, 4, 3, 2, 3,  1, 2, 4, 5, 6, 5, 4, 2]
quiet = lambda t: 0.45 if (tSh-0.5 < t < tM1) else 1.0
for b in range(BARS):
    for i in range(8):
        t0 = b*bar+i*beat/2; q = quiet(t0)
        if q < 1 and i % 2: continue
        m = scale[pat[(b*8+i) % 16]]
        t_ = np.arange(int(1.6*SR))/SR; f = mf(m)
        s = (np.sin(2*np.pi*f*t_)+0.35*np.sin(2*np.pi*2*f*t_)*np.exp(-t_*6)+0.12*np.sin(2*np.pi*3.01*f*t_)*np.exp(-t_*10))*np.exp(-t_*3.2)*np.minimum(1, t_/0.012)
        put(music, s, t0, (0.085 if i % 2 == 0 else 0.055)*q); put(music, s, t0+0.02, 0.03*q)
# soft pad under everything
for b in range(BARS):
    for m, g in [(50, 0.05), (57, 0.04), (62, 0.035), (66, 0.022)]:
        t_ = np.arange(int((bar+0.6)*SR))/SR; f = mf(m)
        s = (np.sin(2*np.pi*f*t_)+np.sin(2*np.pi*f*1.003*t_)+0.2*np.sin(2*np.pi*2*f*t_))*np.minimum(1, t_/0.8)*np.minimum(1, (bar+0.6-t_)/0.8)
        put(music, s, b*bar, g)
# epic layer: deep booms, choir swell at the cosmic reveal
def boom(g=1.0):
    t_ = np.arange(int(1.6*SR))/SR
    return (np.sin(2*np.pi*(42+30*np.exp(-t_*14))*t_)*np.exp(-t_*3.2) + lp(rng.standard_normal(len(t_)), 220)*np.exp(-t_*7)*0.8)*g
for b in range(BARS):
    t0 = b*bar
    if not (tSh-0.5 < t0 < tM1): put(music, boom(), t0, 0.5); put(music, boom(), t0+2.5*beat, 0.22)
def choir(d, notes):
    t_ = np.arange(int(d*SR))/SR; out = np.zeros(len(t_))
    for m in notes:
        f = mf(m)*(1+0.004*np.sin(2*np.pi*5*t_+m)); ph = 2*np.pi*np.cumsum(f)/SR; saw = sum(np.sin(ph*h)/h for h in range(1, 14))
        for fc, g in [(650, 1.0), (1100, 0.6), (2700, 0.25)]:
            b_, a_ = butter(2, [fc*0.8/(SR/2), fc*1.25/(SR/2)], 'band'); out += lfilter(b_, a_, saw)*g
    return out*np.minimum(1, t_/1.8)*np.minimum(1, (d-t_)/2.0)
put(music, choir(tM1-tK+1.5, [50, 57, 62, 66, 69]), tK+0.4, 0.05)
put(music, boom(1.6), tK+0.7, 0.9)
sfx = np.zeros(N)
def whoosh(d, f0=400, f1=2500):
    n = int(d*SR); x = rng.standard_normal(n); t = np.arange(n)/SR; out = np.zeros(n)
    for i in range(0, n, 512):
        f = f0+(f1-f0)*(i/n); b, a = butter(2, [f*0.7/(SR/2), min(f*1.4, 18000)/(SR/2)], 'band'); out[i:i+512] = lfilter(b, a, x[max(0, i-2048):i+512])[-len(x[i:i+512]):]
    return out*np.sin(np.pi*t/d)**2
def bell(f, d=2.2): t = np.arange(int(d*SR))/SR; return sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*dc) for r, a, dc in [(1, 1, 1.6), (2.76, 0.5, 2.6), (5.4, 0.25, 4), (8.9, 0.12, 6)])
def conch(d=1.9, f=233):
    t = np.arange(int(d*SR))/SR; fr = f*(1+0.06*np.clip(t/0.5, 0, 1)); ph = 2*np.pi*np.cumsum(fr)/SR
    s = sum(np.sin(ph*h)/h for h in range(1, 7)); return lp(s, 1400)*np.minimum(1, t/0.25)*np.minimum(1, (d-t)/0.5)*(1+0.05*np.sin(2*np.pi*5.5*t))
put(sfx, conch(), 0.0, 0.16); put(sfx, conch(2.6, 196), tK+0.6, 0.14)
t_ = np.arange(int(0.35*SR))/SR; thud = np.sin(2*np.pi*(80+60*np.exp(-t_*25))*t_)*np.exp(-t_*12)+lp(rng.standard_normal(len(t_)), 900)*np.exp(-t_*25)*0.6
put(sfx, thud, tDrop+0.7, 0.7); put(sfx, thud, tDrop+0.95, 0.25)
put(sfx, whoosh(0.9), tFear, 0.3); put(sfx, whoosh(1.0, 2500, 500), tK-0.6, 0.25)
put(sfx, bell(880), tK+0.5, 0.2); put(sfx, bell(1320), tK+0.9, 0.12)
for k, m in enumerate([74, 78, 81, 86, 90]): put(sfx, bell(mf(m), 1.2), tK+0.6+k*0.12, 0.07)
put(sfx, bell(660, 3), L['sh1']['start']-0.1, 0.22); put(sfx, bell(660, 3), L['sh2']['start']-0.1, 0.2); put(sfx, bell(880, 3), L['sh2']['end'], 0.16)
put(sfx, whoosh(0.9), tM1, 0.25)
for k, m in enumerate([69, 74, 78]): put(sfx, bell(mf(m), 0.8), tStand+0.5+k*0.1, 0.12)
for k in range(3): put(sfx, bell(mf([74, 76, 78][k]), 0.5), tToday+0.3+[0, 1.05, 2.0][k], 0.14)
put(sfx, whoosh(0.8), tToday, 0.3); put(sfx, whoosh(0.7, 2500, 600), tShoot, 0.3)
t_ = np.arange(int(0.5*SR))/SR; twang = np.sin(2*np.pi*(180+140*np.exp(-t_*18))*t_)*np.exp(-t_*9)*(1+0.3*np.sin(2*np.pi*40*t_))
put(sfx, twang, tFire, 0.6); put(sfx, whoosh(0.6, 800, 5000), tFire, 0.5)
put(sfx, whoosh(1.2, 2500, 400), tCta, 0.25); put(sfx, bell(1320, 1.2), tCta+0.6, 0.12)
from scipy.signal import fftconvolve
def reverb(x, d=1.4, wet=0.2, tone=3500):
    n = int(d*SR); t = np.arange(n)/SR; ir = lp(np.random.default_rng(9).standard_normal(n), tone)*np.exp(-t*(5.5/d)); ir[:int(0.012*SR)] = 0; ir /= np.sqrt((ir**2).sum())
    return x + wet*fftconvolve(x, ir)[:len(x)]
vo, sr = sf.read('/home/claude/gita/vo.wav'); vo = resample_poly(vo, 147, 80)
vo = lp(hp(vo, 75), 9500); voice = np.zeros(N); voice[:min(N, len(vo))] = vo[:N]
voice /= np.abs(voice).max()
# gentle levelling: slow gain riding, then soft saturation
env = np.maximum(lp(np.abs(voice), 4, 1), 1e-4); g = np.clip(0.16/env, 0.6, 1.8); g = lp(g, 3, 1); voice = np.tanh(voice*g*1.2)/1.2
voice = reverb(voice, 0.9, 0.09, 4500)
music = reverb(lp(music, 6500), 2.0, 0.35); sfx = reverb(lp(sfx, 8000), 1.6, 0.3)
env = lp(np.abs(voice), 5, 1); duck = 1-0.5*np.clip(env/0.1, 0, 1); duck = lp(duck, 4, 1)
music /= np.abs(music).max(); voice /= np.abs(voice).max()
mix = voice*0.95 + music*0.3*duck + sfx*0.3
e = int(0.05*SR); mix[:e] *= np.linspace(0, 1, e); mix[-e:] *= np.linspace(1, 0, e)
st = np.stack([mix, mix], 1)
m = pyln.Meter(SR)
for _ in range(3):
    st = st*10**((-14.0-m.integrated_loudness(st))/20); st = np.tanh(st*1.15)/1.15 if np.abs(st).max()>0.9 else st
print('LUFS', m.integrated_loudness(st), 'peak', np.abs(st).max())
sf.write('/home/claude/gita/mix.wav', st, SR)
