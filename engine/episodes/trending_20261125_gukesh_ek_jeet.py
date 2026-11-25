"""Trending Today · Fan Buzz · Wed 25 Nov 2026 · "Chess ki EK jeet = ₹1.9 crore? HAAN!" — Notebook Math style (Hinglish).
FIDE World Chess Championship 2026, Gukesh D (20, IND, defending champion) vs Javokhir Sindarov (20, UZB, Candidates 2026 winner),
Fondation Martin Bodmer, Cologny/Geneva, 24 Nov - 12 Dec. 14 classical games, first to 7.5 points. Prize fund $2.5M;
$200,000 to a player for each game won, rest shared (Wikipedia / Business Standard 24 Nov / WorldChess 22 Nov).
Ratings: Sindarov 2782, world No. 4; Gukesh ~2710, No. 26 (Business Standard, ESPN 22 Nov).
Game 1 (24 Nov): draw, Berlin; Gukesh with Black held under time pressure (ChessBase India, ANI 25 Nov).
Game 2: Wed 25 Nov, 7:30 PM IST, Gukesh White (colours alternate). Our maths: $200,000 x ~₹94 (RBI-ref ~94, Nov 2026) ≈ ₹1.88 cr.
Usage: python3 episodes/trending_20261125_gukesh_ek_jeet.py OUT_DIR
"""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFont
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_A", "parler:Rohit:news")
HAND = "/home/claude/gfonts/ofl/hind/Hind-SemiBold.ttf"

LINES = [
    Line(V, "शतरंज की एक जीत, करीब एक करोड़ नब्बे लाख? हाँ!", "Chess ki EK jeet = ~₹1.9 crore? HAAN!", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "गुकेश, बीस साल के वर्ल्ड चैंपियन, अपना ताज बचाने उतरे हैं, जिनेवा में।",
         "Gukesh, 20 saal, World Champion: taj bachane Geneva mein", lang="hi", tag="who", sfx="pop"),
    Line(V, "सामने हैं उज़्बेकिस्तान के सिंदारोव, वो भी बीस साल के।", "Saamne: Uzbekistan ke Sindarov, wo bhi 20 ke", lang="hi", tag="vs", sfx="tick"),
    Line(V, "ट्विस्ट! रेटिंग में सिंदारोव आगे, दुनिया में नंबर चार। गुकेश छब्बीसवें।",
         "Twist! Rating mein Sindarov aage: World No. 4. Gukesh 26th", lang="hi", tag="twist", sfx="hit"),
    Line(V, "शतरंज वाले दोस्त को भेजो, आज रात गेम है।", "Chess wale dost ko bhejo, aaj raat game hai", lang="hi", tag="nudge", sfx="pop"),
    Line(V, "चौदह गेम। जीत का एक पॉइंट, ड्रॉ का आधा। साढ़े सात पॉइंट, और ताज तुम्हारा।",
         "14 game. Jeet = 1, draw = ½. 7.5 point = taj", lang="hi", tag="format", sfx="tick"),
    Line(V, "इनाम, कुल ढाई मिलियन डॉलर। और हर जीते गेम के, दो लाख डॉलर अलग।",
         "Inaam: $2.5 million. Har jeete game ke $200,000 alag", lang="hi", tag="prize", sfx="tick"),
    Line(V, "दो लाख डॉलर, गुणा चौरानवे रुपये। यानी एक जीत, करीब एक करोड़ अट्ठासी लाख!",
         "$200,000 × ₹94 = ~₹1.88 crore, ek jeet!", lang="hi", tag="math", sfx="hit"),
    Line(V, "कल पहला गेम, ड्रॉ। काले मोहरों से, टाइम प्रेशर में भी, गुकेश ने गेम बचा लिया।",
         "Kal Game 1: DRAW. Kale mohron se Gukesh ne bacha liya", lang="hi", tag="g1", sfx="tick"),
    Line(V, "आज गेम दो, शाम साढ़े सात बजे। सफ़ेद मोहरे, गुकेश के पास।", "Aaj Game 2: shaam 7:30 baje. Safed mohre Gukesh ke paas",
         lang="hi", tag="g2", sfx="whoosh"),
    Line(V, "उस दोस्त को भेजो, जो कहता है, चेस में पैसा नहीं है।", "Us dost ko bhejo jo kehta hai \"chess mein paisa nahi\"",
         lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "तो बताओ, शतरंज की एक जीत, कितने की?", "To batao… chess ki EK jeet, kitne ki?", lang="hi", tag="loop", gap=.05),
]

