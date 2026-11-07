"""Bhai Dooj story: timings -> timings.js + index.html (HyperFrames) -> render -> mix voice + music + sfx -> mux."""
import json, os, subprocess, sys, random, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/kitzz.ai/engine")
import audio as A
from reel import Reel

G = "/home/claude/work/bd"; HF = f"{G}/hf"
lines = json.load(open(f"{G}/lines.json"))
LEAD = .3; GAP = {"hook": .35, "call": .3, "busy": .3, "arrive": .3, "tilak": .55, "ask": .25, "boon": .3, "tathastu": .45, "name": .35}
t = LEAD; T = dict(lines=[], at={}, idx={}); voice = np.zeros(0, np.float32)
for i, L in enumerate(lines):
    a, sr = sf.read(f"{G}/line_{i:02d}.wav", dtype="float32"); assert sr == A.SR
    if L["tag"] == "tilak": t += .2
    start = t; dur = len(a) / A.SR
    T["lines"].append(dict(t0=round(start, 3), dur=round(dur, 3), who=L.get("who", ""))); T["at"][L["tag"]] = round(start, 3); T["idx"][L["tag"]] = i
    voice = np.concatenate([voice, np.zeros(max(0, int((start - len(voice) / A.SR) * A.SR)), np.float32), a])
    t = start + dur + GAP.get(L["tag"], .25)
    if L["tag"] == "tilak": t += 1.4      # room for the close-up tilak moment
DUR = round(t + 3.6, 2)
voice = np.concatenate([voice, np.zeros(int(DUR * A.SR) - len(voice), np.float32)])
open(f"{HF}/timings.js", "w").write(f"window.T = {json.dumps(T)}; window.DUR = {DUR};")

r = random.Random(5)
stars = "".join(f'<circle cx="{r.uniform(20, 1060):.0f}" cy="{r.uniform(40, 760):.0f}" r="{r.choice([1.5, 2, 2.5, 3]):.1f}" fill="#fff6dc"/>' for _ in range(70))
waves = "".join(f'<path d="M{x} {y} q15 -8 30 0 t30 0"/>' for x in range(-200, 1400, 90) for y in (942, 968, 990))
sparks = "".join(f'<circle cx="{r.uniform(100, 980):.0f}" cy="{r.uniform(900, 1060):.0f}" r="{r.uniform(2, 4):.1f}" fill="#ffd36b"/>' for _ in range(26))
petals = "".join(f'<use href="#petal" x="{r.uniform(40, 1040):.0f}" y="{r.uniform(-400, 600):.0f}" transform="rotate({r.uniform(-40, 40):.0f} {r.uniform(40, 1040):.0f} 0)"/>' for _ in range(60))
years = "".join(f'<div class="yn">{n}</div>' for n in (1, 2, 3, 5, 7, 10, 12, 15, 20, 25))
def cap(L, i):
    txt = L["en"]; kw = L.get("kw")
    if kw and kw in txt: txt = txt.replace(kw, f"<b>{kw}</b>", 1)
    who = f'<span class="who {L["who"]}">{L["who"]}</span><br/>' if L.get("who") else ""
    return f'<div class="cap" id="cap{i}">{who}<span class="box">{txt}</span></div>'
html = open(f"{HF}/index.tpl.html").read()
for k, v in {"{{DUR}}": str(DUR), "{{STARS}}": stars, "{{WAVES}}": waves, "{{SPARKS}}": sparks, "{{PETALS}}": petals, "{{YEARS}}": years,
             "{{CAPS}}": "\n".join(cap(L, i) for i, L in enumerate(lines))}.items():
    html = html.replace(k, v)
open(f"{HF}/index.html", "w").write(html)
print("DUR", DUR, T["at"])
if "--no-render" in sys.argv: sys.exit()

env = dict(os.environ, HYPERFRAMES_BROWSER_PATH="/usr/bin/google-chrome")
subprocess.run(["npx", "-y", "hyperframes@0.9.20", "render", HF, "-o", f"{G}/bd_v.mp4", "-q", "looks", "-w", "2", "--fps", "30"], env=env, check=True)
R = Reel("BhaiDooj_Story", "festive", [], tone="warm", seed=21); R.dur = DUR; R.voice = voice
a = T["at"]
R.events = [(.05, "whoosh"), (1.4, "chime"), (a["arrive"], "whoosh"), (a["tilak"] + 1.4, "whoosh"), (a["tilak"] + 1.8, "pop"),
            (a["boon"] + .5, "chime"), (a["tathastu"] + .2, "hit"), (a["name"] + .1, "chime"), (a["cta"], "pop")]
R.mix(f"{G}/bd_mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{G}/bd_v.mp4", "-i", f"{G}/bd_mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", f"{G}/BhaiDooj_Story.mp4"], check=True)
print("OUT", f"{G}/BhaiDooj_Story.mp4", "LUFS", A.lufs(f"{G}/bd_mix.wav"))
