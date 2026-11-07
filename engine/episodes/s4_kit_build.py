"""S4 Hook Shots shared build + helpers (Swiss Kinetic Type)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from PIL import ImageDraw
from reel import Reel, Line, F, ease, eout, W, H
from s4_199 import BASE, INK, RED, CREAM, GREY, slide
V = "af_heart"
def fish(d, x, y, s, col):
    d.ellipse((x - 70 * s, y - 40 * s, x + 70 * s, y + 40 * s), fill=col)
    d.polygon([(x + 60 * s, y), (x + 120 * s, y - 45 * s), (x + 120 * s, y + 45 * s)], fill=col)
    d.ellipse((x - 45 * s, y - 14 * s, x - 25 * s, y + 6 * s), fill=CREAM)
def frame_start(fr, t, R, label):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    ph = (t - t0) / max(.01, L.t1 - L.t0) if L else 0
    d.rectangle((65, 288, 470, 334), fill=RED); fr.text((80, 292), label, F("xb", 32), (255, 255, 255))
    return d, L, tag, t0, ph
def build(name, n, lines, scene, out, nudge, cta_body):
    for L in lines: L.speed = round(L.speed * 1.08, 3)
    R = Reel(name, "swiss", lines, tone="warm", seed=40 + n)
    R.cap_style.update(fg=(255, 255, 255), hi=(255, 90, 90), bg=(15, 15, 15, 235))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text=nudge, icon="send", at=round(dur * .38, 2), bg=RED, fg=(255, 255, 255))
    R.cta = dict(at=R.T("cta"), until=R.T("loop") - .05, icon="send", head="Send this", body=cta_body, bg=INK, acc=RED, fg=(255, 255, 255))
    stills = sorted([.5, 1.0] + [L.t0 + .6 for L in lines] + [L.t1 - .2 for L in lines] + [R.nudge["at"] + 1, dur - .2])
    return R, R.render(scene, out, stills=stills)
