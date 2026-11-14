"""Shot-recipe cards + 2.5D layer camera for flat storybook scenes (scout pick, 14 Nov 2026).

Idea (not code) from video-shotcraft's "shot recipe" cards (Apache-2.0): every shot is a small card with a
purpose, an energy, a duration and pitfalls, so a page never just sits there. Our own implementation in Pillow.

A page is a list of Layer(img, depth, origin). depth 0 = far sky, 1 = foreground / characters.
cam(name, k) -> Cam(x, y, zoom, fx, fy) for k in 0..1. compose(layers, cam) draws the frame:
near layers move and scale more than far ones, which is what makes flat paper feel 3D.
"""
import math, numpy as np
from dataclasses import dataclass
from PIL import Image

W, H = 1080, 1920

def _ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def _eout(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def _eback(x, s=1.6):
    x = min(1, max(0, x)) - 1; return x * x * ((s + 1) * x + s) + 1

@dataclass
class Layer:
    img: Image.Image          # RGBA, may be bigger than the frame (bleed for camera moves)
    depth: float              # 0 far ... 1 near
    origin: tuple = (0, 0)    # where the layer's top-left sits in frame coords (negative = bleed)

@dataclass
class Cam:
    x: float = 0; y: float = 0          # pan offset in px at depth 1
    zoom: float = 1.0                   # zoom at depth 1
    fx: float = W / 2; fy: float = 800  # zoom focus point (frame coords)
    blur: float = 0                     # horizontal motion blur in px (whip)

# ---- the recipe cards ---------------------------------------------------------------------------
SHOTS = {
    "push_in": dict(purpose="lean in on a feeling / the speaker", energy="low", dur=(3, 6),
                    params=dict(zoom=1.10), pitfall="> 4 % zoom per second makes captions swim"),
    "pull_out": dict(purpose="reveal where we are / the consequence", energy="low", dur=(3, 5),
                     params=dict(zoom=1.12), pitfall="start tight enough that the reveal means something"),
    "parallax_slide": dict(purpose="time passing, travel, a new place", energy="medium", dur=(3, 6),
                           params=dict(dx=170), pitfall="keep the subject inside x 65-1015 at both ends"),
    "rise": dict(purpose="look up: hope, the sky, a big idea", energy="medium", dur=(2, 4),
                 params=dict(dy=140), pitfall="near layers move most; check feet don't leave frame"),
    "whip_pan": dict(purpose="hard page turn, on the beat", energy="high", dur=(0.3, 0.45),
                     params=dict(blur=90), pitfall="max one whip per 6 s; never mid-sentence"),
    "settle_bounce": dict(purpose="arrival of a new page / punchline close-up", energy="high", dur=(0.5, 0.8),
                          params=dict(over=1.06), pitfall="one bounce only, then hold still"),
    "drift": dict(purpose="calm hold while someone talks", energy="low", dur=(2, 8),
                  params=dict(amp=10), pitfall="tiny; it should be felt, not seen"),
}

def cam(name, k, focus=(W / 2, 800), **over):
    """Camera for shot `name` at progress k (0..1)."""
    p = dict(SHOTS[name]["params"]); p.update(over); fx, fy = focus
    if name == "push_in":   return Cam(zoom=1 + (p["zoom"] - 1) * _ease(k), fx=fx, fy=fy)
    if name == "pull_out":  return Cam(zoom=p["zoom"] - (p["zoom"] - 1) * _eout(k), fx=fx, fy=fy)
    if name == "parallax_slide": return Cam(x=p["dx"] * (0.5 - _ease(k)), zoom=1.04, fx=fx, fy=fy)
    if name == "rise":      return Cam(y=-p["dy"] * (0.5 - _ease(k)), zoom=1.04, fx=fx, fy=fy)
    if name == "settle_bounce":
        # arrive slightly big, overshoot down, settle at 1.0
        k = min(1, max(0, k)); z = 1 + (p["over"] - 1) * math.cos(k * math.pi * 1.5) * (1 - k) ** 1.5
        return Cam(zoom=z, fx=fx, fy=fy)
    if name == "drift":     return Cam(x=p["amp"] * math.sin(k * math.pi * 2), y=p["amp"] * .5 * math.cos(k * math.pi * 2), zoom=1.03, fx=fx, fy=fy)
    raise KeyError(name)

def whip(k, direction=1, blur=90):
    """Whip pan between two pages: returns (out_cam, in_cam, show_in). k 0..1 over ~0.35 s."""
    e = _ease(k); b = blur * math.sin(math.pi * min(1, k))
    return Cam(x=-direction * W * e, blur=b, zoom=1.04), Cam(x=direction * W * (1 - e), blur=b, zoom=1.04), k >= .5

def compose(layers, c, bg=(0, 0, 0)):
    """Render layers through camera c. Near layers get the full pan/zoom, far layers ~25 %."""
    out = Image.new("RGBA", (W, H), bg + (255,))
    for L in layers:
        w = 0.25 + 0.75 * L.depth
        s = 1 + (c.zoom - 1) * w
        sx, sy = c.x * w, c.y * w
        ox, oy = L.origin
        # frame pixel p -> layer pixel: (p - f)/s + f - shift - origin
        a = 1 / s
        cx = c.fx - c.fx / s - sx - ox
        cy = c.fy - c.fy / s - sy - oy
        lay = L.img.transform((W, H), Image.AFFINE, (a, 0, cx, 0, a, cy), resample=Image.BILINEAR)
        out.alpha_composite(lay)
    if c.blur > 2: out = hblur(out, c.blur)
    return out

def hblur(img, px):
    """Cheap horizontal motion blur (average of shifted copies)."""
    a = np.asarray(img.convert("RGB"), dtype=np.float32); n = 7; acc = np.zeros_like(a)
    for i in range(n):
        acc += np.roll(a, int((i / (n - 1) - .5) * px), axis=1)
    return Image.fromarray((acc / n).astype(np.uint8)).convert("RGBA")

def card_sheet():
    """Plain-text table of the recipe cards (for the README / scout notes)."""
    rows = [f"{k:15s} {v['energy']:6s} {v['dur'][0]}-{v['dur'][1]} s  {v['purpose']}  | pitfall: {v['pitfall']}" for k, v in SHOTS.items()]
    return "\n".join(rows)
