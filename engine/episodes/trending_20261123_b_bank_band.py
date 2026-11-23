"""Trending Today · Kaam Ki Khabar · Mon 23 Nov 2026 · "24 नवंबर को बैंक बंद!" — Group Chat style (Hindi).
Guru Nanak Jayanti + Kartik Purnima on Tue 24 Nov: bank branches shut in 16 states (Upstox list, 30 Oct 2026),
Karnataka 27 Nov, 4th Saturday 28 Nov, Sunday 29 Nov. UPI / ATM / net banking keep working.
Usage: python3 episodes/trending_20261123_b_bank_band.py OUT_DIR
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFont
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_B", "parler:Rohit:calm")
FB = "/home/claude/gfonts/ofl/hind/Hind-Bold.ttf"; FSB = "/home/claude/gfonts/ofl/hind/Hind-SemiBold.ttf"
FY = "/home/claude/gfonts/ofl/yatraone/YatraOne-Regular.ttf"
def HB(s): return ImageFont.truetype(FB, s)
def HS(s): return ImageFont.truetype(FSB, s)
def YO(s): return ImageFont.truetype(FY, s)

LINES = [
    Line(V, "चौबीस नवंबर को बैंक बंद!", "24 नवंबर को बैंक बंद!", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "कल गुरु नानक जयंती और कार्तिक पूर्णिमा, एक ही दिन है।", "कल गुरु नानक जयंती + कार्तिक पूर्णिमा, एक ही दिन", lang="hi", tag="why", sfx="pop"),
    Line(V, "पंजाब, हरियाणा, यू पी, एम पी समेत, सोलह राज्यों में ब्रांच बंद रहेंगी।",
         "पंजाब, हरियाणा, UP, MP समेत 16 राज्यों में ब्रांच बंद", lang="hi", tag="states", sfx="tick"),
    Line(V, "तारीखें सेव कर लो, क्योंकि इसी हफ़्ते और भी छुट्टियाँ हैं।", "तारीखें सेव कर लो, इसी हफ़्ते और भी छुट्टी", lang="hi", tag="save", sfx="pop"),
    Line(V, "सत्ताईस नवंबर, शुक्रवार को, कर्नाटक में कनकदास जयंती।", "27 नवंबर (शुक्र): कर्नाटक में कनकदास जयंती", lang="hi", tag="d27", sfx="tick"),
    Line(V, "अट्ठाईस को चौथा शनिवार, उनतीस को रविवार, पूरे देश में ब्रांच बंद।",
         "28: चौथा शनिवार, 29: रविवार। पूरे देश में ब्रांच बंद", lang="hi", tag="d28", sfx="tick"),
    Line(V, "पर घबराओ मत। यू पी आई, ए टी एम और नेट बैंकिंग चालू रहेंगे।", "पर घबराओ मत: UPI, ATM, नेट बैंकिंग चालू", lang="hi", tag="upi", sfx="chime"),
    Line(V, "चेक या लॉकर का काम, आज ही, या पच्चीस, छब्बीस को निपटा लो।",
         "चेक या लॉकर का काम? आज ही, या 25-26 नवंबर को", lang="hi", tag="tip", sfx="tick"),
    Line(V, "दिल्ली वाले, अपनी ब्रांच से एक बार पूछ लें।", "दिल्ली वाले: अपनी ब्रांच से एक बार पूछ लें", lang="hi", tag="delhi"),
    Line(V, "ये पापा को भेजो, जिनका कल बैंक का काम पेंडिंग है।", "पापा को भेजो, जिनका कल बैंक का काम पेंडिंग है", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "क्योंकि कल, चौबीस नवंबर है।", "क्योंकि कल… 24 नवंबर है", lang="hi", tag="loop", gap=.05),
]

BG, PAPER, INK = (236, 229, 221), (250, 247, 242), (30, 34, 40)
GREEN, RED, BLUE, GOLD = (32, 140, 90), (215, 45, 45), (40, 95, 190), (240, 175, 40)
ME, THEM = (214, 245, 200), (255, 255, 255)

# chat bubbles: (appears with tag, who, text, mine)
CHAT = [
    ("hook", "पापा", "कल बैंक जाकर FD करवा दूँगा", False),
    ("hook", "बंटी", "पापा कल बैंक बंद है!", True),
    ("why", "मम्मी", "हाँ, कल गुरुपर्व और पूर्णिमा है", False),
    ("states", "पापा", "हमारे राज्य में भी?", False),
    ("d27", "पिंकी", "बेंगलुरु में 27 को भी छुट्टी", False),
    ("d28", "बंटी", "और 28-29 को पूरे देश में", True),
    ("upi", "पापा", "तो किराया कैसे भेजूँ?", False),
    ("upi", "बंटी", "UPI चालू है पापा", True),
    ("tip", "मम्मी", "लॉकर वाला काम 25 को करेंगे", False),
    ("cta", "पापा", "अच्छा हुआ बता दिया", False),
]

def base():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(0, H, 46):
        for x in range((y // 46) % 2 * 23, W, 46): d.ellipse((x, y, x + 5, y + 5), fill=(226, 218, 208))
    return im
BASE = base()

def bubble(fr, x, y, who, text, mine, k):
    f = HS(48); fw = HB(28)
    tw = fr.d.textlength(text, font=f); w = min(760, tw + 60); h = 100
    x = 900 - w if mine else 80
    dy = (1 - eback(k)) * 40
    fr.d.rounded_rectangle((x, y + dy, x + w, y + h + dy), 26, fill=ME if mine else THEM, outline=(205, 198, 190), width=2)
    fr.text((x + 30, y + 4 + dy), who, fw, GREEN if not mine else BLUE)
    fr.text((x + 30, y + 30 + dy), text, f, INK)
    return h

def hero(fr, t, R, tag, t0):
    d = fr.d; x0, y0, x1, y1 = 80, 370, 900, 700
    d.rounded_rectangle((x0 + 6, y0 + 8, x1 + 6, y1 + 8), 34, fill=(205, 196, 186))
    d.rounded_rectangle((x0, y0, x1, y1), 34, fill=PAPER, outline=INK, width=4)
    if tag in ("hook", "why", "loop"):
        # calendar page: "24" counts up, then the verdict pill
        d.rounded_rectangle((x0 + 40, y0 + 30, x0 + 300, y1 - 30), 24, fill=(255, 255, 255), outline=INK, width=4)
        d.rounded_rectangle((x0 + 40, y0 + 30, x0 + 300, y0 + 95), 24, fill=RED); d.rectangle((x0 + 40, y0 + 70, x0 + 300, y0 + 95), fill=RED)
        fr.text((x0 + 170, y0 + 62), "नवंबर", HB(40), (255, 255, 255), anchor="mm")
        fx.count_up(fr, t, 0.0, 24, (x0 + 85, y0 + 95), size=150, col=INK, dur=.25, font=lambda s: F("black", s))
        fr.text((x0 + 340, y0 + 36), "मंगलवार", HB(54), INK)
        fx.verdict_pill(fr, t, .5, "बैंक बंद!", (x0 + 340, y0 + 120), size=84, bg=RED, font=HB)
    elif tag == "states":
        fr.text((x0 + 40, y0 + 22), "16 राज्य", HB(96), RED)
        names = ["पंजाब", "हरियाणा", "UP", "MP", "महाराष्ट्र", "राजस्थान", "बंगाल", "तेलंगाना"]
        x, y = x0 + 40, y0 + 150
        for i, n in enumerate(names):
            a = t - (t0 + .25 + i * .35)
            if a < 0: break
            f = HB(44); w = fr.d.textlength(n, font=f) + 36
            if x + w > x1 - 30: x, y = x0 + 40, y + 66
            d.rounded_rectangle((x, y, x + w, y + 56), 16, fill=(255, 232, 226), outline=RED, width=3)
            fr.text((x + 18, y + 2), n, f, INK); x += w + 14
    elif tag in ("save", "d27", "d28"):
        fr.text((x0 + 40, y0 + 20), "इस हफ़्ते", HB(64), INK)
        days = [("24", "मंगल", "16 राज्य", "hook"), ("27", "शुक्र", "कर्नाटक", "d27"), ("28", "शनि", "पूरा देश", "d28"), ("29", "रवि", "पूरा देश", "d28")]
        order = ["hook", "save", "d27", "d28"]
        for i, (dd, wd, wh, need) in enumerate(days):
            on = order.index(tag) >= order.index(need) if need != "hook" else True
            cx = x0 + 40 + i * 190; cy = y0 + 110
            d.rounded_rectangle((cx, cy, cx + 170, cy + 160), 20, fill=(255, 255, 255) if not on else (255, 236, 230), outline=RED if on else (190, 185, 178), width=4)
            fr.text((cx + 85, cy + 50), dd, F("black", 72), RED if on else (170, 165, 158), anchor="mm")
            fr.text((cx + 85, cy + 112), wd, HB(40), INK, anchor="mm")
            if on: fr.text((cx + 85, cy + 186), wh, HB(34), INK, anchor="mm")
    elif tag == "upi":
        fr.text((x0 + 40, y0 + 22), "ये चालू रहेंगे", HB(72), GREEN)
        for i, n in enumerate(["UPI", "ATM", "नेट बैंकिंग"]):
            a = t - (t0 + .9 + i * .45)
            if a < 0: break
            cx = x0 + 40 + i * 250; cy = y0 + 150
            d.rounded_rectangle((cx, cy, cx + 230, cy + 100), 22, fill=(222, 245, 230), outline=GREEN, width=4)
            fr.text((cx + 115, cy + 50), n, F("black", 50) if n.isascii() else HB(42), INK, anchor="mm")
            d.line((cx + 60, cy + 120, cx + 100, cy + 125), fill=GREEN, width=0)
    elif tag in ("tip", "delhi", "cta"):
        fr.text((x0 + 40, y0 + 22), "काम निपटाओ", HB(72), BLUE)
        fr.text((x0 + 40, y0 + 120), "आज (23)  या  25-26 नवंबर", HB(56), INK)
        if tag != "tip" or t > t0 + 1.2:
            fr.text((x0 + 40, y0 + 200), "दिल्ली: ब्रांच से पूछें", HB(48), RED)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    # chat header (unbranded)
    d.rounded_rectangle((80, 280, 900, 352), 22, fill=GREEN)
    d.ellipse((96, 290, 148, 342), fill=(255, 255, 255)); fr.text((122, 316), "श", HB(34), GREEN, anchor="mm")
    fr.text((166, 284), "शर्मा परिवार", HB(44), (255, 255, 255))
    d.rounded_rectangle((640, 294, 886, 338), 20, fill=GOLD); fr.text((763, 316), "काम की खबर", HB(32), INK, anchor="mm")
    hero(fr, t, R, tag, t0)
    # chat bubbles: last 3 that have appeared
    shown = []
    for tg, who, txt, mine in CHAT:
        try: tt = R.T(tg)
        except KeyError: continue
        delay = 0.0 if tg != "hook" else (0.0 if not mine else .9)
        if tg != "hook" and [c for c in CHAT if c[0] == tg].index((tg, who, txt, mine)) == 1: delay = 1.2
        if t >= tt + delay: shown.append((tt + delay, who, txt, mine))
    shown = shown[-3:]; y = 716
    for ts, who, txt, mine in shown:
        bubble(fr, 80, y, who, txt, mine, (t - ts) / .3); y += 110

R = Reel("Trending_20261123_B", "story", LINES, tone="warm", seed=23)
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(20, 24, 30, 215), font="xb", who_fg=(255, 210, 60),
                   fontfile=FB, size=50, lh=62, maxchars=24)

def setup(R):
    s = R.T("save")
    s = R.T("d27") - .3
    R.nudge = dict(text="सेव करो: 24 · 27 · 28 नवंबर", icon="save", at=s, dur=4.5, bg=(255, 210, 60), fg=(20, 20, 20), fontfile=FB)
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="पापा को भेजो", body="जिनका कल बैंक का\nकाम पेंडिंग है",
                 acc=(215, 45, 45), fontfile=FB)
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "save at", round(s, 2), f"({s / R.dur:.0%})")
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
