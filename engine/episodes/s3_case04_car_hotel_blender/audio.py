# S3 score: tense noir pulse (C minor, 84 bpm) — low piano-ish hits, ticking clock, tape hiss, static bursts, CCTV beeps.
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/bk'); from kit import put, mix_and_master, SR
from scipy.signal import butter, lfilter
D = '/home/claude/s3'; VO = json.load(open(f'{D}/vo.json')); S = {l['key']: l['start'] for l in VO['lines']}; T = VO['total']; N = int(SR*T)
rng = np.random.default_rng(8)
def lp(x, f): b, a = butter(2, f/(SR/2)); return lfilter(b, a, x)
def hp(x, f): b, a = butter(2, f/(SR/2), 'high'); return lfilter(b, a, x)
mf = lambda m: 440*2**((m-69)/12)
def tt(d): return np.arange(int(d*SR))/SR
def piano(f, d=1.8): t = tt(d); return sum(np.sin(2*np.pi*f*h*t)*np.exp(-t*(1.8+h*0.9))/h for h in (1, 2, 3, 4))
def pad(f, d): t = tt(d); return (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*1.005*t))*np.minimum(1, t/1.0)*np.minimum(1, (d-t)/1.0)
music = np.zeros(N); beat = 60/84; bar = 4*beat
prog = [[48, 51, 55], [44, 48, 51], [46, 50, 53], [43, 47, 50]]   # Cm Ab Bb G
for b in range(int(T/bar)+1):
    ch = prog[b % 4]; t0 = b*bar
    for m in ch: put(music, pad(mf(m), bar+0.5), t0, 0.05)
    put(music, piano(mf(ch[0]-12), 2.2), t0, 0.2); put(music, piano(mf(ch[0]-12), 1.2), t0 + 2.5*beat, 0.12)
    for k in range(8):   # clock tick
        put(music, hp(rng.standard_normal(int(0.012*SR)), 3000)*np.exp(-tt(0.012)*300), t0 + k*beat/2, 0.08 if k % 2 == 0 else 0.04)
    put(music, piano(mf(ch[2]+12), 1.0), t0 + 1.5*beat, 0.05)
music += hp(rng.standard_normal(N), 4000)*0.004   # tape hiss
# music drops out under the question
a, b = int((S['ask']-0.1)*SR), int((S['clue']-0.2)*SR); music[a:b] *= 0.25
sfx = np.zeros(N)
def static(d=0.35): n = rng.standard_normal(int(d*SR)); return hp(n, 1200)*np.exp(-tt(d)*4)
def beep(f=1400): t = tt(0.12); return np.sin(2*np.pi*f*t)*np.minimum(1, (0.12-t)/0.02)
put(sfx, static(0.4), 0.0, 0.3)
put(sfx, beep(1200), S['solved']-0.05, 0.25); put(sfx, beep(1600), S['solved']+0.1, 0.25)
for k in range(3): put(sfx, beep(1400), S['log']-0.3 + k*0.18, 0.18)
for t_ in (S['stop']+0.6, S['clue'], S['cta']+0.3): put(sfx, static(0.3), t_-0.1, 0.35)
put(sfx, piano(mf(36), 3.0), S['stop']+3.2, 0.5)   # "I'm bankrupt" low hit
put(sfx, piano(mf(72), 1.5) + piano(mf(79), 1.5), S['clue']+0.1, 0.12)
mix_and_master(D, music, sfx, music_gain=0.8)
