# S2 score: whimsical claymation folk — pizzicato plucks, bansuri-like flute with vibrato, dholak taps, drone; boing/pop foley.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/bk'); from kit import put, mix_and_master, SR
from scipy.signal import butter, lfilter
D = '/home/claude/s2'; VO = json.load(open(f'{D}/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; E = {l['key']: l['end'] for l in VO['lines']}; T = VO['total']; N = int(SR*T)
rng = np.random.default_rng(4)
def lp(x, f): b, a = butter(2, f/(SR/2)); return lfilter(b, a, x)
mf = lambda m: 440*2**((m-69)/12)
def tt(d): return np.arange(int(d*SR))/SR
def pizz(f, d=0.35): t = tt(d); return (np.sin(2*np.pi*f*t) + 0.4*np.sin(2*np.pi*2*f*t))*np.exp(-t*14)
def flute(f, d):
    t = tt(d); v = 1 + 0.006*np.sin(2*np.pi*5.5*t)*np.minimum(1, t/0.3)
    return (np.sin(2*np.pi*f*v*t) + 0.15*np.sin(2*np.pi*2*f*v*t) + 0.02*rng.standard_normal(len(t)))*np.minimum(1, t/0.08)*np.minimum(1, (d-t)/0.12)
def dhol(lo=True): t = tt(0.25); f = 90 if lo else 300; return np.sin(2*np.pi*(f + f*0.8*np.exp(-t*30))*t)*np.exp(-t*(14 if lo else 30))
music = np.zeros(N); beat = 60/104; bar = 4*beat
scale = [62, 64, 66, 69, 71, 74]   # D major-pentatonic-ish
prog = [[50, 57, 62], [55, 59, 62], [52, 57, 61], [50, 57, 62]]
t_ = np.arange(N)/SR; music += (np.sin(2*np.pi*mf(38)*t_) + 0.5*np.sin(2*np.pi*mf(45)*t_))*0.03   # drone
for b in range(int(T/bar)+1):
    ch = prog[b % 4]; t0 = b*bar
    for k in range(8): put(music, pizz(mf(ch[k % 3] + (12 if k % 4 == 3 else 0))), t0 + k*beat/2, 0.12)
    for k, lo in enumerate([1, 0, 0, 1, 0, 1, 0, 0]): put(music, dhol(bool(lo)), t0 + k*beat/2, 0.2 if lo else 0.1)
    if b % 2 == 0:
        mel = [scale[i] + 12 for i in rng.choice(6, 4)]
        for i, m in enumerate(mel): put(music, flute(mf(m), beat*0.9), t0 + i*beat, 0.05)
sfx = np.zeros(N)
def pop(): t = tt(0.1); return np.sin(2*np.pi*(700 + 900*t/0.1)*t)*np.exp(-t*35)
def boing(): t = tt(0.4); return np.sin(2*np.pi*(260 + 120*np.sin(t*45)*np.exp(-t*7))*t)*np.exp(-t*6)
for i in range(3): put(sfx, pop(), S['chai'] + 0.6 + i*0.55, 0.3)
for i in range(3): put(sfx, pop()*0.7, E['chai'] + 0.1 + i*0.2, 0.25)
put(sfx, boing(), S['b2'], 0.35)
for i in range(4): put(sfx, pop(), S['chain'] + 0.4 + i*0.8, 0.3)
put(sfx, boing(), S['t3'] + 0.5, 0.3)
t = tt(2.0); put(sfx, np.sin(2*np.pi*(300 + 400*t/2.0)*t)*np.minimum(1, t/1.5)*0.3, S['cliff'] + 0.2, 0.3)   # mystery rise
put(sfx, flute(mf(81), 1.2), S['cliff'] + 1.3, 0.12)
mix_and_master(D, music, sfx, music_gain=0.7)
