# Kokoro am_michael 1.08x voiceover -> $WORK/vo.wav + vo.json
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
WORK = os.environ.get('WORK', '/home/claude/mw'); os.makedirs(WORK, exist_ok=True)
k = Kokoro('/home/claude/models/kokoro-v1.0.onnx', '/home/claude/models/voices-v1.0.bin')
LINES = [
 ("hook",   "Your microwave never heats your food. Your food heats itself.", None),
 ("mol",    "Food is full of water. Each water molecule has a plus end and a minus end, like a tiny magnet.", None),
 ("mag",    "A part called a magnetron fires invisible microwaves.", None),
 ("flip",   "Their field flips two point four five billion times a second, and the water keeps twisting to line up.", "Their field flips 2.45 billion times a second, and the water keeps twisting to line up."),
 ("heat",   "All that twisting jostles everything around it. That jostling is heat.", None),
 ("spin",   "The waves leave hot and cold spots. That's why the plate spins.", None),
 ("metal",  "Metal bounces the waves back, and sharp edges can spark. Keep the spoon out.", None),
 ("origin", "In 1945, engineer Percy Spencer stood next to a radar magnetron, and the chocolate bar in his pocket melted.", None),
 ("cta",    "Send this to the friend who reheats their chai five times a day. Because your microwave never heats your food.", None),
]
SR = 24000
out, meta, t = [np.zeros(int(SR*0.12), np.float32)], [], 0.12
for key, text, shown in LINES:
    s, sr = k.create(text, voice='am_michael', speed=1.08, lang='en-us')
    s = s.astype(np.float32); idx = np.where(np.abs(s) > 0.01)[0]
    s = s[max(0, idx[0]-500): idx[-1]+2000]
    gap = 0.26
    meta.append(dict(key=key, text=shown or text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out += [s, np.zeros(int(SR*gap), np.float32)]; t += len(s)/SR + gap
t += 0.5; out.append(np.zeros(int(SR*0.5), np.float32))
sf.write(f'{WORK}/vo.wav', np.concatenate(out), SR)
json.dump(dict(lines=meta, total=round(t, 3)), open(f'{WORK}/vo.json', 'w'), indent=1)
for m in meta: print(m['key'], m['start'], m['end'])
print('total', t)
