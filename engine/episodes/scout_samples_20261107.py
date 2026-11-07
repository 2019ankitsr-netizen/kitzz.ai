"""Scout samples, 7 Nov 2026: three short style tests (music + SFX, no voice) for the top picks in scout_20261107.txt.
A  S4 Hook Shots   - grapheme-safe text presets (elastic rise, weight morph, collapse-burst, centre-out Hindi stagger)
B  S1 How Things Work - hidden-line isometric draw-on (front parts first, hidden lines never show) + hatch sweep + signal dot
C  Festival        - Warli Chhath scene that draws itself (payoff first)
Methods ported from the scouted repos' ideas, all code written here from scratch. Run: python3 episodes/scout_samples_20261107.py out/
"""
import os, sys, math, random, subprocess, unicodedata, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import audio as A
from reel import ease, eout, eback, FPS
from style_frames import Frame, F, FM, SAFE, RAIL, W, H, caption
from drawon import Sketch, ellipse_pts, bez
import fx

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
INTER = "/usr/share/fonts/opentype/inter/"
WEIGHTS = ["Thin", "ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]
POP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"      # has Devanagari
_fc = {}
def FW(wt, s):
    k = (wt, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(f"{INTER}Inter-{wt}.otf", s)
    return _fc[k]
def HP(s):
    k = ("pop", s)
    if k not in _fc: _fc[k] = ImageFont.truetype(POP, s, layout_engine=ImageFont.Layout.RAQM)
    return _fc[k]

# ---------------- grapheme clusters (Devanagari-safe) ----------------
VIRAMA, ZWJ, ZWNJ = "्", "‍", "‌"
def clusters(s):
    """Split into user-perceived letters: combining marks, nukta, matras and virama+consonant (conjuncts) stay attached."""
    out = []
    for ch in s:
        if out and (unicodedata.category(ch).startswith("M") or ch in (ZWJ, ZWNJ) or out[-1].endswith(VIRAMA)):
            out[-1] += ch
        else: out.append(ch)
    return out

def stagger_order(n, order):
    idx = list(range(n))
    if order == "center": idx.sort(key=lambda i: abs(i - (n - 1) / 2))
    elif order == "edges": idx.sort(key=lambda i: -abs(i - (n - 1) / 2))
    elif order == "end": idx.reverse()
    elif order == "random": random.Random(4).shuffle(idx)
    rank = [0] * n
    for r, i in enumerate(idx): rank[i] = r
    return rank

def text_preset(fr, t, t0, s, xy, font, col, preset="elastic-rise", order="start", stagger=.03, dur=.38, anchor_center=False):
    """Draw string s with a per-letter enter preset. Letter x comes from the shaped prefix width, so kerning/conjuncts hold."""
    cl = clusters(s); rank = stagger_order(len(cl), order); d = fr.d
    total = d.textlength(s, font=font); x0 = xy[0] - (total / 2 if anchor_center else 0)
    acc = ""
    for i, c in enumerate(cl):
        px = x0 + d.textlength(acc, font=font); acc += c
        if c.isspace(): continue
        a = (t - t0 - rank[i] * stagger) / dur
        if a <= 0: continue
        if preset == "elastic-rise":
            k = eback(a, 2.4); fr.text((px, xy[1] + (1 - k) * 90), c, font, col)
        elif preset == "drop-in":
            k = eback(a, 1.8); fr.text((px, xy[1] - (1 - k) * 120), c, font, col)
        elif preset == "fade-up":
            k = eout(a); cc = tuple(int(244 + (v - 244) * k) for v in col); fr.text((px, xy[1] + (1 - k) * 40), c, font, cc)

def burst_out(fr, t, t0, s, xy, font, col, dur=.45, seed=3):
    """collapse-burst exit: each letter flies off with a spin and falls (rendered as rotated tiles)."""
    a = (t - t0) / dur
    if a >= 1: return
    rr = random.Random(seed); d = fr.d; acc = ""
    for c in clusters(s):
        px = xy[0] + d.textlength(acc, font=font); acc += c
        vx, vy, rot = rr.uniform(-520, 520), rr.uniform(-700, -250), rr.uniform(-260, 260)
        if c.isspace(): continue
        k = max(0, a); x = px + vx * k; y = xy[1] + vy * k + 1900 * k * k
        bb = d.textbbox((0, 0), c, font=font); tw, th = bb[2] + 20, bb[3] + 20
        tile = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); ImageDraw.Draw(tile).text((10, 10), c, font=font, fill=col + (255,))
        tile = tile.rotate(rot * k, expand=True, resample=Image.BICUBIC)
        if k > 0 and (y < SAFE[1] or y + tile.height > SAFE[3] or x < SAFE[0] or x + tile.width > SAFE[2]):
            continue                                               # letters vanish as they leave the safe zone
        fr.img.paste(tile, (int(x), int(y)), tile); fr.box((int(x), int(y), int(x) + tile.width, int(y) + tile.height), "burst " + c)

def morph_weight(fr, t, t0, s, xy, size, col, dur=.5):
    """Key word swells Thin -> Black on the beat (stepped through Inter's 9 static weights)."""
    if t < t0: return
    k = eout((t - t0) / dur); wt = WEIGHTS[min(8, int(k * 8.999))]
    fr.text(xy, s, FW(wt, size), col)

def sample_tag(fr, text, col):
    fr.text((92, 292), text, FM(28), col)

# ============ A · S4 Hook Shots ============
def scene_A(fr, t):
    BG, INK, RED = (244, 241, 234), (15, 15, 15), (225, 30, 30)
    fr.img.paste(BG, (0, 0, W, H)); fr.d = ImageDraw.Draw(fr.img); d = fr.d
    sample_tag(fr, "HOOK SHOTS · TEXT PRESETS · SAMPLE", RED)
    if t < 3.0:
        text_preset(fr, t, 0.0, "This one word", (90, 480), FW("Black", 104), INK, "elastic-rise", "start")
        morph_weight(fr, t, 0.55, "changes", (90, 620), 190, RED)
        text_preset(fr, t, 0.95, "every answer.", (90, 850), FW("Black", 104), INK, "elastic-rise", "center", stagger=.025)
    elif t < 3.5:
        text_preset(fr, t, -9, "This one word", (90, 480), FW("Black", 104), INK)
        burst_out(fr, t, 3.0, "changes", (90, 620), FW("Black", 190), RED)
        text_preset(fr, t, -9, "every answer.", (90, 850), FW("Black", 104), INK)
    else:
        text_preset(fr, t, 3.5, "कौन सा शब्द?", (540, 480), HP(136), INK, "drop-in", "center", stagger=.05, anchor_center=True)
        text_preset(fr, t, 4.1, "क्षमा · स्त्री · ज़्यादा", (540, 720), HP(84), (110, 106, 100), "fade-up", "edges", stagger=.06, anchor_center=True)
        fr.text((540, 850), "conjuncts stay whole", FW("Bold", 44), (150, 146, 140), anchor="ma") if t > 4.8 else None
        if t > 5.3:
            fx.verdict_pill(fr, t, 5.3, "WAIT FOR IT", (90, 950), size=88, bg=RED)
    caption(fr, "Kinetic hook presets,", "English + Hindi") if t > 1.6 and t < 3.0 else None

# ============ B · S1 How Things Work ============
S_ISO = 1.2
def iso(x, y, z, ox=540, oy=760):
    c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
    return (ox + (x - y) * c * S_ISO, oy + (x + y) * s * S_ISO - z * S_ISO)

def box_faces(x, y, z, dx, dy, dz):
    P = lambda a, b, c: iso(a, b, c)
    top = [P(x, y, z + dz), P(x + dx, y, z + dz), P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)]
    left = [P(x, y + dy, z), P(x + dx, y + dy, z), P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)]   # face toward viewer-left
    right = [P(x + dx, y, z), P(x + dx, y + dy, z), P(x + dx, y + dy, z + dz), P(x + dx, y, z + dz)]  # face toward viewer-right
    return top, left, right

