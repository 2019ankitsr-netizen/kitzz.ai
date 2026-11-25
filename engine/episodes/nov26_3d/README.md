# Nov 26 3D / particle pilots (Three.js, frame-by-frame)

Four series pilots rendered deterministically in headless Chrome: each page exposes `window.seek(t)`,
`render.py` screenshots every frame at 30 fps, ffmpeg muxes with the synthesized soundtrack.

| Series | Page | Video | Voice |
|---|---|---|---|
| SCALE ON 01 – Sooraj football at Wankhede | web/scaleon_ep01.html (+ timeline.json) | queue/ScaleOn_01_SoorajFootball.mp4 | Kokoro hm_omega |
| Brahmand Katha 01 – Samudra Manthan (particles) | web/manthan.html | queue/BrahmandKatha_01_SamudraManthan.mp4 | Kokoro hf_alpha 0.97 |
| Andar Kya Hai? 01 – Pressure cooker (exploded/cutaway) | web/cooker.html | queue/AndarKyaHai_01_PressureCooker.mp4 | Kokoro hf_beta |
| Ek Shape, Ek Kahani 01 – Ret se AI tak (15 s loop) | web/morph.html | queue/EkShape_01_RetSeAI.mp4 | music only |

## Rebuild
```
cd web && npm i three@0.170.0
mkdir -p fonts tex
cp /usr/share/fonts/opentype/inter/Inter-{Black,ExtraBold,Bold,SemiBold}.otf fonts/; cp /usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf fonts/
# Google Fonts (OFL): ofl/yatraone/YatraOne-Regular.ttf, ofl/hind/Hind-Bold.ttf, ofl/hind/Hind-SemiBold.ttf, ofl/cinzel/Cinzel[wght].ttf (save as Cinzel-VF.ttf)
# Textures: raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/{earth_atmos_2048.jpg,earth_lights_2048.png,moon_1024.jpg} -> tex/
python3 -m http.server 8765 &      # from web/
```
Voice: `pip install kokoro torch espeakng-loader` (tts.py points phonemizer at espeakng_loader). `python3 mkvo.py <series> <voice> <speed>` reads `<series>/lines.json` (+gaps.json) and writes `web/<series>_timeline.json`.
Frames: `PAGE=manthan.html python3 render.py frames "list(range(N))" 2` (N = end*30). Stills check: `python3 sheet.py stills out.jpg 6` (safe-zone overlay).
Audio: `python3 audio_<series>.py` (original synth score + ducked VO). Mux: ffmpeg libx264 crf 19 + loudnorm I=-14.
Note: common.js uses mulberry32 for randoms (the old LCG made particle shapes clump).