PAPER, LINE_C, MARGIN = (250, 248, 238), (190, 214, 236), (236, 150, 150)
INK, BLUE, RED, GREEN, HL = (28, 32, 48), (30, 70, 170), (210, 40, 40), (30, 130, 80), (255, 232, 90)

def base():
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    for y in range(120, H, 58): d.line((0, y, W, y), fill=LINE_C, width=2)
    d.line((70, 0, 70, H), fill=MARGIN, width=3)
    r = random.Random(5)
    for _ in range(900): x, y = r.randint(0, W), r.randint(0, H); d.point((x, y), fill=(232, 228, 214))
    return im
BASE = base()

def hand(s): return ImageFont.truetype(HAND, s)
def blk(s): return F("black", s)

def underline(d, t, t0, x0, x1, y, col=RED, w=8, dur=.35):
    if t < t0: return
    k = eout((t - t0) / dur); pts = [(x0 + (x1 - x0) * i / 20, y + math.sin(i * .9) * 4) for i in range(int(20 * k) + 1)]
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")

def board(d, x, y, s, k=1.0):
    """hand-drawn 8x8 board, squares appear row by row (k 0..1)"""
    c = s / 8; n = int(64 * k)
    for i in range(n):
        r, q = divmod(i, 8)
        if (r + q) % 2: d.rectangle((x + q * c, y + r * c, x + (q + 1) * c, y + (r + 1) * c), fill=(120, 132, 160))
    d.rectangle((x, y, x + s, y + s), outline=INK, width=5)

def king(d, cx, cy, s, fill, out=INK):
    """simple original king silhouette: base, body, cross"""
    d.rounded_rectangle((cx - s * .55, cy + s * .55, cx + s * .55, cy + s * .75), 6, fill=fill, outline=out, width=4)
    d.polygon([(cx - s * .38, cy + s * .55), (cx - s * .25, cy - s * .25), (cx + s * .25, cy - s * .25), (cx + s * .38, cy + s * .55)], fill=fill, outline=out)
    d.line([(cx - s * .38, cy + s * .55), (cx - s * .25, cy - s * .25), (cx + s * .25, cy - s * .25), (cx + s * .38, cy + s * .55)], fill=out, width=4)
    d.ellipse((cx - s * .3, cy - s * .45, cx + s * .3, cy - s * .15), fill=fill, outline=out, width=4)
    d.line((cx, cy - s * .8, cx, cy - s * .45), fill=out, width=6); d.line((cx - s * .14, cy - s * .65, cx + s * .14, cy - s * .65), fill=out, width=6)