def shade(c, k): return tuple(int(v * k) for v in c)

# parts: name, box, colour, label, label-anchor   (nearer = larger x+y+z)
PARTS = [
    ("port",  (300, 120, 40, 30, 70, 34), (255, 210, 60), "USB-C port"),
    ("chip",  (150, 40, 40, 140, 200, 18), (40, 200, 140), "Charge chip"),
    ("cell3", (0, 190, 40, 130, 70, 70), (80, 140, 255), None),
    ("cell2", (0, 110, 40, 130, 70, 70), (80, 140, 255), None),
    ("cell1", (0, 30, 40, 130, 70, 70), (80, 140, 255), "Li-ion cells"),
    ("floor", (-30, 0, 0, 380, 290, 40), (70, 80, 110), None),
    ("wallL", (-30, 0, 40, 20, 290, 150), (60, 70, 100), None),
    ("wallB", (-30, 0, 40, 380, 20, 150), (52, 60, 90), "Case (cut open)"),
]
OUT_C = (8, 12, 24)

def build_B():
    parts = []
    for name, (x, y, z, dx, dy, dz), col, label in PARTS:
        top, left, right = box_faces(x, y, z, dx, dy, dz)
        sk = Sketch(seed=hash(name) % 99)
        for face, k in ((top, 1.0), (left, .72), (right, .55)):
            sk.shape(face, shade(col, k), OUT_C, 6, cost=30)
        sil = Image.new("L", (W, H), 0); sd = ImageDraw.Draw(sil)
        for f in (top, left, right): sd.polygon(f, fill=255)
        parts.append(dict(name=name, sk=sk, sil=sil, col=col, label=label, faces=(top, left, right),
                          anchor=iso(x + dx, y + dy / 2, z + dz)))
    return parts

