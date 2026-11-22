"""Sharma Ghar AI Wala · Ep 5 · "Papa, ye AI kya hai?" — STYLE: Video-Call Split (flat, thick outlines).
Papa (Kanpur) and Bunty (Bengaluru) on a call; stickers, typing, sticky-note slaps; zoom punch into Papa for the twist."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from kit import *                      # noqa: F401,F403
import lines48 as LN

NAME = "SharmaGhar_Ep5_PapaYeAIKyaHai"
BG = (255, 236, 214); ORANGE = (255, 122, 40); MAROON = (140, 38, 52); TEAL = (32, 160, 150); NAVY = (36, 52, 96)
SKIN = (233, 182, 140); SKIN2 = (214, 160, 118); GREY = (170, 170, 170); CREAMS = (252, 246, 232); PURPLE = (110, 70, 220)
GROUP = {"hook": "split", "mic": "split", "ask": "split", "result": "split", "wah": "split", "rule1": "split", "rule2": "split",
         "turn": "papa", "lesson": "papa", "haan": "bunty", "cta": "cta", "loop": "loop"}

def background():
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    for x in range(-H, W, 70): d.line((x, 0, x + H, H), fill=(252, 226, 200), width=22)
    return im
BGI = background()

# ---------------------------------------------------------------- characters
def papa(d, cx, cy, s=1.0, talk=0.0, blink=False, mood="calm", t=0):
    r = 95 * s
    # body: cream shirt + maroon sweater vest
    d.rounded_rectangle((cx - 150 * s, cy + 70 * s, cx + 150 * s, cy + 400 * s), int(70 * s), fill=CREAMS, outline=OUT, width=6)
    d.polygon([(cx - 120 * s, cy + 105 * s), (cx, cy + 230 * s), (cx + 120 * s, cy + 105 * s), (cx + 140 * s, cy + 400 * s), (cx - 140 * s, cy + 400 * s)], fill=MAROON, outline=OUT)
    d.line([(cx - 120 * s, cy + 105 * s), (cx, cy + 230 * s), (cx + 120 * s, cy + 105 * s)], fill=OUT, width=6)
    d.rectangle((cx - 28 * s, cy + 60 * s, cx + 28 * s, cy + 110 * s), fill=SKIN2, outline=OUT, width=5)    # neck
    # ears + head
    for sx in (-1, 1): circ(d, cx + sx * r * .98, cy + 8 * s, 22 * s, SKIN)
    d.ellipse((cx - r, cy - r * 1.05, cx + r, cy + r), fill=SKIN, outline=OUT, width=6)
    # grey side hair, shiny forehead
    for sx in (-1, 1):
        d.chord((cx + sx * r * .55 - 45 * s, cy - r * .55, cx + sx * r * .55 + 45 * s, cy + 10 * s), 90 if sx < 0 else -90, 270 if sx < 0 else 90, fill=GREY)
    d.arc((cx - 40 * s, cy - r * .9, cx + 10 * s, cy - r * .55), 200, 300, fill=(255, 225, 190), width=int(7 * s))
    d.line((cx, cy - r * .62, cx, cy - r * .42), fill=(220, 40, 40), width=int(9 * s))          # tilak
    # brows
    by = cy - 28 * s - (14 * s if mood in ("wow", "star") else 0)
    for sx in (-1, 1): d.line((cx + sx * 20 * s, by, cx + sx * 62 * s, by - 6 * s), fill=(120, 120, 120), width=int(11 * s))
    # spectacles
    for sx in (-1, 1): d.rounded_rectangle((cx + sx * 42 * s - 30 * s, cy - 16 * s, cx + sx * 42 * s + 30 * s, cy + 22 * s), int(12 * s), outline=OUT, width=int(6 * s))
    d.line((cx - 12 * s, cy, cx + 12 * s, cy), fill=OUT, width=int(5 * s))
    # eyes
    for sx in (-1, 1):
        ex, ey = cx + sx * 42 * s, cy + 3 * s
        if mood == "star":
            pts = [(ex + math.cos(a) * (16 if i % 2 == 0 else 7) * s, ey + math.sin(a) * (16 if i % 2 == 0 else 7) * s) for i, a in enumerate([j * math.pi / 5 - math.pi / 2 for j in range(10)])]
            d.polygon(pts, fill=(255, 196, 30), outline=OUT)
        elif blink: d.line((ex - 11 * s, ey, ex + 11 * s, ey), fill=OUT, width=int(5 * s))
        else: d.ellipse((ex - 8 * s, ey - 9 * s, ex + 8 * s, ey + 9 * s), fill=OUT)
    # nose, moustache, mouth
    d.arc((cx - 14 * s, cy + 8 * s, cx + 14 * s, cy + 44 * s), 300, 120, fill=OUT, width=int(5 * s))
    mo = 6 * s + 26 * s * talk
    d.ellipse((cx - 26 * s, cy + 58 * s, cx + 26 * s, cy + 58 * s + mo), fill=(120, 30, 40), outline=OUT, width=int(4 * s))
    d.chord((cx - 66 * s, cy + 30 * s, cx + 4 * s, cy + 82 * s), 180, 360, fill=(150, 150, 150), outline=OUT, width=int(4 * s))
    d.chord((cx - 4 * s, cy + 30 * s, cx + 66 * s, cy + 82 * s), 180, 360, fill=(150, 150, 150), outline=OUT, width=int(4 * s))

def bunty(d, cx, cy, s=1.0, talk=0.0, blink=False, mood="calm", t=0):
    r = 88 * s
    d.rounded_rectangle((cx - 150 * s, cy + 70 * s, cx + 150 * s, cy + 400 * s), int(70 * s), fill=TEAL, outline=OUT, width=6)   # hoodie
    d.ellipse((cx - 70 * s, cy + 50 * s, cx + 70 * s, cy + 125 * s), fill=(24, 120, 112), outline=OUT, width=5)            # hood rim
    for sx in (-1, 1): d.line((cx + sx * 26 * s, cy + 110 * s, cx + sx * 30 * s, cy + 190 * s), fill=CREAMS, width=int(7 * s))
    for sx in (-1, 1): circ(d, cx + sx * r * .97, cy + 10 * s, 20 * s, SKIN)
    d.ellipse((cx - r, cy - r, cx + r, cy + r * 1.02), fill=SKIN, outline=OUT, width=6)
    # messy hair
    hair = [(cx - r * 1.02, cy - 5 * s)] + [(cx - r + i * r / 4, cy - r * (1.15 if i % 2 else .9) - (10 * s if i % 2 else 0)) for i in range(9)] + [(cx + r * 1.02, cy - 5 * s), (cx + r * .75, cy - r * .55), (cx - r * .7, cy - r * .55)]
    d.polygon(hair, fill=(35, 28, 28), outline=OUT)
    by = cy - 24 * s - (10 * s if mood == "wow" else 0)
    for sx in (-1, 1): d.line((cx + sx * 18 * s, by + (6 * s if mood == "sheepish" and sx > 0 else 0), cx + sx * 56 * s, by), fill=(35, 28, 28), width=int(10 * s))
    for sx in (-1, 1):
        ex, ey = cx + sx * 38 * s, cy + 4 * s
        if blink or mood == "sheepish": d.arc((ex - 12 * s, ey - 8 * s, ex + 12 * s, ey + 10 * s), 200, 340, fill=OUT, width=int(5 * s))
        else: d.ellipse((ex - 8 * s, ey - 9 * s, ex + 8 * s, ey + 9 * s), fill=OUT)
    d.arc((cx - 12 * s, cy + 6 * s, cx + 12 * s, cy + 38 * s), 300, 120, fill=OUT, width=int(5 * s))
    if talk > .05:
        mo = 6 * s + 24 * s * talk; d.ellipse((cx - 24 * s, cy + 50 * s, cx + 24 * s, cy + 50 * s + mo), fill=(120, 30, 40), outline=OUT, width=int(4 * s))
    else:
        d.arc((cx - 28 * s, cy + 36 * s, cx + 28 * s, cy + 70 * s), 20, 160, fill=OUT, width=int(6 * s))
    if mood == "sheepish":   # sweat drop
        d.polygon([(cx + r * .8, cy - r * .5), (cx + r * .7, cy - r * .2), (cx + r * .9, cy - r * .2)], fill=(120, 200, 255), outline=OUT)
        d.ellipse((cx + r * .68, cy - r * .32, cx + r * .92, cy - r * .1), fill=(120, 200, 255), outline=OUT, width=3)

def mouth(t, R, spk):
    L = R.speaking(t, spk)
    if not L: return 0.0
    return .5 + .5 * math.sin(t * 22) * abs(math.sin(t * 7.3))

def blinking(t, ph=0): return (t + ph) % 3.1 < .12

# ---------------------------------------------------------------- panels
def papa_room(w, h):
    im = Image.new("RGB", (w, h), (250, 204, 102)); d = ImageDraw.Draw(im)
    d.rectangle((0, h - 40, w, h), fill=(214, 160, 80))
    d.rounded_rectangle((w - 260, 50, w - 90, 230), 10, fill=(255, 255, 255), outline=OUT, width=5)       # wall calendar
    d.rectangle((w - 260, 50, w - 90, 100), fill=(220, 50, 50), outline=OUT, width=5)
    d.text((w - 210, 56), "NOV", font=F("black", 36), fill=(255, 255, 255))
    for i in range(4):
        for j in range(5): d.rectangle((w - 245 + j * 30, 112 + i * 28, w - 225 + j * 30, 130 + i * 28), fill=(235, 225, 210))
    d.rectangle((w - 520, 40, w - 340, 170), fill=(255, 250, 235), outline=(120, 80, 40), width=10)         # framed picture
    d.polygon([(w - 510, 160), (w - 450, 80), (w - 400, 140), (w - 370, 110), (w - 350, 160)], fill=(120, 170, 110))
    d.rectangle((40, 18, 380, 30), fill=(255, 255, 240))                                                       # tube light
    return im

def bunty_room(w, h):
    im = Image.new("RGB", (w, h), NAVY); d = ImageDraw.Draw(im)
    d.rectangle((w - 380, 30, w - 60, 250), fill=(18, 26, 56), outline=OUT, width=6)                          # window
    import random; r = random.Random(3)
    for _ in range(40):
        x = r.uniform(w - 370, w - 70); y = r.uniform(120, 245); d.rectangle((x, y, x + 8, y + 8), fill=(255, 214, 110))
    for i in range(6): d.rectangle((w - 370 + i * 52, 150 - (i % 3) * 30, w - 330 + i * 52, 248), outline=(60, 80, 130), width=3)
    d.line((w - 220, 30, w - 220, 250), fill=OUT, width=6)
    d.polygon([(560, 0), (640, 0), (700, h), (500, h)], fill=(48, 66, 116))                                    # lamp glow
    return im
PROOM = papa_room(950, 340); BROOM = bunty_room(950, 328)

def panel(fr, box, room, who, label, t, R, s=1.0, mood="calm", head=(230, 175)):
    x0, y0, x1, y1 = box; w, h = int(x1 - x0), int(y1 - y0)
    im = room.resize((w, h)) if room.size != (w, h) else room.copy(); d = ImageDraw.Draw(im)
    spk = LN.PAPA if who == "papa" else LN.BUNTY; talk = mouth(t, R, spk)
    bob = math.sin(t * 9) * 4 * talk
    fn = papa if who == "papa" else bunty
    fn(d, head[0], head[1] + bob, s, talk, blinking(t, 0 if who == "papa" else 1.3), mood, t)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 36, fill=255)
    fr.img.paste(im, (int(x0), int(y0)), m); fr.d = ImageDraw.Draw(fr.img)
    fr.d.rounded_rectangle(box, 36, outline=OUT, width=7)
    # name pill + call timer
    f = F("black", 34); tw = fr.d.textlength(label, font=f)
    fr.d.rounded_rectangle((x0 + 22, y0 + 20, x0 + 22 + tw + 40, y0 + 72), 26, fill=(255, 255, 255), outline=OUT, width=4)
    fr.text((x0 + 42, y0 + 26), label, f, OUT)
    sec = int(t) + 12; tm = f"{sec // 60:02d}:{sec % 60:02d}"
    fr.d.ellipse((x0 + 22, y1 - 58, x0 + 42, y1 - 38), fill=(235, 40, 40))
    fr.text((x0 + 50, y1 - 66), tm, F("xb", 32), (255, 255, 255), stroke=3, stroke_fill=OUT)

PBOX, BBOX, FULL = (65, 356, 1015, 696), (65, 716, 1015, 1044), (65, 356, 1015, 1044)

def header(fr, t):
    fr.d.rounded_rectangle((65, 286, 545, 340), 27, fill=ORANGE, outline=OUT, width=4)
    fr.text((88, 291), "SHARMA GHAR · AI WALA", F("black", 36), (255, 255, 255))
    fr.d.rounded_rectangle((560, 286, 690, 340), 27, fill=OUT)
    fr.text((582, 291), "EP 5", F("black", 36), (255, 214, 80))

def say_bubble(fr, t, t0, box, txt, font, tail, fill=(255, 255, 255), col=OUT):
    if t < t0: return
    k = eback(prog(t, t0, .28)); x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    b = (cx - (cx - x0) * k, cy - (cy - y0) * k, cx + (x1 - cx) * k, cy + (y1 - cy) * k)
    bubble(fr, b, fill, tail if k > .8 else None)
    if k > .7: fr.text((x0 + 34, y0 + 22), txt, font, col, spacing=6)

def scene(fr, t, R):
    compose(fr, t, R, draw, trans={"turn": "zoom", "haan": "whip", "cta": "iris", "loop": "whip", "*": "whip"},
            same=lambda a, b: GROUP[a] == GROUP[b])

def draw(fr, tag, t, L, R):
    fr.img = BGI.copy(); fr.d = ImageDraw.Draw(fr.img); header(fr, t)
    t0 = L.t0; g = GROUP[tag]
    if g in ("split", "cta", "loop"):
        k = eout(prog(t, .0, .35)) if tag == "hook" else 1
        pm = "star" if tag == "wah" else ("wow" if tag in ("result",) else "calm")
        panel(fr, (PBOX[0] - (1 - k) * 1000, PBOX[1], PBOX[2] - (1 - k) * 1000, PBOX[3]), PROOM, "papa", "PAPA · KANPUR", t, R, mood=pm)
        panel(fr, (BBOX[0] + (1 - k) * 1000, BBOX[1], BBOX[2] + (1 - k) * 1000, BBOX[3]), BROOM, "bunty", "BUNTY · BENGALURU", t, R)
    if tag in ("hook", "loop"):
        say_bubble(fr, t, t0 + .05, (470, 400, 960, 600), "Ye AI kya\nhota hai??", F("black", 74), [(500, 560), (430, 600), (540, 590)])
        if tag == "hook" and t > t0 + 1.0:
            say_bubble(fr, t, t0 + 1.0, (470, 770, 900, 880), "Haan Papa?", F("black", 56), [(500, 850), (430, 880), (540, 870)])
    elif tag == "mic":
        cx, cy = 760, 520; k = pop_scale(t, t0 + .2)
        for i in range(3):
            rr_ = 70 + ((t * 90 + i * 45) % 135); a = max(0, 1 - (rr_ - 70) / 135)
            fr.d.ellipse((cx - rr_, cy - rr_, cx + rr_, cy + rr_), outline=(int(255 - 80 * a), int(122 + 60 * (1 - a)), 40), width=6)
        r_ = 70 * k
        if r_ > 1:
            circ(fr.d, cx, cy, r_, (235, 50, 60), w=6)
            fr.d.rounded_rectangle((cx - 18 * k, cy - 38 * k, cx + 18 * k, cy + 12 * k), int(18 * k), fill=(255, 255, 255))
            fr.d.arc((cx - 30 * k, cy - 20 * k, cx + 30 * k, cy + 26 * k), 0, 180, fill=(255, 255, 255), width=max(1, int(7 * k)))
            fr.d.line((cx, cy + 26 * k, cx, cy + 40 * k), fill=(255, 255, 255), width=max(1, int(7 * k)))
        say_bubble(fr, t, t0 + .1, (450, 760, 905, 950), "Mic dabao,\nHindi mein bolo!", F("black", 54), [(480, 910), (420, 960), (530, 940)])
    elif tag in ("ask", "result", "wah"):
        msg = "AI ji, Sharma ji ki\nbeti ki shaadi ke liye\n2 line aashirwad"
        k = 1 if tag != "ask" else prog(t, t0 + .3, (L.t1 - t0) * .85)
        box = (440, 384, 990, 640) if tag == "ask" else (440, 384, 990, 560)
        fsz = 46 if tag == "ask" else 36
        shadowed(fr, box, 30, (255, 255, 255), outline=OUT, w=5)
        fr.text((box[0] + 30, box[1] + 22), type_on(msg, k) + ("|" if tag == "ask" and int(t * 3) % 2 else ""), F("xb", fsz), OUT, spacing=6)
        if tag in ("result", "wah"):
            kk = eback(prog(t, t0 + .1, .35)); y = 740 + (1 - kk) * 60
            reply = (250, y, 905, y + 230)
            shadowed(fr, reply, 34, (245, 238, 255), outline=PURPLE, w=6)
            fr.d.rounded_rectangle((reply[0] + 24, reply[1] - 26, reply[0] + 210, reply[1] + 24), 25, fill=PURPLE)
            fr.text((reply[0] + 44, reply[1] - 22), "AI reply", F("black", 34), (255, 255, 255))
            fr.text((reply[0] + 30, reply[1] + 44), "Sada khush raho, saath nibhao,\nhar din ko tyohar banao!", F("xb", 37), (60, 30, 130), spacing=12)
            for i, (sx, sy) in enumerate([(870, y + 20), (320, y + 190), (880, y + 200)]):
                a = .5 + .5 * math.sin(t * 8 + i); rr_ = 14 + 10 * a
                fr.d.polygon([(sx, sy - rr_), (sx + rr_ * .3, sy - rr_ * .3), (sx + rr_, sy), (sx + rr_ * .3, sy + rr_ * .3), (sx, sy + rr_), (sx - rr_ * .3, sy + rr_ * .3), (sx - rr_, sy), (sx - rr_ * .3, sy - rr_ * .3)], fill=(255, 200, 40))
            if tag == "result":
                fr.d.rounded_rectangle((95, 760, 270, 830), 35, fill=OUT); fr.text((118, 768), "2 sec", F("black", 46), (255, 214, 80))
        if tag == "wah":
            k2 = eback(prog(t, t0, .3)); f = HF(int(150 * max(.2, k2)), "bang")
            fr.d.polygon([(650 + 230 * math.cos(a) * (1 if i % 2 else .75), 520 + 120 * math.sin(a) * (1 if i % 2 else .75)) for i, a in enumerate([j * math.pi / 8 for j in range(16)])], fill=(255, 214, 40), outline=OUT)
            fr.text((650, 520), "WAAH!", f, MAROON, anchor="mm", stroke=4, stroke_fill=OUT)
            Confetti(60, 8).draw(fr.d, t, t0)
    elif tag in ("rule1", "rule2"):
        st1 = t0 + .05 if tag == "rule1" else R.T("rule1") + .05
        sticky(fr, t, st1, (95, 380, 700, 690), "1. AI bhi galat ho sakta hai", "Zaroori baat?\nPehle jaanch lo.", (255, 226, 90), -3,
               fonts=(F("black", 44), F("xb", 50)))
        if tag == "rule2":
            sticky(fr, t, t0 + .05, (300, 720, 905, 1030), "2. OTP + bank details", "Kabhi kisi chat\nmein nahi.", (255, 170, 190), 3,
                   fonts=(F("black", 50), F("xb", 50)))
            if t > t0 + .4:   # lock icon
                cx, cy = 800, 900; fr.d.rounded_rectangle((cx - 45, cy - 10, cx + 45, cy + 60), 12, fill=(60, 60, 70), outline=OUT, width=5)
                fr.d.arc((cx - 30, cy - 55, cx + 30, cy + 10), 180, 360, fill=OUT, width=12)
    elif g == "papa":
        z = 1 + .04 * prog(t, t0, 3)
        panel(fr, FULL, PROOM.resize((950, 688)), "papa", "PAPA · KANPUR", t, R, s=1.55 * z, mood="calm", head=(290, 250))
        if tag == "turn":
            say_bubble(fr, t, t0 + .1, (520, 420, 980, 620), "Ab meri bhi\nek baat sun.", F("black", 58), [(540, 580), (470, 630), (590, 610)])
        else:
            kk = eout(prog(t, t0 + .2, .5)); y = 790 + (1 - kk) * 50
            shadowed(fr, (110, y, 900, y + 240), 30, (255, 250, 236), outline=OUT, w=6)
            fr.text((150, y + 24), "AI sab jawab de dega.", F("xb", 50), OUT)
            k2 = prog(t, t0 + (L.t1 - t0) * .45, .8)
            fr.text((150, y + 92), type_on("Par Sunday ko phone…", k2), HF(64, "baloo"), MAROON)
            fr.text((150, y + 162), type_on("tujhe khud karna padega.", prog(t, t0 + (L.t1 - t0) * .7, .6)), HF(58, "baloo"), MAROON)
    elif g == "bunty":
        panel(fr, FULL, BROOM.resize((950, 688)), "bunty", "BUNTY · BENGALURU", t, R, s=1.6, mood="sheepish", head=(300, 300))
        say_bubble(fr, t, t0 + .1, (560, 420, 950, 560), "…Haan Papa.", F("black", 56), [(580, 530), (510, 570), (630, 550)])
    if tag == "cta":
        Confetti(40, 2).draw(fr.d, t, t0)

def build(out):
    R = Reel(NAME, "story", LN.SHARMA, tone="warm", seed=5)
    R.cap_style.update(fg=(255, 255, 255), hi=(255, 196, 60), bg=(30, 20, 22, 230))
    dur = R.build_audio(f"{out}/cache")
    R.nudge = dict(text="Papa ko bhejo", icon="send", at=round(dur * .38, 2), bg=ORANGE, fg=(255, 255, 255))
    R.cta = dict(at=R.T("cta"), icon="send", head="Papa ko bhejo", body="…aur aaj hi\nphone karo.", sub="Sunday wait mat karo.",
                 bg=(255, 255, 255), acc=ORANGE, fg=OUT, until=R.T("loop") - .05)
    stills = sorted([.3, 1.2] + [R.T(x) + .7 for x in ["mic", "ask", "result", "wah", "rule1", "rule2", "turn", "lesson", "haan", "cta", "loop"]]
                    + [R.line("lesson").t1 - .2, R.nudge["at"] + 1.0, dur - .2])
    return R, R.render(scene, out, stills=stills)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/out48"
    R, path = build(out)
    print(path, round(R.dur, 1), "s", "violations:", len(R.violations), R.violations[:15])
