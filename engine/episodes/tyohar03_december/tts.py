"""Voice lines for Tyohar 03: दिसंबर के 3 बड़े त्योहार (Kokoro hm_omega, festival guide)."""
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, '/home/claude/kitzz.ai/engine')
from audio import say

L = [
    "दिसंबर में, तीन बड़े त्योहार आ रहे हैं! तारीख़ें नोट कर लो।",
    "पहला, काल भैरव जयंती। मंगलवार, एक दिसंबर।",
    "मान्यता है, इसी दिन, शिव जी ने काल भैरव का रूप लिया था। काशी के कोतवाल, और समय के स्वामी।",
    "दूसरा, विवाह पंचमी। सोमवार, चौदह दिसंबर।",
    "इसी दिन, जनकपुर में, श्री राम और माता सीता का विवाह हुआ था। अयोध्या और जनकपुर में, आज भी बारात निकलती है।",
    "तीसरा, गीता जयंती। रविवार, बीस दिसंबर।",
    "कुरुक्षेत्र में, श्री कृष्ण ने, अर्जुन को गीता का ज्ञान दिया था। और इसी दिन, मोक्षदा एकादशी भी है।",
    "ये रील, फ़ैमिली ग्रुप में भेजो, और सेव कर लो। क्योंकि दिसंबर में, तीन बड़े त्योहार आ रहे हैं!",
]
if __name__ == '__main__':
    voice = sys.argv[1] if len(sys.argv) > 1 else 'hm_omega'
    sp = float(sys.argv[2]) if len(sys.argv) > 2 else 1.05
    durs = []
    for i, t in enumerate(L):
        a = say(t, voice, speed=sp, lang='hi')
        sf.write(f'v{i}.wav', a, 24000); durs.append(len(a) / 24000)
    json.dump(durs, open('durs.json', 'w'))
    print([round(d, 2) for d in durs], round(sum(durs), 1))
