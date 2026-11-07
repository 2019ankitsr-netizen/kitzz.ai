"""Diwali 2026 · Phuljhadi Wishes — sparkler light-painting greeting (send to the family group)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from diwali_common import *

V = "hf_alpha"
LINES = [
    HL(V, "इस दिवाली...", tag="hook", sfx="whoosh", gap=.25),
    HL(V, "आपका घर, रोशनी से भरा रहे।", tag="l1", sfx="tick"),
    HL(V, "दिल, अपनों से।", tag="l2", sfx="tick"),
    HL(V, "मिठाई का डिब्बा, कभी खाली न हो।", tag="l3", sfx="tick"),
    HL(V, "और फ़ैमिली ग्रुप में, सिर्फ़ असली फ़ोटो जाएँ। ए आई वाली नकली नहीं।",
       "और फ़ैमिली ग्रुप में सिर्फ़ असली फ़ोटो जाएँ, AI वाली नकली नहीं।", pre=.3, pitch=.5, tag="l4", sfx="pop"),
    HL(V, "शुभ दीपावली!", pitch=.5, tag="finale", sfx="chime", gap=.5),
    HL(V, "ये रील अपने फ़ैमिली ग्रुप में भेजो, और सबसे पहले विश करो।", tag="cta", sfx="pop", gap=.3),
]
BG = night_bg()
def _garland(im):
    d = ImageDraw.Draw(im)
    for x in range(40, 1060, 34):
        y = 352 + 26 * math.sin((x - 40) / 1020 * math.pi * 3) ** 2
        d.ellipse((x - 19, y - 19, x + 19, y + 19), fill=(255, 150, 20) if (x // 34) % 2 else (255, 200, 40))
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(230, 110, 10))
    for x in range(90, 1000, 170): d.polygon([(x, 380), (x + 22, 430), (x - 22, 430)], fill=(40, 140, 60))
    return im
BG = _garland(BG)
WRITE = {"hook": ["इस दिवाली..."], "l1": ["आपका घर", "रोशनी से भरा रहे"], "l2": ["दिल,", "अपनों से"],
         "l3": ["मिठाई का डिब्बा", "कभी खाली न हो"], "l4": ["फ़ैमिली ग्रुप में", "सिर्फ़ असली फ़ोटो"], "finale": ["शुभ", "दीपावली"]}
SP = Sparks()
def render_lines(fr, rows, font, col, y_top, reveal, glow=True):
    """Write rows left->right up to `reveal` (0..1 over all rows); return the sparkler head position."""
    d = fr.d; total = sum(d.textlength(r, font=font) for r in rows); done = reveal * total; head = None
    lh = font.size * 1.35
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, r in enumerate(rows):
        w = d.textlength(r, font=font); x0 = 540 - w / 2; y = y_top + i * lh
        show = max(0, min(w, done)); done -= w
        if show <= 0: continue
        rl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(rl).text((x0, y), r, font=font, fill=col)
        if show < w:
            a = rl.getchannel("A"); ImageDraw.Draw(a).rectangle((x0 + show, 0, W, H), fill=0); rl.putalpha(a)
            head = (x0 + show, y + font.size * .6)
        layer.alpha_composite(rl)
        fr.boxes.append((r, (x0, y, x0 + w, y + font.size * 1.25)))
    if glow:
        g = layer.copy(); g.putalpha(g.getchannel("A").point(lambda v: v * .8))
        tint = Image.new("RGBA", (W, H), (255, 140, 30, 0)); tint.putalpha(g.getchannel("A"))
        fr.img.alpha_composite(tint.filter(ImageFilter.GaussianBlur(16)))
    fr.img.alpha_composite(layer); fr.d = ImageDraw.Draw(fr.img)
    return head

def scene(fr, t, R):
    fr.img = BG.copy(); d = ImageDraw.Draw(fr.img); fr.d = d
    for i, x in enumerate((180, 400, 680, 900)):                               # diyas along the bottom of the safe zone
        paste_glow(fr.img, x, 1000, 90, (255, 150, 40, 70))
    d = ImageDraw.Draw(fr.img); fr.d = d
    for i, x in enumerate((180, 400, 680, 900)): diya(d, x, 1020, .9, t, i * 1.7)
    L = R.active(t) or R.lines[0]; tag = L.tag
    src = []
    if tag in WRITE:
        rows = WRITE[tag]; fin = tag == "finale"
        font = YF(170) if fin else YF(104)
        dur = (L.t1 - L.t0) * (.9 if not fin else .7)
        rev = min(1, max(0, (t - L.t0 + .1) / max(.4, dur)))
        out = ease((t - (L.t1 + L.gap - .25)) / .25)                            # fade the line out before the next one
        col = (255, 214, 120) if fin else (255, 244, 220)
        if out < 1:
            head = render_lines(fr, rows, font, col, 470 if not fin else 420, rev)
            if head: src.append((head[0], head[1], 1.0))
        if fin and rev >= 1:
            k = t - (L.t0 + dur)
            if 0 <= k < .6: src += [(540 + 300 * math.cos(a), 640 + 160 * math.sin(a), 1.5) for a in (0, 1.6, 3.2, 4.8)]
    elif tag == "cta":
        render_lines(fr, ["शुभ दीपावली"], YF(100), (255, 214, 120), 380, 1.0, glow=True)
    SP.step(t, src, rate=150); d = ImageDraw.Draw(fr.img)
    for (hx, hy, k) in src[:1]:                                                 # the sparkler itself: stick + white-hot head
        d.line((hx, hy, hx + 70, hy + 210), fill=(120, 120, 125), width=6)
        paste_glow(fr.img, hx, hy, 60, (255, 230, 150, 160)); d = ImageDraw.Draw(fr.img)
        d.ellipse((hx - 10, hy - 10, hx + 10, hy + 10), fill=(255, 255, 240))
    SP.draw(d); fr.d = ImageDraw.Draw(fr.img)
    fr.text((90, 292), "KITZZ.AI · DIWALI 2026", FM(30), (255, 200, 120))

if __name__ == "__main__":
    nudge = dict(text="फ़ैमिली ग्रुप में भेजो", icon="send", bg=(255, 196, 70), fg=(60, 15, 20), fontfile=f"{FONTS}/Hind-Bold.ttf")
    cta = dict(icon="send", head="भेजो!", body="फ़ैमिली ग्रुप में\nसबसे पहले विश करो।", bg=(255, 246, 230), acc=(200, 60, 30), fg=(60, 15, 20),
               fontfile=f"{FONTS}/Hind-Bold.ttf")
    R, p = build("Diwali2026_01_PhuljhadiWishes", LINES, scene, sys.argv[1], nudge=nudge, cta=cta, seed=81)
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
