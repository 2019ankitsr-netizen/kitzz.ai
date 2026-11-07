"""Diwali Did You Know · 03 · Bandi Chhor Divas (Sikh Day of Liberation, same day as Diwali). Abstract visuals only."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from dyk_kit import *
LINES = [
    HL(V, "क्या आप जानते हैं? दिवाली के दिन, सिख बंदी छोड़ दिवस मनाते हैं।", tag="hook", sfx="whoosh", gap=.3),
    HL(V, "बंदी छोड़ दिवस, यानी मुक्ति का दिन।", tag="l1", sfx="tick"),
    HL(V, "सन सोलह सौ उन्नीस। ग्वालियर के किले में, छठे गुरु, गुरु हरगोबिंद साहिब जी, और बावन राजा क़ैद थे।",
       "सन 1619. ग्वालियर के किले में छठे गुरु, गुरु हरगोबिंद साहिब जी, और 52 राजा क़ैद थे।", speed=.96, tag="l2", sfx="tick"),
    HL(V, "रिहाई मिली, तो गुरु जी अकेले नहीं निकले।", pre=.3, pitch=.5, tag="l3", drop=True),
    HL(V, "परंपरा के अनुसार, उन्होंने बावन कलियों वाला चोला पहना। हर राजा ने एक कली पकड़ी, और सब साथ बाहर आए।",
       "परंपरा के अनुसार उन्होंने 52 कलियों वाला चोला पहना। हर राजा ने एक कली पकड़ी, और सब साथ बाहर आए।", tag="l4", sfx="pop"),
    HL(V, "वो अमृतसर पहुँचे, तो हरमंदिर साहिब दीयों से जगमगा उठा।", tag="l5", sfx="chime"),
    HL(V, "ये रील उस दोस्त को भेजो, जो ये कहानी नहीं जानता।", tag="cta", sfx="pop", gap=.3),
]
def fiftytwo(fr, t, R):
    d = fr.d; T = R.T
    if t < T("l2") - .1: return
    cx, cy = 540, 960
    # fort wall silhouette
    if t < T("l5"):
        d.rectangle((120, 1000, 960, 1060), fill=(60, 50, 40))
        for x in range(120, 960, 60): d.rectangle((x, 980, x + 34, 1000), fill=(60, 50, 40))
    n_show = 52 if t >= T("l2") + 1.5 else int(52 * max(0, (t - T("l2")) / 1.5))
    out = ease((t - T("l4") - .6) / 2.0) if t >= T("l4") else 0
    for i in range(n_show):
        a = math.pi * (1.05 + .9 * i / 51); r = 150
        px, py = cx + r * 1.9 * math.cos(a), cy + 20 + r * .55 * math.sin(a) + 40 - 120 * out
        if t >= T("l4"): d.line((px, py, cx, cy - 120 * out), fill=(236, 190, 80), width=2)
        d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=(255, 230, 170))
    d.ellipse((cx - 16, cy - 16 - 120 * out, cx + 16, cy + 16 - 120 * out), fill=(255, 196, 70))
    if t >= T("l5"):                                                                       # lamps reflected in water
        k = ease((t - T("l5")) / 1.0)
        for i in range(17):
            x = 140 + i * 50
            d.ellipse((x - 9, 940 - 9, x + 9, 940 + 9), fill=(255, 210, 110))
            d.line((x, 990, x, 990 + 40 * k), fill=(255, 210, 110, ), width=4)
def scene(fr, t, R):
    card_scene(fr, t, R, "बंदी छोड़ दिवस", "दिवाली का सिख इतिहास", deco=fiftytwo, accent=(236, 150, 40),
               chips=["मुक्ति का दिन", "ग्वालियर किला · 1619", "अकेले नहीं निकले", "52 कलियों वाला चोला", "हरमंदिर साहिब जगमगाया"],
               chip_tags=("l1", "l2", "l3", "l4", "l5"))
if __name__ == "__main__":
    R, p = build_dyk("DiwaliDYK_03_BandiChhorDivas", LINES, scene, sys.argv[1], "भेजो!", "उस दोस्त को, जो ये\nकहानी नहीं जानता।", "दोस्त को ये कहानी भेजो", 93)
    print(p, round(R.dur, 1), "s violations:", R.violations[:8], len(R.violations))
