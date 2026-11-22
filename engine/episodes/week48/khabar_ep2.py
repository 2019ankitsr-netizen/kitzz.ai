"""AI Khabar · Ep 2 · "ChatGPT 4 saal ka ho gaya" — STYLE: Birthday Pop Timeline
(halftone purple, confetti, count-up numbers, calendar flip, family sticker cards; whip / zoom / slide-up cuts).
Facts: launched 30 Nov 2022 (HISTORY.com); 1 million users in 5 days (Entrepreneur India, Dec 2022);
India 100 million weekly users (Sam Altman via TechCrunch, 15 Feb 2026). No logos."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from kit import *                      # noqa: F401,F403
import lines48 as LN
from fx import words_in

NAME = "AIKhabar_Ep2_ChatGPT4Saal"
YEL = (255, 214, 40); PINK = (255, 92, 140); CYAN = (80, 220, 255); RED = (235, 40, 60); WHITE = (255, 255, 255); INK = (25, 12, 40)
BGI = halftone()
CONF = Confetti(80, 11)

def header(fr):
    fr.d.rounded_rectangle((65, 286, 585, 340), 27, fill=RED, outline=INK, width=4)
    fr.text((88, 291), "AI KHABAR · 60 SEC MEIN", F("black", 36), WHITE)
    fr.d.rounded_rectangle((600, 286, 730, 340), 27, fill=YEL, outline=INK, width=4)
    fr.text((622, 291), "EP 2", F("black", 36), INK)

def cake(d, cx, top, t, s=1.0, candles=4):
    w1, w2 = 300 * s, 220 * s; h1, h2 = 120 * s, 100 * s
    d.ellipse((cx - w1 * 1.25, top + h2 + h1 - 20 * s, cx + w1 * 1.25, top + h2 + h1 + 50 * s), fill=(235, 235, 245), outline=INK, width=6)   # plate
    d.rounded_rectangle((cx - w1, top + h2, cx + w1, top + h2 + h1), int(20 * s), fill=(255, 170, 200), outline=INK, width=6)
    d.rounded_rectangle((cx - w2, top, cx + w2, top + h2 + 10 * s), int(20 * s), fill=(255, 240, 220), outline=INK, width=6)
    for i in range(7):   # drips
        x = cx - w1 + 30 * s + i * (2 * w1 - 60 * s) / 6
        d.ellipse((x - 18 * s, top + h2 - 6 * s, x + 18 * s, top + h2 + (34 + 14 * (i % 2)) * s), fill=(250, 250, 255), outline=INK, width=3)
    d.rectangle((cx - w1 + 4, top + h2 + 4, cx + w1 - 4, top + h2 + 18 * s), fill=(250, 250, 255))
    for i in range(candles):
        x = cx - w2 + 60 * s + i * (2 * w2 - 120 * s) / max(1, candles - 1)
        d.rounded_rectangle((x - 13 * s, top - 90 * s, x + 13 * s, top + 6), int(6 * s), fill=CYAN if i % 2 else PINK, outline=INK, width=4)
        fl = 1 + .15 * math.sin(t * 17 + i * 2)
        d.ellipse((x - 14 * s, top - 140 * s * fl, x + 14 * s, top - 92 * s), fill=YEL, outline=(255, 120, 30), width=3)

def face(d, cx, cy, r, kind):
    skin = {"mummy": (226, 172, 132), "papa": (214, 160, 118), "riya": (236, 186, 148), "dadaji": (222, 170, 130)}[kind]
    if kind == "mummy": d.ellipse((cx - r * .55, cy - r * 1.28, cx + r * .55, cy - r * .6), fill=(30, 24, 24), outline=INK, width=4)    # bun
    if kind == "riya":
        d.polygon([(cx + r * .7, cy - r * .5), (cx + r * 1.35, cy + r * .2), (cx + r * .9, cy + r * .9), (cx + r * .6, cy)], fill=(40, 28, 28), outline=INK)   # ponytail
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=skin, outline=INK, width=6)
    hair = {"mummy": (30, 24, 24), "papa": (40, 34, 34), "riya": (40, 28, 28), "dadaji": (235, 235, 235)}[kind]
    if kind == "dadaji":
        for sx in (-1, 1): d.chord((cx + sx * r * .62 - r * .4, cy - r * .7, cx + sx * r * .62 + r * .4, cy + r * .1), 0, 360, fill=hair)
    else: d.chord((cx - r, cy - r, cx + r, cy + r * .3), 180, 360, fill=hair, outline=INK, width=4)
    for sx in (-1, 1): d.ellipse((cx + sx * r * .38 - r * .09, cy - r * .02, cx + sx * r * .38 + r * .09, cy + r * .2), fill=INK)
    if kind in ("papa", "dadaji"):
        for sx in (-1, 1): d.ellipse((cx + sx * r * .38 - r * .24, cy - r * .14, cx + sx * r * .38 + r * .24, cy + r * .34), outline=INK, width=5)
        d.chord((cx - r * .5, cy + r * .2, cx + r * .5, cy + r * .62), 180, 360, fill=hair, outline=INK, width=3)
    if kind == "mummy": d.ellipse((cx - r * .08, cy - r * .42, cx + r * .08, cy - r * .26), fill=RED)
    d.arc((cx - r * .4, cy + r * .2, cx + r * .4, cy + r * .7), 20, 160, fill=INK, width=6)

FAM = {"mummy": ("MUMMY", "Fridge mein jo bacha hai,\nusse aaj kya banaun?", PINK),
       "papa": ("PAPA", "Bank ko complaint ka\nemail, English mein.", CYAN),
       "riya": ("RIYA", "Kal ka exam,\n5 minute mein samjhao.", YEL),
       "dadaji": ("DADAJI", "Meri purani photo\nrangeen kar do.", (150, 255, 150))}
ORDER = ["mummy", "papa", "riya", "dadaji"]

def counter(fr, t, t0, value, xy, size, col, suffix="", dur=.9, anchor="mm", font=None):
    a = t - t0
    if a < 0: return
    n = value if a >= dur else eout(a / dur) * value
    land = a - dur; punch = 1 + .18 * max(0, 1 - land / .2) if land > 0 else 1
    f = (font or (lambda s: F("black", s)))(int(size * punch))
    fr.text(xy, indian(n) + suffix, f, col, anchor=anchor, stroke=8, stroke_fill=INK)

def scene(fr, t, R):
    compose(fr, t, R, draw, trans={"launch": "whip", "five": "zoom", "india": "zoom", "q": "slide_up", "mummy": "whip", "papa": "whip",
                                   "riya": "whip", "dadaji": "whip", "rule": "zoom", "cta": "iris", "loop": "whip"})

def draw(fr, tag, t, L, R):
    fr.img = BGI.copy(); fr.d = ImageDraw.Draw(fr.img); d = fr.d; header(fr); t0 = L.t0
    if tag in ("hook", "loop", "cta"):
        if tag != "cta":
            a = t - t0; n = min(4, int(eout(a / .5) * 4.999)) if a < .5 else 4
            land = a - .5; p = 1 + .25 * max(0, 1 - land / .18) if land > 0 else 1
            fr.text((330, 560), str(n), F("black", int(330 * p)), YEL, anchor="mm", stroke=10, stroke_fill=INK)
            words_in(fr, t, t0 + .25, ["SAAL."], (500, 430), size=120, col=WHITE)
            words_in(fr, t, t0 + .7, ["EK", "CHATBOT."], (500, 580), size=72, col=CYAN)
        cake(d, 540, 860 if tag != "cta" else 880, t, .95)
        CONF.draw(d, t, t0 - (0 if tag != "loop" else 1))
    elif tag == "launch":
        k = eback(prog(t, t0, .4)); cx, top, bot = 540, 380, 900
        hh = (bot - top) * k
        shadowed(fr, (220, top, 860, top + hh), 30, WHITE, outline=INK, w=7); d = fr.d
        if k > .6:
            d.rounded_rectangle((220, top, 860, top + 130), 30, fill=RED, outline=INK, width=7); d.rectangle((227, top + 100, 853, top + 130), fill=RED)
            fr.text((cx, top + 66), "NOVEMBER", F("black", 64), WHITE, anchor="mm")
            fr.text((cx, top + 300), "30", F("black", 250), INK, anchor="mm")
            fr.text((cx, top + 465), "2022", F("black", 70), RED, anchor="mm")
            for i in range(2): d.ellipse((330 + i * 380, top - 20, 370 + i * 380, top + 20), fill=INK)
        if t > t0 + (L.t1 - t0) * .4:
            kk = eout(prog(t, t0 + (L.t1 - t0) * .4, .3))
            d.rounded_rectangle((120, 935 + (1 - kk) * 40, 900, 1030 + (1 - kk) * 40), 48, fill=INK)
            fr.text((510, 982 + (1 - kk) * 40), "ChatGPT launch hua", F("black", 58), YEL, anchor="mm")
    elif tag == "five":
        d.rounded_rectangle((330, 380, 750, 480), 50, fill=YEL, outline=INK, width=6); fr.text((540, 430), "SIRF 5 DIN", F("black", 64), INK, anchor="mm")
        counter(fr, t, t0 + .3, 1000000, (540, 640), 170, WHITE)
        fr.text((540, 790), "log", F("black", 80), CYAN, anchor="mm")
        for i in range(5):
            k = prog(t, t0 + .3 + i * .18, .18); x0 = 130 + i * 160
            d.rounded_rectangle((x0, 880, x0 + 140, 950), 18, fill=(70, 40, 110), outline=INK, width=5)
            if k > 0: d.rounded_rectangle((x0, 880, x0 + 140 * k, 950), 18, fill=PINK)
            fr.text((x0 + 70, 990), f"Din {i + 1}", F("xb", 34), WHITE, anchor="mm")
    elif tag == "india":
        d.rounded_rectangle((180, 380, 900, 470), 45, fill=WHITE, outline=INK, width=6)
        fr.text((540, 425), "Har hafte · sirf Bharat", F("black", 54), INK, anchor="mm")
        counter(fr, t, t0 + (L.t1 - t0) * .45, 10, (330, 610), 230, YEL, dur=.6)
        if t > t0 + (L.t1 - t0) * .45 + .6: fr.text((500, 640), "CRORE", F("black", 110), WHITE, anchor="lm", stroke=8, stroke_fill=INK)
        # bar race: 10 lakh (5 days) vs 10 crore (every week)
        fr.text((120, 790), "5 din, 2022: 10 lakh", F("xb", 40), WHITE); d.rounded_rectangle((120, 845, 128, 885), 4, fill=PINK)
        k = eout(prog(t, t0 + .4, 1.2))
        fr.text((120, 905), "Har hafte, 2026: 10 crore", F("xb", 40), WHITE)
        d.rounded_rectangle((120, 960, 120 + 780 * k, 1010), 12, fill=YEL, outline=INK, width=4)
        fr.text((900, 1032), "Source: Sam Altman, Feb 2026", F("sb", 26), (200, 190, 230), anchor="ra")
    elif tag == "q":
        k = eback(prog(t, t0, .4)); cx = 540
        d.polygon([(cx - 280 * k, 640), (cx, 420 + (1 - k) * 80), (cx + 280 * k, 640)], fill=PINK, outline=INK)
        d.rectangle((cx - 230 * k, 640, cx + 230 * k, 900), fill=(255, 240, 220), outline=INK, width=7)
        for i in range(4):
            on = t > t0 + .35 + i * .25; x = cx - 180 + (i % 2) * 230; y = 670 + (i // 2) * 110
            if k > .8: d.rectangle((x, y, x + 130, y + 90), fill=YEL if on else (90, 70, 120), outline=INK, width=5)
        fr.text((540, 990), "Ghar mein kya badla?", F("black", 70), WHITE, anchor="mm", stroke=6, stroke_fill=INK)
    elif tag in FAM:
        nm, ask, col = FAM[tag]; k = eback(prog(t, t0, .35))
        shadowed(fr, (90, 380, 990, 760), 44, col, outline=INK, w=7); d = fr.d
        face(d, 250, 560, 110 * max(.3, k), tag)
        d.rounded_rectangle((150, 690, 350, 745), 27, fill=INK); fr.text((250, 718), nm, F("black", 36), WHITE, anchor="mm")
        kk = prog(t, t0 + .25, .9)
        bubble(fr, (390, 430, 970, 690), WHITE, [(400, 600), (340, 640), (410, 650)]); d = fr.d
        fr.text((420, 465), type_on(ask, kk), F("xb", 44), INK, spacing=12)
        # progress strip with the family so far
        for i, who in enumerate(ORDER):
            x = 220 + i * 160; done = ORDER.index(tag) >= i
            circ(d, x, 870, 58, FAM[who][2] if done else (80, 55, 120), w=5)
            if done: face(d, x, 872, 44, who)
        d.rounded_rectangle((90, 950, 900, 1030), 40, fill=INK)
        fr.text((495, 990), "Sab ne AI se poocha", F("black", 46), YEL, anchor="mm")
    elif tag == "rule":
        k = eout(prog(t, t0, .35))
        d.rectangle((65, 380 - (1 - k) * 80, 1015, 480 - (1 - k) * 80), fill=RED); fr.text((540, 430 - (1 - k) * 80), "EK NIYAM NAHI BADLA", F("black", 64), WHITE, anchor="mm")
        cx, cy = 540, 620; s = eback(prog(t, t0 + .2, .35))
        d.polygon([(cx, cy - 120 * s), (cx + 135 * s, cy + 100 * s), (cx - 135 * s, cy + 100 * s)], fill=YEL, outline=INK)
        if s > .7: fr.text((cx, cy + 25), "!", F("black", 150), INK, anchor="mm")
        p = (t - t0) / max(.1, L.t1 - t0)
        if p > .3: fr.text((540, 820), "AI galat bhi", F("black", 84), WHITE, anchor="mm", stroke=6, stroke_fill=INK); fr.text((540, 910), "ho sakta hai.", F("black", 84), WHITE, anchor="mm", stroke=6, stroke_fill=INK)
        if p > .68:
            d.rounded_rectangle((140, 965, 880, 1040), 38, fill=(150, 255, 150), outline=INK, width=5)
            fr.text((510, 1003), "Zaroori baat? Khud jaancho.", F("black", 44), INK, anchor="mm")

def build(out):
    A_ = __import__("audio"); R = Reel(NAME, "festive", LN.KHABAR, tone="bright", seed=8)
    R.cap_style.update(fg=WHITE, hi=YEL, bg=(25, 12, 40, 235))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Family group mein bhejo", icon="send", at=round(dur * .38, 2), bg=YEL, fg=INK)
    R.cta = dict(at=R.T("cta"), icon="send", head="Family group", body="mein bhejo… aur poocho:\nsabse zyada AI kaun\nchalata hai?", bg=WHITE, acc=RED, fg=INK, until=R.T("loop") - .05)
    stills = sorted([.3, .9] + [R.T(x) + .8 for x in ["launch", "five", "india", "q", "mummy", "papa", "riya", "dadaji", "rule", "cta", "loop"]]
                    + [R.line("india").t1 - .2, R.line("rule").t1 - .2, R.nudge["at"] + 1.0, dur - .2])
    return R, R.render(scene, out, stills=stills)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/out48"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", len(R.violations), R.violations[:15])
