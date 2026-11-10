Tyohar 01 · Chhath 4 days (Hindi). HyperFrames 0.9.20 + GSAP 3.12.5, Kokoro hf_alpha voice (SMOOTH).
Run: python3 build.py -> hf/index.html; HYPERFRAMES_BROWSER_PATH=<chromium> npx -y hyperframes@0.9.20 render hf -o t1_v.mp4 -q looks -w 2 --fps 30; python3 mix.py; mux.
Needs hf/gsap.min.js and hf/fonts (Hind, Yatra One) copied locally. Note: Yatra One drops the anusvara in Chrome, use Hind for words like घंटे.
