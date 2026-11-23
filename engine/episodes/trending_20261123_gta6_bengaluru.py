"""Trending Today · Fan Buzz · Mon 23 Nov 2026 · "GTA 6 kisne banaya? Sirf America ne? NAHI!" — Notebook Math style (Hinglish).
Rockstar India's Bengaluru (Whitefield) studio: 1,600+ developers worked on GTA 6 (open world, environments, assets, Leonida).
Studio began as Dhruva Interactive (Bengaluru, 1995), acquired by Rockstar in 2019 (Oneindia, NewsBytes 19 Nov 2026).
Sensor Tower estimate: ~17 million copies by 18 Nov (Oneindia / GGRecon 19 Nov). Our maths: 17,000,000 / 1,600 ≈ 10,600.
Usage: python3 episodes/trending_20261123_gta6_bengaluru.py OUT_DIR
"""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFont
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_A", "parler:Rohit:news")
FB = "/home/claude/gfonts/ofl/hind/Hind-Bold.ttf"
HAND = "/home/claude/gfonts/ofl/hind/Hind-SemiBold.ttf"

LINES = [
    Line(V, "जी टी ए सिक्स किसने बनाया? सिर्फ़ अमेरिका ने? नहीं!", "GTA 6 kisne banaya? Sirf America ne? NAHI!", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "बेंगलुरु के व्हाइटफ़ील्ड में, सोलह सौ से ज़्यादा लोगों ने इस गेम पर काम किया।",
         "Bengaluru (Whitefield) mein 1,600+ log is game par lage", lang="hi", tag="dots", sfx="pop"),
    Line(V, "ये रॉकस्टार इंडिया का स्टूडियो है, जो उन्नीस सौ पचानवे में ध्रुवा इंटरैक्टिव नाम से शुरू हुआ।",
         "Rockstar India ka studio: 1995 mein Dhruva Interactive naam se shuru", lang="hi", tag="history", sfx="tick"),
    Line(V, "दो हज़ार उन्नीस में रॉकस्टार ने ख़रीदा।", "2019 mein Rockstar ne khareeda", lang="hi", tag="bought", sfx="tick"),
    Line(V, "गेमर दोस्त को भेजो, अभी मैथ्स बाकी है।", "Gamer dost ko bhejo, abhi maths baaki hai", lang="hi", tag="nudge", sfx="pop"),
    Line(V, "इन्होंने खुली दुनिया बनाई, इमारतें, सड़कें, लियोनिडा के इलाक़े।",
         "Inhone banayi open world: buildings, sadkein, Leonida ke ilaake", lang="hi", tag="world", sfx="whoosh"),
    Line(V, "सेंसर टावर के अंदाज़े से, सत्रह मिलियन कॉपियाँ बिक चुकी हैं।",
         "Sensor Tower ka andaaza: 17 million copies bik chuki", lang="hi", tag="sales", sfx="tick"),
    Line(V, "सत्रह मिलियन भाग सोलह सौ। हर बेंगलुरु डेवलपर के हिस्से, करीब दस हज़ार छह सौ कॉपियाँ!",
         "17,000,000 ÷ 1,600 = ~10,600 copies har Bengaluru dev ke hisse!", lang="hi", tag="math", sfx="hit"),
    Line(V, "जिस सड़क पर आप गाड़ी चला रहे हो, शायद बेंगलुरु में बनी है।",
         "Jis sadak par gaadi chala rahe ho, shayad Bengaluru mein bani", lang="hi", tag="road"),
    Line(V, "उस गेमर दोस्त को भेजो, जो कहता है इंडिया में गेम नहीं बनते।", "Us gamer dost ko bhejo jo kehta hai \"India mein games nahi bante\"",
         lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "अब बताओ, जी टी ए सिक्स किसने बनाया?", "Ab batao… GTA 6 kisne banaya?", lang="hi", tag="loop", gap=.05),
]

PAPER, LINE_C, MARGIN = (250, 248, 238), (190, 214, 236), (236, 150, 150)
INK, BLUE, RED, GREEN, HL = (28, 32, 48), (30, 70, 170), (210, 40, 40), (30, 130, 80), (255, 232, 90)

def base():
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    for y in range(120, H, 58): d.line((0, y, W, y), fill=LINE_C, width=2)
    d.line((70, 0, 70, H), fill=MARGIN, width=3)
    r = random.Random(3)
    for _ in range(900): x, y = r.randint(0, W), r.randint(0, H); d.point((x, y), fill=(232, 228, 214))
    return im
BASE = base()

def hand(s): return ImageFont.truetype(HAND, s)
def blk(s): return F("black", s)

