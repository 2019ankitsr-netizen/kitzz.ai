"""Trending Today · Fan Buzz · Fri 27 Nov 2026 · "Film aayi bhi nahi, ₹65 crore ke ticket BIK GAYE!" — Breaking Board style (Hinglish).
Avengers: Doomsday India advance booking (Sacnilk overall report, updated 27 Nov 2026 2:20 AM IST): ₹65.22 cr gross incl. blocked seats
(₹57.17 cr excl.), 10.36 lakh tickets, avg ticket ₹629; English ₹54.77 cr = 84%, Hindi ₹8.14 cr = 12%; Day 1 (Thu 17 Dec) ₹27.57 cr.
BusinessToday 25 Nov: +₹7.72 cr from 24 to 25 Nov (₹7.72 cr / 86,400 s ≈ ₹893 per second). India release Thu 17 Dec 2026 (9to5Marvel).
Biggest Hollywood opening day in India: Spider-Man: Brand New Day ₹72.50 cr (Sacnilk table, 19 Nov 2026).
No posters, characters, faces or logos: original split-flap board, drawn tickets, popcorn, countdown.
Usage: python3 episodes/trending_20261127_doomsday_advance.py OUT_DIR
"""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFont
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_A", "parler:Rohit:news")

LINES = [
    Line(V, "फ़िल्म आई भी नहीं, और पैंसठ करोड़ के टिकट बिक गए!", "Film aayi bhi nahi… ₹65 crore ke ticket BIK GAYE!", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "एवेंजर्स डूम्सडे, सत्रह दिसंबर को आ रही है। अभी बीस दिन बाकी।", "Avengers: Doomsday · 17 Dec · abhi 20 din baaki", lang="hi", tag="what", sfx="pop"),
    Line(V, "फिर भी, दस लाख से ज़्यादा टिकट, पहले से बुक।", "Phir bhi 10 lakh+ ticket pehle se BOOK", lang="hi", tag="tix", sfx="tick"),
    Line(V, "चौबीस से पच्चीस नवंबर, एक ही दिन में, सात करोड़ सत्तर लाख। यानी हर सेकंड, करीब आठ सौ नब्बे रुपये!",
         "Ek din mein ₹7.7 crore = har SECOND ~₹890!", lang="hi", tag="sec", sfx="hit"),
    Line(V, "मार्वल वाले दोस्त को अभी भेजो।", "Marvel wale dost ko abhi bhejo", lang="hi", tag="nudge", sfx="pop"),
    Line(V, "ट्विस्ट ये, चौरासी परसेंट पैसा, इंग्लिश वर्ज़न का। हिंदी सिर्फ़ बारह परसेंट।", "Twist: 84% English version! Hindi sirf 12%", lang="hi", tag="twist", sfx="hit"),
    Line(V, "एक टिकट, औसतन छह सौ उनतीस रुपये।", "Average ticket: ₹629", lang="hi", tag="avg", sfx="tick"),
    Line(V, "सिर्फ़ पहले दिन के, सत्ताईस करोड़ साठ लाख, अभी से।", "Sirf Day 1: ₹27.6 crore, abhi se", lang="hi", tag="day1", sfx="tick"),
    Line(V, "भारत में हॉलीवुड का ओपनिंग डे रिकॉर्ड, बहत्तर करोड़ पचास लाख। स्पाइडर मैन का।",
         "India mein Hollywood Day 1 record: ₹72.5 cr (Spider-Man)", lang="hi", tag="record", sfx="whoosh"),
    Line(V, "बीस दिन में, ये रिकॉर्ड टूटेगा? कमेंट में बताओ।", "20 din mein record tootega? Comment karo", lang="hi", tag="ask", sfx="pop"),
    Line(V, "उस दोस्त को भेजो, जो कहता है, टिकट बाद में ले लूँगा।", "Us dost ko bhejo jo kehta hai \"ticket baad mein le lunga\"",
         lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "क्योंकि फ़िल्म आई भी नहीं, और...", "Kyunki film aayi bhi nahi… aur", lang="hi", tag="loop", gap=.05),
]

NAVY, PANEL, TILE, INK = (14, 20, 38), (24, 34, 62), (34, 40, 52), (240, 244, 250)
RED, GOLD, GREEN, CYAN, GREY = (230, 45, 50), (255, 200, 40), (40, 190, 110), (90, 200, 255), (150, 160, 180)

def base():
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(18, 26, 48), width=2)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(18, 26, 48), width=2)
    return im
BASE = base()
def blk(s): return F("black", s)
def xb(s): return F("xb", s)

