"""S2 AI Ki Kahani · Ep 02 · Galat jawab, pura confidence (hallucination)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pilots"))
from s2_kit import L, build, text_card, N, T_, B, F
from reel import eout, ease
INK, RED, MUTE = (60, 35, 25), (200, 40, 40), (150, 110, 90)
LINES = [
    L(N, "आज तारा ने, पूरे भरोसे के साथ, एक गलत जवाब दिया।", "Aaj Tara ne poore bharose ke saath ek galat jawab diya.", tag="hook", sfx="whoosh", gap=.3),
    L(B, "तारा, हमारे शहर में पहली ट्रेन कब आई थी?", "Tara, hamare shehar mein pehli train kab aayi thi?", who="BABLU", tag="q", sfx="pop"),
    L(T_, "अठारह सौ बावन में! एक सौ बीस डिब्बों के साथ!", "1852 mein! 120 dibbon ke saath!", who="TARA", tag="ans", pitch=.5, sfx="chime"),
    L(N, "ना ऐसी कोई तारीख थी। ना एक सौ बीस डिब्बे। तारा ने बना दिया।", "Na aisi koi taareekh thi, na 120 dibbe. Tara ne bana diya.", speed=.95, tag="fake", drop=True),
    L(B, "तुमने झूठ बोला?", "Tumne jhooth bola?", who="BABLU", tag="b2"),
    L(T_, "झूठ नहीं। जो सबसे सही लगा, वो बोल दिया।", "Jhooth nahi. Jo sabse sahi laga, woh bol diya.", who="TARA", tag="t2"),
    L(N, "इसे कहते हैं हैलुसिनेशन। जब ए आई के पास सही जानकारी नहीं होती, तब भी वो पूरे भरोसे से अंदाज़ा बोल देता है।",
      "Ise kehte hain hallucination: sahi jaankari na ho, tab bhi AI poore bharose se andaaza bol deta hai.", speed=.95, tag="halluc"),
    L(B, "तो मैं क्या करूँ?", "Toh main kya karoon?", who="BABLU", tag="b3"),
    L(T_, "मुझसे सोर्स पूछो। और ज़रूरी बात, खुद चेक करो।", "Mujhse source poocho. Aur zaroori baat: khud check karo.", who="TARA", pitch=.5, tag="tip", sfx="pop"),
    L(N, "बबलू ने सीख लिया। पर अगले दिन, तारा उसका नाम ही भूल गई।", "Bablu ne seekh liya. Par agle din, Tara uska naam hi bhool gayi.", pre=.4, speed=.93, pitch=-1, tag="cliff", drop=True),
    L(N, "भाग तीन, कल। फ़ॉलो करो, और उस दोस्त को टैग करो, जो ए आई की हर बात मान लेता है।",
      "Part 3 kal. Follow karo, aur us dost ko tag karo jo AI ki har baat maan leta hai.", tag="cta", sfx="pop", gap=.2),
]
def cards(fr, t, R):
    T = R.T
    if T("q") - .1 <= t < T("b3"):
        text_card(fr, t, T("q"), T("b3"), [("Pehli train kab aayi?", 60, INK, "black", T("q")),
                                           ("1852! 120 dibbe!", 72, (200, 80, 40), "black", T("ans") + .2)])
        if t >= T("fake") + .6:
            k = ease((t - T("fake") - .6) / .5); d = fr.d
            d.line((125, 488, 125 + 590 * k, 470), fill=RED, width=9)
            if t >= T("halluc"): fr.text((130, 560), "= HALLUCINATION", F("black", 52), RED)
            elif t >= T("fake") + 1.2: fr.text((130, 560), "Banaya hua. Koi source nahi.", F("xb", 48), RED)
    text_card(fr, t, T("tip"), T("cliff"), [("Tara se poochho:", 56, INK, "black", T("tip")),
                                             ("1. Source kya hai?", 56, (200, 80, 40), "xb", T("tip") + .3),
                                             ("2. Khud check karo.", 56, (200, 80, 40), "xb", T("tip") + 1.4)])
    text_card(fr, t, R.line("cliff").t0 + 1.2, T("cta"), [("Agle din...", 56, (120, 30, 30), "xb", R.line("cliff").t0 + 1.2),
                                                          ("\"Aap kaun?\"", 80, RED, "black", R.line("cliff").t0 + 2.2)],
              box=(90, 340, 990, 580), fill=(255, 235, 230))
if __name__ == "__main__":
    R, p = build("S2_AIKiKahani_ep02_GalatJawab", 2, "Galat jawab,\npura confidence", LINES, cards, "cliff", sys.argv[1], alarm=True)
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
