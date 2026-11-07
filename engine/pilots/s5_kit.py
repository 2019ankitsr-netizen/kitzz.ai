"""S5 Space Transit kit — metro window, star rush, LED next-stop board, FACT/THEORY/IMAGINE chip, telemetry."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from PIL import Image, ImageDraw
from reel import Reel, Line, F, FM, ease, eout, eback, W, H
from s5_saturn import SKY, FRAME, STARS

M, E = "am_michael", "bf_emma"

def stars(img, t, spd):
    d = ImageDraw.Draw(img)
    z = (STARS[:, 2] - t * spd) % 1 + .02
    sx, sy = 540 + STARS[:, 0] / z * 260, 760 + STARS[:, 1] / z * 260
    for x, y, zz in zip(sx, sy, z):
        if 0 < x < W and 0 < y < H:
            r = max(1, 3 * (1 - zz)); c = int(150 + 105 * (1 - zz)); d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c, 255))

def hud(fr, t, R, stop_no, board_now, board_next, telemetry, kinds):
    img = fr.img; img.alpha_composite(FRAME); d = ImageDraw.Draw(img); fr.d = d
    d.rounded_rectangle((90, 300, 990, 460), 20, fill=(20, 12, 4), outline=(90, 60, 20), width=4)
    for x in range(100, 980, 12):
        for y in range(310, 452, 12): d.point((x, y), fill=(45, 28, 8))
    nxt = t >= R.T("next") - .1
    lab = board_next if nxt else board_now
    size = 62
    while size > 40 and d.textlength(lab, font=FM(size)) > 860: size -= 2
    fr.text((540, 338), "NEXT STOP", FM(36), (255, 170, 40), anchor="mm")
    fr.text((540, 405), lab, FM(size), (255, 190, 60), anchor="mm")
    kind = None
    for tag, kd in kinds:
        if t >= R.T(tag) - .05: kind = kd
    fr.text((100, 488), f"STOP {stop_no:02d} / 13", FM(32), (120, 220, 255))
    if kind:
        col = {"FACT": (90, 220, 255), "THEORY": (255, 180, 60), "IMAGINE": (255, 120, 200)}[kind]
        tw = d.textlength(kind, font=F("black", 40)); d.rounded_rectangle((350, 482, 350 + tw + 40, 534), 26, fill=col)
        fr.text((370, 508), kind, F("black", 40), (10, 10, 20), anchor="lm")
    fr.text((980, 488), telemetry, FM(32), (120, 220, 255), anchor="ra")

def label(fr, xy, txt, size=56, col=(255, 190, 60)):
    fr.text(xy, txt, F("black", size), col, anchor="mm", stroke=5, stroke_fill=(5, 8, 16))

def build(name, n, lines, scene, out, cta_body):
    R = Reel(name, "space", lines, tone="bright", seed=50 + n)
    R.cap_style.update(fg=(255, 255, 255), hi=(255, 190, 60), bg=(8, 10, 20, 210))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Save this ride", icon="save", at=round(dur * .38, 2), bg=(255, 190, 60), fg=(15, 15, 25))
    R.cta = dict(at=R.T("cta"), icon="save", head="Save this ride", body=cta_body, bg=(16, 20, 36), acc=(255, 190, 60), fg=(255, 255, 255))
    stills = sorted([.6, 2.5] + [L.t0 + 1.3 for L in lines] + [L.t1 - .3 for L in lines] + [R.nudge["at"] + 1, dur - .2])
    return R, R.render(scene, out, stills=stills)