def flap(fr, d, t, t0, text, x, y, cw=78, ch=118, col=INK, size=96, stagger=.05):
    """split-flap tiles: each char rolls through random glyphs then settles"""
    r = random.Random(int(t * 30) + x)
    for i, c in enumerate(text):
        cx = x + i * (cw + 8)
        d.rounded_rectangle((cx, y, cx + cw, y + ch), 10, fill=TILE, outline=(10, 12, 18), width=3)
        d.line((cx + 2, y + ch // 2, cx + cw - 2, y + ch // 2), fill=(10, 12, 18), width=3)
        settle = t0 + .12 + i * stagger
        g = c if (t >= settle or c == " ") else r.choice("0123456789₹")
        if t >= t0: fr.text((cx + cw / 2, y + ch / 2 + 2), g, blk(size), col if t >= settle else GREY, anchor="mm")

def ticket(d, x, y, w, h, col, k=1.0):
    if k <= 0: return
    h2 = h * min(1, k)
    d.rounded_rectangle((x, y, x + w, y + h2), 14, fill=col, outline=(10, 12, 18), width=4)
    if k >= 1:
        for yy in range(int(y + 12), int(y + h - 10), 22): d.ellipse((x + w * .72 - 5, yy, x + w * .72 + 5, yy + 10), fill=NAVY)
        d.rectangle((x + 20, y + 24, x + w * .62, y + 40), fill=(255, 255, 255))
        d.rectangle((x + 20, y + 54, x + w * .45, y + 66), fill=(255, 255, 255))

def popcorn(d, cx, cy, s):
    d.polygon([(cx - s * .5, cy - s * .2), (cx + s * .5, cy - s * .2), (cx + s * .38, cy + s * .7), (cx - s * .38, cy + s * .7)], fill=(250, 250, 250), outline=(10, 12, 18))
    for i in range(-2, 3): d.rectangle((cx + i * s * .2 - s * .05, cy - s * .2, cx + i * s * .2 + s * .05, cy + s * .7), fill=RED)
    for i in range(7):
        a = i / 6 * math.pi; d.ellipse((cx - s * .55 + i * s * .17 - s * .14, cy - s * .38 - math.sin(a) * s * .18 - s * .14,
                                        cx - s * .55 + i * s * .17 + s * .14, cy - s * .38 - math.sin(a) * s * .18 + s * .14), fill=(255, 236, 170), outline=(10, 12, 18))

def header(fr, d, t):
    d.rounded_rectangle((90, 285, 900, 350), 14, fill=RED)
    on = int(t * 2) % 2 == 0
    d.ellipse((110, 302, 140, 332), fill=(255, 255, 255) if on else (255, 160, 160))
    fr.text((160, 288), "BREAKING · BOX OFFICE", xb(44), (255, 255, 255))

def bar(d, x, y, w, h, frac, col):
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=PANEL, outline=(60, 70, 100), width=3)
    if frac > .02: d.rounded_rectangle((x, y, x + w * frac, y + h), h // 2, fill=col)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    dur = (L.t1 - L.t0) if L else 1
    header(fr, d, t)
    if tag in ("hook", "loop"):
        h0 = t0 if tag == "loop" else 0.0
        fx.words_in(fr, t, h0, ["Film", "aayi", "bhi", "NAHI…"], (100, 385), size=92, col=INK, gap=.07)
        if t > h0 + .1:
            k = eout((t - h0 - .1) / .35)
            fr.text((100, 505), f"₹{int(round(65 * k))}", blk(250), GOLD); fr.text((620, 615), "crore", blk(100), GOLD)
        fx.verdict_pill(fr, t, h0 + .6, "BIK GAYE!", (100, 790), size=120, bg=RED)
        if t > h0 + 1.0:
            for i in range(3): ticket(d, 720 + i * 14, 930 - i * 22, 170, 84, (GOLD, CYAN, GREEN)[i], (t - h0 - 1.0 - i * .1) / .25)
    elif tag == "what":
        fr.text((100, 385), "Avengers: Doomsday", xb(76), INK)
        fr.text((100, 480), "Release · India", xb(52), GREY)
        flap(fr, d, t, t0, "17 DEC", 100, 560, cw=110, ch=160, size=130, col=GOLD)
        fr.text((100, 770), "Abhi", xb(64), INK); flap(fr, d, t, t0 + .5, "20", 280, 750, cw=100, ch=140, size=110, col=RED)
        fr.text((500, 770), "din baaki", xb(64), INK)
    elif tag == "tix":
        fr.text((100, 385), "Advance booking", xb(70), INK)
        flap(fr, d, t, t0, "10.36", 100, 490, cw=110, ch=160, size=130, col=GOLD)
        fr.text((700, 540), "LAKH", blk(80), GOLD)
        fr.text((100, 680), "ticket · pehle se BOOK", xb(58), INK)
        n = int(min(1, (t - t0) / 1.5) * 12)
        for i in range(n): ticket(d, 100 + (i % 6) * 128, 790 + (i // 6) * 100, 112, 80, (GOLD, CYAN, GREEN)[i % 3])
    elif tag in ("sec", "nudge"):
        fr.text((100, 385), "24 → 25 Nov: 1 din", xb(64), INK)
        flap(fr, d, t, t0, "₹7.7 CR", 100, 470, cw=96, ch=140, size=110, col=GOLD)
        if tag == "nudge" or t > t0 + dur * .55:
            fr.text((100, 660), "= har SECOND", xb(72), INK)
            k = eout((t - (t0 if tag == "nudge" else t0 + dur * .55)) / .5) if tag == "sec" else 1
            fr.text((100, 750), f"~₹{int(890 * k)}", blk(170), RED)
            # second hand
            cx, cy, r = 800, 860, 80
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=6)
            a = (t % 1) * 2 * math.pi - math.pi / 2
            d.line((cx, cy, cx + math.cos(a) * r * .8, cy + math.sin(a) * r * .8), fill=RED, width=8)
    elif tag == "twist":
        fr.text((100, 385), "Kis language mein?", xb(70), INK)
        k = eout((t - t0 - .2) / 1.0)
        fr.text((100, 500), "English", xb(64), CYAN); bar(d, 100, 585, 800, 70, .84 * k, CYAN)
        fr.text((640, 500), f"{int(84 * k)}%", blk(80), CYAN)
        if t > t0 + 1.4:
            k2 = eout((t - t0 - 1.4) / .8)
            fr.text((100, 690), "Hindi", xb(64), GOLD); bar(d, 100, 775, 800, 70, .12 * k2, GOLD)
            fr.text((640, 690), f"{int(12 * k2)}%", blk(80), GOLD)
    elif tag in ("avg", "day1"):
        fr.text((100, 385), "Average ticket", xb(64), GREY)
        flap(fr, d, t, t0 if tag == "avg" else -5, "₹629", 100, 470, cw=110, ch=160, size=130, col=GOLD)
        popcorn(d, 790, 560, 150)
        if tag == "day1":
            fr.text((100, 690), "Sirf Day 1 (17 Dec)", xb(64), INK)
            flap(fr, d, t, t0 + .3, "₹27.6 CR", 100, 780, cw=88, ch=130, size=100, col=GREEN)
    elif tag in ("record", "ask"):
        fr.text((100, 385), "Hollywood Day 1 record", xb(64), INK)
        fr.text((100, 465), "(India)", xb(48), GREY)
        fr.text((100, 540), "Spider-Man", xb(60), INK); fr.text((560, 530), "₹72.5 cr", blk(80), RED)
        bar(d, 100, 640, 800, 60, 1.0, RED)
        fr.text((100, 730), "Doomsday Day 1", xb(60), INK); fr.text((620, 720), "₹27.6", blk(80), GREEN)
        bar(d, 100, 830, 800, 60, 27.6 / 72.5 * eout((t - t0 - .3) / .8) if tag == "record" else 27.6 / 72.5, GREEN)
        if tag == "ask": fx.verdict_pill(fr, t, t0 + .1, "TOOTEGA?", (100, 920), size=80, bg=GOLD, fg=(15, 15, 15))
    elif tag == "cta":
        fr.text((100, 385), "₹65 crore · 10 lakh ticket", xb(56), GOLD)
    if tag not in ("cta", "loop", "hook", "ask", "record", "tix"): fr.text((100, 1010), "Source: Sacnilk · 27 Nov", xb(34), GREY)

for _L in LINES:
    if _L.gap > .2: _L.gap = .2
R = Reel("Trending_20261127", "xray", LINES, tone="bright", seed=41, tail=.35)
R.nat_speed = 1.12
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(6, 10, 22, 225), font="xb", who_fg=(255, 210, 60))

def setup(R):
    s = R.T("nudge")
    R.nudge = dict(text="Marvel dost ko bhejo", icon="send", at=s, dur=4.5, bg=(255, 200, 40), fg=(15, 15, 25))
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="Bhejo!", body="Us dost ko jo kehta\nhai \"ticket baad\nmein le lunga\"",
                 acc=(230, 45, 50))
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "nudge at", round(s, 2), f"({s / R.dur:.0%})")
    if os.environ.get("AUDIO_ONLY"): sys.exit()
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
