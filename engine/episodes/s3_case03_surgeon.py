"""S3 CCTV Riddles · Case 03 · "He's my son" (opens with Case 02's answer)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from PIL import Image, ImageDraw
from s3_kit import DL, EL, cctv_finish, board_base, draw_cards, glitch, hook_box, build, person, F, FM
from reel import ease, eout, W, H
LINES = [
    DL("The surgeon looked at the boy and said: | I can't operate. | He's my son.", "The surgeon looked at the boy and said: I can't operate. He's my son.",
       speed=1.05, tag="hook", sfx="static", gap=.25),
    EL("Case two, solved.", tag="solved", sfx="beep", gap=.2),
    DL("Switch one on for ten minutes, then off. | Switch two on, and go up. | Lit? Two. | Off but warm? One. | Cold? Three.",
       "Switch 1 on for 10 min, then off. Switch 2 on, go up. Lit? 2. Off but warm? 1. Cold? 3.", tag="ans"),
    EL("CCTV log. | Camera four. | City hospital. | Zero two forty.", "CCTV log · Cam 04 · City Hospital · 02:40", tag="log", sfx="beep", gap=.3),
    DL("A father and his son are hurt in a road accident. | The father is taken to a hospital across town.",
       "A father and son are hurt in a road accident. The father goes to a hospital across town.", tag="setup", sfx="tick"),
    DL("The boy is rushed here, to City Hospital, | straight into surgery.", "The boy is rushed to City Hospital, straight into surgery.", tag="rush"),
    DL("The surgeon walks in, looks at him, and says: | I can't operate on this boy. | He's my son.",
       "The surgeon walks in, looks at him and says: I can't operate on this boy. He's my son.", tag="says"),
    DL("The father is across town. | So who is the surgeon?", speed=.95, pitch=-.5, tag="ask", drop=True, sfx="static"),
    DL("Rewind the tape. | Then ask yourself who you pictured.", pre=.5, pitch=1, tag="clue", sfx="hit"),
    DL("Answer in the comments. | Send it to the smartest person you know.", tag="cta", sfx="pop", gap=.25),
    DL("I can't operate. | He's my son. | Who said it?", tag="loop", gap=.1),
]
def base():
    im = Image.new("RGB", (W, H), (36, 40, 40)); d = ImageDraw.Draw(im)
    d.polygon([(380, 420), (700, 420), (1010, 1240), (70, 1240)], fill=(70, 78, 76))          # corridor floor
    for y in range(440, 1240, 80):
        w = (y - 420) / 820; d.line((380 - 310 * w, y, 700 + 310 * w, y), fill=(78, 86, 84), width=2)
    for side in (0, 1):
        for i, y in enumerate((470, 620, 820)):
            w = (y - 420) / 820; x = 380 - 310 * w if side == 0 else 700 + 310 * w
            d.rectangle((x - 30 if side else x - 10, y, x + 10 if side else x + 30, y + 90), fill=(110, 116, 112))
    d.rectangle((460, 300, 620, 420), fill=(90, 96, 94)); d.rectangle((470, 315, 610, 345), fill=(200, 60, 60))   # OT door + light
    return im
BASE = base()
def cctv(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    rush = R.line("rush"); says = R.line("says")
    k = ease((t - rush.t0) / max(1, rush.t1 - rush.t0)) if t >= rush.t0 else 0
    sy = 1100 - 560 * k                                                                            # stretcher moves up the corridor
    d.rounded_rectangle((470, sy - 90, 610, sy + 90), 18, fill=(205, 210, 205)); d.ellipse((510, sy - 80, 570, sy - 20), fill=(150, 152, 140))
    person(d, 420, sy + 60, 34, (140, 146, 140)); person(d, 660, sy + 60, 34, (140, 146, 140))
    if t >= says.t0 - .5:
        ks = ease((t - says.t0 + .5) / 1.0); person(d, 540, 470 + 40 * ks, 40, (120, 160, 150))     # surgeon in scrubs
        d.ellipse((520, 450 + 40 * ks, 560, 470 + 40 * ks), fill=(90, 130, 120))
    cctv_finish(fr, t, cam="CAM 04", start=(2, 40, 10))
def scene(fr, t, R):
    T = R.T; ans_end = T("log") - .1; ask, clue = T("ask") - .15, R.line("clue")
    if T("solved") - .15 <= t < ans_end:
        board_base(fr, "CASE #02 · SOLVED")
        a = R.line("ans"); dur = a.t1 - a.t0
        draw_cards(fr, t, [("Switch 1: ON 10 min,\nthen OFF", (100, 340, 900, 500), a.t0 + .2, "answer"),
                           ("Switch 2: ON. Go up.", (100, 570, 900, 680), a.t0 + dur * .32, "answer"),
                           ("Lit = 2 · Warm = 1\nCold = 3", (100, 750, 900, 920), a.t0 + dur * .55, "note")])
    elif ask <= t < clue.t0 or (T("cta") - .1 <= t < T("loop")):
        board_base(fr, "CASE #03 · EVIDENCE")
        a = R.line("ask"); s0 = R.T("setup")
        draw_cards(fr, t, [("Father: across town", (100, 340, 640, 450), a.t0 + .1, "note"), ("Boy: City Hospital", (380, 520, 930, 630), a.t0 + .3, "note"),
                           ("Surgeon: \"He's my son\"", (100, 700, 830, 810), a.t0 + .5, "note"), ("Who is the surgeon?", (150, 880, 900, 1010), a.t0 + (a.t1 - a.t0) * .6, "key")])
    else:
        cctv(fr, t, R)
        if clue.t0 + .6 <= t < T("cta"):
            k = ease((t - clue.t0 - .6) / .6); fr.d.arc((450, 400, 630, 600), -90, -90 + 360 * k, fill=(255, 215, 0), width=8)
    glitch(fr, t, [T("solved") - .15, ans_end, ask, clue.t0, T("cta") - .1, T("loop")])
    hook_box(fr, t, "\"I can't operate.\nHe's my son.\"", T("solved") - .15)
if __name__ == "__main__":
    R, p = build("S3_CCTVRiddle_case03_HesMySon", 3, LINES, scene, sys.argv[1], ["hook", "solved", "ans", "log", "setup", "rush", "says", "ask", "clue", "cta", "loop"])
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
