import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/reel/models/kokoro.onnx', '/home/claude/reel/models/voices.bin')
LINES = [
 ("hook",   "An anar is a rocket that's not allowed to take off."),
 ("inside", "Inside the clay pot is a tightly packed powder. Fuel, plus a chemical that carries its own oxygen."),
 ("burn",   "Light the top, and it burns downward, layer by layer, making a rush of hot gas."),
 ("jet",    "The only way out is that tiny hole. So the gas shoots up as a jet, and pushes the pot into the ground."),
 ("sparks", "The sparks? Tiny bits of metal, like iron and aluminium, glowing white hot as they fly."),
 ("col0",   "And the colours are metal salts."),
 ("red",    "Strontium burns red."),
 ("green",  "Barium, green."),
 ("blue",   "Copper, blue."),
 ("bomb",   "Trap that gas with no way out, and you get a bang instead."),
 ("cta",    "Send this to whoever lights the anar at your place. Arm's length, always. Because remember,"),
]
SR = 24000
out, meta, t = [], [], 0.35
out.append(np.zeros(int(SR*0.35), dtype=np.float32))
for key, text in LINES:
    s, sr = k.create(text, voice='am_michael', speed=1.04, lang='en-us')
    s = s.astype(np.float32)
    # trim silence
    idx = np.where(np.abs(s) > 0.01)[0]
    s = s[max(0, idx[0]-600): idx[-1]+2400]
    gap = 0.12 if key in ('red','green') else (0.3 if key != 'cta' else 0.35)
    meta.append(dict(key=key, text=text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out.append(s); out.append(np.zeros(int(SR*gap), dtype=np.float32))
    t += len(s)/SR + gap
a = np.concatenate(out)
sf.write('/home/claude/anar/vo.wav', a, SR)
json.dump(dict(lines=meta, total=round(t, 3)), open('/home/claude/anar/vo.json', 'w'), indent=1)
print(json.dumps(meta, indent=1), t)