def hatch_layer(face, col, spacing=18):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    xs = [p[0] for p in face]; ys = [p[1] for p in face]
    lines = []
    for c in range(int(min(xs) - (max(ys) - min(ys))), int(max(xs)), spacing):
        lines.append(((c, max(ys)), (c + (max(ys) - min(ys)), min(ys))))
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(face, fill=255)
    return lines, m

PB = None
def scene_B(fr, t):
    global PB
    if PB is None:
        PB = build_B()
        acc = Image.new("L", (W, H), 0)
        for p in PB:                                     # front-to-back: mask = everything nearer
            p["mask"] = Image.eval(acc, lambda v: 255 - v); acc = Image.composite(Image.new("L", (W, H), 255), acc, p["sil"])
            p["hatch"] = hatch_layer(p["faces"][2], p["col"])
    BG = (10, 18, 38)
    fr.img.paste(BG, (0, 0, W, H)); d = ImageDraw.Draw(fr.img); fr.d = d
    for x in range(-W, 2 * W, 60):
        d.line((x, 0, x + H * .577, H), fill=(22, 36, 70), width=1); d.line((x, 0, x - H * .577, H), fill=(22, 36, 70), width=1)
    sample_tag(fr, "HOW THINGS WORK · SAMPLE", (255, 210, 60))
    k = eback(min(1, t / .35)); fr.text((90, 330 + (1 - k) * 60), "What's inside a\npower bank?", F("black", 74), (255, 255, 255), spacing=4)
    T0, per = 0.5, 0.55
    for i, p in enumerate(PB):
        pr = (t - T0 - i * per) / per
        if pr <= 0: continue
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        tip = p["sk"].draw(ld, min(1, pr))
        # hatch sweep on the shadow face after the part is drawn
        hp = (t - T0 - i * per - per) / .4
        if hp > 0:
            lines, m = p["hatch"]; n = int(min(1, hp) * len(lines))
            hl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hl)
            for a, b in lines[:n]: hd.line((a, b), fill=OUT_C + (110,), width=3)
            lay.alpha_composite(Image.composite(hl, Image.new("RGBA", (W, H), (0, 0, 0, 0)), m))
        al = lay.getchannel("A"); lay.putalpha(Image.composite(al, Image.new("L", (W, H), 0), p["mask"]))
        fr.img.paste(lay, (0, 0), lay); d = ImageDraw.Draw(fr.img); fr.d = d
        if tip and pr < 1 and p["mask"].getpixel((int(tip[0]), int(tip[1]))) > 0:
            d.ellipse((tip[0] - 9, tip[1] - 9, tip[0] + 9, tip[1] + 9), fill=(255, 255, 255))
        fr.box((min(x for f in p["faces"] for x, _ in f), min(y for f in p["faces"] for _, y in f),
                max(x for f in p["faces"] for x, _ in f), max(y for f in p["faces"] for _, y in f)), "part " + p["name"])
    tl = T0 + len(PB) * per + .3                          # labels
    LBL = {"port": (660, 1110), "chip": (660, 1170), "cell1": (90, 1010), "wallB": (690, 560)}
    for j, p in enumerate([q for q in PB if q["label"]]):
        a = t - tl - j * .18
        if a <= 0: continue
        lx, ly = LBL[p["name"]]; ax, ay = p["anchor"]
        kk = eout(a / .3); ex, ey = ax + (lx - ax) * kk, ay + (ly + 22 - ay) * kk
        d.line((ax, ay, ex, ey), fill=(120, 230, 255), width=3); d.ellipse((ax - 7, ay - 7, ax + 7, ay + 7), fill=(120, 230, 255))
        if kk > .9: fr.text((lx, ly), p["label"], F("b", 40), (255, 255, 255), stroke=4, stroke_fill=BG)
    # signal: port -> chip -> cells
    path_pts = [iso(330, 155, 74), iso(260, 155, 58), iso(200, 140, 58), iso(130, 140, 110), iso(65, 225, 110), iso(65, 65, 110)]
    path = []
    for a, b in zip(path_pts, path_pts[1:]):
        for s in range(12): path.append((a[0] + (b[0] - a[0]) * s / 12, a[1] + (b[1] - a[1]) * s / 12))
    path.append(path_pts[-1])
    fx.travel(d, t, tl + 1.0, path, dur=1.6)

