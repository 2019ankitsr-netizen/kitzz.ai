# S1 ep06 — Why a torn QR code still pays (Blender pilot)

New S1 look (Nov 2026): **cinematic product-macro 3D in Blender 5.1 (bpy from PyPI, Cycles CPU)**.
Glossy black ceramic modules + matte white tiles, AgX high-contrast, DOF, warm key / cool rim.

Pipeline: `vo.py` (Kokoro am_michael 1.08×) → `scene.py frames --res 50 --spp 6` (540×960, OIDN denoise, 24 fps, ~8.5 s/frame on 2 CPUs)
→ `audio.py` (original cinematic pulse score + SFX, ducking, -14 LUFS) → `compose.py video out.mp4`
(LANCZOS 2× upscale + unsharp + vignette, crisp Pillow overlays: hook, toast, labels, karaoke captions, blinking nudge, CTA; safe-zone check).

Setup: `pip install --break-system-packages bpy==5.1.2 qrcode kokoro-onnx soundfile pyloudnorm scipy` and `apt-get install espeak-ng`.
