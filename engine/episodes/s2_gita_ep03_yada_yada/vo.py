import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/reel/models/kokoro.onnx', '/home/claude/reel/models/voices.bin')
# key, spoken text, on-screen text, speed, gap after
LINES = [
 ("hook",  "जब हर तरफ़ ग़लत जीत रहा हो, तब क्या होता है? कृष्ण ने ख़ुद बताया।", "Jab har taraf galat jeet raha ho, tab kya hota hai? Krishna ne khud bataya.", 0.97, 0.35),
 ("fear",  "अर्जुन हैरान थे। कृष्ण बार बार धरती पर क्यों आते हैं?", "Arjun hairaan the. Krishna baar baar dharti par kyun aate hain?", 0.95, 0.35),
 ("krishna", "कृष्ण का जवाब,", "Krishna ka jawaab,", 0.95, 0.45),
 ("sh1",   "यदा यदा हि धर्मस्य, ग्लानिर् भवति भारत।", "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत ।", 0.8, 0.35),
 ("sh2",   "अभ्युत्थानम् अधर्मस्य, तदात्मानं सृजाम्यहम्।", "अभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम् ॥", 0.8, 0.55),
 ("mean1", "यानी, हे भारत, जब जब धर्म घटता है, और अधर्म बढ़ता है,", "Yaani, he Bharat, jab jab dharm ghatta hai, aur adharm badhta hai,", 0.95, 0.3),
 ("mean2", "तब तब मैं ख़ुद प्रकट होता हूँ।", "tab tab main khud prakat hota hoon.", 0.93, 0.4),
 ("today", "आज भी, जब ग़लत बढ़े और सब चुप रहें, अँधेरा वहीं बढ़ता है।", "Aaj bhi, jab galat badhe aur sab chup rahein, andhera wahin badhta hai.", 0.95, 0.35),
 ("shoot", "रोशनी का इंतज़ार मत करो। एक दीया तुम जलाओ।", "Roshni ka intezaar mat karo. Ek diya tum jalao.", 0.93, 0.5),
 ("cta",   "जो ग़लत के सामने अकेला खड़ा है, उसे ये भेजो। क्योंकि,", "Jo galat ke saamne akela khada hai, use ye bhejo. Kyunki,", 0.95, 0.35),
]
SR = 24000; out = [np.zeros(int(SR*0.3), dtype=np.float32)]; meta = []; t = 0.3
for key, text, disp, sp, gap in LINES:
    s, sr = k.create(text, voice='hm_omega', speed=sp, lang='hi'); s = s.astype(np.float32)
    idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0]-600): idx[-1]+2400]; f=int(0.012*SR); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f)
    meta.append(dict(key=key, text=disp or text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out.append(s); out.append(np.zeros(int(SR*gap), dtype=np.float32)); t += len(s)/SR + gap
sf.write('/home/claude/gita3/vo.wav', np.concatenate(out), SR)
json.dump(dict(lines=meta, total=round(t, 3)), open('/home/claude/gita3/vo.json', 'w'), ensure_ascii=False, indent=1)
for m in meta: print(m['key'], m['start'], m['end'])
print(t)
