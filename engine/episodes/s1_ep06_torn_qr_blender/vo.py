import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/models/kokoro-v1.0.onnx', '/home/claude/models/voices-v1.0.bin')
LINES = [
 ("hook",   "This Q R code is torn. And it still works.", "This QR code is torn. And it still works."),
 ("finder", "See these three big squares? They tell your phone where the corners are, so it reads the code from any angle.", None),
 ("bits",   "Every tiny block is one bit. Black is a one. White is a zero.", None),
 ("backup", "But a big part of the code isn't your data at all. It's backup.", None),
 ("rs",     "A bit of maths called Reed Solomon lets your phone use those extra blocks to rebuild the missing pieces.", "A bit of maths called Reed–Solomon lets your phone use those extra blocks to rebuild the missing pieces."),
 ("thirty", "At the highest level, up to thirty percent of the code can be gone.", "At the highest level, up to 30% of the code can be gone."),
 ("origin", "It was invented in Japan in 1994, to track car parts in factories.", None),
 ("cta",    "Save this, and send it to the friend whose shop Q R is falling apart. Because now you know.", "Save this, and send it to the friend whose shop QR is falling apart. Because now you know."),
]
SR = 24000
out, meta, t = [np.zeros(int(SR*0.15), np.float32)], [], 0.15
for key, text, shown in LINES:
    s, sr = k.create(text, voice='am_michael', speed=1.08, lang='en-us')
    s = s.astype(np.float32); idx = np.where(np.abs(s) > 0.01)[0]
    s = s[max(0, idx[0]-500): idx[-1]+2000]
    gap = 0.28
    meta.append(dict(key=key, text=shown or text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out += [s, np.zeros(int(SR*gap), np.float32)]; t += len(s)/SR + gap
t += 0.6; out.append(np.zeros(int(SR*0.6), np.float32))
sf.write('vo.wav', np.concatenate(out), SR)
json.dump(dict(lines=meta, total=round(t, 3)), open('vo.json', 'w'), indent=1)
for m in meta: print(m['key'], m['start'], m['end'])
print('total', t)
