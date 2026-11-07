"""Style frames for the 5 @kitzz.ai series (1080x1920), with a safe-zone check on every text box."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
SAFE = (65, 269, 1015, 1248)          # Meta Reels margins: top 14%, bottom 35%, sides 6%
RAIL = (930, 900, 1080, 1700)          # right-side like/comment/share/save buttons
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + {"black": "InterDisplay-Black.otf", "xb": "InterDisplay-ExtraBold.otf",
                                            "b": "Inter-Bold.otf", "sb": "Inter-SemiBold.otf", "m": "Inter-Medium.otf",
                                            "r": "Inter-Regular.otf"}[w], s)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def FM(s): return ImageFont.truetype(MONO, s)

class Frame:
    def __init__(self, name, img):
        self.name, self.img, self.d, self.boxes = name, img, ImageDraw.Draw(img), []
    def text(self, xy, s, font, fill, anchor="la", stroke=0, stroke_fill=None, spacing=8):
        d = self.d
        bb = d.multiline_textbbox(xy, s, font=font, anchor=anchor, spacing=spacing, stroke_width=stroke) if "\n" in s \
            else d.textbbox(xy, s, font=font, anchor=anchor, stroke_width=stroke)
        (d.multiline_text if "\n" in s else d.text)(xy, s, font=font, fill=fill, anchor=anchor, stroke_width=stroke,
                                                    stroke_fill=stroke_fill, **({"spacing": spacing} if "\n" in s else {}))
        self.boxes.append((s.replace("\n", " / ")[:40], bb))
        return bb
    def check(self):
        bad = []
        for label, (x0, y0, x1, y1) in self.boxes:
            out = x0 < SAFE[0] or y0 < SAFE[1] or x1 > SAFE[2] or y1 > SAFE[3]
            rail = x1 > RAIL[0] and y1 > RAIL[1] and y0 < RAIL[3]
            if out or rail: bad.append((label, (x0, y0, x1, y1), "outside safe zone" if out else "under icon rail"))
        return bad

def caption(fr, line1, line2=None, fg=(255, 255, 255), bg=(0, 0, 0, 170)):
    """Burned-in caption band: y 1060-1230, x 120-920, centred, max 2 lines."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle((120, 1080, 920, 1220 if line2 else 1160), 28, fill=bg)
    fr.img.alpha_composite(ov) if fr.img.mode == "RGBA" else fr.img.paste(Image.alpha_composite(fr.img.convert("RGBA"), ov).convert("RGB"))
    fr.d = ImageDraw.Draw(fr.img)
    fr.text((520, 1120), line1, F("b", 50), fg, anchor="mm")
    if line2: fr.text((520, 1180), line2, F("b", 50), fg, anchor="mm")

# ---------------- S1 How Things Work: Isometric X-Ray Cutaway ----------------
def s1():
    img = Image.new("RGB", (W, H), (10, 18, 38)); fr = Frame("S1_how_things_work", img); d = fr.d
    for x in range(-W, 2 * W, 60):                    # isometric grid
        d.line((x, 0, x + H * 0.577, H), fill=(22, 36, 70), width=1); d.line((x, 0, x - H * 0.577, H), fill=(22, 36, 70), width=1)
    cx, cy = 360, 760
    def slab(y, col, edge, label, tag):
        w, h, t = 300, 150, 26
        top = [(cx, y - h), (cx + w, y), (cx, y + h), (cx - w, y)]
        d.polygon([(cx - w, y), (cx, y + h), (cx, y + h + t), (cx - w, y + t)], fill=tuple(int(c * .55) for c in col))
        d.polygon([(cx, y + h), (cx + w, y), (cx + w, y + t), (cx, y + h + t)], fill=tuple(int(c * .75) for c in col))
        d.polygon(top, fill=col, outline=edge); d.line(top + [top[0]], fill=edge, width=3)
        lx = cx + w - 70
        d.line((lx, y - 10, 640, y - 40), fill=(120, 230, 255), width=3); d.ellipse((lx - 7, y - 17, lx + 7, y - 3), fill=(120, 230, 255))
        fr.text((650, y - 96), tag, FM(26), (120, 230, 255))
        fr.text((650, y - 62), label, F("b", 38), (255, 255, 255))
    slab(1010, (40, 70, 130), (90, 160, 255), "Mobile tower", "LAYER 03")
    slab(840, (30, 110, 120), (90, 230, 220), "Bank server", "LAYER 02")
    slab(670, (70, 60, 140), (170, 140, 255), "Your OTP app", "LAYER 01")
    d.rounded_rectangle((cx - 165, 670 - 36, cx + 165, 670 + 36), 16, fill=(255, 210, 60))
    fr.text((cx, 670), "4 8 2 9 1 7", FM(40), (20, 20, 30), anchor="mm")
    fr.text((90, 340), "This 6-digit code\ncrossed India in 3 s.", F("black", 70), (255, 255, 255), spacing=6)
    fr.text((92, 292), "HOW THINGS WORK · 01", FM(28), (255, 210, 60))
    caption(fr, "Here's the route it took,", "in 3 hops.")
    return fr

