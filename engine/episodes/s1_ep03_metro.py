"""S1 How Things Work · Ep 03 · Metro token."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from reel import Line
import s1_kit
M = "am_michael"
LINES = [
    Line(M, "How does the metro gate know where you got in?", speed=1.06, pitch=.5, tag="hook", sfx="whoosh", gap=.25),
    Line(M, "The answer is inside your token.", tag="route", gap=.4, sfx="whoosh"),
    Line(M, "Stop one. | That plastic token is a contactless chip. | It's sold for one trip, | and it carries the fare you paid.",
         "Stop 1: that plastic token is a contactless chip. Sold for one trip, it carries the fare you paid.", tag="s1", sfx="tick"),
    Line(M, "Stop two. | At the entry gate, you hold it near the reader. | The gate checks it, | and the flaps open.",
         "Stop 2: at the entry gate, you hold it near the reader. The gate checks it and the flaps open.", tag="s2", sfx="tick"),
    Line(M, "Stop three. | Your ride. | The token is still carrying your trip: | where it was bought, and what was paid.",
         "Stop 3: your ride. The token still carries your trip: where it was bought, and what was paid.", speed=.96, pitch=-1, tag="s3", drop=True, sfx="tick"),
    Line(M, "Wrong station for that fare? | The exit gate won't open.", speed=.95, pitch=-1, tag="block", drop=True, gap=.3),
    Line(M, "And at the exit, you don't tap it. | You drop it in. | The gate keeps your token, | so it can be used again.",
         "At the exit you don't tap it. You drop it in. The gate keeps it, so it can be used again.", pre=.45, pitch=1, tag="s4", sfx="whoosh"),
    Line(M, "Buy. | Tap in. | Ride. | Drop. | Reuse. | Every single day.", "Buy. Tap in. Ride. Drop. Reuse. Every single day.", speed=.95, tag="payoff", gap=.4),
    Line(M, "A smart card works the same way, | but your fare is cut from the balance when you exit.",
         "A smart card works the same way, but the fare is cut from your balance at the exit.", tag="never"),
    Line(M, "Save it. | Send it to the friend who always loses their token.", tone="bright", tag="cta", sfx="pop", gap=.2),
    Line(M, "Now watch that gate open again.", tone="bright", tag="loop", gap=.1),
]
CFG = dict(name="S1_HowThingsWork_ep03_MetroToken", ep=3, title="The token's trip", hook_text="How does the gate\nknow where you got in?",
           chip="TOKEN ₹30", banner="Smart card? Fare is\ncut at the exit.",
           stops=[("STOP 01", "Ticket counter", (70, 60, 140), (170, 140, 255)), ("STOP 02", "Entry gate", (30, 110, 120), (90, 230, 220)),
                  ("STOP 03", "Your ride", (120, 80, 30), (255, 190, 80)), ("STOP 04", "Exit gate", (40, 70, 130), (90, 160, 255)),
                  ("STOP 05", "Used again", (110, 40, 90), (255, 120, 200))],
           seq=[("s1", 0), ("s2", 1), ("s3", 2), ("block", 3), ("s4", 3)], wave=(1, "s2"), block_tag="block", block_stop=3, rest=0,
           clock=None, cta_body="Send it to the friend\nwho always loses\ntheir token.")
if __name__ == "__main__":
    R, p = s1_kit.build(CFG, LINES, sys.argv[1]); print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
