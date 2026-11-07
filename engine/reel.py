"""@kitzz.ai reel engine: voice-timed scenes, burned-in captions, save/send prompts, safe-zone checks, encode + mux.

A reel = a list of Line()s (voice + caption + timing) and a scene function scene(fr, t, R) that draws one frame.
Every text box drawn through Frame.text()/Frame.box() is checked against the Reels safe zone on sampled frames.
"""
import os, sys, math, subprocess, json, numpy as np, soundfile as sf
from dataclasses import dataclass, field
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import audio as A
from style_frames import Frame, F, FM, SAFE, RAIL, W, H

FPS = 30
CAP_BOX = (120, 1060, 920, 1230)        # burned-in caption band

@dataclass
class Line:
    spk: str                    # voice id, e.g. am_michael
    say: str                    # spoken text (Devanagari for Hindi lines)
    cap: str = None             # on-screen caption (defaults to say)
    speed: float = 1.0
    pitch: float = 0.0
    tone: str = None            # warm / bright (defaults to the reel's tone)
    gap: float = 0.35           # silence after the line
    pre: float = 0.0            # silence before the line (a beat before a surprise)
    lang: str = "en-us"
    tag: str = None             # name visuals can hook onto
    who: str = None             # speaker label shown on the caption (story reels)
    drop: bool = False          # music drops out under this line
    sfx: str = None             # sound effect at line start
    t0: float = 0; t1: float = 0

