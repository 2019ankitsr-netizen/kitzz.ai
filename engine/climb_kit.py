"""Scale-climb kit (look of the user's reference reel): deep-blue screen, one glowing column rising from the ground, side ruler,
counter + progress line at top, thin outline objects that shrink as the camera zooms out, Earth / Moon / Sun / stars markers,
one line of story text at the bottom, music only. Everything drawn in code; text via fr.text so the safe-zone check runs.

Config: keys [(t, value)], value_to_m(v) -> metres, fmt(m) -> label, objects [...], markers [...], story [(t, text, keyword)]."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reel import F, FM, ease, eout, eback, W, H

FONTS = "/home/claude/fonts"
def HF(s, w="Bold"): return ImageFont.truetype(f"{FONTS}/Hind-{w}.ttf", s)
CX, GY, TOPY = 540, 1000, 575                 # column x, ground y, column top y when fully zoomed
TEAL, WHITE, DIM, GOLDL = (110, 232, 220), (240, 240, 250), (150, 156, 190), (240, 196, 110)
LIGHT = (255, 238, 200)

def background(seed=3):
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(-1, 1, W)[None, :]
    r = np.sqrt(x ** 2 * .6 + (y - .45) ** 2)
    base = np.stack([22 + 30 * (1 - r), 26 + 34 * (1 - r), 70 + 70 * (1 - r)], -1).clip(0, 255)
    im = Image.fromarray(base.astype(np.uint8)).convert("RGB"); d = ImageDraw.Draw(im); rng = np.random.default_rng(seed)
    for _ in range(260):
        sx, sy, b = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(60, 190)
        d.point((sx, sy), fill=(int(b), int(b), int(b + 30)))
    return im

def interp(keys, t):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            k = (t - t0) / (t1 - t0); k = k * k * (3 - 2 * k); return v0 + (v1 - v0) * k
    return keys[-1][1]

def nice_step(x):
    e = 10 ** math.floor(math.log10(x)); m = x / e
    return (1 if m < 2 else 2 if m < 5 else 5) * e

def dashed(d, p0, p1, col, w=2, dash=8):
    L = math.dist(p0, p1); n = max(1, int(L / dash))
    for i in range(0, n, 2):
        a, b = i / n, min(1, (i + 1) / n)
        d.line((p0[0] + (p1[0] - p0[0]) * a, p0[1] + (p1[1] - p0[1]) * a, p0[0] + (p1[0] - p0[0]) * b, p0[1] + (p1[1] - p0[1]) * b), fill=col, width=w)

# ---------- outline icons, drawn standing on the ground, height h px, centred at x ----------
def icon(d, kind, x, h, col, lw=3):
    g = GY
    if kind == "grain": d.ellipse((x - h * .18, g - h, x + h * .18, g), outline=col, width=lw)
    elif kind == "door":
        d.rectangle((x - h * .23, g - h, x + h * .23, g), outline=col, width=lw); d.ellipse((x + h * .12, g - h * .5, x + h * .16, g - h * .46), fill=col)
    elif kind == "house":
        d.rectangle((x - h * .45, g - h * .62, x + h * .45, g), outline=col, width=lw); d.line((x - h * .55, g - h * .6, x, g - h, x + h * .55, g - h * .6), fill=col, width=lw)
        d.rectangle((x - h * .1, g - h * .3, x + h * .1, g), outline=col, width=lw)
    elif kind == "tower":    # tapering minaret with bands
        d.polygon([(x - h * .1, g), (x + h * .1, g), (x + h * .04, g - h), (x - h * .04, g - h)], outline=col, width=lw)
        for k in (.25, .5, .72, .9): w = h * (.1 - .06 * k) + 4; d.line((x - w, g - h * k, x + w, g - h * k), fill=col, width=lw)
    elif kind == "spire":
        d.polygon([(x - h * .09, g), (x + h * .09, g), (x + h * .02, g - h * .8), (x, g - h), (x - h * .02, g - h * .8)], outline=col, width=lw)
    elif kind == "mountain":
        d.polygon([(x - h * .9, g), (x - h * .1, g - h), (x + h * .15, g - h * .8), (x + h * .9, g)], outline=col, width=lw)
        d.line((x - h * .3, g - h * .75, x - h * .1, g - h * .62, x + h * .05, g - h * .78), fill=col, width=lw)

def column(img, top, base, wdt=40):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for i, a in enumerate((26, 18, 12, 7)):
        g = 14 + i * 16; ld.rectangle((CX - wdt / 2 - g, top - g / 2, CX + wdt / 2 + g, base), fill=(255, 225, 160, a))
    ld.rectangle((CX - wdt / 2, top, CX + wdt / 2, base), fill=LIGHT + (255,))
    ld.rectangle((CX - wdt / 2 + 6, top, CX - wdt / 2 + 12, base), fill=(255, 250, 235, 255))
    img.alpha_composite(lay) if img.mode == "RGBA" else img.paste(Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB"))
    d = ImageDraw.Draw(img); d.ellipse((CX - wdt * 1.5, top - 14, CX + wdt * 1.5, top + 14), outline=(240, 240, 255), width=2)
    return d

def mini_board(d, x, y, c=4):
    for k in range(64):
        r, q = divmod(k, 8); d.rectangle((x + q * c, y + r * c, x + q * c + c - 1, y + r * c + c - 1), fill=(230, 230, 240) if (r + q) % 2 else (90, 90, 120))

def render_frame(fr, t, cfg, BG):
    fr.img = BG.copy(); fr.d = d = ImageDraw.Draw(fr.img)
    v = interp(cfg["keys"], t); L = cfg["value_to_m"](v); n = int(v + 1e-6)
    span = GY - TOPY; ppm = span / max(L, cfg["min_view_m"])     # pixels per metre
    colh = L * ppm; top = GY - colh
    # --- top: title, counter, progress line ---
    for i, line in enumerate(cfg["title"]):
        fr.text((540, 280 + i * 54), line, HF(46), WHITE, anchor="ma")
    lab = f"{cfg['unit_word']} {n} = "; val = cfg["fmt"](cfg["value_to_m"](n))
    f1 = HF(44); w1 = d.textlength(lab, font=f1); w2 = d.textlength(val, font=f1)
    x0 = 540 - (w1 + w2) / 2; fr.text((x0, 400), lab, f1, WHITE); fr.text((x0 + w1, 400), val, f1, TEAL)
    py = 480; d.line((150, py, 880, py), fill=(90, 96, 140), width=3)
    px = 150 + (880 - 150) * (v - 1) / (cfg["max_value"] - 1); d.line((150, py, px, py), fill=TEAL, width=4)
    d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=WHITE); mini_board(d, 890, py - 16)
    # --- Earth (space phase) / ground ---
    R = 6.371e6 * ppm
    if R > 4000:
        d.rectangle((0, GY, W, GY + 70), fill=(14, 16, 40)); d.line((60, GY, 1020, GY), fill=GOLDL, width=3)
    else:
        rr = max(R, 7)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.ellipse((CX - rr, GY - 2, CX + rr, GY - 2 + 2 * rr), fill=(48, 98, 176, 255), outline=(140, 200, 255, 255), width=2)
        if rr > 20:
            for (ax, ay, s) in ((-.35, .35, .28), (.25, .6, .22), (.05, .2, .15)):
                ld.ellipse((CX + ax * rr - s * rr, GY + ay * 2 * rr - s * rr, CX + ax * rr + s * rr, GY + ay * 2 * rr + s * rr), fill=(70, 150, 90, 255))
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rectangle((0, 0, W, GY + 46), fill=255)
        for yy in range(GY + 46, GY + 60): ImageDraw.Draw(m).line((0, yy, W, yy), fill=int(255 * (GY + 60 - yy) / 14))
        a = lay.getchannel("A"); lay.putalpha(Image.fromarray((np.array(a) * (np.array(m) / 255)).astype(np.uint8)))
        fr.img.paste(Image.alpha_composite(fr.img.convert("RGBA"), lay).convert("RGB")); fr.d = d = ImageDraw.Draw(fr.img)
        if 30 < rr < 400: fr.text((CX + 60, GY + 6), cfg.get("earth_label", "पृथ्वी"), HF(26), (200, 225, 255))
    # --- ruler ---
    vis = GY - 560
    step = nice_step(max(L, cfg["min_view_m"]) / 3.5)
    d.line((100, 560, 100, GY), fill=(80, 86, 130), width=2)
    k = 1
    while k * step * ppm <= vis and k < 12:
        y = GY - k * step * ppm; d.line((100, y, 116, y), fill=(120, 126, 170), width=2)
        fr.text((122, y - 14), cfg["fmt"](k * step, short=True), HF(22, "SemiBold"), (120, 126, 170)); k += 1
    # --- ground objects ---
    for name, hm, kind, side in cfg["objects"]:
        h = hm * ppm
        if h < 5 or hm > L * 1.02 or R < 4000: continue
        x = CX - 230 if side == "L" else CX + 230
        a = 1 if h > 14 else (h - 5) / 9
        col = tuple(int(c * a + 30 * (1 - a)) for c in cfg["obj_col"])
        icon(d, kind, x, min(h, 900), col)
        if h > 18:
            ly = max(575, GY - min(h, 900)); dashed(d, (x + (40 if side == "L" else -40), ly), (CX - 22 if side == "L" else CX + 22, ly), (130, 136, 180))
            fr.text((x, ly - 58), name, HF(26), col, anchor="ma"); fr.text((x, ly - 30), cfg["fmt"](hm), HF(22, "SemiBold"), DIM, anchor="ma")
    # --- sky markers (plane, space line, Moon, Sun, ...) ---
    for name, dm, kind in cfg["markers"]:
        h = dm * ppm
        if h < 10 or dm > L * 1.02: continue
        y = GY - h
        if y < 560: continue
        if kind == "line":
            dashed(d, (110, y), (1000, y), (110, 170, 255), 2, 12); fr.text((150, y - 34), f"{name} {cfg['fmt'](dm)}", HF(26), (140, 190, 255)); continue
        mx = CX - 200
        if kind == "moon": d.ellipse((mx - 14, y - 14, mx + 14, y + 14), fill=(200, 200, 210))
        elif kind == "sun":
            for g, a in ((46, 40), (32, 90)): d.ellipse((mx - g, y - g, mx + g, y + g), fill=(255, 200, 80))
            d.ellipse((mx - 22, y - 22, mx + 22, y + 22), fill=(255, 236, 140))
        elif kind == "planet": d.ellipse((mx - 9, y - 9, mx + 9, y + 9), fill=(170, 150, 200))
        elif kind == "star":
            d.ellipse((mx - 20, y - 20, mx + 20, y + 20), fill=(120, 160, 255)); d.ellipse((mx - 10, y - 10, mx + 10, y + 10), fill=(235, 245, 255))
        elif kind == "plane": d.polygon([(mx - 18, y), (mx + 18, y - 4), (mx + 18, y + 4)], fill=(200, 210, 230))
        dashed(d, (mx + 28, y), (CX - 24, y), (130, 136, 180))
        fr.text((mx, y - 66), name, HF(28), WHITE, anchor="ma"); fr.text((mx, y - 36), cfg["fmt"](dm), HF(22, "SemiBold"), DIM, anchor="ma")
    # --- the column ---
    d = column(fr.img, max(TOPY - 10, top), GY); fr.d = d
    # --- story line ---
    cur = None
    for (ts, text, kw) in cfg["story"]:
        if t >= ts: cur = (ts, text, kw)
    if cur:
        ts, text, kw = cur; a = min(1, (t - ts) / .25); f = HF(50)
        parts = text.split(kw) if kw else [text]
        segs = [(parts[0], WHITE)] + ([(kw, GOLDL), (parts[1], WHITE)] if kw and len(parts) > 1 else [])
        tw = sum(d.textlength(s, font=f) for s, _ in segs); x = 520 - tw / 2; y = 1092 + (1 - a) * 16
        for s, c in segs:
            if s: fr.text((x, y), s, f, c, stroke=3, stroke_fill=(10, 12, 30)); x += d.textlength(s, font=f)
