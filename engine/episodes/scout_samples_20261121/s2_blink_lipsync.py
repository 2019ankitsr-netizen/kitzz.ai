"""Scout sample 3 (21 Nov 2026): eye blinks + voice-driven mouths for S2 AI Ki Kahani (Tara + Bablu).
Same 3 lines twice: PEHLE (current sine-wave mouth, fixed-period blink) then AB (mouth picked from the TTS loudness with an
attack/release smoother, 4 mouth shapes, random blinks, listener blinks after a turn change, eyes glance at the speaker).
Method idea from styk-tv/wireface (MIT): audio energy -> mouth-open target, heavier smoothing on the mouth. Our own Pillow code."""
import os, sys, math, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..')); sys.path.insert(0, os.path.join(HERE, '..', '..', 'pilots'))
from PIL import Image, ImageDraw, ImageFilter
from reel import Reel, Line, F, FM, ease, eout, eback, W, H, FPS
import audio as A
import s2_tara as K

T_, B = "hf_beta", "hm_psi"
def L(spk, say, cap, **k): return Line(spk, say, cap, lang="hi", **k)
BASE = [(T_, "नमस्ते बबलू! मैं तारा हूँ। तुम्हारी ए आई दोस्त।", "Namaste Bablu! Main Tara hoon. Tumhari AI dost.", "TARA"),
        (B, "ए आई? मतलब तुम मेरी तरह सोचती हो?", "AI? Matlab tum meri tarah sochti ho?", "BABLU"),
        (T_, "नहीं बबलू। मैं सोचती नहीं। मैं अंदाज़ा लगाती हूँ।", "Nahi Bablu. Main sochti nahi. Main andaaza lagaati hoon.", "TARA")]
LINES = []
for part in ("old", "new"):
    for i, (s, say, cap, who) in enumerate(BASE):
        LINES.append(L(s, say, cap, who=who, tag=f"{part}{i}", speed=1.08, gap=.3, pre=(.9 if part == "new" and i == 0 else 0)))

# ---------- mouth level from the voice track ----------
def mouth_track(R):
    v = np.abs(R.voice); hop = A.SR // FPS; n = int(R.dur * FPS) + 2
    rms = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(v) else 0 for i in range(n)])
    lev = np.zeros(n)
    for Ln in R.lines:                               # normalise per line, so quiet voices still open the mouth
        a, b = int(Ln.t0 * FPS), int(Ln.t1 * FPS) + 1
        ref = np.percentile(rms[a:b], 90) + 1e-6; lev[a:b] = np.clip(rms[a:b] / ref, 0, 1.2)
    out = np.zeros(n); x = 0.0; dt = 1 / FPS
    for i in range(n):                               # attack ~40 ms, release ~90 ms
        tau = .04 if lev[i] > x else .09; x += (lev[i] - x) * (1 - math.exp(-dt / tau)); out[i] = x
    return out
def shape(level):   # 0 closed, 1 small, 2 open, 3 wide
    return 0 if level < .14 else 1 if level < .38 else 2 if level < .7 else 3

# ---------- blinks ----------
def blink_times(seed, dur, extra=()):
    r = random.Random(seed); t, out = r.uniform(.8, 2.0), []
    while t < dur: out.append(t); t += r.uniform(2.5, 5.0)
    return sorted(out + list(extra))
def lid(t, times):
    """0 open .. 1 closed: 1 frame half, 2 frames shut, 1 frame half (~130 ms)."""
    for b in times:
        k = (t - b) * FPS
        if 0 <= k < 4: return [.55, 1, 1, .55][int(k)]
    return 0

# ---------- characters (same art as pilots/s2_tara.py, new eyes/mouth) ----------
def shadow(img, box, r, kind="rr"):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle(box, r, fill=(60, 40, 20, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))

def eye(d, cx, cy, rx, ry, closed, look, col):
    if closed >= .99: d.line((cx - rx, cy + ry * .2, cx + rx, cy + ry * .2), fill=col, width=6); return
    h = ry * (1 - closed); d.ellipse((cx - rx, cy - h, cx + rx, cy + h), fill=col)
    if closed < .3: d.ellipse((cx - rx * .35 + look * rx * .35, cy - h * .55, cx + rx * .05 + look * rx * .35, cy - h * .1), fill=(255, 255, 255))  # glint

def tara2(img, x, y, sh_, closed, look, t):
    shadow(img, (x + 12, y + 12, x + 212, y + 372), 34); d = ImageDraw.Draw(img)
    d.rounded_rectangle((x, y, x + 200, y + 360), 34, fill=(40, 45, 70))
    d.rounded_rectangle((x + 14, y + 22, x + 186, y + 338), 24, fill=(120, 220, 230))
    for ex in (x + 65, x + 135): eye(d, ex + look * 6, y + 142, 15, 17, closed, look, (30, 30, 50))
    mx, my = x + 100, y + 212; c = (30, 30, 50)
    if sh_ == 0: d.arc((mx - 40, my - 42, mx + 40, my + 22), 20, 160, fill=c, width=8)
    else:
        wv, hv = [(0, 0), (26, 9), (28, 20), (32, 30)][sh_]
        d.rounded_rectangle((mx - wv, my - hv, mx + wv, my + hv), min(wv, hv), fill=c)
        if sh_ >= 2: d.ellipse((mx - wv * .5, my + hv * .1, mx + wv * .5, my + hv * .9), fill=(230, 110, 120))   # tongue

