import asyncio,sys
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page(viewport={'width':1080,'height':1920}); await pg.goto('http://localhost:8765/'+__import__('os').environ.get('PAGE','index.html')); await pg.wait_for_function('window.READY===true')
    print(await pg.evaluate(sys.argv[1])); await b.close()
asyncio.run(m())
