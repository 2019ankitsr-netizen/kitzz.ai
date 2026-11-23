"""Run inside an episode folder: python3 ../tyohar_kit/build.py <OutName>  (after tts.py). Renders, mixes, -14 LUFS, safe-zone contact sheet."""
import sys, subprocess, importlib.util, os
sys.path.insert(0, '/home/claude/kitzz.ai/engine/episodes/tyohar_kit')
import kit, skia
from PIL import Image, ImageDraw
out = sys.argv[1]; K = '/home/claude/kitzz.ai/engine/episodes/tyohar_kit'
spec = importlib.util.spec_from_file_location('episode', 'episode.py'); ep = importlib.util.module_from_spec(spec); spec.loader.exec_module(ep)
kit.init('durs.json', ep.CAPS, ep.SCENES)
n = len(kit.D)
procs = [subprocess.Popen([sys.executable, 'episode.py', 'render', str(i)]) for i in range(n)]
for p in procs: p.wait()
subprocess.run([sys.executable, f'{K}/audio.py'], check=True)
open('list.txt', 'w').write(''.join(f"file 'sc{i}.mp4'\n" for i in range(n)))
R = lambda *a: subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
R('-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'video.mp4')
R('-i', 'mix.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', 'mixn.wav')
R('-i', 'video.mp4', '-i', 'mixn.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', f'{out}.mp4')
# caption-box safe-zone check
kit.CAP_BOXES.clear(); cv = skia.Surface(10, 10).getCanvas()
for i in range(n):
    for f in range(0, int(kit.D[i] * 30), 5): kit.draw_caption(cv, i, f / 30)
bad = [b for b in kit.CAP_BOXES if b[0] < 65 or b[2] > 920 or b[1] < 269 or b[3] > 1248]
print('duration', round(kit.TOT, 1), 'caption boxes out of zone:', len(bad))
ts = [0.6, 2.0] + [kit.START[i] + kit.D[i] * 0.7 for i in range(1, n)] + [kit.NUDGE_AT + 0.6, kit.TOT - 1.0]
ims = []
for t in ts:
    R('-ss', f'{t:.2f}', '-i', f'{out}.mp4', '-frames:v', '1', 'f.png')
    im = Image.open('f.png').convert('RGB').resize((270, 480)); d = ImageDraw.Draw(im, 'RGBA'); s = 0.25
    d.rectangle([0, 0, 270, 269 * s], fill=(255, 0, 0, 60)); d.rectangle([0, 1248 * s, 270, 480], fill=(255, 0, 0, 60))
    d.rectangle([0, 0, 65 * s, 480], fill=(255, 0, 0, 60)); d.rectangle([270 - 65 * s, 0, 270, 480], fill=(255, 0, 0, 60)); d.rectangle([930 * s, 900 * s, 270, 1700 * s], fill=(255, 170, 0, 70))
    d.text((5, 462), f'{t:.1f}s', fill='black'); ims.append(im)
cols = 6; rows = (len(ims) + cols - 1) // cols
sh = Image.new('RGB', (270 * cols, 480 * rows), 'white')
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 270, (i // cols) * 480))
sh.save('contact_safezone.png')
print(subprocess.run(['ffmpeg', '-i', f'{out}.mp4', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr.split('Integrated loudness:')[-1].split('\n')[1].strip())
