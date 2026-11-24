"""Trending Today · Fan Buzz follow-up · Tue 24 Nov 2026 · "GTA 6 mein Indian easter egg? Humne check kiya" — Fact-check desk style (Hinglish).
Follow-up to trending_20261123_gta6_bengaluru (reel DgFacfEhg0n), built from a follower comment claiming an Indian dev put his name
on a pizza shop ("Soham Plaza").
Checked 24 Nov 2026: not in vicecitydb.org (52), gta6wiki.eu (72) or gtaside.com (14) easter-egg lists; gtaside: Rockstar has confirmed none.
Official credits (rockstargames.com/VI/credits): no "Soham"; South Asian names credited incl. Senior Lead / Lead Animator in Ambient World
Animation, a Lead Animator in Face Animation and an Animation Director. No individual names are shown on screen.
Usage: python3 episodes/trending_20261124_gta6_easter_egg_factcheck.py OUT_DIR
"""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reel import Reel, Line, F, ease, eout, eback, W, H
import fx

V = os.environ.get("KITZZ_VOICE_A", "parler:Rohit:news")

LINES = [
    Line(V, "जी टी ए सिक्स में इंडियन ईस्टर एग? हमने चेक किया।", "GTA 6 mein Indian easter egg? Humne check kiya", lang="hi", tag="hook", sfx="hit", gap=.2),
    Line(V, "एक फ़ॉलोअर ने कमेंट किया, कि एक इंडियन डेवलपर ने पिज़्ज़ा शॉप पर अपना नाम डाला। सोहम प्लाज़ा।",
         "Follower ka comment: ek Indian dev ne pizza shop pe apna naam daala, \"Soham Plaza\"", lang="hi", tag="claim", sfx="pop"),
    Line(V, "हमने तीन बड़ी ईस्टर एग लिस्ट देखीं। बावन, बहत्तर, और चौदह सीक्रेट्स वाली।",
         "Humne 3 badi easter egg lists dekhi: 52, 72 aur 14 secrets", lang="hi", tag="check", sfx="tick"),
    Line(V, "सोहम प्लाज़ा? कहीं नहीं मिला। ऑफ़िशियल क्रेडिट्स में, सोहम नाम भी नहीं।",
         "\"Soham Plaza\"? Kahin nahi mila. Credits mein \"Soham\" naam bhi nahi", lang="hi", tag="result", sfx="beep"),
    Line(V, "तो अभी के लिए, ये अनवेरिफ़ाइड है।", "Toh abhi ke liye: UNVERIFIED", lang="hi", tag="verdict", sfx="hit"),
    Line(V, "गेमर दोस्त को भेजो, असली ईस्टर एग अभी बाकी है।", "Gamer dost ko bhejo, asli easter egg abhi baaki hai", lang="hi", tag="nudge", sfx="pop"),
    Line(V, "असली इंडियन ईस्टर एग, गेम के क्रेडिट्स में छुपा है।", "Asli Indian easter egg game ke credits mein chhupa hai", lang="hi", tag="twist", sfx="whoosh"),
    Line(V, "हज़ारों नाम। सड़क पर चलते लोग, उनके चेहरे, इनकी एनिमेशन टीमों में, लीड रोल्स पर इंडियन नाम हैं।",
         "Hazaaron naam. NPC animation, face animation: lead roles mein Indian naam", lang="hi", tag="credits", sfx="tick"),
    Line(V, "यानी लियोनिडा में लोग जैसे चलते हैं, वो चाल शायद बेंगलुरु में बनी।",
         "Leonida mein log jaise chalte hain, woh chaal shayad Bengaluru mein bani", lang="hi", tag="payoff"),
    Line(V, "तुम्हें गेम में कुछ इंडियन दिखा? स्क्रीनशॉट कमेंट करो, हम चेक करेंगे।",
         "Game mein kuch Indian dikha? Screenshot comment karo, hum check karenge", lang="hi", tag="cta", sfx="pop", gap=.2),
    Line(V, "तो, जी टी ए सिक्स में इंडियन ईस्टर एग?", "Toh… GTA 6 mein Indian easter egg?", lang="hi", tag="loop", gap=.05),
]

