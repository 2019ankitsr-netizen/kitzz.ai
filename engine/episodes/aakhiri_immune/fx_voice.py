import sys, numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt, fftconvolve
SR=48000; rng=np.random.default_rng(8)
src,dst,mode=sys.argv[1:4]
a,sr=sf.read(src,dtype='float32'); a=resample_poly(a,SR,sr)
if mode=='room':
    a=sosfilt(butter(2,100,btype='high',fs=SR,output='sos'),a)
    n=int(0.3*SR); ir=rng.normal(0,1,n)*np.exp(-np.arange(n)/SR*16); ir/=np.abs(ir).sum()*0.6
    a=a*0.9+fftconvolve(a,ir)[:len(a)]*0.12; lead=0.1
elif mode=='megaphone':
    a=sosfilt(butter(4,[500,2600],btype='band',fs=SR,output='sos'),a); a=np.tanh(a/np.abs(a).max()*3.0)
    d=int(0.12*SR); e=np.zeros(len(a)+d); e[:len(a)]+=a; e[d:]+=a*0.35; a=e; lead=0.5
    fb=np.sin(2*np.pi*1800*np.arange(int(0.35*SR))/SR)*np.linspace(0.3,0,int(0.35*SR))
    a=np.concatenate([fb,np.zeros(int(0.15*SR)),a])
out=np.concatenate([np.zeros(int(lead*SR)),a]); out=out/np.abs(out).max()*0.8
sf.write(dst,out.astype(np.float32),SR,subtype='PCM_16')
