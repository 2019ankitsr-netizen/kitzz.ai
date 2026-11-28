"""Trending Today · Kaam Ki Khabar (Reel B) · Sat 28 Nov 2026 · posts 3:43 PM IST · Kalamkari Ink (Hindi).
"मम्मी, दिसंबर में 7 व्रत! पहला 4 दिसंबर" — the December 2026 vrat calendar (New Delhi, Drik Panchang via HinduTone):
Fri 4 Dec Utpanna Ekadashi (parana 5 Dec) · Sun 6 Dec Ravi Pradosh · Mon 7 Dec Masik Shivratri · Tue 8 Dec Margashirsha Amavasya ·
Sun 20 Dec Mokshada Ekadashi + Gita Jayanti · Mon 21 Dec Soma Pradosh · Sat 26 Dec Akhuratha Sankashti Chaturthi (moonrise).
Purnima left out on purpose (23 vs 24 Dec differs by panchang). Two Ekadashis 16 days apart.
Sources: drikpanchang.com/ekadashis/utpanna (4 Dec) · drikpanchang.com/vrats/pradoshdates.html?year=2026 ·
hindutone.com/festivals/december-2026-vrat-fasting-calendar-ekadashi-pradosh · drikpanchang.com/vrats/sankashti-chaturthi-dates.html
Run inside this folder:  python3 ../tyohar_kit/tts.py parler:Rohit:calm 1.06  ->  python3 ../tyohar_kit/build.py Trending_20261128_B
"""
import sys, math
sys.path.insert(0, '/home/claude/kitzz.ai/engine/episodes/tyohar_kit')
import kit
from kit import *
kit.PAD0, kit.PADE = 0.08, 0.18

LINES = [
    "मम्मी, दिसंबर में, सात व्रत हैं! और पहला, चार दिसंबर को।",
    "चार दिसंबर, शुक्रवार, उत्पन्ना एकादशी। पारण, अगले दिन सुबह।",
    "फिर लगातार तीन दिन। छह को रवि प्रदोष, सात को मासिक शिवरात्रि, और आठ को अमावस्या।",
    "ये लिस्ट, अभी सेव कर लो। पूरे महीने काम आएगी।",
    "बीस दिसंबर, रविवार, मोक्षदा एकादशी। और उसी दिन, गीता जयंती भी।",
    "अगले ही दिन, इक्कीस दिसंबर, सोमवार को, सोम प्रदोष।",
    "और छब्बीस दिसंबर, शनिवार, संकष्टी चतुर्थी। व्रत, चाँद देखकर खुलेगा।",
    "यानी, सात व्रत। और दो एकादशी, सिर्फ़ सोलह दिन के अंतर पर।",
    "समय शहर से बदलता है, तो अपना पंचांग, ज़रूर देखें।",
    "ये रील, मम्मी को भेजो। जो हर महीने पूछती हैं, एकादशी कब है?",
    "क्योंकि दिसंबर में, सात व्रत हैं। और पहला, चार दिसंबर को।",
]
CAPS = [
    ["मम्मी, दिसंबर में 7 व्रत!", "पहला — 4 दिसंबर"],
    ["4 दिसंबर, शुक्रवार", "उत्पन्ना एकादशी", "पारण — अगले दिन सुबह"],
    ["फिर लगातार 3 दिन", "6 — रवि प्रदोष", "7 — मासिक शिवरात्रि", "8 — अमावस्या"],
    ["ये लिस्ट अभी सेव कर लो", "पूरे महीने काम आएगी"],
    ["20 दिसंबर, रविवार", "मोक्षदा एकादशी", "उसी दिन — गीता जयंती"],
    ["अगले ही दिन, 21 दिसंबर", "सोमवार — सोम प्रदोष"],
    ["26 दिसंबर, शनिवार", "संकष्टी चतुर्थी", "व्रत खुलेगा — चाँद देखकर"],
    ["यानी 7 व्रत", "और 2 एकादशी", "सिर्फ़ 16 दिन के अंतर पर"],
    ["समय शहर से बदलता है", "अपना पंचांग ज़रूर देखें"],
    ["ये रील मम्मी को भेजो", "जो हर महीने पूछती हैं", "“एकादशी कब है?”"],
    ["क्योंकि दिसंबर में 7 व्रत", "और पहला — 4 दिसंबर"],
]
BELLS = [1, 4, 7]
SCRATCH = [0.6, 1.0]
VRAT = [4, 6, 7, 8, 20, 21, 26]

