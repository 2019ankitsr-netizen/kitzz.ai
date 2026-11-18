# हनुमान चालीसा — रोज़ 2 पंक्तियाँ (22 reels)

Din 1 = the two opening dohas (hand-built, `din01/`). Din 2–21 = two chaupais a day. Din 22 = closing doha.
Approved 18 Nov 2026. Look: Kalamkari ink (eng.py, art.py, motifs.py). Voice: Indic Parler-TTS **Rohit**, smooth calm conversational,
whole-line takes, each line checked against `assets/ref_hook.wav` (pitch + MFCC) so the voice never changes; `assets/save.wav` is reused every day.
Format: "क्या आप जानते हैं…?" hook → "इस वीडियो को सेव कर लीजिए, और मैं आपको आराम से बताता हूँ" → recitation card → 2 meanings → insight → follow + "कल…".

```
python3 build.py <din> <outdir> vo        # ~8 min (Parler on CPU)
python3 build.py <din> <outdir> render    # ~4 min; prints dur / LUFS / safe-zone violations
HC_STILLS=1 python3 build.py <din> <outdir> render   # contact sheet with safe-zone overlay
python3 captions.py <din> > HanumanChalisa_DinNN.txt
```
Scripts: `episodes.py`. Output name: `queue/HanumanChalisa_DinNN.mp4`.
