# S4 score: bouncy pop (122 bpm, F major), punchy kick/clap, plucky bass, cut whooshes, boings, bee buzz, bubble pops, steam hiss.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/bk'); from kit import put, mix_and_master, SR
from scipy.signal import butter, lfilter
D = '/home/claude/s4'; VO = json.load(open(f'{D}/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; T = VO['total']; N = int(SR*T)
rng = np.random.default_rng(6)
def lp(x, f): b, a = butter(2, f/(SR/2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f/(SR/2), 'high'); return lfilter(b, a, x)
def bpf(x, f1, f2): b, a = butter(2, [f1/(SR/2), f2/(SR/2)], 'band'); return lfilter(b, a, x)
mf = lambda m: 440*2**((m-69)/12)
def tt(d): return np.arange(int(d*SR))/SR
def pluck(f, d=0.3): t = tt(d); return (np.sign(np.sin(2*np.pi*f*t))*0.3 + np.sin(2*np.pi*f*t))*np.exp(-t*9)
def bell(f, d=0.5): t = tt(d); return np.sin(2*np.pi*f*t + 0.8*np.sin(2*np.pi*f*3.5*t)*np.exp(-t*6))*np.exp(-t*7)
def kick(): t = tt(0.3); return np.sin(2*np.pi*(50 + 110*np.exp(-t*28))*t)*np.exp(-t*10)
def clap(): t = tt(0.18); n = rng.standard_normal(len(t)); return hp(lp(n, 3000), 900)*(np.exp(-t*30) + 0.5*np.exp(-(t-0.012).clip(0)*40)*(t > 0.012))
def hat(): t = tt(0.05); return hp(rng.standard_normal(len(t)), 8000)*np.exp(-t*90)
bpm = 122; beat = 60/bpm; bar = 4*beat
prog = [[53, 57, 60], [48, 52, 55], [50, 53, 57], [46, 50, 53]]   # F C Dm Bb
music = np.zeros(N)
for b in range(int(T/bar)+1):
    ch = prog[b % 4]; t0 = b*bar
    for k in range(8):
        put(music, pluck(mf(ch[0]-12 if k % 2 == 0 else ch[0]), 0.25), t0 + k*beat/2, 0.16)
    for k in range(4):
        put(music, kick(), t0 + k*beat, 0.5)
        if k % 2: put(music, clap(), t0 + k*beat, 0.35)
        put(music, hat(), t0 + k*beat + beat/2, 0.12)
    mel = [ch[2]+12, ch[0]+24, ch[1]+12, ch[2]+12, ch[1]+12, ch[0]+12]
    for i, m in enumerate(mel): put(music, bell(mf(m), 0.4), t0 + i*beat*0.66, 0.07)
sfx = np.zeros(N)
def whoosh(d=0.35): t = tt(d); n = rng.standard_normal(len(t)); return hp(lp(n, 5000), 600)*np.sin(np.pi*t/d)**2
def boing(f=220): t = tt(0.35); return np.sin(2*np.pi*(f + 160*np.sin(t*40)*np.exp(-t*8))*t)*np.exp(-t*7)
def pop(f=900): t = tt(0.08); return np.sin(2*np.pi*(f - 600*t/0.08)*t)*np.exp(-t*40)
def bloop(d=1.6): t = tt(d); return np.sin(2*np.pi*np.cumsum(700 - 400*t/d)/SR)*np.exp(-t*1.2)*0.6
def splat(): t = tt(0.25); return lp(rng.standard_normal(len(t)), 900)*np.exp(-t*18)
def deflate(d=1.8): t = tt(d); f = 520*np.exp(-t*1.1); return np.sin(2*np.pi*np.cumsum(f)/SR)*(0.5 + 0.5*np.sin(2*np.pi*7*t))*np.exp(-t*0.9)*0.5
def buzz(d): t = tt(d); f = 210 + 15*np.sin(2*np.pi*0.9*t); s = np.sign(np.sin(2*np.pi*np.cumsum(f)/SR)); return bpf(s, 180, 2400)*(0.6 + 0.4*np.sin(2*np.pi*0.5*t)**2)
def hiss(d=1.5): t = tt(d); return hp(rng.standard_normal(len(t)), 3500)*np.sin(np.pi*t/d)
cuts = [S['tomb']-0.1, S['water']-0.15, S['acid']-0.15, S['bee']-0.15, S['crystal']-0.15, S['cta']-0.15]
for c in cuts: put(sfx, whoosh(), c-0.12, 0.5)
for i in range(3): put(sfx, boing(200 + 40*i), 0.42 + i*0.12, 0.3)
for i in range(9): put(sfx, pop(1100 + 60*i), 0.5 + i*0.05 + 0.18, 0.18)
put(sfx, pop(), 0.8 + 0.2, 0.4)
put(sfx, whoosh(0.9)*0.5, S['tomb'] - 0.1 + 0.3, 0.35)                 # pot slides out
put(sfx, bloop(), S['water'] + 1.0, 0.3)                             # drop shrinks
tg = S['water'] + 3.6; put(sfx, splat(), tg + 0.45, 0.7); put(sfx, deflate(), tg + 1.4, 0.35)
put(sfx, pop(), S['acid'] + 0.35, 0.5); put(sfx, pop(1000), S['acid'] + 0.55, 0.5)
tE = S['bee'] - 0.15; put(sfx, buzz(S['crystal'] - 0.15 - tE), tE, 0.13)
for i in range(12): put(sfx, pop(1400 + rng.uniform(-200, 300)), S['bee'] + 2.0 + i*0.22 + 1.5, 0.12)
tw = S['crystal'] + 4.4; put(sfx, boing(160), tw + 0.35, 0.4); put(sfx, hiss(1.8), tw + 0.4, 0.15)
put(sfx, bell(1760, 0.6) + bell(2637, 0.6), S['crystal'] + 2.0, 0.15)
for c in (S['water'] + 6.6, S['cta'] + 0.1): put(sfx, pop(), c, 0.35)
for i in range(3): put(sfx, whoosh(0.3)*0.6, T - 0.45 + i*0.05, 0.4)
mix_and_master(D, music, sfx, music_gain=0.6)
