"""S1 How Things Work kit — Isometric X-Ray Cutaway, reusable for any 5-stop route episode.

cfg keys: name, ep (int), title, hook_text, chip, banner, stops [(tag, name, col, edge)x5],
seq [(line_tag, stop_index)], wave (stop_index, line_tag) or None, block_tag (or None),
clock (max seconds or None), nudge_text, cta_body.
Line tags expected: hook, route, ..., payoff, never, cta, loop.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw
from reel import Reel, F, FM, ease, eout, eback, W, H
from s1_otp import BG, slab as _slab

CX, SW, SH, ST = 320, 250, 62, 24
YOPEN = [520, 640, 760, 880, 1000]

def slab(d, y, col, edge, glow):
    import s1_otp; s1_otp.CX, s1_otp.SW, s1_otp.SH, s1_otp.ST = CX, SW, SH, ST
    _slab(d, y, col, edge, glow)

def make_scene(cfg):
    STOPS = cfg["stops"]
    def scene(fr, t, R):
        fr.img = BG.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
        T = R.T
        sy = 300 + ((t * 260) % 900); d.line((70, sy, 1010, sy), fill=(40, 90, 140), width=2)
        op = ease((t - T("route")) / .8) * (1 - ease((t - T("never")) / .8))
        ys = [800 + (k - 2) * 34 + (YOPEN[k] - (800 + (k - 2) * 34)) * op for k in range(5)]
        act = -1
        for tag, k in cfg["seq"]:
            if t >= T(tag) - .1: act = k
        last = cfg["seq"][-1][0]
        if t >= R.line(last).t1 - .2: act = 4
        pay = R.line("payoff")
        if pay.t0 <= t <= pay.t1: act = min(4, int((t - pay.t0) / (pay.t1 - pay.t0) * 6))
        if t >= T("never"): act = -1
        for k in range(4, -1, -1): slab(d, ys[k], STOPS[k][2], STOPS[k][3], 1.0 if k == act else 0)
        if op > .5:
            for k in range(4):
                for yy in range(int(ys[k] + SH + ST), int(ys[k + 1] - SH), 14): d.line((CX, yy, CX, yy + 6), fill=(120, 230, 255), width=3)
        if op > .05:
            for k, (tag, name, col, edge) in enumerate(STOPS):
                al = ease(op * 1.4 - k * .08)
                if al <= 0: continue
                y = ys[k]; lx = CX + SW - 60; x2 = 600 - (1 - al) * 40
                c = edge if k == act else (150, 170, 200)
                d.line((lx, y, x2 - 10, y - 30), fill=c, width=3); d.ellipse((lx - 7, y - 7, lx + 7, y + 7), fill=c)
                fr.text((x2, y - 78), tag, FM(30), c)
                fr.text((x2, y - 46), name, F("b", 48), (255, 255, 255) if k == act or act < 0 else (170, 180, 200))
        if cfg.get("wave"):
            ws, wt = cfg["wave"]; L = R.line(wt)
            if L.t0 <= t <= L.t1:
                for i in range(3):
                    r = 40 + ((t * 120 + i * 40) % 120)
                    d.arc((CX - 150 - r, ys[ws] - r, CX - 150 + r, ys[ws] + r), 150, 210, fill=STOPS[ws][3], width=4)
        if t < T("route") + .4 or t >= T("never"): py = ys[cfg.get("rest", 4)] - 4
        else: py = ys[act if act >= 0 else cfg.get("rest", 4)] - 4
        cw = 330 if op < .5 else 250
        d.rounded_rectangle((CX - cw / 2, py - 34, CX + cw / 2, py + 34), 16, fill=(255, 210, 60))
        fr.text((CX, py), cfg["chip"], FM(36 if op < .5 else 30), (20, 20, 30), anchor="mm")
        if cfg.get("block_tag"):
            b = R.line(cfg["block_tag"]); bs = cfg.get("block_stop", 2)
            if b.t0 <= t <= b.t1 + .6:
                k = max(.1, eback((t - b.t0) / .5)); x = 120; y = ys[bs] - 20
                d.rounded_rectangle((x - 50 * k, y - 34 * k, x + 50 * k, y + 34 * k), 10, fill=(70, 20, 30), outline=(255, 80, 80), width=4)
                if t > b.t0 + (b.t1 - b.t0) * .7:
                    d.line((x - 36, y - 36, x + 36, y + 36), fill=(255, 70, 70), width=10); d.line((x - 36, y + 36, x + 36, y - 36), fill=(255, 70, 70), width=10)
        fr.text((90, 292), f"HOW THINGS WORK · {cfg['ep']:02d}", FM(32), (255, 210, 60))
        if t < T("route") + .3:
            k = eout((t - .05) / .35)
            fr.text((90, 340 + (1 - k) * 30), cfg["hook_text"], F("black", 72), (255, 255, 255), spacing=4)
        elif t < T("never") - .1 or t >= T("cta") - .1:
            fr.text((90, 340), cfg["title"], F("black", 76), (255, 255, 255))
        else:
            k = eback((t - T("never")) / .45)
            d.rounded_rectangle((80, 330, 80 + 860 * k, 500), 22, fill=(255, 210, 60))
            if k > .9: fr.text((110, 415), cfg["banner"], F("black", 60), (20, 20, 30), anchor="lm", spacing=2)
        if cfg.get("clock"):
            s0, s1 = T(cfg["seq"][0][0]), R.line("payoff").t1
            clock = cfg["clock"] * ease((t - s0) / (s1 - s0)) if t >= s0 else 0.0
            if t >= T("loop"): clock = 0.0
            fr.text((995, 292), f"{clock:4.1f} s", FM(34), (120, 230, 255), anchor="ra")
    return scene

def build(cfg, lines, out):
    for L in lines: L.speed = round(L.speed * 1.08, 3); L.gap = min(L.gap, .3)
    R = Reel(cfg["name"], "xray", lines, tone="warm", seed=cfg["ep"])
    R.cap_style.update(hi=(255, 210, 60))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text=cfg.get("nudge_text", "Save this for later"), icon="save", at=round(dur * .38, 2))
    R.cta = dict(at=R.T("cta"), until=R.T("loop") - .05, icon="save", head="Save it.", body=cfg["cta_body"],
                 bg=(255, 255, 255), acc=(225, 150, 0), fg=(15, 20, 40))
    tags = [L.tag for L in lines if L.tag]
    stills = sorted([.6] + [R.T(x) + 1 for x in tags] + [R.nudge["at"] + 1, dur - .3])
    return R, R.render(make_scene(cfg), out, stills=stills)
