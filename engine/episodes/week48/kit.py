"""Shared helpers for the week-48 episodes (Sharma Ghar Ep5, AI Khabar Ep2, Dev Katha Ep1).

- compose(): per-line scenes with creative transitions (whip pan, ink bleed, zoom punch, iris), so every cut moves.
- Devanagari fonts (Hind / Yatra One, shaped by Pillow+raqm) and display fonts.
- small drawing helpers: thick-outline shapes, sticky notes, speech bubbles, confetti, halftone, paper texture.
All art is drawn in code; no logos, no real people, no other creators' footage.
"""
import os, sys, math, random, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
from reel import Reel, Line, F, ease, eout, eback, W, H, icon      # noqa: E402
from style_frames import Frame                                      # noqa: E402

FONT_DIR = os.environ.get("KITZZ_FONTS", "/home/claude/fonts")
_fc = {}
def HF(size, w="b"):
    """Devanagari / Latin text font: Hind Bold (b), Hind SemiBold (sb), Yatra One (y), Bangers (bang), Baloo Bhai 2 (baloo)."""
    k = (w, size)
    if k not in _fc:
        fn = {"b": "Hind-Bold.ttf", "sb": "Hind-SemiBold.ttf", "y": "YatraOne-Regular.ttf",
              "bang": "Bangers-Regular.ttf", "baloo": "BalooBhai2.ttf"}[w]
        f = ImageFont.truetype(os.path.join(FONT_DIR, fn), size, layout_engine=ImageFont.Layout.RAQM)
        if w == "baloo":
            try: f.set_variation_by_axes([800])
            except Exception: pass
        _fc[k] = f
    return _fc[k]
def HFP(w="b"): return os.path.join(FONT_DIR, {"b": "Hind-Bold.ttf", "y": "YatraOne-Regular.ttf"}[w])

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, dur): return clamp((t - t0) / max(1e-3, dur))
def lerp(a, b, k): return a + (b - a) * k

