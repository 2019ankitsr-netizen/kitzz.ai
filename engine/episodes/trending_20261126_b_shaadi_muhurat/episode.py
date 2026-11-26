"""Trending Today · Kaam Ki Khabar (Reel B) · Thu 26 Nov 2026 · posts 3:43 PM IST · Kalamkari Ink (Hindi).
"शादी की तारीख़? 16 दिसंबर से खरमास" — Kharmas (Sun enters Dhanu) Wed 16 Dec 2026 ~10:20-10:29 AM IST -> Makar Sankranti
transit 14 Jan 2027 (festival 15 Jan). December 2026 vivah muhurat (New Delhi panchang, swarnsiddhi 25 Nov / starstell 24 Nov /
HinduTone-Drik): 2, 3, 4, 5, 6, 11, 12 Dec = 7 dates; last = 12 Dec (vedaz lists 13 Dec - minority). First after Kharmas: 15 Jan 2027.
Sources: divinehindu.in/blogs/news/kharmas-2026-27-dates-dos-donts · swarnsiddhi.com/vivah-muhurat/2026/december ·
starstell.com/blog/sun-in-sagittarius-2026-why-are-vivah-muhurats-restricted · sahitavivahamatching.com/kharmas-2026-no-vivah-muhurat
Run inside this folder:  python3 ../tyohar_kit/tts.py parler:Rohit:calm 1.06  ->  python3 ../tyohar_kit/build.py Trending_20261126_B
"""
import sys, math
sys.path.insert(0, '/home/claude/kitzz.ai/engine/episodes/tyohar_kit')
import kit
from kit import *
kit.PAD0, kit.PADE = 0.08, 0.18

LINES = [
    "शादी की तारीख़ ढूँढ रहे हो? सोलह दिसंबर से, एक महीने तक, शादी का कोई मुहूर्त नहीं!",
    "क्यों? सोलह दिसंबर को, सूर्य, धनु राशि में जाएंगे। इसे कहते हैं, खरमास।",
    "मान्यता है, खरमास में, शादी, गृह प्रवेश, और मुंडन जैसे, शुभ काम नहीं किए जाते।",
    "ये चलेगा, मकर संक्रांति तक। यानी, चौदह जनवरी, दो हज़ार सत्ताईस।",
    "ये तारीख़ें, अभी सेव कर लो। बहुत काम आएंगी।",
    "तो खरमास से पहले, दिसंबर में, बचे हैं सिर्फ़ सात मुहूर्त।",
    "दो, तीन, चार, पाँच, और छह दिसंबर। फिर, ग्यारह, और बारह दिसंबर।",
    "ज़्यादातर पंचांगों में, बारह दिसंबर, इस साल का, आख़िरी शादी मुहूर्त है।",
    "और खरमास के बाद, पहला मुहूर्त, पंद्रह जनवरी को।",
    "ये रील, मम्मी को भेजो, और फ़ैमिली ग्रुप में डाल दो, इससे पहले कि कोई पूछे।",
    "क्योंकि सोलह दिसंबर से, एक महीने तक, शादी का कोई मुहूर्त नहीं।",
]
CAPS = [
    ["शादी की तारीख़ ढूँढ रहे हो?", "16 दिसंबर से", "1 महीना — कोई मुहूर्त नहीं!"],
    ["क्यों? 16 दिसंबर को", "सूर्य धनु राशि में", "इसे कहते हैं — खरमास"],
    ["मान्यता है, खरमास में", "शादी, गृह प्रवेश, मुंडन", "जैसे शुभ काम नहीं होते"],
    ["ये चलेगा मकर संक्रांति तक", "यानी 14 जनवरी 2027"],
    ["ये तारीख़ें अभी सेव कर लो", "बहुत काम आएंगी"],
    ["तो खरमास से पहले, दिसंबर में", "बचे हैं सिर्फ़ 7 मुहूर्त"],
    ["2, 3, 4, 5 और 6 दिसंबर", "फिर 11 और 12 दिसंबर"],
    ["ज़्यादातर पंचांगों में", "12 दिसंबर — इस साल का", "आख़िरी शादी मुहूर्त"],
    ["और खरमास के बाद", "पहला मुहूर्त — 15 जनवरी"],
    ["ये रील मम्मी को भेजो", "फ़ैमिली ग्रुप में डाल दो", "इससे पहले कि कोई पूछे"],
    ["क्योंकि 16 दिसंबर से", "1 महीना — कोई मुहूर्त नहीं"],
]
BELLS = [1, 7, 8]
SCRATCH = [0.6, 1.0]
MUH = [2, 3, 4, 5, 6, 11, 12]

