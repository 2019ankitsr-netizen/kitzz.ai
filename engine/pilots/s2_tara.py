"""S2 AI Ki Kahani · Ep 01 · Tara ka pehla din — Paper Pop-up Storybook (Hindi voices, Hinglish captions)."""
import os, sys, math, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reel import Reel, Line, F, FM, ease, eout, eback, W, H

N, T_, B = "hf_alpha", "hf_beta", "hm_psi"
def L(spk, say, cap, **k): return Line(spk, say, cap, lang="hi", **k)
LINES = [
    L(N, "बबलू के फ़ोन में आज, एक अनजानी आवाज़ आई।", "Bablu ke phone mein aaj ek anjaani awaaz aayi...", tag="hook", sfx="whoosh", gap=.3),
    L(T_, "नमस्ते बबलू! मैं तारा हूँ। तुम्हारी ए आई दोस्त।", "Namaste Bablu! Main Tara hoon. Tumhari AI dost.", who="TARA", tag="tara", sfx="chime"),
    L(B, "ए आई? मतलब तुम मेरी तरह सोचती हो?", "AI? Matlab tum meri tarah sochti ho?", who="BABLU", tag="b1"),
    L(T_, "नहीं बबलू। मैं सोचती नहीं। मैं अंदाज़ा लगाती हूँ।", "Nahi Bablu. Main sochti nahi. Main andaaza lagaati hoon.", who="TARA", tag="t2"),
    L(N, "बबलू को यक़ीन नहीं हुआ। उसने एक टेस्ट लिया।", "Bablu ko yakeen nahi hua. Usne ek test liya.", speed=.95, tag="test", drop=True),
    L(B, "अच्छा? तो बताओ, चाय के साथ?", "Achha? Toh batao... chai ke saath?", who="BABLU", tag="chai", sfx="pop"),
    L(T_, "बिस्कुट! क्योंकि लाखों बार, मैंने यही पढ़ा है।", "Biscuit! Kyunki laakhon baar maine yahi padha hai.", who="TARA", pre=.35, pitch=.5, tag="biscuit", sfx="pop"),
    L(N, "यही है ए आई का राज़। वो हर बार, अगला सबसे सही लगने वाला शब्द चुनता है।",
      "Yahi hai AI ka raaz: har baar, agla sabse sahi lagne wala shabd chunna.", speed=.95, tag="secret"),
    L(B, "मतलब, तुम्हें सच में कुछ पता नहीं?", "Matlab tumhe sach mein kuch pata nahi?", who="BABLU", tag="b3"),
    L(T_, "पता? नहीं। पर अंदाज़ा... बहुत अच्छा।", "Pata? Nahi. Par andaaza... bahut achha.", who="TARA", pitch=.5, tag="t4"),
    L(N, "पर अगली सुबह, तारा ने एक ऐसा जवाब दिया... जो पूरे भरोसे के साथ, बिलकुल ग़लत था।",
      "Par agli subah, Tara ne ek aisa jawab diya... jo poore bharose ke saath, bilkul galat tha.", pre=.4, speed=.93, pitch=-1, tag="cliff", drop=True),
    L(N, "भाग दो, कल। फ़ॉलो करो, वरना तारा का सच मिस हो जाएगा।", "Part 2 kal. Follow karo, warna Tara ka sach miss ho jayega.", tag="cta", sfx="pop", gap=.2),
]

PAPER = (246, 232, 205)
def shadow_layer(base, pts, col, sh=14, blur=8):
    sl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sl)
    sd.polygon([(x + sh, y + sh) for x, y in pts], fill=(60, 40, 20, 90)); sl = sl.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sl); ImageDraw.Draw(base).polygon(pts, fill=col)

def hill_pts(y0, amp, seed):
    r = random.Random(seed)
    return [(-60, H)] + [(x, y0 - amp * math.sin(x / 170 + seed) - r.randint(0, 14)) for x in range(-60, W + 101, 40)] + [(W + 100, H)]

def make_bg(night):
    sky = (40, 44, 82) if night else PAPER
    im = Image.new("RGBA", (W, H), sky + (255,)); d = ImageDraw.Draw(im)
    # paper grain
    r = random.Random(4)
    for _ in range(5000):
        x, y = r.randint(0, W), r.randint(0, H); c = r.randint(-12, 8)
        d.point((x, y), fill=tuple(max(0, min(255, v + c)) for v in sky) + (255,))
    if night:
        for _ in range(140):
            x, y = r.randint(70, 1010), r.randint(280, 760); s = r.choice([2, 2, 3])
            d.ellipse((x, y, x + s, y + s), fill=(255, 245, 210, 255))
        shadow_layer(im, [(820 + 80 * math.cos(a / 20 * math.pi), 470 + 80 * math.sin(a / 20 * math.pi)) for a in range(40)], (250, 240, 200, 255))
        ImageDraw.Draw(im).ellipse((790, 410, 910, 530), fill=sky + (255,))
    else:
        shadow_layer(im, [(820 + 85 * math.cos(a / 20 * math.pi), 480 + 85 * math.sin(a / 20 * math.pi)) for a in range(40)], (252, 200, 80, 255))
    return im

