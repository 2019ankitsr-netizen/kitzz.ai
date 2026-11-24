"""Trending Today · Fan Buzz · Tue 24 Nov 2026 · "720 RUN! Phir bhi jeet nahi? Kyun?" — Pop Comic style (Hinglish).
NZ v India, 1st Test, Basin Reserve, Wellington, 19-23 Nov 2026: NZ 368 & 239/5; India 720/9 d. Drawn (captains shook hands in the final hour).
720/9 d = highest Test total in New Zealand (beat NZ's 715/6 d v Bangladesh, Hamilton 2019) and highest by a visiting side at the
Basin Reserve (beat West Indies 660/5 d, Feb 1995). KL Rahul 136, Pant 128. Mitchell 49* off 186 balls on day 5. 2nd Test 27 Nov, Christchurch.
(CricTracker 22 Nov, CREX 22 Nov, NationPath 23 Nov, NewsBytes 23 Nov, NewsWire NZ 24 Nov.) Our maths: 368+720+239 = 1,327 runs, 10+9+5 = 24 wickets.
Usage: python3 episodes/trending_20261124_720_draw.py OUT_DIR
"""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_A", "parler:Rohit:news")

LINES = [
    Line(V, "सात सौ बीस रन! फिर भी इंडिया जीता नहीं? क्यों?", "720 RUN! Phir bhi jeet nahi? Kyun?", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "न्यूज़ीलैंड में किसी भी टीम का, सबसे बड़ा टेस्ट स्कोर। बेसिन रिज़र्व का इकत्तीस साल पुराना रिकॉर्ड भी टूटा।",
         "NZ mein sabse bada Test score! 31 saal purana record toota", lang="hi", tag="record", sfx="hit"),
    Line(V, "राहुल एक सौ छत्तीस, पंत एक सौ अट्ठाईस।", "Rahul 136 · Pant 128", lang="hi", tag="names", sfx="pop"),
    Line(V, "पर टेस्ट रन से नहीं जीतते। जीतने के लिए, बीस विकेट चाहिए।", "Par Test runs se nahi jeette. Chahiye 20 WICKET", lang="hi", tag="rule", sfx="tick"),
    Line(V, "क्रिकेट वाले दोस्त को भेजो, असली हिसाब अभी बाकी है।", "Cricket dost ko bhejo, asli hisaab baaki hai", lang="hi", tag="nudge", sfx="pop"),
    Line(V, "न्यूज़ीलैंड पहली पारी में, तीन सौ अड़सठ पर ऑल आउट। दस विकेट।", "NZ 1st innings: 368 all out = 10 wicket", lang="hi", tag="nz1", sfx="tick"),
    Line(V, "आख़िरी दिन, दूसरी पारी में, बस पाँच विकेट गिरे।", "Last day, 2nd innings: sirf 5 wicket", lang="hi", tag="nz2", sfx="tick"),
    Line(V, "मिचेल ने एक सौ छियासी गेंदें खेलीं, उनचास नॉट आउट। दीवार बन गए।", "Mitchell: 186 ball, 49 not out. Deewar!", lang="hi", tag="wall", sfx="whoosh"),
    Line(V, "पंद्रह विकेट मिले, चाहिए थे बीस। पाँच कम, तो मैच ड्रॉ।", "Mile 15, chahiye the 20. Paanch kam = DRAW", lang="hi", tag="miss", sfx="hit"),
    Line(V, "पाँच दिन, तेरह सौ सत्ताईस रन, और गिरे सिर्फ़ चौबीस विकेट।", "5 din · 1,327 run · sirf 24 wicket", lang="hi", tag="total", sfx="tick"),
    Line(V, "उस दोस्त को भेजो, जो बोलता है, ज़्यादा रन मतलब जीत पक्की।", "Us dost ko bhejo jo bolta hai \"zyada run = jeet pakki\"",
         lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "तो बताओ, सात सौ बीस रन, फिर भी जीत क्यों नहीं?", "To batao… 720 run, phir bhi jeet kyun nahi?", lang="hi", tag="loop", gap=.05),
]

YEL, RED, CYAN, INK, WHITE = (255, 214, 0), (230, 40, 50), (40, 190, 230), (18, 18, 24), (255, 255, 255)
PINK, GREEN, GREY = (255, 120, 160), (40, 170, 90), (175, 175, 182)

