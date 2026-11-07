"""Diwali 2026 · 'Diwali from space' viral photo is fake — satellite night-map style (fact check)."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
from diwali_common import *

V = "hm_omega"
LINES = [
    HL(V, "दिवाली की रात, अंतरिक्ष से भारत की ये फ़ोटो... नकली है।", tag="hook", sfx="hit", gap=.25),
    HL(V, "हर साल ये फ़ोटो, नासा के नाम से वायरल होती है।", "हर साल ये फ़ोटो NASA के नाम से वायरल होती है।", tag="viral", sfx="whoosh"),
    HL(V, "असल में, ये कई सालों की सैटेलाइट तस्वीरों को जोड़कर बनाई गई थी।", tag="composite", sfx="tick"),
    HL(V, "अलग-अलग रंग बताते हैं, कि किस साल, कहाँ नई रोशनी दिखी।", tag="colors"),
    HL(V, "दो हज़ार पंद्रह में, नासा ने खुद लिखा: ये बहुत पुराना फ़ेक है।", "2015 में NASA ने खुद लिखा: ये बहुत पुराना फ़ेक है।",
       pre=.3, pitch=1, tag="nasa", sfx="pop"),
    HL(V, "दिवाली की रात की असली नासा तस्वीर, दो हज़ार बारह की है। और वो, किसी आम रात जैसी ही दिखती है।",
       "दिवाली की रात की असली NASA तस्वीर 2012 की है, और वो किसी आम रात जैसी ही दिखती है।", speed=.95, pitch=-.5, tag="real", drop=True),
    HL(V, "क्योंकि दीयों की रोशनी, अंतरिक्ष से अलग दिखने के लिए बहुत कम है।", tag="why", sfx="tick"),
    HL(V, "तो इस बार, फ़ेक फ़ोटो नहीं, ये रील फ़ैमिली ग्रुप में भेजो।", tag="cta", sfx="pop", gap=.3),
]
# an abstract "landmass" of lights (illustration, not a map)
r = random.Random(12)
CL = [(r.uniform(300, 780), r.uniform(560, 1000), r.uniform(10, 46)) for _ in range(34)]
DOTS = []
for cx, cy, sz in CL:
    for _ in range(int(sz * 2.2)):
        a = r.uniform(0, 2 * math.pi); rr = abs(r.gauss(0, sz))
        DOTS.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * .9, r.choice([0, 0, 1, 1, 2, 3])))
YEAR_COL = [(255, 255, 255), (255, 220, 60), (60, 220, 255), (255, 80, 200)]
def base():
    im = Image.new("RGBA", (W, H), (4, 8, 22, 255)); d = ImageDraw.Draw(im)
    for x in range(60, W, 90): d.line((x, 270, x, 1250), fill=(14, 28, 56), width=2)
    for y in range(300, 1250, 90): d.line((60, y, 1020, y), fill=(14, 28, 56), width=2)
    return im
BASE = base()
def lights(img, mode, k=1.0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for x, y, c in DOTS:
        if mode == "fake": col = YEAR_COL[c] + (int(255 * k),); s = 4
        else: col = (235, 230, 200, int(150 * k)); s = 2.6
        d.ellipse((x - s, y - s, x + s, y + s), fill=col)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3 if mode == "fake" else 1.6))); img.alpha_composite(lay)
def scene(fr, t, R):
    T = R.T; fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    sx = 60 + (t * 220) % 960; d.line((sx, 270, sx, 1250), fill=(40, 90, 140), width=3)                        # satellite sweep
    real = T("real") - .1 <= t < T("cta")
    lights(fr.img, "real" if real else "fake"); fr.d = d = ImageDraw.Draw(fr.img)
    if t < T("real") - .1:
        d.rounded_rectangle((90, 300, 520, 370), 16, fill=(200, 30, 40)); fr.text((110, 335), "वायरल फ़ोटो", HF(48), (255, 255, 255), anchor="lm")
        if t >= T("hook") + 1.6:
            k = ease((t - T("hook") - 1.6) / .5); fr.text((560, 335), "नकली", HF(60), (255, 90, 90), anchor="lm")
            d.line((90, 300 + 70 * (1 - k), 90 + 430 * k, 370 - 70 * (1 - k)), fill=(255, 255, 255), width=0)
    c = R.line("colors")
    if c.t0 <= t < T("real") - .1:
        for i, (yr, col) in enumerate(zip(("1992", "1998", "2000", "2003"), YEAR_COL)):
            x = 100 + i * 200; d.ellipse((x, 975, x + 34, 1009), fill=col); fr.text((x + 46, 992), yr, F("b", 44), (220, 230, 245), anchor="lm")
    cp = R.line("composite")
    if cp.t0 + .5 <= t < c.t0:
        for i in range(4):
            k = eout((t - cp.t0 - .5 - i * .35) / .4)
            if k > 0: d.rounded_rectangle((640 + i * 22, 420 + i * 22, 940 + i * 22, 560 + i * 22), 12, outline=(120, 200, 255), width=4)
        fr.text((640, 640), "कई सालों का जोड़", HF(52), (120, 200, 255))
    n = R.line("nasa")
    if n.t0 + .4 <= t < T("real") - .1:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((90, 420, 990, 620), 24, fill=(255, 255, 255, 235))
        fr.img.alpha_composite(lay); fr.d = d = ImageDraw.Draw(fr.img)
        fr.text((130, 450), "NASA Earth · 2015", F("b", 44), (40, 60, 100)); fr.text((130, 515), "\"a really old fake\"", F("black", 72), (200, 30, 40))
    if real:
        d.rounded_rectangle((90, 300, 640, 370), 16, fill=(30, 150, 90)); fr.text((110, 335), "असली · NASA 2012", HF(48), (255, 255, 255), anchor="lm")
        w = R.line("why")
        if t >= w.t0: fr.text((540, 470), "दीयों की रोशनी = बहुत कम", HF(60), (255, 214, 120), anchor="mm")
    fr.text((975, 335), "चित्रण", HF(36), (120, 140, 170), anchor="rm")
if __name__ == "__main__":
    nudge = dict(text="फ़ैमिली ग्रुप में भेजो", icon="send", bg=(255, 196, 70), fg=(20, 20, 40), fontfile=f"{FONTS}/Hind-Bold.ttf")
    cta = dict(icon="send", head="भेजो!", body="फ़ेक फ़ोटो नहीं,\nये रील भेजो।", bg=(240, 246, 255), acc=(200, 30, 40), fg=(20, 20, 40),
               fontfile=f"{FONTS}/Hind-Bold.ttf")
    R, p = build("Diwali2026_03_SpacePhotoFake", LINES, scene, sys.argv[1], music="space", nudge=nudge, cta=cta, seed=83)
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
