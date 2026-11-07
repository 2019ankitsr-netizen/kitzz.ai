"""Diwali Did You Know · 01 · Kukur Tihar (dogs are worshipped in Nepal's Diwali)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from dyk_kit import *
LINES = [
    HL(V, "क्या आप जानते हैं? नेपाल में दिवाली पर, कुत्तों की पूजा होती है।", tag="hook", sfx="whoosh", gap=.3),
    HL(V, "नेपाल में दिवाली को तिहार कहते हैं। पाँच दिन का त्योहार।", tag="l1", sfx="tick"),
    HL(V, "और इसका एक दिन है, कुकुर तिहार। कुत्तों को माला, टीका, और ख़ास खाना मिलता है।", tag="l2", sfx="tick"),
    HL(V, "सिर्फ़ पालतू नहीं, गली के कुत्तों को भी।", tag="l3", sfx="pop"),
    HL(V, "और नेपाल पुलिस के डॉग्स को भी, पूरे सम्मान के साथ।", pre=.3, pitch=.5, tag="l4", sfx="tick"),
    HL(V, "क्योंकि वफ़ादारी का भी, एक त्योहार होना चाहिए।", tag="l5", drop=True),
    HL(V, "ये रील उस दोस्त को भेजो, जिसका डॉगी उसकी जान है।", tag="cta", sfx="pop", gap=.3),
]
import math
def dog(fr, t, R):
    if t < R.T("l2") - .1: return
    k = eback((t - R.T("l2")) / .5); d = fr.d; cx, cy = 540, 972 + (1 - k) * 80; s = .78 * min(1, k)
    if s <= 0.05: return
    wag = math.sin(t * 6) * 4
    d.ellipse((cx - 130 * s, cy - 40 * s, cx - 60 * s, cy + 90 * s), fill=(120, 70, 40))          # ears
    d.ellipse((cx + 60 * s, cy - 40 * s, cx + 130 * s, cy + 90 * s), fill=(120, 70, 40))
    d.ellipse((cx - 100 * s, cy - 90 * s, cx + 100 * s, cy + 90 * s), fill=(200, 140, 80))       # head
    d.ellipse((cx - 55 * s, cy + 5 * s, cx + 55 * s, cy + 85 * s), fill=(240, 210, 170))         # muzzle
    for ex in (-40, 40): d.ellipse((cx + ex * s - 13 * s, cy - 30 * s, cx + ex * s + 13 * s, cy - 4 * s), fill=(30, 20, 15))
    d.ellipse((cx - 18 * s, cy + 18 * s, cx + 18 * s, cy + 42 * s), fill=(30, 20, 15))           # nose
    d.ellipse((cx - 14 * s, cy + 52 * s + wag * .3, cx + 14 * s, cy + 86 * s + wag * .3), fill=(230, 90, 100))   # tongue
    d.ellipse((cx - 9 * s, cy - 70 * s, cx + 9 * s, cy - 48 * s), fill=(220, 20, 40))            # tika
    for i in range(13):                                                                          # marigold garland
        a = math.pi * (.15 + .7 * i / 12); gx, gy = cx + 120 * s * math.cos(a), cy + 70 * s + 45 * s * math.sin(a)
        d.ellipse((gx - 15 * s, gy - 15 * s, gx + 15 * s, gy + 15 * s), fill=(255, 150, 20) if i % 2 else (255, 200, 40))
def scene(fr, t, R):
    card_scene(fr, t, R, "कुत्तों की पूजा", "नेपाल का कुकुर तिहार", deco=dog, chips=
               ["तिहार = नेपाल की दिवाली", "माला · टीका · दावत", "गली के कुत्ते भी", "पुलिस डॉग्स भी", "वफ़ादारी का त्योहार"],
               chip_tags=("l1", "l2", "l3", "l4", "l5"))
if __name__ == "__main__":
    R, p = build_dyk("DiwaliDYK_01_KukurTihar", LINES, scene, sys.argv[1], "भेजो!", "उस दोस्त को, जिसका\nडॉगी उसकी जान है।", "डॉग लवर को भेजो", 91)
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
