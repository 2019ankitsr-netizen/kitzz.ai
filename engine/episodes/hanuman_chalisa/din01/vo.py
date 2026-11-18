"""Whole-line Parler generation with one fixed speaker; 2 seeds per line, keep the take closest to the reference voice."""
import os, sys, json, numpy as np, soundfile as sf, torch, librosa
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lines import LINES
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
REPO = "RXD03/indic-parler-tts"; torch.set_num_threads(2)
m = ParlerTTSForConditionalGeneration.from_pretrained(REPO)
tok = AutoTokenizer.from_pretrained(REPO); dtok = AutoTokenizer.from_pretrained(m.config.text_encoder._name_or_path)
SR = m.config.sampling_rate
BASE = "Rohit speaks in a smooth, calm and friendly conversational voice{p}, warmly explaining with gentle and natural intonation, with a very close recording that has no background noise."
MOODS = {"calm": BASE.format(p=" at a moderate pace"), "chant": BASE.format(p=" at a slow pace, reciting a devotional verse melodiously")}
SEEDS = [7, 21]
def gen(desc, text, seed):
    torch.manual_seed(seed)
    ids = dtok(desc, return_tensors='pt'); pids = tok(text, return_tensors='pt')
    with torch.no_grad():
        a = m.generate(input_ids=ids.input_ids, attention_mask=ids.attention_mask,
                       prompt_input_ids=pids.input_ids, prompt_attention_mask=pids.attention_mask).cpu().numpy().squeeze().astype(np.float32)
    idx = np.where(np.abs(a) > 0.012)[0]
    return a[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.15 * SR)]
def feats(a):
    f0, _, _ = librosa.pyin(a, fmin=60, fmax=400, sr=SR, frame_length=4096); f = f0[~np.isnan(f0)]
    mf = librosa.feature.mfcc(y=a, sr=SR, n_mfcc=20).mean(1)
    return np.median(f) if len(f) else 0, mf, len(a) / SR
os.makedirs('vo', exist_ok=True); os.makedirs('vo/takes', exist_ok=True)
ref = None; only = sys.argv[1:]; report = {}
for key, text, mood in LINES:
    if only and key not in only: continue
    takes = []
    for sd in SEEDS:
        a = gen(MOODS[mood], text, sd); sf.write(f'vo/takes/{key}_{sd}.wav', a, SR)
        takes.append((sd, a, feats(a)))
    if ref is None:  # reference = hook take with median pitch nearest 130 Hz (calm male)
        sd, a, f = min(takes, key=lambda t: abs(t[2][0] - 130)); ref = f
    else:
        def score(t):
            return abs(t[2][0] - ref[0]) / 10 + np.linalg.norm(t[2][1][1:] - ref[1][1:]) / 20
        sd, a, f = min(takes, key=score)
    sf.write(f'vo/{key}.wav', a, SR)
    report[key] = dict(seed=sd, f0=round(float(f[0]), 1), dur=round(f[2], 2), chars_s=round(len(text) / f[2], 1),
                       all=[(t[0], round(float(t[2][0]), 1)) for t in takes])
    print(key, report[key], flush=True)
json.dump(report, open('vo/report.json', 'w'), ensure_ascii=False, indent=1)
