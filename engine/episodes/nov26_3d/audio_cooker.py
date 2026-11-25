import json, numpy as np, soundfile as sf
SR = 48000
TL = json.load(open('web/cooker_timeline.json')); S = TL['S']; END = TL['end']
n = int(END * SR); t = np.arange(n) / SR
rng = np.random.default_rng(3)

def env(a, b, fa=.3, fb=.5):
    e = np.clip((t - a) / fa, 0, 1) * np.clip((b - t) / fb, 0, 1)
    return e

mus = np.zeros(n)
# drone pad: A minor-ish, slow detuned saws filtered by simple averaging
def pad(freqs, amp, a, b):
    global mus
    e = env(a, b, 1.2, 1.5)
    for f in freqs:
        for d in (-0.15, 0.15):
            ph = 2 * np.pi * (f + d) * t
            mus += amp * e * (np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph))
pad([110, 164.8, 220], .03, 0, END)
bpm = 112; beat = 60 / bpm
for j,k in enumerate(np.arange(0.2, END, beat)):
    i = int(k * SR); L = int(.25 * SR)
    if i + L > n: break
    tt = np.arange(L) / SR
    if j % 2 == 0: mus[i:i+L] += .22 * np.sin(2 * np.pi * (50 + 70 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 12)
    else: mus[i:i+L] += .05 * rng.standard_normal(L) * np.exp(-tt * 40)
    if j % 4 == 2:
        f = [523.25, 659.25, 587.33, 783.99][(j // 4) % 4]
        mus[i:i+L] += .05 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 9)
sfx = np.zeros(n)
def hiss(a, dur, amp=.35):
    i = int(a * SR); L = min(int(dur * SR), n - i)
    no = rng.standard_normal(L); no = no - np.convolve(no, np.ones(8) / 8, 'same')
    tt = np.arange(L) / SR; e = np.minimum(1, tt / .05) * np.minimum(1, (dur - tt) / .3)
    wob = .7 + .3 * np.abs(np.sin(tt * 9 * np.pi))
    sfx[i:i+L] += amp * no * e * wob
def whistle(a, dur, amp=.25):
    i = int(a * SR); L = min(int(dur * SR), n - i); tt = np.arange(L) / SR
    e = np.minimum(1, tt / .15) * np.minimum(1, (dur - tt) / .3)
    f = 1900 + 120 * np.sin(tt * 8)
    sfx[i:i+L] += amp * e * (np.sin(2 * np.pi * np.cumsum(f) / SR) + .3 * rng.standard_normal(L) * .3)
whistle(0.15, 1.6, .2); hiss(0.15, 1.6, .25)
whistle(S['whistle'] + 3.0, 3.3, .22); hiss(S['whistle'] + 3.0, 3.4, .3)
hiss(S['loop'] + .3, END - S['loop'] - .3, .18)
def clank(a, amp=.25):
    i = int(a * SR); L = int(.5 * SR); tt = np.arange(L) / SR
    sfx[i:i+L] += amp * sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * d) for f, d in ((1250, 9), (2730, 14), (4100, 20)))
for a in (S['parts'] + 0.3, S['parts'] + 0.7, S['parts'] + 1.1, S['pressure'] - .1, S['pressure'] + .3): clank(a, .15)
def ticks(a, b, every=.07, amp=.1, f=2400):
    for k in np.arange(a, b, every):
        i = int(k * SR); L = int(.02 * SR); tt = np.arange(L) / SR
        sfx[i:i+L] += amp * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 300)
ticks(S['pressure'] + 2.5, S['pressure'] + 6.0, .1)
ticks(S['boil'] + .3, S['boil'] + 2.5, .08)
# bubbling during cutaway
for k in np.arange(S['pressure'] + 1.5, S['whistle'], .045):
    i = int((k + rng.random() * .03) * SR); L = int(.03 * SR); tt = np.arange(L) / SR
    sfx[i:i+L] += .05 * np.sin(2 * np.pi * (300 + 500 * rng.random()) * tt * (1 + tt * 20)) * np.exp(-tt * 120)
# voice
vo = np.zeros(n)
import scipy.signal as ss
for l in TL['lines']:
    a, sr = sf.read(f"vo/cooker/{l['id']}.wav")
    a = ss.resample_poly(a, 2, 1)  # 24k -> 48k
    i = int(l['start'] * SR); vo[i:i+len(a)] += a[:n-i]
# duck music under voice
act = np.convolve((np.abs(vo) > .01).astype(float), np.ones(int(.25 * SR)) / int(.25 * SR), 'same')
duck = 1 - .45 * np.clip(act * 3, 0, 1)
mix = vo * 1.0 + mus * duck * .9 + sfx * .8
# fade loop seam: tiny fades
mix[:int(.02*SR)] *= np.linspace(0, 1, int(.02*SR)); mix[-int(.05*SR):] *= np.linspace(1, 0, int(.05*SR))
mix /= max(1e-9, np.abs(mix).max()) / .9
sf.write('mix_cooker.wav', np.stack([mix, mix], 1), SR)
print('ok', END)