def base():
    im = Image.new("RGB", (W, H), (255, 236, 120)); d = ImageDraw.Draw(im)
    for y in range(0, H, 34):            # halftone dots
        for x in range((y // 34) % 2 * 17, W, 34):
            r = 3 + 3 * (y / H); d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 200, 60))
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
    x0, y0, x1, y1 = box; x1 = x0 + (x1 - x0) * k
    d.rectangle((x0 + 10, y0 + 12, x1 + 10, y1 + 12), fill=INK)
    d.rectangle((x0, y0, x1, y1), fill=col, outline=INK, width=7)

def stumps(d, x, y, out=False, k=1.0, col=None):
    """One wicket icon: 3 stumps + bails. out = knocked (tilted, red)."""
    c = col or (RED if out else WHITE)
    for i in range(3):
        sx = x + i * 22; tilt = (i - 1) * 22 * k if out else 0
        d.line((sx, y + 120, sx + tilt, y), fill=INK, width=15); d.line((sx, y + 118, sx + tilt, y + 3), fill=c, width=8)
    by = y - 8 - (26 * k if out else 0)
    d.line((x - 6, by, x + 50, by + (12 * k if out else 0)), fill=INK, width=9)

def wicket_grid(fr, d, t, fallen, new_from=0, t_new=0, per=.12):
    """20 wickets in 2 rows of 10. First `fallen` are out; those from new_from fall one by one from t_new."""
    for i in range(20):
        r, c = divmod(i, 10); x = 112 + c * 78; y = 580 + r * 200
        if i < new_from: stumps(d, x, y, True)
        elif i < fallen:
            k = (t - (t_new + (i - new_from) * per)) / .2
            stumps(d, x, y, k > 0, max(0, min(1, k)))
        else: stumps(d, x, y, False, col=WHITE)