NAVY, CARD, CARD2 = (12, 18, 36), (28, 38, 66), (40, 54, 92)
WHITE, MUTED, SAFF, GREEN, RED, AMBER = (245, 246, 250), (150, 160, 190), (255, 153, 51), (40, 190, 110), (235, 70, 70), (255, 196, 40)

def base():
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line((x, 0, x, H), fill=(18, 26, 50), width=1)
    for y in range(0, H, 60): d.line((0, y, W, y), fill=(18, 26, 50), width=1)
    return im
BASE = base()

def header(fr, d):
    d.rounded_rectangle((90, 288, 600, 344), 14, fill=SAFF)
    fr.text((110, 293), "FACT CHECK · TRENDING", F("xb", 36), NAVY)

def magnifier(d, cx, cy, r=56, col=WHITE):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=14)
    a = math.radians(45); x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
    d.line((x0 + 4, y0 + 4, x0 + r * .9, y0 + r * .9), fill=col, width=22)

LISTS = [("List A", "52 secrets"), ("List B", "72 secrets"), ("List C", "14 secrets")]

def list_cards(fr, d, t, t0, dur, results=False, r0=0):
    for i, (a, b) in enumerate(LISTS):
        y = 520 + i * 150
        if not results and t < t0 + i * dur / 3.4: continue
        d.rounded_rectangle((100, y, 900, y + 124), 24, fill=CARD)
        fr.text((140, y + 22), a, F("xb", 50), WHITE); fr.text((140, y + 78), b, F("m", 32), MUTED)
        if not results:
            k = eout((t - t0 - i * dur / 3.4) / .9)
            d.rounded_rectangle((440, y + 52, 440 + 420 * k, y + 72), 10, fill=SAFF)
        else:
            ti = r0 + i * .35
            if t > ti:
                d.rounded_rectangle((440, y + 52, 860, y + 72), 10, fill=CARD2)
                fx.slam_word(fr, t, ti, "0 match", (560, y + 34), size=50, col=RED, frm=120)

def credits_roll(fr, d, t, t0, dur):
    fr.img.paste((4, 4, 8), (0, 0, W, H)); d = ImageDraw.Draw(fr.img); fr.d = d
    fr.text((540, 300), "rockstargames.com/VI/credits", F("sb", 34), MUTED, anchor="ma")
    heads = ["AMBIENT WORLD ANIMATION", "FACE ANIMATION", "ANIMATION RETARGETING", "AI / GAMEPLAY TECHNOLOGY", "ANIMATION"]
    rng = random.Random(7); off = (t - t0) * 150
    y = 820 - off + 60
    for hi, h in enumerate(heads):
        if 360 < y < 800: fr.text((540, y), h, F("xb", 44), WHITE, anchor="ma")
        y += 80
        for j in range(5):
            w = rng.randint(220, 420); lit = (j in (0, 1) and hi == 0) or (j == 0 and hi in (1, 4)) or (j == 2 and hi in (2, 3))
            if 360 < y < 820:
                d.rounded_rectangle((540 - w / 2, y, 540 + w / 2, y + 30), 15, fill=SAFF if lit else (70, 74, 88))
            y += 56
        y += 50
    # fade top / bottom so the roll sits inside the safe zone
    for yy in range(360, 460): d.line((0, yy, W, yy), fill=(4, 4, 8)) if yy < 380 else None
    if t > t0 + dur * .55:
        k = eback((t - t0 - dur * .55) / .35)
        d.rounded_rectangle((120, 900 - (1 - k) * 60, 900, 1020 - (1 - k) * 60), 30, fill=SAFF)
        if k > .8: fr.text((510, 928), "Lead roles: Indian naam", F("black", 58), NAVY, anchor="ma")

