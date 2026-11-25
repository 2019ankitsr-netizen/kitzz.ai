import json, sys, os, numpy as np, soundfile as sf
from tts import say
name, voice = sys.argv[1], sys.argv[2]; speed=float(sys.argv[3]) if len(sys.argv)>3 else 1.05
L=json.load(open(f'{name}/lines.json')); gap=json.load(open(f'{name}/gaps.json')) if os.path.exists(f'{name}/gaps.json') else {}
os.makedirs(f'vo/{name}',exist_ok=True)
for l in L:
    a=say(l['tts'],voice,speed)
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-600):idx[-1]+2400]
    sf.write(f"vo/{name}/{l['id']}.wav",a,24000); l['dur']=round(len(a)/24000,2)
t=0.15; S={}
for i,l in enumerate(L):
    if i: t+=gap.get(l['id'],0.35)
    l['start']=round(t,2); S[l['id']]=l['start']; t+=l['dur']
end=round(t+0.4,2)
json.dump({'lines':L,'S':S,'end':end},open(f'web/{name}_timeline.json','w'),ensure_ascii=False,indent=1)
print(S,end)