def hills(night):
    out = []
    cols = [(120, 110, 150), (90, 80, 120), (60, 55, 90)] if night else [(233, 160, 90), (205, 110, 70), (150, 80, 60)]
    for i, (y0, amp) in enumerate([(1060, 50), (1150, 40), (1250, 30)]):
        lay = Image.new("RGBA", (W + 160, H), (0, 0, 0, 0))
        shadow_layer(lay, [(x + 80, y) for x, y in hill_pts(y0, amp, i + 1)], cols[i] + (255,))
        out.append(lay)
    return out

BG = {False: make_bg(False), True: make_bg(True)}
HL = {False: hills(False), True: hills(True)}

def house(d, x, y, night):
    d.polygon([(x, y), (x, y + 150), (x + 190, y + 150), (x + 190, y), (x + 95, y - 80)], fill=(255, 250, 240) if not night else (190, 185, 200))
    d.rectangle((x + 70, y + 70, x + 120, y + 150), fill=(140, 70, 60))
    d.rectangle((x + 20, y + 30, x + 55, y + 65), fill=(255, 220, 120) if night else (150, 200, 230))

def bablu(img, x, y, talk, t):
    """Original paper cut-out boy: round face, hair tuft, orange kurta."""
    d = ImageDraw.Draw(img); bob = math.sin(t * 14) * 6 if talk else 0; y = y + bob
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse((x - 70 + 12, y - 70 + 12, x + 70 + 12, y + 70 + 12), fill=(60, 40, 20, 80)); sd.rounded_rectangle((x - 90 + 12, y + 70 + 12, x + 90 + 12, y + 300 + 12), 40, fill=(60, 40, 20, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7))); d = ImageDraw.Draw(img)
    d.rounded_rectangle((x - 90, y + 70, x + 90, y + 300), 40, fill=(235, 130, 50))
    d.line((x, y + 80, x, y + 180), fill=(200, 100, 30), width=5)
    d.ellipse((x - 70, y - 70, x + 70, y + 70), fill=(214, 160, 120))
    d.chord((x - 74, y - 80, x + 74, y + 30), 180, 360, fill=(40, 30, 30)); d.polygon([(x - 10, y - 80), (x + 25, y - 110), (x + 30, y - 70)], fill=(40, 30, 30))
    blink = (t % 3.3) < .12
    for ex in (x - 26, x + 26):
        if blink: d.line((ex - 10, y + 5, ex + 10, y + 5), fill=(30, 20, 20), width=4)
        else: d.ellipse((ex - 9, y - 4, ex + 9, y + 14), fill=(30, 20, 20))
    mo = 10 + 10 * abs(math.sin(t * 18)) if talk else 4
    d.ellipse((x - 16, y + 30, x + 16, y + 30 + mo), fill=(120, 40, 40))

def tara(img, x, y, talk, t, mood="happy"):
    """Tara: a phone with a face."""
    d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x + 12, y + 12, x + 212, y + 372), 34, fill=(60, 40, 20, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8))); d = ImageDraw.Draw(img)
    d.rounded_rectangle((x, y, x + 200, y + 360), 34, fill=(40, 45, 70))
    scr = (255, 120, 110) if mood == "alarm" else (120, 220, 230)
    glow = .5 + .5 * math.sin(t * 3)
    d.rounded_rectangle((x + 14, y + 22, x + 186, y + 338), 24, fill=scr)
    blink = (t % 2.7) < .12
    for ex in (x + 65, x + 135):
        if blink: d.line((ex - 14, y + 140, ex + 14, y + 140), fill=(30, 30, 50), width=6)
        else: d.ellipse((ex - 15, y + 125, ex + 15, y + 158), fill=(30, 30, 50))
    if talk:
        mo = 8 + 18 * abs(math.sin(t * 17)); d.ellipse((x + 75, y + 195, x + 125, y + 195 + mo), fill=(30, 30, 50))
    elif mood == "alarm": d.line((x + 70, y + 215, x + 130, y + 205), fill=(30, 30, 50), width=8)
    else: d.arc((x + 60, y + 170, x + 140, y + 235), 20, 160, fill=(30, 30, 50), width=8)