def underline(d, t, t0, x0, x1, y, col=RED, w=8, dur=.35):
    if t < t0: return
    k = eout((t - t0) / dur); pts = [(x0 + (x1 - x0) * i / 20, y + math.sin(i * .9) * 4) for i in range(int(20 * k) + 1)]
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint="curve")

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
        fx.words_in(fr, t, h0, ["GTA 6", "kisne"], (100, 380), size=120, col=INK, gap=.1)
        fx.words_in(fr, t, h0 + .2, ["banaya?"], (100, 510), size=120, col=INK)
        a0 = h0 + .45
        if t > a0:
            fx.slam_word(fr, t, a0, "Sirf America?", (120, 660), size=92, col=BLUE)
            fx.strike(d, t, a0 + .35, (115, 718), (740, 703), col=RED, width=18)
        fx.verdict_pill(fr, t, a0 + .55, "NAHI!", (100, 800), size=120, bg=RED)
        if tag == "hook" and t > 1.6:
            fr.text((520, 805), "1,600+ log", blk(76), GREEN)
            fr.text((520, 895), "Bengaluru se", hand(60), INK)
    elif tag == "dots":
        # 1,600 people = 40 x 40 dots, filling row by row
        n = int(1600 * eout((t - t0 - .2) / max(.5, dur - .4)))
        for i in range(n):
            r, c = divmod(i, 40); x = 120 + c * 19; y = 500 + r * 12
            d.ellipse((x, y, x + 12, y + 9), fill=BLUE if i % 97 else RED)
        fx.count_up(fr, t, t0, 1600, (100, 370), size=130, col=INK, dur=max(.5, dur * .6), fmt="{:,}+", font=blk)
        fr.text((620, 400), "log", hand(80), INK)
        fr.text((120, 985), "Bengaluru · Whitefield", hand(56), RED)
    elif tag in ("history", "bought"):
        fr.text((100, 370), "Studio ki kahani", hand(76), INK); underline(d, t, t0, 100, 640, 470)
        d.line((140, 640, 880, 640), fill=INK, width=6)
        pts = [(230, "1995", "Dhruva\nInteractive"), (520, "2019", "Rockstar ne\nkhareeda"), (850, "2026", "GTA 6")]
        for i, (x, yr, lab) in enumerate(pts):
            tt = t0 + i * .9 if tag == "history" else 0
            show = (tag == "bought") or t > tt or i == 0
            if tag == "history" and i == 2: show = False
            if tag == "history" and i == 1: show = t > t0 + dur * .85
            if not show: continue
            d.ellipse((x - 18, 622, x + 18, 658), fill=RED if i == 1 else BLUE)
            fr.text((x, 560), yr, blk(64), INK, anchor="mm")
            fr.text((x, 690), lab, hand(48), INK, anchor="ma", spacing=0) if x < 800 else fr.text((x - 10, 690), lab, hand(48), INK, anchor="ra")
    elif tag in ("nudge", "world"):
        fr.text((100, 370), "Inhone kya banaya?", hand(76), INK); underline(d, t, t0, 100, 720, 470)
        # simple sketched city block: buildings + road
        k = eout((t - t0) / max(.6, dur * .8)) if tag == "world" else .25
        blds = [(110, 900, 130, 330), (255, 900, 110, 250), (380, 900, 150, 400), (545, 900, 120, 290), (680, 900, 170, 360)]
        for i, (x, yb, w, h) in enumerate(blds):
            kk = min(1, max(0, k * len(blds) - i))
            if kk <= 0: continue
            hh = h * kk; d.rectangle((x, yb - hh, x + w, yb), outline=INK, width=5, fill=(222, 230, 245))
            for wy in range(int(yb - hh) + 24, yb - 20, 44):
                for wx in range(x + 18, x + w - 18, 34): d.rectangle((wx, wy, wx + 16, wy + 20), fill=HL)
        if k > .5:
            d.polygon([(100, 905), (870, 905), (890, 1040), (80, 1040)], fill=(110, 112, 120))
            for x in range(140, 850, 110): d.rectangle((x, 965, x + 60, 980), fill=(255, 255, 255))
            fr.text((100, 1010), "open world · buildings · sadkein", hand(48), INK) if False else None
    elif tag == "sales":
        fr.text((100, 370), "Sensor Tower ka andaaza", hand(64), INK); underline(d, t, t0, 100, 760, 455)
        fx.count_up(fr, t, t0 + .2, 17, (100, 520), size=260, col=RED, dur=.45, fmt="{}M")
        fr.text((110, 830), "copies, 18 Nov tak", hand(64), INK)
    elif tag in ("math", "road"):
        fr.text((100, 370), "Ab maths", hand(76), INK); underline(d, t, t0, 100, 420, 470)
        rows = [("17,000,000", INK), ("÷   1,600", BLUE)]
        for i, (s, col) in enumerate(rows):
            if tag == "road" or t > t0 + i * .7: fr.text((140, 500 + i * 110), s, blk(96), col)
        if tag == "road" or t > t0 + 1.6: d.line((130, 730, 820, 730), fill=INK, width=8)
        if tag == "road" or t > t0 + dur * .55:
            fx.count_up(fr, t, (t0 + dur * .55) if tag == "math" else 0, 10600, (140, 750), size=128, col=GREEN, dur=.6, fmt="≈{:,}")
        if tag == "road": fr.text((140, 900), "copies har dev ke hisse", hand(56), INK)

R = Reel("Trending_20261123", "xray", LINES, tone="bright", seed=19, tail=.35)
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(20, 24, 40, 220), font="xb", who_fg=(255, 210, 60))

def setup(R):
    s = R.T("nudge")
    R.nudge = dict(text="Gamer dost ko bhejo", icon="send", at=s, dur=4.5, bg=(255, 232, 90), fg=(20, 20, 30))
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="send", head="Bhejo!", body="Us gamer dost ko jo\nkehta hai India mein\ngames nahi bante",
                 acc=(210, 40, 40))
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "nudge at", round(s, 2), f"({s / R.dur:.0%})")
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
