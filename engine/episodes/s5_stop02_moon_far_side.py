"""S5 Space Transit · Stop 02 · The Moon's far side."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from s5_kit import M, E, Line, stars, hud, label, build, F, ease, eout, W, H
from s5_saturn import SKY
LINES = [
    Line(E, "Next stop! | The Moon's far side.", "Next stop: the Moon's far side.", tag="hook", sfx="dingdong", gap=.3),
    Line(M, "Everyone calls it the dark side. | It isn't.", tag="dark"),
    Line(M, "Fact. | The Moon turns exactly once per orbit, | so the same face always points at Earth.",
         "FACT: the Moon turns once per orbit, so the same face always points at Earth.", tag="lock", sfx="tick"),
    Line(M, "The far side gets just as much sunlight. | About two weeks of day, | and two weeks of night.",
         "The far side gets just as much sunlight: about 2 weeks of day, 2 weeks of night.", speed=.94, pitch=-1, tag="sun", drop=True),
    Line(M, "Fact. | In 2019, China's Chang'e 4 made the first soft landing there. | In 2024, Chang'e 6 brought back the first far side samples.",
         "FACT: Chang'e 4 made the first far-side landing in 2019. Chang'e 6 brought back the first samples in 2024.", pre=.35, pitch=.5, tag="land", sfx="tick"),
    Line(M, "Theory. | Its crust is thicker, | which may be why it has so few dark lava plains.",
         "THEORY: its crust is thicker, which may be why it has so few dark lava plains.", tag="theory", sfx="tick"),
    Line(M, "Imagine. | Standing there, | Earth would never rise in your sky. | Not once.",
         "IMAGINE: standing there, Earth would never rise in your sky. Not once.", tag="imagine", sfx="tick"),
    Line(E, "Next stop! | A blue sunset on Mars.", "Next stop: a blue sunset on Mars.", tag="next", sfx="dingdong", gap=.3),
    Line(M, "Save this ride. | Tag who you'd take to the Moon.", tone="bright", tag="cta", sfx="pop", gap=.1),
]
_r = random.Random(4); CRATERS = [(_r.uniform(-.8, .8), _r.uniform(-.8, .8), _r.uniform(.04, .14)) for _ in range(26)]
_MC = {}
def moon(img, cx, cy, R, light):
    """light: angle (rad) of the sunlit side; 0 = lit from the right."""
    key = (int(R), round(light, 2))
    if key not in _MC:
        if len(_MC) > 300: _MC.clear()
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(196, 196, 190, 255))
        for x, y, r in CRATERS:
            if x * x + y * y < .75: d.ellipse((cx + x * R - r * R, cy + y * R - r * R, cx + x * R + r * R, cy + y * R + r * R), fill=(165, 165, 160, 255))
        sh = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sh)
        ox, oy = -math.cos(light) * R * 1.1, -math.sin(light) * R * 1.1
        sd.ellipse((cx + ox - R * 1.05, cy + oy - R * 1.05, cx + ox + R * 1.05, cy + oy + R * 1.05), fill=200)
        mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
        lay.paste((10, 10, 18, 255), (0, 0), ImageChops.multiply(sh, mask).filter(ImageFilter.GaussianBlur(10)))
        _MC[key] = lay
    img.alpha_composite(_MC[key])
def scene(fr, t, R):
    T = R.T
    img = SKY.copy().convert("RGBA"); fr.img = img
    stars(img, t, .5 if t < T("dark") else .1)
    s = .45 + .55 * eout((t - .2) / 6); Rm = 200 * s
    sun = R.line("sun"); imag = R.line("imagine")
    light = 0.0
    if sun.t0 <= t < T("land"): light = (t - sun.t0) / (T("land") - sun.t0) * math.pi * 2       # sunlight sweeps right round
    lk_ = R.line("lock")
    if not (imag.t0 <= t < T("next")) and not (lk_.t0 + .8 <= t < sun.t0): moon(img, 540, 800, Rm, light)
    d = ImageDraw.Draw(img); fr.d = d
    lk = R.line("lock")
    if lk.t0 + .8 <= t < sun.t0:                                                                    # tidal-lock diagram
        k = ease((t - lk.t0 - .8) / .6); ex, ey, orb = 540, 800, 300
        d.ellipse((ex - orb, ey - orb, ex + orb, ey + orb), outline=(90, 110, 160), width=3)
        a = (t - lk.t0) * 1.2; mx, my = ex + orb * math.cos(a), ey + orb * math.sin(a)
        d.ellipse((ex - 46, ey - 46, ex + 46, ey + 46), fill=(70, 140, 230), outline=(160, 220, 255), width=3)
        d.ellipse((mx - 34, my - 34, mx + 34, my + 34), fill=(196, 196, 190)); fx, fy = mx - 26 * math.cos(a), my - 26 * math.sin(a)
        d.ellipse((fx - 9, fy - 9, fx + 9, fy + 9), fill=(225, 60, 60))
        label(fr, (540, 1020), "Same face → Earth", 52)
    if sun.t0 + .5 <= t < sun.t1 + .5: label(fr, (540, 562), "14 days day · 14 days night", 50)
    ld = R.line("land")
    if ld.t0 + 1 <= t < T("theory"):
        label(fr, (200, 640), "2019", 72, (90, 220, 255)); label(fr, (200, 700), "first landing", 40, (255, 255, 255))
        if t >= ld.t0 + (ld.t1 - ld.t0) * .5: label(fr, (870, 640), "2024", 72, (90, 220, 255)); label(fr, (870, 700), "first samples", 40, (255, 255, 255))
    th = R.line("theory")
    if th.t0 + .8 <= t < imag.t0: label(fr, (540, 562), "Thicker crust?", 64, (255, 180, 60))
    if imag.t0 <= t < T("next"):
        k = ease((t - imag.t0) / 1.0)
        d.polygon([(60, 1250), (60, 1000), (200, 980), (330, 1010), (480, 970), (620, 1000), (780, 975), (900, 1005), (1020, 985), (1020, 1250)], fill=(110, 110, 108))
        for x, y, r in ((200, 1080, 40), (600, 1120, 60), (880, 1060, 30)): d.ellipse((x - r, y - r * .4, x + r, y + r * .4), fill=(90, 90, 88))
        if t > imag.t0 + 1.5: label(fr, (540, 700), "No Earthrise. Ever.", 64, (255, 120, 200))
    hud(fr, t, R, 2, "THE MOON'S FAR SIDE", "MARS · BLUE SUNSET", "384,400 km from Earth",
        [("lock", "FACT"), ("land", "FACT"), ("theory", "THEORY"), ("imagine", "IMAGINE"), ("next", None)])
if __name__ == "__main__":
    R, p = build("S5_SpaceTransit_stop02_MoonFarSide", 2, LINES, scene, sys.argv[1], "Tag who you'd\ntake to the Moon.")
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
