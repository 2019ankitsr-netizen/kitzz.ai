"""python3 ../tyohar_kit/tts.py [voice] [speed]  (run inside an episode folder with episode.py defining LINES)"""
import sys, json, importlib.util, soundfile as sf
sys.path.insert(0, '/home/claude/kitzz.ai/engine')
from audio import say
spec = importlib.util.spec_from_file_location('episode', 'episode.py'); ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
voice = sys.argv[1] if len(sys.argv) > 1 else 'hm_omega'; sp = float(sys.argv[2]) if len(sys.argv) > 2 else 1.05
durs = []
for i, t in enumerate(ep.LINES):
    a = say(t, voice, speed=sp, lang='hi'); sf.write(f'v{i}.wav', a, 24000); durs.append(len(a) / 24000)
json.dump(durs, open('durs.json', 'w')); print([round(d, 2) for d in durs], round(sum(durs), 1))
