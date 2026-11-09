import numpy as np, soundfile as sf, json
from scipy.signal import butter, sosfilt
from scenes import D, START, PAD0, cap_times
SR = 44100; TOT = sum(D); N = int(TOT * SR) + SR
rng = np.random.default_rng(1)
def t_(d): return np.arange(int(d * SR)) / SR
def add(buf, x, at, g=1.0):
    i = int(at * SR); x = x[:max(0, len(buf) - i)]; buf[i:i + len(x)] += x * g
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)

music = np.zeros(N); sfx = np.zeros(N); voice = np.zeros(N)
SA = 146.83
def tanpura(f, d=2.4):
    t = t_(d); x = np.zeros_like(t)
    for h in range(1, 12):
        x += (0.7 ** h) * np.sin(2 * np.pi * f * h * t + 0.3 * np.sin(2 * np.pi * 3 * t) * (h > 3)) * np.exp(-t * (0.8 + 0.25 * h))
    return x * np.minimum(1, t / 0.01)
def pluck(f, d=1.2):
    t = t_(d); x = np.zeros_like(t)
    for h, a in [(1, 1), (2, .5), (3, .25), (4, .12)]:
        x += a * np.sin(2 * np.pi * f * h * t * (1 + 0.0007 * h)) * np.exp(-t * (3 + 2 * h))
    return x * np.minimum(1, t / 0.003)
def thump(d=0.5):
    t = t_(d); f = 70 + 80 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def bell(f=880, d=4.0):
    t = t_(d); x = np.zeros_like(t)
    for r, a, dc in [(1, 1, 1.0), (2.0, .5, 1.6), (2.76, .4, 2.2), (5.4, .2, 3.5), (8.9, .1, 5)]:
        x += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dc)
    return x * np.minimum(1, t / 0.002)

beat = 60 / 92
# tanpura cycle Pa Sa' Sa' Sa
cyc = [SA * 1.5 / 2, SA, SA, SA / 2]
t = 0; i = 0
while t < TOT:
    add(music, tanpura(cyc[i % 4] * 2), t, 0.22); t += beat * 1.0; i += 1
# bhupali plucks
scale = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2, 9 / 4, 5 / 2]
pat = [0, 2, 3, 4, 5, 4, 3, 2, 0, 3, 5, 7, 6, 5, 3, 4]
t = beat * 2; i = 0
while t < TOT - 1:
    if not (i % 8 in (3, 7)):
        add(music, pluck(SA * 2 * scale[pat[i % 16]]), t, 0.16)
    t += beat / 2; i += 1
t = 0; i = 0
while t < TOT:
    if i % 4 in (0, 2): add(music, thump(), t, 0.35 if i % 4 == 0 else 0.2)
    t += beat; i += 1

def scratch(d):
    x = rng.normal(0, 1, int(d * SR)); x = bp(x, 2500, 7000)
    env = (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * t_(d)))) * np.minimum(1, t_(d) / 0.03) * np.minimum(1, (d - t_(d)) / 0.05)
    return x * env
def whoosh(d=0.35):
    x = bp(rng.normal(0, 1, int(d * SR)), 400, 3000); tt = t_(d)
    return x * np.sin(np.pi * tt / d) ** 2

add(sfx, bell(1046, 3), 0.02, 0.18)
add(sfx, scratch(0.6), 0.55, 0.12)
for i in range(1, 9): add(sfx, whoosh(), START[i] - 0.15, 0.10)
add(sfx, bell(880, 4), START[1] + 4.7, 0.22)
for r in range(4):
    for side in (0, 1):
        t0 = 1.2 + (r * 2 + side) * 0.5 + 0.12
        add(sfx, scratch(0.33), START[2] + t0, 0.10)
add(sfx, bell(1174, 3), START[4] + 0.9, 0.16)
ct = cap_times(7); add(sfx, scratch(ct[1][1] - ct[1][0] + 0.4), START[7] + ct[1][0] - 0.2, 0.10)
add(sfx, bell(988, 3), START[8] + 0.1, 0.12)

from scipy.signal import resample_poly
for i in range(9):
    v, sr = sf.read(f'v{i}.wav'); v = resample_poly(v, 147, 80)
    add(voice, v, START[i] + PAD0, 1.0)
# ducking
env = np.abs(voice); k = int(0.08 * SR)
env = np.convolve(env, np.ones(k) / k, 'same'); env = np.minimum(1, env / 0.05)
duck = 1 - 0.55 * env
mix = voice * 1.0 + music * duck * 0.5 + sfx
mix = mix[:int(TOT * SR)]
mix /= np.max(np.abs(mix)) * 1.05
sf.write('mix.wav', np.stack([mix, mix], 1), SR)
print('ok', TOT)
