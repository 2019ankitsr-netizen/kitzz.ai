import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('/home/claude/reel/models/kokoro.onnx', '/home/claude/reel/models/voices.bin')
LINES = [
 ("hook",  "Your internet isn't in the cloud. It's at the bottom of the ocean."),
 ("tower", "Hit play on a video, and your phone shouts the request to the nearest tower."),
 ("fibre", "From there, nothing is wireless. It dives underground into glass fibre, thin as a hair, as pulses of light."),
 ("coast", "That light races to the coast, and plunges straight into the sea."),
 ("ocean", "Cables no thicker than a garden hose cross entire oceans. About ninety nine percent of data between continents travels this way."),
 ("sat",   "Satellites? Less than one percent."),
 ("dc",    "On the far shore, a data centre grabs your video, and sends it all the way back. In about the blink of an eye."),
 ("cta",   "Send this to the friend who thinks it's all satellites. Because, no."),
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
    gap = 0.32 if key != 'cta' else 0.5
    meta.append(dict(key=key, text=text, start=round(t, 3), end=round(t+len(s)/SR, 3)))
    out.append(s); out.append(np.zeros(int(SR*gap), dtype=np.float32))
    t += len(s)/SR + gap
a = np.concatenate(out)
sf.write('/home/claude/reel/vo.wav', a, SR)
json.dump(dict(lines=meta, total=round(t, 3)), open('/home/claude/reel/vo.json', 'w'), indent=1)
print(json.dumps(meta, indent=1), t)