# ---- BIG blinking mid-reel pill (band x 90-900, y 1262-1392) instead of the kit's soft chip ----
def big_nudge(c, tau, t0, _dur=None, T=0):
    dur = 4.5
    if t0 <= tau < t0 + dur:
        a = clamp((tau - t0) / 0.15) * clamp((t0 + dur - tau) / 0.25)
        bl = 0.75 + 0.25 * (0.5 + 0.5 * math.sin(T * 9))
        chip(c, "सेव करो: 7 मुहूर्त · 12 दिसंबर", 495, 1327, 50, SAF, INK, a * bl,
             scale=(0.9 + 0.1 * back((tau - t0) / 0.3)) * (1 + 0.03 * math.sin(T * 9)), pad=(30, 16))
kit.nudge = big_nudge

def ann(i): return kit.START[i]

def dec_cal(c, k, tau, T, rings=(), cross16=False, t0=0.05):
    cells = calendar_page(c, k, tau, T, t0, 2026, 12, "दिसंबर 2026")
    for j, n in enumerate(rings):
        x, y = cells[n]; t1 = 0.5 + j * 0.18
        ring(k, x, y - 2, 30, t1, t1 + 0.3, GRN, 6)
    if cross16:
        x, y = cells[16]; ring(k, x, y - 2, 32, 0.6, 0.95, RED, 8)
        a = clamp((tau - 0.9) / 0.2)
        if a > 0: glow(c, x, y, 38, RED, 0.25 * a)
    return cells

def s0(c, k, tau, T):   # HOOK: date on screen at 0 s
    headline(c, "शादी की तारीख़?", tau, 0.0, 320, 86, INK)
    if tau > 0.05:
        chip(c, "16 दिसंबर से — 1 महीना", 540, 430, 54, RED, CREAM, clamp((tau - 0.05) / 0.15), scale=0.9 + 0.1 * back((tau - 0.05) / 0.3), pad=(30, 12))
    dec_cal(c, k, tau, T, cross16=True)
    a = clamp((tau - 0.45) / 0.15)
    if a > 0: chip(c, "कोई मुहूर्त नहीं!", 480, 1035, 64, INK, GOLDL, a, scale=0.85 + 0.15 * back((tau - 0.45) / 0.3), pad=(30, 12))

def s1(c, k, tau, T):
    ct = cap_times(1)
    headline(c, "क्यों?", tau, 0.0, 330, 96, RED)
    sun(k, 540, 680, 130, 0.1, 0.9, T)
    # simple bow + arrow (Dhanu = archer's bow) drawn in ink
    bow = P(('M', 700, 860), ('Q', 860, 940, 700, 1020))
    k.shape(bow, ct[1][0], ct[1][0] + 0.5, w=9, col=RED)
    k.shape(P(('M', 700, 860), ('L', 700, 1020)), ct[1][0] + 0.3, ct[1][0] + 0.6, w=3, col=INK)
    k.shape(P(('M', 620, 940), ('L', 830, 940)), ct[1][0] + 0.5, ct[1][0] + 0.8, w=5, col=INK)
    label(c, "सूर्य: धनु राशि में", 330, 900, tau, ct[1][0], 46, '#FFF6DA', RED)
    label(c, "= खरमास", 330, 985, tau, ct[2][0], 60, SAF, INK)

def s2(c, k, tau, T):
    ct = cap_times(2)
    headline(c, "खरमास में…", tau, 0.0, 330, 88, RED)
    mandap(k, 0.1, 1.2, T)
    for j, (txt, y) in enumerate([("शादी", 820), ("गृह प्रवेश", 900), ("मुंडन", 980)]):
        label(c, txt + " — नहीं", 300, y, tau, ct[1][0] + j * 0.35, 48, CREAM, RED)

def s3(c, k, tau, T):
    headline(c, "कब तक?", tau, 0.0, 330, 92, RED)
    mini_card(c, k, tau, 300, 640, "16", "खरमास", "शुरू", RED, 0.1, hdr="दिसंबर")
    k.shape(P(('M', 420, 640), ('L', 650, 640)), 0.5, 0.9, w=8, col=INK)
    k.shape(P(('M', 625, 620), ('L', 655, 640), ('L', 625, 660)), 0.85, 1.0, w=8, col=INK)
    mini_card(c, k, tau, 780, 640, "14", "मकर", "संक्रांति", SAF, 0.6, hdr="जनवरी")
    label(c, "करीब 30 दिन", 520, 900, tau, 1.2, 56, '#FFF6DA', RED)

def s4(c, k, tau, T):
    headline(c, "सेव कर लो!", tau, 0.0, 330, 92, RED)
    dec_cal(c, k, tau, T, rings=MUH, cross16=True, t0=0.0)

def s5(c, k, tau, T):
    headline(c, "दिसंबर में बचे", tau, 0.0, 320, 80, INK)
    for m in (150, 920): marigold(k, m, 560, 34, 0.2, 0.7)
    a = clamp((tau - 0.3) / 0.2)
    if a > 0:
        draw_text(c, "7", 540, 640, F_Y, 300, RED, alpha=a, scale=0.7 + 0.3 * back((tau - 0.3) / 0.35), stroke=8, sfill=CREAM)
    label(c, "शादी मुहूर्त", 540, 860, tau, 0.6, 64, SAF, INK)
    garland(k, 150, 980, 930, 980, 60, 0.5, 1.4)

