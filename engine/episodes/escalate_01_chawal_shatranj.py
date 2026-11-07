"""Escalation 01 · 'शतरंज और चावल' — one grain on square 1, doubled every square. Exponential climb format.
Facts checked 7 Nov 2026: total grains 2^64-1 = 18,446,744,073,709,551,615; a grain weighs ~20-30 mg (we use 25 mg);
India rice 2024-25 = 149.07 million t (3rd advance estimate); world rice 2025/26 ~556 million t milled (FAO);
square 53 is the first where the running total beats India's year (robust for 20-30 mg), square 55 beats the world's year;
total ~461 billion t ~ 830 years of world harvest at 25 mg. Ambalappuzha legend: king pays the debt by serving paal payasam
(told as legend, deity not depicted)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from diwali_common import *
from drawon import Sketch, ellipse_pts, bez

V = "hf_alpha"; GOLD = (246, 196, 80); CREAM = (255, 244, 220); LINE = (150, 210, 255); RICE = (250, 240, 214)
MG = 25e-3  # grams per grain

def indian(n):
    s = str(int(n))
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]; parts = []
    while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ",".join(parts) + "," + tail

def weight(n_sq):
    g = (2 ** n_sq - 1) * MG
    if g < 1000: return f"≈ {g:.0f} ग्राम" if g >= 1 else "≈ 0.025 ग्राम"
    kg = g / 1000
    if kg < 1000: return f"≈ {kg:.1f} किलो" if kg < 10 else f"≈ {kg:.0f} किलो"
    t = kg / 1000
    if t < 1e5: return f"≈ {indian(round(t))} टन"
    if t < 1e7: return f"≈ {t / 1e5:.1f} लाख टन"
    if t < 1e9: return f"≈ {t / 1e7:.1f} करोड़ टन"
    return f"≈ {t / 1e9:.0f} अरब टन"

LINES = [
    HL(V, "शतरंज के पहले खाने पर एक दाना, फिर हर खाने पर दोगुना। चौंसठवें तक, कितना चावल?", tag="hook", sfx="whoosh", gap=.15),
    HL(V, "दसवाँ खाना। कुल हज़ार दाने, बस दो चम्मच।", tag="s10", sfx="tick", gap=.15),
    HL(V, "बीसवाँ। दस लाख दाने, एक पूरी बोरी।", tag="s20", sfx="tick", gap=.15),
    HL(V, "तीसवाँ। एक भरा हुआ ट्रक।", tag="s30", sfx="tick", gap=.15),
    HL(V, "चालीसवाँ। एक पूरा मालवाहक जहाज़।", tag="s40", sfx="whoosh", gap=.15),
    HL(V, "तिरपनवाँ। भारत की पूरे साल की फ़सल से भी ज़्यादा।", tag="s53", sfx="hit", gap=.15),
    HL(V, "पचपनवाँ। पूरी दुनिया की, साल भर की फ़सल।", tag="s55", sfx="hit", gap=.15),
    HL(V, "और चौंसठवाँ? चार सौ अरब टन से ज़्यादा। यानी दुनिया की, लगभग आठ सौ साल की फ़सल।", tag="s64", sfx="hit", drop=True, gap=.2),
    HL(V, "कहते हैं, केरल के अंबलप्पुझा का राजा ये कर्ज़ चुका नहीं पाया, इसलिए वहाँ आज भी पाल पायसम बँटता है।", tag="legend", sfx="chime", gap=.2),
    HL(V, "ये रील उस दोस्त को भेजो, जो कहता है, बस एक दाना ही तो है।", tag="cta", sfx="pop", gap=.3),
]
STEPS = {"s10": 10, "s20": 20, "s30": 30, "s40": 40, "s53": 53, "s55": 55, "s64": 64}

# ---------- comparison icons (drawn stroke by stroke) ----------
IX, IG = 720, 1000   # icon centre x, ground y
def spoon():
    s = Sketch(seed=1); s.shape(ellipse_pts(IX - 50, IG - 70, 48, 30), None, LINE, 5); s.line([(IX - 2, IG - 76), (IX + 120, IG - 110)], LINE, 9); return s
def sack():
    s = Sketch(seed=2); body = bez((IX - 90, IG), (IX - 120, IG - 120), (IX - 70, IG - 200), (IX - 30, IG - 210), 14) + [(IX + 30, IG - 210)] + bez((IX + 30, IG - 210), (IX + 70, IG - 200), (IX + 120, IG - 120), (IX + 90, IG), 14)
    s.line(body + [(IX - 90, IG)], LINE, 6); s.line([(IX - 34, IG - 214), (IX + 34, IG - 214)], LINE, 8)
    s.line([(IX - 40, IG - 120), (IX + 40, IG - 120)], LINE, 3); s.line([(IX - 40, IG - 95), (IX + 40, IG - 95)], LINE, 3); return s
def truck():
    s = Sketch(seed=3); s.rect(IX - 170, IG - 170, IX + 60, IG - 40, LINE, 6); s.line([(IX + 60, IG - 120), (IX + 120, IG - 120), (IX + 160, IG - 80), (IX + 160, IG - 40), (IX + 60, IG - 40)], LINE, 6)
    for x in (IX - 120, IX - 40, IX + 110): s.line(ellipse_pts(x, IG - 26, 24, 24), LINE, 6)
    return s
def ship():
    s = Sketch(seed=4); s.line([(IX - 200, IG - 90), (IX + 200, IG - 90), (IX + 160, IG - 10), (IX - 170, IG - 10), (IX - 200, IG - 90)], LINE, 6)
    for i in range(5):
        for j in range(2): s.rect(IX - 160 + i * 56, IG - 140 - j * 48, IX - 112 + i * 56, IG - 96 - j * 48, LINE, 4)
    s.rect(IX + 130, IG - 190, IX + 175, IG - 90, LINE, 5); return s
def godown():
    s = Sketch(seed=5); s.line([(IX - 170, IG), (IX - 170, IG - 150), (IX, IG - 230), (IX + 170, IG - 150), (IX + 170, IG)], LINE, 6)
    s.rect(IX - 50, IG - 110, IX + 50, IG, LINE, 5)
    for i in range(3): s.line(ellipse_pts(IX - 120 + i * 30, IG - 22, 16, 20), LINE, 3)
    return s
def globe():
    s = Sketch(seed=6); r = 108; cy = IG - 118; s.line(ellipse_pts(IX, cy, r, r), LINE, 6)
    for k in (.35, .7): s.line(ellipse_pts(IX, cy, r * k, r), LINE, 3)
    for dy in (-60, 0, 60): w = math.sqrt(r * r - dy * dy); s.line([(IX - w, cy + dy), (IX + w, cy + dy)], LINE, 3)
    return s
def hourglass():
    s = Sketch(seed=7); s.line([(IX - 90, IG - 228), (IX + 90, IG - 228)], LINE, 8); s.line([(IX - 90, IG), (IX + 90, IG)], LINE, 8)
    s.line([(IX - 70, IG - 223), (IX + 70, IG - 223), (IX + 8, IG - 115), (IX + 70, IG - 5), (IX - 70, IG - 5), (IX - 8, IG - 115), (IX - 70, IG - 223)], LINE, 6)
    return s
def bowl():
    s = Sketch(seed=8); s.line(ellipse_pts(IX, IG - 120, 140, 90, 0, 180, 24) + [(IX - 140, IG - 120)], GOLD, 6); s.line(ellipse_pts(IX, IG - 120, 140, 22), GOLD, 5)
    for i in range(3): x = IX - 50 + i * 50; s.line(bez((x, IG - 150), (x - 20, IG - 190), (x + 20, IG - 220), (x, IG - 260), 12), (230, 230, 240), 4)
    return s
ICONS = {"s10": (spoon(), "दो चम्मच", 25), "s20": (sack(), "एक बोरी (25 किलो)", 25e3), "s30": (truck(), "भरा ट्रक (~25 टन)", 25e6),
         "s40": (ship(), "मालवाहक जहाज़", 27e9), "s53": (godown(), "भारत की 1 साल की फ़सल", 149e12), "s55": (globe(), "दुनिया की 1 साल की फ़सल", 556e12),
         "s64": (hourglass(), "~800 साल की फ़सल", 556e12 * 800), "legend": (bowl(), "पाल पायसम", None)}

ICON_H = {"s10": 70, "s20": 210, "s30": 170, "s40": 190, "s53": 230, "s55": 226, "s64": 228}
BG = night_bg((8, 12, 36), (28, 18, 52), seed=31)
def board(d, x0, y0, n, t, cell=36):
    for k in range(64):
        r, c = divmod(k, 8); x = x0 + c * cell; y = y0 + (7 - r) * cell
        base = (60, 50, 70) if (r + c) % 2 else (90, 80, 100)
        if k < n:
            base = GOLD if k < n - 1 else tuple(int(v) for v in (255, 230 + 25 * (math.sin(t * 12) * .5 + .5), 150))
        d.rectangle((x, y, x + cell - 2, y + cell - 2), fill=base)
    d.rectangle((x0 - 6, y0 - 6, x0 + 8 * cell + 4, y0 + 8 * cell + 4), outline=CREAM, width=3)

def sq_at(t, R):
    h = R.line("hook")
    if t < R.T("s10"):                                         # hook: 1, 2, 4, 8 ... doubling slowly
        return min(6, 1 + int(max(0, t - .25) / .55))
    prev, cur, t0 = 6, 6, 0
    for tag, n in STEPS.items():
        if t >= R.T(tag): prev, cur, t0 = cur, n, R.T(tag)
    k = eout(min(1, (t - t0) / .9))
    return int(round(prev + (cur - prev) * k))

def cur_tag(t, R):
    tag = "hook"
    for g in list(STEPS) + ["legend", "cta"]:
        if t >= R.T(g): tag = g
    return tag

def pile(d, x, ground, h, t):
    w = h * 1.7; pts = ellipse_pts(x, ground, w / 2, h, 180, 360, 36)
    d.polygon(pts, fill=(236, 214, 160)); d.line(pts, fill=(255, 240, 200), width=3)
    r = (int(h) * 7) % 97
    for i in range(int(min(60, h / 3))):
        a = ((i * 37 + r) % 100) / 100 * math.pi; rr = ((i * 53) % 100) / 100 * .9
        px = x + math.cos(a) * w / 2 * rr; py = ground - math.sin(a) * h * rr
        d.ellipse((px - 4, py - 2, px + 4, py + 2), fill=RICE)

def scene(fr, t, R):
    fr.img = BG.copy(); fr.d = d = ImageDraw.Draw(fr.img)
    tag = cur_tag(t, R); n = sq_at(t, R)
    fr.text((90, 284), "हर खाने पर दोगुने दाने", HF(50), GOLD)
    board(d, 96, 372, n, t)
    fr.text((420, 362), "खाना", HF(40, "SemiBold"), (200, 190, 220))
    f = F("black", 130); fr.text((420, 400), str(n), f, CREAM); x2 = 420 + d.textlength(str(n), font=f) + 10
    fr.text((x2, 470), "/ 64", F("black", 52), (170, 160, 190))
    fr.text((420, 548), "कुल दाने", HF(36, "SemiBold"), (200, 190, 220))
    num = indian(2 ** n - 1); size = 56
    while size > 26 and d.textlength(num, font=F("black", size)) > 560: size -= 2
    fr.text((420, 586), num, F("black", size), GOLD)
    fr.text((420, 652), weight(n), HF(44), CREAM)
    d.line((90, IG, 990, IG), fill=(120, 110, 150), width=3)
    if tag in ICONS:
        sk, label, ref_g = ICONS[tag]; t0 = R.T(tag)
        sk.draw(d, min(1, (t - t0) / .7))
        if t - t0 > .45: fr.text((IX, 716), label, HF(42), LINE if tag != "legend" else GOLD, anchor="ma")
        if ref_g:
            g = (2 ** n - 1) * MG; ratio = g / ref_g
            h = ICON_H[tag] * max(.08, min(1.6, ratio ** (1 / 3)))
            if tag == "s64": h = min(300, 230 * max(1, (t - t0) / .9) ** 1.4)
            pile(d, 310, IG, h, t)
            if ratio > 1.3 and t - t0 > .9: fr.text((310, IG - h - 70), "ज़्यादा!", HF(44), (255, 120, 90), anchor="ma")
    elif tag == "hook":
        k = min(n, 6); cnt = 2 ** (k - 1)
        for i in range(cnt):                                     # the grains on the current square
            x = 300 + (i % 8) * 40 - min(cnt, 8) * 20; y = IG - 40 - (i // 8) * 26
            d.ellipse((x - 12, y - 6, x + 12, y + 6), fill=RICE)
        fr.text((IX, 770), "1 → 2 → 4 → 8 → …", F("black", 56), LINE, anchor="ma")
        fr.text((IX, 840), "64 खाने बाद?", HF(56), GOLD, anchor="ma")
    if tag == "s64" and t - R.T("s64") < .35:                   # small shake when the total lands
        a = (t - R.T("s64")) * 60; fr.img = fr.img.transform(fr.img.size, Image.AFFINE, (1, 0, math.sin(a) * 8, 0, 1, 0)); fr.d = ImageDraw.Draw(fr.img)

if __name__ == "__main__":
    out = sys.argv[1]
    for L in LINES: L.speed = round(L.speed * 1.1, 3)
    nudge = dict(text="दोस्त को भेजो", icon="send", bg=GOLD, fg=(30, 20, 10), fontfile=f"{FONTS}/Hind-Bold.ttf")
    cta = dict(icon="send", head="भेजो!", body="उस दोस्त को जो कहता है,\n'बस एक दाना ही तो है'", bg=(255, 248, 232), acc=(160, 90, 20), fg=(30, 20, 10),
               fontfile=f"{FONTS}/Hind-Bold.ttf")
    R, p = build("Escalate_01_ChawalShatranj", LINES, scene, out, music="space", nudge=nudge, cta=cta, seed=101, cap_bg=(10, 10, 30, 220))
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
