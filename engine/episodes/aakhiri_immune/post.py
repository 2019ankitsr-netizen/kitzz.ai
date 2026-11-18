import numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt, fftconvolve
rng=np.random.default_rng(3); SR=48000
def breath(dur=0.45, inhale=True):
    n=int(dur*SR); x=rng.normal(0,1,n)
    sos=butter(2,[500,3500],btype='band',fs=SR,output='sos'); x=sosfilt(sos,x)
    e=np.sin(np.linspace(0,np.pi,n))**(1.5 if inhale else 0.8)
    if not inhale: e*=np.linspace(1,0.3,n)
    return (x*e/np.abs(x).max()*0.05).astype(np.float32)
ir_n=int(0.35*SR); ir=rng.normal(0,1,ir_n)*np.exp(-np.arange(ir_n)/SR*14); ir[0]=0; ir/=np.abs(ir).sum()*0.6
hp=butter(2,90,btype='high',fs=SR,output='sos'); pres=butter(2,[2500,5000],btype='band',fs=SR,output='sos')
BREATH_BEFORE={3:0.4,4:0.5,6:0.45,7:0.5,8:0.55}
for i in range(1,9):
    a,sr=sf.read(f'../xtts/pc_{i}.wav',dtype='float32'); a=resample_poly(a,SR,sr).astype(np.float32)
    # trim leading/trailing silence
    th=0.01*np.abs(a).max(); idx=np.where(np.abs(a)>th)[0]; a=a[max(0,idx[0]-1200):idx[-1]+4800]
    t=np.arange(len(a))/SR
    trem=1+0.06*np.sin(2*np.pi*5.5*t+rng.uniform(0,6))*(0.6+0.4*np.sin(2*np.pi*0.7*t))
    a=a*trem
    a=sosfilt(hp,a)+0.25*sosfilt(pres,a)
    wet=fftconvolve(a,ir)[:len(a)]; a=a*0.9+wet*0.12
    a=a/np.abs(a).max()*0.85
    lead=np.zeros(int(0.05*SR),np.float32)
    if i in BREATH_BEFORE:
        b=breath(BREATH_BEFORE[i]); lead=np.concatenate([b,np.zeros(int(0.08*SR),np.float32)])
    out=np.concatenate([lead,a.astype(np.float32)])
    if i in (4,8): out=np.concatenate([out,breath(0.5,False)])
    sf.write(f'vo2/{i}_48.wav',out,SR,subtype='PCM_16'); print(i,round(len(out)/SR,2))
