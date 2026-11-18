import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy.signal import butter, sosfilt, resample_poly
from scenes import D, START, PAD0, TOT, KEYS, NUDGE, chunks, CAPS, LINES
SR = 44100; N = int(TOT * SR) + SR; rng = np.random.default_rng(1)
def t_(d): return np.arange(int(d * SR)) / SR
def add(buf, x, at, g=1.0):
    i = int(at * SR); x = x[:max(0, len(buf) - i)]; buf[i:i + len(x)] += x * g
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
music = np.zeros(N); sfx = np.zeros(N); voice = np.zeros(N)
SA = 138.59  # C#
def tanpura(f, d=2.6):
    t = t_(d); x = np.zeros_like(t)
    for h in range(1, 12):
        x += (0.7 ** h) * np.sin(2 * np.pi * f * h * t + 0.3 * np.sin(2 * np.pi * 3 * t) * (h > 3)) * np.exp(-t * (0.7 + 0.22 * h))
    return x * np.minimum(1, t / 0.01)
def pluck(f, d=1.4):
    t = t_(d); x = np.zeros_like(t)
    for h, a in [(1, 1), (2, .5), (3, .25), (4, .12)]:
        x += a * np.sin(2 * np.pi * f * h * t * (1 + 0.0007 * h)) * np.exp(-t * (2.5 + 2 * h))
    return x * np.minimum(1, t / 0.003)
def bell(f=880, d=4.0):
    t = t_(d); x = np.zeros_like(t)
    for r, a, dc in [(1, 1, 1.0), (2.0, .5, 1.6), (2.76, .4, 2.2), (5.4, .2, 3.5), (8.9, .1, 5)]:
        x += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dc)
    return x * np.minimum(1, t / 0.002)
def manjira(d=1.2):
    t = t_(d); x = np.zeros_like(t)
    for f in (3150, 4420, 5870, 7310): x += np.sin(2 * np.pi * f * t) * np.exp(-t * 4)
    return x * 0.25 * np.minimum(1, t / 0.001)
def whoosh(d=0.35):
    x = bp(rng.normal(0, 1, int(d * SR)), 400, 3000); return x * np.sin(np.pi * t_(d) / d) ** 2
def scratch(d):
    x = bp(rng.normal(0, 1, int(d * SR)), 2500, 7000)
    return x * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * t_(d)))) * np.minimum(1, t_(d) / 0.03) * np.minimum(1, (d - t_(d)) / 0.05)
beat = 60 / 66
cyc = [SA * 0.75, SA, SA, SA / 2]
t = 0; i = 0
while t < TOT:
    add(music, tanpura(cyc[i % 4] * 2), t, 0.22); t += beat; i += 1
scale = [1, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2, 9 / 4, 5 / 2]
pat = [0, 2, 3, 4, 5, 4, 3, 2, 0, 3, 5, 7, 6, 5, 3, 4]
t = beat * 2; i = 0
while t < TOT - 1:
    chant = any(START[j] <= t < START[j] + D[j] for j, k in enumerate(KEYS) if LINES[j][2] == 'chant')
    if i % 8 not in (3, 7) and not chant: add(music, pluck(SA * 2 * scale[pat[i % 16]], 2.2), t, 0.09)
    if i % 8 == 0: add(music, manjira(), t, 0.035)
    t += beat / 2; i += 1
add(sfx, bell(1108, 3.5), 0.02, 0.2)
for i in range(1, len(KEYS)): add(sfx, whoosh(), START[i] - 0.15, 0.08)
for i, k in enumerate(KEYS):
    if LINES[i][2] == 'chant': add(sfx, bell(880, 4.5), START[i] + 0.02, 0.24)
    
add(sfx, bell(1318, 3), START[KEYS.index('save')] + 0.05, 0.10)
add(sfx, bell(988, 4), START[-1] + D[-1] - 2.2, 0.14)
for i, k in enumerate(KEYS):
    v, sr = sf.read(f'vo/{k}.wav', dtype='float32')
    if sr != SR: v = resample_poly(v, SR, sr)
    idx = np.where(np.abs(v) > 0.01)[0]; v = v[max(0, idx[0] - 400): idx[-1] + 4000]
    add(voice, v, START[i] + PAD0 + (0.25 if LINES[i][2] == 'chant' else 0), 1.0)
env = np.convolve(np.abs(voice), np.ones(int(0.08 * SR)) / int(0.08 * SR), 'same'); env = np.minimum(1, env / 0.04)
mix = voice + music * (1 - 0.55 * env) * 0.42 + sfx
mix = mix[:int(TOT * SR)]
fo = int(1.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
meter = pyln.Meter(SR)
def soft(x, th=0.6):
    y = x.copy(); o = np.abs(x) > th
    y[o] = np.sign(x[o]) * (th + (1 - th) * np.tanh((np.abs(x[o]) - th) / (1 - th)))
    return y
for _ in range(4):
    mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), -14); mix = soft(mix) * 0.97
print('LUFS', round(meter.integrated_loudness(mix), 2), 'peak', round(float(np.abs(mix).max()), 3))
sf.write('mix.wav', np.stack([mix, mix], 1), SR); print('mix', TOT)
