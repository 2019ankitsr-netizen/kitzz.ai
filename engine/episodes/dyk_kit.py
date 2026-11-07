"""'क्या आप जानते हैं?' Diwali Did-You-Know kit — gold scratch-card reveal + fact chips."""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(__file__))
from diwali_common import *

V = "hf_alpha"
GOLD = (236, 190, 80)

def bg():
    yy = np.linspace(0, 1, H)[:, None, None]
    g = np.array([8, 48, 44]) + (np.array([4, 22, 30]) - np.array([8, 48, 44])) * yy
    im = Image.fromarray(np.repeat(g, W, axis=1).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    for x in range(-200, W + 200, 120):                                   # faint jaali (lattice) pattern
        for y in range(240, 1300, 120):
            d.polygon([(x, y - 50), (x + 50, y), (x, y + 50), (x - 50, y)], outline=(20, 70, 64))
    return im
BG = bg()

_rng = np.random.default_rng(5)
FOIL = Image.fromarray(np.clip(_rng.normal(0, 18, (H // 4, W // 4)) + np.array([0]), -40, 40).astype(np.int16).astype(np.uint8))
def foil_layer(box):
    x0, y0, x1, y1 = box
    base = Image.new("RGBA", (x1 - x0, y1 - y0), (214, 170, 70, 255))
    n = Image.fromarray((_rng.random((y1 - y0, x1 - x0)) * 40).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1))
    shade = Image.merge("RGBA", (n, n, n, Image.new("L", n.size, 255)))
    base = Image.blend(base, Image.alpha_composite(base, shade), .6)
    d = ImageDraw.Draw(base)
    for i in range(-(y1 - y0), x1 - x0, 36): d.line((i, 0, i + (y1 - y0), y1 - y0), fill=(240, 205, 120, 120), width=6)
    return base
CARD = (100, 390, 980, 760)
FOILIMG = foil_layer(CARD)

def scratch_mask(p):
    """Zig-zag scratch path covering the card; p = 0..1 progress. Returns (mask, coin_xy)."""
    x0, y0, x1, y1 = CARD; m = Image.new("L", (x1 - x0, y1 - y0), 0); d = ImageDraw.Draw(m)
    rows = 6; pts = []
    for r in range(rows):
        y = (r + .5) / rows * (y1 - y0)
        xs = (40, x1 - x0 - 40) if r % 2 == 0 else (x1 - x0 - 40, 40)
        pts += [(xs[0], y), (xs[1], y)]
    seg = len(pts) - 1; total = p * seg; coin = pts[0]
    for i in range(seg):
        k = min(1, max(0, total - i))
        if k <= 0: break
        a, b = pts[i], pts[i + 1]; e = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        d.line((a, e), fill=255, width=110); d.ellipse((e[0] - 55, e[1] - 55, e[0] + 55, e[1] + 55), fill=255); coin = e
    return m.filter(ImageFilter.GaussianBlur(2)), (coin[0] + x0, coin[1] + y0)

def card_scene(fr, t, R, headline, sub, chips, reveal_tag="hook", chip_tags=(), accent=GOLD, deco=None):
    fr.img = BG.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    T = R.T; L0 = R.line(reveal_tag)
    fr.text((90, 292), "क्या आप जानते हैं?", HF(56), GOLD)
    fr.text((990, 300), "DIWALI · DID YOU KNOW", FM(26), (150, 210, 200), anchor="ra")
    x0, y0, x1, y1 = CARD
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((x0 + 10, y0 + 14, x1 + 10, y1 + 14), 40, fill=(0, 0, 0, 110))
    ld.rounded_rectangle(CARD, 40, fill=(255, 248, 232, 255), outline=accent + (255,), width=8)
    fr.img.alpha_composite(lay); fr.d = d = ImageDraw.Draw(fr.img)
    hf = HF(118 if len(headline) < 14 else 92)
    fr.text((540, 540), headline, hf, (150, 30, 20), anchor="mm")
    fr.text((540, 680), sub, HF(54), (60, 60, 60), anchor="mm")
    # scratch foil (finished a little before the hook line ends)
    p = ease((t - (L0.t0 + .5)) / max(.8, (L0.t1 - L0.t0) * .75))
    if p < 1:
        mask, coin = scratch_mask(p)
        f = FOILIMG.copy(); a = f.getchannel("A"); a.paste(Image.eval(mask, lambda v: 255 - v)); f.putalpha(a)
        rounded = Image.new("L", f.size, 0); ImageDraw.Draw(rounded).rounded_rectangle((0, 0, f.width - 1, f.height - 1), 40, fill=255)
        f.putalpha(Image.composite(f.getchannel("A"), Image.new("L", f.size, 0), rounded))
        fr.img.alpha_composite(f, (x0, y0)); d = ImageDraw.Draw(fr.img); fr.d = d
        if p < .02: fr.text((540, 585), "स्क्रैच करो", HF(80), (110, 60, 10), anchor="mm")
        if p > 0:
            cx, cy = coin; d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), fill=(200, 200, 205), outline=(140, 140, 150), width=5)
            d.text((cx, cy), "₹", font=F("black", 46), fill=(120, 120, 130), anchor="mm")
        fr.boxes = [b for b in fr.boxes if b[0] not in (headline, sub)]
    if deco: deco(fr, t, R); d = fr.d = ImageDraw.Draw(fr.img)
    # fact chips stack below the card, one per line tag
    shown = [(txt, tag) for txt, tag in zip(chips, chip_tags) if t >= T(tag) - .1]
    if shown:
        txt, tag = shown[-1]; k = eback((t - T(tag)) / .35)
        font = HF(54); w = d.textlength(txt, font=font) + 80
        cx = 520; y = 785
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((cx - w / 2 * k, y, cx + w / 2 * k, y + 96), 48, fill=accent + (255,))
        fr.img.alpha_composite(lay); fr.d = d = ImageDraw.Draw(fr.img)
        if k > .8: fr.text((cx, y + 48), txt, font, (40, 20, 10), anchor="mm")

def build_dyk(name, lines, scene, out, cta_head, cta_body, nudge_text, seed):
    for L in lines: L.speed = round(L.speed * 1.04, 3)
    nudge = dict(text=nudge_text, icon="send", bg=GOLD, fg=(40, 20, 10), fontfile=f"{FONTS}/Hind-Bold.ttf")
    cta = dict(icon="send", head=cta_head, body=cta_body, bg=(255, 248, 232), acc=(160, 40, 20), fg=(40, 20, 10), fontfile=f"{FONTS}/Hind-Bold.ttf")
    return build(name, lines, scene, out, music="festive", nudge=nudge, cta=cta, seed=seed, cap_bg=(6, 40, 36, 220))
