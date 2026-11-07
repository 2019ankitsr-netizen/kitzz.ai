"""Diwali Did You Know · 02 · Blue is the hardest firework colour."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
from dyk_kit import *
LINES = [
    HL(V, "क्या आप जानते हैं? आसमान में सबसे मुश्किल रंग है... नीला।", tag="hook", sfx="whoosh", gap=.3),
    HL(V, "पटाखों के रंग, धातुओं से आते हैं। लाल स्ट्रॉन्शियम से, हरा बेरियम से, पीला सोडियम से।",
       "पटाखों के रंग धातुओं से आते हैं: लाल स्ट्रॉन्शियम, हरा बेरियम, पीला सोडियम।", tag="l1", sfx="tick"),
    HL(V, "और नीला? कॉपर से।", tag="l2", sfx="pop"),
    HL(V, "पर नीला रंग देने वाला कॉपर क्लोराइड, ज़्यादा गर्मी में टूट जाता है। और नीला, सफ़ेद पड़ जाता है।",
       "पर नीला रंग देने वाला कॉपर क्लोराइड ज़्यादा गर्मी में टूट जाता है, और नीला सफ़ेद पड़ जाता है।", speed=.95, tag="l3", drop=True),
    HL(V, "इसलिए एक्सपर्ट्स, साफ़ नीले को पटाखों का होली ग्रेल कहते हैं।", "इसलिए एक्सपर्ट्स साफ़ नीले को पटाखों का 'होली ग्रेल' कहते हैं।",
       pre=.3, pitch=.5, tag="l4", sfx="tick"),
    HL(V, "अगली बार गहरा नीला दिखे, तो समझना, किसी मास्टर का काम है।", tag="l5"),
    HL(V, "ये रील उस दोस्त को भेजो, जो हर दिवाली पटाखों का एक्सपर्ट बन जाता है।", tag="cta", sfx="pop", gap=.3),
]
COLS = {"red": (240, 60, 60), "green": (60, 220, 120), "yellow": (255, 220, 60), "blue": (70, 120, 255), "white": (240, 240, 255)}
def burst(d, cx, cy, r, col, k):
    for i in range(18):
        a = i / 18 * 2 * math.pi; rr = r * k
        d.line((cx + rr * .3 * math.cos(a), cy + rr * .3 * math.sin(a), cx + rr * math.cos(a), cy + rr * math.sin(a)), fill=col, width=5)
        d.ellipse((cx + rr * math.cos(a) - 5, cy + rr * math.sin(a) - 5, cx + rr * math.cos(a) + 5, cy + rr * math.sin(a) + 5), fill=col)
def fireworks(fr, t, R):
    d = fr.d; T = R.T
    seq = []
    if t >= T("l1"):
        L = R.line("l1"); ph = (t - L.t0) / (L.t1 - L.t0)
        seq = [("red", 220), ("green", 540), ("yellow", 860)][:1 + int(ph * 3)]
    if t >= T("l2"): seq = [("red", 220), ("green", 540), ("yellow", 860)] if t < T("l2") else seq + [("blue", 540)]
    if t >= T("l3"):
        L = R.line("l3"); fade = ease((t - L.t0 - (L.t1 - L.t0) * .45) / 1.0)
        b = tuple(int(COLS["blue"][i] + (COLS["white"][i] - COLS["blue"][i]) * fade) for i in range(3))
        seq = [("x", 540, b)]
    if t >= T("l4"): seq = [("blue", 540)]
    for item in seq:
        if item[0] == "x": _, x, col = item
        else: col = COLS[item[0]]; x = item[1]
        k = .6 + .4 * abs(math.sin(t * 2.2 + x))
        burst(d, x, 985, 80, col, k)
def scene(fr, t, R):
    card_scene(fr, t, R, "नीला = सबसे मुश्किल", "पटाखों का सबसे कठिन रंग", deco=fireworks, accent=(110, 150, 255),
               chips=["लाल · हरा · पीला = आसान", "नीला = कॉपर", "ज़्यादा गर्मी = रंग ग़ायब", "'होली ग्रेल'", "गहरा नीला = मास्टर का काम"],
               chip_tags=("l1", "l2", "l3", "l4", "l5"))
if __name__ == "__main__":
    R, p = build_dyk("DiwaliDYK_02_BlueFirework", LINES, scene, sys.argv[1], "भेजो!", "उस दोस्त को, जो हर\nदिवाली पटाखों का\nएक्सपर्ट बनता है।", "पटाखा एक्सपर्ट को भेजो", 92)
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