def card(fr, box, k, fill=(255, 250, 240)):
    """Paper card that folds up from its bottom edge (k 0..1)."""
    x0, y0, x1, y1 = box; h = (y1 - y0) * k
    if k <= 0.02: return None
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle((x0 + 10, y1 - h + 12, x1 + 10, y1 + 12), 22, fill=(60, 40, 20, 80))
    fr.img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(6)))
    fr.d = ImageDraw.Draw(fr.img); fr.d.rounded_rectangle((x0, y1 - h, x1, y1), 22, fill=fill)
    return y1 - h

def scene(fr, t, R):
    T = R.T
    night = t >= T("cliff") - .2
    fr.img = BG[night].copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    sway = math.sin(t * .6)
    house(d, 120 + sway * 4, 800, night)
    for i, lay in enumerate(HL[night]):
        fr.img.alpha_composite(lay, (int(-80 + sway * (6 + 6 * i)), 0))
    d = ImageDraw.Draw(fr.img); fr.d = d
    sp = R.speaking(t)
    # characters pop up at the start
    k = eback((t - .15) / .5)
    bablu(fr.img, 300, int(700 + (1 - k) * 400), sp is not None and sp.spk == B, t)
    kt = eback((t - (T("tara") - .3)) / .5) if t >= T("tara") - .3 else 0
    mood = "alarm" if night and t < T("cta") else "happy"
    if kt > 0: tara(fr.img, 640, int(650 + (1 - kt) * 500), sp is not None and sp.spk == T_, t, mood)
    fr.d = ImageDraw.Draw(fr.img); d = fr.d
    # header
    tc = (255, 220, 160) if night else (180, 70, 50); hc = (255, 245, 230) if night else (60, 35, 25)
    fr.text((90, 292), "AI KI KAHANI · EP 1", FM(32), tc)
    if t < T("b1"):
        kk = eout((t - .05) / .4)
        fr.text((90, 340 + (1 - kk) * 30), "Tara ka\npehla din", F("black", 96), hc, spacing=0)
    # chai test card -> next-word guesses
    c0 = T("chai")
    if c0 - .1 <= t < T("b3"):
        y = card(fr, (90, 340, 990, 632), eback((t - c0) / .5))
        if y is not None and y < 360:
            fr.text((130, 370), "chai ke saath ___", F("black", 72), (60, 35, 25))
            if t >= T("biscuit") - .1:
                opts = [("biscuit", .62), ("pakode", .21), ("samosa", .09)]
                for i, (w_, p) in enumerate(opts):
                    kk = eout((t - T("biscuit") - i * .25) / .5); yy = 455 + i * 56
                    if kk <= 0: continue
                    col = (225, 120, 40) if i == 0 else (190, 150, 110)
                    d.rounded_rectangle((340, yy + 14, 340 + 400 * p / .62 * kk, yy + 46), 12, fill=col)
                    fr.text((130, yy), w_, F("b", 48), (60, 35, 25))
                    fr.text((770, yy), f"{int(p * 100)}%", F("b", 48), (60, 35, 25))
            if t >= T("secret"):
                fr.text((960, 372), "example", F("m", 30), (120, 90, 70), anchor="ra")
    # Tara can be confidently wrong: the cliffhanger card
    cl = R.line("cliff")
    if cl.t0 + 1.0 <= t < T("cta"):
        y = card(fr, (90, 340, 990, 560), eback((t - cl.t0 - 1.0) / .5), fill=(255, 235, 230))
        if y is not None and y < 360:
            fr.text((130, 380), "Poore bharose ke saath...", F("xb", 54), (120, 30, 30))
            if t > cl.t0 + (cl.t1 - cl.t0) * .7: fr.text((130, 460), "bilkul galat.", F("black", 72), (200, 40, 40))

def build(out):
    for L_ in LINES: L_.speed = round(L_.speed * 1.08, 3); L_.gap = min(L_.gap, .3)
    R = Reel("S2_AIKiKahani_ep01_TaraKaPehlaDin", "story", LINES, tone="bright", pitch=1.0, seed=2)
    R.cap_style.update(fg=(255, 250, 240), hi=(255, 200, 90), bg=(60, 35, 25, 215), who_fg=(255, 200, 90), who_stroke=(60, 35, 25))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Tag a friend", icon="send", at=round(dur * .4, 2), xy=(560, 282), bg=(60, 35, 25), fg=(255, 245, 230))
    R.cta = dict(at=R.T("cta"), icon="follow", head="Part 2 kal", body="Follow karo, warna\nTara ka sach\nmiss ho jayega.",
                 bg=(255, 250, 240), acc=(200, 80, 40), fg=(60, 35, 25))
    tags = ["hook", "tara", "b1", "t2", "test", "chai", "biscuit", "secret", "b3", "t4", "cliff", "cta"]
    stills = sorted([.7] + [R.T(x) + .9 for x in tags] + [R.nudge["at"] + .5, R.line("cliff").t1 - .3, dur - .3])
    return R, R.render(scene, out, stills=stills)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", R.violations[:20], len(R.violations))
