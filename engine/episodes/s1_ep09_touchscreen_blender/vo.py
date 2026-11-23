# Kokoro am_michael 1.08x voiceover -> $WORK/vo.wav + vo.json
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
WORK = os.environ.get('WORK', '/home/claude/ts'); os.makedirs(WORK, exist_ok=True)
k = Kokoro('/home/claude/models/kokoro-v1.0.onnx', '/home/claude/models/voices-v1.0.bin')
LINES = [
 ("hook",   "Your phone can't feel your finger. It feels your electricity.", None),
 ("grid",   "Under the glass is a grid of see-through wires. Rows one way, columns the other.", None),
 ("field",  "Every crossing point holds a tiny electric charge.", None),
 ("touch",  "Your body conducts electricity. So your finger pulls a little charge away from the crossings under it.", None),
 ("scan",   "A chip checks every crossing over a hundred times a second, and finds where the charge dropped. That's your tap.", None),
 ("swipe",  "Move your finger, and the dip moves too. Two dips? Pinch to zoom.", None),
 ("glove",  "That's why normal gloves don't work. But a sausage does. It conducts, just like you.", None),
 ("origin", "This kind of touchscreen was invented in England in 1965, and first used for air traffic control.", None),
 ("cta",    "Send this to the friend who taps harder when the screen doesn't respond. Because your phone can't feel your finger.", None),
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
