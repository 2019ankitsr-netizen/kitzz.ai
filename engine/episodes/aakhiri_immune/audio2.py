import wave, sys, numpy as np
from scipy.signal import lfilter
import render2 as E
R = E.R
SR = 48000
TOT = sum(R.DUR); N = int(TOT * SR) + SR
mix = np.zeros(N, np.float32); rng = np.random.default_rng(4)
S = R.START
def add(sig, t0, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig)); mix[i:j] += g * sig[:j - i]
def tone(f0, f1, dur, decay=8.0):
    t = np.arange(int(dur * SR)) / SR; f = np.linspace(f0, f1, len(t))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)).astype(np.float32)
def lp(x, a): return lfilter([a], [1, a - 1], x).astype(np.float32)
def knock(t0, g=0.6):
    add(tone(95, 60, 0.25, 22), t0, g); n = lp(rng.normal(0, 1, int(0.08 * SR)).astype(np.float32), 0.15) * np.exp(-np.arange(int(0.08 * SR)) / SR * 50); add(n, t0, g * 1.4)
def boom(t0, g=0.5):
    add(tone(70, 32, 1.6, 2.5), t0, g); n = lp(rng.normal(0, 1, int(1.2 * SR)).astype(np.float32), 0.05) * np.exp(-np.arange(int(1.2 * SR)) / SR * 4); add(n, t0, g * 0.5)

t = np.arange(N) / SR
pad = (np.sin(2 * np.pi * 49 * t) * 0.5 + np.sin(2 * np.pi * 73.4 * t) * 0.3 + np.sin(2 * np.pi * 98 * t) * 0.15) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.08 * t))
noise = lp(rng.normal(0, 1, N).astype(np.float32), 0.004) * 6
end_vo = S[7] + R.DUR[7] - 2.6
env = np.clip(t / 1.5, 0, 1) * np.where(t > end_vo, np.exp(-(t - end_vo) * 6), 1) * (0.8 + 0.5 * np.clip((t - S[5]) / 20, 0, 1))
mix += (pad * 0.05 + noise * 0.03) * env
# S1 knocks
for k in E.KNOCKS_S1: knock(S[0] + k)
boom(S[0] + 1.2, 0.3)
# S2 emergency alert: harsh two-tone
for k in range(4):
    add(tone(853, 853, 0.45, 0.5) + tone(960, 960, 0.45, 0.5), S[1] + 0.3 + k * 0.5, 0.05)
# S3 ECG beeps then flatline
tb = 0.3
while tb < 4.2:
    add(tone(1000, 1000, 0.09, 25), S[2] + tb, 0.10); tb += 0.62
add(tone(1000, 1000, max(0.5, R.DUR[2] - 4.3), 0.15), S[2] + 4.2, 0.07)
add(rng.normal(0, 1, int(0.15 * SR)).astype(np.float32), S[2] + 4.2, 0.08)
# S4 type clicks for each row
for k in range(7):
    for j in range(5):
        c = rng.normal(0, 1, 500).astype(np.float32) * np.exp(-np.arange(500) / 70); add(c, S[3] + 0.4 + k * 0.75 + j * 0.05, 0.05)
    add(tone(140, 90, 0.3, 10), S[3] + 0.75 + k * 0.75, 0.12)
# S5 heartbeat slow
tb = S[4] + 0.4
while tb < S[5] - 0.3:
    add(tone(60, 40, 0.18, 22), tb, 0.3); add(tone(55, 38, 0.15, 25), tb + 0.22, 0.2); tb += 1.0
# S6 engines + doors
eng = lp(rng.normal(0, 1, int(R.DUR[5] * SR)).astype(np.float32), 0.01) * 3
eng *= np.clip(np.linspace(0, 3.0, len(eng)), 0, 1) * np.clip(np.linspace(3, -1, len(eng)), 0.15, 1)
add(eng, S[5], 0.35)
for k in (2.7, 3.0, 3.25): add(tone(110, 70, 0.2, 18), S[5] + k, 0.25)
# S7 knocks
for k in E.KNOCKS_S7: knock(S[6] + k, 0.75)
# S8 wind + crowd moans + riser + boom
wind = lp(rng.normal(0, 1, int(R.DUR[7] * SR)).astype(np.float32), 0.03); add(wind, S[7], 0.35)
for k in range(5):
    m = tone(140 + k * 9, 110 + k * 7, 1.6, 0.8) * np.sin(np.linspace(0, np.pi, int(1.6 * SR))); add(m.astype(np.float32), S[7] + 1.0 + k * 0.7, 0.05)
riser = lp(rng.normal(0, 1, int(2.0 * SR)).astype(np.float32), 0.08) * np.linspace(0, 1, int(2.0 * SR)) ** 2; add(riser, end_vo - 2.0, 0.6)
boom(end_vo, 0.8)

vo = np.zeros(N, np.float32)
for i in range(8):
    w = wave.open(f'vo2/{i + 1}_48.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    j = int((S[i] + R.VO_OFF) * SR); vo[j:j + len(a)] += a
duck = 1 - 0.35 * np.clip(lp(np.abs(vo), 0.001) * 12, 0, 1)
out = (mix * duck + vo * 1.05)[:int(TOT * SR)]
out = np.tanh(out * 1.1) / np.tanh(1.1); out = out / np.abs(out).max() * 0.93
wv = wave.open('mix.wav', 'wb'); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype(np.int16).tobytes()); wv.close()
print('ok', TOT)