def s6(c, k, tau, T):
    ct = cap_times(6)
    headline(c, "ये हैं तारीख़ें", tau, 0.0, 320, 80, RED)
    cells = calendar_page(c, k, tau, T, 0.0, 2026, 12, "दिसंबर 2026")
    span = max(0.6, ct[0][1] - ct[0][0])
    for j, n in enumerate(MUH):
        t1 = ct[0][0] + j * span / 5 if j < 5 else ct[1][0] + (j - 5) * 0.45
        x, y = cells[n]; ring(k, x, y - 2, 30, t1, t1 + 0.3, GRN, 7)

def s7(c, k, tau, T):
    headline(c, "आख़िरी मुहूर्त", tau, 0.0, 320, 88, RED)
    mini_card(c, k, tau, 540, 660, "12", "शनिवार", "", RED, 0.15, hdr="दिसंबर")
    for m in (250, 830): marigold(k, m, 640, 40, 0.3, 0.8)
    label(c, "ज़्यादातर पंचांग", 540, 930, tau, 0.8, 48, '#FFF6DA', INK)

def s8(c, k, tau, T):
    headline(c, "खरमास के बाद", tau, 0.0, 320, 84, INK)
    sun(k, 820, 560, 80, 0.0, 0.6, T)
    mini_card(c, k, tau, 420, 680, "15", "पहला", "मुहूर्त", GRN, 0.25, hdr="जनवरी")
    kalash(k, 790, 860, 0.9, 0.4, 1.2)
    label(c, "समय शहर से बदलता है", 400, 930, tau, 1.0, 40, CREAM, INK)
    label(c, "पंडित जी से ज़रूर पूछें", 400, 1000, tau, 1.3, 40, SAF, INK)

def s9(c, k, tau, T):
    ct = cap_times(9)
    headline(c, "एक ज़रूरी बात", tau, 0.0, 320, 84, RED)
    diya(k, 540, 700, 1.5, 0.1, 0.8, T)
    label(c, "पंचांग देखें", 540, 520, tau, 0.4, 52, SAF, INK)
    label(c, "समय शहर से बदलता है", 520, 900, tau, 0.4, 46, CREAM, INK)
    label(c, "पंडित जी से पूछें", 520, 990, tau, ct[2][0], 54, SAF, INK)

def s10(c, k, tau, T):   # main SEND ask card inside the safe zone (arrow stays left of x 920)
    ct = cap_times(9)
    bl = 0.82 + 0.18 * (0.5 + 0.5 * math.sin(T * 8))
    a = clamp((tau - 0.05) / 0.2)
    if a > 0:
        r = skia.Rect(110, 330, 900, 1010)
        sh = skia.Paint(AntiAlias=True, Color=C(INK, 255 * a))
        c.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(10, 12), 34, 34), sh)
        c.drawRRect(skia.RRect.MakeRectXY(r, 34, 34), skia.Paint(AntiAlias=True, Color=C('#FFF6DA', 255 * a)))
        st = skia.Paint(AntiAlias=True, Color=C(RED, 255 * a), Style=skia.Paint.kStroke_Style, StrokeWidth=8)
        c.drawRRect(skia.RRect.MakeRectXY(r, 34, 34), st)
    headline(c, "मम्मी को भेजो", tau, 0.1, 430, 96, RED)
    draw_text(c, "फ़ैमिली ग्रुप में डाल दो", 505, 560, F_HB, 58, INK, alpha=clamp((tau - ct[1][0]) / 0.2))
    draw_text(c, "इससे पहले कि कोई पूछे", 505, 640, F_HB, 52, INK, alpha=clamp((tau - ct[2][0]) / 0.2))
    mini_card(c, k, tau, 330, 820, "12", "आख़िरी", "मुहूर्त", RED, 0.3, hdr="दिसंबर")
    mini_card(c, k, tau, 640, 820, "16", "खरमास", "शुरू", SAF, 0.45, hdr="दिसंबर")
    # send arrow toward the share rail, kept left of x 920
    k.shape(P(('M', 760, 960), ('Q', 850, 930, 880, 870)), 0.6, 1.0, w=9, col=RED)
    k.shape(P(('M', 850, 862), ('L', 884, 866), ('L', 878, 900)), 0.95, 1.1, w=9, col=RED)
    _ = bl

def s11(c, k, tau, T):
    headline(c, "16 दिसंबर से…", tau, 0.0, 320, 86, INK)
    dec_cal(c, k, tau, T, cross16=True, t0=0.0)
    a = clamp((tau - 0.6) / 0.2)
    if a > 0: chip(c, "कोई मुहूर्त नहीं!", 480, 1035, 64, INK, GOLDL, a, scale=0.85 + 0.15 * back((tau - 0.6) / 0.3), pad=(30, 12))

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s10, s11]

if __name__ == '__main__':
    kit.init('durs.json', CAPS, SCENES, nudge_frac=None)
    kit.NUDGE_AT = kit.START[4]
    kit.main()