# ---------------- S2 AI Ki Kahani: Paper Pop-up Storybook ----------------
def s2():
    img = Image.new("RGBA", (W, H), (246, 232, 205, 255)); fr = Frame("S2_ai_ki_kahani", img)
    rnd = random.Random(3)
    def layer(col, pts, sh=14):
        sl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sl)
        sd.polygon([(x + sh, y + sh) for x, y in pts], fill=(60, 40, 20, 90)); sl = sl.filter(ImageFilter.GaussianBlur(8))
        fr.img.alpha_composite(sl); ImageDraw.Draw(fr.img).polygon(pts, fill=col)
    def hill(y0, amp, col, seed):
        r = random.Random(seed); pts = [(0, H)] + [(x, y0 - amp * math.sin(x / 170 + seed) - r.randint(0, 18)) for x in range(0, W + 41, 40)] + [(W, H)]
        layer(col, pts)
    hill(1150, 60, (233, 160, 90, 255), 1); hill(1250, 50, (205, 110, 70, 255), 2); hill(1360, 40, (150, 80, 60, 255), 3)
    layer((252, 200, 80, 255), [(780 + 90 * math.cos(a / 20 * math.pi), 470 + 90 * math.sin(a / 20 * math.pi)) for a in range(40)])
    layer((255, 250, 240, 255), [(230, 860), (230, 1010), (420, 1010), (420, 860), (325, 780)])   # house
    layer((140, 70, 60, 255), [(300, 1010), (300, 930), (350, 930), (350, 1010)])
    # Tara: a phone with a face
    layer((40, 45, 70, 255), [(560, 720), (760, 720), (760, 1060), (560, 1060)])
    d = ImageDraw.Draw(fr.img); fr.d = d
    d.rounded_rectangle((575, 740, 745, 1040), 22, fill=(120, 220, 230))
    d.ellipse((610, 840, 640, 870), fill=(30, 30, 50)); d.ellipse((680, 840, 710, 870), fill=(30, 30, 50))
    d.arc((620, 870, 700, 930), 20, 160, fill=(30, 30, 50), width=8)
    fr.text((90, 300), "EPISODE 1", FM(30), (180, 70, 50))
    fr.text((90, 345), "Tara ka\npehla din", F("black", 96), (60, 35, 25), spacing=0)
    fr.text((90, 585), "AI KI KAHANI", F("xb", 34), (180, 70, 50))
    caption(fr.__class__ and fr, "Bablu ke phone mein", "ek nayi awaaz aayi...", fg=(255, 245, 230), bg=(60, 35, 25, 200))
    fr.img = fr.img.convert("RGB"); return fr

# ---------------- S3 CCTV Riddles: CCTV Case File ----------------
def s3():
    rnd = random.Random(7)
    img = Image.new("RGB", (W, H), (30, 32, 30)); d = ImageDraw.Draw(img)
    # dhaba counter scene, top-down CCTV perspective
    d.polygon([(120, 1250), (960, 1250), (800, 700), (280, 700)], fill=(70, 72, 66))
    d.rectangle((300, 560, 780, 700), fill=(52, 54, 50)); d.rectangle((420, 600, 660, 690), fill=(90, 92, 85))
    for i, x in enumerate((330, 520, 710)):
        d.ellipse((x - 45, 820, x + 45, 910), fill=(110, 112, 104)); d.rectangle((x - 60, 900, x + 60, 1060), fill=(95, 97, 90))
    d.rectangle((470, 640, 610, 680), fill=(140, 140, 120))            # cash box
    noise = Image.effect_noise((W, H), 38).convert("RGB"); img = Image.blend(img, noise, 0.18)
    img = img.filter(ImageFilter.GaussianBlur(1.2)); fr = Frame("S3_cctv_riddle", img); d = fr.d
    for y in range(0, H, 6): d.line((0, y, W, y), fill=(0, 0, 0), width=1)
    d.rectangle((70, 280, 1010, 1240), outline=(200, 205, 195), width=3)
    d.ellipse((100, 310, 132, 342), fill=(230, 40, 40)); fr.text((145, 309), "REC", FM(34), (235, 235, 225))
    fr.text((995, 309), "CAM 03", FM(34), (235, 235, 225), anchor="ra")
    fr.text((100, 360), "07-11-2026  21:14:22", FM(32), (235, 235, 225))
    # case file tag + red string
    d.line((520, 660, 820, 470), fill=(220, 40, 40), width=5); d.ellipse((508, 648, 532, 672), fill=(220, 40, 40))
    d.rectangle((640, 400, 960, 540), fill=(240, 228, 190)); d.rectangle((640, 400, 960, 430), fill=(200, 60, 50))
    fr.text((655, 403), "EVIDENCE #1", FM(24), (255, 245, 230))
    fr.text((655, 450), "₹30 paid\n₹25 bill\n₹5 back?", FM(28), (40, 30, 20), spacing=2)
    fr.text((540, 980), "CASE #01", FM(36), (255, 220, 80), anchor="mm")
    caption(fr, "3 friends paid ₹30.", "So where did ₹1 go?")
    return fr

