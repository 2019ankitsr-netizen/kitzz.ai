import json, numpy as np, soundfile as sf, scipy.signal as ss
SR = 48000
TL = json.load(open('web/manthan_timeline.json')); S = TL['S']; END = TL['end']
n = int(END * SR); t = np.arange(n) / SR
rng = np.random.default_rng(5)
mus = np.zeros(n)
SA = 130.81  # C3

def pluck(f, at, amp, dur=3.5, buzz=.5):
    i = int(at * SR); L = min(int(dur * SR), n - i)
    if L <= 0: return
    tt = np.arange(L) / SR
    s = np.zeros(L)
    for h in range(1, 14):  # jawari-ish rich harmonics, upper ones decay slower (buzz)
        s += (1 / h) * np.sin(2 * np.pi * f * h * tt + h) * np.exp(-tt * (1.6 - buzz * min(h, 8) / 8 * 1.1))
    s *= np.minimum(1, tt / .01)
    mus[i:i+L] += amp * s

# tanpura cycle Pa Sa Sa Sa(low), ~ 4.6 s cycle, whole length (loop-safe)
cyc = 4.6
for c0 in np.arange(-cyc, END, cyc):
    for k, f in enumerate([SA * 1.5 / 2, SA, SA, SA / 2]):
        at = c0 + k * cyc / 4
        if at >= 0: pluck(f, at, .05)
# low drone pad
for f in (SA / 2, SA / 2 * 1.5):
    mus += .03 * np.sin(2 * np.pi * f * t) * (0.7 + .3 * np.sin(2 * np.pi * t / 9))

def bell(at, f=880, amp=.18, d=4):
    i = int(at * SR); L = min(int(d * SR), n - i); tt = np.arange(L) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * tt) * np.exp(-tt * dd) for r, a, dd in ((1, 1, 1.2), (2.76, .5, 2.2), (5.4, .25, 3.5), (8.9, .12, 5)))
    mus[i:i+L] += amp * s

def conch(at, amp=.22, d=3.0, f=SA):
    i = int(at * SR); L = min(int(d * SR), n - i); tt = np.arange(L) / SR
    e = np.minimum(1, tt / .5) * np.minimum(1, (d - tt) / .8)
    vib = 1 + .004 * np.sin(2 * np.pi * 5 * tt)
    s = sum((1 / h ** 1.3) * np.sin(2 * np.pi * f * h * vib * tt) for h in range(1, 9))
    no = np.convolve(rng.standard_normal(L), np.ones(30) / 30, 'same') * .3
    mus[i:i+L] += amp * e * (s + no)

conch(0.0, .22, 3.2)
bell(S['ocean'] + 2.0, 1046, .12)
bell(S['vasuki'] + .1, 784, .12)
bell(S['kurma'] + 2.0, 659, .14)
# poison: low dissonant swell
i0, i1 = int(S['poison'] * SR), int((S['shiva'] + 1) * SR); tt = np.arange(i1 - i0) / SR
sw = np.minimum(1, tt / 2.5) * np.minimum(1, (tt[-1] - tt) / 1.0)
mus[i0:i1] += .1 * sw * (np.sin(2 * np.pi * 55 * tt) + .7 * np.sin(2 * np.pi * 58.3 * tt) + .4 * np.sin(2 * np.pi * 82.4 * tt * (1 + .002 * tt)))
bell(S['shiva'] + 2.2, 523, .22, 5)   # Neelkanth temple bell
bell(S['shiva'] + 2.9, 523, .12, 5)
for k in range(4): bell(S['ratna'] + 0.7 + k * .55, [1318, 1568, 1760, 2093][k], .08, 2)
# amrit choir pad
i0, i1 = int(S['amrit'] * SR), int((S['cta'] + .5) * SR); tt = np.arange(i1 - i0) / SR
sw = np.minimum(1, tt / 2) * np.minimum(1, (tt[-1] - tt) / 1.5)
mus[i0:i1] += .05 * sw * sum(np.sin(2 * np.pi * f * tt) * (1 + .3 * np.sin(2 * np.pi * .3 * tt + f)) for f in (SA * 2, SA * 2.5, SA * 3, SA * 4))
bell(S['lesson'] + 2.0, 698, .14, 4)

vo = np.zeros(n)
for l in TL['lines']:
    a, sr = sf.read(f"vo/manthan/{l['id']}.wav"); a = ss.resample_poly(a, 2, 1)
    i = int(l['start'] * SR); vo[i:i+len(a)] += a[:n-i]
act = np.convolve((np.abs(vo) > .01).astype(float), np.ones(int(.3 * SR)) / int(.3 * SR), 'same')
duck = 1 - .4 * np.clip(act * 3, 0, 1)
mix = vo + mus * duck * 1.1
mix[:int(.02*SR)] *= np.linspace(0, 1, int(.02*SR)); mix[-int(.05*SR):] *= np.linspace(1, 0, int(.05*SR))
mix /= np.abs(mix).max() / .9
sf.write('mix_manthan.wav', np.stack([mix, mix], 1), SR); print('ok')