# ---- BIG blinking mid-reel save pill (band x 90-900, y 1262-1392) ----
def big_nudge(c, tau, t0, _dur=None, T=0):
    dur = 4.5
    if t0 <= tau < t0 + dur:
        a = clamp((tau - t0) / 0.15) * clamp((t0 + dur - tau) / 0.25)
        bl = 0.75 + 0.25 * (0.5 + 0.5 * math.sin(T * 9))
        chip(c, "सेव करो: दिसंबर के 7 व्रत", 495, 1327, 50, SAF, INK, a * bl,
             scale=(0.9 + 0.1 * back((tau - t0) / 0.3)) * (1 + 0.03 * math.sin(T * 9)), pad=(30, 16))
kit.nudge = big_nudge

def dec_cal(c, k, tau, T, rings=(), t0=0.05, rt=0.5, step=0.18, col=GRN):
    cells = calendar_page(c, k, tau, T, t0, 2026, 12, "दिसंबर 2026")
    for j, n in enumerate(rings):
        x, y = cells[n]; t1 = rt + j * step
        ring(k, x, y - 2, 30, t1, t1 + 0.3, col, 7)
    return cells

def s0(c, k, tau, T):   # HOOK: number + date on screen at 0 s
    headline(c, "मम्मी, दिसंबर में", tau, 0.0, 330, 78, INK)
    if tau > 0.05:
        chip(c, "7 व्रत!", 540, 440, 70, RED, CREAM, clamp((tau - 0.05) / 0.15), scale=0.85 + 0.15 * back((tau - 0.05) / 0.3), pad=(34, 10))
    cells = dec_cal(c, k, tau, T, rings=[4], t0=0.0, rt=0.35)
    a = clamp((tau - 0.45) / 0.15)
    if a > 0: chip(c, "पहला — 4 दिसंबर", 480, 1040, 62, INK, GOLDL, a, scale=0.85 + 0.15 * back((tau - 0.45) / 0.3), pad=(30, 12))

def s1(c, k, tau, T):
    ct = cap_times(1)
    headline(c, "उत्पन्ना एकादशी", tau, 0.0, 330, 84, RED)
    mini_card(c, k, tau, 330, 660, "4", "शुक्रवार", "व्रत", RED, 0.1)
    k.shape(P(('M', 490, 660), ('L', 590, 660)), ct[2][0], ct[2][0] + 0.3, w=8, col=INK)
    k.shape(P(('M', 565, 640), ('L', 595, 660), ('L', 565, 680)), ct[2][0] + 0.25, ct[2][0] + 0.4, w=8, col=INK)
    mini_card(c, k, tau, 750, 660, "5", "सुबह", "पारण", SAF, ct[2][0] + 0.2)
    diya(k, 540, 960, 1.0, 0.3, 0.9, T)

def s2(c, k, tau, T):
    ct = cap_times(2)
    headline(c, "लगातार 3 दिन", tau, 0.0, 330, 84, RED)
    cells = calendar_page(c, k, tau, T, 0.0, 2026, 12, "दिसंबर 2026")
    for j, n in enumerate([6, 7, 8]):
        x, y = cells[n]; t1 = ct[j + 1][0]
        ring(k, x, y - 2, 30, t1, t1 + 0.3, RED, 8)
    trishul(k, 140, 760, 0.7, ct[1][0], ct[1][0] + 0.6)
    crescent(k, 945, 600, 36, ct[3][0], ct[3][0] + 0.5)

def s3(c, k, tau, T):
    headline(c, "सेव कर लो!", tau, 0.0, 330, 92, RED)
    dec_cal(c, k, tau, T, rings=VRAT, t0=0.0, rt=0.25, step=0.15)

def s4(c, k, tau, T):
    ct = cap_times(4)
    headline(c, "मोक्षदा एकादशी", tau, 0.0, 330, 84, RED)
    mini_card(c, k, tau, 215, 680, "20", "रविवार", "एकादशी", GRN, 0.1)
    book(k, 660, 640, ct[2][0], ct[2][0] + 0.8, tau)
    label(c, "+ गीता जयंती", 640, 880, tau, ct[2][0] + 0.3, 50, SAF, INK)
    for m in (150, 930): marigold(k, m, 990, 32, 0.4, 0.9)

def s5(c, k, tau, T):
    headline(c, "अगले ही दिन", tau, 0.0, 330, 84, INK)
    mini_card(c, k, tau, 330, 680, "20", "मोक्षदा", "एकादशी", GRN, 0.05)
    k.shape(P(('M', 490, 680), ('L', 590, 680)), 0.5, 0.8, w=8, col=INK)
    k.shape(P(('M', 565, 660), ('L', 595, 680), ('L', 565, 700)), 0.75, 0.9, w=8, col=INK)
    mini_card(c, k, tau, 750, 680, "21", "सोमवार", "सोम प्रदोष", RED, 0.7)
    crescent(k, 540, 950, 40, 1.0, 1.5)

