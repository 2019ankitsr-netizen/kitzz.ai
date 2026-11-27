"""Trending Today · Kaam Ki Khabar · Fri 27 Nov 2026 · "1 दिसंबर से कोहरे की वजह से ट्रेनें रद्द!" — Group Chat style (Hindi).
North Western Railway (CPRO Amit Sudarshan, via Udaipur Kiran 25 Nov 2026): fog schedule 1 Dec 2026 - 28 Feb 2027, 156 trips cancelled:
19611 Ajmer-Amritsar 26 + 19614 Amritsar-Ajmer 26; 12988 Ajmer-Sealdah 39 + 12987 Sealdah-Ajmer 39; 15909/15910 Avadh Assam 13 + 13.
Other zones (NCR, NR Ambala) are also cutting/cancelling trains Dec 2026 - Mar 2027 (HelloRail 17 Nov 2026) -> we only say "other zones too".
Refund: when the railway cancels a train, IRCTC e-ticket fares are refunded automatically in full; counter tickets at the reservation counter.
Usage: python3 episodes/trending_20261127_b_kohra_train.py OUT_DIR
"""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFont
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_B", "parler:Rohit:calm")
FB = "/home/claude/gfonts/ofl/hind/Hind-Bold.ttf"; FSB = "/home/claude/gfonts/ofl/hind/Hind-SemiBold.ttf"
def HB(s): return ImageFont.truetype(FB, s)
def HS(s): return ImageFont.truetype(FSB, s)

LINES = [
    Line(V, "एक दिसंबर से, कोहरे की वजह से, ट्रेनें रद्द!", "1 दिसंबर से कोहरे की वजह से ट्रेनें रद्द!", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "सिर्फ़ नॉर्थ वेस्टर्न रेलवे में, अट्ठाईस फ़रवरी तक, एक सौ छप्पन फेरे रद्द।",
         "सिर्फ़ उत्तर-पश्चिम रेलवे: 28 फ़रवरी तक 156 फेरे रद्द", lang="hi", tag="num", sfx="pop"),
    Line(V, "अजमेर सियालदह एक्सप्रेस, उनतालीस फेरे, दोनों तरफ़।", "अजमेर–सियालदह: 39 फेरे, दोनों तरफ़", lang="hi", tag="t1", sfx="tick"),
    Line(V, "अजमेर अमृतसर, छब्बीस फेरे। अवध असम एक्सप्रेस, तेरह।", "अजमेर–अमृतसर: 26 · अवध असम: 13", lang="hi", tag="t2", sfx="tick"),
    Line(V, "ये तारीख़ें सेव कर लो। एक दिसंबर से, अट्ठाईस फ़रवरी।", "सेव करो: 1 दिसंबर – 28 फ़रवरी", lang="hi", tag="save", sfx="pop"),
    Line(V, "बाकी ज़ोन भी, दिसंबर से मार्च तक, ट्रेनें घटा रहे हैं।", "बाकी ज़ोन भी: दिसंबर–मार्च, ट्रेनें कम", lang="hi", tag="zones", sfx="tick"),
    Line(V, "इसलिए निकलने से पहले, एक तीन नौ पर, या एन टी ई एस पर, ट्रेन नंबर डालकर चेक करो।",
         "निकलने से पहले: 139 या NTES पर ट्रेन नंबर चेक करो", lang="hi", tag="check", sfx="whoosh"),
    Line(V, "और रेलवे ने ट्रेन रद्द की, तो ई टिकट का पूरा पैसा, अपने आप वापस।",
         "रेलवे ने रद्द की? ई-टिकट का पूरा पैसा अपने-आप वापस", lang="hi", tag="refund", sfx="chime"),
    Line(V, "काउंटर टिकट है, तो स्टेशन की खिड़की से रिफ़ंड लो।", "काउंटर टिकट? स्टेशन की खिड़की से रिफ़ंड", lang="hi", tag="counter", sfx="tick"),
    Line(V, "ये शादी वाले फ़ैमिली ग्रुप में डाल दो, जो दिसंबर में ट्रेन से आ रहे हैं।",
         "फ़ैमिली ग्रुप में डालो: जो दिसंबर में ट्रेन से शादी में आ रहे हैं", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "क्योंकि एक दिसंबर से, कोहरा, और ट्रेनें रद्द।", "क्योंकि 1 दिसंबर से… कोहरा और ट्रेनें रद्द", lang="hi", tag="loop", gap=.05),
]

BG, PAPER, INK = (226, 230, 236), (250, 251, 253), (28, 34, 44)
GREEN, RED, BLUE, GOLD, FOG = (32, 140, 90), (215, 45, 45), (40, 95, 190), (240, 175, 40), (200, 206, 216)
ME, THEM = (214, 245, 200), (255, 255, 255)

