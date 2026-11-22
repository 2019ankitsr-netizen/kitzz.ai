import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/reel/models/kokoro.onnx', '/home/claude/reel/models/voices.bin')
# key, spoken text, on-screen text, speed, gap after
LINES = [
 ("hook",  "कुछ भी हमेशा नहीं रहता। न सुख, न दुख। कृष्ण ने ख़ुद बताया।", "Kuch bhi hamesha nahi rehta. Na sukh, na dukh. Krishna ne khud bataya.", 0.97, 0.35),
 ("fear",  "अर्जुन का दिल टूटा था। हर तरफ़ दर्द, हर तरफ़ दुख।", "Arjun ka dil toota tha. Har taraf dard, har taraf dukh.", 0.95, 0.35),
 ("krishna", "कृष्ण मुस्कुराए, और बोले,", "Krishna muskuraaye, aur bole,", 0.95, 0.45),
 ("sh1",   "मात्रा स्पर्शास्तु कौन्तेय, शीतोष्ण सुख दुःखदाः।", "मात्रास्पर्शास्तु कौन्तेय शीतोष्णसुखदुःखदाः ।", 0.8, 0.35),
 ("sh2",   "आगमापायिनो अनित्याः, तांस् तितिक्षस्व भारत।", "आगमापायिनोऽनित्यास्तांस्तितिक्षस्व भारत ॥", 0.8, 0.55),
 ("mean1", "यानी, हे कौन्तेय, सर्दी गर्मी, सुख दुख, ये सब आते हैं, और चले जाते हैं।", "Yaani, he Kaunteya, sardi garmi, sukh dukh, ye sab aate hain, aur chale jaate hain.", 0.95, 0.3),
 ("mean2", "ये टिकते नहीं। इन्हें सहना सीखो, हे भारत।", "Ye tikte nahi. Inhe sehna seekho, he Bharat.", 0.93, 0.4),
 ("today", "फ़ेल रिज़ल्ट, टूटा दिल, बुरा दिन। मौसम की तरह, ये भी बदलेगा।", "Fail result, toota dil, bura din. Mausam ki tarah, ye bhi badlega.", 0.95, 0.35),
 ("shoot", "तूफ़ान में रुको मत। चलते रहो, सुबह ज़रूर आएगी।", "Toofan mein ruko mat. Chalte raho, subah zaroor aayegi.", 0.93, 0.5),
 ("cta",   "जो अभी मुश्किल वक़्त से गुज़र रहा है, उसे ये भेजो। क्योंकि,", "Jo abhi mushkil waqt se guzar raha hai, use ye bhejo. Kyunki,", 0.95, 0.35),
]
SR = 24000; out = [np.zeros(int(SR*0.3), dtype=np.float32)]; meta = []; t = 0.3
for key, text, disp, sp, gap in LINES:
    s, sr = k.create(text, voice='hm_omega', speed=sp, lang='hi'); s = s.astype(np.float32)
    idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0]-600): idx[-1]+2400]; f=int(0.012*SR); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f)
    meta.append(dict(key=key, text=disp or text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out.append(s); out.append(np.zeros(int(SR*gap), dtype=np.float32)); t += len(s)/SR + gap
sf.write('/home/claude/gita4/vo.wav', np.concatenate(out), SR)
json.dump(dict(lines=meta, total=round(t, 3)), open('/home/claude/gita4/vo.json', 'w'), ensure_ascii=False, indent=1)
for m in meta: print(m['key'], m['start'], m['end'])
print(t)
