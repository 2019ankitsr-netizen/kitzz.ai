import json, numpy as np, soundfile as sf
from lines import LINES
d = {}
for k, _, _ in LINES:
    v, sr = sf.read(f'vo/{k}.wav', dtype='float32'); idx = np.where(np.abs(v) > 0.01)[0]
    d[k] = (idx[-1] + 4000 - max(0, idx[0] - 400)) / sr
json.dump(d, open('durs.json', 'w'), indent=1); print({k: round(v, 2) for k, v in d.items()}, round(sum(d.values()), 1))
