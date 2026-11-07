"""Assemble narration timings, write timings.js + index.html for HyperFrames, render, then mix voice + music + sfx and mux."""
import json, os, subprocess, sys, random, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/kitzz.ai/engine")
import audio as A
from reel import Reel

G = "/home/claude/work/gov"; HF = f"{G}/hf"
lines = json.load(open(f"{G}/lines.json")); meta = json.load(open(f"{G}/voice_meta.json")); SR_V = meta["sr"]
LEAD, GAP = .35, {"hook": .35, "krishna": .3, "storm": .2, "lift": .45, "days": .3, "end": .3, "annakut": .35}
t = LEAD; T = dict(lines=[], at={}, idx={}); parts = []
voice = np.zeros(0, dtype=np.float32)
for i, L in enumerate(lines):
    a, sr = sf.read(f"{G}/line_{i:02d}.wav", dtype="float32")
    if sr != A.SR:
        import librosa; a = librosa.resample(a, orig_sr=sr, target_sr=A.SR)
    start = t; dur = len(a) / A.SR
    T["lines"].append(dict(t0=round(start, 3), dur=round(dur, 3))); T["at"][L["tag"]] = round(start, 3); T["idx"][L["tag"]] = i
    pad = int((start - len(voice) / A.SR) * A.SR); voice = np.concatenate([voice, np.zeros(max(0, pad), np.float32), a])
    t = start + dur + GAP.get(L["tag"], .25)
DUR = round(t + 3.6, 2)   # time for the CTA card after the last line
voice = np.concatenate([voice, np.zeros(int(DUR * A.SR) - len(voice), np.float32)])
open(f"{HF}/timings.js", "w").write(f"window.T = {json.dumps(T)}; window.DUR = {DUR};")

r = random.Random(3); rain = "".join(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 10:.0f}" y2="{y + 46:.0f}" stroke="#bcd0ff" stroke-width="3" stroke-opacity=".7"/>'
                                    for x, y in ((r.uniform(0, 1100), r.uniform(-240, 1900)) for _ in range(230)))
days = "".join(f'<div class="dn num" id="d{k}">{k}</div>' for k in range(1, 8))
def cap(L, i):
    txt = L["en"]; kw = L.get("kw")
    if kw and kw in txt: txt = txt.replace(kw, f"<b>{kw}</b>", 1)
    return f'<div class="cap" id="cap{i}"><span class="box">{txt}</span></div>'
html = open(f"{HF}/index.tpl.html").read().replace("{{DUR}}", str(DUR)).replace("{{RAIN}}", rain).replace("{{DAYS}}", days) \
    .replace("{{CAPS}}", "\n".join(cap(L, i) for i, L in enumerate(lines)))
open(f"{HF}/index.html", "w").write(html)
print("DUR", DUR, "timings", T["at"])
if "--no-render" in sys.argv: sys.exit()

env = dict(os.environ, HYPERFRAMES_BROWSER_PATH="/usr/bin/google-chrome")
subprocess.run(["npx", "-y", "hyperframes@0.9.20", "render", HF, "-o", f"{G}/gov_v.mp4", "-q", "looks", "-w", "2", "--fps", "30"], env=env, check=True)

R = Reel("Govardhan_Story", "festive", [], tone="warm", seed=11)
R.dur = DUR; R.voice = voice
R.events = [(T["at"]["hook"] - .05, "whoosh"), (T["at"]["storm"], "hit"), (T["at"]["lift"] + 1.3, "hit"), (T["at"]["end"] + .3, "chime"),
            (T["at"]["annakut"] + .6, "pop"), (T["at"]["cta"], "pop")] + [(T["at"]["storm"] + d, "static") for d in (.9, 2.1, 3.4)]
R.mix(f"{G}/gov_mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{G}/gov_v.mp4", "-i", f"{G}/gov_mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", f"{G}/Govardhan_Story.mp4"], check=True)
print("OUT", f"{G}/Govardhan_Story.mp4", "LUFS", A.lufs(f"{G}/gov_mix.wav"))
