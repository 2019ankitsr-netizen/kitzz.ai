# S5 score: wide ambient space (D lydian), slow pads, shimmering arp, sub swells; transit ding-dong; surface rumble.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/bk'); from kit import put, mix_and_master, SR
from scipy.signal import butter, lfilter
D = '/home/claude/s5'; VO = json.load(open(f'{D}/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; T = VO['total']; N = int(SR*T)
rng = np.random.default_rng(5)
def lp(x, f): b, a = butter(2, f/(SR/2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f/(SR/2), 'high'); return lfilter(b, a, x)
mf = lambda m: 440*2**((m-69)/12)
def tt(d): return np.arange(int(d*SR))/SR
def pad(f, d):
    t = tt(d); s = sum(np.sin(2*np.pi*f*(1+dv)*t + ph) for dv, ph in [(0, 0), (0.004, 1), (-0.004, 2), (0.008, 3)])/4
    env = np.minimum(1, t/1.5)*np.minimum(1, (d-t)/1.5); return s*env
def shimmer(f, d=1.2): t = tt(d); return np.sin(2*np.pi*f*t)*np.exp(-t*2.5)*(1+0.3*np.sin(2*np.pi*6*t))
music = np.zeros(N)
chords = [[50, 57, 62, 64, 68], [52, 59, 64, 66, 71], [47, 54, 59, 62, 66], [50, 57, 62, 66, 69]]
seg = 5.5
for b in range(int(T/seg)+1):
    ch = chords[b % 4]; t0 = b*seg
    for m in ch: put(music, pad(mf(m), seg+2), t0-0.8, 0.06)
    put(music, pad(mf(ch[0]-24), seg+2), t0-0.8, 0.12)
    for i in range(11):
        m = ch[[1, 2, 3, 4, 3, 2][i % 6]] + 12
        put(music, shimmer(mf(m)), t0 + i*seg/11, 0.035)
music = lp(music, 4000)
sfx = np.zeros(N)
def ding(f): t = tt(1.0); return sum(np.sin(2*np.pi*f*h*t)*np.exp(-t*(3+h)) for h in (1, 2, 3))/2
for k in ('hook', 'next'):
    put(sfx, ding(659.25), S[k]-0.55, 0.35); put(sfx, ding(523.25), S[k]-0.25, 0.35)
def whoosh(d=1.2): t = tt(d); n = rng.standard_normal(len(t)); return lp(n, 1800)*np.sin(np.pi*t/d)**2
for c in (S['intro']+2.0, S['day']+1.6, S['west']-0.15, S['hot']-0.15, S['next']-0.15, S['cta']-0.1):
    put(sfx, whoosh(), c-0.6, 0.35)
# surface rumble / heat
a, b = S['hot']-0.15, S['next']-0.15; n = rng.standard_normal(int((b-a)*SR)); r = lp(n, 120)*3
env = np.minimum(1, np.arange(len(r))/SR/0.6)*np.minimum(1, (len(r)/SR - np.arange(len(r))/SR)/0.4)
put(sfx, r*env, a, 0.5)
# sizzle when lead melts
n = rng.standard_normal(int(3*SR)); put(sfx, hp(n, 3000)*np.linspace(0, 1, len(n))*np.linspace(1, 0, len(n))**0.5, S['hot']+3.0, 0.08)
mix_and_master(D, music, sfx, music_gain=0.85)
