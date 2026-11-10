import sys, json, subprocess, os, time
from playwright.sync_api import sync_playwright
# usage: shoot.py stills t1,t2,...   |   shoot.py seg f0 f1 out.mp4
mode = sys.argv[1]
vo = json.load(open('/home/claude/anar/vo.json'))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--no-sandbox'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('console', lambda m: print('console:', m.text, file=sys.stderr) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: print('pageerror:', e, file=sys.stderr))
    pg.goto('http://localhost:8766/index.html')
    pg.wait_for_function('window.READY===true', timeout=60000)
    caps = pg.evaluate('()=>window.setCaps()'); times = pg.evaluate('()=>window.TIMES')
    if mode == 'stills':
        print(caps); print(times)
        for t in sys.argv[2].split(','):
            t0 = time.time(); pg.evaluate('t=>window.setTime(t)', float(t))
            pg.screenshot(path=f'/home/claude/anar/stills/s_{float(t):05.2f}.jpg', type='jpeg', quality=85)
            print(t, round(time.time()-t0, 2))
    else:
        f0, f1, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        tmp = out.replace('.mp4', '.tmp.mp4')
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', tmp], stdin=subprocess.PIPE)
        for f in range(f0, f1):
            pg.evaluate('t=>window.setTime(t)', f/30)
            ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close()
        if ff.wait() == 0: os.rename(tmp, out); print('done', out)
    b.close()
