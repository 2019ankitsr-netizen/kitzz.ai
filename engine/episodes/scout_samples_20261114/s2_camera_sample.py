"""Scout sample 2 (14 Nov 2026): S2 AI Ki Kahani with shot-recipe cards + 2.5D layer camera. ~16 s, 3 pages.
Page 1 push_in on Tara · whip_pan · Page 2 parallax_slide (night) · whip_pan · Page 3 settle_bounce close-up, then drift.
The small "SHOT ·" label top-left is only for review; production episodes keep the series header there."""
import os, sys, math
HERE = os.path.dirname(__file__); ENG = os.path.join(HERE, "..", "..")
sys.path[:0] = [ENG, os.path.join(ENG, "pilots")]
from PIL import Image, ImageDraw
from reel import Reel, F, FM, W, H
from shots import Layer, cam, whip, compose
from s2_tara import BG, HL, house, bablu, tara, N, T_, B, L

LINES = [
    L(N, "बबलू के फ़ोन में आज, एक अनजानी आवाज़ आई।", "Bablu ke phone mein aaj ek anjaani awaaz aayi...", tag="p1", sfx="whoosh", gap=.3),
    L(T_, "नमस्ते बबलू! मैं तारा हूँ।", "Namaste Bablu! Main Tara hoon.", who="TARA", tag="t1", sfx="chime"),
    L(N, "उस रात, बबलू सो नहीं पाया।", "Us raat, Bablu so nahi paaya.", tag="p2", pre=.25),
    L(B, "तारा, तुम कभी सोती हो?", "Tara, tum kabhi soti ho?", who="BABLU", tag="b2"),
    L(T_, "नहीं बबलू। पर मैं भूल ज़रूर जाती हूँ।", "Nahi Bablu. Par main bhool zaroor jaati hoon.", who="TARA", tag="p3", pre=.25, pitch=.5, sfx="pop"),
    L(N, "भाग दो, कल।", "Part 2 kal.", tag="end", gap=.2),
]

# ---- static layers (built once) -------------------------------------------------------------
def big_sky(night):
    return Layer(BG[night].resize((W + 400, H + 240)), 0.0, (-200, -120))
def hills(night): return [Layer(h, .25 + .2 * i, (-80, 0)) for i, h in enumerate(HL[night])]
def house_layer(night, x=120, y=800):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); house(ImageDraw.Draw(im), x, y, night); return Layer(im, .55)
STATIC = {1: [big_sky(False)] + hills(False)[:1] + [house_layer(False)] + hills(False)[1:],
          2: [big_sky(True)] + hills(True)[:2] + [house_layer(True, 820, 900)] + hills(True)[2:],
          3: [big_sky(True)] + hills(True)[:1]}

def chars(page, t, R):
    sp = R.speaking(t); talk = lambda who: sp is not None and sp.spk == who
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if page == 1:
        bablu(im, 300, 700, talk(B), t); tara(im, 640, 650, talk(T_), t)
    elif page == 2:
        bablu(im, 330, 690, talk(B), t); tara(im, 600, 760, talk(T_), t)
    else:                                   # close-up: draw Tara small, crop, enlarge 2.1x
        sm = Image.new("RGBA", (W, H), (0, 0, 0, 0)); tara(sm, 440, 600, talk(T_), t)
        crop = sm.crop((410, 570, 680, 1000)); s = 2.1
        crop = crop.resize((int(crop.width * s), int(crop.height * s)), Image.LANCZOS)
        im.alpha_composite(crop, (int(540 - crop.width / 2), 300))
    return Layer(im, 1.0)

def page_layers(page, t, R): return STATIC[page] + [chars(page, t, R)]

FOCUS = {1: (740, 830), 2: (540, 900), 3: (540, 760)}
def page_cam(page, t, R):
    """The shot-recipe card for each page, timed to the narration."""
    if page == 1:
        t0, t1 = 0, R.T("p2"); return cam("push_in", (t - t0) / (t1 - t0), FOCUS[1], zoom=1.12), "push_in"
    if page == 2:
        t0, t1 = R.T("p2") - .2, R.T("p3"); return cam("parallax_slide", (t - t0) / (t1 - t0), FOCUS[2], dx=200), "parallax_slide"
    t0 = R.T("p3") - .2
    if t - t0 < .7: return cam("settle_bounce", (t - t0) / .7, FOCUS[3], over=1.07), "settle_bounce"
    return cam("drift", (t - t0 - .7) / 6, FOCUS[3], amp=8), "drift"

WHIP = .36
def scene(fr, t, R):
    cuts = [(R.T("p2") - .2, 1, 2), (R.T("p3") - .2, 2, 3)]
    page = 1 + sum(t >= c for c, _, _ in cuts)
    label = None
    for c, a, b in cuts:
        if c - WHIP / 2 <= t < c + WHIP / 2:
            k = (t - (c - WHIP / 2)) / WHIP
            out_c, in_c, show_in = whip(k, 1, blur=90)
            pg = b if show_in else a
            base_c, _ = page_cam(pg, max(t, c) if show_in else min(t, c - .01), R)
            cc = in_c if show_in else out_c
            cc.zoom *= base_c.zoom; cc.fx, cc.fy = base_c.fx, base_c.fy
            img = compose(page_layers(pg, t, R), cc, bg=(40, 44, 82)); label = "whip_pan"
            break
    else:
        c_, label = page_cam(page, t, R)
        img = compose(page_layers(page, t, R), c_, bg=(40, 44, 82))
    fr.img = img; fr.d = ImageDraw.Draw(fr.img)
    night = page > 1
    fr.text((90, 292), f"SAMPLE · SHOT: {label}", FM(30), (255, 220, 160) if night else (180, 70, 50))
    if t < R.lines[1].t0:
        fr.text((90, 340), "Tara ki\nawaaz", F("black", 80), (60, 35, 25), spacing=0)

if __name__ == "__main__":
    out = sys.argv[1]
    for L_ in LINES: L_.speed = round(L_.speed * 1.08, 3); L_.gap = min(L_.gap, .3)
    R = Reel("S2_sample_camera", "story", LINES, tone="bright", pitch=1.0, seed=21)
    R.cap_style.update(fg=(255, 250, 240), hi=(255, 200, 90), bg=(60, 35, 25, 215), who_fg=(255, 200, 90), who_stroke=(60, 35, 25))
    dur = R.build_audio(f"{out}/cache")
    stills = sorted([.3, 1.5, R.T("p2") - .25, R.T("p2") - .15, R.T("p2") + .4, (R.T("p2") + R.T("p3")) / 2,
                     R.T("p3") - .3, R.T("p3") - .1, R.T("p3") + .1, R.T("p3") + .4, R.T("p3") + 1.5, dur - .3])
    p = R.render(scene, out, stills=stills)
    print(p, round(dur, 1), "s violations:", R.violations[:6], len(R.violations))