def bablu2(img, x, y, sh_, closed, look, t, talking):
    bob = math.sin(t * 7) * 3 if talking else 0; y = y + bob
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse((x - 58, y - 58, x + 82, y + 82), fill=(60, 40, 20, 80)); sd.rounded_rectangle((x - 78, y + 82, x + 102, y + 312), 40, fill=(60, 40, 20, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7))); d = ImageDraw.Draw(img)
    d.rounded_rectangle((x - 90, y + 70, x + 90, y + 300), 40, fill=(235, 130, 50)); d.line((x, y + 80, x, y + 180), fill=(200, 100, 30), width=5)
    d.ellipse((x - 70, y - 70, x + 70, y + 70), fill=(214, 160, 120))
    d.chord((x - 74, y - 80, x + 74, y + 30), 180, 360, fill=(40, 30, 30)); d.polygon([(x - 10, y - 80), (x + 25, y - 110), (x + 30, y - 70)], fill=(40, 30, 30))
    for ex in (x - 26, x + 26): eye(d, ex + look * 5, y + 5, 9, 10, closed, look, (30, 20, 20))
    mx, my = x + look * 3, y + 38; c = (120, 40, 40)
    if sh_ == 0: d.line((mx - 12, my, mx + 12, my), fill=c, width=5)
    else:
        wv, hv = [(0, 0), (12, 5), (14, 11), (17, 16)][sh_]; d.ellipse((mx - wv, my - hv, mx + wv, my + hv), fill=c)

def scene(fr, t, R):
    new = t >= R.T("new0") - .9
    fr.img = K.BG[False].copy(); d = ImageDraw.Draw(fr.img)
    sway = math.sin(t * .6); K.house(d, 120 + sway * 4, 800, False)
    for i, lay in enumerate(K.HL[False]): fr.img.alpha_composite(lay, (int(-80 + sway * (6 + 6 * i)), 0))
    sp = R.speaking(t); f = min(len(R.MT) - 1, int(t * FPS))
    if not new:
        K.bablu(fr.img, 300, 700, sp is not None and sp.spk == B, t)
        K.tara(fr.img, 640, 650, sp is not None and sp.spk == T_, t)
    else:
        tal_t = sp is not None and sp.spk == T_; tal_b = sp is not None and sp.spk == B
        lv = R.MT[f]
        # eyes glance toward whoever is speaking
        look_t = -1 if tal_b else 0; look_b = 1 if tal_t else 0
        bablu2(fr.img, 300, 700, shape(lv) if tal_b else 0, lid(t, R.BL_B), look_b, t, tal_b)
        tara2(fr.img, 640, 650, shape(lv) if tal_t else 0, lid(t, R.BL_T), look_t, t)
    fr.d = ImageDraw.Draw(fr.img)
    # label chip: which version
    lab = "AB: voice-driven mouth + blinks" if new else "PEHLE: sine-wave mouth"
    col = (200, 80, 40) if new else (110, 100, 90)
    fnt = F("black", 46); w_ = fr.d.textlength(lab, font=fnt)
    fr.d.rounded_rectangle((90, 300, 90 + w_ + 60, 380), 40, fill=col)
    fr.text((120, 340), lab, fnt, (255, 250, 240), anchor="lm")
    fr.text((92, 400), "S2 AI KI KAHANI · SCOUT SAMPLE", FM(26), (180, 70, 50))

def build(out):
    R = Reel("Scout3_S2_BlinkLipSync_HI", "story", LINES, tone="bright", pitch=1.0, seed=2, tail=.6)
    R.cap_style.update(fg=(255, 250, 240), hi=(255, 200, 90), bg=(60, 35, 25, 215), who_fg=(255, 200, 90), who_stroke=(60, 35, 25))
    dur = R.build_audio(f"{out}/cache")
    R.MT = mouth_track(R)
    turns = [Ln.t0 + .15 for Ln in R.lines if Ln.tag.startswith("new")]
    R.BL_T = blink_times(11, dur, [x for x, Ln in zip(turns, [l for l in R.lines if l.tag.startswith("new")]) if Ln.spk == B])
    R.BL_B = blink_times(23, dur, [x for x, Ln in zip(turns, [l for l in R.lines if l.tag.startswith("new")]) if Ln.spk == T_])
    st = [R.T("old0") + .6, R.T("old1") + .5, R.T("new0") + .4, R.T("new0") + .55, R.T("new1") + .5, R.T("new2") + .8]
    return R, R.render(scene, out, stills=st)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    R, p = build(out); print(p, round(R.dur, 1), "s violations:", len(R.violations), R.violations[:6])
