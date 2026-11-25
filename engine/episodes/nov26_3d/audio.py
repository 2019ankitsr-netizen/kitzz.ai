import json, numpy as np, soundfile as sf
SR = 48000
TL = json.load(open('web/timeline.json')); S = TL['S']; END = TL['end']
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
pad([55, 110, 164.8], .05, 0, S['star'] + .2)
pad([43.65, 87.3, 130.8, 196], .05, S['star'] - .3, S['dark'] + .3)   # lift (F) on star reveal
pad([55, 82.4], .035, S['cta'] - .5, END)
# pulse: soft kick 100 bpm from sun to dark
bpm = 100; beat = 60 / bpm
for k in np.arange(S['sun'], S['dark'], beat):
    i = int(k * SR); L = int(.35 * SR)
    if i + L > n: break
    tt = np.arange(L) / SR
    mus[i:i+L] += .28 * np.sin(2 * np.pi * (48 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
# plucks (sparkle) on 8ths during scale-up
notes = [440, 523.25, 659.25, 783.99, 659.25, 523.25]
for j, k in enumerate(np.arange(S['jup'], S['star'] + 3, beat / 2)):
    i = int(k * SR); L = int(.5 * SR)
    if i + L > n: break
    tt = np.arange(L) / SR
    mus[i:i+L] += .045 * np.sin(2 * np.pi * notes[j % 6] * tt) * np.exp(-tt * 7)
# sub boom at star reveal and dark
for k, a in ((S['star'] + 2.3, .5), (S['dark'], .35)):
    i = int(k * SR); L = int(2.5 * SR); tt = np.arange(L) / SR
    mus[i:i+L] += a * np.sin(2 * np.pi * (38 + 30 * np.exp(-tt * 4)) * tt) * np.exp(-tt * 1.6)

sfx = np.zeros(n)
def whoosh(a, dur, amp=.25, up=True):
    i = int(a * SR); L = int(dur * SR); tt = np.arange(L) / dur / SR
    no = rng.standard_normal(L)
    # crude bandpass sweep via moving average differences
    out = np.zeros(L); w0 = 40 if up else 6
    for seg in range(20):
        s0, s1 = seg * L // 20, (seg + 1) * L // 20
        w = int(w0 + (6 - w0) * seg / 19) if up else int(6 + (40 - 6) * seg / 19)
        k = np.ones(max(w, 1)) / max(w, 1)
        out[s0:s1] = np.convolve(no, k, 'same')[s0:s1]
    e = np.sin(np.pi * tt) ** 2
    seg = amp * out * e
    sfx[i:i+L] += seg[:max(0, min(L, n - i))]
whoosh(S['sun'] + .1, 1.4, .35)
whoosh(S['earth'], 1.4, .4, False)
whoosh(S['dist'] + .1, 1.4, .35)
whoosh(S['moon'] - .1, 1.2, .35, False)
whoosh(S['jup'], 1.7, .4)
whoosh(S['nep'], 1.4, .4)
whoosh(S['star'] - .2, 2.0, .45)
whoosh(S['loop'], 1.0, .3, False)
# counter ticks
def ticks(a, b, every=.07, amp=.12, f=2400):
    for k in np.arange(a, b, every):
        i = int(k * SR); L = int(.02 * SR); tt = np.arange(L) / SR
        sfx[i:i+L] += amp * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 300)
ticks(S['dist'] + .2, S['dist'] + 3.2)
ticks(S['star'] + 2.4, S['star'] + 4.6, .06, .1, 2000)
# HUD lock chimes
def chime(a, amp=.12):
    i = int(a * SR); L = int(.8 * SR); tt = np.arange(L) / SR
    sfx[i:i+L] += amp * (np.sin(2*np.pi*1318.5*tt) + .5*np.sin(2*np.pi*1975.5*tt)) * np.exp(-tt * 6)
for a in (S['sun'] + 1.2, S['earth'] + 1.1, S['moon'] + 1.0, S['jup'] + 1.6, S['nep'] + 1.0, S['star'] + 4.5, S['moon'] + .15, S['cta'] - .1):
    chime(a)

# voice
vo = np.zeros(n)
import scipy.signal as ss
for l in TL['lines']:
    a, sr = sf.read(f"vo/{l['id']}.wav")
    a = ss.resample_poly(a, 2, 1)  # 24k -> 48k
    i = int(l['start'] * SR); vo[i:i+len(a)] += a[:n-i]
# duck music under voice
act = np.convolve((np.abs(vo) > .01).astype(float), np.ones(int(.25 * SR)) / int(.25 * SR), 'same')
duck = 1 - .45 * np.clip(act * 3, 0, 1)
mix = vo * 1.0 + mus * duck * .9 + sfx * .8
# fade loop seam: tiny fades
mix[:int(.02*SR)] *= np.linspace(0, 1, int(.02*SR)); mix[-int(.05*SR):] *= np.linspace(1, 0, int(.05*SR))
mix /= max(1e-9, np.abs(mix).max()) / .9
sf.write('mix.wav', np.stack([mix, mix], 1), SR)
print('ok', END)
