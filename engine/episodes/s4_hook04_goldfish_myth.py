"""S4 Hook Shots · 04 · The 8-second goldfish attention span is a myth."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from s4_kit_build import *
LINES = [
    Line(V, "You have an 8-second attention span? | Fake.", "You have an 8-second attention span? Fake.", speed=1.04, tag="hook", sfx="hit", gap=.2),
    Line(V, "You've heard it: | shorter than a goldfish.", tag="heard", sfx="whoosh"),
    Line(V, "It spread from a 2015 Microsoft Canada report.", tag="report", sfx="tick"),
    Line(V, "But the number wasn't Microsoft's own research. | It was credited to a website called Statistic Brain.",
         "But the number wasn't Microsoft's own research. It was credited to a website, Statistic Brain.", tag="source", sfx="tick"),
    Line(V, "When the BBC checked in 2017, | no one could find the study behind it.", pre=.25, pitch=1, tag="bbc", drop=True),
    Line(V, "And the goldfish? | There's no study behind that number either.", tag="fish", sfx="tick"),
    Line(V, "Send this to the friend who still quotes it.", tag="cta", sfx="pop", gap=.2),
    Line(V, "Eight seconds. | Still believe it?", tag="loop", gap=.05),
]
def scene(fr, t, R):
    d, L, tag, t0, ph = frame_start(fr, t, R, "HOOK SHOT 04")
    if tag in ("hook", "loop"):
        dx, _ = slide(t, max(0, t0 - .05)); fr.text((80 + dx, 360), "8 sec", F("black", 290), INK)
        if tag == "loop" or ph > .55:
            d.rectangle((70, 690, 560, 850), fill=RED); fr.text((100, 705), "FAKE", F("black", 120), (255, 255, 255))
    elif tag == "heard":
        fish(d, 300, 520, 2.2, (240, 140, 40)); fr.text((90, 740), "8 s  <  9 s ?", F("black", 120), INK)
    elif tag == "report":
        dx, _ = slide(t, t0); fr.text((80 - dx, 380), "2015", F("black", 260), INK); fr.text((90, 680), "Microsoft Canada\nreport", F("black", 84), RED, spacing=4)
    elif tag == "source":
        fr.text((84, 380), "Source:", F("xb", 72), GREY); fr.text((84, 480), "Statistic Brain", F("black", 110), INK)
        if ph > .25: fr.text((84, 660), "Not Microsoft's\nown research.", F("black", 84), RED, spacing=4)
    elif tag == "bbc":
        dx, _ = slide(t, t0); fr.text((80 + dx, 380), "BBC · 2017", F("black", 140), INK)
        fr.text((84, 600), "Study behind it?", F("xb", 72), INK); fr.text((84, 700), "Not found.", F("black", 120), RED)
    elif tag == "fish":
        fish(d, 260, 520, 1.8, GREY); fr.text((520, 440), "9 s?", F("black", 160), INK)
        if ph > .4: fr.text((90, 720), "No study either.", F("black", 96), RED)
    elif tag == "cta":
        fr.text((70, 360), "8 sec", F("black", 150), GREY)
if __name__ == "__main__":
    R, p = build("S4_HookShots_04_GoldfishMyth", 4, LINES, scene, sys.argv[1], "Send this to someone", "to the friend who\nstill quotes it.")
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
