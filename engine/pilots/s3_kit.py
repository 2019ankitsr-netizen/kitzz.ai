"""S3 CCTV Riddles kit — helpers shared by every case: CCTV finish (grain, scanlines, HUD), evidence board, glitch cuts."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reel import Reel, Line, F, FM, ease, eout, eback, W, H
from s3_rupee import NOISE, SCAN, BOARD, person, pin

D, E = "am_fenrir", "bf_emma"
def DL(say, cap=None, **k):
    k["pitch"] = k.get("pitch", 0) - .5; return Line(D, say, cap, **k)
def EL(say, cap=None, **k): return Line(E, say, cap, **k)

def cctv_finish(fr, t, cam="CAM 03", date="07-11-2026", start=(21, 14, 22)):
    fr.img = Image.blend(fr.img.convert("RGB").filter(ImageFilter.GaussianBlur(1.1)), NOISE[int(t * 15) % 6], .14).convert("RGBA")
    fr.img.alpha_composite(SCAN); fr.img = fr.img.convert("RGB")
    d = ImageDraw.Draw(fr.img); fr.d = d
    d.rectangle((70, 280, 1010, 1240), outline=(200, 205, 195), width=3)
    if int(t * 2) % 2 == 0: d.ellipse((100, 310, 132, 342), fill=(230, 40, 40))
    fr.text((145, 309), "REC", FM(34), (235, 235, 225)); fr.text((985, 309), cam, FM(34), (235, 235, 225), anchor="ra")
    s = start[0] * 3600 + start[1] * 60 + start[2] + int(t)
    fr.text((100, 360), f"{date}  {s // 3600 % 24:02d}:{s // 60 % 60:02d}:{s % 60:02d}", FM(34), (235, 235, 225))

def board_base(fr, header):
    fr.img = BOARD.copy(); fr.d = ImageDraw.Draw(fr.img); fr.text((90, 292), header, FM(34), (255, 220, 80))

def draw_cards(fr, t, cards):
    """cards: [(text, box, start_time, style)] style: 'note' | 'key' | 'answer'"""
    d = fr.d; shown = []
    for txt, (x0, y0, x1, y1), st, style in cards:
        k = eback((t - st) / .4)
        if k <= 0: continue
        ox = (1 - k) * 40; shown.append(((x0 + x1) / 2 + ox, y0))
        fill = {"note": (250, 238, 200), "key": (255, 225, 210), "answer": (215, 245, 215)}[style]
        col = {"note": (40, 30, 20), "key": (180, 30, 30), "answer": (20, 100, 40)}[style]
        d.rectangle((x0 + 8 + ox, y0 + 10, x1 + 8 + ox, y1 + 10), fill=(20, 14, 10)); d.rectangle((x0 + ox, y0, x1 + ox, y1), fill=fill)
        size = 54 if style == "note" else 60
        while size > 40 and max(d.textlength(r, font=F("black", size)) for r in txt.split("\n")) > (x1 - x0) - 50: size -= 2
        fr.text((x0 + 30 + ox, (y0 + y1) / 2), txt, F("black", size), col, anchor="lm", spacing=6)
        pin(d, (x0 + x1) / 2 + ox, y0 + 4)
    for a, b in zip(shown, shown[1:]): d.line((a[0], a[1] + 4, b[0], b[1] + 4), fill=(200, 30, 30), width=4)

def glitch(fr, t, cuts):
    for tc in cuts:
        if 0 <= t - tc < .2:
            fr.img = Image.blend(fr.img.convert("RGB"), NOISE[int(t * 30) % 6], .6); fr.d = ImageDraw.Draw(fr.img)

def hook_box(fr, t, text, until):
    if t < until:
        k = eout((t - .05) / .3); fr.d.rectangle((90, 430, 990, 610), fill=(0, 0, 0))
        fr.text((120, 445 + (1 - k) * 20), text, F("black", 66), (255, 255, 255), spacing=4)

def build(name, case, lines, scene, out, stills_tags):
    R = Reel(name, "cctv", lines, tone="warm", seed=30 + case)
    R.cap_style.update(hi=(255, 220, 80), bg=(0, 0, 0, 200))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Send to a smart friend", icon="send", at=round(dur * .38, 2), bg=(255, 220, 80), fg=(20, 20, 20))
    R.cta = dict(at=R.T("cta"), until=R.T("loop") - .05, icon="comment", head="Your answer?", body="Comment it. Then send\nit to the smartest\nperson you know.",
                 bg=(250, 238, 200), acc=(200, 30, 30), fg=(40, 30, 20))
    stills = sorted([.7] + [R.T(x) + 1.2 for x in stills_tags] + [R.nudge["at"] + 1, dur - .3])
    return R, R.render(scene, out, stills=stills)
