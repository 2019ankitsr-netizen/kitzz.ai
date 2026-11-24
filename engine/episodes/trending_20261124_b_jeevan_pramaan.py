"""Trending Today · Kaam Ki Khabar · Tue 24 Nov 2026 · "30 नवंबर! पेंशन वालों की आख़िरी तारीख़" — Notebook Math style (Hindi).
Annual life certificate (Jeevan Pramaan) for central/state govt pensioners: last date 30 Nov 2026; 80+ could submit from 1 Oct,
others from 1 Nov; if missed, pension may be paused from December until submitted, then released with arrears (NewsKarnataka 6 Nov,
Sentinel Assam 7 Nov 2026). Face authentication: Jeevan Pramaan app + AadhaarFaceRD (Upstox 2 Nov 2026). ~13 crore DLCs since 2014.
Usage: python3 episodes/trending_20261124_b_jeevan_pramaan.py OUT_DIR
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
def blk(s): return F("black", s)

LINES = [
    Line(V, "तीस नवंबर! पेंशन वालों की आख़िरी तारीख़।", "30 नवंबर! पेंशन की आख़िरी तारीख़", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "जीवन प्रमाण, यानी लाइफ़ सर्टिफ़िकेट, हर साल जमा करना होता है।", "जीवन प्रमाण = Life Certificate, हर साल ज़रूरी", lang="hi", tag="what", sfx="pop"),
    Line(V, "नहीं किया, तो दिसंबर से पेंशन रुक सकती है।", "नहीं किया? दिसंबर से पेंशन रुक सकती है", lang="hi", tag="stop", sfx="tick"),
    Line(V, "आख़िरी तारीख़ सबकी एक, तीस नवंबर। सेव कर लो।", "आख़िरी तारीख़ सबकी: 30 नवंबर। सेव करो", lang="hi", tag="save", sfx="pop"),
    Line(V, "दो हज़ार चौदह से अब तक, करीब तेरह करोड़ डिजिटल सर्टिफ़िकेट बन चुके हैं।",
         "2014 से अब तक ~13 करोड़ Digital Life Certificate", lang="hi", tag="crore", sfx="tick"),
    Line(V, "घर बैठे तरीक़ा। फ़ोन में जीवन प्रमाण ऐप, और आधार फ़ेस आर डी ऐप।", "घर बैठे: Jeevan Pramaan + AadhaarFaceRD ऐप", lang="hi", tag="app", sfx="whoosh"),
    Line(V, "आधार और पेंशन की डिटेल डालो, चेहरा कैमरे में दिखाओ, प्रमाण आई डी मिल जाएगी।",
         "आधार + पेंशन डिटेल, चेहरा दिखाओ, Pramaan ID", lang="hi", tag="steps", sfx="tick"),
    Line(V, "फ़ोन नहीं चलता? बैंक ब्रांच, डाकिये की डोरस्टेप सर्विस, या सी एस सी सेंटर।",
         "फ़ोन नहीं? बैंक, डाकिया (IPPB) या CSC सेंटर", lang="hi", tag="offline", sfx="tick"),
    Line(V, "और छूट गया, तो घबराओ मत। जमा करते ही, रुकी पेंशन आमतौर पर बकाया के साथ मिल जाती है।",
         "छूट गया? जमा करते ही बकाया पेंशन आमतौर पर मिल जाती है", lang="hi", tag="missed", sfx="chime"),
    Line(V, "ये दादाजी या नानाजी को भेजो, जिनकी पेंशन आती है।", "दादाजी/नानाजी को भेजो, जिनकी पेंशन आती है", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "क्योंकि आख़िरी तारीख़ है, तीस नवंबर।", "क्योंकि आख़िरी तारीख़… 30 नवंबर", lang="hi", tag="loop", gap=.05),
]

PAPER, LINE_C, MARGIN = (251, 247, 234), (196, 216, 234), (232, 150, 150)
INK, BLUE, RED, GREEN, HL = (32, 30, 44), (30, 70, 170), (205, 40, 40), (30, 125, 75), (255, 228, 92)

def base():
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    for y in range(120, H, 58): d.line((0, y, W, y), fill=LINE_C, width=2)
    d.line((70, 0, 70, H), fill=MARGIN, width=3)
    r = random.Random(24)
    for _ in range(900): x, y = r.randint(0, W), r.randint(0, H); d.point((x, y), fill=(232, 226, 210))
    return im
BASE = base()

def underline(d, t, t0, x0, x1, y, col=RED, w=8, dur=.35):
    if t < t0: return
    k = eout((t - t0) / dur); pts = [(x0 + (x1 - x0) * i / 20, y + math.sin(i * .9) * 4) for i in range(int(20 * k) + 1)]
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")

def circle(d, t, t0, box, col=RED, w=7, dur=.45):
    if t < t0: return
    k = eout((t - t0) / dur); d.arc(box, -100, -100 + 370 * k, fill=col, width=w)

def arrow(d, t, t0, p0, p1, col=INK, w=7, dur=.3):
    if t < t0: return
    k = eout((t - t0) / dur); x = p0[0] + (p1[0] - p0[0]) * k; y = p0[1] + (p1[1] - p0[1]) * k
    d.line((p0[0], p0[1], x, y), fill=col, width=w)
    if k > .95:
        a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        for s in (2.6, -2.6): d.line((x, y, x + 24 * math.cos(a + s), y + 24 * math.sin(a + s)), fill=col, width=w)

def tag_strip(fr, d):
    d.rounded_rectangle((90, 288, 470, 348), 14, fill=INK)
    fr.text((112, 290), "काम की खबर", HB(42), HL)

def big_date(fr, d, t, t0, y=370, pill_at=.45):
    fx.count_up(fr, t, t0, 30, (100, y), size=230, col=RED, dur=.25, font=blk)
    fr.text((440, y + 50), "नवंबर", HB(110), INK)
    fx.verdict_pill(fr, t, t0 + pill_at, "6 दिन बाकी!", (100, y + 280), size=84, bg=INK, fg=HL, font=HB)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    dur = (L.t1 - L.t0) if L else 1
    tag_strip(fr, d)
    if tag in ("hook", "loop", "cta"):
        h0 = 0.0 if tag == "hook" else t0
        big_date(fr, d, t, h0 if tag != "cta" else -5)
        if tag == "hook" and t > 1.0:
            fr.text((100, 860), "पेंशन वालों की", HB(64), INK); fr.text((100, 935), "आख़िरी तारीख़", HB(64), RED)
            underline(d, t, 1.3, 100, 520, 1020)
    elif tag == "what":
        fr.text((100, 380), "जीवन प्रमाण", HB(110), INK); underline(d, t, t0 + .2, 100, 700, 530)
        if t > t0 + .8: fr.text((100, 570), "= Life Certificate", blk(78), BLUE)
        if t > t0 + 1.6:
            fr.text((130, 720), "हर साल", HB(90), RED); circle(d, t, t0 + 1.7, (95, 700, 470, 850))
        if t > t0 + 2.4: fr.text((520, 740), "ज़िंदा होने का सबूत", HS(52), INK)
    elif tag == "stop":
        fr.text((100, 380), "नहीं किया तो?", HB(96), INK)
        # December calendar card
        x0, y0 = 120, 540
        d.rounded_rectangle((x0, y0, x0 + 420, y0 + 380), 24, fill=(255, 255, 255), outline=INK, width=5)
        d.rounded_rectangle((x0, y0, x0 + 420, y0 + 90), 24, fill=BLUE); d.rectangle((x0, y0 + 60, x0 + 420, y0 + 90), fill=BLUE)
        fr.text((x0 + 210, y0 + 46), "दिसंबर", HB(58), (255, 255, 255), anchor="mm")
        fr.text((x0 + 210, y0 + 230), "पेंशन", HB(96), INK, anchor="mm")
        if t > t0 + .9:
            k = eout((t - t0 - .9) / .3)
            d.line((x0 + 40, y0 + 130, x0 + 40 + 340 * k, y0 + 130 + 220 * k), fill=RED, width=16)
            d.line((x0 + 380, y0 + 130, x0 + 380 - 340 * k, y0 + 130 + 220 * k), fill=RED, width=16)
        if t > t0 + 1.4: fr.text((590, 640), "रुक", HB(110), RED); fr.text((590, 780), "सकती है", HB(72), RED)
    elif tag in ("age", "save"):
        fr.text((100, 380), "कब से जमा?", HB(84), INK); underline(d, t, t0, 100, 520, 495) if tag == "age" else None
        rows = [("80+ साल", "1 अक्टूबर से", 0.0), ("बाकी सब", "1 नवंबर से", dur * .55 if tag == "age" else 0)]
        for i, (a, b, at) in enumerate(rows):
            if tag == "save" or t > t0 + at:
                y = 540 + i * 130
                fr.text((110, y), a, HB(70), BLUE); arrow(d, t, (t0 + at) if tag == "age" else -5, (420, y + 50), (500, y + 50))
                fr.text((530, y), b, HB(70), INK)
        if tag == "save":
            d.rounded_rectangle((100, 820, 880, 1000), 26, fill=HL, outline=INK, width=5)
            fr.text((130, 836), "सबकी आख़िरी तारीख़", HB(52), INK)
            fx.count_up(fr, t, t0 + .2, 30, (130, 892), size=90, col=RED, dur=.3, fmt="{} नवंबर", font=HB)
    elif tag == "crore":
        fr.text((100, 380), "2014 से अब तक", HB(76), INK); underline(d, t, t0, 100, 600, 485)
        fx.count_up(fr, t, t0 + .3, 13, (100, 500), size=300, col=RED, dur=.5, fmt="~{}", font=blk)
        if t > t0 + .8: fr.text((110, 790), "करोड़", HB(130), RED)
        if t > t0 + 1.2: fr.text((110, 960), "Digital Life Certificate", blk(56), BLUE)
    elif tag in ("app", "steps"):
        # generic phone outline with a face oval (no real app UI)
        px, py = 110, 380
        d.rounded_rectangle((px, py, px + 330, py + 620), 44, fill=(255, 255, 255), outline=INK, width=7)
        d.rounded_rectangle((px + 120, py + 22, px + 210, py + 36), 7, fill=INK)
        k = ease((t - t0) / .6) if tag == "app" else 1
        d.ellipse((px + 85, py + 140, px + 85 + 160 * k, py + 140 + 210 * k), outline=GREEN, width=8)
        if k >= 1:
            d.ellipse((px + 125, py + 220, px + 140, py + 235), fill=INK); d.ellipse((px + 190, py + 220, px + 205, py + 235), fill=INK)
            d.arc((px + 125, py + 250, px + 205, py + 310), 20, 160, fill=INK, width=6)
            fr.text((px + 165, py + 430), "Face", blk(58), GREEN, anchor="mm")
        if tag == "app":
            if t > t0 + .9: fr.text((490, 420), "Jeevan", blk(64), BLUE); fr.text((490, 495), "Pramaan", blk(64), BLUE)
            if t > t0 + 1.8: fr.text((490, 610), "+", blk(70), INK); fr.text((490, 690), "AadhaarFaceRD", blk(44), BLUE)
            if t > t0 + 2.4: fr.text((490, 780), "घर बैठे", HB(72), RED)
        else:
            steps = [("1", "आधार + पेंशन", "डिटेल"), ("2", "चेहरा", "कैमरे में"), ("3", "Pramaan ID", "मिल गई")]
            for i, (n, a, b) in enumerate(steps):
                if t < t0 + i * dur * .3: continue
                y = 400 + i * 200
                d.ellipse((480, y, 560, y + 80), fill=RED if i == 2 else INK); fr.text((520, y + 40), n, blk(52), (255, 255, 255), anchor="mm")
                fr.text((580, y - 4), a, HB(56) if not a.isascii() else blk(50), INK); fr.text((580, y + 70), b, HS(46), INK)
    elif tag == "offline":
        fr.text((100, 380), "फ़ोन नहीं चलता?", HB(90), INK); underline(d, t, t0, 100, 720, 500)
        opts = [("बैंक ब्रांच", BLUE), ("डाकिया (IPPB)", GREEN), ("CSC सेंटर", RED)]
        for i, (s, col) in enumerate(opts):
            if t < t0 + .5 + i * .6: continue
            y = 560 + i * 150; k = eback((t - t0 - .5 - i * .6) / .3)
            d.rounded_rectangle((110, y, 110 + 640 * k, y + 120), 26, fill=(255, 255, 255), outline=col, width=7)
            if k > .9: fr.text((150, y + 18), s, HB(66), col)
    elif tag == "missed":
        fr.text((100, 380), "छूट गया?", HB(100), INK); fr.text((520, 400), "घबराओ मत", HB(70), GREEN)
        if t > t0 + 1.0:
            d.rounded_rectangle((110, 580, 420, 720), 24, fill=(255, 255, 255), outline=INK, width=5); fr.text((265, 650), "जमा करो", HB(60), INK, anchor="mm")
            arrow(d, t, t0 + 1.4, (440, 650), (540, 650))
        if t > t0 + 1.8:
            d.rounded_rectangle((560, 580, 880, 720), 24, fill=HL, outline=INK, width=5); fr.text((720, 650), "पेंशन चालू", HB(56), INK, anchor="mm")
        if t > t0 + 2.6: fr.text((110, 780), "बकाया भी आमतौर पर मिलता है", HS(54), BLUE)

R = Reel("Trending_20261124_B", "cctv", LINES, tone="warm", seed=24)
R.nat_speed = 1.12
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(20, 24, 40, 220), font="xb", who_fg=(255, 210, 60),
                   fontfile=FB, size=50, lh=62, maxchars=24)

def setup(R):
    s = R.line("crore").t1 - .6
    R.nudge = dict(text="सेव करो: 30 नवंबर", icon="save", at=s, dur=4.5, bg=(255, 210, 60), fg=(20, 20, 20), fontfile=FB)
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="दादाजी को भेजो", body="या नानाजी को, जिनकी\nपेंशन आती है",
                 acc=(205, 40, 40), fontfile=FB)
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "save at", round(s, 2), f"({s / R.dur:.0%})")
    if os.environ.get("AUDIO_ONLY"): sys.exit()
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
