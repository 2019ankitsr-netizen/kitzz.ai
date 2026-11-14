"""Scout sample 3 (14 Nov 2026): S3 CCTV Riddles with word-pop captions coloured by speaker. ~15 s test clip."""
import os, sys, math
HERE = os.path.dirname(__file__); ENG = os.path.join(HERE, "..", "..")
sys.path[:0] = [ENG, os.path.join(ENG, "pilots"), os.path.join(ENG, "episodes")]
from PIL import ImageDraw
from reel import ease
from wordpop import WordPopReel
from s3_kit import DL, EL, D, E, cctv_finish, glitch, F, FM
import s3_case03_surgeon as C3

LINES = [
    EL("CCTV log. | Camera four. | City hospital.", "CCTV log. Cam 04. City Hospital.", tag="log", sfx="beep", gap=.25),
    DL("A boy is rushed into surgery.", tag="rush", sfx="tick", gap=.2),
    DL("The surgeon walks in and says: | I can't operate. | He's my son.", "The surgeon walks in and says: I can't operate. He's my son.", tag="says", gap=.25),
    EL("The father is across town.", tag="alibi", sfx="beep", gap=.25),
    DL("So who is the surgeon?", speed=.95, tag="ask", drop=True, sfx="static", gap=.4),
]

def scene(fr, t, R):
    C3.cctv(fr, t, R)
    glitch(fr, t, [R.T("alibi") - .1, R.T("ask") - .1])
    fr.text((90, 420), "SAMPLE · WORD-POP CAPTIONS", FM(28), (255, 220, 80))

if __name__ == "__main__":
    out = sys.argv[1]
    R = WordPopReel("S3_sample_wordpop", "cctv", LINES, tone="warm", seed=33)
    R.cap_style.update(fg=(255, 255, 255), bg=(0, 0, 0, 205), font="black", size=58, lh=72)
    R.speaker_style = {D: dict(col=(255, 205, 60), who="DETECTIVE"), E: dict(col=(110, 225, 255), who="CCTV LOG")}
    dur = R.build_audio(f"{out}/cache")
    # C3.cctv uses the "rush" and "says" tags for the stretcher + surgeon moves
    stills = sorted([L.t0 + f for L in LINES for f in (.05, .12, .6)] + [dur - .3])
    p = R.render(scene, out, stills=stills)
    print(p, round(dur, 1), "s violations:", R.violations[:6], len(R.violations))
