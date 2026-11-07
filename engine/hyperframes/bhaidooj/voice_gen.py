"""Natural voices for each line via the engine's Parler backend (Rohit narrator, Divya = Yamuna, Aman = Yamraj)."""
import json, sys, soundfile as sf
sys.path.insert(0, "/home/claude/kitzz.ai/engine")
import audio as A
G = "/home/claude/work/bd"; lines = json.load(open(f"{G}/lines.json")); out = []
for i, L in enumerate(lines):
    a = A.say_parler(L["hi"], L["spk"], L["mood"], seed=7)
    sf.write(f"{G}/line_{i:02d}.wav", a, A.SR); out.append(dict(i=i, dur=len(a) / A.SR)); print(i, round(len(a) / A.SR, 1), flush=True)
json.dump(dict(sr=A.SR, lines=out), open(f"{G}/voice_meta.json", "w")); print("DONE")