def s6(c, k, tau, T):
    ct = cap_times(6)
    headline(c, "संकष्टी चतुर्थी", tau, 0.0, 330, 84, RED)
    mini_card(c, k, tau, 330, 680, "26", "शनिवार", "चतुर्थी", SAF, 0.1)
    full_moon(k, 760, 600, 80, ct[2][0], ct[2][0] + 0.6)
    modak_thali(k, 760, 860, 0.9, 0.5, 1.2)
    label(c, "चाँद देखकर", 760, 990, tau, ct[2][0] + 0.2, 46, '#FFF6DA', INK)

def s7(c, k, tau, T):
    ct = cap_times(7)
    headline(c, "यानी…", tau, 0.0, 330, 92, INK)
    a = clamp((tau - 0.1) / 0.2)
    if a > 0:
        draw_text(c, "7", 300, 600, F_Y, 260, RED, alpha=a, scale=0.7 + 0.3 * back((tau - 0.1) / 0.35), stroke=8, sfill=CREAM)
        draw_text(c, "व्रत", 300, 790, F_Y, 80, INK, alpha=a)
    b = clamp((tau - ct[1][0]) / 0.2)
    if b > 0:
        draw_text(c, "2", 720, 600, F_Y, 260, GRN, alpha=b, scale=0.7 + 0.3 * back((tau - ct[1][0]) / 0.35), stroke=8, sfill=CREAM)
        draw_text(c, "एकादशी", 720, 790, F_Y, 72, INK, alpha=b)
    label(c, "4 से 20 दिसंबर = 16 दिन", 520, 920, tau, ct[2][0], 52, SAF, INK)

def s8(c, k, tau, T):
    ct = cap_times(8)
    headline(c, "एक ज़रूरी बात", tau, 0.0, 330, 84, RED)
    diya(k, 540, 700, 1.4, 0.1, 0.8, T)
    label(c, "समय शहर से बदलता है", 520, 900, tau, 0.3, 48, CREAM, INK)
    label(c, "पंचांग / पंडित जी से पूछें", 520, 990, tau, ct[1][0], 48, SAF, INK)

def s9(c, k, tau, T):   # main SEND ask card inside the safe zone (arrow stays left of x 920)
    ct = cap_times(9)
    a = clamp((tau - 0.05) / 0.2)
    if a > 0:
        r = skia.Rect(110, 330, 900, 1010)
        c.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(10, 12), 34, 34), skia.Paint(AntiAlias=True, Color=C(INK, 255 * a)))
        c.drawRRect(skia.RRect.MakeRectXY(r, 34, 34), skia.Paint(AntiAlias=True, Color=C('#FFF6DA', 255 * a)))
        c.drawRRect(skia.RRect.MakeRectXY(r, 34, 34), skia.Paint(AntiAlias=True, Color=C(RED, 255 * a), Style=skia.Paint.kStroke_Style, StrokeWidth=8))
    headline(c, "मम्मी को भेजो", tau, 0.1, 430, 96, RED)
    draw_text(c, "जो हर महीने पूछती हैं", 505, 545, F_HB, 56, INK, alpha=clamp((tau - ct[1][0]) / 0.2))
    draw_text(c, "“एकादशी कब है?”", 505, 620, F_Y, 64, RED, alpha=clamp((tau - ct[2][0]) / 0.2))
    mini_card(c, k, tau, 330, 845, "4", "पहला", "व्रत", RED, 0.3)
    mini_card(c, k, tau, 640, 845, "20", "दूसरी", "एकादशी", GRN, 0.45)
    k.shape(P(('M', 790, 960), ('Q', 860, 930, 885, 870)), 0.6, 1.0, w=9, col=RED)
    k.shape(P(('M', 855, 862), ('L', 889, 866), ('L', 883, 900)), 0.95, 1.1, w=9, col=RED)

def s10(c, k, tau, T):
    headline(c, "दिसंबर में 7 व्रत", tau, 0.0, 330, 84, INK)
    dec_cal(c, k, tau, T, rings=VRAT, t0=0.0, rt=0.2, step=0.12)
    a = clamp((tau - 0.9) / 0.2)
    if a > 0: chip(c, "पहला — 4 दिसंबर", 480, 1040, 62, INK, GOLDL, a, scale=0.85 + 0.15 * back((tau - 0.9) / 0.3), pad=(30, 12))

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

if __name__ == '__main__':
    kit.init('durs.json', CAPS, SCENES, nudge_frac=None)
    kit.NUDGE_AT = kit.START[3]
    kit.main()
