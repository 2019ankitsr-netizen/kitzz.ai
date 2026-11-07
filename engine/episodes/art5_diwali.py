"""Diwali Did You Know · Art 01 · 'एक दीया, पाँच कलाएँ' — one diya drawn stroke by stroke in five Indian art styles
(Madhubani, Warli, Pattachitra, Mughal miniature, Kalamkari), each with one verified fact. All art is drawn in code.
Facts checked 7 Nov 2026: Madhubani leaves no empty space; Warli uses circle/triangle/square in white rice paste;
Pattachitra white is powdered conch shell; Mughal miniature brushes of squirrel-tail hair; Kalamkari = kalam (pen),
cloth soaked in buffalo milk (with myrobalan) so the natural dyes don't spread."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from diwali_common import *
from drawon import Sketch, ellipse_pts, bez, leaf, offset

V = "hf_alpha"; GOLD = (236, 190, 80)
CW, CH = 900, 640                     # local canvas size
AX, AY = 90, 400                      # canvas position in frame (ends y 1040, captions start 1060)
BLK = (25, 18, 15)

def paper(col, noise=10, seed=1, weave=False):
    r = np.random.default_rng(seed)
    a = np.clip(np.array(col)[None, None, :] + r.normal(0, noise, (CH, CW, 1)), 0, 255).astype(np.uint8)
    im = Image.fromarray(a).convert("RGBA")
    if weave:
        d = ImageDraw.Draw(im)
        for x in range(0, CW, 6): d.line((x, 0, x, CH), fill=tuple(max(0, c - 8) for c in col) + (255,))
        for y in range(0, CH, 6): d.line((0, y, CW, y), fill=tuple(max(0, c - 6) for c in col) + (255,))
    return im

def teardrop(cx, base, top, wdt):
    l = bez((cx, base), (cx - wdt, base - 10), (cx - wdt * .55, top + (base - top) * .35), (cx, top), 16)
    r = bez((cx, top), (cx + wdt * .55, top + (base - top) * .35), (cx + wdt, base - 10), (cx, base), 16)
    return l + r[1:]

def bowl(cx, cy, rx, depth): return ellipse_pts(cx, cy, rx, depth, 0, 180, 30)

# ---------------- 1 · Madhubani ----------------
def madhubani():
    bg = paper((242, 224, 184), 7, 11)
    s = Sketch(wobble=1.2, seed=3); RED, YEL, GRN, BLU, ORG = (196, 40, 32), (240, 186, 40), (52, 132, 62), (40, 86, 160), (232, 120, 30)
    b = bowl(450, 440, 125, 92); s.shape(b + [(325, 440)], RED, BLK, 5); s.line(offset(b, 450, 440, .86), BLK, 2)
    s.shape(ellipse_pts(450, 440, 125, 20), YEL, BLK, 4)
    for j in range(7): s.dot(370 + j * 27, 478 + 12 * math.sin(j / 6 * math.pi), 6, YEL)
    fl = teardrop(450, 424, 290, 46); s.shape(fl, YEL, BLK, 4); s.shape(teardrop(450, 420, 340, 22), ORG, None)
    s.rect(14, 14, CW - 14, CH - 14, BLK, 5); s.rect(42, 42, CW - 42, CH - 42, BLK, 3)
    zz = []
    for i in range(0, 29): zz.append((14 + 14 + i * 30.5, 22 if i % 2 else 36))
    s.line(zz, RED, 3); s.line([(x, CH - y) for x, y in zz], RED, 3)
    s.shape(ellipse_pts(450, 130, 52, 52), YEL, BLK, 4); s.line(ellipse_pts(450, 130, 40, 40), BLK, 2)
    for i in range(12):
        a = i * math.pi / 6; s.line([(450 + 64 * math.cos(a), 130 + 64 * math.sin(a)), (450 + 86 * math.cos(a), 130 + 86 * math.sin(a))], RED, 4)
    for fx, dirn in ((190, 1), (710, -1)):                               # two fish (Madhubani auspicious motif)
        body = ellipse_pts(fx, 330, 78, 34, 0, 360, 36)
        s.shape(body, ORG, BLK, 4); s.line(offset(body, fx, 330, .78), BLK, 2)
        tail = [(fx - dirn * 70, 330), (fx - dirn * 118, 296), (fx - dirn * 118, 364)]
        s.shape(tail, RED, BLK, 4)
        for j in range(3): s.line(ellipse_pts(fx - dirn * (10 - j * 22), 330, 14, 22, 270 if dirn > 0 else 90, 450 if dirn > 0 else 270, 10), BLK, 2)
        s.dot(fx + dirn * 50, 322, 7, BLK)
    extra = Sketch(wobble=1.0, seed=5)
    spots = [(120, 120), (780, 120), (280, 130), (620, 130), (110, 470), (790, 470), (250, 520), (650, 520),
             (180, 210), (720, 210), (330, 250), (570, 250), (450, 590), (110, 570), (790, 570), (310, 590), (590, 590)]
    for i, (x, y) in enumerate(spots):
        c = [(220, 60, 90), GRN, BLU, RED][i % 4]
        for k in range(6):
            a = k * math.pi / 3; extra.shape(leaf(x + 15 * math.cos(a), y + 15 * math.sin(a), 22, 12, math.degrees(a)), c, BLK, 2, cost=10)
        extra.dot(x, y, 7, YEL, 6)
    return dict(name="मधुबनी", place="बिहार", bg=bg, main=s, extra=extra, flame=(450, 380), tool=(120, 70, 40), chip="ख़ाली जगह: ज़ीरो", acc=RED)

# ---------------- 2 · Warli ----------------
def warli():
    bg = paper((150, 72, 46), 9, 12); WH = (246, 238, 222)
    s = Sketch(wobble=.8, seed=7)
    s.shape([(370, 440), (530, 440), (450, 505)], WH, None)
    s.shape([(430, 432), (470, 432), (450, 350)], WH, None)
    s.dot(450, 343, 10, WH)
    s.rect(310, 250, 590, 520, WH, 4)                                           # chauk (square)
    for i in range(9):
        x = 322 + i * 31; s.line([(x, 250), (x + 15, 236), (x + 30, 250)], WH, 2)
    s.line(ellipse_pts(130, 110, 46, 46), WH, 4)
    for i in range(16):
        a = i * math.pi / 8; s.dot(130 + 66 * math.cos(a), 110 + 66 * math.sin(a), 4, WH, 4)
    for x0 in range(30, 900, 110): s.line([(x0, 625), (x0 + 55, 545), (x0 + 110, 625)], WH, 3)
    for tx in (60, 840):
        for j in range(3): s.line([(tx - 28 + j * 4, 470 - j * 34), (tx, 420 - j * 34), (tx + 28 - j * 4, 470 - j * 34)], WH, 3, closed=True)
        s.line([(tx, 470), (tx, 520)], WH, 3)
    return dict(name="वारली", place="महाराष्ट्र", bg=bg, main=s, extra=Sketch(), flame=(450, 380), tool=(200, 160, 110), chip="गोला · त्रिकोण · चौकोर",
                acc=(150, 72, 46), dancers=True)

def warli_dancers(d, t, k):
    WH = (246, 238, 222); n = 11; shown = int(round(k * n))
    for i in range(shown):
        a = t * .55 + i * 2 * math.pi / n; x = 450 + 300 * math.cos(a); y = 395 + 150 * math.sin(a)
        if 265 < y < 520 and 300 < x < 600: continue                            # pass behind the chauk
        sc = .8 + .25 * (math.sin(a) + 1) / 2; step = math.sin(t * 7 + i) * 4
        d.ellipse((x - 7 * sc, y - 48 * sc, x + 7 * sc, y - 34 * sc), fill=WH)
        d.polygon([(x - 13 * sc, y - 32 * sc), (x + 13 * sc, y - 32 * sc), (x, y - 12 * sc)], fill=WH)
        d.polygon([(x, y - 12 * sc), (x - 12 * sc, y + 6 * sc), (x + 12 * sc, y + 6 * sc)], fill=WH)
        d.line((x - 6 * sc, y + 6 * sc, x - 10 * sc - step, y + 26 * sc), fill=WH, width=3)
        d.line((x + 6 * sc, y + 6 * sc, x + 10 * sc + step, y + 26 * sc), fill=WH, width=3)
        a2 = a + 2 * math.pi / n; x2 = 450 + 300 * math.cos(a2); y2 = 395 + 150 * math.sin(a2)
        if i + 1 < shown and not (265 < y2 < 520 and 300 < x2 < 600): d.line((x + 10 * sc, y - 26 * sc, x2 - 10 * sc, y2 - 26 * sc), fill=WH, width=2)

# ---------------- 3 · Pattachitra ----------------
def pattachitra():
    RED, YEL, BLKk, GRN, PNK, WHT = (168, 32, 26), (232, 182, 40), (20, 14, 12), (36, 116, 60), (232, 120, 136), (252, 246, 236)
    bg = paper(RED, 6, 13)
    s = Sketch(wobble=.6, seed=9)
    s.fill([(10, 10), (CW - 10, 10), (CW - 10, CH - 10), (10, CH - 10)], YEL, 30)
    s.fill([(52, 52), (CW - 52, 52), (CW - 52, CH - 52), (52, CH - 52)], RED, 30)
    b = bowl(450, 430, 118, 80); s.shape(b + [(332, 430)], YEL, BLKk, 7); s.shape(ellipse_pts(450, 430, 118, 20), (120, 20, 20), BLKk, 6)
    fl = teardrop(450, 414, 280, 48); s.shape(fl, (240, 120, 30), BLKk, 6); s.shape(teardrop(450, 410, 330, 24), YEL, None)
    s.rect(10, 10, CW - 10, CH - 10, BLKk, 7); s.rect(52, 52, CW - 52, CH - 52, BLKk, 6)
    for x in range(40, CW - 30, 44):
        s.shape(leaf(x, 31, 30, 14, 0), BLKk, None, cost=6); s.shape(leaf(x, CH - 31, 30, 14, 0), BLKk, None, cost=6)
    for y in range(80, CH - 60, 44):
        s.shape(leaf(31, y, 30, 14, 90), BLKk, None, cost=6); s.shape(leaf(CW - 31, y, 30, 14, 90), BLKk, None, cost=6)
    for i, a in enumerate(range(-80, 81, 32)):                                  # lotus
        s.shape(leaf(450 + 70 * math.sin(math.radians(a)), 548 - 40 * math.cos(math.radians(a)), 120, 46, a - 90), PNK if i % 2 else WHT, BLKk, 5)
    for op in [o for o in s.ops[2:8]]: s.ops.append((op[0], op[1], op[2], op[3], 0.0))
    s.shape(leaf(260, 560, 170, 50, 10), GRN, BLKk, 5); s.shape(leaf(640, 560, 170, 50, -10), GRN, BLKk, 5)
    conch = bez((170, 380), (90, 360), (100, 240), (190, 200), 18) + bez((190, 200), (250, 230), (260, 330), (170, 380), 18)[1:]
    s.shape(conch, WHT, BLKk, 6)
    sp = [(185 + 40 * math.exp(-.18 * i) * math.cos(i * .55), 290 + 40 * math.exp(-.18 * i) * math.sin(i * .55)) for i in range(26)]
    s.line(sp, BLKk, 3)
    extra = Sketch(seed=10)
    for x in range(70, CW - 60, 26): extra.dot(x, 64, 5, WHT, 3); extra.dot(x, CH - 64, 5, WHT, 3)
    for j in range(9): extra.dot(355 + j * 24, 468 + 10 * math.sin(j / 8 * math.pi), 6, WHT, 4)
    for j in range(12): extra.dot(700 + 40 * math.cos(j * .52), 220 + 40 * math.sin(j * .52), 6, WHT, 4)
    return dict(name="पट्टचित्र", place="ओडिशा", bg=bg, main=s, extra=extra, flame=(450, 365), tool=(110, 80, 50), chip="सफ़ेद रंग = पिसा हुआ शंख", acc=(168, 32, 26))

# ---------------- 4 · Mughal miniature ----------------
def mughal():
    NAVY, IVORY, GLD, BRN, NIGHT, CYP = (26, 40, 78), (240, 230, 206), (206, 164, 66), (110, 70, 40), (22, 30, 62), (46, 86, 56)
    bg = paper(NAVY, 5, 14)
    s = Sketch(seed=11)
    s.fill([(60, 56), (CW - 60, 56), (CW - 60, CH - 56), (60, CH - 56)], IVORY, 30)
    s.rect(60, 56, CW - 60, CH - 56, GLD, 3); s.rect(70, 66, CW - 70, CH - 66, GLD, 1)
    arch = [(300, 540), (300, 260)] + bez((300, 260), (310, 200), (360, 190), (385, 180), 10)[1:] + bez((385, 180), (410, 150), (450, 140), (450, 120), 10)[1:] \
        + bez((450, 120), (450, 140), (490, 150), (515, 180), 10)[1:] + bez((515, 180), (540, 190), (590, 200), (600, 260), 10)[1:] + [(600, 540)]
    s.shape(arch, NIGHT, BRN, 2); s.line(offset(arch, 450, 360, 1.08), BRN, 1)
    r = random.Random(4)
    for _ in range(22): s.dot(r.uniform(320, 580), r.uniform(170, 420), 2, GLD, 2)
    for cx in (180, 720):
        s.shape(leaf(cx, 380, 300, 70, 90), CYP, (30, 50, 30), 1)
        for j in range(9): s.line([(cx, 250 + j * 28), (cx - 18, 262 + j * 28)], (80, 130, 80), 1); s.line([(cx, 250 + j * 28), (cx + 18, 262 + j * 28)], (80, 130, 80), 1)
        s.line([(cx, 530), (cx, 548)], BRN, 3)
    s.shape([(270, 540), (630, 540), (640, 566), (260, 566)], (204, 156, 112), BRN, 1)
    b = bowl(450, 510, 48, 28); s.shape(b + [(402, 510)], (196, 120, 70), BRN, 1); s.shape(ellipse_pts(450, 510, 48, 7), GLD, BRN, 1)
    for j in range(5): s.dot(422 + j * 14, 524, 2, GLD, 2)
    s.shape(teardrop(450, 504, 450, 16), (255, 200, 90), BRN, 1); s.shape(teardrop(450, 502, 470, 7), (255, 245, 210), None)
    for x in range(90, CW - 80, 22):
        s.line([(x, 600), (x, 588)], (60, 110, 60), 1); s.dot(x, 586, 3, (200, 60, 70) if x % 44 else GLD, 1)
    vine = [(30 + i * 4, 26 + 8 * math.sin(i * .25)) for i in range(211)]
    s.line(vine, GLD, 2); s.line([(x, CH - y) for x, y in vine], GLD, 2)
    for i in range(0, 211, 12):
        x, y = vine[i]; s.shape(leaf(x, y + 10, 12, 6, 60), GLD, None, cost=3); s.shape(leaf(x, CH - y - 10, 12, 6, -60), GLD, None, cost=3)
    return dict(name="मुग़ल मिनिएचर", place="दरबारी कला", bg=bg, main=s, extra=Sketch(), flame=(450, 480), tool=(150, 110, 70), chip="ब्रश = गिलहरी के बाल",
                acc=NAVY, loupe=True, fine=True)

# ---------------- 5 · Kalamkari ----------------
def kalamkari():
    CLOTH, MAD, IND, MUS = (232, 214, 178), (158, 42, 30), (40, 58, 108), (200, 146, 40)
    bg = paper(CLOTH, 5, 15, weave=True)
    outl = Sketch(wobble=.9, seed=13); fills = []
    b = bowl(450, 480, 100, 64); outl.line(b + [(350, 480)], BLK, 4, closed=True); fills.append((b + [(350, 480)], MAD))
    rim = ellipse_pts(450, 480, 100, 16); outl.line(rim, BLK, 3, closed=True); fills.append((rim, IND))
    fl = teardrop(450, 468, 360, 38); outl.line(fl, BLK, 4, closed=True); fills.append((fl, MUS))
    trunk = bez((450, 358), (425, 300), (478, 220), (450, 100), 30)
    outl.line(trunk, BLK, 5)
    cols = [MAD, IND, MUS]
    for i, (y, side) in enumerate([(335, -1), (305, 1), (262, -1), (236, 1), (196, -1), (170, 1), (136, -1), (118, 1)]):
        x0 = 450 + 12 * math.sin(y / 40)
        br = bez((x0, y), (x0 + side * 70, y - 10), (x0 + side * 130, y - 70), (x0 + side * 170, y - 40), 16)
        outl.line(br, BLK, 3)
        lx, ly = br[-1]; lf = leaf(lx + side * 30, ly + 4, 70, 34, side * 15)
        outl.line(lf, BLK, 3, closed=True); fills.append((lf, cols[i % 3]))
        mid = br[len(br) // 2]; lf2 = leaf(mid[0], mid[1] - 26, 46, 22, -side * 50)
        outl.line(lf2, BLK, 2, closed=True); fills.append((lf2, cols[(i + 1) % 3]))
    for a in range(-70, 71, 35):
        p = leaf(450 + 52 * math.sin(math.radians(a)), 572 - 28 * math.cos(math.radians(a)), 80, 32, a - 90)
        outl.line(p, BLK, 3, closed=True); fills.append((p, MAD if a % 70 == 0 else MUS))
    for yb in (24, CH - 70):
        outl.line([(20, yb), (CW - 20, yb)], BLK, 3); outl.line([(20, yb + 46), (CW - 20, yb + 46)], BLK, 3)
        for x in range(30, CW - 40, 46):
            outl.line(ellipse_pts(x + 23, yb + 46, 20, 30, 180, 360, 12), BLK, 2); fills.append((ellipse_pts(x + 23, yb + 46, 14, 22, 180, 360, 10), MAD))
    fills = fills[3:] + fills[:3]
    for pts, c in fills: outl.fill(pts, c, 14)
    for x in range(90, CW - 80, 22): pass
    redo = Sketch(seed=14)
    for kind, g, col, w, cst in outl.ops:
        if kind == "L": redo.ops.append(("L", g, col, w, 0.0))
    return dict(name="कलमकारी", place="आंध्र प्रदेश", bg=bg, main=outl, extra=redo, flame=(450, 420), tool=(170, 130, 70), chip="कलम = पेन", acc=MAD, kalam=True)

STYLES = [madhubani(), warli(), pattachitra(), mughal(), kalamkari()]
TAGS = ["m", "w", "p", "mu", "k"]
for st in STYLES:                                                              # finished canvases (used for caching + end grid)
    im = st["bg"].copy(); d = ImageDraw.Draw(im); st["main"].draw(d, 1); st["extra"].draw(d, 1); st["done"] = im

LINES = [
    HL(V, "क्या आप जानते हैं? एक दीया, पाँच कलाएँ, और पाँच राज़।", tag="hook", sfx="whoosh", gap=.2),
    HL(V, "पहली, बिहार की मधुबनी। इसमें कोई जगह ख़ाली नहीं छोड़ते। हर कोना, फूल-पत्तियों से भरा जाता है।", tag="m", sfx="whoosh", gap=.2),
    HL(V, "दूसरी, वारली। सिर्फ़ तीन आकार, गोला, त्रिकोण, चौकोर। और रंग बस एक, चावल के पेस्ट का सफ़ेद।", tag="w", sfx="whoosh", gap=.2),
    HL(V, "तीसरी, ओडिशा का पट्टचित्र। इसका सफ़ेद रंग, शंख पीसकर बनता है।", tag="p", sfx="whoosh", gap=.2),
    HL(V, "चौथी, मुग़ल मिनिएचर। इतनी बारीक लकीरों का ब्रश, गिलहरी की पूँछ के बालों से बनता था।", tag="mu", sfx="whoosh", gap=.2),
    HL(V, "और पाँचवीं, कलमकारी। कलम, यानी पेन। कपड़ा भैंस के दूध में भिगोते हैं, ताकि रंग न फैले।", tag="k", sfx="whoosh", gap=.2),
    HL(V, "पाँच कलाएँ, एक रोशनी।", tag="end", sfx="chime", drop=True, gap=.2),
    HL(V, "ये रील अपने आर्टिस्ट दोस्त को भेजो, और पूछो, क्या वो जानता है?", tag="cta", sfx="pop", gap=.3),
]

BGN = night_bg((14, 8, 30), (52, 16, 36), seed=21)
WIPE = .45
_cache = {}

def canvas_at(i, t, R):
    st = STYLES[i]; L = R.line(TAGS[i]); a = t - L.t0; dur = L.t1 - L.t0
    pm = eout(min(1, max(0, a / (dur * .45)))); pe = min(1, max(0, (a - dur * .5) / (dur * .38)))
    if pm >= 1 and pe >= 1: im = st["done"].copy(); tip = None
    else:
        key = (i, "main")
        if pm >= 1:
            if key not in _cache:
                b = st["bg"].copy(); st["main"].draw(ImageDraw.Draw(b), 1); _cache[key] = b
            im = _cache[key].copy(); d = ImageDraw.Draw(im); tip = st["extra"].draw(d, pe)
        else:
            im = st["bg"].copy(); d = ImageDraw.Draw(im); tip = st["main"].draw(d, pm)
    d = ImageDraw.Draw(im)
    if st.get("dancers"): warli_dancers(d, t, ease((a - dur * .5) / (dur * .3)))
    if pm >= 1:                                                                  # flame flicker + glow
        fx, fy = st["flame"]; fl = 1 + .15 * math.sin(t * 13 + i) + .08 * math.sin(t * 31)
        paste_glow(im, fx, fy, 70 * fl if not st.get("fine") else 34 * fl, (255, 190, 80, 90))
    if tip and pm < 1 or (tip and pe < 1):                                         # the drawing tool follows the stroke
        x, y = tip; col = st["tool"]
        if st.get("kalam"):
            d.line((x, y, x + 70, y - 120), fill=(150, 110, 60), width=9); d.ellipse((x + 22, y - 52, x + 44, y - 26), fill=(230, 225, 210))
        elif st.get("fine"):
            d.line((x, y, x + 60, y - 130), fill=(140, 40, 30), width=5); d.line((x, y, x + 8, y - 16), fill=(60, 50, 40), width=2)
        else:
            d.line((x, y, x + 58, y - 110), fill=col, width=8); d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=col)
    if st.get("loupe") and a > dur * .45:                                          # magnifier shows how fine the lines are
        k = ease((a - dur * .45) / .5); cx, cy = 700, 470; rr = int(110 * k)
        if rr > 10:
            src = im.crop((450 - 40, 500 - 40, 450 + 40, 500 + 40)).resize((2 * rr, 2 * rr), Image.LANCZOS)
            m = Image.new("L", (2 * rr, 2 * rr), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * rr - 1, 2 * rr - 1), fill=255)
            im.paste(src, (cx - rr, cy - rr), m); d = ImageDraw.Draw(im)
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(206, 164, 66), width=7)
            d.line((cx + rr * .7, cy + rr * .7, cx + rr * 1.2, cy + rr * 1.2), fill=(206, 164, 66), width=12)
            d.line((450 + 40, 500 - 10, cx - rr, cy - 10), fill=(206, 164, 66), width=2)
    return im

def frame_canvas(fr, im, k=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((AX + 10, AY + 16, AX + CW + 10, AY + CH + 16), 30, fill=(0, 0, 0, 120))
    fr.img.alpha_composite(lay)
    m = Image.new("L", (CW, CH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, CW - 1, CH - 1), 30, fill=255)
    if k < 1:
        sc = .82 + .18 * eout(k); w, h = int(CW * sc), int(CH * sc)
        im2 = im.resize((w, h)); m2 = m.resize((w, h)).point(lambda v: int(v * min(1, k * 1.5)))
        fr.img.paste(im2, (AX + (CW - w) // 2, AY + (CH - h) // 2), m2)
    else: fr.img.paste(im, (AX, AY), m)

def wipe(a_im, b_im, k, seed):
    """Ragged diagonal brush wipe from a_im to b_im (k 0..1)."""
    m = Image.new("L", (CW, CH), 0); d = ImageDraw.Draw(m); r = random.Random(seed)
    edge = -300 + (CW + 600) * eout(k); pts = [(-10, -10)]
    for y in range(0, CH + 41, 40): pts.append((edge - y * .35 + r.uniform(-30, 30), y))
    pts += [(-10, CH + 10)]; d.polygon(pts, fill=255)
    return Image.composite(b_im, a_im, m.filter(ImageFilter.GaussianBlur(6)))

def header(fr, i):
    st = STYLES[i]
    fr.text((90, 282), f"{i + 1}/5", FM(34), GOLD)
    fr.text((175, 276), st["name"], YF(70), (255, 240, 220))
    fr.text((990, 300), st["place"], HF(42, "SemiBold"), (230, 190, 150), anchor="ra")

def chip(fr, t, R, i):
    L = R.line(TAGS[i]); dur = L.t1 - L.t0; a = t - (L.t0 + dur * .42)
    if a < 0: return
    k = eback(a / .35); txt = STYLES[i]["chip"]; font = HF(48); d = fr.d
    w = d.textlength(txt, font=font) + 70; cx, y = 520, 958
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((cx - w / 2 * k, y, cx + w / 2 * k, y + 74), 37, fill=GOLD + (245,), outline=(60, 30, 10, 255), width=4)
    fr.img.alpha_composite(lay); fr.d = ImageDraw.Draw(fr.img)
    if k > .8: fr.text((cx, y + 37), txt, font, (40, 20, 10), anchor="mm")

SP = Sparks(17)
def scene(fr, t, R):
    fr.img = BGN.copy(); fr.d = d = ImageDraw.Draw(fr.img)
    starts = [R.T(g) for g in TAGS]; tend = R.T("end")
    if t < starts[0]:                                                         # hook: one diya, five dots
        fr.text((90, 292), "क्या आप जानते हैं?", HF(56), GOLD)
        k = eback(t / .4)
        fr.text((540, 470), "एक दीया", YF(int(130 * max(.3, k))), (255, 236, 200), anchor="mm")
        fr.text((540, 610), "5 कलाएँ · 5 राज़", HF(72), (255, 196, 90), anchor="mm")
        cols = [s["acc"] for s in STYLES]
        for j, c in enumerate(cols):
            on = t > .35 + j * .25; x = 540 + (j - 2) * 110
            d.ellipse((x - 30, 700, x + 30, 760), fill=c if on else (60, 50, 60), outline=(255, 220, 160), width=4)
        paste_glow(fr.img, 540, 905, 120, (255, 170, 60, 120)); d = fr.d = ImageDraw.Draw(fr.img)
        diya(d, 540, 940, 1.5, t)
        SP.step(t, [(540, 870, .5)]); SP.draw(d)
        if t > starts[0] - .35: frame_canvas(fr, canvas_at(0, starts[0], R), (t - (starts[0] - .35)) / .35)
        return
    if t < tend - .2:                                                          # the five styles
        i = max(j for j in range(5) if t >= starts[j] - .001)
        header(fr, i)
        im = canvas_at(i, t, R)
        if i > 0 and t < starts[i] + WIPE:
            im = wipe(canvas_at(i - 1, starts[i] - .01, R), im, (t - starts[i]) / WIPE, i)
        frame_canvas(fr, im); fr.d = ImageDraw.Draw(fr.img)
        chip(fr, t, R, i)
        return
    a = t - (tend - .2)                                                        # end: all five, one light
    fr.text((540, 300), "पाँच कलाएँ · एक रोशनी", HF(64), GOLD, anchor="ma")
    pos = [(80, 400), (390, 400), (700, 400), (235, 690), (545, 690)]
    for j, (x, y) in enumerate(pos):
        k = eback((a - j * .12) / .4)
        if k <= .02: continue
        th = STYLES[j]["done"].resize((300, 213)); w, h = int(300 * k), int(213 * k)
        if w < 4: continue
        paste_glow(fr.img, x + 150, y + 106, 90, (255, 170, 60, 60))
        fr.img.paste(th.resize((w, h)), (x + (300 - w) // 2, y + (213 - h) // 2))
    fr.d = d = ImageDraw.Draw(fr.img)
    for j, (x, y) in enumerate(pos):
        if a > j * .12 + .3: fr.text((x + 150, y + 220), STYLES[j]["name"], HF(34), (255, 236, 200), anchor="ma")

if __name__ == "__main__":
    out = sys.argv[1]
    for L in LINES: L.speed = round(L.speed * 1.1, 3)
    nudge = dict(text="आर्टिस्ट दोस्त को भेजो", icon="send", bg=GOLD, fg=(40, 20, 10), fontfile=f"{FONTS}/Hind-Bold.ttf")
    cta = dict(icon="send", head="भेजो!", body="अपने आर्टिस्ट दोस्त को,\nऔर पूछो, क्या वो जानता है?", bg=(255, 248, 232), acc=(160, 40, 20), fg=(40, 20, 10),
               fontfile=f"{FONTS}/Hind-Bold.ttf")
    R, p = build("DiwaliArt_01_EkDiyaPaanchKalayein", LINES, scene, out, music="festive", nudge=nudge, cta=cta, seed=97, cap_bg=(30, 10, 30, 220),
                 extra_stills=[R_ for R_ in ()])
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
