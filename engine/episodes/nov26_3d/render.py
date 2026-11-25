import asyncio, sys, json, subprocess, os, time
from playwright.async_api import async_playwright
FPS=30
PAGE=os.environ.get('PAGE','index.html')
async def worker(idx, n, frames, out, port):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        msgs=[]; pg.on('console',lambda m: msgs.append(m.text)); pg.on('pageerror',lambda e: print('ERR',e,flush=True))
        await pg.goto(f'http://localhost:{port}/'+PAGE); 
        await pg.wait_for_function('window.READY===true',timeout=60000)
        await pg.evaluate('document.fonts.ready')
        for i in frames[idx::n]:
            t=i/FPS
            await pg.evaluate(f'window.seek({t})')
            await pg.screenshot(path=f'{out}/f{i:05d}.jpg',type='jpeg',quality=93)
        for m in msgs[:5]: print('console',m)
        await b.close()
async def main():
    out=sys.argv[1]; frames=eval(sys.argv[2]); n=int(sys.argv[3]) if len(sys.argv)>3 else 2
    os.makedirs(out,exist_ok=True)
    await asyncio.gather(*[worker(k,n,frames,out,8765) for k in range(n)])
asyncio.run(main())