# ---------------------------------------------------------------- transitions
_NOISE = {}
def _noise(seed=3):
    if seed not in _NOISE:
        rng = np.random.default_rng(seed)
        n = rng.random((H // 40 + 2, W // 40 + 2)).astype(np.float32)
        big = np.array(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
        fine = np.array(Image.fromarray((rng.random((H // 6, W // 6)) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255
        yy = np.linspace(0, 1, H)[:, None]
        _NOISE[seed] = (big * .45 + fine * .07 + yy * .48).astype(np.float32)   # ink bleeds top -> bottom, ragged edge
    return _NOISE[seed]

def hblur(img, amount):
    if amount < 2: return img
    f = max(2, int(amount))
    return img.resize((max(1, W // f), H), Image.BILINEAR).resize((W, H), Image.BILINEAR)

def transition(a, b, k, kind="whip"):
    """a = outgoing frame, b = incoming frame, k = 0..1."""
    k = clamp(k)
    if kind == "whip":                     # fast whip pan with motion blur
        e = ease(k); blur = 40 * math.sin(math.pi * k)
        out = Image.new("RGB", (W, H))
        out.paste(hblur(a, blur), (int(-e * W), 0)); out.paste(hblur(b, blur), (int(W - e * W), 0))
        return out
    if kind == "ink":                      # ink bleed / paper soak
        n = _noise(); m = (n < (k * 1.25 - .05)).astype(np.uint8) * 255
        mask = Image.fromarray(m).filter(ImageFilter.GaussianBlur(2))
        out = a.copy(); out.paste(b, (0, 0), mask)
        edge = ((n >= k * 1.25 - .05) & (n < k * 1.25 - .02)).astype(np.uint8) * 150
        ink = Image.new("RGB", (W, H), (43, 27, 18)); out.paste(ink, (0, 0), Image.fromarray(edge).filter(ImageFilter.GaussianBlur(1.5)))
        return out
    if kind == "zoom":                     # zoom punch: incoming scales 1.18 -> 1 while outgoing pushes in
        e = eout(k); s = 1.18 - .18 * e
        bb = b.resize((int(W * s), int(H * s)), Image.BILINEAR); x, y = (bb.width - W) // 2, (bb.height - H) // 2
        bb = bb.crop((x, y, x + W, y + H))
        sa = 1 + .25 * e; aa = a.resize((int(W * sa), int(H * sa)), Image.BILINEAR); x, y = (aa.width - W) // 2, (aa.height - H) // 2
        aa = aa.crop((x, y, x + W, y + H))
        return Image.blend(aa, bb, clamp(k * 1.6))
    if kind == "iris":
        r = eout(k) * 1250; m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((540 - r, 760 - r, 540 + r, 760 + r), fill=255)
        out = a.copy(); out.paste(b, (0, 0), m); return out
    if kind == "slide_up":
        e = ease(k); out = a.copy(); out.paste(b, (0, int(H - e * H))); return out
    return b

def compose(fr, t, R, draw, trans=None, TR=.3, same=lambda a, b: a == b):
    """Draw the active line's scene; at a scene change, blend from the previous scene with a transition.
    draw(fr, tag, t, L, R) draws one scene. trans = dict(tag -> kind) or a default kind string."""
    L = R.active(t) or R.lines[0]; i = R.lines.index(L)
    cur = Frame(R.name, Image.new("RGB", (W, H))); draw(cur, L.tag, t, L, R)
    if i > 0 and 0 <= t - L.t0 < TR and not same(R.lines[i - 1].tag, L.tag):
        P = R.lines[i - 1]; prev = Frame(R.name, Image.new("RGB", (W, H))); draw(prev, P.tag, L.t0 - .001, P, R)
        kind = trans.get(L.tag, trans.get("*", "whip")) if isinstance(trans, dict) else (trans or "whip")
        fr.img = transition(prev.img.convert("RGB"), cur.img.convert("RGB"), (t - L.t0) / TR, kind)
    else:
        fr.img = cur.img.convert("RGB")
    fr.boxes = cur.boxes; fr.d = ImageDraw.Draw(fr.img)

# ---------------------------------------------------------------- drawing helpers
OUT = (30, 20, 22)
def rr(d, box, r, fill, outline=OUT, w=6): d.rounded_rectangle(box, r, fill=fill, outline=outline, width=w)
def circ(d, cx, cy, r, fill, outline=OUT, w=5): d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=w)

def shadowed(fr, box, r, fill, off=10, sh=(0, 0, 0, 70), outline=OUT, w=6):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle((box[0] + off, box[1] + off, box[2] + off, box[3] + off), r, fill=sh)
    fr.img = Image.alpha_composite(fr.img.convert("RGBA"), ov).convert("RGB"); fr.d = ImageDraw.Draw(fr.img)
    fr.d.rounded_rectangle(box, r, fill=fill, outline=outline, width=w)

def pop_scale(t, t0, dur=.35): return eback(prog(t, t0, dur)) if t >= t0 else 0

def bubble(fr, box, fill=(255, 255, 255), tail=None, r=34):
    d = fr.d
    if tail:
        d.polygon(tail, fill=fill, outline=OUT); d.line(tail[:2], fill=OUT, width=6); d.line(tail[1:], fill=OUT, width=6)
    rr(d, box, r, fill)
    if tail:   # cover the outline where the tail joins
        d.line((tail[0][0] + 6, tail[0][1], tail[2][0] - 6, tail[2][1]), fill=fill, width=9)

def text_fit(fr, txt, font_fn, maxw, start, minsize=30):
    s = start
    while s > minsize and max(fr.d.textlength(r, font=font_fn(s)) for r in txt.split("\n")) > maxw: s -= 2
    return font_fn(s)

def type_on(txt, k):
    n = int(len(txt) * clamp(k)); return txt[:n]

def sticky(fr, t, t0, box, title, body, col=(255, 226, 90), ang=-3, icon_kind=None, fonts=None):
    """Sticky note that slaps on with a little overshoot and settles at an angle."""
    if t < t0: return
    k = eback(prog(t, t0, .32)); x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    note = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); nd = ImageDraw.Draw(note)
    nd.rectangle((26, 30, w + 26, h + 30), fill=(0, 0, 0, 60))
    nd.rectangle((14, 14, w + 14, h + 14), fill=col + (255,), outline=OUT + (255,), width=5)
    nd.rectangle((w // 2 - 50 + 14, 4, w // 2 + 50 + 14, 34), fill=(220, 220, 210, 200))   # tape
    fh, fb = fonts or (F("black", 62), F("xb", 50))
    nd.text((46, 40), title, font=fh, fill=OUT)
    nd.multiline_text((46, 40 + fh.size + 18), body, font=fb, fill=OUT, spacing=10)
    s = .6 + .4 * k; note = note.rotate(ang * k, expand=False, resample=Image.BICUBIC)
    note = note.resize((max(1, int(note.width * s)), max(1, int(note.height * s))), Image.BILINEAR)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    fr.img = fr.img.convert("RGBA"); fr.img.alpha_composite(note, (int(cx - note.width / 2), int(cy - note.height / 2)))
    fr.img = fr.img.convert("RGB"); fr.d = ImageDraw.Draw(fr.img)
    # record text boxes for the safe-zone check (settled position)
    fr.boxes.append((title[:30], (x0 + 30, y0 + 20, x0 + 40 + fr.d.textlength(title, font=fh), y0 + 30 + fh.size)))
    bw = max(fr.d.textlength(r, font=fb) for r in body.split("\n"))
    fr.boxes.append((body[:30].replace("\n", " "), (x0 + 30, y0 + 40 + fh.size, x0 + 40 + bw, y0 + 60 + fh.size + (fb.size + 12) * (body.count("\n") + 1))))

class Confetti:
    def __init__(self, n=70, seed=4, cols=((255, 210, 60), (255, 90, 120), (90, 220, 255), (140, 255, 140), (255, 255, 255))):
        r = random.Random(seed)
        self.p = [(r.uniform(65, 1015), r.uniform(-400, 0), r.uniform(120, 300), r.uniform(-60, 60), r.choice(cols),
                   r.uniform(0, 6.28), r.uniform(4, 9), r.randint(0, 1)) for _ in range(n)]
    def draw(self, d, t, t0, y0=269, y1=1248):
        a = t - t0
        if a < 0: return
        for x, y, vy, vx, col, ph, s, kind in self.p:
            yy = y + vy * a + 260 + 40 * a * a
            if yy > y1 + 400: continue
            xx = x + vx * a + math.sin(a * 3 + ph) * 18
            rot = math.cos(a * 5 + ph)
            if kind: d.rectangle((xx - s * 1.6 * abs(rot), yy - s, xx + s * 1.6 * abs(rot), yy + s), fill=col)
            else: d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=col)

def halftone(size=(W, H), bg=(52, 22, 92), dot=(72, 38, 120), step=34):
    im = Image.new("RGB", size, bg); d = ImageDraw.Draw(im)
    for yy in range(0, size[1] + step, step):
        for xx in range(0, size[0] + step, step):
            off = step / 2 if (yy // step) % 2 else 0
            r = 3 + 6 * (0.5 + 0.5 * math.sin(xx / 210 + yy / 330))
            d.ellipse((xx + off - r, yy - r, xx + off + r, yy + r), fill=dot)
    return im

def paper(seed=7, base=(243, 230, 200)):
    rng = np.random.default_rng(seed)
    img = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    n = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    n = np.array(Image.fromarray(((n * 20) + 128).clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) - 128
    img += n[..., None] * .35 + rng.normal(0, 3, (H, W, 1))
    yy, xx = np.mgrid[0:H, 0:W]
    dd = np.sqrt(((xx - W / 2) / (W * .75)) ** 2 + ((yy - H / 2) / (H * .7)) ** 2)
    img *= (1 - .22 * np.clip(dd - .35, 0, 1))[..., None]
    pil = Image.fromarray(img.clip(0, 255).astype(np.uint8)); dr = ImageDraw.Draw(pil)
    for _ in range(260):
        x, y = rng.uniform(0, W), rng.uniform(0, H); a = rng.uniform(0, 6.28); l = rng.uniform(8, 30)
        dr.line([(x, y), (x + l * math.cos(a), y + l * math.sin(a))], fill=(196, 170, 130), width=1)
    return pil

def indian(n):
    """10,00,000-style grouping."""
    s = str(int(n))
    if len(s) <= 3: return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2: parts.insert(0, head[-2:]); head = head[:-2]
    if head: parts.insert(0, head)
    return ",".join(parts + [tail])
