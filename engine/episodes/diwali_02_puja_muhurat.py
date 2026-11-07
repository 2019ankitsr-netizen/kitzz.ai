"""Diwali 2026 · Lakshmi Puja muhurat, city-wise — paper-lantern (kandil) cards. Times: Drik Panchang (Sun 8 Nov 2026)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from diwali_common import *

V = "hm_omega"
CITIES = [("दिल्ली", "5:54 – 7:50"), ("मुंबई", "6:27 – 8:27"), ("कोलकाता", "5:20 – 7:18"), ("बेंगलुरु", "6:17 – 8:20"),
          ("चेन्नई", "6:07 – 8:09"), ("हैदराबाद", "6:07 – 8:08"), ("पुणे", "6:24 – 8:24"), ("अहमदाबाद", "6:22 – 8:20")]
LINES = [
    HL(V, "आज शाम, लक्ष्मी पूजा का शुभ मुहूर्त, आपके शहर में कब है?", tag="hook", sfx="dingdong", gap=.25),
    HL(V, "सेव कर लो, ताकि पूजा के समय ढूँढना न पड़े।", tag="save"),
    HL(V, "दिल्ली: पाँच बजकर चौवन मिनट से, सात बजकर पचास तक।", "दिल्ली: शाम 5:54 से 7:50 तक", tag="c0", sfx="tick"),
    HL(V, "मुंबई: छह बजकर सत्ताईस से, आठ बजकर सत्ताईस तक।", "मुंबई: 6:27 से 8:27 तक", tag="c1", sfx="tick"),
    HL(V, "कोलकाता: पाँच बजकर बीस से, सात बजकर अठारह तक।", "कोलकाता: 5:20 से 7:18 तक", tag="c2", sfx="tick"),
    HL(V, "बेंगलुरु: छह बजकर सत्रह से, आठ बजकर बीस तक।", "बेंगलुरु: 6:17 से 8:20 तक", tag="c3", sfx="tick"),
    HL(V, "चेन्नई और हैदराबाद: छह बजकर सात से, लगभग आठ बजे तक।", "चेन्नई / हैदराबाद: 6:07 से लगभग 8:08 तक", tag="c4", sfx="tick"),
    HL(V, "बाकी शहर स्क्रीन पर हैं। अपने पंचांग से एक बार ज़रूर मिला लें।", "बाकी शहर स्क्रीन पर। अपने पंचांग से एक बार ज़रूर मिला लें।",
       speed=.95, tag="rest", drop=True),
    HL(V, "सेव करो, और परिवार को भेजो, ताकि सब एक साथ दीया जलाएँ।", tag="cta", sfx="pop", gap=.3),
]
BG = night_bg(top=(70, 10, 20), bottom=(110, 30, 20), seed=3, n=18)
def lantern(img, x, y, s, t, col):
    sw = math.sin(t * 1.6 + x / 90) * 6
    d = ImageDraw.Draw(img); d.line((x, 0, x + sw, y - 70 * s), fill=(220, 180, 120), width=3)
    paste_glow(img, x + sw, y, int(120 * s), col[:3] + (90,)); d = ImageDraw.Draw(img)
    cx = x + sw
    d.polygon([(cx - 60 * s, y - 60 * s), (cx + 60 * s, y - 60 * s), (cx + 80 * s, y), (cx + 60 * s, y + 60 * s), (cx - 60 * s, y + 60 * s), (cx - 80 * s, y)], fill=col)
    d.polygon([(cx - 30 * s, y - 70 * s), (cx + 30 * s, y - 70 * s), (cx + 22 * s, y - 60 * s), (cx - 22 * s, y - 60 * s)], fill=(200, 150, 60))
    for i in range(5): d.line((cx - 40 * s + i * 20 * s, y + 60 * s, cx - 40 * s + i * 20 * s, y + 110 * s), fill=col, width=4)
    d.line((cx - 70 * s, y, cx + 70 * s, y), fill=(255, 230, 160), width=3)

def city_card(fr, t, name, time_, t0, y0=560, h=380):
    k = eback((t - t0) / .4); sy = max(.02, min(1.1, k))
    cy = y0 + h / 2; hh = h * sy / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((110, cy - hh + 12, 910, cy + hh + 12), 36, fill=(0, 0, 0, 90))
    ld.rounded_rectangle((100, cy - hh, 900, cy + hh), 36, fill=(255, 244, 222, 255), outline=(220, 150, 40, 255), width=6)
    fr.img.alpha_composite(lay); fr.d = ImageDraw.Draw(fr.img)
    if sy > .85:
        fr.text((500, y0 + 95), name, HF(92), (130, 30, 20), anchor="mm")
        fr.text((500, y0 + 225), time_, F("black", 104), (200, 80, 20), anchor="mm")
        fr.text((500, y0 + 320), "PM · रवि, 8 नवंबर", HF(48), (130, 70, 40), anchor="mm")

def scene(fr, t, R):
    fr.img = BG.copy()
    for x, s_, c in ((150, .8, (230, 70, 50, 255)), (540, .65, (240, 170, 40, 255)), (930, .8, (200, 60, 120, 255))):
        lantern(fr.img, x, 390, s_, t, c)
    fr.d = ImageDraw.Draw(fr.img)
    T = R.T
    if t < T("c0") - .1:
        k = eout((t - .05) / .35)
        fr.text((540, 640 + (1 - k) * 30), "लक्ष्मी पूजा", YF(130), (255, 214, 120), anchor="mm")
        fr.text((540, 800), "शुभ मुहूर्त · आपके शहर में", HF(64), (255, 244, 222), anchor="mm")
        if t >= T("save") - .1: fr.text((540, 900), "सेव करो", HF(60), (255, 196, 70), anchor="mm")
    elif t < T("rest") - .1:
        idx = 0
        for i in range(5):
            if t >= T(f"c{i}") - .1: idx = i
        if idx == 4: name, tm = "चेन्नई / हैदराबाद", "6:07 – ~8:08"
        else: name, tm = CITIES[idx]
        city_card(fr, t, name, tm, T(f"c{idx}"))
        fr.text((540, 520), f"{idx + 1} / 5", F("xb", 40), (255, 214, 120), anchor="mm")
    else:
        rs = T("rest")
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((90, 515, 910, 1045), 36, fill=(255, 244, 222, 240))
        fr.img.alpha_composite(lay); fr.d = ImageDraw.Draw(fr.img)
        for i, (n, tm) in enumerate(CITIES):
            k = eout((t - rs - i * .12) / .3)
            if k <= 0: continue
            col, row = i % 2, i // 2; x = 125 + col * 395; y = 535 + row * 112
            fr.text((x, y), n, HF(48), (130, 30, 20)); fr.text((x, y + 58), tm + " PM", F("b", 42), (200, 80, 20))
        fr.text((500, 1018), "स्रोत: द्रिक पंचांग · स्थानीय पंचांग देखें", HF(34), (130, 70, 40), anchor="mm")
    fr.text((90, 292), "KITZZ.AI · DIWALI 2026", FM(30), (255, 200, 120))

if __name__ == "__main__":
    nudge = dict(text="सेव करो, शाम को काम आएगा", icon="save", bg=(255, 196, 70), fg=(80, 15, 15), fontfile=f"{FONTS}/Hind-Bold.ttf")
    cta = dict(icon="save", head="सेव करो!", body="परिवार को भेजो,\nसब एक साथ\nदीया जलाएँ।", bg=(255, 246, 230), acc=(190, 50, 20), fg=(80, 15, 15),
               fontfile=f"{FONTS}/Hind-Bold.ttf")
    R, p = build("Diwali2026_02_LakshmiPujaMuhurat", LINES, scene, sys.argv[1], nudge=nudge, cta=cta, seed=82)
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
