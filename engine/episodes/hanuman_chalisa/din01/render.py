import sys, subprocess, numpy as np
from scenes import frame, TOT
part, nparts = int(sys.argv[1]), int(sys.argv[2])
n = int(TOT * 30); a, b = n * part // nparts, n * (part + 1) // nparts
p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30', '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', f'part{part}.mp4'], stdin=subprocess.PIPE)
for f in range(a, b): p.stdin.write(np.ascontiguousarray(frame(f / 30)).tobytes())
p.stdin.close(); p.wait(); print('done', part)
