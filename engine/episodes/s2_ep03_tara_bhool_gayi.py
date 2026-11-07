"""S2 AI Ki Kahani · Ep 03 · Tara bhool gayi (context window)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from s2_kit import L, build, text_card, N, T_, B, F
from s2_tara import card
from reel import eout, ease, eback
INK, RED = (60, 35, 25), (200, 40, 40)
LINES = [
    L(N, "आज तारा, बबलू का नाम ही भूल गई।", "Aaj Tara, Bablu ka naam hi bhool gayi.", tag="hook", sfx="whoosh", gap=.3),
    L(T_, "नमस्ते! आप कौन?", "Namaste! Aap kaun?", who="TARA", tag="who", sfx="chime"),
    L(B, "मैं बबलू! कल ही तो बताया था!", "Main Bablu! Kal hi toh bataya tha!", who="BABLU", tag="b1"),
    L(N, "तारा की याद, एक खिड़की जैसी है। उसमें बस उतना ही आता है, जितना इस बातचीत में लिखा है।",
      "Tara ki yaad ek khidki jaisi hai: usmein bas utna hi aata hai jitna is baatcheet mein likha hai.", speed=.95, tag="window", drop=True),
    L(N, "इसे कहते हैं कॉन्टेक्स्ट विंडो। नई बातचीत, नई खिड़की।", "Ise kehte hain context window. Nayi baatcheet, nayi khidki.", tag="ctx"),
    L(B, "और अगर बातचीत बहुत लंबी हो जाए?", "Aur agar baatcheet bahut lambi ho jaaye?", who="BABLU", tag="b2"),
    L(T_, "तो सबसे पुरानी बातें, खिड़की से बाहर गिरने लगती हैं।", "Toh sabse purani baatein khidki se bahar girne lagti hain.", who="TARA", tag="fall", sfx="whoosh"),
    L(T_, "इसलिए ज़रूरी बातें, हर नई बातचीत में, फिर से बता दो।", "Isliye zaroori baatein har nayi baatcheet mein phir se bata do.", who="TARA", pitch=.5, tag="tip", sfx="pop"),
    L(B, "ठीक है। मैं बबलू। मुझे चाय पसंद है। और तुम मेरी दोस्त हो।", "Theek hai. Main Bablu. Mujhe chai pasand hai. Aur tum meri dost ho.", who="BABLU", tag="b3"),
    L(T_, "याद आ गया! चाय के साथ... बिस्कुट!", "Yaad aa gaya! Chai ke saath... biscuit!", who="TARA", pitch=.5, tag="t3", sfx="pop"),
    L(N, "पर उसी शाम, बबलू ने तारा से एक लाइन में ऐसा सवाल पूछा, कि जवाब सुनकर सब हैरान रह गए।",
      "Par usi shaam, Bablu ne Tara se ek line mein aisa sawaal poocha ki jawab sunkar sab hairaan reh gaye.", pre=.4, speed=.93, pitch=-1, tag="cliff", drop=True),
    L(N, "भाग चार, जल्द। फ़ॉलो करो, ताकि आप तारा की तरह भूलें नहीं।", "Part 4 jald. Follow karo, taaki aap Tara ki tarah bhoolein nahi.", tag="cta", sfx="pop", gap=.2),
]
MSGS = ["Main Bablu hoon", "Chai pasand hai", "Kal exam hai", "Biscuit wala joke", "Train ka sawaal", "Naya sawaal..."]
def cards(fr, t, R):
    T = R.T
    w0, w1 = T("window"), T("tip")
    if w0 - .1 <= t < w1:
        y = card(fr, (90, 340, 990, 632), eback((t - w0) / .5))
        if y is not None and y < 360:
            d = fr.d
            d.rectangle((380, 360, 960, 612), outline=(60, 35, 25), width=6)     # the "window"
            fr.text((130, 380), "CONTEXT", F("black", 44), (200, 80, 40)); fr.text((130, 430), "WINDOW", F("black", 44), (200, 80, 40))
            fall = R.line("fall"); n_in = 3 + (min(3, int((t - fall.t0) / .8)) if t >= fall.t0 else 0)
            visible = MSGS[max(0, n_in - 3):n_in]
            for i, m in enumerate(visible):
                fr.text((405, 378 + i * 76), m, F("xb", 50), (60, 35, 25))
            if t >= fall.t0 and n_in > 3:
                old = MSGS[n_in - 4]; k = ((t - fall.t0) % .8) / .8
                fr.text((130, 520 + 60 * k), old, F("xb", 44), (190, 150, 120))
    text_card(fr, t, T("tip"), T("t3") + 1.6, [("Har nayi chat mein:", 56, INK, "black", T("tip")),
                                                ("zaroori baatein", 64, (200, 80, 40), "black", T("tip") + .4),
                                                ("phir se batao.", 64, (200, 80, 40), "black", T("tip") + .8)])
    c = R.line("cliff")
    text_card(fr, t, c.t0 + 1.2, T("cta"), [("Ek line ka sawaal...", 60, (120, 30, 30), "black", c.t0 + 1.2),
                                            ("aur sab hairaan.", 60, RED, "black", c.t0 + 2.6)], box=(90, 340, 990, 560), fill=(255, 235, 230))
if __name__ == "__main__":
    R, p = build("S2_AIKiKahani_ep03_TaraBhoolGayi", 3, "Tara bhool\ngayi", LINES, cards, "cliff", sys.argv[1],
                 cta_head="Part 4 jald", cta_body="Follow karo, taaki\naap Tara ki tarah\nbhoolein nahi.")
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
