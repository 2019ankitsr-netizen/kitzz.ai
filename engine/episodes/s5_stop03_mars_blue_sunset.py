"""S5 Space Transit · Stop 03 · A blue sunset on Mars."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from s5_kit import M, E, Line, hud, label, build, F, ease, eout, W, H
LINES = [
    Line(E, "Next stop! | A blue sunset on Mars.", "Next stop: a blue sunset on Mars.", tag="hook", sfx="dingdong", gap=.3),
    Line(M, "The red planet. | The Sun going down. | And the sky around it turns blue.", tag="intro"),
    Line(M, "Fact. | NASA's Curiosity rover photographed it in 2015.", "FACT: NASA's Curiosity rover photographed it in 2015.", tag="photo", sfx="tick"),
    Line(M, "Mars dust is so fine, | that blue light gets through it a little more easily, | and stays close to the Sun.",
         "Mars dust is so fine that blue light gets through a little more easily, and stays close to the Sun.", speed=.94, pitch=-1, tag="why", drop=True),
    Line(M, "Fact. | From Mars, the Sun looks only about two thirds as big as it does from Earth.",
         "FACT: from Mars, the Sun looks only about ⅔ as big as from Earth.", pre=.35, pitch=.5, tag="size", sfx="tick"),
    Line(M, "Fact. | Dust high in the sky can keep twilight glowing for two hours or more after sunset.",
         "FACT: high dust can keep twilight glowing for 2 hours or more after sunset.", tag="twilight", sfx="tick"),
    Line(M, "Imagine. | Your evening chai on Mars, | under a blue sun.", "IMAGINE: your evening chai on Mars, under a blue sun.", tag="imagine", sfx="tick"),
    Line(E, "Next stop! | Venus.", "Next stop: Venus.", tag="next", sfx="dingdong", gap=.3),
    Line(M, "Save this ride. | Tag who you'd watch this sunset with.", tone="bright", tag="cta", sfx="pop", gap=.1),
]
yy = np.linspace(0, 1, H)[:, None]
def sky(dusk):
    top = np.array([60, 40, 34]) * (1 - dusk) + np.array([14, 12, 22]) * dusk
    bot = np.array([200, 150, 100]) * (1 - dusk) + np.array([120, 80, 70]) * dusk
    g = top + (bot - top) * np.clip(yy * 1.3, 0, 1)[..., None]
    return Image.fromarray(np.repeat(g, W, axis=1).astype(np.uint8)).convert("RGBA")
SKIES = [sky(i / 20) for i in range(21)]
GLOW = {}
def glow(r):
    r = int(r)
    if r not in GLOW:
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(im).ellipse((540 - r, 900 - r, 540 + r, 900 + r), fill=(110, 170, 255, 150))
        GLOW[r] = im.filter(ImageFilter.GaussianBlur(r / 2.5))
    return GLOW[r]
def scene(fr, t, R):
    T = R.T; dur = R.dur
    sunset = ease((t - 1) / (T("twilight") - 1))
    img = SKIES[int(min(1, sunset) * 20)].copy(); fr.img = img
    sy = 640 + 360 * sunset
    blue = ease((t - R.T("intro")) / 3)
    if sy < 1000: img.alpha_composite(glow(60 + 220 * blue), (0, int(sy - 900)))
    d = ImageDraw.Draw(img); fr.d = d
    sz = R.line("size")
    rs = 34
    if sy < 1010: d.ellipse((540 - rs, sy - rs, 540 + rs, sy + rs), fill=(235, 245, 255))
    d.polygon([(60, 1250), (60, 990), (160, 960), (260, 985), (380, 940), (520, 975), (640, 950), (760, 990), (880, 955), (1020, 980), (1020, 1250)], fill=(70, 34, 24))
    if sz.t0 + .8 <= t < T("twilight"):
        d.ellipse((230 - 51, 640 - 51, 230 + 51, 640 + 51), fill=(255, 220, 120)); d.ellipse((780 - 34, 640 - 34, 780 + 34, 640 + 34), fill=(235, 245, 255))
        label(fr, (230, 740), "from Earth", 44, (255, 255, 255)); label(fr, (780, 740), "from Mars (~⅔)", 44, (255, 255, 255))
    ph = R.line("photo")
    if ph.t0 + .8 <= t < T("why"): label(fr, (540, 620), "Curiosity · 2015", 64, (90, 220, 255))
    wy = R.line("why")
    if wy.t0 + .8 <= t < sz.t0: label(fr, (540, 620), "fine dust → blue near the Sun", 48, (150, 200, 255))
    tw = R.line("twilight")
    if tw.t0 + .8 <= t < T("imagine"): label(fr, (540, 620), "2+ hours of twilight", 60, (255, 190, 60))
    im = R.line("imagine")
    if im.t0 + .8 <= t < T("next"):
        x, y = 760, 940                                                                                   # a chai glass on the window ledge
        d.polygon([(x - 50, y - 120), (x + 50, y - 120), (x + 38, y), (x - 38, y)], fill=(230, 230, 235, 200))
        d.polygon([(x - 46, y - 80), (x + 46, y - 80), (x + 38, y), (x - 38, y)], fill=(190, 120, 60))
        label(fr, (420, 700), "Chai, under a blue sun", 54, (255, 120, 200))
    hud(fr, t, R, 3, "MARS · BLUE SUNSET", "VENUS", "~225 M km from Earth (avg)",
        [("photo", "FACT"), ("size", "FACT"), ("imagine", "IMAGINE"), ("next", None)])
if __name__ == "__main__":
    R, p = build("S5_SpaceTransit_stop03_MarsBlueSunset", 3, LINES, scene, sys.argv[1], "Tag who you'd watch\nthis sunset with.")
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
