"""Trending Today · Fan Buzz (Reel A) · Sat 28 Nov 2026 · "No. 11 ka WORLD RECORD? Ek Indian BOWLER!" — Pop Comic (Hinglish).
Jaydev Unadkat (Saurashtra captain, batting No. 11) 40 off 26 balls (3x4, 2x6) v Tamil Nadu, Syed Mushtaq Ali Trophy 2026,
Elite Group B, Holkar Stadium, Indore, Thu 26 Nov 2026 = highest T20 score by a No. 11 (previous: Danny Briggs 35* off 18,
Adelaide Strikers v Hobart Hurricanes, BBL, 13 Dec 2020). Came in at 92/9 chasing 193; Saurashtra 154 all out (16.4 ov);
62-run 10th-wicket stand with Chetan Sakariya (21*) = joint-2nd highest 10th-wkt stand in men's T20 (record 63, Elliott/Babar,
PSL 2016). Tamil Nadu won by 38. Sources: indiatvnews.com 27 Nov; aajsamaaj.com 27 Nov 11:22 UTC; bcci.tv video "40(26)".
Google Trends India 28 Nov morning: "जयदेव उनादकट" 50K+. Our maths: 62 / 154 = 40% of the total from the last wicket.
No faces/logos: original comic bursts, batting-order ladder, bars, ball grid.
Usage: python3 episodes/trending_20261128_unadkat_no11.py OUT_DIR
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_A", "parler:Rohit:news")

LINES = [
    Line(V, "टी ट्वेंटी में, नंबर ग्यारह का, वर्ल्ड रिकॉर्ड किसके नाम? एक इंडियन बॉलर के!",
         "No. 11 ka WORLD RECORD? Ek Indian BOWLER!", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "जयदेव उनादकट। सैयद मुश्ताक अली ट्रॉफ़ी, सौराष्ट्र बनाम तमिलनाडु, इंदौर में।",
         "Jaydev Unadkat · Saurashtra vs Tamil Nadu", lang="hi", tag="who", sfx="pop"),
    Line(V, "टारगेट, एक सौ तिरानवे। और स्कोर, बानवे पर नौ विकेट।", "Target 193… score 92/9!", lang="hi", tag="score", sfx="hit"),
    Line(V, "तब आए, नंबर ग्यारह पर। और मारे, छब्बीस गेंदों में, चालीस रन!", "No. 11 pe aaye… 26 ball, 40 RUN!",
         lang="hi", tag="forty", sfx="tick"),
    Line(V, "क्रिकेट वाले दोस्त को भेजो, असली ट्विस्ट अभी बाकी है।", "Cricket dost ko bhejo, twist baaki hai",
         lang="hi", tag="nudge", sfx="pop"),
    Line(V, "पहले रिकॉर्ड था, पैंतीस नॉट आउट। इंग्लैंड के डैनी ब्रिग्स, बिग बैश में, दो हज़ार बीस में।",
         "Pehle: 35* · Danny Briggs · Big Bash 2020", lang="hi", tag="bars", sfx="whoosh"),
    Line(V, "और चेतन सकारिया के साथ, आख़िरी विकेट के लिए, बासठ रन की पार्टनरशिप।",
         "Last wicket: 62 run ki partnership!", lang="hi", tag="stand", sfx="tick"),
    Line(V, "टी ट्वेंटी में, दसवें विकेट की, ये संयुक्त रूप से, दूसरी सबसे बड़ी साझेदारी है।",
         "T20 mein 10th wicket: joint No. 2!", lang="hi", tag="rank", sfx="hit"),
    Line(V, "बानवे से, एक सौ चौवन। यानी, आख़िरी विकेट ने, टीम के, चालीस परसेंट रन जोड़ दिए।",
         "92 → 154 · last wicket = team ka 40%!", lang="hi", tag="math", sfx="hit"),
    Line(V, "लेकिन ट्विस्ट? सौराष्ट्र फिर भी, अड़तीस रन से हार गया।", "Twist? Saurashtra phir bhi 38 run se HAARA",
         lang="hi", tag="twist", sfx="whoosh"),
    Line(V, "उस दोस्त को भेजो, जो गली क्रिकेट में, हमेशा नंबर ग्यारह पर आता है।",
         "Gully ke No. 11 dost ko bhejo!", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "तो बताओ, नंबर ग्यारह का वर्ल्ड रिकॉर्ड, किसके नाम?", "To batao… No. 11 ka record kiske naam?", lang="hi", tag="loop", gap=.05),
]

YEL, RED, CYAN, INK, WHITE = (255, 214, 0), (230, 40, 50), (40, 190, 230), (18, 18, 24), (255, 255, 255)
PINK, GREEN, GREY, ORANGE = (255, 120, 160), (40, 170, 90), (175, 175, 182), (255, 140, 30)

def base():
    im = Image.new("RGB", (W, H), (120, 225, 170)); d = ImageDraw.Draw(im)
    for y in range(0, H, 34):            # halftone dots (mint page: new vs 24 Nov yellow / 26 Nov sky-blue)
        for x in range((y // 34) % 2 * 17, W, 34):
            r = 3 + 3 * (y / H); d.ellipse((x - r, y - r, x + r, y + r), fill=(80, 200, 140))
    return im
BASE = base()

def burst(d, cx, cy, r, col, k=1.0, n=14, rot=0.0):
    if k <= 0: return
    pts = []
    for i in range(n * 2):
        a = rot + i * math.pi / n; rr = r * k * (1 if i % 2 == 0 else .68)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon([(x + 10, y + 12) for x, y in pts], fill=INK)
    d.polygon(pts, fill=col, outline=INK, width=7)

def panel(d, box, col=WHITE, k=1.0):
    x0, y0, x1, y1 = box; x1 = x0 + (x1 - x0) * max(.01, k)
    d.rectangle((x0 + 10, y0 + 12, x1 + 10, y1 + 12), fill=INK)
    d.rectangle((x0, y0, x1, y1), fill=col, outline=INK, width=7)

def title(fr, d, text, col=INK, y=372, size=78, bg=WHITE):
    f = F("black", size); w = fr.d.textlength(text, font=f)
    panel(d, (90, y, 90 + w + 50, y + size + 34), bg)
    fr.text((115, y + 10), text, f, col)

def ball(d, x, y, r=14, col=RED):
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=INK, width=4)
    d.arc((x - r * .6, y - r, x + r * .6, y + r), 250, 290, fill=WHITE, width=2)

def ball_grid(fr, d, t, t0, n, per=.03, hi=(), y0=560, cols=10, col=WHITE, x0=140):
    for i in range(n):
        if t < t0 + i * per: break
        r_, c_ = divmod(i, cols); x = x0 + c_ * 74; y = y0 + r_ * 74
        ball(d, x, y, 24, RED if i in hi else col)

def bat(d, x, y, k=1.0, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    def R(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    blade = [R(0, -30), R(220, -36), R(230, 0), R(220, 36), R(0, 30)]
    d.polygon([(a + 8, b + 10) for a, b in blade], fill=INK)
    d.polygon(blade, fill=(235, 195, 125), outline=INK, width=6)
    d.line([R(-120, 0), R(0, 0)], fill=INK, width=26); d.line([R(-115, 0), R(-5, 0)], fill=RED, width=14)

def ladder(fr, d, t, t0, hi=11, x=110, y0=500, k_all=None):
    """batting order 1..11 as stacked chips; No. 11 highlighted."""
    for n in range(1, 12):
        tt = t0 + (n - 1) * .04
        if t < tt: break
        y = y0 + (n - 1) * 46; c = YEL if n == hi else WHITE
        d.rectangle((x, y, x + 120, y + 40), fill=c, outline=INK, width=4)
        fr.text((x + 60, y + 20), str(n), F("black", 30), INK, anchor="mm")

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    dur = (L.t1 - L.t0) if L else 1
    if tag in ("hook", "loop"):
        h0 = 0.0 if tag == "hook" else t0
        fx.words_in(fr, t, h0, ["T20", "MEIN"], (110, 380), size=72, col=INK, gap=.08, font=lambda s: F("black", s))
        burst(d, 500, 620, 230, YEL, eback((t - h0) / .3), rot=t * .3)
        if t > h0 + .05:
            k = eback((t - h0 - .05) / .25)
            fr.text((500, 620), "No. 11", F("black", int(150 * max(.3, k))), RED, anchor="mm")
        if t > h0 + .3:
            panel(d, (100, 800, 100 + 720 * min(1, eout((t - h0 - .3) / .2)), 900), WHITE, 1)
            if t > h0 + .4: fr.text((130, 812), "WORLD RECORD?", F("black", 66), INK)
        fx.verdict_pill(fr, t, h0 + .65, "EK INDIAN BOWLER!", (100, 950), size=70, bg=INK, fg=YEL)
    elif tag == "who":
        title(fr, d, "JAYDEV UNADKAT", INK, size=68)
        k = eback((t - t0) / .35)
        panel(d, (100, 500, 900, 680), YEL, min(1, k)); fr.text((140, 530), "Saurashtra", F("black", 100), INK)
        if t > t0 + .8:
            panel(d, (100, 740, 900, 870), WHITE); fr.text((130, 762), "vs Tamil Nadu", F("black", 70), INK)
        if t > t0 + 1.6:
            panel(d, (100, 920, 640, 1020), CYAN); fr.text((125, 935), "Indore · SMAT", F("xb", 54), INK)
    elif tag == "score":
        title(fr, d, "TARGET: 193", INK)
        if t > t0 + dur * .2:
            k = eback((t - t0 - dur * .2) / .35)
            burst(d, 480, 720, 230, RED, k, n=12, rot=.2)
            fr.text((480, 720), "92/9", F("black", 150), WHITE, anchor="mm")
            fx.verdict_pill(fr, t, t0 + dur * .55, "9 OUT!", (100, 990), size=72, bg=INK, fg=YEL)
    elif tag == "forty":
        title(fr, d, "No. 11 PE AAYE…", INK, size=66)
        ladder(fr, d, t, t0, y0=500)
        ball_grid(fr, d, t, t0 + .3, 26, per=min(.04, dur * .4 / 26), hi={3, 9, 14, 19, 23}, y0=530, cols=7, x0=310)
        if t > t0 + dur * .55:
            fx.verdict_pill(fr, t, t0 + dur * .55, "26 BALL · 40 RUN!", (100, 1000), size=70, bg=RED, fg=WHITE)
    elif tag == "nudge":
        title(fr, d, "TWIST BAAKI HAI", INK)
        burst(d, 480, 760, 240, PINK, 1, rot=t * .4)
        fr.text((480, 760), "???", F("black", 150), WHITE, anchor="mm")
    elif tag == "bars":
        title(fr, d, "No. 11: SABSE BADA SCORE", INK, size=58)
        k1 = eout((t - t0 - .3) / .8); k2 = eout((t - t0 - dur * .55) / .6)
        full = 760
        panel(d, (100, 560, 100 + full * 35 / 40 * k1, 680), GREY, 1)
        if k1 > .6: fr.text((120, 580), "35*  Briggs · 2020", F("black", 56), INK)
        if k2 > 0:
            panel(d, (100, 740, 100 + full * k2, 860), RED, 1)
            if k2 > .6: fr.text((120, 760), "40  Unadkat", F("black", 62), WHITE)
        if t > t0 + dur * .8:
            fx.verdict_pill(fr, t, t0 + dur * .8, "NEW WORLD RECORD", (100, 930), size=66, bg=INK, fg=YEL)
    elif tag in ("stand", "rank"):
        title(fr, d, "LAST WICKET", INK)
        k = eout((t - t0 - .2) / .9) if tag == "stand" else 1
        panel(d, (100, 520, 900, 700), WHITE); fr.text((140, 540), "Unadkat", F("black", 64), INK); fr.text((140, 615), "+ Sakariya", F("black", 56), INK)
        panel(d, (100, 740, 100 + 800 * k, 880), YEL, 1)
        if k > .3: fx.count_up(fr, t, t0 + .2, 62, (140, 745), size=120, col=RED, dur=.6) if tag == "stand" else fr.text((140, 745), "62", F("black", 120), RED)
        if k > .5: fr.text((420, 790), "run partnership", F("xb", 48), INK)
        if tag == "rank":
            fx.verdict_pill(fr, t, t0 + .2, "T20: JOINT No. 2", (100, 930), size=72, bg=RED, fg=WHITE)
    elif tag == "math":
        title(fr, d, "HISAAB", INK)
        panel(d, (100, 520, 900, 690), WHITE); fr.text((140, 535), "92 → 154", F("black", 120), INK)
        if t > t0 + dur * .45:
            cx, cy, r = 330, 860, 130
            d.ellipse((cx - r + 8, cy - r + 10, cx + r + 8, cy + r + 10), fill=INK)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=INK, width=6)
            kk = eout((t - t0 - dur * .45) / .6)
            d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * .40 * kk, fill=RED, outline=INK, width=6)
            fx.count_up(fr, t, t0 + dur * .45, 40, (520, 780), size=150, col=RED, dur=.5)
            fr.text((760, 800), "%", F("black", 110), INK)
    elif tag == "twist":
        title(fr, d, "TWIST?", RED, size=90)
        burst(d, 480, 720, 250, WHITE, eback((t - t0) / .3), n=12)
        fr.text((480, 690), "HAAR", F("black", 120), RED, anchor="mm"); fr.text((480, 790), "38 run se", F("black", 56), INK, anchor="mm")
        if t > t0 + dur * .5:
            panel(d, (100, 960, 700, 1040), YEL); fr.text((120, 968), "Record phir bhi PAKKA", F("black", 48), INK)
    elif tag == "cta":
        pass   # CTA card (reel.py) owns this scene
    d.rectangle((90, 288, 480, 346), fill=INK); fr.text((108, 292), "TRENDING TODAY", F("xb", 38), YEL)

R = Reel("Trending_20261128", "swiss", LINES, tone="bright", seed=43, tail=.35)
R.nat_speed = 1.2
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 214, 0), bg=(18, 18, 24, 225), font="xb", who_fg=(255, 214, 0))

def setup(R):
    s = R.T("nudge")
    R.nudge = dict(text="Cricket dost ko bhejo", icon="send", at=s, dur=4.5, bg=(255, 214, 0), fg=(18, 18, 24))
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="Bhejo!",
                 body="Us dost ko jo gully\ncricket mein hamesha\nNo. 11 pe aata hai", acc=(230, 40, 50))
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "nudge at", round(s, 2), f"({s / R.dur:.0%})")
    if os.environ.get("AUDIO_ONLY"): sys.exit()
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
