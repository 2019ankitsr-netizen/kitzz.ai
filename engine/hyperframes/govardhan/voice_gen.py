"""Generate the Govardhan narration line by line with Indic Parler-TTS (Rohit). Writes line_XX.wav + timings.json."""
import json, time, torch, soundfile as sf, numpy as np
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration
torch.set_num_threads(2)
REPO = "RXD03/indic-parler-tts"
model = ParlerTTSForConditionalGeneration.from_pretrained(REPO)
tok = AutoTokenizer.from_pretrained(REPO); dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
SR = model.config.sampling_rate
DESC = {
    "calm": "Rohit speaks in a warm, expressive storytelling voice at a moderate pace, with clear audio and very little background noise.",
    "tense": "Rohit speaks in a deep, dramatic and intense storytelling voice at a moderate pace, with clear audio and very little background noise.",
    "bright": "Rohit speaks in a warm, joyful and expressive storytelling voice at a moderate pace, with clear audio and very little background noise.",
}
LINES = json.load(open("/home/claude/work/gov/lines.json"))
out = []
for i, L in enumerate(LINES):
    t0 = time.time(); torch.manual_seed(7)
    ids = dtok(DESC[L["mood"]], return_tensors="pt"); pids = tok(L["hi"], return_tensors="pt")
    with torch.no_grad():
        a = model.generate(input_ids=ids.input_ids, attention_mask=ids.attention_mask,
                           prompt_input_ids=pids.input_ids, prompt_attention_mask=pids.attention_mask).cpu().numpy().squeeze()
    # trim leading/trailing silence
    e = np.abs(a) > 0.01; idx = np.where(e)[0]
    if len(idx): a = a[max(0, idx[0] - int(.05 * SR)): idx[-1] + int(.12 * SR)]
    sf.write(f"/home/claude/work/gov/line_{i:02d}.wav", a, SR)
    out.append(dict(i=i, dur=len(a) / SR)); print(i, round(len(a) / SR, 1), "s in", round(time.time() - t0), "s", flush=True)
json.dump(dict(sr=SR, lines=out), open("/home/claude/work/gov/voice_meta.json", "w"))
print("DONE")
