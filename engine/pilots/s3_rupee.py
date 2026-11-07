"""S3 CCTV Riddles · Case 01 · The missing ₹1 — CCTV Case File."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from reel import Reel, Line, F, FM, ease, eout, eback, W, H

D, E = "am_fenrir", "bf_emma"
LINES = [
    Line(D, "One rupee vanished from this counter. | Nobody stole it.", speed=1.05, tag="hook", sfx="static", gap=.3),
    Line(E, "CCTV log. | Camera three. | Highway dhaba. | Twenty-one fourteen.", "CCTV log · Cam 03 · Highway dhaba · 21:14", tag="log", sfx="beep", gap=.3),
    Line(D, "Three friends ask for a room. | ₹30. | They pay ₹10 each.", "3 friends ask for a room. ₹30. They pay ₹10 each.", tag="pay", sfx="tick"),
    Line(D, "Later, the owner says, | wait, the room is only ₹25. | He sends the helper back with ₹5.",
         "Later the owner says: wait, the room is only ₹25. He sends the helper back with ₹5.", tag="refund"),
    Line(D, "The helper can't split five three ways. | He gives each friend ₹1 back, | and keeps ₹2.",
         "The helper can't split 5 three ways. He gives each friend ₹1 back and keeps ₹2.", tag="split", sfx="tick"),
    Line(D, "Now do the maths. | Each friend paid ₹9. | Nine times three, | ₹27. | Plus the helper's ₹2... | ₹29.",
         "Now do the maths. Each friend paid ₹9. 9 × 3 = ₹27. Plus the helper's ₹2... ₹29.", speed=.95, pitch=-.5, tag="math", drop=True, sfx="static"),
    Line(D, "So where did the last rupee go?", pre=.5, pitch=1, tag="where", sfx="hit", gap=.45),
    Line(D, "Rewind the tape. | The clue is in what you just added.", tag="clue"),
    Line(D, "Answer in the comments. | Send it to the smartest person you know.", tag="cta", sfx="pop", gap=.25),
    Line(D, "Play it back. | One rupee is still missing.", tag="loop", gap=.1),
]
for L in LINES:
    if L.spk == D: L.pitch -= .5          # chosen take: Fenrir, a touch lower

RNG = np.random.default_rng(3)
NOISE = [Image.fromarray(RNG.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)).resize((W, H)).convert("RGB") for _ in range(6)]
SCAN = Image.new("RGBA", (W, H), (0, 0, 0, 0)); _sd = ImageDraw.Draw(SCAN)
for y in range(0, H, 6): _sd.line((0, y, W, y), fill=(0, 0, 0, 70), width=2)

def counter_bg():
    im = Image.new("RGB", (W, H), (34, 36, 34)); d = ImageDraw.Draw(im)
    d.rectangle((70, 280, 1010, 1240), fill=(46, 48, 44))
    for x in range(70, 1010, 70): d.line((x, 280, x, 1240), fill=(52, 54, 50), width=2)          # floor tiles
    for y in range(280, 1240, 70): d.line((70, y, 1010, y), fill=(52, 54, 50), width=2)
    d.rectangle((70, 280, 1010, 470), fill=(58, 60, 55))                                            # back wall + shelves
    for i in range(5): d.rectangle((110 + i * 175, 300, 240 + i * 175, 330), fill=(80, 82, 76))
    d.rectangle((140, 560, 940, 680), fill=(88, 90, 82)); d.rectangle((140, 560, 940, 580), fill=(110, 112, 104))   # counter
    d.rectangle((640, 590, 760, 660), fill=(70, 72, 66)); d.rectangle((650, 600, 750, 650), fill=(100, 100, 90))   # cash box
    for x, y in ((180, 1120), (900, 1100)): d.ellipse((x - 50, y - 50, x + 50, y + 50), fill=(60, 62, 58))         # stools / tables
    return im
CBG = counter_bg()

def person(d, x, y, r, col, label=None):
    d.ellipse((x - r * 1.5, y - r * .7, x + r * 1.5, y + r * .9), fill=tuple(int(c * .7) for c in col))   # shoulders
    d.ellipse((x - r, y - r, x + r, y + r), fill=col)

def note(fr, x, y, s, col=(180, 200, 170)):
    d = fr.d; d.rounded_rectangle((x - 62, y - 32, x + 62, y + 32), 8, fill=col, outline=(60, 70, 60), width=3)
    fr.text((x, y), s, F("xb", 40), (30, 40, 30), anchor="mm")

def coin(fr, x, y, s):
    d = fr.d; d.ellipse((x - 38, y - 38, x + 38, y + 38), fill=(210, 190, 120), outline=(120, 100, 50), width=3)
    fr.text((x, y), s, F("xb", 34), (60, 45, 15), anchor="mm")

FRIENDS = [(300, 860), (540, 900), (780, 860)]
OWNER = (420, 520); HELPER0 = (860, 520)

def cctv(fr, t, R):
    T = R.T
    img = CBG.copy(); fr.img = img; d = ImageDraw.Draw(img); fr.d = d
    # people
    for x, y in FRIENDS: person(d, x, y, 46, (150, 152, 140))
    person(d, *OWNER, 48, (130, 125, 115))
    # helper path: counter -> friends -> back
    hr, hs = R.line("refund"), R.line("split")
    if t < hr.t1 - .6: hx, hy = HELPER0
    elif t < hs.t0 + .4:
        k = ease((t - (hr.t1 - .6)) / (hs.t0 + .4 - (hr.t1 - .6))); hx, hy = HELPER0[0] + (540 - HELPER0[0]) * k, HELPER0[1] + (760 - HELPER0[1]) * k
    else: hx, hy = 540, 760
    person(d, hx, hy, 36, (120, 128, 118))
    # money
    p = R.line("pay")
    if p.t0 <= t < T("split") + 3:
        for i, (x, y) in enumerate(FRIENDS):
            k = ease((t - p.t0 - 1.2 - i * .35) / .6)
            note(fr, x + (600 - x) * k * .0 + (0 if k < 1 else 0), y - 110 - (y - 640) * k * .8, "₹10")
    if hr.t0 + 1.5 <= t < hs.t0 + .6:
        coin(fr, hx - 60, hy, "₹5")
    if t >= hs.t0 + .6:
        for i, (x, y) in enumerate(FRIENDS):
            k = eout((t - hs.t0 - 1.2 - i * .3) / .5)
            if k > 0: coin(fr, 540 + (x - 540) * k, 760 + (y - 70 - 760) * k, "₹1")
        k = eout((t - hs.t0 - 2.6) / .5)
        if k > 0: coin(fr, hx + 70, hy - 10, "₹2")
    # camera push-in during the split
    z = 1 + .08 * ease((t - hs.t0) / 4) if t >= hs.t0 else 1
    if z > 1:
        cw, ch = W / z, H / z; cx, cy = 540, 760
        fr.img = fr.img.crop((cx - cw / 2, cy - ch / 2 + 40, cx + cw / 2, cy + ch / 2 + 40)).resize((W, H))
        fr.boxes = [(lab, ((x0 - (cx - cw / 2)) * z, (y0 - (cy - ch / 2 + 40)) * z, (x1 - (cx - cw / 2)) * z, (y1 - (cy - ch / 2 + 40)) * z))
                    for lab, (x0, y0, x1, y1) in fr.boxes]
    # grain + blur + scanlines
    fr.img = Image.blend(fr.img.filter(ImageFilter.GaussianBlur(1.1)), NOISE[int(t * 15) % 6], .14).convert("RGBA")
    fr.img.alpha_composite(SCAN); fr.img = fr.img.convert("RGB")
    d = ImageDraw.Draw(fr.img); fr.d = d
    d.rectangle((70, 280, 1010, 1240), outline=(200, 205, 195), width=3)
    if int(t * 2) % 2 == 0: d.ellipse((100, 310, 132, 342), fill=(230, 40, 40))
    fr.text((145, 309), "REC", FM(34), (235, 235, 225))
    fr.text((985, 309), "CAM 03", FM(34), (235, 235, 225), anchor="ra")
    s = 14 * 60 + 22 + int(t); fr.text((100, 360), f"07-11-2026  21:{s // 60:02d}:{s % 60:02d}", FM(34), (235, 235, 225))

BOARD = None
def board_bg():
    im = Image.new("RGB", (W, H), (48, 34, 26)); d = ImageDraw.Draw(im); r = random.Random(2)
    for _ in range(9000):
        x, y = r.randint(0, W), r.randint(0, H); c = r.randint(-14, 14); d.point((x, y), fill=(48 + c, 34 + c, 26 + c))
    return im
BOARD = board_bg()

CARDS = [  # (text, box, appears at fraction of the math line)
    ("₹30 paid", (100, 330, 470, 440), -1),
    ("₹25 bill", (560, 350, 930, 460), -1),
    ("₹5 back =\n₹1+₹1+₹1+₹2", (100, 510, 520, 690), -1),
    ("₹9 × 3 = ₹27", (580, 560, 930, 670), .25),
    ("₹27 + ₹2 = ₹29 ?", (150, 790, 900, 940), .7),
]
def pin(d, x, y): d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(220, 40, 40)); d.ellipse((x - 5, y - 7, x + 1, y - 1), fill=(255, 150, 150))

def board(fr, t, R):
    fr.img = BOARD.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    m = R.line("math"); pm = (t - m.t0) / (m.t1 - m.t0)
    shown = []
    for i, (txt, (x0, y0, x1, y1), at) in enumerate(CARDS):
        st = m.t0 + .2 + i * .25 if at < 0 else m.t0 + at * (m.t1 - m.t0)
        k = eback((t - st) / .4)
        if k <= 0: continue
        shown.append(((x0 + x1) / 2, y0))
        ox = (1 - k) * 40
        d.rectangle((x0 + 8 + ox, y0 + 10, x1 + 8 + ox, y1 + 10), fill=(20, 14, 10))
        last = i == 4
        d.rectangle((x0 + ox, y0, x1 + ox, y1), fill=(250, 238, 200) if not last else (255, 225, 210))
        fr.text((x0 + 30 + ox, (y0 + y1) / 2), txt, F("black", 54 if not last else 66), (40, 30, 20) if not last else (180, 30, 30), anchor="lm", spacing=6)
        pin(d, (x0 + x1) / 2 + ox, y0 + 4)
    for a, b in zip(shown, shown[1:]): d.line((a[0], a[1] + 4, b[0], b[1] + 4), fill=(200, 30, 30), width=4)
    # the clue: circle the "+ ₹2"
    c = R.line("clue")
    if t >= c.t0 + .8 and t < R.T("cta") + .2:
        k = ease((t - c.t0 - .8) / .6)
        f = F("black", 66); x0 = 150 + 30 + d.textlength("₹27 ", font=f); x1 = 150 + 30 + d.textlength("₹27 + ₹2", font=f)
        d.arc((x0 - 30, 815, x1 + 30, 915), -90, -90 + 360 * k, fill=(255, 215, 0), width=8)
    fr.text((90, 292), "CASE #01 · EVIDENCE", FM(34), (255, 220, 80))
    w = R.line("where")
    if w.t0 - .1 <= t < c.t0:
        k = eout((t - w.t0) / .4); fr.text((540, 1000 - 20 * k), "Where's ₹1?", F("black", 76), (255, 220, 80), anchor="mm")

def scene(fr, t, R):
    m = R.T("math"); c = R.line("clue"); lp = R.T("loop")
    rewind = c.t0 <= t < c.t0 + .8
    if t < m - .15 or rewind or t >= lp:
        cctv(fr, t if not rewind else max(0, R.T("split") + 3 - (t - c.t0) * 8), R)
        if rewind:
            d = fr.d
            for i in range(2): d.polygon([(700 + i * 60, 760), (760 + i * 60, 720), (760 + i * 60, 800)], fill=(255, 255, 255))
            fr.text((540, 700), "REWIND", FM(56), (255, 255, 255), anchor="mm")
    else:
        board(fr, t, R)
    # static glitch at cuts
    for tc in (m - .15, c.t0, c.t0 + .8, lp):
        if 0 <= t - tc < .2:
            fr.img = Image.blend(fr.img.convert("RGB"), NOISE[int(t * 30) % 6], .6); fr.d = ImageDraw.Draw(fr.img)
    if t < R.T("pay") - .1 and t < 2.6:
        k = eout((t - .05) / .3)
        fr.d.rectangle((90, 430, 990, 610), fill=(0, 0, 0))
        fr.text((120, 445 + (1 - k) * 20), "One rupee vanished.\nNobody stole it.", F("black", 70), (255, 255, 255), spacing=4)

def build(out):
    R = Reel("S3_CCTVRiddle_case01_MissingRupee", "cctv", LINES, tone="warm", seed=3)
    R.cap_style.update(hi=(255, 220, 80), bg=(0, 0, 0, 200))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Send to your smartest friend", icon="send", at=round(dur * .4, 2), xy=(90, 430), bg=(255, 220, 80), fg=(20, 20, 20))
    R.cta = dict(at=R.T("cta"), until=R.T("loop") - .05, icon="comment", head="Your answer?", body="Comment it. Then send\nit to the smartest\nperson you know.",
                 bg=(250, 238, 200), acc=(200, 30, 30), fg=(40, 30, 20))
    tags = ["hook", "log", "pay", "refund", "split", "math", "where", "clue", "cta", "loop"]
    stills = sorted([.7] + [R.T(x) + 1.2 for x in tags] + [R.line("math").t1 - .2, R.nudge["at"] + .5, R.line("clue").t0 + .3, dur - .3])
    return R, R.render(scene, out, stills=stills)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", R.violations[:20], len(R.violations))