# ============ C · Festival: Warli Chhath ============
TERRA, WH = (150, 72, 46), (246, 238, 222)
def warli_fig(s, x, y, sc=1.0, arms="up", soop=False):
    h = 14 * sc
    s.line(ellipse_pts(x, y - 5.2 * h, 1.1 * h, 1.1 * h, n=20), WH, max(3, int(.35 * h)))
    s.shape([(x - 1.5 * h, y - 4 * h), (x + 1.5 * h, y - 4 * h), (x, y - 1.8 * h)], WH, None, cost=10)
    s.shape([(x, y - 1.8 * h), (x - 1.6 * h, y + .3 * h), (x + 1.6 * h, y + .3 * h)], WH, None, cost=10)   # sari: wider lower triangle
    lw = max(3, int(.3 * h))
    if arms == "up":
        s.line([(x - 1.3 * h, y - 3.8 * h), (x - 2.3 * h, y - 5.6 * h), (x - 1.3 * h, y - 7.0 * h)], WH, lw)
        s.line([(x + 1.3 * h, y - 3.8 * h), (x + 2.3 * h, y - 5.6 * h), (x + 1.3 * h, y - 7.0 * h)], WH, lw)
        if soop:   # soop (winnowing basket) held up, with fruit dots
            s.shape([(x - 2.2 * h, y - 7.0 * h), (x + 2.2 * h, y - 7.0 * h), (x + 1.4 * h, y - 8.0 * h), (x - 1.4 * h, y - 8.0 * h)], WH, None, cost=8)
            for j in range(3): s.dot(x - h + j * h, y - 8.6 * h, .45 * h, WH, 3)
    else:
        s.line([(x - 1.3 * h, y - 3.8 * h), (x - 2.4 * h, y - 2.2 * h)], WH, lw); s.line([(x + 1.3 * h, y - 3.8 * h), (x + 2.4 * h, y - 2.2 * h)], WH, lw)
    s.line([(x - .7 * h, y + .3 * h), (x - .9 * h, y + 2 * h)], WH, lw); s.line([(x + .7 * h, y + .3 * h), (x + .9 * h, y + 2 * h)], WH, lw)

def build_C():
    s = Sketch(wobble=.8, seed=12)
    sx, sy = 540, 562                                         # setting sun (Surya)
    s.line(ellipse_pts(sx, sy, 92, 92, n=48), WH, 8)
    for i in range(20):
        a = i * math.pi / 10; s.line([(sx + 110 * math.cos(a), sy + 110 * math.sin(a)), (sx + 128 * math.cos(a), sy + 128 * math.sin(a))], WH, 5)
    for i in range(10): s.dot(sx + 52 * math.cos(i * .628), sy + 52 * math.sin(i * .628), 7, WH, 4)
    for x in (130, 880):                                 # sugarcane stalks with leaves
        s.line([(x, 1000), (x, 700)], WH, 6)
        for j in range(4):
            yy = 960 - j * 70; s.line([(x, yy), (x + 34, yy - 40)], WH, 4); s.line([(x, yy - 20), (x - 34, yy - 60)], WH, 4)
    for r in range(4):                                        # river (wave lines)
        y0 = 840 + r * 42
        s.line([(110 + i * 19, y0 + 9 * math.sin(i * .7 + r)) for i in range(41)], WH, 4)
    for i, x in enumerate((265, 420, 640, 790)):              # women in the water offering arghya
        warli_fig(s, x, 880, 1.5, "up", soop=True)
    for i in range(9):                                        # ghat steps + diyas
        x = 140 + i * 90
        s.shape([(x - 20, 1060), (x + 20, 1060), (x, 1080)], WH, None, cost=6)
        s.shape([(x - 6, 1058), (x + 6, 1058), (x, 1032)], (255, 196, 70), None, cost=6)
    s.line([(110, 1092), (900, 1092)], WH, 5)
    return s

