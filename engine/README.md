# kitzz.ai reel engine

Everything is rendered in code (Pillow + ffmpeg + Kokoro TTS), so every reel is original.

| File | What it does |
|---|---|
| `style_frames.py` | Style frames for the 5 series + `Frame` with the safe-zone check |
| `audio.py` | Kokoro voice lines (pronunciation fixes for OTP, UPI, FASTag, ₹, Hindi "ए आई"), voice polish, synthesized music beds + SFX, ducking, -14 LUFS |
| `reel.py` | Voice-timed reels: burned-in captions, mid-reel nudge chip, end CTA card, safe-zone check on sampled frames, contact sheet, encode |
| `voicetest.py`, `voicetest_s3b.py` | Voice tests (3 speeds × 2 tones) per series |
| `pilots/` | One pilot per series (S1 OTP, S2 Tara Ep 1, S3 Missing ₹1, S4 ₹199, S5 Saturn's rings) |

## Setup (new session)
```bash
pip install --break-system-packages kokoro-onnx soundfile pyloudnorm fonttools scipy
apt-get install -y espeak-ng          # Hindi + English phonemes
mkdir -p /home/claude/models && cd /home/claude/models
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python3 engine/pilots/s1_otp.py out/   # -> out/<name>.mp4 + out/<name>_contact_safezone.png
```
Set `KOKORO_DIR` if the model files live elsewhere.

## Chosen voices (Nov 2026 voice tests)
- S1 How Things Work: am_michael, warm, 1.08×
- S2 AI Ki Kahani: hf_alpha / hf_beta / hm_psi, lively (+1 semitone), 1.08×
- S3 CCTV Riddles: am_fenrir detective (warm, −0.5 semitone, 1.0×) + bf_emma CCTV log
- S4 Hook Shots: af_heart, confident (warm), 1.08×
- S5 Space Transit: am_michael + bf_emma announcer, clear, 1.0×

## Rules baked in
Safe zone x 65–1015, y 269–1248; right rail x > 930 in y 900–1700 stays clear; captions in y 1060–1230.
One mid-reel nudge (~40%, 1.6 s) and one end ask after the value; loop line flows back into the hook.
