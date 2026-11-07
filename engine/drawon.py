"""Stroke-by-stroke drawing for reels: build a Sketch of lines / fills / dots, then draw(d, p) shows it p (0..1) of the way
through, in order, the way a hand would draw it. Returns the pen-tip position so a tool can follow the stroke.
Idea borrowed from 'draw itself' explainer skills; written from scratch for the kitzz.ai Pillow engine."""
import math, random

def lerp(a, b, k): return a + (b - a) * k

def ellipse_pts(cx, cy, rx, ry, a0=0, a1=360, n=48, rot=0):
    out = []; c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i in range(n + 1):
        a = math.radians(lerp(a0, a1, i / n)); x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out

def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out

def plen(pts): return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

def trunc(pts, L):
    out = [pts[0]]; acc = 0
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; seg = math.dist(a, b)
        if acc + seg >= L:
            k = (L - acc) / seg if seg else 1; out.append((lerp(a[0], b[0], k), lerp(a[1], b[1], k))); return out
        out.append(b); acc += seg
    return out

def leaf(cx, cy, L, wdt, ang, n=14):
    """Almond / leaf outline centred at (cx, cy), length L, width wdt, rotated ang degrees."""
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang)); pts = []
    for i in range(n + 1):
        t = i / n; x = (t - .5) * L; y = math.sin(t * math.pi) * wdt / 2; pts.append((x, y))
    for i in range(n - 1, 0, -1):
        t = i / n; x = (t - .5) * L; y = -math.sin(t * math.pi) * wdt / 2; pts.append((x, y))
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]

def offset(pts, cx, cy, k):
    return [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in pts]

class Sketch:
    def __init__(self, wobble=0.0, seed=1, speed=1.0):
        self.ops = []; self.r = random.Random(seed); self.wob = wobble
    def _w(self, pts):
        if not self.wob: return list(pts)
        return [(x + self.r.uniform(-self.wob, self.wob), y + self.r.uniform(-self.wob, self.wob)) for x, y in pts]
    def line(self, pts, col, w=3, closed=False):
        pts = self._w(pts)
        if closed: pts = pts + [pts[0]]
        self.ops.append(("L", pts, col, w, max(1.0, plen(pts)))); return self
    def fill(self, pts, col, cost=45):
        self.ops.append(("F", list(pts), col, 0, cost)); return self
    def shape(self, pts, fill=None, col=None, w=3, cost=45):
        """Outline first, then the fill, then the outline again on top (crisp edge)."""
        if col: self.line(pts, col, w, closed=True)
        if fill: self.fill(pts, fill, cost)
        if col and fill: self.ops.append(("L", self.ops[-2][1], col, w, 0.0))
        return self
    def dot(self, x, y, r, col, cost=8):
        self.ops.append(("D", (x, y), col, r, cost)); return self
    def rect(self, x0, y0, x1, y1, col, w=3):
        return self.line([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, w, closed=True)
    @property
    def total(self): return sum(o[4] for o in self.ops)
    def draw(self, d, p):
        budget = max(0, p) * self.total; tip = None; prev_done = True
        for kind, g, col, w, c in self.ops:
            if c <= 0:
                if not prev_done: break
                k = 1.0
            else:
                if budget <= 0: break
                k = min(1, budget / c); budget -= c; prev_done = k >= 1
            if kind == "L":
                pts = g if k >= 1 else trunc(g, k * c)
                if len(pts) >= 2:
                    d.line(pts, fill=col, width=w, joint="curve")
                    if w >= 5:
                        for (x, y) in (pts[0], pts[-1]): d.ellipse((x - w / 2 + .5, y - w / 2 + .5, x + w / 2 - .5, y + w / 2 - .5), fill=col)
                    if c > 0: tip = pts[-1]
            elif kind == "F":
                if k >= .5:
                    d.polygon(g, fill=col)
                    tip = (sum(x for x, _ in g) / len(g), sum(y for _, y in g) / len(g))
            elif kind == "D":
                rr = w * min(1, k * 1.6)
                if rr > .4: d.ellipse((g[0] - rr, g[1] - rr, g[0] + rr, g[1] + rr), fill=col); tip = g
        return tip
