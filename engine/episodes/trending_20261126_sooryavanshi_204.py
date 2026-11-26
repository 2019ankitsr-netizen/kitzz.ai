"""Trending Today · Fan Buzz (Reel A) · Thu 26 Nov 2026 · "Sabse tez 200 kisne mara? 15 SAAL ke ladke ne!" — Pop Comic (Hinglish).
Vaibhav Sooryavanshi (15 y 242 d) 204* off 53 balls (7x4, 28x6) for India A v UAE, Asia Cup Rising Stars 2026 (50 overs), Doha, Tue 24 Nov 2026.
100 off 28 balls = fastest List A hundred (beat Jake Fraser-McGurk's 29). 200 off 52 balls = fastest List A double (previous: Chad Bowes, 103).
28 sixes = most in a List A innings (previous 23, D'Arcy Short). UAE 249/8; India A 254/3 in 14.2 ov, won by 7 wkts.
Semi-final v Sri Lanka A, Thu 26 Nov, 3:30 PM IST, Doha. (Outlook India 24 Nov; The Daily Star; SportsTak 25 Nov.)
Our maths: 28 x 6 = 168 runs from sixes alone. No faces/logos: original comic bursts, ball grid, bars.
Usage: python3 episodes/trending_20261126_sooryavanshi_204.py OUT_DIR
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_A", "parler:Rohit:news")

LINES = [
    Line(V, "पचास ओवर क्रिकेट में, सबसे तेज़ दो सौ किसने मारा? एक पंद्रह साल के लड़के ने!",
         "Sabse tez 200 kisne mara? 15 SAAL ke ladke ne!", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "वैभव सूर्यवंशी। इंडिया ए के लिए, यू ए ई के ख़िलाफ़, दोहा में।", "Vaibhav Sooryavanshi · India A vs UAE · Doha",
         lang="hi", tag="who", sfx="pop"),
    Line(V, "तिरेपन गेंद, दो सौ चार रन, नॉट आउट।", "53 ball · 204 run · NOT OUT", lang="hi", tag="score", sfx="hit"),
    Line(V, "सौ रन, सिर्फ़ अट्ठाईस गेंदों में। लिस्ट ए क्रिकेट का, सबसे तेज़ शतक।", "100 sirf 28 ball mein! List A ka sabse tez",
         lang="hi", tag="hundred", sfx="tick"),
    Line(V, "क्रिकेट वाले दोस्त को भेजो, असली नंबर अभी बाकी है।", "Cricket dost ko bhejo, asli number baaki hai",
         lang="hi", tag="nudge", sfx="pop"),
    Line(V, "पहले, सबसे तेज़ दो सौ, एक सौ तीन गेंदों में बना था। वैभव ने, बावन गेंदों में कर दिया।",
         "Pehle: 200 in 103 ball. Vaibhav: 52 ball!", lang="hi", tag="bars", sfx="whoosh"),
    Line(V, "यानी, आधी से भी कम गेंदें।", "Yaani AADHI se bhi kam ball!", lang="hi", tag="half", sfx="hit"),
    Line(V, "छक्के, अट्ठाईस! पिछला रिकॉर्ड था, तेईस।", "28 CHHAKKE! Pichla record: 23", lang="hi", tag="sixes", sfx="tick"),
    Line(V, "अट्ठाईस गुणा छह। यानी, एक सौ अड़सठ रन, सिर्फ़ छक्कों से।", "28 × 6 = 168 run sirf chhakkon se",
         lang="hi", tag="math", sfx="hit"),
    Line(V, "दो सौ पचास का चेज़, पंद्रह ओवर से पहले ख़त्म। और आज, सेमीफ़ाइनल, श्रीलंका ए से।",
         "250 ka chase, 15 over se pehle khatam · Aaj SEMI-FINAL vs SL A", lang="hi", tag="chase", sfx="whoosh"),
    Line(V, "उस दोस्त को भेजो, जो कहता है, पंद्रह की उम्र में, मैं भी ऐसा ही खेलता था।",
         "Us dost ko bhejo jo kehta hai \"15 mein main bhi aisa khelta tha\"", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "तो बताओ, सबसे तेज़ दो सौ, किसने मारा?", "To batao… sabse tez 200 kisne mara?", lang="hi", tag="loop", gap=.05),
]

YEL, RED, CYAN, INK, WHITE = (255, 214, 0), (230, 40, 50), (40, 190, 230), (18, 18, 24), (255, 255, 255)
PINK, GREEN, GREY, ORANGE = (255, 120, 160), (40, 170, 90), (175, 175, 182), (255, 140, 30)

def base():
    im = Image.new("RGB", (W, H), (120, 215, 255)); d = ImageDraw.Draw(im)
    for y in range(0, H, 34):            # halftone dots (sky-blue page, different from 24 Nov's yellow)
        for x in range((y // 34) % 2 * 17, W, 34):
            r = 3 + 3 * (y / H); d.ellipse((x - r, y - r, x + r, y + r), fill=(80, 185, 240))
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

def ball_grid(fr, d, t, t0, n, per=.03, hi=(), y0=560, cols=10, col=WHITE):
    """n balls in a grid; indices in hi drawn red (sixes)."""
    for i in range(n):
        if t < t0 + i * per: break
        r_, c_ = divmod(i, cols); x = 140 + c_ * 74; y = y0 + r_ * 74
        ball(d, x, y, 24, RED if i in hi else col)

def bat(d, x, y, k=1.0, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    def R(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    blade = [R(0, -30), R(220, -36), R(230, 0), R(220, 36), R(0, 30)]
    d.polygon([(a + 8, b + 10) for a, b in blade], fill=INK)
    d.polygon(blade, fill=(235, 195, 125), outline=INK, width=6)
    d.line([R(-120, 0), R(0, 0)], fill=INK, width=26); d.line([R(-115, 0), R(-5, 0)], fill=RED, width=14)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    dur = (L.t1 - L.t0) if L else 1
    if tag in ("hook", "loop"):
        h0 = 0.0 if tag == "hook" else t0
        burst(d, 480, 650, 300, YEL, eback((t - h0) / .3), rot=t * .3)
        fx.words_in(fr, t, h0, ["SABSE", "TEZ"], (300, 400), size=66, col=INK, gap=.08, font=lambda s: F("black", s))
        fx.count_up(fr, t, h0, 200, (290, 470), size=200, col=RED, dur=.35, font=lambda s: F("black", s))
        fx.slam_word(fr, t, h0 + .3, "KISNE?", (320, 770), size=84, col=INK)
        fx.verdict_pill(fr, t, h0 + .65, "15 SAAL KA LADKA!", (100, 960), size=72, bg=INK, fg=YEL)
    elif tag == "who":
        title(fr, d, "VAIBHAV SOORYAVANSHI", INK, size=60)
        k = eback((t - t0) / .35)
        panel(d, (100, 500, 900, 700), YEL, min(1, k)); fr.text((140, 520), "AGE: 15", F("black", 120), INK)
        if t > t0 + .8:
            panel(d, (100, 760, 900, 900), WHITE); fr.text((130, 780), "India A  vs  UAE", F("black", 70), INK)
        if t > t0 + 1.6:
            panel(d, (100, 940, 560, 1040), CYAN); fr.text((125, 955), "Doha · 24 Nov", F("xb", 54), INK)
    elif tag == "score":
        title(fr, d, "53 BALL", INK)
        ball_grid(fr, d, t, t0 + .1, 53, per=min(.03, dur * .6 / 53))
        if t > t0 + dur * .6:
            fx.verdict_pill(fr, t, t0 + dur * .6, "204* NOT OUT", (100, 990), size=76, bg=RED, fg=WHITE)
    elif tag == "hundred":
        title(fr, d, "100 = 28 BALL", RED)
        ball_grid(fr, d, t, t0, 28, per=.02, col=YEL)
        if t > t0 + 1.0:
            burst(d, 690, 900, 150, YEL, eback((t - t0 - 1.0) / .3), n=12)
            fr.text((690, 870), "No.1", F("black", 70), RED, anchor="mm"); fr.text((690, 935), "List A", F("xb", 42), INK, anchor="mm")
            panel(d, (100, 860, 470, 960), WHITE); fr.text((120, 872), "Sabse tez", F("black", 54), INK)
    elif tag == "nudge":
        title(fr, d, "ASLI NUMBER?", INK)
        burst(d, 480, 760, 240, PINK, 1, rot=t * .4)
        fr.text((480, 760), "???", F("black", 150), WHITE, anchor="mm")
    elif tag in ("bars", "half"):
        title(fr, d, "200 RUN: KITNI BALL?", INK, size=64)
        k1 = eout((t - t0 - .3) / .8) if tag == "bars" else 1
        L2 = R.line("bars"); k2 = eout((t - (L2.t0 + (L2.t1 - L2.t0) * .55)) / .5) if tag == "bars" else 1
        full = 760
        panel(d, (100, 560, 100 + full * k1, 680), GREY, 1); fr.text((120, 580), "Pehle: 103", F("black", 66), INK) if k1 > .5 else None
        if k2 > 0:
            panel(d, (100, 740, 100 + full * 52 / 103 * k2, 860), RED, 1)
            if k2 > .6: fr.text((120, 760), "52", F("black", 70), WHITE)
            if k2 > .9: fr.text((520, 760), "Vaibhav", F("black", 66), INK)
        if tag == "half":
            fx.verdict_pill(fr, t, t0 + .1, "AADHI SE KAM!", (100, 930), size=80, bg=INK, fg=YEL)
            d.line((100 + full / 2, 540, 100 + full / 2, 890), fill=INK, width=6)
    elif tag == "sixes":
        title(fr, d, "CHHAKKE", RED)
        ball_grid(fr, d, t, t0 + .1, 28, per=min(.05, dur * .5 / 28), hi=set(range(28)), y0=560)
        if t > t0 + dur * .55:
            panel(d, (100, 820, 560, 920), WHITE); fr.text((120, 832), "Pichla: 23", F("black", 62), INK)
            fx.verdict_pill(fr, t, t0 + dur * .55, "28!", (600, 815), size=86, bg=INK, fg=YEL)
    elif tag == "math":
        title(fr, d, "CHHAKKON KA HISAAB", INK, size=64)
        panel(d, (100, 520, 900, 700), WHITE); fr.text((140, 540), "28 × 6", F("black", 130), INK)
        if t > t0 + dur * .4:
            panel(d, (100, 740, 900, 960), YEL)
            fx.count_up(fr, t, t0 + dur * .4, 168, (140, 750), size=170, col=RED, dur=.45)
            fr.text((580, 820), "run", F("black", 80), INK)
    elif tag == "chase":
        title(fr, d, "CHASE: 250", INK)
        k = eout((t - t0) / (dur * .5))
        bat(d, 300, 700, ang=-0.6 + 0.9 * k)
        ball(d, 420 + 380 * k, 680 - 200 * math.sin(math.pi * min(1, k)), 22)
        if t > t0 + dur * .3:
            panel(d, (100, 820, 680, 920), WHITE); fr.text((120, 832), "14.2 over: KHATAM", F("black", 56), INK)
        if t > t0 + dur * .6:
            fx.verdict_pill(fr, t, t0 + dur * .6, "AAJ: SEMI-FINAL", (100, 950), size=70, bg=RED, fg=WHITE)
    elif tag == "cta":
        burst(d, 480, 640, 260, YEL, 1, rot=t * .3)
        fr.text((480, 600), "15 SAAL", F("black", 120), RED, anchor="mm"); fr.text((480, 720), "204*", F("black", 90), INK, anchor="mm")
    d.rectangle((90, 288, 480, 346), fill=INK); fr.text((108, 292), "TRENDING TODAY", F("xb", 38), YEL)

R = Reel("Trending_20261126", "swiss", LINES, tone="bright", seed=41, tail=.35)
R.nat_speed = 1.12
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 214, 0), bg=(18, 18, 24, 225), font="xb", who_fg=(255, 214, 0))

def setup(R):
    s = R.T("nudge")
    R.nudge = dict(text="Cricket dost ko bhejo", icon="send", at=s, dur=4.5, bg=(255, 214, 0), fg=(18, 18, 24))
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="Bhejo!",
                 body="Us dost ko jo kehta hai\n\"15 mein main bhi\naisa khelta tha\"", acc=(230, 40, 50))
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "nudge at", round(s, 2), f"({s / R.dur:.0%})")
    if os.environ.get("AUDIO_ONLY"): sys.exit()
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