def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eout(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def eback(x, s=1.7):
    x = min(1, max(0, x)) - 1; return max(0.0, x * x * ((s + 1) * x + s) + 1)

class Reel:
    def __init__(self, name, music_style, lines, tone="warm", pitch=0.0, lead=0.25, tail=0.8, seed=0):
        self.name, self.music_style, self.lines, self.tone, self.pitch = name, music_style, lines, tone, pitch
        self.lead, self.tail, self.seed = lead, tail, seed
        self.events = []                       # (t, sfx)
        self.cap_style = dict(fg=(255, 255, 255), hi=(255, 210, 60), bg=(0, 0, 0, 175), font="xb", who_fg=(255, 210, 60))
        self.nudge = None                      # dict(text, icon, at)
        self.cta = None                        # dict(lines, icon, sub)
        self.violations = []

    # ---------- audio ----------
    def build_audio(self, cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        parts, t = [A.silence(self.lead)], self.lead
        vmap = json.loads(os.environ.get("KITZZ_VOICE_MAP", "{}"))   # e.g. {"hf_alpha": "parler:Divya:calm"} re-voices a series
        for i, L in enumerate(self.lines):
            if L.pre: parts.append(A.silence(L.pre)); t += L.pre
            key = f"{cache_dir}/{self.name}_{i:02d}.wav"
            spk = vmap.get(L.spk, L.spk); nat = spk.startswith("parler:")
            # natural voices carry their own pace and pitch: no speed-up or pitch shift on top
            speed, pitch = (1.0, 0.0) if nat else (L.speed, L.pitch + self.pitch)
            meta = json.dumps([spk, L.say, speed, pitch, L.tone or self.tone, L.lang])
            if os.path.exists(key) and open(key + ".json").read() == meta:
                a, _ = sf.read(key, dtype="float32")
            else:
                a = A.say(L.say, spk, speed, L.lang, pitch, L.tone or self.tone)
                sf.write(key, a, A.SR); open(key + ".json", "w").write(meta)
            L.t0, L.t1 = t, t + len(a) / A.SR
            if L.sfx: self.events.append((max(0, t - 0.05), L.sfx))
            parts += [a, A.silence(L.gap)]; t = L.t1 + L.gap
        self.voice = np.concatenate(parts + [A.silence(self.tail)])
        self.dur = len(self.voice) / A.SR
        return self.dur

    def mix(self, out_wav):
        drops = [(L.t0 - .1, L.t1 + .1) for L in self.lines if L.drop]
        bed = A.music(self.music_style, self.dur, seed=self.seed, drop=drops)
        fx = np.zeros(len(self.voice), np.float32)
        for t, k in self.events: A.place(fx, A.sfx(k), t)
        A.mixdown(self.voice, bed, fx, out_wav)

    # ---------- timing helpers ----------
    def line(self, tag):
        for L in self.lines:
            if L.tag == tag: return L
        raise KeyError(tag)
    def T(self, tag): return self.line(tag).t0
    def active(self, t):
        cur = None
        for L in self.lines:
            if L.t0 - 0.05 <= t: cur = L
        return cur
    def speaking(self, t, spk=None):
        for L in self.lines:
            if L.t0 <= t <= L.t1 and (spk is None or L.spk == spk): return L
        return None

    # ---------- overlays ----------
    def wrap(self, text, font, maxw=760, maxchars=24):
        d = ImageDraw.Draw(Image.new("RGB", (8, 8))); words, lines, cur = text.split(), [], ""
        for w_ in words:
            nxt = (cur + " " + w_).strip()
            if cur and (d.textlength(nxt, font=font) > maxw or len(nxt) > maxchars): lines.append(cur); cur = w_
            else: cur = nxt
        if cur: lines.append(cur)
        return lines

    def caption(self, fr, t):
        L = None
        for x in self.lines:
            if x.t0 - 0.08 <= t <= x.t1 + min(x.gap, 0.3): L = x
        if L is None: return
        st = self.cap_style
        font = ImageFont.truetype(st["fontfile"], st.get("size", 56)) if st.get("fontfile") else F(st["font"], 52)
        rows = self.wrap((L.cap or L.say).replace("|", ""), font, maxchars=st.get("maxchars", 24))
        chunks = [rows[i:i + 2] for i in range(0, len(rows), 2)]
        nch = sum(len(" ".join(c)) for c in chunks); p = (t - L.t0) / max(.01, L.t1 - L.t0)
        acc, ci = 0, 0
        for i, c in enumerate(chunks):
            acc += len(" ".join(c))
            if p * nch <= acc or i == len(chunks) - 1: ci = i; break
        chunk = chunks[ci]; before = sum(len(" ".join(c)) for c in chunks[:ci])
        lh = st.get("lh", 64); y0 = 1145 - (len(chunk) * lh) // 2
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        bw = max(od.textlength(r, font=font) for r in chunk) + 70
        if L.who: bw = max(bw, 260)
        od.rounded_rectangle((520 - bw / 2, y0 - 22, 520 + bw / 2, y0 + len(chunk) * lh + 8), 26, fill=st["bg"])
        fr.img.alpha_composite(ov) if fr.img.mode == "RGBA" else fr.img.paste(Image.alpha_composite(fr.img.convert("RGBA"), ov).convert("RGB"))
        fr.d = ImageDraw.Draw(fr.img)
        if L.who:
            fr.text((520 - bw / 2 + 24, y0 - 70), L.who, F("black", 44), st["who_fg"], stroke=5, stroke_fill=st.get("who_stroke", (0, 0, 0)))
        done_chars = (p * nch - before)
        k = 0
        for r_i, row in enumerate(chunk):
            y = y0 + r_i * lh; x = 520 - fr.d.textlength(row, font=font) / 2
            for wd in row.split(" "):
                col = st["hi"] if k <= done_chars < k + len(wd) + 1 else st["fg"]
                fr.text((x, y), wd, font, col); x += fr.d.textlength(wd + " ", font=font); k += len(wd) + 1

    def draw_nudge(self, fr, t):
        """Mid-reel ask: big blinking pill in the band under the burned-in captions (y 1262-1392, x 90-900),
        on screen for ~4.5 s. Kept left of the like/share rail and above Instagram's own caption text."""
        n = self.nudge
        if not n: return
        dur = n.get("dur", 4.5); a = t - n["at"]
        if not 0 <= a <= dur: return
        k_in = eback(min(1, a / .35)); k_out = 1 - ease((a - (dur - .3)) / .3)
        k = max(0, min(k_in, k_out))
        if k <= .02: return
        blink = (int(a / .45) % 2 == 0)                 # blink: alternate full / dimmed every 0.45 s
        x0, y0 = n.get("xy", (90, 1262)); h = 130; maxw = 900 - x0 - 150
        size = 66
        FN = (lambda z: ImageFont.truetype(n["fontfile"], z)) if n.get("fontfile") else (lambda z: F("black", z))
        while size > 44 and fr.d.textlength(n["text"], font=FN(size)) > maxw: size -= 2
        font = FN(size); tw = fr.d.textlength(n["text"], font=font)
        w = tw + 150
        bg = n.get("bg", (255, 255, 255)); fg = n.get("fg", (20, 20, 20))
        if not blink: bg, fg = fg, bg                    # invert colours on the off-beat so it reads as blinking
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        al = int(255 * min(1, k * 1.4))
        od.rounded_rectangle((x0 + 6, y0 + 8, x0 + w + 6, y0 + h + 8), h // 2, fill=(0, 0, 0, int(al * .35)))
        od.rounded_rectangle((x0, y0, x0 + w, y0 + h), h // 2, fill=bg + (al,), outline=fg + (al,), width=5)
        icon(od, n["icon"], x0 + 66, y0 + h / 2, 30, fg + (al,))
        fr.img.paste(Image.alpha_composite(fr.img.convert("RGBA"), ov).convert(fr.img.mode))
        fr.d = ImageDraw.Draw(fr.img)
        if k > .5:
            fr.text((x0 + 116, y0 + h / 2), n["text"], font, fg, anchor="lm")
            fr.boxes[-1] = ("nudge text", fr.boxes[-1][1])
        fr.boxes.append(("nudge (bottom band)", (x0, y0, x0 + w, y0 + h)))

    def draw_cta(self, fr, t):
        c = self.cta
        if not c: return
        a = (t - c["at"])
        if a < 0 or (c.get("until") and t > c["until"]): return
        k = eback(min(1, a / .45))
        x0, y0, x1, y1 = 90, 560, 900, 1000
        dy = (1 - k) * 120
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rounded_rectangle((x0 + 8, y0 + dy + 12, x1 + 8, y1 + dy + 12), 44, fill=(0, 0, 0, 90))
        od.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), 44, fill=c.get("bg", (255, 255, 255)) + (int(255 * min(1, k)),))
        icon(od, c["icon"], x0 + 110, y0 + dy + 120, 52, c.get("acc", (225, 30, 30)) + (255,))
        # arrow nudging toward the share button, stays left of x 920
        wob = math.sin(a * 6) * 10
        ax = 760 + wob; ay = y1 + dy - 80
        od.line((ax - 90, ay, ax, ay), fill=c.get("acc", (225, 30, 30)) + (255,), width=12)
        od.polygon([(ax + 30, ay), (ax - 6, ay - 26), (ax - 6, ay + 26)], fill=c.get("acc", (225, 30, 30)) + (255,))
        fr.img.paste(Image.alpha_composite(fr.img.convert("RGBA"), ov).convert(fr.img.mode)); fr.d = ImageDraw.Draw(fr.img)
        fg = c.get("fg", (15, 15, 15))
        FH = (lambda z: ImageFont.truetype(c["fontfile"], z)) if c.get("fontfile") else (lambda z: F("black", z))
        FB = (lambda z: ImageFont.truetype(c["fontfile"], z)) if c.get("fontfile") else (lambda z: F("xb", z))
        fr.text((x0 + 200, y0 + dy + 85), c["head"], FH(76), c.get("acc", (225, 30, 30)))
        fr.text((x0 + 60, y0 + dy + 210), c["body"], FB(54), fg, spacing=10)
        if c.get("sub"): fr.text((x0 + 60, y1 + dy - 110), c["sub"], FB(44), fg)
        fr.box((x0, y0 + dy, x1 + 8, y1 + dy + 12), "cta card")

    # ---------- render ----------
    def render(self, scene, out_dir, check_every=0.5, stills=()):
        os.makedirs(out_dir, exist_ok=True)
        wav = f"{out_dir}/{self.name}.wav"; self.mix(wav)
        n = int(self.dur * FPS); vid = f"{out_dir}/{self.name}_v.mp4"
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", vid],
                             stdin=subprocess.PIPE)
        sample_t = set(int(round(s * FPS)) for s in np.arange(0, self.dur, check_every))
        still_f = {int(round(s * FPS)): s for s in stills}
        self.sheet = []
        for i in range(n):
            t = i / FPS
            fr = Frame(self.name, Image.new("RGB", (W, H)))
            scene(fr, t, self)
            self.draw_nudge(fr, t); self.draw_cta(fr, t); self.caption(fr, t)
            img = fr.img.convert("RGB")
            if i in sample_t:
                for lab, bb, why in fr.check(): self.violations.append((round(t, 2), lab, [int(v) for v in bb], why))
            if i in still_f: self.sheet.append((still_f[i], img.copy()))
            p.stdin.write(img.tobytes())
        p.stdin.close(); p.wait()
        final = f"{out_dir}/{self.name}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-ar", "48000", "-shortest", "-movflags", "+faststart", final], check=True)
        os.remove(vid)
        self.contact_sheet(f"{out_dir}/{self.name}_contact_safezone.png")
        return final

    def contact_sheet(self, path, cols=6):
        if not self.sheet: return
        tw, th = 270, 480; rows = math.ceil(len(self.sheet) / cols)
        sheet = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 40) + 8), (250, 250, 250)); d = ImageDraw.Draw(sheet)
        for k, (t, im) in enumerate(self.sheet):
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov); red = (230, 40, 40, 85)
            for r in [(0, 0, W, SAFE[1]), (0, SAFE[3], W, H), (0, SAFE[1], SAFE[0], SAFE[3]), (SAFE[2], SAFE[1], W, SAFE[3])]: od.rectangle(r, fill=red)
            od.rectangle(RAIL, fill=(255, 170, 0, 85))
            x = 8 + (k % cols) * (tw + 8); y = 8 + (k // cols) * (th + 40)
            sheet.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB").resize((tw, th)), (x, y))
            d.text((x, y + th + 6), f"{t:.1f}s", font=F("b", 24), fill=(30, 30, 30))
        sheet.save(path)

NUDGE_BAND = (65, 1248, 920, 1440)   # agreed exception: under the burned-in captions, clear of the rail
_orig_check = Frame.check
def _check(self):
    bad = []
    for label, bb, why in _orig_check(self):
        x0, y0, x1, y1 = bb
        if label.startswith("nudge") and x0 >= NUDGE_BAND[0] and y0 >= NUDGE_BAND[1] and x1 <= NUDGE_BAND[2] and y1 <= NUDGE_BAND[3]: continue
        bad.append((label, bb, why))
    return bad
Frame.check = _check

# Frame.box: record a non-text key visual for the safe-zone check
def _box(self, bb, label): self.boxes.append((label, bb))
Frame.box = _box

def icon(d, kind, cx, cy, r, col):
    """Drawn icons (Inter/Hind lack emoji): save (bookmark), send (paper plane), follow (+person), comment (bubble), tag (@)."""
    if kind == "save":
        d.polygon([(cx - r * .7, cy - r), (cx + r * .7, cy - r), (cx + r * .7, cy + r), (cx, cy + r * .45), (cx - r * .7, cy + r)], fill=col)
    elif kind == "send":
        d.polygon([(cx - r, cy - r * .1), (cx + r, cy - r * .9), (cx + r * .25, cy + r), (cx - r * .05, cy + r * .2)], fill=col)
    elif kind == "follow":
        d.ellipse((cx - r * .45, cy - r, cx + r * .45, cy - r * .1), fill=col)
        d.pieslice((cx - r * .8, cy - r * .05, cx + r * .8, cy + r * 1.5), 180, 360, fill=col)
        d.rectangle((cx + r * .75, cy - r * .55, cx + r * 1.0, cy + r * .15), fill=col); d.rectangle((cx + r * .52, cy - r * .32, cx + r * 1.23, cy - r * .08), fill=col)
    elif kind == "comment":
        d.ellipse((cx - r, cy - r * .8, cx + r, cy + r * .7), fill=col); d.polygon([(cx - r * .6, cy + r * .4), (cx - r * .9, cy + r), (cx - r * .1, cy + r * .6)], fill=col)
    elif kind == "heart":
        d.ellipse((cx - r, cy - r * .7, cx, cy + r * .2), fill=col); d.ellipse((cx, cy - r * .7, cx + r, cy + r * .2), fill=col)
        d.polygon([(cx - r * .97, cy - r * .1), (cx + r * .97, cy - r * .1), (cx, cy + r)], fill=col)

def glyph_check(text, font_path):
    """Return characters the font can't draw (shows as tofu)."""
    from fontTools.ttLib import TTFont
    cmap = TTFont(font_path).getBestCmap()
    return sorted({c for c in text if not c.isspace() and ord(c) not in cmap})
