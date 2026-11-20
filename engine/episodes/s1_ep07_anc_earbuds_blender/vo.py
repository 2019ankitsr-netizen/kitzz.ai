# Kokoro am_michael 1.08x voiceover -> $WORK/vo.wav + vo.json
import json, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
WORK = os.environ.get('WORK', '/home/claude/anc'); os.makedirs(WORK, exist_ok=True)
k = Kokoro('/home/claude/models/kokoro-v1.0.onnx', '/home/claude/models/voices-v1.0.bin')
LINES = [
 ("hook",   "Your earbuds make noise, to give you silence.", None),
 ("mic",    "A tiny mic on the outside listens to the world. Like this engine hum.", None),
 ("flip",   "A chip flips that sound wave upside down. Every peak becomes a dip.", None),
 ("cancel", "Play both together, and they cancel out. Peak plus dip, equals flat. Silence.", None),
 ("fast",   "It redoes this thousands of times a second. Even a tiny delay, and it stops working.", None),
 ("inside", "A second mic inside your ear checks what's left, and fixes it.", None),
 ("low",    "That's why it kills the plane hum, but you still hear voices. High, sharp sounds are blocked by the ear tip instead.", "That's why it kills the plane hum, but you still hear voices. High, sharp sounds are blocked by the ear tip instead."),
 ("origin", "The idea was patented in 1936. Decades later, it went into headsets for pilots.", None),
 ("cta",    "Send this to the friend who never takes their earbuds out. Because now you know, your earbuds make noise.", None),
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
