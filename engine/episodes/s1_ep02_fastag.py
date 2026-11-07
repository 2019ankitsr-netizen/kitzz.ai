"""S1 How Things Work · Ep 02 · FASTag toll."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from reel import Line
import s1_kit
M = "am_michael"
LINES = [
    Line(M, "The toll gate charged you before you even braked.", speed=1.06, pitch=.5, tag="hook", sfx="whoosh", gap=.25),
    Line(M, "Here's what happened in those few seconds.", tag="route", gap=.4, sfx="whoosh"),
    Line(M, "Stop one. | The sticker on your windscreen is a FASTag. | A tiny radio chip, | with no battery.",
         "Stop 1: the sticker on your windscreen is a FASTag. A tiny radio chip with no battery.", tag="s1", sfx="tick"),
    Line(M, "Stop two. | A reader above the lane powers it up with radio waves, | and reads its ID.",
         "Stop 2: a reader above the lane powers it with radio waves and reads its ID.", tag="s2", sfx="tick"),
    Line(M, "Stop three. | The toll plaza's bank asks NPCI: | whose tag is this, | and is it valid?",
         "Stop 3: the toll plaza's bank asks NPCI: whose tag is this, and is it valid?", speed=.96, pitch=-1, tag="s3", drop=True, sfx="tick"),
    Line(M, "Blacklisted tag? | The lane won't accept it.", speed=.95, pitch=-1, tag="block", drop=True, gap=.3),
    Line(M, "If it's fine, | the toll is worked out from your vehicle type, | and NPCI sends the debit to your bank.",
         "If it's fine, the toll is set by your vehicle type, and NPCI sends the debit to your bank.", pre=.45, pitch=1, tag="s4", sfx="whoosh"),
    Line(M, "Tag. | Reader. | Plaza bank. | NPCI. | Your bank. | Then an SMS to your phone.",
         "Tag. Reader. Plaza bank. NPCI. Your bank. Then an SMS to your phone.", speed=.95, tag="payoff", gap=.4),
    Line(M, "That's why one FASTag works at every participating toll plaza in India.", tag="never"),
    Line(M, "Save it. | Send it to the friend who still pays tolls in cash.", tone="bright", tag="cta", sfx="pop", gap=.2),
    Line(M, "Now watch that barrier open again.", tone="bright", tag="loop", gap=.1),
]
CFG = dict(name="S1_HowThingsWork_ep02_FASTag", ep=2, title="The FASTag route", hook_text="Charged before\nyou even braked.",
           chip="TAG 34161FA8", banner="One tag. Every NETC\ntoll plaza.",
           stops=[("STOP 01", "Your FASTag", (70, 60, 140), (170, 140, 255)), ("STOP 02", "Lane reader", (30, 110, 120), (90, 230, 220)),
                  ("STOP 03", "Plaza's bank", (120, 80, 30), (255, 190, 80)), ("STOP 04", "NPCI", (40, 70, 130), (90, 160, 255)),
                  ("STOP 05", "Your bank", (110, 40, 90), (255, 120, 200))],
           seq=[("s1", 0), ("s2", 1), ("s3", 2), ("block", 3), ("s4", 3)], wave=(1, "s2"), block_tag="block", block_stop=3, rest=0,
           clock=None, cta_body="Send it to the friend\nwho still pays tolls\nin cash.")
if __name__ == "__main__":
    R, p = s1_kit.build(CFG, LINES, sys.argv[1]); print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
