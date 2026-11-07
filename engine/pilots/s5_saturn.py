"""S5 Space Transit · Stop 01 · Saturn's rings — Cosmic Metro HUD."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from reel import Reel, Line, F, FM, ease, eout, eback, W, H

M, E = "am_michael", "bf_emma"
LINES = [
    Line(E, "Next stop! | Saturn's rings.", "Next stop: Saturn's rings.", tag="hook", sfx="dingdong", gap=.3),
    Line(M, "You're about one point four billion kilometres from the Sun. | Look out the window.",
         "You're about 1.4 billion km from the Sun. Look out the window.", tag="window"),
    Line(M, "Fact. | These rings are about 270,000 km across. | That's about twenty-one Earths, side by side.",
         "FACT: these rings are about 270,000 km across. That's about 21 Earths side by side.", tag="fact1", sfx="tick"),
    Line(M, "But their thickness? | In most places, | less than a hundred metres.", "But their thickness? In most places, less than 100 metres.",
         speed=.94, pitch=-1, tag="thin", drop=True),
    Line(M, "Fact. | They're made mostly of ice. | Bits as small as dust, | and chunks as big as a house.",
         "FACT: they're mostly ice. Bits as small as dust, chunks as big as a house.", pre=.35, pitch=.5, tag="ice", sfx="tick"),
    Line(M, "Theory. | Data from the Cassini probe hints the rings could be much younger than Saturn itself.",
         "THEORY: Cassini's data hints the rings could be much younger than Saturn itself.", tag="theory", sfx="tick"),
    Line(M, "Imagine. | If Earth had rings like these, | you'd see a bright arch across India's night sky.",
         "IMAGINE: if Earth had rings like these, you'd see a bright arch across India's night sky.", tag="imagine", sfx="tick"),
    Line(E, "Next stop! | The Moon's far side.", "Next stop: the Moon's far side.", tag="next", sfx="dingdong", gap=.3),
    Line(M, "Save this ride. | Tag who you'd take to Saturn.", tone="bright", tag="cta", sfx="pop", gap=.1),
]

rng = np.random.default_rng(11)
STARS = np.c_[rng.uniform(-1, 1, 420), rng.uniform(-1.6, 1.6, 420), rng.uniform(.05, 1, 420)]
SKY = Image.new("RGB", (W, H), (4, 6, 14))
_d = ImageDraw.Draw(SKY); _r = random.Random(5)
for _ in range(700):
    x, y = _r.randint(0, W), _r.randint(0, H); c = _r.randint(60, 150); _d.point((x, y), fill=(c, c, c + 20))

def frame_overlay():
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rectangle((0, 0, W, H), fill=(28, 32, 42, 255)); d.rounded_rectangle((60, 270, 1020, 1250), 90, fill=(0, 0, 0, 0))
    d.rounded_rectangle((60, 270, 1020, 1250), 90, outline=(80, 88, 104, 255), width=18)
    d.rounded_rectangle((40, 250, 1040, 1270), 100, outline=(50, 56, 68, 255), width=10)
    for x in range(0, W, 120): d.rectangle((x, 1300, x + 80, 1320), fill=(45, 50, 62, 255))      # seat rail
    return ov
FRAME = frame_overlay()

_SC = {}
def saturn(img, cx, cy, s, tilt, t):
    key = (round(s, 3), round(tilt, 3))
    if key in _SC: img.alpha_composite(_SC[key]); return
    if len(_SC) > 400: _SC.clear()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    R = 170 * s; rx, ry = 400 * s, 400 * s * tilt
    def rings(part):
        for i, (rr, col, wd) in enumerate(((1.0, (230, 210, 170, 235), 22), (.9, (200, 175, 130, 220), 26), (.78, (170, 150, 115, 200), 14))):
            box = (cx - rx * rr, cy - ry * rr, cx + rx * rr, cy + ry * rr)
            d.arc(box, 180 if part == "back" else 0, 360 if part == "back" else 180, fill=col, width=max(2, int(wd * s * (.4 + tilt * 2.5))))
    rings("back")
    d.ellipse((cx - R, cy - R * .92, cx + R, cy + R * .92), fill=(222, 190, 130, 255))
    for i in range(7):
        y = cy - R * .8 + i * R * .26
        half = math.sqrt(max(0, (R * .92) ** 2 - (y - cy) ** 2)) / .92
        d.line((cx - half, y, cx + half, y), fill=(205, 168, 110, 255), width=max(2, int(10 * s)))
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).ellipse((cx - R * .2, cy - R, cx + R * 1.6, cy + R), fill=110)
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).ellipse((cx - R, cy - R * .92, cx + R, cy + R * .92), fill=255)
    from PIL import ImageChops
    shade = ImageChops.multiply(sh, mask).filter(ImageFilter.GaussianBlur(20))
    lay.paste((20, 15, 30, 255), (0, 0), shade.point(lambda v: int(v * .8)))
    d = ImageDraw.Draw(lay); rings("front")
    _SC[key] = lay; img.alpha_composite(lay)

def scene(fr, t, R):
    T = R.T
    img = SKY.copy().convert("RGBA"); d = ImageDraw.Draw(img)
    # stars rushing past (first-person ride); slow down as we arrive
    spd = .5 if t < T("window") else .12
    z = (STARS[:, 2] - t * spd) % 1 + .02
    sx, sy = 540 + STARS[:, 0] / z * 260, 760 + STARS[:, 1] / z * 260
    for x, y, zz in zip(sx, sy, z):
        if 0 < x < W and 0 < y < H:
            r = max(1, 3 * (1 - zz)); c = int(150 + 105 * (1 - zz)); d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c, 255))
    # Saturn grows as we pull in; tilts edge-on for the thickness line
    s = .35 + .65 * eout((t - .2) / 7)
    th = R.line("thin")
    tilt = .24 - .225 * ease((t - th.t0) / 1.2) + .225 * ease((t - th.t1 - .2) / 1.2)
    cy = 790
    imag = R.line("imagine")
    in_imag = imag.t0 <= t < T("next")
    if not in_imag: saturn(img, 540, cy, s, tilt, t)
    d = ImageDraw.Draw(img); fr.img = img; fr.d = d
    # 21 Earths along the ring
    f1 = R.line("fact1")
    if f1.t0 + 2.5 <= t < th.t0:
        n = int(21 * ease((t - f1.t0 - 2.5) / 1.5)); w = 2 * 400 * s / 21
        for i in range(n):
            x = 540 - 400 * s + w * (i + .5); d.ellipse((x - w * .42, 975 - w * .42, x + w * .42, 975 + w * .42), fill=(70, 140, 230), outline=(160, 220, 255))
        fr.text((540, 1028), "21 Earths", F("xb", 48), (160, 220, 255), anchor="mm")
    if f1.t0 + .6 <= t < th.t0:
        y = 600; x0, x1 = 540 - 400 * s, 540 + 400 * s
        d.line((x0, y, x1, y), fill=(120, 220, 255), width=4); d.line((x0, y - 16, x0, y + 16), fill=(120, 220, 255), width=4); d.line((x1, y - 16, x1, y + 16), fill=(120, 220, 255), width=4)
        fr.text((540, 560), "~270,000 km", F("xb", 52), (120, 220, 255), anchor="mm")
    if th.t0 + 1 <= t < th.t1 + .8:
        fr.text((540, 592), "< 100 m thick", F("black", 72), (255, 190, 60), anchor="mm")
    # ice chunks drifting past
    ic = R.line("ice")
    if ic.t0 <= t < T("theory"):
        rr = random.Random(9)
        for i in range(14):
            x = (rr.uniform(80, 1000) + (t - ic.t0) * rr.uniform(-40, 40)); y = rr.uniform(560, 1000); r = rr.choice([4, 6, 10, 18, 30])
            d.ellipse((x - r, y - r, x + r, y + r), fill=(220, 235, 250), outline=(150, 180, 210))
    # imagine: a ringed night sky over India
    if in_imag:
        k = ease((t - imag.t0) / 1.2)
        d.ellipse((-700, 650, 1780, 1650), outline=(235, 225, 200), width=int(1 + 26 * k))
        d.ellipse((-640, 690, 1720, 1610), outline=(200, 185, 150), width=int(1 + 12 * k))
        d.polygon([(60, 1250), (60, 980), (140, 960), (180, 990), (260, 930), (300, 960), (340, 900), (370, 960), (430, 950), (470, 990),
                   (560, 940), (620, 980), (700, 920), (760, 970), (860, 950), (940, 990), (1020, 960), (1020, 1250)], fill=(10, 12, 20))
    img.alpha_composite(FRAME); fr.img = img; d = ImageDraw.Draw(img); fr.d = d
    # LED next-stop board
    d.rounded_rectangle((90, 300, 990, 460), 20, fill=(20, 12, 4), outline=(90, 60, 20), width=4)
    for x in range(100, 980, 12):
        for y in range(310, 452, 12): d.point((x, y), fill=(45, 28, 8))
    nxt = t >= T("next") - .1
    fr.text((540, 338), "NEXT STOP", FM(36), (255, 170, 40), anchor="mm")
    fr.text((540, 405), "THE MOON'S FAR SIDE" if nxt else "SATURN'S RINGS", FM(58 if nxt else 62), (255, 190, 60), anchor="mm")
    # stop type chip + telemetry
    kind = None
    for tag, kd in (("fact1", "FACT"), ("ice", "FACT"), ("theory", "THEORY"), ("imagine", "IMAGINE"), ("next", None)):
        if t >= T(tag) - .05: kind = kd
    fr.text((100, 488), "STOP 01 / 13", FM(32), (120, 220, 255))
    if kind:
        col = {"FACT": (90, 220, 255), "THEORY": (255, 180, 60), "IMAGINE": (255, 120, 200)}[kind]
        tw = d.textlength(kind, font=F("black", 40)); d.rounded_rectangle((350, 482, 350 + tw + 40, 534), 26, fill=col)
        fr.text((370, 508), kind, F("black", 40), (10, 10, 20), anchor="lm")
    fr.text((980, 488), "1.4 B km from Sun", FM(32), (120, 220, 255), anchor="ra")

def build(out):
    R = Reel("S5_SpaceTransit_stop01_SaturnsRings", "space", LINES, tone="bright", seed=5)
    R.cap_style.update(fg=(255, 255, 255), hi=(255, 190, 60), bg=(8, 10, 20, 210))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Save this ride", icon="save", at=round(dur * .38, 2), bg=(255, 190, 60), fg=(15, 15, 25))
    R.cta = dict(at=R.T("cta"), icon="save", head="Save this ride", body="Tag who you'd\ntake to Saturn.", bg=(16, 20, 36), acc=(255, 190, 60), fg=(255, 255, 255))
    stills = sorted([.6, 2.5] + [R.T(x) + 1.3 for x in ["window", "fact1", "thin", "ice", "theory", "imagine", "next", "cta"]]
                    + [R.line("fact1").t1 - .3, R.line("thin").t1 - .2, R.nudge["at"] + 1.0, R.line("imagine").t1 - .2, dur - .2])
    return R, R.render(scene, out, stills=stills)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", R.violations[:20], len(R.violations))
