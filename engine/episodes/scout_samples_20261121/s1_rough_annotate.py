"""Scout sample 2 (21 Nov 2026): hand-drawn annotations (circle / underline / strike / box / highlight / bracket) that draw
themselves on the key word as the narrator says it. Method idea from rough-notation (MIT); our own Pillow code.
Demo topic in the S1 How Things Work look: how a microwave heats food."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from PIL import Image, ImageDraw
from reel import Reel, Line, F, FM, ease, eout, eback, W, H

NAVY, GRID, CYAN, AMB, WHITE = (10, 18, 38), (22, 36, 70), (120, 230, 255), (255, 200, 60), (255, 255, 255)
LINES = [
    Line("am_michael", "Your microwave does not heat food from the inside out.", "Your microwave does NOT heat food from the inside out.", speed=1.08, tag="hook", sfx="whoosh", gap=.3),
    Line("am_michael", "A part called the magnetron makes the microwaves.", speed=1.08, tag="mag"),
    Line("am_michael", "They flip water molecules back and forth, 2.45 billion times a second.",
         "They flip water molecules back and forth, 2.45 billion times a second.", speed=1.08, tag="spin"),
    Line("am_michael", "That jiggling is the heat. And it only reaches a few centimetres in.", speed=1.08, tag="heat"),
    Line("am_michael", "The middle cooks later, by plain old conduction.", speed=1.08, tag="mid"),
    Line("am_michael", "Save this, before you blame the microwave again.", speed=1.08, tag="cta", sfx="pop", gap=.2),
]

# ---------- rough annotation (our port of the rough-notation idea) ----------
def _noise(seed):
    r = random.Random(seed); ph = [r.uniform(0, 6.28) for _ in range(3)]
    return lambda u, a=1.0: a * (math.sin(u * 2.1 + ph[0]) * .5 + math.sin(u * 4.7 + ph[1]) * .3 + math.sin(u * 9.3 + ph[2]) * .2)

def ann_paths(kind, box, seed):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; w, h = x1 - x0, y1 - y0
    out = []
    for pss in range(2):                       # two hand-drawn passes, each slightly different
        n = _noise(seed * 7 + pss); r = random.Random(seed * 13 + pss); pts = []
        if kind == "circle":
            a0 = r.uniform(-2.6, -2.0); sweep = 2 * math.pi * r.uniform(1.04, 1.12)
            rx, ry = w / 2 + 26 + pss * 6, h / 2 + 22 + pss * 4
            for i in range(80):
                u = i / 79; a = a0 + sweep * u; j = 1 + 0.05 * n(u * 6)
                pts.append((cx + math.cos(a) * rx * j, cy + math.sin(a) * ry * j))
        elif kind in ("underline", "strike"):
            y = y1 + 12 if kind == "underline" else cy + 4
            for i in range(30):
                u = i / 29; pts.append((x0 - 8 + (w + 16) * u, y + n(u * 4, 4) + (pss * 6 - 3) * (u - .5) * (2 if kind == "strike" else 1)))
        elif kind == "box":
            p = 16 + pss * 4
            cs = [(x0 - p, y0 - p), (x1 + p, y0 - p), (x1 + p, y1 + p), (x0 - p, y1 + p), (x0 - p + 10, y0 - p - 4)]
            for k in range(4):
                (ax, ay), (bx, by) = cs[k], cs[k + 1]
                for i in range(12):
                    u = i / 11; pts.append((ax + (bx - ax) * u + n(k + u, 3), ay + (by - ay) * u + n(k + u + 5, 3)))
        elif kind == "bracket":
            x = x0 - 22 - pss * 4
            for i in range(40):
                u = i / 39
                if u < .15: pts.append((x + 26 * (1 - u / .15), y0 + n(u, 2)))
                elif u > .85: pts.append((x + 26 * ((u - .85) / .15), y1 + n(u, 2)))
                else: pts.append((x + n(u * 5, 3), y0 + (y1 - y0) * (u - .15) / .7))
        elif kind == "highlight":
            for i in range(30):
                u = i / 29; pts.append((x0 - 10 + (w + 20) * u, cy + n(u * 3, 3)))
        out.append(pts)
    return out

def draw_partial(d, pts, p, col, w):
    if p <= 0: return
    L = [0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    want = L[-1] * min(1, p); keep = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= want: keep.append(pts[i])
        else:
            f = (want - L[i - 1]) / max(1e-6, L[i] - L[i - 1]); a, b = pts[i - 1], pts[i]
            keep.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)); break
    if len(keep) > 1: d.line(keep, fill=col, width=w, joint="curve")
    for q in (keep[0], keep[-1]): d.ellipse((q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2), fill=col)

def annotate(img, kind, box, t, t0, dur=0.5, seed=1, col=AMB, w=9):
    if t < t0: return
    p = (t - t0) / dur
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    paths = ann_paths(kind, box, seed)
    if kind == "highlight":
        hgt = int((box[3] - box[1]) * .95); draw_partial(d, paths[0], eout(p / .8), col + (110,), hgt)
    else:
        draw_partial(d, paths[0], eout(p / .62), col + (255,), w)              # first pass
        draw_partial(d, paths[1], eout((p - .45) / .55), col + (255,), max(3, w - 3))   # quicker second pass
    img.alpha_composite(ov)

def wt(R, tag, word):
    """time the narrator reaches `word` in line `tag` (character-proportional estimate from the TTS line length)."""
    L = R.line(tag); i = L.say.find(word); return L.t0 + (L.t1 - L.t0) * max(0, i) / len(L.say)

# ---------- static background: S1 isometric grid ----------
BG = Image.new("RGBA", (W, H), NAVY + (255,)); _d = ImageDraw.Draw(BG)
for x in range(-W, 2 * W, 60):
    _d.line((x, 0, x + H * .577, H), fill=GRID, width=1); _d.line((x, 0, x - H * .577, H), fill=GRID, width=1)

def oven(img, t, R):
    d = ImageDraw.Draw(img)
    # cabinet (front + top + side in iso), cavity
    d.polygon([(110, 620), (580, 620), (580, 880), (110, 880)], fill=(30, 50, 90), outline=CYAN, width=4)
    d.polygon([(110, 620), (170, 575), (640, 575), (580, 620)], fill=(40, 70, 120), outline=CYAN, width=4)
    d.polygon([(580, 620), (640, 575), (640, 835), (580, 880)], fill=(22, 38, 72), outline=CYAN, width=4)
    d.rectangle((135, 645, 420, 855), fill=(14, 26, 52), outline=CYAN, width=3)
    # magnetron (top right) + waveguide
    d.rectangle((450, 650, 555, 720), fill=(70, 60, 140), outline=(170, 140, 255), width=4)
    for k in range(4): d.line((464 + k * 25, 662, 464 + k * 25, 708), fill=(170, 140, 255), width=3)
    d.line((450, 685, 420, 685), fill=(170, 140, 255), width=8)
    if t > R.T("mag") + .6:
        for k in range(3):
            ph = (t * 2.2 + k / 3) % 1; x = 415 - ph * 230; a = int(255 * (1 - ph))
            pts = [(x - 26 * math.sin(i / 4), 660 + i * 6) for i in range(30)]
            ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).line(pts, fill=(255, 200, 60, a), width=5); img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    heat = min(1, max(0, (t - R.T("heat")) / 1.2))
    d.chord((170, 760, 390, 850), 0, 180, fill=(220, 220, 235), outline=WHITE, width=3)
    d.ellipse((178, 730, 382, 792), fill=(255, int(150 - 60 * heat), 60), outline=WHITE, width=3)
    d.ellipse((215, 744, 345, 780), fill=(200, 120, 60) if heat > 0 else (255, 150, 60))
    if t > R.T("spin"):
        for k, (mx, my) in enumerate([(215, 752), (280, 746), (340, 754), (245, 772), (315, 774)]):
            a = math.sin(t * 40 + k) * .6
            for dx, dy, r_, c in [(0, 0, 9, (255, 90, 90)), (13 * math.cos(a + .9), 13 * math.sin(a + .9), 5, WHITE), (13 * math.cos(a - .9 + math.pi), 13 * math.sin(a - .9 + math.pi), 5, WHITE)]:
                d.ellipse((mx + dx - r_, my + dy - r_, mx + dx + r_, my + dy + r_), fill=c)

def scene(fr, t, R):
    img = BG.copy(); oven(img, t, R)
    fr.img = img; fr.d = ImageDraw.Draw(img)
    fr.text((92, 292), "HOW THINGS WORK · DEMO", FM(28), AMB)
    hk = eback(min(1, t / .3))
    fr.text((90, 340 - (1 - hk) * 40), "Heats from the", F("black", 74), WHITE)
    bb = fr.text((90, 425 - (1 - hk) * 40), "inside out?", F("black", 74), WHITE)
    annotate(img, "strike", bb, t, max(0.5, wt(R, "hook", "inside")), .45, seed=3, col=(255, 80, 80), w=12)
    fr.d = ImageDraw.Draw(img)
    if t > R.T("mag") - .1:
        fr.text((680, 590), "Magnetron", F("b", 42), (200, 180, 255))
        fr.d.line((675, 615, 560, 670), fill=(170, 140, 255), width=3)
        annotate(img, "circle", (450, 650, 555, 720), t, wt(R, "mag", "magnetron"), .55, seed=5)
    fr.d = ImageDraw.Draw(img)
    if t > R.T("spin"):
        fr.text((680, 680), "2.45 billion", F("black", 50), AMB)
        fr.text((680, 740), "flips / second", F("b", 36), WHITE)
        annotate(img, "underline", (680, 684, 960, 735), t, wt(R, "spin", "2.45"), .45, seed=8)
    fr.d = ImageDraw.Draw(img)
    if t > R.T("heat") + 1.0:
        x0, y0 = 680, 815
        hb = fr.d.textbbox((x0, y0), "few cm deep", font=F("black", 44))
        annotate(img, "highlight", hb, t, wt(R, "heat", "few"), .4, seed=2, col=(255, 80, 80))
        fr.d = ImageDraw.Draw(img); fr.text((x0, y0), "few cm deep", F("black", 44), WHITE)
        annotate(img, "bracket", (178, 728, 382, 794), t, wt(R, "heat", "few") + .1, .45, seed=4, col=(255, 80, 80), w=8)
    fr.d = ImageDraw.Draw(img)
    if t > R.T("mid") - .05:
        bb3 = fr.text((130, 925), "middle: conduction", F("b", 42), CYAN)
        annotate(img, "box", bb3, t, wt(R, "mid", "conduction"), .55, seed=6, col=CYAN, w=7)
    fr.d = ImageDraw.Draw(img)

def build(out):
    R = Reel("Scout2_S1_RoughAnnotations_EN", "xray", LINES, tone="warm", seed=4)
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Save for later", icon="save", at=round(dur * .4, 2), bg=(255, 200, 60), fg=(10, 18, 38), dur=1.8)
    R.cta = dict(at=R.T("cta"), icon="save", head="Save this", body="Before you blame\nthe microwave again.", bg=(255, 250, 240), acc=(225, 120, 20), fg=(10, 18, 38))
    st = sorted([.3, wt(R, "hook", "inside") + .6, wt(R, "mag", "magnetron") + .7, wt(R, "spin", "2.45") + .7,
                 wt(R, "heat", "few") + .6, wt(R, "mid", "conduction") + .7, dur - .3])
    return R, R.render(scene, out, stills=st)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R, p = build(out); print(p, round(R.dur, 1), "s violations:", len(R.violations), R.violations[:6])
