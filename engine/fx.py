"""Approved motion styles (7 Nov 2026), reusable in any series. Text goes through fr.text so the safe-zone check still runs.

1. Kinetic hook (S4 first, any hook): count_up, slam_word, strike, words_in, verdict_pill
2. Payoff first (art / drawing reels): payoff_first() shows the finished picture ~0.8 s, rewinds fast, then draws it
3. Self-drawing diagram (S1): a drawon.Sketch + travel() signal dot + guess_card() 2 s pause-and-guess
"""
import math
from PIL import ImageDraw
from reel import F, ease, eout, eback

# ---------- 1. kinetic hook ----------
def count_up(fr, t, t0, value, xy, size=300, col=(15, 15, 15), dur=.55, fmt="{}", font=None):
    """Number counts 0 -> value, then lands with a scale punch and a short shake. Returns True once landed."""
    a = t - t0
    if a < 0: return False
    n = value if a >= dur else int(eout(a / dur) * value + 1e-6)
    land = a - dur
    punch = 1 + .25 * max(0, 1 - land / .18) if land > 0 else 1
    shake = math.sin(t * 90) * 10 * max(0, 1 - land / .25) if land > 0 else 0
    f = (font or (lambda s: F("black", s)))(int(size * punch))
    fr.text((xy[0] + shake, xy[1] - (punch - 1) * size * .4), fmt.format(n), f, col)
    return land > 0

def slam_word(fr, t, t0, text, xy, size=120, col=(15, 15, 15), frm=500, font=None):
    """Word slams in from the right with a slight overshoot."""
    if t < t0: return
    k = eback((t - t0) / .25); f = (font or (lambda s: F("black", s)))(size)
    fr.text((xy[0] + (1 - k) * frm, xy[1]), text, f, col)

def strike(d, t, t0, p0, p1, col=(225, 30, 30), width=22, dur=.3):
    """A line drawn through a claim, left to right."""
    if t < t0: return
    k = eout((t - t0) / dur); d.line((p0[0], p0[1], p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k), fill=col, width=width)

def words_in(fr, t, t0, words, xy, size=96, col=(160, 156, 150), gap=.12, font=None):
    """Words pop up one by one on the beat."""
    f = (font or (lambda s: F("black", s)))(size); x = xy[0]
    for i, w in enumerate(words):
        a = t - (t0 + i * gap)
        if a > 0: k = eback(a / .25); fr.text((x, xy[1] + (1 - k) * 80), w, f, col)
        x += fr.d.textlength(w + " ", font=f)

def verdict_pill(fr, t, t0, text, xy, size=120, bg=(225, 30, 30), fg=(255, 255, 255), font=None):
    """Pill grows from the left, then the verdict word appears (not a stamp)."""
    if t < t0: return
    f = (font or (lambda s: F("black", s)))(size); w = fr.d.textlength(text, font=f) + 60; h = size * 1.25
    k = eback((t - t0) / .3); x, y = xy
    fr.d.rounded_rectangle((x, y, x + w * k, y + h), 20, fill=bg)
    if k > .9: fr.text((x + 30, y + h * .06), text, f, fg)

# ---------- 2. payoff first ----------
def payoff_first(t, bg, done, sketches, show=.8, rewind=.6, draw=3.2, extra_dur=.8, arrows=True):
    """Canvas image at time t (local to the reel/segment start): finished art for `show` s, fast rewind, then it draws itself.
    sketches = [main, extra?]; bg = blank canvas image; done = finished canvas image."""
    if t < show: return done.copy(), None
    im = bg.copy(); d = ImageDraw.Draw(im); tip = None
    if t < show + rewind:
        p = 1 - eout((t - show) / rewind); tip = sketches[0].draw(d, p)
        if arrows:
            cx, cy = im.width / 2, im.height / 2
            for i in range(2):
                x = cx - 70 + i * 70; d.polygon([(x, cy), (x + 60, cy - 40), (x + 60, cy + 40)], fill=(255, 255, 255))
        return im, tip
    p = min(1, (t - show - rewind) / draw); tip = sketches[0].draw(d, p)
    if p >= 1 and len(sketches) > 1: tip = sketches[1].draw(d, min(1, (t - show - rewind - draw) / extra_dur))
    return im, tip

# ---------- 3. self-drawing diagram ----------
def travel(d, t, t0, path, dur=1.7, col=(255, 210, 80), r=16, width=6):
    """Signal dot travels along `path` (list of points), leaving a trail. Returns progress 0..1."""
    if t < t0: return 0
    k = min(1, (t - t0) / dur); n = int(k * (len(path) - 1))
    if n > 0: d.line(path[:n + 1], fill=col, width=width)
    x, y = path[n]; d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    return k

def guess_card(fr, t, t0, line1, line2, box=(110, 960, 940, 1160), secs=2, col=(120, 230, 255), bg=(10, 30, 50), hi=(255, 210, 80), font=None):
    """'Pause and guess' card with a countdown ring (keep box clear of the caption band when captions are on)."""
    if t < t0: return
    a = t - t0; x0, y0, x1, y1 = box; f = (font or (lambda s: F("black", s)))(50)
    fr.d.rounded_rectangle(box, 30, fill=bg, outline=col, width=4)
    tx = (x0 + x1 - 120) / 2
    fr.text((tx, y0 + 30), line1, f, (255, 255, 255), anchor="ma"); fr.text((tx, y0 + 95), line2, f, hi, anchor="ma")
    k = min(1, a / secs); cx, cy = x1 - 80, (y0 + y1) / 2
    fr.d.arc((cx - 45, cy - 45, cx + 45, cy + 45), -90, -90 + 360 * (1 - k), fill=col, width=10)
    fr.text((cx, cy), str(max(0, secs - int(a))), F("black", 44), (255, 255, 255), anchor="mm")
