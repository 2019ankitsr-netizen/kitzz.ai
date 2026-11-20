# S1 ep07: How noise-cancelling earbuds work (Blender)

Same S1 look as ep06: cinematic product-macro 3D in Blender 5.1 (bpy from PyPI, Cycles CPU, AgX, DOF).
Glossy white earbud, neon sound-wave tubes (amber = outside noise, cyan = flipped anti-noise, white = what reaches your ear),
a small jet engine for the "hum". All animation is procedural per frame in `scene.py` (`update(t)`), no keyframes.

Beats: payoff-first hook (two waves merge into silence) → outer mic hears the hum → chip flips the wave →
peak + dip = flat → late anti-wave leaks (red) vs on time (green) → inner mic fixes the rest →
low hum cancelled vs voices blocked by the ear tip → 1936 patent, pilots' headsets → save/send CTA, loops into the hook.

Pipeline (WORK=/home/claude/anc):
`vo.py` (Kokoro am_michael 1.08×) → `scene.py $WORK/frames --res 60 --spp 10` (648×1152, ~4.4 s/frame on 2 CPUs)
→ `audio.py` (original score, engine hum that gets "cancelled" in sync with the picture, SFX, ducking, -14 LUFS)
→ `compose.py video out.mp4` (2× LANCZOS upscale, overlays, karaoke captions, blinking nudge, CTA, safe-zone check).

Setup: `pip install --break-system-packages bpy==5.1.2 kokoro-onnx soundfile pyloudnorm scipy` and `apt-get install espeak-ng`.
