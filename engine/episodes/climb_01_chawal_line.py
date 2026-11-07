"""Climb 01 · 'चावल के दाने एक लाइन में' — 1 grain on square 1, doubled each square, laid end to end (6 mm a grain).
Style: the user's reference scale-climb reel (music only). Facts checked 7 Nov 2026:
common Indian rice grain ~6 mm (IR64/Sharbati 6-6.15 mm); door ~2.1 m; Qutub Minar 72.5 m; Burj Khalifa 828 m;
Everest 8,849 m; Karman line 100 km; Moon 384,400 km; Sun 149.6 million km; Pluto ~5.9 billion km (avg);
Alpha Centauri 4.37 light-years. Line length after n squares = (2^n - 1) x 6 mm:
9 -> 3.07 m, 11 -> 12.3 m, 14 -> 98 m, 18 -> 1.57 km, 21 -> 12.6 km, 25 -> 201 km, 36 -> 412,317 km,
45 -> 211 million km, 50 -> 6.76 billion km, 63 -> 5.85 ly, 64 -> 11.7 ly."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from PIL import Image
from reel import Reel
import audio as A
import climb_kit as C

GRAIN = 0.006; LY = 9.4607e15
def to_m(v): return (2 ** v - 1) * GRAIN

def fmt(m, short=False):
    if m < 0.01: return f"{m * 1000:.0f} mm"
    if m < 1: return f"{m * 100:.0f} सेमी"
    if m < 1000: return (f"{m:.1f} मीटर" if m < 10 else f"{m:,.0f} मीटर") if not short else f"{m:.3g} मी"
    km = m / 1000
    if m > 0.05 * LY: return f"{m / LY:.1f} प्रकाश-वर्ष" if not short else f"{m / LY:.2g} ly"
    if km < 1e5: return f"{km:,.0f} किमी" if not short else f"{km:.3g} किमी"
    if km < 1e7: return f"{km / 1e5:.1f} लाख किमी" if not short else f"{km / 1e5:.3g} लाख किमी"
    if km < 1e9: return f"{km / 1e7:.1f} करोड़ किमी" if not short else f"{km / 1e7:.3g} करोड़ किमी"
    return f"{km / 1e9:.1f} अरब किमी" if not short else f"{km / 1e9:.3g} अरब किमी"

KEYS = [(0, 1), (1.6, 3), (4.0, 9), (6.4, 11), (8.8, 14), (11.2, 18), (13.6, 21), (16.0, 25), (19.0, 36), (22.0, 45), (25.0, 50), (28.6, 63), (31.2, 64)]
STORY = [(0, "शतरंज के पहले खाने पर एक दाना", "एक दाना"), (1.6, "…और हर खाने पर दोगुना", "दोगुना"),
         (4.0, "9 खाने: दरवाज़े से ऊँचा", "दरवाज़े"), (6.4, "11 खाने: घर से ऊँचा", "घर"),
         (8.8, "14 खाने: क़ुतुब मीनार के पार", "क़ुतुब मीनार"), (11.2, "18 खाने: बुर्ज ख़लीफ़ा के पार", "बुर्ज ख़लीफ़ा"),
         (13.6, "21 खाने: एवरेस्ट से ऊँचा", "एवरेस्ट"), (16.0, "25 खाने: अंतरिक्ष में!", "अंतरिक्ष"),
         (19.0, "36 खाने: चाँद तक!", "चाँद"), (22.0, "45 खाने: सूरज के पार", "सूरज"), (25.0, "50 खाने: प्लूटो के पार", "प्लूटो"),
         (28.6, "63 खाने: सबसे पास वाले तारे के पार", "तारे"), (31.2, "64 खाने: 11.7 प्रकाश-वर्ष!", "11.7 प्रकाश-वर्ष"),
         (34.0, "…सब एक चावल के दाने से", "एक चावल के दाने")]
CFG = dict(title=["चावल के दाने एक लाइन में", "64 खानों तक कितनी दूर?"], unit_word="खाना", keys=KEYS, value_to_m=to_m, fmt=fmt,
           max_value=64, min_view_m=0.03, obj_col=(120, 230, 210),
           objects=[("चावल का दाना", 0.006, "grain", "L"), ("दरवाज़ा", 2.1, "door", "L"), ("घर", 9, "house", "R"),
                    ("क़ुतुब मीनार", 72.5, "tower", "L"), ("बुर्ज ख़लीफ़ा", 828, "spire", "R"), ("एवरेस्ट", 8849, "mountain", "L")],
           markers=[("हवाई जहाज़", 10_000, "plane"), ("अंतरिक्ष", 100_000, "line"), ("चाँद", 3.844e8, "moon"), ("सूरज", 1.496e11, "sun"),
                    ("प्लूटो", 5.9e12, "planet"), ("अल्फ़ा सेंटॉरी", 4.37 * LY, "star")],
           story=STORY)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    DUR = 39.0
    R = Reel("Climb_01_ChawalLine", "space", [], tone="warm", seed=7)
    R.dur = DUR; R.voice = np.zeros(int(DUR * A.SR), dtype=np.float32)
    R.events = [(k[0], "tick") for k in KEYS[1:]] + [(16.0, "whoosh"), (19.0, "chime"), (31.2, "hit"), (34.0, "chime")]
    R.nudge = dict(text="दोस्त को भेजो", icon="send", at=round(DUR * .38, 2), bg=(240, 196, 110), fg=(20, 20, 40), fontfile=f"{C.FONTS}/Hind-Bold.ttf")
    R.cta = dict(at=35.2, icon="send", head="भेजो!", body="उस दोस्त को जो कहता है,\n'बस एक दाना ही तो है'", bg=(250, 246, 236), acc=(30, 120, 140),
                 fg=(20, 20, 40), fontfile=f"{C.FONTS}/Hind-Bold.ttf")
    BG = C.background()
    scene = lambda fr, t, R_: C.render_frame(fr, t, CFG, BG)
    stills = [.4, 1.2, 3.0, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.5, 23.5, 26.5, 30.0, 32.5, 34.5, 37.5]
    p = R.render(scene, out, stills=stills)
    print(p, DUR, "violations:", R.violations[:8], len(R.violations))
