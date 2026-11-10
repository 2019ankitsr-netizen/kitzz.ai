import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, lfilter, resample_poly
SR = 44100; T = 43.2; N = int(SR*T)
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
music = np.zeros(N)
BPM = 100; beat = 60/BPM; bar = beat*4          # 18 bars = 43.2 s exactly
chords = [[50, 57, 62, 65], [46, 53, 58, 62], [53, 60, 65, 69], [48, 55, 60, 64]]   # Dm Bb F C
for b in range(18):
    ch = chords[b % 4]; t0 = b*bar
    for m in ch: put(music, note(mf(m), bar+0.3, a=0.4, r=0.6, kind='pad'), t0, 0.055)
    put(music, note(mf(ch[0]-12), bar, a=0.02, r=0.4, kind='pad'), t0, 0.11)
    arp = [ch[0]+12, ch[2]+12, ch[3]+12, ch[1]+24, ch[3]+12, ch[2]+12, ch[1]+12, ch[2]+12]
    for i, m in enumerate(arp):
        if b >= 1: put(music, note(mf(m), 0.5), t0+i*beat/2, 0.085 if i % 2 == 0 else 0.055)
    if b >= 2:
        for k in range(4):   # soft kick + shaker
            tt = np.arange(int(0.18*SR))/SR
            put(music, np.sin(2*np.pi*(55+70*np.exp(-tt*30))*tt)*np.exp(-tt*16), t0+k*beat, 0.22)
            sh = hp(rng.standard_normal(int(0.05*SR)), 6000)*np.exp(-np.arange(int(0.05*SR))/SR*70)
            put(music, sh, t0+k*beat+beat/2, 0.05)
# underwater feel: darker filter while under the sea (hook dive and ocean leg)
dark = lp(music, 900)
tt = np.arange(N)/SR
def win(a, b, f=0.5): return np.clip((tt-a)/f, 0, 1)*np.clip((b-tt)/f, 0, 1)
w = np.maximum.reduce([win(1.6, 4.5, 0.4), win(19.6, 29.3), win(31.8, 33.4), win(35.9, 37.6, 0.3)])
music = music*(1-w*0.85) + dark*w*1.25

sfx = np.zeros(N)
def whoosh(d, f0=400, f1=2500):
    n = int(d*SR); x = rng.standard_normal(n); t = np.arange(n)/SR; out = np.zeros(n)
    for i in range(0, n, 512):
        f = f0+(f1-f0)*(i/n); b, a = butter(2, [f*0.7/(SR/2), min(f*1.4, 18000)/(SR/2)], 'band'); out[i:i+512] = lfilter(b, a, x[max(0, i-2048):i+512])[-len(x[i:i+512]):]
    return out*np.sin(np.pi*t/d)**2
def ping(f, d=0.5): t = np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*9)
def bubble():
    t = np.arange(int(0.09*SR))/SR; f = 500+rng.uniform(0, 900); return np.sin(2*np.pi*(f+f*4*t)*t)*np.exp(-t*40)
def splash(): n = int(0.7*SR); return lp(hp(rng.standard_normal(n), 500), 5000)*np.exp(-np.arange(n)/SR*6)
put(sfx, whoosh(1.5, 2500, 300), 0.8, 0.5); put(sfx, splash(), 1.75, 0.35)
put(sfx, whoosh(0.5), 4.3, 0.45)
put(sfx, ping(1320, 0.25), 5.05, 0.3)                       # tap play
for k in range(3): put(sfx, ping(880+k*110, 0.3), 5.5+k*0.9, 0.12)   # radio rings
put(sfx, ping(660, 0.8), 8.7, 0.3); put(sfx, whoosh(1.2, 1500, 400), 9.0, 0.3)
put(sfx, splash(), 19.3, 0.4)
for x, tp in [(11.5, 22.2), (15.5, 25.0), (19.5, 27.8)]: put(sfx, ping(990, 0.6), tp, 0.22)   # repeaters
for t0, t1 in [(1.9, 4.4), (19.6, 29.2), (36.0, 37.5)]:
    for _ in range(int((t1-t0)*3)): put(sfx, bubble(), rng.uniform(t0, t1), 0.07)
for k in range(5): put(sfx, ping(1175*2**(k/12*0), 0.3), 24.75+k*0.2, 0.0)  # (unused)
put(sfx, ping(1568, 0.9), 25.7, 0.25)                        # 99%
put(sfx, whoosh(0.7, 500, 3000), 29.2, 0.35); put(sfx, whoosh(0.6, 3000, 500), 31.4, 0.3)
for k in range(4): put(sfx, ping(1760, 0.12), 29.9+k*0.3, 0.1)       # satellite beeps
for k in range(6): put(sfx, ping(1400+200*(k % 3), 0.1), 34.9+k*0.12, 0.14)  # servers
put(sfx, whoosh(2.5, 300, 4000), 35.7, 0.5)
for k, m in enumerate([74, 77, 81, 86]): put(sfx, ping(mf(m), 0.7), 38.75+k*0.09, 0.22)   # video arrives
put(sfx, ping(1320, 0.3), 39.2, 0.2); put(sfx, whoosh(1.6, 300, 2500), 41.6, 0.4)

vo, sr = sf.read('/home/claude/reel/vo.wav'); vo = resample_poly(vo, 147, 80)   # 24k -> 44.1k
vo = hp(vo, 70); voice = np.zeros(N); voice[:min(N, len(vo))] = vo[:N]
voice /= np.abs(voice).max()
# duck music under the voice
env = lp(np.abs(voice), 6, 1); duck = 1-0.55*np.clip(env/0.12, 0, 1)
music /= np.abs(music).max()
mix = voice*0.95 + music*0.34*duck + sfx*0.5
# loop-friendly edges
e = int(0.03*SR); mix[:e] *= np.linspace(0, 1, e); mix[-e:] *= np.linspace(1, 0, e)
st = np.stack([mix, mix], 1)
m = pyln.Meter(SR)
for _ in range(3):
    st = st*10**((-14.0-m.integrated_loudness(st))/20); st = np.tanh(st*1.15)/1.15 if np.abs(st).max()>0.9 else st
print('LUFS', m.integrated_loudness(st), 'peak', np.abs(st).max())
sf.write('/home/claude/reel/mix.wav', st, SR)
