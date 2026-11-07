"""S2 AI Ki Kahani kit — Paper Pop-up Storybook scene shared by every Tara episode.

An episode supplies LINES (Hindi TTS, Roman Hinglish captions, tags), a cards(fr, t, R) callback for its pop-up
cards (drawn in y 340-632, above the characters), and a night tag (scene turns to night from that line)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import ImageDraw
from reel import Reel, Line, F, FM, ease, eout, eback, W, H
from s2_tara import BG, HL, house, bablu, tara, card, N, T_, B

def L(spk, say, cap, **k): return Line(spk, say, cap, lang="hi", **k)

def make_scene(ep, title, cards, night_tag, tara_from="hook", alarm=False):
    def scene(fr, t, R):
        T = R.T
        night = t >= T(night_tag) - .2
        fr.img = BG[night].copy(); d = ImageDraw.Draw(fr.img); fr.d = d
        sway = math.sin(t * .6)
        house(d, 120 + sway * 4, 800, night)
        for i, lay in enumerate(HL[night]): fr.img.alpha_composite(lay, (int(-80 + sway * (6 + 6 * i)), 0))
        sp = R.speaking(t)
        k = eback((t - .15) / .5)
        bablu(fr.img, 300, int(700 + (1 - k) * 400), sp is not None and sp.spk == B, t)
        t0 = T(tara_from) - .3 if tara_from != "hook" else .1
        kt = eback((t - t0) / .5) if t >= t0 else 0
        mood = "alarm" if (alarm and night and t < T("cta")) else "happy"
        if kt > 0: tara(fr.img, 640, int(650 + (1 - kt) * 500), sp is not None and sp.spk == T_, t, mood)
        fr.d = ImageDraw.Draw(fr.img)
        tc = (255, 220, 160) if night else (180, 70, 50); hc = (255, 245, 230) if night else (60, 35, 25)
        fr.text((90, 292), f"AI KI KAHANI · EP {ep}", FM(32), tc)
        first_card = min(L.t0 for L in R.lines if L.tag and L.tag != "hook") if R.lines else 3
        if t < R.lines[1].t0:
            kk = eout((t - .05) / .4)
            fr.text((90, 340 + (1 - kk) * 30), title, F("black", 80), hc, spacing=0)
        cards(fr, t, R)
    return scene

def build(name, ep, title, lines, cards, night_tag, out, nudge="Tag a friend who needs Tara", cta_body=None, cta_head=None, **kw):
    for L_ in lines: L_.speed = round(L_.speed * 1.08, 3); L_.gap = min(L_.gap, .3)
    R = Reel(name, "story", lines, tone="bright", pitch=1.0, seed=ep * 7)
    R.cap_style.update(fg=(255, 250, 240), hi=(255, 200, 90), bg=(60, 35, 25, 215), who_fg=(255, 200, 90), who_stroke=(60, 35, 25))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text=nudge, icon="send", at=round(dur * .38, 2), bg=(60, 35, 25), fg=(255, 245, 230))
    R.cta = dict(at=R.T("cta"), icon="follow", head=cta_head or f"Part {ep + 1} kal", body=cta_body or "Follow karo, warna\nTara ka sach\nmiss ho jayega.",
                 bg=(255, 250, 240), acc=(200, 80, 40), fg=(60, 35, 25))
    stills = sorted([.7] + [L_.t0 + .9 for L_ in lines] + [R.nudge["at"] + 1, dur - .3])
    return R, R.render(make_scene(ep, title, cards, night_tag, **kw), out, stills=stills)

def text_card(fr, t, start, end, lines_, box=(90, 340, 990, 632), fill=(255, 250, 240)):
    """Fold-up paper card with a list of (text, size, colour, weight, appear_at) rows."""
    if not (start - .1 <= t < end): return
    y = card(fr, box, eback((t - start) / .5), fill=fill)
    if y is None or y > box[1] + 20: return
    yy = box[1] + 30
    for txt, size, col, wt, at in lines_:
        if t >= at:
            k = eout((t - at) / .3)
            fr.text((130 + (1 - k) * 20, yy), txt, F(wt, size), col)
        yy += int(size * 1.18)
