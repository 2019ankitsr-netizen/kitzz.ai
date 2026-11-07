"""S3 CCTV Riddles · Case 02 · Three switches, one bulb (opens with Case 01's answer)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from PIL import Image, ImageDraw
from s3_kit import DL, EL, cctv_finish, board_base, draw_cards, glitch, hook_box, build, person, F, FM
from reel import ease, eout, W, H
LINES = [
    DL("Three switches. | One bulb. | One look.", "3 switches. 1 bulb. 1 look.", speed=1.05, tag="hook", sfx="static", gap=.25),
    EL("Case one, solved.", tag="solved", sfx="beep", gap=.2),
    DL("The ₹27 already included the helper's ₹2. | Add the ₹3 given back, not the ₹2. | Nothing was missing.",
       "₹27 already included the helper's ₹2. Add the ₹3 given back, not the ₹2. Nothing was missing.", tag="ans"),
    EL("CCTV log. | Camera one. | Building basement. | Twenty-two zero five.", "CCTV log · Cam 01 · Basement · 22:05", tag="log", sfx="beep", gap=.3),
    DL("Three switches on the basement wall. | Only one of them works a bulb, | in a closed room upstairs.",
       "3 switches on the basement wall. Only one works a bulb in a closed room upstairs.", tag="setup", sfx="tick"),
    DL("From down here, | you can't see that bulb. | Flip the switches as much as you like. | But you can go upstairs only once.",
       "From down here you can't see the bulb. Flip the switches all you like. But you can go up only once.", tag="rule"),
    DL("One trip. | Three switches. | How do you know which one it is?", "One trip. 3 switches. How do you know which one it is?",
       speed=.95, pitch=-.5, tag="ask", drop=True, sfx="static"),
    DL("Light isn't the only clue.", pre=.5, pitch=1, tag="hint", sfx="hit", gap=.4),
    DL("Rewind the tape. | Watch the wall clock.", tag="clue"),
    DL("Answer in the comments. | Send it to the smartest person you know.", tag="cta", sfx="pop", gap=.25),
    DL("Three switches. | One bulb. | Still dark upstairs.", "3 switches. 1 bulb. Still dark upstairs.", tag="loop", gap=.1),
]
def base():
    im = Image.new("RGB", (W, H), (36, 38, 36)); d = ImageDraw.Draw(im)
    d.rectangle((70, 280, 1010, 1240), fill=(50, 52, 48))
    for y in range(700, 1240, 60): d.line((70, y, 1010, y), fill=(56, 58, 54), width=2)
    d.rectangle((70, 420, 1010, 700), fill=(66, 68, 62))                                 # wall
    for i in range(6): d.polygon([(780 + i * 34, 700 - i * 40), (1010, 700 - i * 40), (1010, 740 - i * 40), (780 + i * 34, 740 - i * 40)], fill=(80, 82, 76))  # stairs
    d.rectangle((200, 470, 560, 620), fill=(90, 92, 85), outline=(120, 122, 114), width=4)  # switch panel
    return im
BASE = base()
def switches(d, t, R):
    rule = R.line("rule"); states = [0, 0, 0]
    if t >= rule.t0:
        k = int((t - rule.t0) / .7); states = [(k + i) % 2 for i in range(3)]
    for i, s in enumerate(states):
        x = 250 + i * 110; d.rectangle((x, 500, x + 60, 590), fill=(60, 62, 58))
        d.rectangle((x + 12, 510 if s else 548, x + 48, 552 if s else 580), fill=(200, 200, 190))
def clock(d, t, cx=680, cy=530, r=60):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(200, 200, 190), outline=(90, 90, 85), width=5)
    a = math.radians(t * 30 - 90); d.line((cx, cy, cx + r * .8 * math.cos(a), cy + r * .8 * math.sin(a)), fill=(30, 30, 30), width=5)
    a2 = math.radians(t * 2.5 - 90); d.line((cx, cy, cx + r * .5 * math.cos(a2), cy + r * .5 * math.sin(a2)), fill=(30, 30, 30), width=7)
def cctv(fr, t, R):
    fr.img = BASE.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    switches(d, t, R); clock(d, t)
    px = 380 + (math.sin(t * 1.3) * 60 if t >= R.T("rule") else 0); person(d, px, 760, 46, (150, 152, 140))
    cctv_finish(fr, t, cam="CAM 01", start=(22, 5, 3))
def scene(fr, t, R):
    T = R.T; ans_end = T("log") - .1; ask, clue = T("ask") - .15, R.line("clue")
    if T("solved") - .15 <= t < ans_end:
        board_base(fr, "CASE #01 · SOLVED")
        a = R.line("ans")
        draw_cards(fr, t, [("₹25 bill + ₹2 helper\n= ₹27 paid", (100, 360, 900, 540), a.t0 + .2, "answer"),
                           ("₹27 + ₹3 back = ₹30", (100, 620, 900, 760), a.t0 + (a.t1 - a.t0) * .45, "answer"),
                           ("Nothing missing.", (100, 840, 700, 960), a.t0 + (a.t1 - a.t0) * .8, "note")])
    elif ask <= t < clue.t0 or (T("cta") - .1 <= t < T("loop")):
        board_base(fr, "CASE #02 · EVIDENCE")
        a = R.line("ask")
        draw_cards(fr, t, [("3 switches", (100, 340, 480, 450), a.t0 + .1, "note"), ("1 bulb, upstairs", (540, 360, 930, 470), a.t0 + .35, "note"),
                           ("Go up only ONCE", (100, 540, 620, 650), a.t0 + .6, "note"), ("Which switch?", (180, 790, 880, 930), a.t0 + (a.t1 - a.t0) * .7, "key")])
        h = R.line("hint")
        if h.t0 - .1 <= t < clue.t0: fr.text((540, 1000), "Not just light...", F("black", 70), (255, 220, 80), anchor="mm")
    else:
        cctv(fr, t, R)
        if clue.t0 + .6 <= t < T("cta"):
            k = ease((t - clue.t0 - .6) / .6); fr.d.arc((600, 450, 760, 610), -90, -90 + 360 * k, fill=(255, 215, 0), width=8)
    glitch(fr, t, [T("solved") - .15, ans_end, ask, clue.t0, T("cta") - .1, T("loop")])
    hook_box(fr, t, "3 switches. 1 bulb.\nOne look.", T("solved") - .15)
if __name__ == "__main__":
    R, p = build("S3_CCTVRiddle_case02_ThreeSwitches", 2, LINES, scene, sys.argv[1], ["hook", "solved", "ans", "log", "setup", "rule", "ask", "hint", "clue", "cta", "loop"])
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