def walker(d, x, y, ph, col=WHITE, s=1.0):
    b = math.sin(ph) * 6 * s
    d.ellipse((x - 18 * s, y - 120 * s + b, x + 18 * s, y - 84 * s + b), fill=col)
    d.line((x, y - 84 * s + b, x, y - 40 * s + b), fill=col, width=int(10 * s))
    for sgn in (1, -1):
        d.line((x, y - 40 * s + b, x + sgn * math.sin(ph) * 22 * s, y), fill=col, width=int(10 * s))
        d.line((x, y - 74 * s + b, x - sgn * math.sin(ph) * 20 * s, y - 48 * s + b), fill=col, width=int(8 * s))

def scene(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    L = R.active(t); tag = L.tag if L else "hook"; t0 = L.t0 if L else 0
    dur = (L.t1 - L.t0) if L else 1
    if tag in ("twist", "credits"):
        credits_roll(fr, d, t, R.T("twist"), R.line("credits").t1 - R.T("twist"))
        return
    header(fr, d)
    if tag in ("hook", "loop"):
        h0 = t0 if tag == "loop" else 0.0
        fx.words_in(fr, t, h0, ["GTA 6", "mein"], (100, 400), size=118, col=WHITE, gap=.1)
        fx.slam_word(fr, t, h0 + .2, "Indian", (120, 540), size=150, col=SAFF)
        fx.words_in(fr, t, h0 + .35, ["easter", "egg?"], (100, 720), size=118, col=WHITE, gap=.1)
        if t > h0 + .6:
            k = (t - h0 - .6); magnifier(d, 760 + math.sin(k * 3) * 60, 960 + math.cos(k * 2.4) * 20, 60, AMBER)
    elif tag == "claim":
        k = eback((t - t0) / .35); y0 = 420 + (1 - k) * 80
        d.rounded_rectangle((100, y0, 900, y0 + 330), 30, fill=CARD)
        d.ellipse((135, y0 + 35, 215, y0 + 115), fill=(90, 100, 130))
        fr.text((240, y0 + 42), "Follower ka comment", F("b", 38), MUTED)
        fr.text((140, y0 + 140), "Ek Indian dev ne pizza", F("sb", 48), WHITE)
        fr.text((140, y0 + 205), "shop pe apna naam daala", F("sb", 48), WHITE)
        if t > t0 + dur * .45:
            kk = eback((t - t0 - dur * .45) / .3)
            d.rounded_rectangle((150, 800, 150 + 720 * kk, 960), 22, fill=(150, 30, 40), outline=AMBER, width=6)
            for i in range(8): d.ellipse((175 + i * 88, 812, 195 + i * 88, 832), fill=AMBER if (int(t * 6) + i) % 2 else (120, 90, 30))
            if kk > .9: fr.text((510, 845), "SOHAM PLAZA", F("black", 80), WHITE, anchor="ma")
            fr.text((510, 975), "claim", F("m", 34), MUTED, anchor="ma") if kk > .9 else None
    elif tag in ("check", "result"):
        d.rounded_rectangle((100, 380, 900, 480), 50, fill=WHITE)
        q = "soham plaza gta 6"; n = len(q) if tag == "result" else int(len(q) * min(1, (t - t0) / .9))
        fr.text((180, 405), q[:n] + ("|" if tag == "check" and int(t * 3) % 2 else ""), F("sb", 46), NAVY)
        magnifier(d, 830, 430, 22, NAVY)
        if tag == "check": list_cards(fr, d, t, t0, dur)
        else:
            list_cards(fr, d, t, t0, dur, results=True, r0=t0 + .2)
            if t > t0 + dur * .55:
                k = eback((t - t0 - dur * .55) / .3)
                d.rounded_rectangle((100, 980 - (1 - k) * 40, 900, 1050 - (1 - k) * 40), 20, fill=CARD2)
                if k > .8: fr.text((130, 990), "Official credits: \"Soham\" = 0", F("xb", 42), WHITE)
    elif tag in ("verdict", "nudge"):
        fr.text((100, 400), "Soham Plaza", F("black", 96), WHITE)
        fx.strike(d, t, R.T("verdict") + .1, (95, 460), (720, 460), col=RED, width=14)
        fx.verdict_pill(fr, t, R.T("verdict") + .25, "UNVERIFIED", (100, 560), size=104, bg=AMBER, fg=NAVY)
        fr.text((100, 760), "Abhi ke liye.", F("sb", 52), MUTED)
        fr.text((100, 840), "Rockstar ne koi easter egg", F("sb", 46), MUTED)
        fr.text((100, 900), "confirm nahi kiya", F("sb", 46), MUTED)
        if tag == "nudge":
            bob = math.sin(t * 5) * 8
            fr.text((560, 960 + bob), "Asli wala? ->", F("black", 60), SAFF, anchor="ma")
    elif tag in ("payoff", "cta"):
        fr.text((100, 380), "Leonida ki chaal", F("black", 84), WHITE)
        fr.text((100, 480), "shayad Made in Bengaluru", F("xb", 58), SAFF)
        d.polygon([(80, 1000), (960, 1000), (1000, 1140), (40, 1140)], fill=(46, 50, 64))
        for x in range(100, 960, 120): d.rectangle((x, 1062, x + 60, 1074), fill=(220, 220, 220))
        ts = t - R.T("payoff")
        for i, (x0, sp, col) in enumerate([(120, 70, WHITE), (330, 55, SAFF), (560, 80, WHITE), (760, 62, GREEN)]):
            x = 90 + ((x0 + ts * sp) % 820); walker(d, x, 990, ts * 7 + i, col, .9)
        # dotted arc to a Bengaluru pin
        px, py = 790, 690
        k = eout(ts / 1.2)
        pts = [(260 + (px - 260) * u, 880 - math.sin(u * math.pi) * 200 + (py - 880) * u) for u in [i / 30 for i in range(int(30 * k) + 1)]]
        for j, p in enumerate(pts):
            if j % 2 == 0: d.ellipse((p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6), fill=AMBER)
        if k > .95:
            d.ellipse((px - 30, py - 70, px + 30, py - 10), fill=RED); d.polygon([(px - 26, py - 30), (px + 26, py - 30), (px, py + 20)], fill=RED)
            d.ellipse((px - 11, py - 51, px + 11, py - 29), fill=WHITE)
            fr.text((px - 40, py + 30), "Bengaluru", F("xb", 44), WHITE, anchor="ma")

R = Reel("Trending_20261124_GTA6_FactCheck", "xray", LINES, tone="bright", seed=24, tail=.35)
R.cap_style = dict(fg=(255, 255, 255), hi=(255, 196, 40), bg=(0, 0, 0, 210), font="xb", who_fg=(255, 196, 40))

def setup(R):
    s = R.T("nudge")
    R.nudge = dict(text="Gamer dost ko bhejo", icon="send", at=s, dur=4.0, bg=(255, 153, 51), fg=(12, 18, 36))
    R.cta = dict(at=R.T("cta"), until=R.line("loop").t0 + .1, icon="comment", head="Comment karo!",
                 body="Kuch Indian dikha?\nScreenshot bhejo,\nhum check karenge", acc=(255, 153, 51))
    return s

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R.build_audio(f"{out}/cache"); s = setup(R)
    print("duration", round(R.dur, 2), "nudge at", round(s, 2), f"({s / R.dur:.0%})")
    st = [0.3, 0.8, 1.4] + [R.T(L.tag) + .9 for L in LINES] + [R.line("credits").t1 - .3, R.dur - .5]
    print(R.render(scene, out, stills=sorted(set(round(x, 2) for x in st))))
    print("violations", R.violations[:20])
