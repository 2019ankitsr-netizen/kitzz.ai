"""Word-pop captions, Reels-tuned (scout pick, 14 Nov 2026).

Timing numbers only (no code) from the ffmpeg-kinetic-captions skill notes:
  pop-in   50 % -> 118 % over 0-100 ms, settle to 100 % over 100-200 ms   (Reels grow: 120-180 ms at 115-120 %)
  frame-aligned at 30 fps; shake never used (keeps it calm and legible).
Each word appears exactly when it is spoken, in its SPEAKER's colour, then cools to white.
Layout is measured at 100 % so lines never reflow while words pop. Same caption band as reel.py
(y 1060-1230, x 120-920, max 2 lines, ~24 chars a line); every popped word box goes into the safe-zone check.

Usage: R = WordPopReel(...); R.speaker_style = {"am_fenrir": dict(col=(255,200,60), who="DETECTIVE"), ...}
Word times are estimated from the line's audio length by character share (Kokoro gives no word stamps).
"""
from PIL import Image, ImageDraw, ImageFont
from reel import Reel, F, W, H

POP_IN, SETTLE, HOT = .10, .10, .35       # seconds: grow, settle, keep speaker colour
START, PEAK = .50, 1.16
GAP = 10                                 # extra px between words so a popping word never touches its neighbour

def _scale(a):
    if a < 0: return 0
    if a < POP_IN: x = a / POP_IN; return START + (PEAK - START) * (1 - (1 - x) ** 2)
    if a < POP_IN + SETTLE: x = (a - POP_IN) / SETTLE; return PEAK - (PEAK - 1) * x * x * (3 - 2 * x)
    return 1.0

def _mix(c1, c2, k): return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))

class WordPopReel(Reel):
    speaker_style = {}
    def word_times(self, L, words):
        n = sum(len(w) + 1 for w in words); dur = max(.2, L.t1 - L.t0 - .05); out, acc = [], 0
        for w in words:
            out.append(L.t0 + dur * acc / n); acc += len(w) + 1
        return out

    def caption(self, fr, t):
        L = None
        for x in self.lines:
            if x.t0 - 0.08 <= t <= x.t1 + min(x.gap, 0.3): L = x
        if L is None: return
        st = self.cap_style; sp = self.speaker_style.get(L.spk, {})
        col = sp.get("col", st["hi"]); fg = st["fg"]
        font = F(st.get("font", "xb"), st.get("size", 56))
        text = (L.cap or L.say).replace("|", "")
        rows = self.wrap(text, font, maxw=680, maxchars=st.get("maxchars", 22))
        chunks = [rows[i:i + 2] for i in range(0, len(rows), 2)]
        words_all = text.split(); times = self.word_times(L, words_all)
        # which 2-line chunk is live: the one holding the most recently started word
        wi, ci, base = 0, 0, []
        for c_i, c in enumerate(chunks):
            n = sum(len(r.split()) for r in c); base.append(wi); wi += n
        for c_i in range(len(chunks)):
            if times[base[c_i]] - .02 <= t: ci = c_i
        chunk, w0 = chunks[ci], base[ci]
        lh = st.get("lh", 70); y0 = 1150 - (len(chunk) * lh) // 2
        d = fr.d
        bw = max(d.textlength(r, font=font) + GAP * (len(r.split()) - 1) for r in chunk) + 80
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rounded_rectangle((520 - bw / 2, y0 - 26, 520 + bw / 2, y0 + len(chunk) * lh + 6), 28, fill=st["bg"])
        if sp.get("who"):
            od.rounded_rectangle((520 - bw / 2, y0 - 26, 520 - bw / 2 + 14, y0 + len(chunk) * lh + 6), 7, fill=col + (255,))
        fr.img = Image.alpha_composite(fr.img.convert("RGBA"), ov).convert(fr.img.mode); fr.d = d = ImageDraw.Draw(fr.img)
        if sp.get("who"):
            fr.text((520 - bw / 2 + 6, y0 - 84), sp["who"], F("black", 40), col, stroke=5, stroke_fill=(0, 0, 0))
        k = w0
        for r_i, row in enumerate(chunk):
            y = y0 + r_i * lh; x = 520 - (d.textlength(row, font=font) + GAP * (len(row.split()) - 1)) / 2
            for wd in row.split(" "):
                ww = d.textlength(wd, font=font); a = t - times[k]
                s = _scale(a)
                if s > 0:
                    hot = 1 - min(1, max(0, (a - HOT) / .25))
                    c = _mix(fg, col, hot)
                    size = max(8, int(round(st.get("size", 56) * s))); f2 = font if size == st.get("size", 56) else F(st.get("font", "xb"), size)
                    fr.text((x + ww / 2, y + lh * .42), wd, f2, c, anchor="mm", stroke=3, stroke_fill=(0, 0, 0))
                x += d.textlength(wd + " ", font=font) + GAP; k += 1
