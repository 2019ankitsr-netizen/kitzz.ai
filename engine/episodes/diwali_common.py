"""Shared bits for the Diwali 2026 reels: Devanagari fonts, bokeh night, diyas, sparks, build helper."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reel import Reel, Line, F, FM, ease, eout, eback, W, H

FONTS = os.environ.get("DEVANAGARI_FONTS", "/home/claude/fonts")
def HF(s, w="Bold"): return ImageFont.truetype(f"{FONTS}/Hind-{w}.ttf", s)
def YF(s): return ImageFont.truetype(f"{FONTS}/YatraOne-Regular.ttf", s)
def HL(spk, say, cap=None, **k): return Line(spk, say, cap, lang="hi", **k)

def night_bg(top=(18, 10, 40), bottom=(60, 18, 40), seed=1, n=26):
    yy = np.linspace(0, 1, H)[:, None, None]
    g = np.array(top) + (np.array(bottom) - np.array(top)) * yy
    im = Image.fromarray(np.repeat(g, W, axis=1).astype(np.uint8)).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); r = random.Random(seed)
    for _ in range(n):
        x, y, rad = r.randint(0, W), r.randint(200, 1500), r.randint(30, 110)
        c = r.choice([(255, 170, 60), (255, 120, 60), (255, 210, 120), (255, 90, 120)])
        d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=c + (r.randint(25, 60),))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18)))
    return im

def diya(d, x, y, s, t, phase=0.0):
    d.chord((x - 60 * s, y - 30 * s, x + 60 * s, y + 40 * s), 0, 180, fill=(170, 80, 40))
    d.ellipse((x - 60 * s, y - 12 * s, x + 60 * s, y + 12 * s), fill=(210, 110, 50))
    fl = 1 + .12 * math.sin(t * 13 + phase) + .06 * math.sin(t * 29 + phase * 2)
    d.ellipse((x - 26 * s, y - 70 * s * fl, x + 26 * s, y - 2 * s), fill=(255, 200, 80))
    d.ellipse((x - 13 * s, y - 50 * s * fl, x + 13 * s, y - 6 * s), fill=(255, 250, 210))

def glow_layer(size, xy, rad, col):
    g = Image.new("RGBA", size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((xy[0] - rad, xy[1] - rad, xy[0] + rad, xy[1] + rad), fill=col)
    return g.filter(ImageFilter.GaussianBlur(rad / 2))

_GP = {}
def paste_glow(img, x, y, rad, col):
    """Fast glow: cached blurred patch pasted at (x, y)."""
    key = (int(rad), col)
    if key not in _GP:
        n = int(rad * 4); g = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse((n / 2 - rad, n / 2 - rad, n / 2 + rad, n / 2 + rad), fill=col); _GP[key] = g.filter(ImageFilter.GaussianBlur(rad / 2))
    g = _GP[key]; n = g.width; x0, y0 = int(x - n / 2), int(y - n / 2)
    cx0, cy0 = max(0, -x0), max(0, -y0); cx1, cy1 = min(n, img.width - x0), min(n, img.height - y0)
    if cx1 > cx0 and cy1 > cy0: img.alpha_composite(g.crop((cx0, cy0, cx1, cy1)), (x0 + cx0, y0 + cy0))

class Sparks:
    """Deterministic spark particles; call step(t, sources) once per frame in order."""
    def __init__(self, seed=7): self.p = []; self.r = random.Random(seed); self.last = 0.0
    def step(self, t, sources, rate=40):
        dt = max(0.0, t - self.last); self.last = t
        for (x, y, k) in sources:
            for _ in range(int(rate * k * dt * 30 / 30) + (1 if self.r.random() < (rate * k * dt) % 1 else 0)):
                a = self.r.uniform(0, 2 * math.pi); v = self.r.uniform(120, 520)
                self.p.append([x, y, v * math.cos(a), v * math.sin(a) - 80, self.r.uniform(.25, .7), 0.0])
        for q in self.p:
            q[0] += q[2] * dt; q[1] += q[3] * dt; q[3] += 500 * dt; q[5] += dt
        self.p = [q for q in self.p if q[5] < q[4]]
    def draw(self, d):
        for x, y, vx, vy, life, age in self.p:
            k = 1 - age / life; L = .03
            d.line((x, y, x - vx * L, y - vy * L), fill=(255, int(200 + 55 * k), int(140 * k)), width=max(2, int(6 * k)))

def build(name, lines, scene, out, music="festive", nudge=None, cta=None, cap_size=58, seed=80, extra_stills=(), cap_bg=(40, 10, 20, 215)):
    R = Reel(name, music, lines, tone="warm", seed=seed)
    R.cap_style.update(fontfile=f"{FONTS}/Hind-Bold.ttf", size=cap_size, lh=74, maxchars=34, fg=(255, 248, 235), hi=(255, 196, 70), bg=cap_bg)
    dur = R.build_audio(f"{out}/cache")
    if nudge: R.nudge = dict(at=round(dur * .38, 2), **nudge)
    if cta: R.cta = dict(at=R.T("cta"), **cta)
    stills = sorted([.5, 1.2] + [L.t0 + .7 for L in lines] + [L.t1 - .2 for L in lines] + ([R.nudge["at"] + 1] if nudge else []) + [dur - .2] + list(extra_stills))
    return R, R.render(scene, out, stills=stills)
