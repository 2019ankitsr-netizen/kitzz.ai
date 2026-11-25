"""Trending Today · Kaam Ki Khabar · Wed 25 Nov 2026 · "1 दिसंबर से SBI कार्ड पर 1% फ़ीस! पर सब पर नहीं" — Group Chat style (Hindi).
SBI Card notice (27 Oct 2026, via Outlook Money 17 Nov, GoodReturns 24 Nov, Utkarsh, CardInsider): from 1 Dec 2026
- fuel: if total fuel spend in one billing cycle > ₹50,000, 1% on the ENTIRE fuel spend (₹55,000 -> ₹550)
- transport (bus, toll, local/suburban commute; MCC 4111/4784/4131): 1% on any SINGLE transaction > ₹30,000 (2 x ₹20,000 = no fee)
UIDAI: adding/updating email in Aadhaar via the Aadhaar app is free (₹75 fee waived) from 1 Jul to 31 Dec 2026.
Usage: python3 episodes/trending_20261125_b_sbi_card_fee.py OUT_DIR
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFont
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_B", "parler:Rohit:calm")
FB = "/home/claude/gfonts/ofl/hind/Hind-Bold.ttf"; FSB = "/home/claude/gfonts/ofl/hind/Hind-SemiBold.ttf"
def HB(s): return ImageFont.truetype(FB, s)
def HS(s): return ImageFont.truetype(FSB, s)

LINES = [
    Line(V, "एक दिसंबर से, एस बी आई कार्ड पर, एक परसेंट फ़ीस! पर सब पर नहीं।", "1 दिसंबर से SBI कार्ड पर 1% फ़ीस! पर सब पर नहीं", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "पापा का फ़ॉरवर्ड, हर पेमेंट पर कटेगा? सच ये है।", "पापा का फ़ॉरवर्ड: हर पेमेंट पर कटेगा? सच ये है", lang="hi", tag="why", sfx="pop"),
    Line(V, "पेट्रोल पर तभी, जब एक बिल में, कुल खर्च पचास हज़ार से ऊपर जाए।",
         "पेट्रोल: एक बिल में कुल ₹50,000 से ऊपर, तभी", lang="hi", tag="fuel", sfx="tick"),
    Line(V, "तब एक परसेंट, पूरे खर्च पर। पचपन हज़ार पर, पाँच सौ पचास।", "तब 1% पूरे खर्च पर: ₹55,000 पर ₹550", lang="hi", tag="fuel2", sfx="tick"),
    Line(V, "ये दो नंबर सेव कर लो। पचास हज़ार, तीस हज़ार।", "सेव कर लो: ₹50,000 और ₹30,000", lang="hi", tag="save", sfx="pop"),
    Line(V, "बस, टोल, लोकल सफ़र में, एक ही पेमेंट तीस हज़ार से ऊपर, तभी।",
         "बस, टोल, लोकल सफ़र: एक पेमेंट ₹30,000+ तभी 1%", lang="hi", tag="transport", sfx="tick"),
    Line(V, "बीस बीस हज़ार के दो पेमेंट? ज़ीरो फ़ीस।", "₹20,000 के दो पेमेंट? ज़ीरो फ़ीस", lang="hi", tag="split", sfx="chime"),
    Line(V, "यानी घर का आम पेट्रोल, बिल्कुल सेफ़।", "यानी घर का आम पेट्रोल: बिल्कुल सेफ़", lang="hi", tag="safe", sfx="chime"),
    Line(V, "और इकत्तीस दिसंबर तक, आधार में ईमेल जोड़ना, आधार ऐप से फ़्री है।",
         "31 दिसंबर तक: आधार में ईमेल जोड़ना फ़्री (आधार ऐप से)", lang="hi", tag="aadhaar", sfx="pop"),
    Line(V, "वरना, पचहत्तर रुपये।", "वरना फ़ीस ₹75", lang="hi", tag="fee", sfx="tick"),
    Line(V, "ये पापा को भेजो, जो हर फ़ॉरवर्ड पर घबरा जाते हैं।", "पापा को भेजो, जो हर फ़ॉरवर्ड पर घबरा जाते हैं", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "क्योंकि एक दिसंबर से, एक परसेंट, पर सब पर नहीं।", "क्योंकि 1 दिसंबर से 1%… पर सब पर नहीं", lang="hi", tag="loop", gap=.05),
]

BG, PAPER, INK = (236, 229, 221), (250, 247, 242), (30, 34, 40)
GREEN, RED, BLUE, GOLD = (32, 140, 90), (215, 45, 45), (40, 95, 190), (240, 175, 40)
ME, THEM = (214, 245, 200), (255, 255, 255)

CHAT = [
    ("hook", "पापा", "1 दिसंबर से कार्ड पर फ़ीस!!", False),
    ("hook", "बंटी", "रुको पापा, पूरा पढ़ो", True),
    ("why", "मम्मी", "हर पेमेंट पर कटेगा क्या?", False),
    ("fuel", "बंटी", "₹50,000 से ऊपर हो तभी", True),
    ("fuel2", "पापा", "हमारा तो ₹6,000 का पेट्रोल है", False),
    ("transport", "पिंकी", "टोल वाला भी?", False),
    ("split", "बंटी", "एक पेमेंट ₹30,000+ हो तभी", True),
    ("safe", "पापा", "चलो, जान में जान आई", False),
    ("aadhaar", "मम्मी", "आधार में ईमेल भी जोड़ दो", False),
    ("cta", "पापा", "अगला फ़ॉरवर्ड पहले तुम्हें भेजूँगा", False),
]

def base():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(0, H, 46):
        for x in range((y // 46) % 2 * 23, W, 46): d.ellipse((x, y, x + 5, y + 5), fill=(226, 218, 208))
    return im
BASE = base()

def bubble(fr, y, who, text, mine, k):
    f = HS(48); fw = HB(28)
    tw = fr.d.textlength(text, font=f); w = min(800, tw + 60); h = 100
    x = 900 - w if mine else 80
    dy = (1 - eback(k)) * 40
    fr.d.rounded_rectangle((x, y + dy, x + w, y + h + dy), 26, fill=ME if mine else THEM, outline=(205, 198, 190), width=2)
    fr.text((x + 30, y + 4 + dy), who, fw, GREEN if not mine else BLUE)
    fr.text((x + 30, y + 32 + dy), text, f, INK)

def tick(d, cx, cy, s, col, w=12):
    d.line([(cx - s, cy), (cx - s * .3, cy + s * .7), (cx + s, cy - s * .8)], fill=col, width=w, joint="curve")

def chip(fr, x, y, txt, f, fg, bg, ol):
    w = fr.d.textlength(txt, font=f) + 44
    fr.d.rounded_rectangle((x, y, x + w, y + f.size + 34), 20, fill=bg, outline=ol, width=4)
    fr.text((x + 22, y + 6), txt, f, fg); return w

def hero(fr, t, R, tag, t0):
    d = fr.d; x0, y0, x1, y1 = 80, 370, 900, 700
    d.rounded_rectangle((x0 + 6, y0 + 8, x1 + 6, y1 + 8), 34, fill=(205, 196, 186))
    d.rounded_rectangle((x0, y0, x1, y1), 34, fill=PAPER, outline=INK, width=4)
    if tag in ("hook", "why", "loop"):
        h0 = t0 if tag == "loop" else 0.0
        # calendar page "1 दिसंबर" on screen at t=0, then "1%" slam + verdict pill
        d.rounded_rectangle((x0 + 40, y0 + 30, x0 + 290, y1 - 30), 24, fill=(255, 255, 255), outline=INK, width=4)
        d.rounded_rectangle((x0 + 40, y0 + 30, x0 + 290, y0 + 95), 24, fill=RED); d.rectangle((x0 + 40, y0 + 70, x0 + 290, y0 + 95), fill=RED)
        fr.text((x0 + 165, y0 + 62), "दिसंबर", HB(40), (255, 255, 255), anchor="mm")
        fr.text((x0 + 165, y0 + 190), "1", F("black", 170), INK, anchor="mm")
        fx.slam_word(fr, t, h0 + .05, "1% फ़ीस?", (x0 + 330, y0 + 40), size=96, col=RED, font=HB)
        fx.verdict_pill(fr, t, h0 + .45, "सब पर नहीं!", (x0 + 330, y0 + 175), size=72, bg=GREEN, font=HB)
    elif tag in ("fuel", "fuel2"):
        fr.text((x0 + 40, y0 + 20), "पेट्रोल-डीज़ल (एक बिल में)", HB(50), INK)
        # meter: 0 -> 60k, red line at 50k
        bx0, bx1, by = x0 + 50, x1 - 50, y0 + 140
        d.rounded_rectangle((bx0, by, bx1, by + 60), 18, fill=(235, 232, 226), outline=INK, width=3)
        fill = 55000 if tag == "fuel2" else 55000 * eout((t - t0 - .3) / 2.2)
        px = bx0 + (bx1 - bx0) * min(fill, 60000) / 60000
        if px > bx0 + 20: d.rounded_rectangle((bx0, by, px, by + 60), 18, fill=RED if fill > 50000 else GOLD)
        lx = bx0 + (bx1 - bx0) * 50000 / 60000
        d.line((lx, by - 20, lx, by + 80), fill=INK, width=6)
        fr.text((lx, by + 88), "₹50,000", HB(44), INK, anchor="ma")
        if tag == "fuel2":
            fr.text((x0 + 40, y0 + 255), "₹55,000 × 1% = ₹550", HB(56), RED)
    elif tag == "save":
        fr.text((x0 + 40, y0 + 20), "ये 2 नंबर याद रखो", HB(64), INK)
        f = F("black", 84)
        if t > t0 + .2: chip(fr, x0 + 40, y0 + 130, "₹50,000", f, RED, (255, 236, 230), RED)
        if t > t0 + 1.0: chip(fr, x0 + 450, y0 + 130, "₹30,000", f, BLUE, (228, 236, 252), BLUE)
        if t > t0 + .2: fr.text((x0 + 60, y0 + 262), "पेट्रोल / महीना", HB(40), INK)
        if t > t0 + 1.0: fr.text((x0 + 470, y0 + 262), "एक पेमेंट", HB(40), INK)
    elif tag in ("transport", "split"):
        fr.text((x0 + 40, y0 + 20), "बस · टोल · लोकल", HB(64), BLUE)
        if tag == "transport":
            fr.text((x0 + 40, y0 + 130), "एक पेमेंट > ₹30,000", HB(62), INK)
            if t > t0 + 1.4: fr.text((x0 + 40, y0 + 225), "तो 1% फ़ीस", HB(56), RED)
        else:
            f = F("black", 60)
            chip(fr, x0 + 40, y0 + 130, "₹20,000", f, INK, (255, 255, 255), INK)
            fr.text((x0 + 345, y0 + 140), "+", F("black", 70), INK)
            chip(fr, x0 + 400, y0 + 130, "₹20,000", f, INK, (255, 255, 255), INK)
            if t > t0 + .9:
                fr.text((x0 + 40, y0 + 240), "फ़ीस = ₹0", HB(60), GREEN); tick(d, x0 + 400, y0 + 270, 30, GREEN)
    elif tag == "safe":
        fr.text((x0 + 40, y0 + 20), "आम घर का पेट्रोल", HB(64), INK)
        k = eback((t - t0) / .4)
        if k > 0:
            s = 70 * k; tick(d, x0 + 140, y0 + 200, s, GREEN, w=int(20 * k) + 1)
            fr.text((x0 + 260, y0 + 140), "बिल्कुल सेफ़", HB(90), GREEN)
    elif tag in ("aadhaar", "fee"):
        fr.text((x0 + 40, y0 + 20), "आधार + ईमेल", HB(68), BLUE)
        fr.text((x0 + 40, y0 + 120), "31 दिसंबर तक फ़्री", HB(66), GREEN)
        fr.text((x0 + 40, y0 + 205), "सिर्फ़ आधार ऐप से", HB(46), INK)
        if tag == "fee": fr.text((x0 + 460, y0 + 205), "वरना ₹75", HB(54), RED)
    elif tag == "cta":
        fr.text((x0 + 40, y0 + 20), "याद रखो", HB(64), INK)
        fr.text((x0 + 40, y0 + 110), "₹50,000 · ₹30,000 · 31 दिसंबर", HB(50), RED)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    d.rounded_rectangle((80, 280, 900, 352), 22, fill=GREEN)
    d.ellipse((96, 290, 148, 342), fill=(255, 255, 255)); fr.text((122, 316), "श", HB(34), GREEN, anchor="mm")
    fr.text((166, 284), "शर्मा परिवार", HB(44), (255, 255, 255))
    d.rounded_rectangle((640, 294, 886, 338), 20, fill=GOLD); fr.text((763, 316), "काम की खबर", HB(32), INK, anchor="mm")
    hero(fr, t, R, tag, t0)
    shown = []
    for i, (tg, who, txt, mine) in enumerate(CHAT):
        try: tt = R.T(tg)
        except KeyError: continue
        same = [c for c in CHAT if c[0] == tg]
        delay = .9 if same.index((tg, who, txt, mine)) == 1 else 0.0
        if tg != "hook" and same.index((tg, who, txt, mine)) == 0: delay = .3
        if t >= tt + delay: shown.append((tt + delay, who, txt, mine))
    shown = shown[-3:] if tag != "cta" else []; y = 716
    for ts, who, txt, mine in shown:
        bubble(fr, y, who, txt, mine, (t - ts) / .3); y += 110

R = Reel("Trending_20261125_B", "story", LINES, tone="warm", seed=25)
R.nat_speed = 1.05
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(20, 24, 30, 215), font="xb", who_fg=(255, 210, 60),
                   fontfile=FB, size=50, lh=62, maxchars=24)

def setup(R):
    s = R.T("save")
    R.nudge = dict(text="सेव करो: ₹50,000 · ₹30,000", icon="save", at=s, dur=4.5, bg=(255, 210, 60), fg=(20, 20, 20), fontfile=FB)
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="पापा को भेजो", body="जो हर फ़ॉरवर्ड पर\nघबरा जाते हैं",
                 acc=(215, 45, 45), fontfile=FB)
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "save at", round(s, 2), f"({s / R.dur:.0%})")
    if os.environ.get("AUDIO_ONLY"): sys.exit()
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
