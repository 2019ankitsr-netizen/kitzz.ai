"""Climb 01 (English) · 'One grain of rice, doubled on every square' — same facts and timing as climb_01_chawal_line.py."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from reel import Reel
import audio as A
import climb_kit as C
from climb_01_chawal_line import KEYS, to_m, LY

def fmt(m, short=False):
    if m < 0.01: return f"{m * 1000:.0f} mm"
    if m < 1: return f"{m * 100:.0f} cm"
    if m < 1000: return (f"{m:.1f} m" if m < 10 else f"{m:,.0f} m") if not short else (f"{m:,.0f} m" if m >= 100 else f"{m:.3g} m")
    km = m / 1000
    if m > 0.05 * LY: return f"{m / LY:.1f} light-years" if not short else f"{m / LY:.2g} ly"
    if km < 1e6: return f"{km:,.0f} km" if not short else (f"{km:,.0f} km" if km >= 100 else f"{km:.3g} km")
    if km < 1e9: return f"{km / 1e6:.1f} million km" if not short else f"{km / 1e6:.3g}M km"
    return f"{km / 1e9:.1f} billion km" if not short else f"{km / 1e9:.3g}B km"

STORY = [(0, "One grain of rice on square 1", "One grain"), (1.6, "…and double it every square", "double"),
         (4.0, "9 squares: taller than a door", "door"), (6.4, "11 squares: taller than a house", "house"),
         (8.8, "14 squares: past Qutub Minar", "Qutub Minar"), (11.2, "18 squares: past the Burj Khalifa", "Burj Khalifa"),
         (13.6, "21 squares: higher than Everest", "Everest"), (16.0, "25 squares: in SPACE", "SPACE"),
         (19.0, "36 squares: the MOON!", "MOON"), (22.0, "45 squares: past the Sun", "Sun"), (25.0, "50 squares: past Pluto", "Pluto"),
         (28.6, "63 squares: past the nearest star", "nearest star"), (31.2, "64 squares: 11.7 light-years!", "11.7 light-years"),
         (34.0, "…all from one grain of rice", "one grain of rice")]
CFG = dict(title=["One grain of rice, doubled every square.", "How far after 64 squares?"], unit_word="Square", keys=KEYS, value_to_m=to_m, fmt=fmt,
           max_value=64, min_view_m=0.03, obj_col=(120, 230, 210), earth_label="Earth",
           objects=[("Rice grain", 0.006, "grain", "L"), ("Door", 2.1, "door", "L"), ("House", 9, "house", "R"),
                    ("Qutub Minar", 72.5, "tower", "L"), ("Burj Khalifa", 828, "spire", "R"), ("Everest", 8849, "mountain", "L")],
           markers=[("Plane", 10_000, "plane"), ("Space", 100_000, "line"), ("Moon", 3.844e8, "moon"), ("Sun", 1.496e11, "sun"),
                    ("Pluto", 5.9e12, "planet"), ("Alpha Centauri", 4.37 * LY, "star")],
           story=STORY)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    DUR = 39.0
    R = Reel("Climb_01_RiceLine_EN", "space", [], tone="warm", seed=7)
    R.dur = DUR; R.voice = np.zeros(int(DUR * A.SR), dtype=np.float32)
    R.events = [(k[0], "tick") for k in KEYS[1:]] + [(16.0, "whoosh"), (19.0, "chime"), (31.2, "hit"), (34.0, "chime")]
    R.nudge = dict(text="Send to a friend", icon="send", at=round(DUR * .38, 2), bg=(240, 196, 110), fg=(20, 20, 40))
    R.cta = dict(at=35.2, icon="send", head="Send this!", body="to the friend who says\n\"it's just one grain\"", bg=(250, 246, 236), acc=(30, 120, 140), fg=(20, 20, 40))
    BG = C.background()
    scene = lambda fr, t, R_: C.render_frame(fr, t, CFG, BG)
    stills = [.4, 3.0, 7.5, 12.5, 17.5, 20.5, 23.5, 30.0, 32.5, 37.5]
    p = R.render(scene, out, stills=stills)
    print(p, DUR, "violations:", R.violations[:8], len(R.violations))