# ---------------- S4 Hook Shots: Swiss Kinetic Type ----------------
def s4():
    img = Image.new("RGB", (W, H), (244, 242, 236)); fr = Frame("S4_hook_shots", img); d = fr.d
    for x in range(65, 1016, 95): d.line((x, 0, x, H), fill=(226, 222, 214), width=2)
    d.rectangle((65, 290, 540, 330), fill=(225, 30, 30))
    fr.text((80, 293), "HOOK SHOT 02", F("xb", 30), (255, 255, 255))
    fr.text((70, 360), "₹99", F("black", 330), (15, 15, 15))
    fr.text((80, 760), "not ₹100.", F("black", 110), (225, 30, 30))
    fr.text((80, 905), "Your brain\nfell for it.", F("xb", 64), (15, 15, 15), spacing=4)
    d.line((80, 1060, 470, 1060), fill=(15, 15, 15), width=8)
    caption(fr, "The left digit decides", "before you even read.", fg=(255, 255, 255), bg=(15, 15, 15, 230))
    return fr

# ---------------- S5 Space Transit: Cosmic Metro HUD ----------------
def s5():
    img = Image.new("RGB", (W, H), (4, 6, 14)); d = ImageDraw.Draw(img); rnd = random.Random(11)
    for _ in range(900):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.choice([1, 1, 1, 2]); c = rnd.randint(140, 255)
        d.ellipse((x, y, x + r, y + r), fill=(c, c, min(255, c + 20)))
    # Saturn
    pl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pl)
    pd.ellipse((330, 640, 750, 1060), fill=(222, 190, 130, 255))
    for i in range(6): pd.ellipse((330, 700 + i * 55, 750, 740 + i * 55), outline=(200, 160, 100, 120), width=10)
    rings = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(rings)
    for i, a in enumerate((255, 200, 150)): rd.ellipse((150 - i * 30, 790 - i * 8, 930 + i * 30, 910 + i * 8), outline=(230, 210, 170, a), width=14 - i * 3)
    img = Image.alpha_composite(img.convert("RGBA"), pl.filter(ImageFilter.GaussianBlur(1)))
    img = Image.alpha_composite(img, rings).convert("RGB")
    fr = Frame("S5_space_transit", img); d = fr.d
    # metro window frame
    d.rounded_rectangle((40, 250, 1040, 1270), 90, outline=(70, 78, 92), width=40)
    # LED "next stop" board
    d.rounded_rectangle((90, 300, 990, 470), 20, fill=(20, 12, 4), outline=(90, 60, 20), width=4)
    for x in range(100, 980, 12):
        for y in range(310, 462, 12): d.point((x, y), fill=(45, 28, 8))
    fr.text((540, 345), "NEXT STOP", FM(36), (255, 170, 40), anchor="mm")
    fr.text((540, 415), "SATURN'S RINGS", FM(62), (255, 190, 60), anchor="mm")
    fr.text((100, 500), "STOP 01 / 13   FACT", FM(28), (120, 220, 255))
    fr.text((975, 500), "1.2 BILLION km", FM(28), (120, 220, 255), anchor="ra")
    caption(fr, "These rings are wider than", "8 Earths. And this thin.")
    return fr

if __name__ == "__main__":
    import os, sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True); report = []
    frames = [s1(), s2(), s3(), s4(), s5()]
    for fr in frames:
        fr.img.convert("RGB").save(f"{out}/{fr.name}.png")
        bad = fr.check(); report.append((fr.name, bad))
    # contact sheet with safe-zone overlay
    tw, th = 360, 640; sheet = Image.new("RGB", (tw * 5 + 60, th + 20), (255, 255, 255))
    for i, fr in enumerate(frames):
        im = fr.img.convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        red = (230, 40, 40, 90)
        for r in [(0, 0, W, SAFE[1]), (0, SAFE[3], W, H), (0, SAFE[1], SAFE[0], SAFE[3]), (SAFE[2], SAFE[1], W, SAFE[3])]: od.rectangle(r, fill=red)
        od.rectangle(RAIL, fill=(255, 170, 0, 90))
        sheet.paste(Image.alpha_composite(im, ov).convert("RGB").resize((tw, th)), (10 + i * (tw + 10), 10))
    sheet.save(f"{out}/contact_sheet_safezone.png")
    for name, bad in report: print(name, "OK" if not bad else bad)
