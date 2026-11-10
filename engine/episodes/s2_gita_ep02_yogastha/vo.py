import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/reel/models/kokoro.onnx', '/home/claude/reel/models/voices.bin')
# key, spoken text, on-screen text, speed, gap after
LINES = [
 ("hook",  "जीत पर उछलना, हार पर टूटना। कृष्ण कहते हैं, दोनों छोड़ दो।", None, 0.97, 0.35),
 ("fear",  "फल की चिंता नहीं करनी, ठीक है। तो फिर कर्म करें कैसे?", None, 0.95, 0.35),
 ("krishna", "कृष्ण का जवाब,", None, 0.95, 0.45),
 ("sh1",   "योगस्थः कुरु कर्माणि, संगं त्यक्त्वा धनंजय।", "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय ।", 0.8, 0.35),
 ("sh2",   "सिद्ध्य सिद्ध्योः समो भूत्वा, समत्वं योग उच्यते।", "सिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते ॥", 0.8, 0.55),
 ("mean1", "यानी, हे अर्जुन, आसक्ति छोड़कर, योग में टिककर कर्म करो।", None, 0.95, 0.3),
 ("mean2", "सफलता मिले या असफलता, मन को बराबर रखो। इसी बराबरी का नाम योग है।", None, 0.95, 0.35),
 ("today", "रील वायरल हो या फ़्लॉप, नंबर आएँ या ना आएँ। अगला काम उसी मन से करो।", None, 0.95, 0.3),
 ("shoot", "बस, मन का तराज़ू सीधा रखो।", None, 0.95, 0.45),
 ("cta",   "जो हर रिज़ल्ट पर हिल जाता है, उसे ये भेजो। क्योंकि,", None, 0.95, 0.35),
]
SR = 24000; out = [np.zeros(int(SR*0.3), dtype=np.float32)]; meta = []; t = 0.3
for key, text, disp, sp, gap in LINES:
    s, sr = k.create(text, voice='hm_omega', speed=sp, lang='hi'); s = s.astype(np.float32)
    idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0]-600): idx[-1]+2400]; f=int(0.012*SR); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f)
    meta.append(dict(key=key, text=disp or text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out.append(s); out.append(np.zeros(int(SR*gap), dtype=np.float32)); t += len(s)/SR + gap
sf.write('/home/claude/gita2/vo.wav', np.concatenate(out), SR)
json.dump(dict(lines=meta, total=round(t, 3)), open('/home/claude/gita2/vo.json', 'w'), ensure_ascii=False, indent=1)
for m in meta: print(m['key'], m['start'], m['end'])
print(t)
