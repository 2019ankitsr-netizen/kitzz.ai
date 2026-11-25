import sys,glob
from PIL import Image,ImageDraw
fs=sorted(glob.glob(sys.argv[1]+'/*.jpg'));cols=int(sys.argv[3]) if len(sys.argv)>3 else 5
tw,th=324,576;rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(cols*tw,rows*th),'gray')
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGBA');ov=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(ov)
    d.rectangle([0,0,1080,269],fill=(255,0,0,50));d.rectangle([0,1248,1080,1920],fill=(255,0,0,50))
    d.rectangle([0,0,65,1920],fill=(255,0,0,50));d.rectangle([1015,0,1080,1920],fill=(255,0,0,50))
    d.rectangle([930,900,1080,1700],fill=(255,180,0,60))
    im=Image.alpha_composite(im,ov).convert('RGB').resize((tw,th))
    ImageDraw.Draw(im).text((6,6),f.split('/')[-1],fill='yellow')
    S.paste(im,((i%cols)*tw,(i//cols)*th))
S.save(sys.argv[2])
