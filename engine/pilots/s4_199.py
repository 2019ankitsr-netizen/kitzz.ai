"""S4 Hook Shots · 02 · ₹199, not ₹200 (left-digit effect) — Swiss Kinetic Type."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw
from reel import Reel, Line, F, FM, ease, eout, eback, W, H

V = "af_heart"
LINES = [
    Line(V, "₹199. | Not ₹200.", "₹199. Not ₹200.", speed=1.04, tag="hook", sfx="hit", gap=.2),
    Line(V, "Your brain fell for it.", tag="fell", gap=.25, sfx="whoosh"),
    Line(V, "You read left to right, | so the first digit lands first.", tag="left", sfx="tick"),
    Line(V, "One feels cheap. | Two feels expensive. | One rupee apart.", tag="onetwo", sfx="tick"),
    Line(V, "Researchers at N-Y-U tested this in 2005.", "NYU researchers tested this in 2005.", tag="nyu", sfx="whoosh"),
    Line(V, "It only works when the first digit changes.", pre=.25, pitch=1, tag="only", drop=True),
    Line(V, "₹201 to ₹200? | Nobody notices. | ₹200 to ₹199? | Feels like a deal.",
         "₹201 → ₹200? Nobody notices. ₹200 → ₹199? Feels like a deal.", tag="compare", sfx="tick"),
    Line(V, "Send this to someone. | They won't believe it.", tag="cta", sfx="pop", gap=.2),
    Line(V, "Now look at that price again.", tag="loop", gap=.05),
]
INK, RED, CREAM, GREY = (15, 15, 15), (225, 30, 30), (244, 242, 236), (160, 156, 150)

def base():
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    for x in range(65, 1016, 95): d.line((x, 0, x, H), fill=(228, 224, 216), width=2)
    return im
BASE = base()

def slide(t, t0, dx=60, dur=.22): k = eout((t - t0) / dur); return (1 - k) * dx, k

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    ph = (t - t0) / max(.01, L.t1 - L.t0) if L else 0
    d.rectangle((65, 288, 470, 334), fill=RED); fr.text((80, 292), "HOOK SHOT 02", F("xb", 32), (255, 255, 255))
    if tag in ("hook", "loop"):
        dx, k = slide(t, t0 - .05)
        fr.text((70 + dx, 380), "₹199", F("black", 300), INK)
        if tag == "hook" and ph > .35 or tag == "loop":
            dx2, _ = slide(t, t0 + (L.t1 - t0) * .35)
            fr.text((80 + dx2, 720), "not ₹200.", F("black", 140), RED)
    elif tag == "fell":
        dx, k = slide(t, t0)
        fr.text((80 - dx, 400), "Your brain\nfell for it.", F("black", 130), INK, spacing=0)
        d.rectangle((80, 720, 80 + 700 * ease((t - t0 - .3) / .5), 740), fill=RED)
    elif tag == "left":
        dx, k = slide(t, t0)
        fr.text((80, 360), "1", F("black", 330), RED); fr.text((300 - dx, 360), "99", F("black", 330), GREY)
        ax = 90 + 760 * ease((t - t0 - .2) / (L.t1 - t0 - .2))
        d.rectangle((90, 800, ax, 816), fill=INK); d.polygon([(ax + 40, 808), (ax, 780), (ax, 836)], fill=INK)
        fr.text((90, 860), "read first", F("xb", 64), RED)
    elif tag == "onetwo":
        k1 = eout((t - t0) / .2); k2 = eout((t - t0 - (L.t1 - t0) * .35) / .2)
        fr.text((90, 340 + (1 - k1) * 40), "1", F("black", 300), INK); fr.text((100, 700), "cheap", F("xb", 72), INK)
        if k2 > 0:
            fr.text((560, 340 + (1 - k2) * 40), "2", F("black", 300), RED); fr.text((560, 700), "expensive", F("xb", 72), RED)
        if ph > .7: d.rectangle((90, 820, 900, 830), fill=INK); fr.text((90, 860), "₹1 apart.", F("black", 90), INK)
    elif tag == "nyu":
        dx, k = slide(t, t0)
        fr.text((80 - dx, 380), "NYU", F("black", 220), INK); fr.text((80 + dx, 620), "2005", F("black", 150), RED)
        fr.text((84, 830), "Thomas & Morwitz,\nJournal of Consumer Research", F("b", 48), INK, spacing=8)
    elif tag == "only":
        dx, k = slide(t, t0)
        fr.text((80 - dx, 380), "Only when the", F("black", 96), INK)
        fr.text((80 - dx, 500), "first digit", F("black", 130), RED)
        fr.text((80 - dx, 660), "changes.", F("black", 96), INK)
    elif tag == "compare":
        k1 = eout((t - t0) / .2); k2 = eout((t - t0 - (L.t1 - t0) * .5) / .2)
        fr.text((80 - (1 - k1) * 60, 380), "₹201 → ₹200", F("black", 104), GREY); fr.text((84, 510), "nobody notices", F("xb", 60), GREY)
        if k2 > 0:
            fr.text((80 - (1 - k2) * 60, 660), "₹200 → ₹199", F("black", 104), INK); fr.text((84, 790), "feels like a deal", F("xb", 60), RED)
    elif tag == "cta":
        fr.text((70, 360), "₹199", F("black", 150), GREY)

def build(out):
    for L in LINES: L.speed = round(L.speed * 1.08, 3)
    R = Reel("S4_HookShots_02_Rs199", "swiss", LINES, tone="warm", seed=4)
    R.cap_style.update(fg=(255, 255, 255), hi=(255, 90, 90), bg=(15, 15, 15, 235))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Send this", icon="send", at=round(dur * .4, 2), xy=(90, 968), bg=RED, fg=(255, 255, 255))
    R.cta = dict(at=R.T("cta"), icon="send", head="Send this", body="to someone.\nThey won't believe it.", bg=INK, acc=RED, fg=(255, 255, 255), until=R.T("loop") - .05)
    stills = sorted([.4, .9] + [R.T(x) + .6 for x in ["fell", "left", "onetwo", "nyu", "only", "compare", "cta", "loop"]]
                    + [R.line("onetwo").t1 - .2, R.line("compare").t1 - .2, R.nudge["at"] + .5, dur - .2])
    return R, R.render(scene, out, stills=stills)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", R.violations[:20], len(R.violations))