SC = None; C_BG = C_DONE = None
def scene_C(fr, t):
    global SC, C_BG, C_DONE
    if SC is None:
        SC = build_C(); C_BG = Image.new("RGB", (W, H), TERRA); C_DONE = C_BG.copy(); SC.draw(ImageDraw.Draw(C_DONE), 1)
    im, tip = fx.payoff_first(t, C_BG, C_DONE, [SC], show=.8, rewind=.5, draw=4.6, arrows=True)
    fr.img.paste(im); d = ImageDraw.Draw(fr.img); fr.d = d
    if tip: d.ellipse((tip[0] - 10, tip[1] - 10, tip[0] + 10, tip[1] + 10), fill=(255, 196, 70))
    fr.text((92, 292), "FESTIVAL · वारली · SAMPLE", HP(30), (255, 214, 160))
    fr.text((540, 330), "छठ पूजा, वारली में", HP(84), WH, anchor="ma")
    for b in [(100, 400, 910, 1100)]: fr.box(b, "scene")
    if t > 6.0:
        a = t - 6.0; k = eback(min(1, a / .35))
        d.rounded_rectangle((160, 1120, 160 + 720 * k, 1210), 40, fill=(246, 238, 222))
        if k > .9: fr.text((520, 1165), "गोला · त्रिकोण · रेखा", HP(52), TERRA, anchor="mm")

# ============ render ============
def render(name, scene, dur, music, events):
    os.makedirs(OUT, exist_ok=True)
    bed = A.music(music, dur, seed=7)
    sfx = np.zeros(int(A.SR * (dur + 1)), np.float32)
    for tt, kind in events: A.place(sfx, A.sfx(kind), tt)
    mix = bed * .55 + sfx[:len(bed)] * 1.0
    raw = f"{OUT}/{name}_raw.wav"; wav = f"{OUT}/{name}.wav"; sf.write(raw, mix, A.SR); A.loudnorm(raw, wav); os.remove(raw)
    vid = f"{OUT}/{name}_v.mp4"; n = int(dur * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    viol, sheet = [], []
    stills = [round(x * dur / 12, 2) for x in range(12)]
    for i in range(n):
        t = i / FPS; fr = Frame(name, Image.new("RGB", (W, H))); scene(fr, t)
        if i % 15 == 0:
            for lab, bb, why in fr.check(): viol.append((round(t, 2), lab, [int(v) for v in bb], why))
        if any(abs(t - s) < .5 / FPS for s in stills): sheet.append((t, fr.img.convert("RGB").copy()))
        p.stdin.write(fr.img.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    final = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", final], check=True); os.remove(vid); os.remove(wav)
    tw, th, cols = 270, 480, 6; rows = math.ceil(len(sheet) / cols)
    sh = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 40) + 8), (250, 250, 250)); sd = ImageDraw.Draw(sh)
    for k, (t, im) in enumerate(sheet):
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for r in [(0, 0, W, SAFE[1]), (0, SAFE[3], W, H), (0, SAFE[1], SAFE[0], SAFE[3]), (SAFE[2], SAFE[1], W, SAFE[3])]: od.rectangle(r, fill=(230, 40, 40, 85))
        od.rectangle(RAIL, fill=(255, 170, 0, 85))
        x = 8 + (k % cols) * (tw + 8); y = 8 + (k // cols) * (th + 40)
        sh.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").resize((tw, th)), (x, y)); sd.text((x, y + th + 6), f"{t:.1f}s", font=F("b", 24), fill=(30, 30, 30))
    sh.save(f"{OUT}/{name}_contact_safezone.png")
    print(name, "violations:", len(viol)); [print("  ", v) for v in viol[:12]]
    return final

if __name__ == "__main__":
    which = sys.argv[2] if len(sys.argv) > 2 else "ABC"
    if "A" in which:
        render("sampleA_S4_text_presets", scene_A, 7.0, "swiss", [(0, "whoosh"), (.55, "hit"), (.95, "whoosh"), (3.0, "whoosh"), (3.5, "pop"), (4.1, "tick"), (5.3, "hit")])
    if "B" in which:
        ev = [(0.5 + i * .55, "tick") for i in range(len(PARTS))] + [(0.5 + len(PARTS) * .55 + .3 + j * .18, "pop") for j in range(4)] + [(0.5 + len(PARTS) * .55 + 1.3, "beep")]
        render("sampleB_S1_hidden_line_iso", scene_B, 8.5, "xray", ev)
    if "C" in which:
        render("sampleC_festival_warli_chhath", scene_C, 7.5, "festive", [(.8, "whoosh"), (1.3, "tick"), (6.0, "pop"), (6.4, "chime")])
