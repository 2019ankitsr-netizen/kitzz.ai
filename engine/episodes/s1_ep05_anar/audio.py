import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, lfilter, resample_poly
SR = 44100; T = 45.4; N = int(SR*T)
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
VO=json.load(open('/home/claude/anar/vo.json')); L={l['key']:l for l in VO['lines']}
tCut=L['inside']['start']-0.2; tLight=L['burn']['start']+0.55; tJet=L['jet']['start']-0.1; tSp=L['sparks']['start']-0.1; tCol=L['col0']['start']-0.1
tRed=L['red']['start']; tGreen=L['green']['start']; tBlue=L['blue']['start']; tBomb=L['bomb']['start']-0.1; tBang=L['bomb']['end']-0.75; tCta=L['cta']['start']-0.15
music = np.zeros(N); BARS=19; bar=T/BARS; beat=bar/4
chords = [[50, 57, 62, 66], [55, 59, 62, 67], [52, 59, 64, 67], [57, 61, 64, 69]]   # D G Em A  (festive major)
for b in range(BARS):
    ch = chords[b % 4]; t0 = b*bar
    for m in ch: put(music, note(mf(m), bar+0.3, a=0.4, r=0.6, kind='pad'), t0, 0.05)
    put(music, note(mf(38), bar+0.2, a=0.3, r=0.5, kind='pad'), t0, 0.07); put(music, note(mf(45), bar+0.2, a=0.3, r=0.5, kind='pad'), t0, 0.04)   # drone
    put(music, note(mf(ch[0]-12), bar, a=0.02, r=0.4, kind='pad'), t0, 0.1)
    arp = [ch[0]+12, ch[1]+12, ch[2]+12, ch[3]+12, ch[2]+24, ch[3]+12, ch[2]+12, ch[1]+12]
    for i, m in enumerate(arp):
        put(music, note(mf(m), 0.6), t0+i*beat/2, 0.09 if i % 2 == 0 else 0.06)
    for k in range(4):   # dholak-ish: low + high taps
        tt_ = np.arange(int(0.16*SR))/SR
        put(music, np.sin(2*np.pi*(70+60*np.exp(-tt_*35))*tt_)*np.exp(-tt_*18), t0+k*beat, 0.2)
        for off, g in [(0.5, 0.09), (0.75, 0.06)]:
            put(music, np.sin(2*np.pi*(330+80*np.exp(-tt_*50))*tt_)*np.exp(-tt_*30), t0+(k+off)*beat, g)
tt = np.arange(N)/SR
sfx = np.zeros(N)
def whoosh(d, f0=400, f1=2500):
    n = int(d*SR); x = rng.standard_normal(n); t = np.arange(n)/SR; out = np.zeros(n)
    for i in range(0, n, 512):
        f = f0+(f1-f0)*(i/n); b, a = butter(2, [f*0.7/(SR/2), min(f*1.4, 18000)/(SR/2)], 'band'); out[i:i+512] = lfilter(b, a, x[max(0, i-2048):i+512])[-len(x[i:i+512]):]
    return out*np.sin(np.pi*t/d)**2
def ping(f, d=0.5): t = np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*9)
# fountain hiss + crackle following intensity
I = np.where(tt < tCut, 1.0, np.clip((tt-tLight)/1.3, 0, 1)); I *= np.clip((T-tt)/0.05, 0, 1)
close = np.where((tt >= tCut) & (tt < tCol), 1.0, 0.6)
hiss = hp(rng.standard_normal(N), 2500)*0.5 + lp(hp(rng.standard_normal(N), 600), 3000)*0.5
hiss *= (0.8+0.2*np.sin(tt*37))
cr = np.zeros(N); idx = rng.integers(0, N, 5200); cr[idx] = rng.uniform(-1, 1, len(idx)); cr = hp(lp(cr, 9000), 1500)*6
sfx += (hiss*0.16 + cr*0.5)*I*close
put(sfx, whoosh(0.45), tCut-0.25, 0.5)
t_ = np.arange(int(0.5*SR))/SR; put(sfx, hp(rng.standard_normal(len(t_)), 3000)*np.exp(-t_*8), tLight-0.05, 0.3)   # ignition fizz
put(sfx, whoosh(1.2, 300, 3500), tLight, 0.4)
put(sfx, ping(1175, 0.4), tJet+0.9, 0.2); put(sfx, ping(784, 0.4), tJet+3.6, 0.2)
put(sfx, whoosh(1.2, 500, 3000), tSp, 0.3); put(sfx, whoosh(1.4, 3000, 500), tCol, 0.25)
for tk, m in [(tRed, 74), (tGreen, 78), (tBlue, 81)]: put(sfx, ping(mf(m), 0.8), tk, 0.3)
put(sfx, whoosh(0.7, 500, 3000), tBomb, 0.35)
t_ = np.arange(int(0.9*SR))/SR; put(sfx, hp(rng.standard_normal(len(t_)), 4000)*(0.3+0.7*t_/0.9), tBang-0.9, 0.12)   # wick fizz
nb = int(0.9*SR); t_ = np.arange(nb)/SR
boom = lp(rng.standard_normal(nb), 1800)*np.exp(-t_*9) + np.sin(2*np.pi*(90*np.exp(-t_*6)+35)*t_)*np.exp(-t_*5)*1.5 + hp(rng.standard_normal(nb), 3000)*np.exp(-t_*40)*0.6
put(sfx, boom, tBang, 0.9)
put(sfx, whoosh(1.0, 3000, 400), tCta, 0.3); put(sfx, ping(1320, 0.3), tCta+0.6, 0.2)
vo, sr = sf.read('/home/claude/anar/vo.wav'); vo = resample_poly(vo, 147, 80)   # 24k -> 44.1k
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
sf.write('/home/claude/anar/mix.wav', st, SR)