CHAT = [
    ("hook", "बुआ", "12 दिसंबर की शादी में ट्रेन से आ रहे!", False),
    ("hook", "बंटी", "बुआ, कौन सी ट्रेन? पहले चेक करो", True),
    ("num", "पापा", "156 फेरे?? इतने सारे!", False),
    ("t1", "बुआ", "हमारी तो सियालदह वाली है", False),
    ("t2", "बंटी", "बुआ, 139 पर नंबर डालो", True),
    ("zones", "मम्मी", "हमारे रूट का क्या?", False),
    ("check", "बंटी", "NTES ऐप पे सब दिख जाता है", True),
    ("refund", "मम्मी", "रद्द हुई तो पैसा डूबा?", False),
    ("refund", "बंटी", "ई-टिकट है तो अपने-आप वापस", True),
    ("counter", "पापा", "चलो, ये काम की बात है", False),
]

def base():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for y in range(0, H, 46):
        for x in range((y // 46) % 2 * 23, W, 46): d.ellipse((x, y, x + 5, y + 5), fill=(214, 219, 227))
    return im
BASE = base()

def bubble(fr, y, who, text, mine, k):
    f = HS(48); fw = HB(28)
    tw = fr.d.textlength(text, font=f); w = min(820, tw + 60); h = 100
    x = 900 - w if mine else 80
    dy = (1 - eback(k)) * 40
    fr.d.rounded_rectangle((x, y + dy, x + w, y + h + dy), 26, fill=ME if mine else THEM, outline=(200, 204, 210), width=2)
    fr.text((x + 30, y + 4 + dy), who, fw, GREEN if not mine else BLUE)
    fr.text((x + 30, y + 32 + dy), text, f, INK)

def tick(d, cx, cy, s, col, w=12):
    d.line([(cx - s, cy), (cx - s * .3, cy + s * .7), (cx + s, cy - s * .8)], fill=col, width=w, joint="curve")

def train(d, x, y, s, t, crossed=False):
    """flat original train: engine + 2 coaches, wheels, fog wisps drifting"""
    c = (60, 110, 200)
    for i in range(3):
        bx = x + i * s * 1.05
        d.rounded_rectangle((bx, y, bx + s, y + s * .55), int(s * .12), fill=c if i else RED, outline=INK, width=4)
        for j in range(3): d.rectangle((bx + s * (.12 + j * .28), y + s * .1, bx + s * (.3 + j * .28), y + s * .26), fill=(235, 242, 255), outline=INK, width=2)
        for wx in (.22, .78): d.ellipse((bx + s * wx - s * .09, y + s * .48, bx + s * wx + s * .09, y + s * .66), fill=INK)
    d.line((x - 20, y + s * .66, x + s * 3.3, y + s * .66), fill=INK, width=5)
    for k in range(4):
        fx0 = (x + ((t * 40 + k * 140) % (s * 3.15 - 150)))
        d.rounded_rectangle((fx0, y + s * (.05 + .12 * (k % 3)), fx0 + 150, y + s * (.05 + .12 * (k % 3)) + 26), 13, fill=FOG)
    if crossed:
        d.line((x, y - 10, x + s * 3.1, y + s * .7), fill=RED, width=14)

def chip(fr, x, y, txt, f, fg, bg, ol):
    w = fr.d.textlength(txt, font=f) + 44
    fr.d.rounded_rectangle((x, y, x + w, y + f.size + 34), 20, fill=bg, outline=ol, width=4)
    fr.text((x + 22, y + 6), txt, f, fg); return w

def hero(fr, t, R, tag, t0):
    d = fr.d; x0, y0, x1, y1 = 80, 370, 900, 700
    d.rounded_rectangle((x0 + 6, y0 + 8, x1 + 6, y1 + 8), 34, fill=(196, 202, 212))
    d.rounded_rectangle((x0, y0, x1, y1), 34, fill=PAPER, outline=INK, width=4)
    if tag in ("hook", "loop"):
        h0 = t0 if tag == "loop" else 0.0
        d.rounded_rectangle((x0 + 30, y0 + 30, x0 + 260, y1 - 30), 24, fill=(255, 255, 255), outline=INK, width=4)
        d.rounded_rectangle((x0 + 30, y0 + 30, x0 + 260, y0 + 95), 24, fill=RED); d.rectangle((x0 + 30, y0 + 70, x0 + 260, y0 + 95), fill=RED)
        fr.text((x0 + 145, y0 + 62), "दिसंबर", HB(40), (255, 255, 255), anchor="mm")
        fr.text((x0 + 145, y0 + 190), "1", F("black", 170), INK, anchor="mm")
        fx.slam_word(fr, t, h0 + .05, "कोहरा!", (x0 + 300, y0 + 30), size=100, col=BLUE, font=HB)
        fx.verdict_pill(fr, t, h0 + .45, "ट्रेनें रद्द", (x0 + 300, y0 + 175), size=80, bg=RED, font=HB)
    elif tag == "num":
        fr.text((x0 + 40, y0 + 18), "उत्तर-पश्चिम रेलवे", HB(52), INK)
        k = eout((t - t0 - .2) / .6); v = int(round(156 * k))
        fr.text((x0 + 40, y0 + 85), str(v), F("black", 170), RED)
        fr.text((x0 + 400, y0 + 120), "फेरे रद्द", HB(72), RED)
        fr.text((x0 + 400, y0 + 215), "28 फ़रवरी तक", HB(52), INK)
    elif tag in ("t1", "t2"):
        train(d, x0 + 70, y0 + 28, 190, t, crossed=t > t0 + .6)
        rows = [("अजमेर–सियालदह", "39 + 39")] if tag == "t1" else [("अजमेर–अमृतसर", "26 + 26"), ("अवध असम", "13 + 13")]
        for i, (a, b) in enumerate(rows):
            y = y0 + 180 + i * 62
            fr.text((x0 + 50, y), a, HB(54), INK); fr.text((x0 + 540, y), b, HB(54), RED)
    elif tag == "save":
        fr.text((x0 + 40, y0 + 20), "ये तारीख़ें याद रखो", HB(62), INK)
        f = HB(70)
        if t > t0 + .2: chip(fr, x0 + 40, y0 + 130, "1 दिसंबर", f, RED, (255, 236, 230), RED)
        if t > t0 + .2: fr.text((x0 + 395, y0 + 140), "→", F("black", 70), INK)
        if t > t0 + 1.0: chip(fr, x0 + 470, y0 + 130, "28 फ़रवरी", f, BLUE, (228, 236, 252), BLUE)
    elif tag == "zones":
        fr.text((x0 + 40, y0 + 20), "बाकी ज़ोन भी", HB(64), BLUE)
        fr.text((x0 + 40, y0 + 120), "दिसंबर – मार्च", HB(70), INK)
        fr.text((x0 + 40, y0 + 215), "कुछ रद्द, कुछ के दिन कम", HB(50), RED)
    elif tag == "check":
        fr.text((x0 + 40, y0 + 20), "निकलने से पहले", HB(62), INK)
        if t > t0 + .3: chip(fr, x0 + 40, y0 + 120, "139", F("black", 90), RED, (255, 236, 230), RED)
        if t > t0 + 1.3: chip(fr, x0 + 330, y0 + 120, "NTES", F("black", 90), BLUE, (228, 236, 252), BLUE)
        if t > t0 + 2.2: fr.text((x0 + 40, y0 + 262), "ट्रेन नंबर डालो, स्टेटस देखो", HB(48), INK)
    elif tag in ("refund", "counter"):
        fr.text((x0 + 40, y0 + 20), "रेलवे ने रद्द की?", HB(62), INK)
        k = eback((t - t0 - .3) / .4)
        if k > 0:
            tick(d, x0 + 110, y0 + 180, 60 * k, GREEN, w=int(18 * k) + 1)
            fr.text((x0 + 210, y0 + 120), "ई-टिकट: पूरा पैसा", HB(60), GREEN)
            fr.text((x0 + 210, y0 + 195), "अपने-आप वापस", HB(54), GREEN)
        if tag == "counter": fr.text((x0 + 40, y0 + 262), "काउंटर टिकट: स्टेशन खिड़की", HB(48), BLUE)
    elif tag == "cta":
        fr.text((x0 + 40, y0 + 20), "याद रखो", HB(64), INK)
        fr.text((x0 + 40, y0 + 110), "1 दिसंबर – 28 फ़रवरी · 139", HB(52), RED)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    d.rounded_rectangle((80, 280, 900, 352), 22, fill=GREEN)
    d.ellipse((96, 290, 148, 342), fill=(255, 255, 255)); fr.text((122, 316), "गु", HB(34), GREEN, anchor="mm")
    fr.text((166, 284), "गुप्ता परिवार", HB(44), (255, 255, 255))
    d.rounded_rectangle((640, 294, 886, 338), 20, fill=GOLD); fr.text((763, 316), "काम की खबर", HB(32), INK, anchor="mm")
    hero(fr, t, R, tag, t0)
    shown = []
    for i, (tg, who, txt, mine) in enumerate(CHAT):
        try: tt = R.T(tg)
        except KeyError: continue
        same = [c for c in CHAT if c[0] == tg]
        delay = .9 if same.index((tg, who, txt, mine)) == 1 else 0.0
        if tg != "hook" and same.index((tg, who, txt, mine)) == 0: delay = .3
        if tg == "hook" and same.index((tg, who, txt, mine)) == 0: delay = 1.3
        if tg == "hook" and same.index((tg, who, txt, mine)) == 1: delay = 2.2
        if t >= tt + delay: shown.append((tt + delay, who, txt, mine))
    shown = shown[-3:] if tag not in ("cta", "loop") else []; y = 716
    for ts, who, txt, mine in shown:
        bubble(fr, y, who, txt, mine, (t - ts) / .3); y += 110

R = Reel("Trending_20261127_B", "story", LINES, tone="warm", seed=27)
R.nat_speed = 1.14
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(20, 24, 30, 215), font="xb", who_fg=(255, 210, 60),
                   fontfile=FB, size=50, lh=62, maxchars=24)

def setup(R):
    s = R.T("save")
    R.nudge = dict(text="सेव करो: 1 दिसंबर – 28 फ़रवरी", icon="save", at=s, dur=4.5, bg=(255, 210, 60), fg=(20, 20, 20), fontfile=FB)
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="फ़ैमिली ग्रुप में डालो", body="जो दिसंबर में ट्रेन से\nशादी में आ रहे हैं",
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
