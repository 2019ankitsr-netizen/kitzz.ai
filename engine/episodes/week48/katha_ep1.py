"""Dev Katha · Ep 1 · "Kashi ka Kotwal kaun?" (Kaal Bhairav) — STYLE: Kalamkari Ink (approved 9 Nov 2026).
Everything draws itself stroke by stroke in dark-brown ink on handmade cream paper, flat folk fills fade in after the outline,
a quill nib follows headlines, ink-bleed transitions between scenes. Original folk-style figures only.
Story per Kaal Bhairav Mandir legend (Brahma's fifth head, Kapal Mochan Teerth in Varanasi, dog vahana);
Kalabhairav Jayanti: Tuesday 1 Dec 2026 (Drik Panchang / HinduTone)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from kit import *                      # noqa: F401,F403
from drawon import Sketch, ellipse_pts, bez, leaf
import lines48 as LN
import audio as A

NAME = "DevKatha_Ep01_KaalBhairav"
INK = (43, 27, 18); RED = (168, 50, 42); SAF = (224, 138, 30); GOLD = (217, 164, 58); GOLDL = (240, 207, 122)
IND = (47, 74, 122); DIND = (34, 40, 78); GRN = (79, 122, 58); SKIN = (231, 185, 138); CREAM = (251, 243, 220); BLUE = (88, 130, 190)

def make_bg():
    im = paper(); d = ImageDraw.Draw(im)
    for y0, fl in ((150, 1), (1770, -1)):           # scalloped Kalamkari borders, outside the safe zone
        d.rectangle((0, y0 - 22, W, y0 + 22), fill=RED); d.line((0, y0 - 22, W, y0 - 22), fill=INK, width=4); d.line((0, y0 + 22, W, y0 + 22), fill=INK, width=4)
        for i in range(0, W + 60, 60):
            d.ellipse((i - 9, y0 - 9, i + 9, y0 + 9), fill=GOLD)
            yb = y0 + 22 * fl; pts = bez((i - 30, yb), (i - 15, yb + 46 * fl), (i + 15, yb + 46 * fl), (i + 30, yb), 10)
            d.polygon(pts, fill=SAF, outline=INK); d.ellipse((i - 5, yb + 18 * fl - 5, i + 5, yb + 18 * fl + 5), fill=RED)
        for i in range(30, W, 120):                     # little leaf motifs in the band
            d.polygon(leaf(i, y0 - 80 * fl, 50, 22, 90), fill=GRN, outline=INK)
    return im
BGI = make_bg()

# ---------------------------------------------------------------- folk figures (Sketch builders)
def eye(sk, x, y, s, fierce=False):
    sk.shape(leaf(x, y, 40 * s, 18 * s, 0), fill=(255, 250, 240), col=INK, w=max(2, int(4 * s)))
    sk.dot(x, y, 6 * s, RED if fierce else INK)

def head(sk, cx, cy, s, skin, crown=GOLD, fierce=False, small=False, beard=False):
    sk.shape(ellipse_pts(cx, cy, 56 * s, 64 * s), fill=skin, col=INK, w=max(2, int(5 * s)))
    cr = [(cx - 48 * s, cy - 44 * s), (cx + 48 * s, cy - 44 * s), (cx + 30 * s, cy - 140 * s), (cx, cy - 175 * s), (cx - 30 * s, cy - 140 * s)]
    sk.shape(cr, fill=crown, col=INK, w=max(2, int(5 * s)))
    for k in range(3): sk.dot(cx - 20 * s + k * 20 * s, cy - 80 * s, 6 * s, RED)
    eye(sk, cx - 22 * s, cy - 2 * s, s, fierce); eye(sk, cx + 22 * s, cy - 2 * s, s, fierce)
    sk.line([(cx, cy - 36 * s), (cx, cy - 20 * s)], RED, max(2, int(6 * s)))
    if fierce:
        for sx in (-1, 1): sk.line(bez((cx, cy + 26 * s), (cx + sx * 30 * s, cy + 18 * s), (cx + sx * 50 * s, cy + 30 * s), (cx + sx * 56 * s, cy + 14 * s), 10), INK, max(2, int(7 * s)))
    if beard: sk.shape([(cx - 40 * s, cy + 30 * s), (cx + 40 * s, cy + 30 * s), (cx, cy + 95 * s)], fill=(245, 245, 240), col=INK, w=max(2, int(4 * s)))
    sk.line(bez((cx - 12 * s, cy + 38 * s), (cx - 4 * s, cy + 44 * s), (cx + 4 * s, cy + 44 * s), (cx + 12 * s, cy + 38 * s), 6), RED, max(2, int(5 * s)))

def figure(cx, cy, s, skin, robe, halo=GOLDL, heads=1, fierce=False, flames=False, trishul=False, seed=1, beard=False):
    sk = Sketch(wobble=1.2, seed=seed)
    if flames:
        for i in range(18):
            a = i / 18 * 2 * math.pi; r = 150 * s
            sk.shape(leaf(cx + r * math.cos(a), cy - 20 * s + r * math.sin(a), 70 * s, 34 * s, math.degrees(a)), fill=SAF if i % 2 else RED, col=INK, w=3, cost=8)
    sk.shape(ellipse_pts(cx, cy - 20 * s, 120 * s, 120 * s), fill=halo, col=INK, w=4)
    body = [(cx - 70 * s, cy + 80 * s), (cx + 70 * s, cy + 80 * s), (cx + 125 * s, cy + 360 * s), (cx - 125 * s, cy + 360 * s)]
    sk.shape(body, fill=robe, col=INK, w=5)
    for k in range(5): sk.line([(cx - 110 * s + k * 55 * s, cy + 330 * s), (cx - 95 * s + k * 55 * s, cy + 352 * s)], GOLD, max(2, int(6 * s)))
    sk.line([(cx - 70 * s, cy + 150 * s), (cx + 70 * s, cy + 150 * s)], GOLD, max(2, int(10 * s)))
    for sx in (-1, 1):
        arm = bez((cx + sx * 66 * s, cy + 95 * s), (cx + sx * 140 * s, cy + 150 * s), (cx + sx * 135 * s, cy + 220 * s), (cx + sx * 80 * s, cy + 245 * s), 16)
        sk.line(arm, INK, int(32 * s)); sk.line(arm, skin, int(22 * s))
    if trishul:
        x = cx + 150 * s; sk.line([(x, cy + 330 * s), (x, cy - 170 * s)], INK, int(10 * s))
        sk.line(bez((x - 50 * s, cy - 230 * s), (x - 50 * s, cy - 170 * s), (x + 50 * s, cy - 170 * s), (x + 50 * s, cy - 230 * s), 12), INK, int(9 * s))
        sk.line([(x, cy - 175 * s), (x, cy - 250 * s)], INK, int(9 * s))
        for px in (-50, 0, 50): sk.shape([(x + px * s - 12 * s, cy - (230 if px else 250) * s), (x + px * s + 12 * s, cy - (230 if px else 250) * s), (x + px * s, cy - (265 if px else 290) * s)], fill=GOLD, col=INK, w=3, cost=8)
    if heads >= 3:
        for sx in (-1, 1): head(sk, cx + sx * 74 * s, cy + 8 * s, s * .78, skin, beard=beard)
    head(sk, cx, cy, s, skin, fierce=fierce, beard=beard)
    if heads == 5: head(sk, cx, cy - 230 * s, s * .6, skin, crown=GOLDL, beard=beard)
    return sk

def kashi(seed=3):
    sk = Sketch(wobble=1.0, seed=seed); base = 1000
    for (cx, w, h, col) in ((230, 120, 300, RED), (540, 160, 420, SAF), (840, 120, 300, RED)):
        sh = bez((cx - w, base - 120), (cx - w, base - h * .7), (cx - w * .3, base - h), (cx, base - h - 20), 18) + \
             bez((cx, base - h - 20), (cx + w * .3, base - h), (cx + w, base - h * .7), (cx + w, base - 120), 18)
        sk.shape(sh + [(cx + w, base - 120)], fill=col, col=INK, w=5)
        for k in range(4): sk.line([(cx - w + 12, base - 150 - k * 50), (cx + w - 12, base - 150 - k * 50)], INK, 3)
        sk.line([(cx, base - h - 20), (cx, base - h - 90)], INK, 5)
        sk.shape([(cx, base - h - 90), (cx + 50, base - h - 72), (cx, base - h - 55)], fill=RED, col=INK, w=3, cost=8)
        sk.shape([(cx - w - 10, base - 120), (cx + w + 10, base - 120), (cx + w + 10, base - 40), (cx - w - 10, base - 40)], fill=GOLDL, col=INK, w=4)
    for k in range(4): sk.line([(90, base - 40 + k * 14), (990, base - 40 + k * 14)], INK, 3)          # ghat steps
    for row in range(2):
        pts = [(90 + i * 15, base + 30 + row * 26 + 8 * math.sin(i / 2.2)) for i in range(61)]
        sk.line(pts, IND, 6)
    return sk

def dog(cx=300, cy=780, s=1.0):
    sk = Sketch(wobble=1.0, seed=9); col = DIND
    sk.shape(ellipse_pts(cx, cy + 90 * s, 120 * s, 150 * s), fill=col, col=INK, w=5)                     # body (sitting)
    sk.shape(ellipse_pts(cx + 40 * s, cy - 90 * s, 70 * s, 62 * s), fill=col, col=INK, w=5)              # head
    sk.shape([(cx + 90 * s, cy - 100 * s), (cx + 170 * s, cy - 80 * s), (cx + 160 * s, cy - 50 * s), (cx + 95 * s, cy - 55 * s)], fill=col, col=INK, w=5)
    sk.dot(cx + 168 * s, cy - 72 * s, 10 * s, INK)
    sk.shape([(cx + 5 * s, cy - 130 * s), (cx + 30 * s, cy - 200 * s), (cx + 55 * s, cy - 135 * s)], fill=col, col=INK, w=5)
    sk.shape(leaf(cx + 70 * s, cy - 98 * s, 30 * s, 14 * s, 0), fill=(255, 250, 240), col=INK, w=3); sk.dot(cx + 74 * s, cy - 98 * s, 5 * s, INK)
    sk.line(bez((cx - 40 * s, cy - 35 * s), (cx + 10 * s, cy - 10 * s), (cx + 70 * s, cy - 10 * s), (cx + 100 * s, cy - 40 * s), 12), RED, int(14 * s))
    sk.dot(cx + 30 * s, cy - 5 * s, 12 * s, GOLD)
    for lx in (cx + 40 * s, cx + 90 * s): sk.line([(lx, cy + 100 * s), (lx, cy + 235 * s)], INK, int(12 * s))
    sk.line(bez((cx - 110 * s, cy + 190 * s), (cx - 200 * s, cy + 170 * s), (cx - 210 * s, cy + 80 * s), (cx - 170 * s, cy + 40 * s), 14), INK, int(12 * s))
    for i in range(5): sk.line([(cx - 80 * s + i * 20 * s, cy + 60 * s), (cx - 70 * s + i * 20 * s, cy + 80 * s)], GOLD, 4)
    return sk

def small_head(sk, cx, cy, s=.45): head(sk, cx, cy, s, SKIN, beard=True)

SK = {}
def sk(key):
    if key in SK: return SK[key]
    if key == "kashi": v = kashi()
    elif key == "brahma": v = figure(300, 640, .78, SKIN, RED, heads=5, beard=True, seed=2)
    elif key == "vishnu": v = figure(790, 640, .78, BLUE, GRN, seed=4)
    elif key == "brahma_big": v = figure(540, 720, 1.05, SKIN, RED, heads=5, beard=True, seed=2)
    elif key == "bhairav": v = figure(540, 690, 1.0, DIND, RED, halo=SAF, fierce=True, flames=True, trishul=True, seed=6)
    elif key == "bhairav_s": v = figure(360, 700, .75, DIND, RED, halo=SAF, fierce=True, trishul=True, seed=6)
    elif key == "dog": v = dog(300, 780, 1.0)
    elif key == "qmark":
        v = Sketch(wobble=1.0, seed=5); pts = bez((430, 560), (430, 430), (650, 430), (650, 560), 20) + bez((650, 560), (650, 640), (540, 640), (540, 720), 12)
        v.line(pts, INK, 46); v.line(pts, RED, 32); v.dot(540, 800, 30, INK); v.dot(540, 800, 22, RED)
    elif key == "pillar":
        v = Sketch(wobble=0, seed=1); xs = []
        left = [(540 - 70 - 14 * math.sin(y / 30), y) for y in range(1040, 360, -20)]
        right = [(540 + 70 + 14 * math.sin(y / 30 + 1), y) for y in range(360, 1041, 20)]
        v.line(left, INK, 6); v.line(right[::-1], INK, 6)
        v.fill(left + right, SAF, cost=120); v.fill([(x * .55 + 540 * .45, y) for x, y in left] + [(x * .55 + 540 * .45, y) for x, y in right], GOLDL, cost=60)
    else: raise KeyError(key)
    SK[key] = v; return v

def nib(d, tip, t):
    if not tip: return
    x, y = tip; a = math.radians(-35 + 6 * math.sin(t * 9))
    p = [(x, y), (x + 26 * math.cos(a) - 9 * math.sin(a), y - 26 * math.sin(a) - 9 * math.cos(a)), (x + 120 * math.cos(a), y - 120 * math.sin(a)),
         (x + 26 * math.cos(a) + 9 * math.sin(a), y - 26 * math.sin(a) + 9 * math.cos(a))]
    d.polygon(p, fill=GOLD, outline=INK); d.line([p[0], p[2]], fill=INK, width=2)

def write(fr, t, t0, txt, xy, font, col=INK, dur=1.0, anchor="mm", stroke=0, scol=CREAM):
    """Headline that writes itself left to right with the quill nib at the edge."""
    if t < t0: return
    k = prog(t, t0, dur)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    bb = ld.textbbox(xy, txt, font=font, anchor=anchor, stroke_width=stroke)
    ld.text(xy, txt, font=font, fill=col + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=scol)
    x1 = bb[0] + (bb[2] - bb[0]) * eio_(k)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle((0, 0, x1, H), fill=255)
    lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", (W, H), 0), m))
    fr.img = Image.alpha_composite(fr.img.convert("RGBA"), lay).convert("RGB"); fr.d = ImageDraw.Draw(fr.img)
    fr.boxes.append((txt[:30], bb))
    if k < 1: nib(fr.d, (x1, (bb[1] + bb[3]) / 2 + 10), t)
def eio_(x): x = clamp(x); return x * x * (3 - 2 * x)

def glow(fr, cx, cy, r, col, a=110):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for i in range(8):
        rr_ = r * (1 - i / 8); od.ellipse((cx - rr_, cy - rr_, cx + rr_, cy + rr_), fill=col + (int(a / 8),))
    fr.img = Image.alpha_composite(fr.img.convert("RGBA"), ov).convert("RGB"); fr.d = ImageDraw.Draw(fr.img)

def flames(d, cx, cy, t, n=7, r=60):
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * .38; h = r * (1 + .25 * math.sin(t * 13 + i * 1.7))
        d.polygon(leaf(cx + math.cos(a) * r * .6, cy + math.sin(a) * r * .6, h, h * .45, math.degrees(a)), fill=RED if i % 2 else SAF, outline=INK)

def drawsk(fr, key, t, t0, dur, tipnib=False):
    tip = sk(key).draw(fr.d, prog(t, t0, dur))
    if tipnib and prog(t, t0, dur) < 1: nib(fr.d, tip, t)

def scene(fr, t, R):
    compose(fr, t, R, draw, trans="ink", TR=.42, same=lambda a, b: {"cta": "hook", "loop": "hook"}.get(a, a) == {"cta": "hook", "loop": "hook"}.get(b, b))

def draw(fr, tag, t, L, R):
    fr.img = BGI.copy(); fr.d = ImageDraw.Draw(fr.img); t0 = L.t0; D = min(2.2, (L.t1 - t0) * .75)
    if tag in ("hook", "cta", "loop"):
        h0 = R.T("hook") if tag == "hook" else t0 - 2
        write(fr, t, h0, "काशी का कोतवाल कौन?", (540, 400), HF(92, "y"), RED, dur=.7)
        k = prog(t, h0 + .15, .4)
        if k > 0: glow(fr, 540, 640, 300 * k, (240, 170, 60), 120)
        sk("qmark").draw(fr.d, prog(t, h0 + .2, .7))
        for i, x in enumerate((200, 370, 710, 880)):     # diyas
            if t < h0 + .5 + i * .15: continue
            y = 960; fr.d.chord((x - 46, y - 24, x + 46, y + 34), 0, 180, fill=RED, outline=INK, width=4)
            fr.d.polygon(leaf(x, y - 40, 54 * (1 + .15 * math.sin(t * 14 + i)), 24, 90), fill=SAF, outline=INK)
    elif tag == "debate":
        drawsk(fr, "brahma", t, t0, D * .8, True); drawsk(fr, "vishnu", t, t0 + .4, D * .8)
        for i, (x, s_) in enumerate(((300, "मैं बड़ा!"), (790, "नहीं, मैं!"))):
            tt = t0 + D * .55 + i * .5
            if t > tt:
                k = eback(prog(t, tt, .3)); bx = (x - 150 * k, 300 + 80, x + 150 * k, 300 + 170)
                fr.d.rounded_rectangle(bx, 30, fill=CREAM, outline=INK, width=5)
                if k > .8: fr.text((x, 425), s_, HF(56, "b"), RED, anchor="mm")
    elif tag == "pillar":
        sk("brahma").draw(fr.d, 1); sk("vishnu").draw(fr.d, 1)
        k = prog(t, t0, D)
        if k > .3: glow(fr, 540, 700, 420 * k, (255, 200, 80), 140)
        drawsk(fr, "pillar", t, t0, D)
        write(fr, t, t0 + D * .6, "अनंत ज्योति-स्तंभ", (540, 1010), HF(64, "y"), INK, dur=.8, stroke=6)
    elif tag == "ego":
        sk("brahma_big").draw(fr.d, 1 if t > t0 + .5 else prog(t, t0, .5))
        hx, hy = 540, 720 - 230 * 1.05
        glow(fr, hx, hy, 160 * (1 + .1 * math.sin(t * 8)), (230, 60, 30), 150)
        flames(fr.d, hx, hy - 40, t, 9, 90)
        sk("brahma_big").draw(fr.d, 1) if False else None
        write(fr, t, t0 + D * .4, "अहंकार", (540, 1010), HF(84, "y"), RED, dur=.6, stroke=6)
    elif tag == "bhairav":
        k = prog(t, t0, D)
        glow(fr, 540, 680, 380 * k, (230, 90, 30), 120)
        drawsk(fr, "bhairav", t, t0, D, True)
        write(fr, t, t0 + D * .7, "काल भैरव", (540, 1010), HF(96, "y"), RED, dur=.6, stroke=6)
    elif tag == "cut":
        sk("bhairav_s").draw(fr.d, 1)
        k = prog(t, t0, .25)
        if 0 < k < 1 or t < t0 + .5:
            fr.d.line((180, 420, 180 + 720 * eout(k), 420 + 520 * eout(k)), fill=(255, 245, 200), width=int(26 * (1 - prog(t, t0 + .25, .3)) + 1))
        hk = prog(t, t0 + .6, .6); hx, hy = lerp(760, 300, eout(hk)), lerp(420, 860, eout(hk))
        s2 = Sketch(seed=3); small_head(s2, hx, hy, .5); s2.draw(fr.d, 1)
        if hk >= 1:
            for i in range(3): fr.d.line((hx + 70 + i * 22, hy - 60 + i * 8, hx + 95 + i * 22, hy - 95 + i * 8), fill=RED, width=8)
            write(fr, t, t0 + 1.3, "हाथ से चिपक गया!", (620, 1010), HF(62, "y"), RED, dur=.7, stroke=6)
    elif tag == "wander":
        pts = bez((160, 980), (300, 380), (760, 380), (880, 980), 60)
        for i in range(0, len(pts) - 1, 2): fr.d.line((pts[i], pts[i + 1]), fill=INK, width=6)
        for i, (lbl, (x, y), kind) in enumerate((("पर्वत", (200, 760), "m"), ("वन", (540, 470), "f"), ("सागर", (840, 760), "s"))):
            if t < t0 + i * .4: continue
            circ(fr.d, x, y, 105, CREAM, INK, 5)
            if kind == "m": fr.d.polygon([(x - 80, y + 50), (x - 20, y - 60), (x + 10, y), (x + 40, y - 40), (x + 85, y + 50)], fill=GRN, outline=INK)
            if kind == "f":
                for dx in (-45, 0, 45): fr.d.polygon(leaf(x + dx, y - 10, 90, 44, 90), fill=GRN, outline=INK); fr.d.line((x + dx, y + 30, x + dx, y + 70), fill=INK, width=6)
            if kind == "s":
                for r_ in range(3): fr.d.line([(x - 80 + j * 10, y - 30 + r_ * 30 + 8 * math.sin(j / 1.5 + t * 3)) for j in range(17)], fill=IND, width=6)
            fr.text((x, y + 150), lbl, HF(52, "b"), INK, anchor="mm")
        k = prog(t, t0 + .2, (L.t1 - t0) * .9); i = int(k * (len(pts) - 1)); x, y = pts[i]
        circ(fr.d, x, y - 30, 26, DIND, INK, 4); fr.d.polygon([(x - 26, y - 6), (x + 26, y - 6), (x + 36, y + 60), (x - 36, y + 60)], fill=RED, outline=INK)
        circ(fr.d, x + 48, y + 10, 16, SKIN, INK, 3)
    elif tag in ("kashi", "kapal"):
        if tag == "kashi": drawsk(fr, "kashi", t, t0, D * .6)
        else: sk("kashi").draw(fr.d, 1)
        land = t0 + (L.t1 - t0) * .62 if tag == "kashi" else t0 - 5
        if tag == "kashi":
            k = prog(t, t0 + .3, land - t0 - .3); hy = lerp(380, 940, k * k)
            if t > land: hy = 940 - 30 * abs(math.sin((t - land) * 9)) * max(0, 1 - (t - land) * 2.5)
            s2 = Sketch(seed=3); small_head(s2, 540, hy, .5); s2.draw(fr.d, 1)
        if t > land:
            a = t - land; rr_ = 80 + 240 * min(1, a / .4)
            for i in range(16):
                ang = i / 16 * 2 * math.pi; fr.d.line((540 + math.cos(ang) * rr_ * .55, 940 + math.sin(ang) * rr_ * .55, 540 + math.cos(ang) * rr_, 940 + math.sin(ang) * rr_), fill=GOLD, width=7)
        if tag == "kapal":
            for i, x in enumerate((180, 400, 660, 880)):
                y = 1040 + 6 * math.sin(t * 2 + i); fr.d.chord((x - 26, y - 14, x + 26, y + 18), 0, 180, fill=RED, outline=INK)
                fr.d.polygon(leaf(x, y - 26, 30 * (1 + .15 * math.sin(t * 15 + i)), 14, 90), fill=SAF, outline=INK)
            fr.d.rounded_rectangle((150, 330, 930, 470), 30, fill=RED, outline=INK, width=6)
            write(fr, t, t0 + .2, "कपाल मोचन तीर्थ", (540, 400), HF(84, "y"), CREAM, dur=1.0)
    elif tag == "kotwal":
        sk("kashi").draw(fr.d, 1)
        ov = Image.new("RGBA", (W, H), CREAM + (170,)); fr.img = Image.alpha_composite(fr.img.convert("RGBA"), ov).convert("RGB"); fr.d = ImageDraw.Draw(fr.img)
        drawsk(fr, "bhairav", t, t0, D, True)
        p = (t - t0) / max(.1, L.t1 - t0)
        if p > .5:
            fr.d.rounded_rectangle((130, 930, 870, 1040), 30, fill=RED, outline=INK, width=6)
            write(fr, t, t0 + (L.t1 - t0) * .5, "काशी के कोतवाल", (500, 982), HF(76, "y"), CREAM, dur=.9)
    elif tag == "dog":
        drawsk(fr, "dog", t, t0, D * .8, True)
        p = (t - t0) / max(.1, L.t1 - t0)
        if p > .38:
            k = eback(prog(t, t0 + (L.t1 - t0) * .38, .35))
            box = (520, 430, 980, 430 + 470 * k)
            fr.d.rounded_rectangle(box, 26, fill=CREAM, outline=INK, width=6)
            fr.d.rectangle((520, 430, 980, 500), fill=RED, outline=INK, width=6)
            if k > .9:
                fr.text((750, 466), "काल भैरव जयंती", HF(50, "b"), CREAM, anchor="mm")
                fr.text((750, 600), "मंगलवार", HF(70, "y"), INK, anchor="mm")
                fr.text((750, 720), "1 दिसंबर", HF(88, "y"), RED, anchor="mm")
                fr.text((750, 830), "2026", HF(56, "b"), INK, anchor="mm")

def build(out):
    A.STYLES["katha"] = dict(bpm=74, prog=[50, 50, 48, 50], q=[0, 7, 12, 15], lead="pluck", drums="soft")
    R = Reel(NAME, "katha", LN.KATHA, tone="warm", seed=3)
    R.cap_style.update(fg=CREAM, hi=GOLDL, bg=(43, 27, 18, 230), fontfile=HFP("b"), size=56, lh=70, maxchars=26)
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="बनारस वाले दोस्त को भेजो", icon="send", at=round(dur * .38, 2), bg=RED, fg=CREAM, fontfile=HFP("b"))
    R.cta = dict(at=R.T("cta"), icon="send", head="ये कहानी भेजो", body="बनारस वाले दोस्त को…\nऔर पूछो: काशी का\nकोतवाल कौन?", bg=CREAM, acc=RED, fg=INK,
                 fontfile=HFP("b"), until=R.T("loop") - .05)
    stills = sorted([.4, 1.2] + [R.T(x) + .9 for x in ["debate", "pillar", "ego", "bhairav", "cut", "wander", "kashi", "kapal", "kotwal", "dog", "cta", "loop"]]
                    + [R.line("bhairav").t1 - .2, R.line("kashi").t1 - .2, R.line("dog").t1 - .2, R.nudge["at"] + 1.0, dur - .2])
    return R, R.render(scene, out, stills=stills)

PREVIEW_STYLE = dict(fg=CREAM, hi=GOLDL, bg=(43, 27, 18, 230), fontfile=HFP("b"), size=56, lh=70, maxchars=26)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/out48"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", len(R.violations), R.violations[:15])
