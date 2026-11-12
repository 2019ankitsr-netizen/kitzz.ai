# S4 score: bouncy pop (122 bpm, F major), punchy kick/clap, plucky bass, cut whooshes, geiger clicks, boings.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/bk'); from kit import put, mix_and_master, SR
from scipy.signal import butter, lfilter
D = '/home/claude/s4'; VO = json.load(open(f'{D}/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; T = VO['total']; N = int(SR*T)
rng = np.random.default_rng(2)
def lp(x, f): b, a = butter(2, f/(SR/2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f/(SR/2), 'high'); return lfilter(b, a, x)
mf = lambda m: 440*2**((m-69)/12)
def tt(d): return np.arange(int(d*SR))/SR
def pluck(f, d=0.3): t = tt(d); return (np.sign(np.sin(2*np.pi*f*t))*0.3 + np.sin(2*np.pi*f*t))*np.exp(-t*9)
def bell(f, d=0.5): t = tt(d); return np.sin(2*np.pi*f*t + 0.8*np.sin(2*np.pi*f*3.5*t)*np.exp(-t*6))*np.exp(-t*7)
def kick(): t = tt(0.3); return np.sin(2*np.pi*(50 + 110*np.exp(-t*28))*t)*np.exp(-t*10)
def clap(): t = tt(0.18); n = rng.standard_normal(len(t)); return hp(lp(n, 3000), 900)*(np.exp(-t*30) + 0.5*np.exp(-(t-0.012).clip(0)*40)*(t > 0.012))
def hat(): t = tt(0.05); return hp(rng.standard_normal(len(t)), 8000)*np.exp(-t*90)
bpm = 122; beat = 60/bpm; bar = 4*beat
prog = [[53, 57, 60], [50, 53, 57], [46, 50, 53], [48, 52, 55]]   # F Dm Bb C
music = np.zeros(N)
for b in range(int(T/bar)+1):
    ch = prog[b % 4]; t0 = b*bar
    for k in range(8):
        put(music, pluck(mf(ch[0]-12 if k % 2 == 0 else ch[0]), 0.25), t0 + k*beat/2, 0.16)
    for k in range(4):
        put(music, kick(), t0 + k*beat, 0.5)
        if k % 2: put(music, clap(), t0 + k*beat, 0.35)
        put(music, hat(), t0 + k*beat + beat/2, 0.12)
    mel = [ch[2]+12, ch[1]+12, ch[2]+12, ch[0]+24, ch[2]+12, ch[1]+12]
    for i, m in enumerate(mel): put(music, bell(mf(m), 0.4), t0 + i*beat*0.66, 0.07)
sfx = np.zeros(N)
def whoosh(d=0.35): t = tt(d); n = rng.standard_normal(len(t)); return hp(lp(n, 5000), 600)*np.sin(np.pi*t/d)**2
def boing(f=220): t = tt(0.35); return np.sin(2*np.pi*(f + 160*np.sin(t*40)*np.exp(-t*8))*t)*np.exp(-t*7)
def pop(): t = tt(0.08); return np.sin(2*np.pi*(900 - 600*t/0.08)*t)*np.exp(-t*40)
def click(): t = tt(0.006); return rng.standard_normal(len(t))*np.exp(-t*900)
cuts = [S['why']-0.1, S['why']+3.4, S['dose']-0.15, S['xray']-0.15, S['safe']-0.15, S['unit']-0.15, S['cta']-0.15]
for c in cuts: put(sfx, whoosh(), c-0.12, 0.5)
for i in range(3): put(sfx, boing(200 + 40*i), 0.42 + i*0.12, 0.3)
put(sfx, pop(), 0.45, 0.5)
put(sfx, pop(), S['why'] + 2.2, 0.5)
t = S['why'] + 4.8; put(sfx, bell(1760, 0.6) + bell(2637, 0.6), t, 0.25)
# geiger crackle during the dose shot
tc = cuts[2]
while tc < cuts[3]:
    put(sfx, click(), tc, 0.6); tc += rng.exponential(0.07)
# pile rain: many soft thumps
for i in range(50): put(sfx, boing(150 + rng.uniform(-30, 60))*0.5, S['xray'] - 0.15 + 0.3 + i*0.034 + 0.36, 0.12)
put(sfx, pop(), S['unit'] + 1.6, 0.5)
for c in (S['xray'] + 2.6, S['cta'] + 0.1): put(sfx, pop(), c, 0.35)
for i in range(3): put(sfx, whoosh(0.3)*0.6, T - 0.45 + i*0.05, 0.4)
mix_and_master(D, music, sfx, music_gain=0.6)