def tag_strip(fr, d):
    d.rounded_rectangle((90, 288, 520, 344), 14, fill=INK)
    fr.text((110, 292), "TRENDING TODAY", F("xb", 38), HL)

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    dur = (L.t1 - L.t0) if L else 1
    tag_strip(fr, d)
    if tag in ("hook", "loop"):
        h0 = t0 if tag == "loop" else 0.0
        fx.words_in(fr, t, h0, ["Chess", "ki", "EK", "jeet"], (100, 380), size=104, col=INK, gap=.08)
        if t > h0 + .1:
            k = eout((t - h0 - .1) / .35); v = 1.9 * k
            fr.text((100, 500), f"₹{v:.1f}", blk(230), RED); fr.text((640, 600), "crore?", blk(96), RED)
        fx.verdict_pill(fr, t, h0 + .6, "HAAN!", (100, 790), size=120, bg=GREEN)
        if t > h0 + 1.2: king(d, 760, 900, 120, (255, 255, 255))
    elif tag in ("who", "vs"):
        fr.text((100, 370), "World Chess Championship", hand(60), INK); underline(d, t, t0, 100, 820, 455)
        king(d, 270, 640, 140, (255, 255, 255))
        fr.text((270, 820), "Gukesh", blk(64), BLUE, anchor="ma"); fr.text((270, 900), "20 · India", hand(46), INK, anchor="ma")
        fr.text((270, 958), "Champion", hand(46), GREEN, anchor="ma")
        if tag == "vs":
            fr.text((500, 600), "vs", blk(80), RED, anchor="mm")
            king(d, 730, 640, 140, (60, 60, 70), out=INK)
            fr.text((730, 820), "Sindarov", blk(64), RED, anchor="ma"); fr.text((730, 900), "20 · Uzbekistan", hand(42), INK, anchor="ma")
        else:
            fr.text((560, 560), "Geneva", hand(70), RED); fr.text((560, 650), "24 Nov – 12 Dec", hand(52), INK)
    elif tag in ("twist", "nudge"):
        fr.text((100, 370), "Rating ka twist", hand(76), INK); underline(d, t, t0, 100, 600, 470)
        rows = [("Sindarov", "World No. 4", RED, 2782), ("Gukesh", "No. 26", BLUE, 2710)]
        for i, (n, rk, col, rt) in enumerate(rows):
            if tag == "twist" and t < t0 + .3 + i * 1.1: continue
            y = 520 + i * 180
            fr.text((110, y), n, blk(70), col); fr.text((110, y + 84), rk, hand(52), INK)
            fr.text((560, y + 10), str(rt), blk(90), col)
        if tag == "nudge" or t > t0 + dur * .75:
            fx.verdict_pill(fr, t, t0 + (dur * .75 if tag == "twist" else -1), "Champion = underdog!", (100, 900), size=64, bg=INK)
    elif tag == "format":
        fr.text((100, 370), "Kaise jeetein?", hand(76), INK); underline(d, t, t0, 100, 560, 470)
        board(d, 110, 510, 320, eout((t - t0) / .8))
        items = [("14 game", INK, .3), ("Jeet = 1", GREEN, 1.2), ("Draw = ½", BLUE, 2.0), ("7.5 = TAJ", RED, 3.0)]
        for i, (s, col, dl) in enumerate(items):
            if t > t0 + dl: fr.text((480, 510 + i * 88), s, blk(68), col)
    elif tag in ("prize", "math"):
        fr.text((100, 370), "Ab paise ki maths", hand(76), INK); underline(d, t, t0, 100, 700, 470)
        fr.text((110, 500), "Kul inaam: $2.5M", blk(72), INK)
        if tag == "math" or t > t0 + dur * .5: fr.text((110, 600), "Har jeet: $200,000", blk(72), GREEN)
        if tag == "math":
            fr.text((140, 720), "$200,000 × ₹94", blk(80), BLUE)
            d.line((130, 830, 860, 830), fill=INK, width=8)
            k = eout((t - t0 - dur * .5) / .5)
            if k > 0: fr.text((140, 850), f"≈ ₹{1.88 * k:.2f} crore", blk(96), RED)
    elif tag in ("g1", "g2"):
        fr.text((100, 370), "Score", hand(76), INK); underline(d, t, t0, 100, 330, 470)
        fr.text((110, 500), "Game 1: DRAW", blk(80), BLUE)
        fr.text((110, 600), "½ – ½", blk(110), INK)
        if tag == "g1" and t > t0 + 1.5: fr.text((520, 625), "Gukesh (Black)\nne bachaya", hand(46), INK)
        if tag == "g2":
            d.rounded_rectangle((100, 760, 900, 900), 26, fill=HL, outline=INK, width=5)
            fr.text((130, 775), "AAJ Game 2 · 7:30 PM", blk(64), INK)
            king(d, 820, 980, 90, (255, 255, 255))
            fr.text((110, 925), "Safed: Gukesh", hand(60), INK)
    elif tag == "cta":
        fr.text((100, 370), "Chess mein paisa?", hand(76), INK); underline(d, t, t0, 100, 700, 470)
        pass

for _L in LINES:
    if _L.gap > .2: _L.gap = .2
R = Reel("Trending_20261125", "swiss", LINES, tone="bright", seed=31, tail=.35)
R.nat_speed = 1.15
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(20, 24, 40, 220), font="xb", who_fg=(255, 210, 60))

def setup(R):
    s = R.T("nudge")
    R.nudge = dict(text="Chess dost ko bhejo", icon="send", at=s, dur=4.5, bg=(255, 232, 90), fg=(20, 20, 30))
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="Bhejo!", body="Us dost ko jo kehta\nhai chess mein\npaisa nahi",
                 acc=(210, 40, 40))
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "nudge at", round(s, 2), f"({s / R.dur:.0%})")
    if os.environ.get("AUDIO_ONLY"): sys.exit()
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
