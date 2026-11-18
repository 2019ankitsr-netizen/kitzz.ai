import wave, numpy as np, math
import render as R

SR = 48000
TOT = sum(R.DUR)
N = int(TOT * SR) + SR
mix = np.zeros(N, np.float32)
rng = np.random.default_rng(1)

def add(sig, t0, g=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig)); mix[i:j] += g * sig[:j - i]

def tone(f0, f1, dur, decay=8.0):
    t = np.arange(int(dur * SR)) / SR
    f = np.linspace(f0, f1, len(t)); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * decay)).astype(np.float32)

def lp(x, a):
    y = np.zeros_like(x); acc = 0.0
    # vectorized one-pole via lfilter-like loop in chunks
    from scipy.signal import lfilter
    return lfilter([a], [1, a - 1], x).astype(np.float32)

# --- pad: low drone across the whole thing, swelling at the end
t = np.arange(N) / SR
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
pad = (np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 82.4 * t) * 0.3 + np.sin(2 * np.pi * 110.3 * t) * 0.18) * lfo
noise = lp(rng.normal(0, 1, N).astype(np.float32), 0.004) * 6
env = np.clip(t / 2.0, 0, 1) * (0.7 + 0.6 * np.clip((t - R.START[7]) / (R.DUR[7] - 2.6), 0, 1))
end_vo = R.START[7] + R.DUR[7] - 2.6
env = env * np.where(t > end_vo, np.exp(-(t - end_vo) * 6), 1)
mix += (pad * 0.05 + noise * 0.03) * env

def notif_ping(t0):
    add(tone(1320, 1320, 0.12, 30), t0, 0.18); add(tone(990, 990, 0.25, 18), t0 + 0.09, 0.18)
def err(t0):
    s = tone(180, 140, 0.35, 9); s = np.sign(s) * np.abs(s) ** 0.5 * np.exp(-np.arange(len(s)) / SR * 9)
    add(s.astype(np.float32), t0, 0.12)
def boom(t0, g=0.5):
    s = tone(70, 32, 1.6, 2.5); n = lp(rng.normal(0, 1, int(1.2 * SR)).astype(np.float32), 0.05) * np.exp(-np.arange(int(1.2 * SR)) / SR * 4)
    add(s, t0, g); add(n, t0, g * 0.5)

# S1
S = R.START
notif_ping(S[0] + 0.45); err(S[0] + 0.75); boom(S[0] + 3.6, 0.35)
# S3 cancels
for c in R.CANCEL_T: notif_ping(S[2] + c - 0.05); err(S[2] + c + 0.1)
# S4 birds / wind
wind = lp(rng.normal(0, 1, int(R.DUR[3] * SR)).astype(np.float32), 0.02)
wind *= (0.6 + 0.4 * np.sin(np.linspace(0, 6, len(wind))))
add(wind, S[3], 0.25)
for k in range(3): add(tone(3200, 2600, 0.12, 25), S[3] + 1.2 + k * 0.9, 0.04)
# S5 message pops & typing
add(tone(880, 1100, 0.15, 20), S[4] + R.S5_USER, 0.15)
for k in range(int((R.S5_REPLY - R.S5_TYPING) / 0.11)):
    c = rng.normal(0, 1, 600).astype(np.float32) * np.exp(-np.arange(600) / 80); add(c, S[4] + R.S5_TYPING + k * 0.11, 0.05)
add(tone(660, 880, 0.2, 14), S[4] + R.S5_REPLY, 0.18)
# S6
add(tone(880, 1100, 0.15, 20), S[5] + R.S6_ASK, 0.15)
for o in R.S6_OFF: add(tone(620, 300, 0.18, 14), S[5] + o, 0.14)
# S7 static + news sting
st = rng.normal(0, 1, int(0.7 * SR)).astype(np.float32); add(st, S[6], 0.07)
boom(S[6] + 0.7, 0.3)
add(tone(440, 440, 0.6, 3) + tone(554, 554, 0.6, 3) * 0.7, S[6] + 0.72, 0.08)
# S8 heartbeat accelerating, then hit
tb = S[7] + 0.5; iv = 1.0
while tb < end_vo - 0.2:
    g = 0.25 + 0.35 * (tb - S[7]) / (end_vo - S[7])
    add(tone(60, 40, 0.18, 22), tb, g); add(tone(55, 38, 0.15, 25), tb + 0.22, g * 0.7)
    tb += iv; iv = max(0.55, iv * 0.93)
riser = rng.normal(0, 1, int(2.0 * SR)).astype(np.float32)
riser = lp(riser, 0.08) * np.linspace(0, 1, len(riser)) ** 2
add(riser, end_vo - 2.0, 0.6)
boom(end_vo, 0.8)
add(tone(1500, 1500, 1.8, 2.5) * 0.3 + tone(1513, 1513, 1.8, 2.5) * 0.3, end_vo + 0.5, 0.05)

# VO with light ducking
vo = np.zeros(N, np.float32)
for i in range(8):
    w = wave.open(f'vo2/{i + 1}_48.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    j = int((S[i] + R.VO_OFF) * SR); vo[j:j + len(a)] += a
duck = 1 - 0.35 * np.clip(lp(np.abs(vo), 0.001) * 12, 0, 1)
out = mix * duck + vo * 1.05
out = out[:int(TOT * SR)]
out = np.tanh(out * 1.1) / np.tanh(1.1) * 0.95
pk = np.abs(out).max(); out = out / pk * 0.93
wv = wave.open('mix.wav', 'wb'); wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
wv.writeframes((out * 32767).astype(np.int16).tobytes()); wv.close()
print('ok', TOT)
