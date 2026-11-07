"""S1 How Things Work · Ep 01 · OTP delivery — Isometric X-Ray Cutaway."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reel import Reel, Line, F, FM, ease, eout, eback, W, H

M = "am_michael"
LINES = [
    Line(M, "This six-digit code reached you in about three seconds.", "This 6-digit code reached you in about 3 seconds.", speed=1.06, pitch=.5, tag="hook", sfx="whoosh", gap=.25),
    Line(M, "Here's the route it took.", tag="route", gap=.4, sfx="whoosh"),
    Line(M, "Stop one. | Your bank's server picks six random digits, | and starts a short timer.",
         "Stop 1: your bank's server picks 6 random digits and starts a short timer.", tag="s1", sfx="tick"),
    Line(M, "Stop two. | It hands the code to an SMS gateway, | with a sender ID and a message template, | registered with TRAI.",
         "Stop 2: it goes to an SMS gateway, with a sender ID and a template registered with TRAI.", tag="s2", sfx="tick"),
    Line(M, "Stop three. | Your telecom operator checks that registry, | a shared ledger called DLT.",
         "Stop 3: your telecom operator checks that registry, a shared ledger called DLT.", speed=.96, pitch=-1, tag="s3", drop=True, sfx="tick"),
    Line(M, "Wrong sender, | or a template that doesn't match? | Blocked.", "Wrong sender, or a template that doesn't match? Blocked.",
         speed=.95, pitch=-1, tag="block", drop=True, gap=.3),
    Line(M, "Then, the operator's message centre finds the tower your phone is connected to, | and sends the code through the air.",
         "Then the message centre finds the tower your phone is on, and sends the code through the air.", pre=.45, pitch=1, tag="s4", sfx="whoosh"),
    Line(M, "Bank. | Gateway. | Ledger. | Tower. | Phone. | All in a few seconds.", "Bank. Gateway. Ledger. Tower. Phone. All in a few seconds.",
         speed=.95, tag="payoff", gap=.4),
    Line(M, "That's why a bank never asks you for it. | The code works once, | and only for you.",
         "That's why a bank never asks you for it. It works once, and only for you.", tag="never"),
    Line(M, "Save it. | Send it to the friend who reads OTPs out loud on calls.", "Save it. Send it to the friend who reads OTPs out loud on calls.",
         tone="bright", tag="cta", sfx="pop", gap=.2),
    Line(M, "Now watch that code land again.", tone="bright", tag="loop", gap=.1),
]

STOPS = [("STOP 01", "Bank server", (70, 60, 140), (170, 140, 255)),
         ("STOP 02", "SMS gateway", (30, 110, 120), (90, 230, 220)),
         ("STOP 03", "DLT check", (120, 80, 30), (255, 190, 80)),
         ("STOP 04", "Mobile tower", (40, 70, 130), (90, 160, 255)),
         ("STOP 05", "Your phone", (110, 40, 90), (255, 120, 200))]
CX, SW, SH, ST = 320, 250, 62, 24
YOPEN = [520, 640, 760, 880, 1000]

def bg():
    im = Image.new("RGB", (W, H), (10, 18, 38)); d = ImageDraw.Draw(im)
    for x in range(-W, 2 * W, 60):
        d.line((x, 0, x + H * .577, H), fill=(20, 33, 64), width=1); d.line((x, 0, x - H * .577, H), fill=(20, 33, 64), width=1)
    v = Image.new("L", (W, H), 0); vd = ImageDraw.Draw(v); vd.ellipse((-300, -200, W + 300, H + 200), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(180))
    return Image.composite(im, Image.new("RGB", (W, H), (4, 8, 18)), v)
BG = bg()

def slab(d, y, col, edge, glow, a=1.0):
    top = [(CX, y - SH), (CX + SW, y), (CX, y + SH), (CX - SW, y)]
    mul = lambda c, k: tuple(int(v * k) for v in c)
    d.polygon([(CX - SW, y), (CX, y + SH), (CX, y + SH + ST), (CX - SW, y + ST)], fill=mul(col, .55))
    d.polygon([(CX, y + SH), (CX + SW, y), (CX + SW, y + ST), (CX, y + SH + ST)], fill=mul(col, .75))
    d.polygon(top, fill=mul(col, 1 + .5 * glow))
    d.line(top + [top[0]], fill=edge if glow > .1 else mul(edge, .6), width=3 + int(3 * glow))

def scene(fr, t, R):
    fr.img = BG.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    T = R.T; dur = R.dur
    # x-ray sweep line
    sy = 300 + ((t * 260) % 900); d.line((70, sy, 1010, sy), fill=(40, 90, 140), width=2)
    # open/close: closed stack during the hook, explodes on "route", closes again for the loop line
    op = ease((t - T("route")) / .8) * (1 - ease((t - T("never")) / .8))
    ys = [800 + (k - 2) * 34 + (YOPEN[k] - (800 + (k - 2) * 34)) * op for k in range(5)]
    # which stop is active
    seq = [("s1", 0), ("s2", 1), ("s3", 2), ("block", 2), ("s4", 3)]
    act = -1
    for tag, k in seq:
        if t >= T(tag) - .1: act = k
    if t >= R.line("s4").t1 - .2: act = 4
    pay = R.line("payoff")
    if pay.t0 <= t <= pay.t1: act = min(4, int((t - pay.t0) / (pay.t1 - pay.t0) * 6))
    if t >= T("never"): act = -1
    for k in range(4, -1, -1):
        glow = 1.0 if k == act else 0
        slab(d, ys[k], STOPS[k][2], STOPS[k][3], glow)
    # route line between slab centres
    if op > .5:
        for k in range(4):
            for yy in range(int(ys[k] + SH + ST), int(ys[k + 1] - SH), 14):
                d.line((CX, yy, CX, yy + 6), fill=(120, 230, 255), width=3)
    # labels with leader lines
    if op > .05:
        for k, (tag, name, col, edge) in enumerate(STOPS):
            al = ease(op * 1.4 - k * .08)
            if al <= 0: continue
            y = ys[k]; lx = CX + SW - 60; x2 = 600 - (1 - al) * 40
            c = edge if k == act else (150, 170, 200)
            d.line((lx, y, x2 - 10, y - 30), fill=c, width=3); d.ellipse((lx - 7, y - 7, lx + 7, y + 7), fill=c)
            fr.text((x2, y - 78), tag, FM(30), c)
            fr.text((x2, y - 46), name, F("b", 48), (255, 255, 255) if k == act or act < 0 else (170, 180, 200))
    # tower radio waves
    if act == 3 or (R.line("s4").t0 <= t <= R.line("s4").t1):
        for i in range(3):
            r = 40 + ((t * 120 + i * 40) % 120)
            d.arc((CX - 150 - r, ys[3] - r, CX - 150 + r, ys[3] + r), 150, 210, fill=(90, 160, 255), width=4)
    # the OTP packet moving stop to stop
    if t < T("route") + .4: py, px = ys[4] - 4, CX
    else:
        k = max(0, act) if act >= 0 else 4
        tgt = ys[k] - 4
        py = tgt; px = CX
    if t >= T("never"): py = ys[4] - 4
    chip_w = 330 if op < .5 else 250
    fnt = FM(40 if op < .5 else 32)
    d.rounded_rectangle((px - chip_w / 2, py - 34, px + chip_w / 2, py + 34), 16, fill=(255, 210, 60))
    fr.text((px, py), "4 8 2 9 1 7", fnt, (20, 20, 30), anchor="mm")
    # blocked spam example on the DLT stop
    b = R.line("block")
    if b.t0 <= t <= b.t1 + .6:
        k = max(.1, eback((t - b.t0) / .5)); x = 120; y = ys[2] - 20
        if t < b.t0: k = 0
        d.rounded_rectangle((x - 50 * k, y - 34 * k, x + 50 * k, y + 34 * k), 10, fill=(70, 20, 30), outline=(255, 80, 80), width=4)
        if t > b.t0 + (b.t1 - b.t0) * .7:
            d.line((x - 36, y - 36, x + 36, y + 36), fill=(255, 70, 70), width=10); d.line((x - 36, y + 36, x + 36, y - 36), fill=(255, 70, 70), width=10)
    # header / hook
    fr.text((90, 292), "HOW THINGS WORK · 01", FM(32), (255, 210, 60))
    h = R.line("hook")
    if t < T("route") + .3:
        k = eout((t - .05) / .35)
        fr.text((90, 340 + (1 - k) * 30), "This 6-digit code\nreached you in ~3 s.", F("black", 76), (255, 255, 255), spacing=4)
    elif t < T("never") - .1:
        fr.text((90, 340), "The OTP route", F("black", 76), (255, 255, 255))
    elif t < T("cta") - .1:
        k = eback((t - T("never")) / .45)
        d.rounded_rectangle((80, 330, 80 + 860 * k, 500), 22, fill=(255, 210, 60))
        if k > .9: fr.text((110, 415), "A bank never asks\nfor your OTP.", F("black", 66), (20, 20, 30), anchor="lm", spacing=2)
    else:
        fr.text((90, 340), "The OTP route", F("black", 76), (255, 255, 255))
    # time counter (narrative clock: 0 -> ~3 s across the route)
    s0, s1 = T("s1"), R.line("payoff").t1
    clock = 3.0 * ease((t - s0) / (s1 - s0)) if t >= s0 else 0.0
    if t >= T("loop"): clock = 0.0
    fr.text((995, 292), f"{clock:4.1f} s", FM(34), (120, 230, 255), anchor="ra")

def build(out):
    for L in LINES: L.speed = round(L.speed * 1.08, 3); L.gap = min(L.gap, .3)
    R = Reel("S1_HowThingsWork_ep01_OTP", "xray", LINES, tone="warm", seed=1)
    R.cap_style.update(hi=(255, 210, 60))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Save this for later", icon="save", at=round(dur * .38, 2))
    R.cta = dict(at=R.T("cta"), until=R.T("loop") - .05, icon="save", head="Save it.", body="Send it to the friend\nwho reads OTPs\nout loud on calls.",
                 bg=(255, 255, 255), acc=(225, 150, 0), fg=(15, 20, 40))
    stills = [.6, R.T("route") + 1, R.T("s1") + 1, R.T("s2") + 1.5, R.T("s3") + 1, R.T("block") + 1.5, R.T("s4") + 2,
              R.nudge["at"] + 1.0, R.T("payoff") + 1, R.T("never") + 1, R.T("cta") + 1, dur - .3]
    return R, R.render(scene, out, stills=sorted(stills))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", R.violations[:20], len(R.violations))
