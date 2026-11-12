import sys; sys.path.insert(0, '/home/claude/bk'); from kit import make_voice
N, T, B = 'hf_alpha', 'hf_beta', 'hm_psi'
def L(key, v, say, cap, who=None, **k): return dict(key=key, voice=v, say=say, cap=cap, who=who, lang='hi', speed=k.pop('speed', 1.08), pitch=k.pop('pitch', 1.0), **k)
LINES = [
 L('hook', N, "बबलू ने पूछा: तारा, तुम सोचती कैसे हो?", "Bablu ne poocha: Tara, tum sochti kaise ho?", gap=0.25),
 L('t1', T, "सच बताऊँ? मैं बस अगला शब्द अंदाज़ा लगाती हूँ।", "Sach bataun? Main bas agla shabd andaaza lagaati hoon.", who='TARA'),
 L('b1', B, "बस? इतना ही?", "Bas? Itna hi?", who='BABLU', pitch=0.5),
 L('chai', N, "जैसे कोई लिखे, चाय के साथ... तो अगला शब्द?", "Jaise koi likhe 'chai ke saath'... toh agla shabd?"),
 L('b2', B, "बिस्कुट!", "Biscuit!", who='BABLU', pitch=0.5, gap=0.2),
 L('t2', T, "बिल्कुल! मैंने करोड़ों वाक्य पढ़े हैं। तो मुझे पता है, कौन सा शब्द सबसे ज़्यादा आता है।", "Bilkul! Maine crore-on vaakya padhe hain. Toh mujhe pata hai, kaunsa shabd sabse zyada aata hai.", who='TARA'),
 L('chain', N, "एक शब्द चुना, फिर अगला, फिर अगला। ऐसे ही पूरा जवाब बनता है।", "Ek shabd chuna, phir agla, phir agla. Aise hi poora jawaab banta hai."),
 L('b3', B, "तो अगर पढ़ा हुआ ही गलत हो?", "Toh agar padha hua hi galat ho?", who='BABLU', pitch=0.5),
 L('t3', T, "तो मैं भी, पूरे भरोसे से गलत बोल सकती हूँ। इसलिए ज़रूरी बातें, जाँच लेना।", "Toh main bhi poore bharose se galat bol sakti hoon. Isliye zaroori baatein jaanch lena.", who='TARA'),
 L('cliff', N, "पर अगले दिन, तारा ने बबलू को एक ऐसी तस्वीर दिखाई, जो कभी खींची ही नहीं गई थी।", "Par agle din, Tara ne Bablu ko ek aisi tasveer dikhayi, jo kabhi kheenchi hi nahi gayi thi.", pre=0.3, speed=1.0, pitch=0.0),
 L('cta', N, "भाग पाँच, जल्द। फ़ॉलो करो, और ये उस दोस्त को भेजो, जो ए आई पर आँख बंद करके भरोसा करता है।", "Part 5 jald. Follow karo, aur ye us dost ko bhejo jo AI pe aankh band karke bharosa karta hai.", gap=0.1),
]
make_voice('/home/claude/s2', LINES, lead=0.1, tail=0.6)
