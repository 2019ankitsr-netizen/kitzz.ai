import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/reel/models/kokoro.onnx', '/home/claude/reel/models/voices.bin')
# key, spoken text, on-screen text, speed, gap after
LINES = [
 ("hook",  "अर्जुन ने युद्ध शुरू होने से पहले ही धनुष रख दिया था।", None, 0.97, 0.35),
 ("fear",  "सामने अपने ही लोग खड़े थे। जीते तो क्या, हारे तो क्या? नतीजे के डर ने उसे रोक दिया।", None, 0.95, 0.3),
 ("krishna", "तब कृष्ण ने कहा,", None, 0.95, 0.45),
 ("sh1",   "कर्मण्येवाधिकारस्ते, मा फलेषु कदाचन।", "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन ।", 0.8, 0.35),
 ("sh2",   "मा कर्मफल हेतुर्भूर्, मा ते संगोस्त्व कर्मणि।", "मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥", 0.8, 0.55),
 ("mean1", "यानी, तुम्हारा अधिकार सिर्फ़ कर्म पर है, फल पर कभी नहीं।", None, 0.95, 0.3),
 ("mean2", "फल को अपना मक़सद मत बनाओ, और हाथ पर हाथ रखकर बैठ भी मत जाओ।", None, 0.95, 0.35),
 ("today", "एग्ज़ाम हो, इंटरव्यू हो, या रील। मेहनत तुम्हारे हाथ में है, नतीजा नहीं।", None, 0.95, 0.3),
 ("shoot", "तो बस, तीर चलाओ।", None, 0.95, 0.45),
 ("cta",   "जिसे रिज़ल्ट की टेंशन है, उसे ये भेजो। क्योंकि याद है ना,", None, 0.95, 0.35),
]
SR = 24000; out = [np.zeros(int(SR*0.3), dtype=np.float32)]; meta = []; t = 0.3
for key, text, disp, sp, gap in LINES:
    s, sr = k.create(text, voice='hm_omega', speed=sp, lang='hi'); s = s.astype(np.float32)
    idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0]-600): idx[-1]+2400]; f=int(0.012*SR); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f)
    meta.append(dict(key=key, text=disp or text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out.append(s); out.append(np.zeros(int(SR*gap), dtype=np.float32)); t += len(s)/SR + gap
sf.write('/home/claude/gita/vo.wav', np.concatenate(out), SR)
json.dump(dict(lines=meta, total=round(t, 3)), open('/home/claude/gita/vo.json', 'w'), ensure_ascii=False, indent=1)
for m in meta: print(m['key'], m['start'], m['end'])
print(t)