def title(fr, d, text, col=INK, y=372, size=78, bg=WHITE):
    f = F("black", size); w = fr.d.textlength(text, font=f)
    panel(d, (90, y, 90 + w + 50, y + size + 34), bg)
    fr.text((115, y + 10), text, f, col)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    dur = (L.t1 - L.t0) if L else 1
    if tag in ("hook", "loop"):
        h0 = 0.0 if tag == "hook" else t0
        burst(d, 480, 640, 290, RED, eback((t - h0) / .3), rot=t * .3)
        fx.count_up(fr, t, h0, 720, (225, 500), size=230, col=WHITE, dur=.35, font=lambda s: F("black", s))
        fx.slam_word(fr, t, h0 + .25, "RUN!", (350, 740), size=100, col=YEL)
        fx.verdict_pill(fr, t, h0 + .6, "JEET NAHI?", (110, 930), size=88, bg=INK, fg=YEL)
    elif tag in ("score", "record"):
        panel(d, (100, 380, 900, 720), WHITE, eout((t - t0) / .25) if tag == "score" else 1)
        if tag == "record" or t > t0 + .2:
            fr.text((140, 400), "INDIA", F("black", 90), INK); fr.text((140, 500), "720/9 d", F("black", 150), RED)
        if tag == "score" and t > t0 + 1.2: fr.text((140, 660), "Basin Reserve, Wellington", F("xb", 40), INK) if False else None
        if tag == "score" and t > t0 + 1.0:
            panel(d, (100, 760, 900, 900), CYAN); fr.text((130, 778), "NZ: 368  &  239/5", F("black", 72), INK)
        if tag == "record":
            k = eback((t - t0) / .3); burst(d, 660, 930, 185, YEL, k, n=12)
            if k > .9: fr.text((660, 885), "31 SAAL", F("black", 76), RED, anchor="mm"); fr.text((660, 950), "record toota", F("xb", 44), INK, anchor="mm")
            if t > t0 + 1.6:
                panel(d, (100, 760, 400, 1000), WHITE); fr.text((125, 780), "NZ mein", F("xb", 42), INK)
                fr.text((125, 830), "No.1", F("black", 96), RED); fr.text((125, 940), "Test score", F("xb", 36), INK)
    elif tag == "names":
        for i, (n, s, col) in enumerate([("RAHUL", "136", CYAN), ("PANT", "128", PINK)]):
            a = t - (t0 + i * .5)
            if a < 0: continue
            k = eback(a / .3); x = 100 + i * 410
            panel(d, (x, 400 + (1 - k) * 200, x + 380, 880 + (1 - k) * 200), col)
            fr.text((x + 190, 470 + (1 - k) * 200), n, F("black", 72), INK, anchor="mm")
            fr.text((x + 190, 640 + (1 - k) * 200), s, F("black", 170), WHITE, anchor="mm")
            # simple bat
            bx, by = x + 150, 760 + (1 - k) * 200
            d.rounded_rectangle((bx, by, bx + 80, by + 34), 10, fill=(230, 190, 120), outline=INK, width=5)
            d.rectangle((bx - 70, by + 10, bx, by + 24), fill=INK)
    elif tag in ("rule", "nudge", "nz1", "nz2", "wall", "miss"):
        if tag == "rule":
            title(fr, d, "JEET = 20 WICKET", RED)
            wicket_grid(fr, d, t, 0)
            if t > t0 + 1.0: fr.text((110, 960), "Runs se nahi!", F("black", 66), INK)
        elif tag == "nudge":
            title(fr, d, "Chahiye: 20", INK); wicket_grid(fr, d, t, 0)
        elif tag == "nz1":
            title(fr, d, "NZ 368 all out", INK); wicket_grid(fr, d, t, 10, 0, t0 + .4)
            if t > t0 + 1.8: fr.text((110, 935), "10 wicket", F("black", 72), RED)
        elif tag == "nz2":
            title(fr, d, "Last day: 239/5", INK); wicket_grid(fr, d, t, 15, 10, t0 + .5, per=.25)
            if t > t0 + 1.8: fr.text((110, 935), "+5 = 15", F("black", 72), RED)
        elif tag == "wall":
            title(fr, d, "MITCHELL 49*", INK)
            k = eout((t - t0) / max(.6, dur * .6))
            for r in range(6):                   # brick wall builds up
                for c in range(7):
                    i = r * 7 + c
                    if i > k * 42: break
                    x = 110 + c * 112 + (56 if r % 2 else 0); y = 920 - r * 66
                    if x + 104 > 900: continue
                    d.rectangle((x, y, x + 104, y + 58), fill=(205, 85, 60), outline=INK, width=5)
            if t > t0 + 1.0: panel(d, (520, 980, 900, 1045), WHITE); fr.text((540, 984), "186 ball", F("black", 50), INK)
        else:  # miss
            title(fr, d, "15 / 20", RED); wicket_grid(fr, d, t, 15, 15)
            for i in range(15, 20):
                r, c = divmod(i, 10); x = 112 + c * 78; y = 580 + r * 200
                d.ellipse((x - 14, y - 40, x + 60, y + 135), outline=RED, width=6)
            fx.verdict_pill(fr, t, t0 + 1.4, "5 KAM = DRAW", (110, 935), size=76, bg=INK, fg=YEL)
    elif tag == "total":
        title(fr, d, "5 DIN KA HISAAB", INK)
        items = [("1,327", "run", CYAN, 1327, "{:,}"), ("24", "wicket", PINK, 24, "{}")]
        for i, (s, lab, col, v, fm) in enumerate(items):
            a0 = t0 + .5 + i * dur * .35
            if t < a0: continue
            y = 520 + i * 250; panel(d, (100, y, 900, y + 210), col)
            fx.count_up(fr, t, a0, v, (140, y + 20), size=150, col=WHITE if i else INK, dur=.45, fmt=fm)
            fr.text((620, y + 70), lab, F("black", 72), INK)
    elif tag == "next":
        burst(d, 480, 680, 330, CYAN, eback((t - t0) / .3), n=12)
        if t > t0 + .25:
            fr.text((480, 600), "27 NOV", F("black", 110), INK, anchor="mm"); fr.text((480, 710), "Christchurch", F("black", 58), INK, anchor="mm")
            fr.text((480, 790), "Agla Test", F("xb", 48), RED, anchor="mm")
    elif tag == "cta":
        burst(d, 480, 640, 260, RED, 1, rot=t * .3)
        fr.text((480, 600), "720", F("black", 170), WHITE, anchor="mm"); fr.text((480, 730), "= DRAW?!", F("black", 70), YEL, anchor="mm")
    d.rectangle((90, 288, 480, 346), fill=INK); fr.text((108, 292), "TRENDING TODAY", F("xb", 38), YEL)

R = Reel("Trending_20261124", "swiss", LINES, tone="bright", seed=31, tail=.35)
R.nat_speed = 1.12
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 214, 0), bg=(18, 18, 24, 225), font="xb", who_fg=(255, 214, 0))

def setup(R):
    s = R.T("nudge")
    R.nudge = dict(text="Cricket dost ko bhejo", icon="send", at=s, dur=4.5, bg=(255, 214, 0), fg=(18, 18, 24))
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="Bhejo!", body="Us dost ko jo bolta hai\n\"zyada run =\njeet pakki\"",
                 acc=(230, 40, 50))
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "nudge at", round(s, 2), f"({s / R.dur:.0%})")
    if os.environ.get("AUDIO_ONLY"): sys.exit()
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
