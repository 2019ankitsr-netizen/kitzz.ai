import wave, sys, numpy as np
from scipy.signal import lfilter
sys.path.insert(0, '/home/claude/ep1')
import render as R
EP = sys.argv[1]
SR = 48000; TOT = sum(R.DUR); N = int(TOT * SR) + SR
mix = np.zeros(N, np.float32); rng = np.random.default_rng(11); S = R.START; D = R.DUR
def add(sig, t0, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig)); mix[i:j] += g * sig[:j - i]
def tone(f0, f1, dur, decay=8.0):
    t = np.arange(int(dur * SR)) / SR; f = np.linspace(f0, f1, len(t))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)).astype(np.float32)
def lp(x, a): return lfilter([a], [1, a - 1], x).astype(np.float32)
def noise(d): return rng.normal(0, 1, int(d * SR)).astype(np.float32)
def boom(t0, g=0.5): add(tone(70, 32, 1.6, 2.5), t0, g); add(lp(noise(1.2), 0.05) * np.exp(-np.arange(int(1.2 * SR)) / SR * 4), t0, g * 0.5)
def crackle(t0, dur, g):
    x = np.zeros(int(dur * SR), np.float32)
    for k in range(int(dur * 25)):
        i = rng.integers(0, len(x) - 300); x[i:i + 300] += rng.normal(0, 1, 300) * np.exp(-np.arange(300) / 50)
    add(lp(x, 0.5) + lp(noise(dur), 0.02) * 2, t0, g)
def heart(t0, t1, iv, g):
    tb = t0
    while tb < t1: add(tone(60, 40, 0.18, 22), tb, g); add(tone(55, 38, 0.15, 25), tb + 0.2, g * 0.7); tb += iv
t = np.arange(N) / SR
end_vo = S[7] + D[7] - 2.6
if EP == '4':
    pad = (np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 65.4 * t) * 0.3 + np.sin(2 * np.pi * 82.4 * t) * 0.2)
    add(lp(noise(D[0] + D[1] + D[2]), 0.02), 0, 0.25)  # wind
    add(tone(1200, 1200, 0.04, 40), S[0] + 2.0, 0.2); add(tone(400, 300, 0.08, 30), S[0] + 2.0, 0.2)  # gun click
    add(tone(1000, 1000, 0.04, 40), S[1] + 0.3, 0.15)
    crackle(S[3], D[3] + D[4], 0.12)
    add(tone(700, 500, 0.12, 20), S[3] + (D[3] - 0.55) * 0.25, 0.15)  # card drop
    heart(S[4] + 0.5, S[5] - 0.2, 0.7, 0.3)
    crackle(S[5], D[5], 0.08)
    for k in range(5): add(lp(noise(0.05), 0.3) * 0.8, S[5] + 1 + k * 1.2, 0.12)  # pen scratch
    heli = np.arange(int((D[6] + D[7]) * SR)) / SR
    add((lp(noise(len(heli) / SR), 0.05) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 11 * heli)))).astype(np.float32) * 3, S[6], 0.18)
    boom(S[6], 0.4)
    heart(S[7] + 0.3, end_vo - 0.2, 0.55, 0.35)
else:
    pad = (np.sin(2 * np.pi * 49 * t) * 0.5 + np.sin(2 * np.pi * 61.7 * t) * 0.3 + np.sin(2 * np.pi * 73.4 * t) * 0.2)
    tb = S[0] + 0.3
    while tb < S[4]: add(tone(1000, 1000, 0.08, 25), tb, 0.06); tb += 0.8   # monitor beeps
    add(lp(noise(0.6), 0.1) * np.linspace(1, 0, int(0.6 * SR)), S[1] + 0.1, 0.25)  # door hiss
    for k in range(6): add(tone(90, 60, 0.12, 25), S[1] + 1.0 + k * 0.35, 0.15)  # footsteps
    add(tone(300, 200, 0.06, 40), S[3] + 1.1, 0.25); add(tone(260, 180, 0.06, 40), S[3] + 2.6, 0.25)  # buckle
    al = np.arange(int(D[4] * SR)) / SR
    add((np.sign(np.sin(2 * np.pi * (700 + 200 * (np.floor(al * 3) % 2)) * al)) * 0.3).astype(np.float32), S[4], 0.06)
    for k in range(8): add(lp(noise(0.15), 0.3) * np.exp(-np.arange(int(0.15 * SR)) / SR * 15), S[4] + 0.5 + k * 0.8, 0.3)
    boom(S[4], 0.4)
    add(tone(1500, 1500, 1.5, 1.5) * 0.4 + tone(1507, 1507, 1.5, 1.5) * 0.4, S[5] + 0.2, 0.05)
    heart(S[5] + 0.5, S[7] - 0.3, 0.9, 0.3)
    # hopeful major chord rising in final scene
    ft = np.arange(int((D[7] - 2.6) * SR)) / SR
    ch = sum(np.sin(2 * np.pi * f * ft) for f in (196, 247, 294, 392)) * np.clip(ft / 2.0, 0, 1) * 0.25
    add(ch.astype(np.float32), S[7], 0.12)
    for k in range(3): add(tone(1320, 1320, 0.12, 30), S[7] + (D[7] - 2.6) * 0.55 + k * 0.05, 0.12 if k == 0 else 0)
    add(tone(880, 1100, 0.15, 20), S[7] + (D[7] - 2.6) * 0.55 + 1.6, 0.15)
env = np.clip(t / 1.5, 0, 1) * np.where(t > end_vo, np.exp(-(t - end_vo) * 5), 1)
mix += (pad * (0.05 if EP == '4' else 0.04) + lp(noise(N / SR), 0.004)[:N] * 6 * 0.03) * env
add(lp(noise(2.0), 0.08) * np.linspace(0, 1, int(2.0 * SR)) ** 2, end_vo - 2.0, 0.45 if EP == '4' else 0.2)
boom(end_vo, 0.7 if EP == '4' else 0.45)
vo = np.zeros(N, np.float32)
for i in range(8):
    w = wave.open(f'vo2/{i + 1}_48.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    j = int((S[i] + R.VO_OFF) * SR); vo[j:j + len(a)] += a
duck = 1 - 0.4 * np.clip(lp(np.abs(vo), 0.001) * 12, 0, 1)
out = (mix * duck + vo * 1.05)[:int(TOT * SR)]
out = np.tanh(out * 1.1) / np.tanh(1.1); out = out / np.abs(out).max() * 0.93
wv = wave.open('mix.wav', 'wb'); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype(np.int16).tobytes()); wv.close(); print('ok', TOT)
