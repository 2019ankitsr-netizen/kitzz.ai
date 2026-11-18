import wave, numpy as np
from scipy.signal import lfilter
import render3 as E
R = E.R; SR = 48000
TOT = sum(R.DUR); N = int(TOT * SR) + SR
mix = np.zeros(N, np.float32); rng = np.random.default_rng(6); S = R.START; D = R.DUR
def add(sig, t0, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig)); mix[i:j] += g * sig[:j - i]
def tone(f0, f1, dur, decay=8.0):
    t = np.arange(int(dur * SR)) / SR; f = np.linspace(f0, f1, len(t))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)).astype(np.float32)
def lp(x, a): return lfilter([a], [1, a - 1], x).astype(np.float32)
def noise(d): return rng.normal(0, 1, int(d * SR)).astype(np.float32)
def engine(dur, f=38, rough=0.6):
    t = np.arange(int(dur * SR)) / SR
    base = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * 2 * t) * 0.3
    return lp((base * (1 + rough * lp(noise(dur), 0.01) * 3)).astype(np.float32), 0.08)
def boom(t0, g=0.5): add(tone(70, 32, 1.6, 2.5), t0, g); add(lp(noise(1.2), 0.05) * np.exp(-np.arange(int(1.2 * SR)) / SR * 4), t0, g * 0.5)
t = np.arange(N) / SR
pad = (np.sin(2 * np.pi * 52 * t) * 0.5 + np.sin(2 * np.pi * 78 * t) * 0.3 + np.sin(2 * np.pi * 104 * t) * 0.15) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t))
end_vo = S[7] + D[7] - 2.6
env = np.clip(t / 1.5, 0, 1) * np.where(t > end_vo, np.exp(-(t - end_vo) * 6), 1)
mix += (pad * 0.05 + lp(noise(N / SR), 0.004)[:N] * 6 * 0.03) * env
# S1 wind + distant siren
add(lp(noise(D[0]), 0.03), S[0], 0.35)
st = np.arange(int(D[0] * SR)) / SR; add((np.sin(2 * np.pi * np.cumsum(600 + 200 * np.sin(2 * np.pi * 0.4 * st)) / SR) * 0.5).astype(np.float32), S[0], 0.015)
# S2 scrapes, kicks, engine start
for k in range(8): add(lp(noise(0.12), 0.2) * np.exp(-np.arange(int(0.12 * SR)) / SR * 20), S[1] + 0.4 + k * 0.45, 0.25)
vd = D[1] - 0.55
for k in range(3): add(tone(80, 40, 0.3, 10) + lp(noise(0.3), 0.1) * np.exp(-np.arange(int(0.3 * SR)) / SR * 12), S[1] + vd - 2.6 + k * 0.65, 0.35)
add(engine(1.2) * np.linspace(0, 1, int(1.2 * SR)), S[1] + vd - 0.6, 0.18)
# S3 riding
e = engine(D[2], 46); add(e, S[2], 0.18); add(lp(noise(D[2]), 0.06), S[2], 0.25)
# S4 idle then crowd moans
add(engine(D[3] - 1.0, 34) * np.linspace(1, 0.6, int((D[3] - 1.0) * SR)), S[3], 0.12)
turn = S[3] + D[3] - 0.55 - 1.6
for k in range(8): add(tone(130 + k * 8, 100 + k * 6, 1.8, 0.7) * np.sin(np.linspace(0, np.pi, int(1.8 * SR))).astype(np.float32), turn + k * 0.12, 0.05)
add(tone(1200, 1200, 0.05, 30), turn, 0.0)
# S5 engine off click, heartbeat fast
add(tone(300, 100, 0.08, 40), S[4] + 0.1, 0.3)
tb = S[4] + 0.3
while tb < S[5] - 0.2: add(tone(60, 40, 0.18, 22), tb, 0.35); add(tone(55, 38, 0.15, 25), tb + 0.2, 0.25); tb += 0.62
# S6 drone buzz
dt_ = np.arange(int(D[5] * SR)) / SR
buzz = ((2 * ((180 + 6 * np.sin(2 * np.pi * 0.5 * dt_)) * dt_ % 1) - 1) * 0.4 + np.sin(2 * np.pi * 360 * dt_) * 0.2).astype(np.float32)
add(lp(buzz, 0.3) * np.clip(dt_ / 1.0, 0, 1).astype(np.float32), S[5], 0.12)
for k in range(int(D[5] * 2)): add(tone(1800, 1800, 0.06, 30), S[5] + 0.3 + k * 0.5, 0.04)
# S7: radio static under
add(lp(noise(D[6]), 0.5) * 0.3, S[6], 0.06)
# S8 engine fading + warm pad + riser + boom
add(engine(D[7] - 2.6, 44) * np.linspace(1, 0.2, int((D[7] - 2.6) * SR)), S[7], 0.12)
add(lp(noise(2.0), 0.08) * np.linspace(0, 1, int(2.0 * SR)) ** 2, end_vo - 2.0, 0.5)
boom(end_vo, 0.7)
vo = np.zeros(N, np.float32)
for i in range(8):
    w = wave.open(f'vo2/{i + 1}_48.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    j = int((S[i] + R.VO_OFF) * SR); vo[j:j + len(a)] += a
duck = 1 - 0.4 * np.clip(lp(np.abs(vo), 0.001) * 12, 0, 1)
out = (mix * duck + vo * 1.05)[:int(TOT * SR)]
out = np.tanh(out * 1.1) / np.tanh(1.1); out = out / np.abs(out).max() * 0.93
wv = wave.open('mix.wav', 'wb'); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype(np.int16).tobytes()); wv.close(); print('ok', TOT)
