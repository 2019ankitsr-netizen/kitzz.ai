"""Quick look without voices: fake line timings, render stills to a safe-zone contact sheet."""
import sys, importlib, math
sys.path.insert(0, ".")
from kit import *
from PIL import Image, ImageDraw
mod = importlib.import_module(sys.argv[1]); lines = getattr(__import__("lines48"), sys.argv[2])
R = Reel(mod.NAME, "story", lines); t = .25
for L in lines:
    t += L.pre; L.t0 = t; L.t1 = t + max(1.2, len(L.say) / 14); t = L.t1 + L.gap
R.dur = t + .8
R.nudge = dict(text="Send this", icon="send", at=R.dur * .38, bg=(255,122,40), fg=(255,255,255))
R.cta = dict(at=R.T("cta"), icon="send", head="Send this", body="test", bg=(255,255,255), acc=(255,122,40), fg=(30,20,22), until=R.T("loop")-.05)
for k, v in (getattr(mod, "PREVIEW_STYLE", {}) or {}).items(): R.cap_style[k] = v
ts = []
for L in lines: ts += [L.t0 + .02, L.t0 + .15, L.t0 + (L.t1 - L.t0) * .7]
R.sheet = []; viol = []
for tt in ts:
    fr = Frame(R.name, Image.new("RGB", (W, H))); mod.scene(fr, tt, R); R.draw_nudge(fr, tt); R.draw_cta(fr, tt); R.caption(fr, tt)
    viol += [(round(tt,2),) + v for v in fr.check()]; R.sheet.append((tt, fr.img.convert("RGB")))
R.contact_sheet(f"/home/claude/out48/prev_{mod.NAME}.png", cols=9)
print("violations", len(viol)); [print(v) for v in viol[:25]]
if len(sys.argv) > 3:
    for tg in sys.argv[3].split(","):
        L = R.line(tg); tt = L.t0 + (L.t1 - L.t0) * .7
        fr = Frame(R.name, Image.new("RGB", (W, H))); mod.scene(fr, tt, R); R.caption(fr, tt)
        fr.img.convert("RGB").crop((0, 250, W, 1260)).resize((540, 505)).save(f"/home/claude/out48/f_{mod.NAME}_{tg}.png")
