import sys, numpy as np
from PIL import Image, ImageDraw
import scenes
from scenes import *
ts = [float(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [START[i] + D[i]*f for i in range(len(D)) for f in (0.35, 0.9)]
ims = []
for t in ts:
    a = frame(t); im = Image.fromarray(np.ascontiguousarray(a))
    d = ImageDraw.Draw(im, 'RGBA'); d.rectangle([0,0,W,269], fill=(255,0,0,50)); d.rectangle([0,1248,W,H], fill=(255,0,0,50))
    d.rectangle([0,0,65,H], fill=(255,0,0,50)); d.rectangle([W-65,0,W,H], fill=(255,0,0,50)); d.rectangle([930,900,W,1700], fill=(255,180,0,60))
    d.text((80, 1260), f"{t:.1f}", fill=(0,0,0))
    ims.append(im.resize((270, 480)))
cols = 6; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (270 * cols, 480 * rows), 'white')
for j, im in enumerate(ims): sheet.paste(im, ((j % cols) * 270, (j // cols) * 480))
sheet.save('sheet.png'); print(TOT)
