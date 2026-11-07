"""S4 Hook Shots · 03 · Your phone vs the Moon-landing computer."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from s4_kit_build import *
LINES = [
    Line(V, "Your phone. | Versus the computer that landed on the Moon.", speed=1.04, tag="hook", sfx="hit", gap=.2),
    Line(V, "Apollo 11's guidance computer had about 4 KB of working memory.", "Apollo 11's guidance computer had about 4 KB of working memory (RAM).", tag="ram", sfx="whoosh"),
    Line(V, "That's smaller than one photo on your phone.", tag="photo", sfx="tick"),
    Line(V, "A phone with 4 GB of RAM | has over a million times more.", "A phone with 4 GB of RAM has over a million times more.", tag="million", sfx="tick"),
    Line(V, "And still, | with that tiny computer, | they landed on the Moon in 1969.", pre=.25, pitch=1, tag="still", drop=True),
    Line(V, "It's not the hardware. | It's what you do with it.", tag="moral", sfx="tick"),
    Line(V, "Send this to the friend who says their phone is too slow.", tag="cta", sfx="pop", gap=.2),
    Line(V, "Now look at your phone again.", tag="loop", gap=.05),
]
def scene(fr, t, R):
    d, L, tag, t0, ph = frame_start(fr, t, R, "HOOK SHOT 03")
    if tag in ("hook", "loop"):
        dx, _ = slide(t, max(0, t0 - .05))
        fr.text((80 + dx, 380), "PHONE", F("black", 200), INK)
        if tag == "loop" or ph > .3: fr.text((84, 600), "vs", F("black", 110), RED); fr.text((80, 740), "APOLLO 11", F("black", 150), INK)
    elif tag == "ram":
        dx, _ = slide(t, t0); fr.text((80 - dx, 360), "4 KB", F("black", 300), INK); fr.text((90, 700), "of RAM. In 1969.", F("xb", 72), RED)
    elif tag == "photo":
        dx, _ = slide(t, t0)
        d.rectangle((90, 380, 460, 640), outline=INK, width=10); d.polygon([(110, 620), (230, 470), (330, 580), (380, 520), (440, 620)], fill=GREY)
        fr.text((520 - dx, 400), "1 photo", F("black", 110), INK); fr.text((520, 540), "> 4 KB", F("black", 110), RED)
        fr.text((92, 720), "Your phone saves bigger\nfiles every second.", F("xb", 56), INK, spacing=8)
    elif tag == "million":
        k = eout((t - t0) / .3); fr.text((70 + (1 - k) * 40, 380), "×1,000,000+", F("black", 122), RED)
        fr.text((90, 600), "4 GB phone RAM vs", F("xb", 64), INK); fr.text((90, 690), "4 KB Apollo RAM", F("xb", 64), INK)
    elif tag == "still":
        dx, _ = slide(t, t0); fr.text((70 - dx, 380), "1969", F("black", 320), INK); fr.text((90, 760), "Moon landing. Done.", F("black", 84), RED)
    elif tag == "moral":
        fr.text((80, 400), "Not the\nhardware.", F("black", 120), GREY, spacing=0)
        if ph > .45: fr.text((80, 700), "What you do\nwith it.", F("black", 110), RED, spacing=0)
    elif tag == "cta":
        fr.text((70, 360), "4 KB", F("black", 150), GREY)
if __name__ == "__main__":
    R, p = build("S4_HookShots_03_MoonComputer", 3, LINES, scene, sys.argv[1], "Send this to someone", "to the friend who says\ntheir phone is slow.")
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
