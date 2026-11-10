import numpy as np, wave, json
SR=44100; TL=json.load(open("timeline.json")); L=TL["lines"]; T=TL["total"]+0.6; N=int(T*SR); rng=np.random.default_rng(3)
tt=lambda d: np.arange(int(d*SR))/SR
def place(b,x,at):
    i=int(max(0,at)*SR); j=min(N,i+len(x)); b[i:j]+=x[:j-i]
t=np.arange(N)/SR; mus=np.zeros(N); sfx=np.zeros(N)
# low tanpura drone (Sa-Pa) with slow swell + soft shehnai-like pad entering mid
for f,g in [(110,.5),(165,.28),(220,.3),(330,.1)]: mus+=g*np.sin(2*np.pi*f*t+0.6*np.sin(2*np.pi*.15*t))
mus*=0.045*(0.7+0.3*np.sin(2*np.pi*t/3.2)**2)
def drum(at,g):  # dholak-ish
    x=tt(.35); place(mus,np.sin(2*np.pi*(70+90*np.exp(-x*25))*x)*np.exp(-x*9)*g,at)
beat=60/80
for k in range(int(T/beat)):
    a=k*beat
    if 10<a<T-2: drum(a,.10 if k%4==0 else .04)
def boom(at,g=.4): x=tt(1.6); place(sfx,np.sin(2*np.pi*(45+30*np.exp(-x*4))*x)*np.exp(-x*2.5)*g,at)
def whoosh(at,g=.07):
    x=tt(.5); n=np.convolve(rng.standard_normal(len(x)),np.ones(14)/14,'same'); place(sfx,n*np.sin(np.linspace(0,np.pi,len(x)))**2*g,at)
def bell(at,f=880,g=.08): x=tt(2.0); place(sfx,(np.sin(2*np.pi*f*x)+.4*np.sin(2*np.pi*f*2.76*x))*np.exp(-x*2.2)*g,at)
def crash(at,g=.35):
    x=tt(.9); n=rng.standard_normal(len(x)); place(sfx,np.convolve(n,np.ones(6)/6,'same')*np.exp(-x*5)*g,at); boom(at,.3)
s=lambda i:L[i]["start"]; e=lambda i:L[i]["end"]; kw=lambda i,f:s(i)+(e(i)-s(i))*f
bell(0.1,660,.1); whoosh(0.0,.1)   # curtain
for i in [2,3,4,6,7,8,9,10,11,12,13]: whoosh(s(i)-.35)
boom(s(2)-.1,.45); boom(s(5)-.1,.5); crash(kw(6,.25)+.55)
bell(kw(7,.84),1047,.07); bell(kw(7,.84)+.15,1319,.06)
boom(s(8),.45)
for k in range(4): bell(kw(9,.42+k*.1),784+k*100,.05)
crash(kw(9,.86)+.17,.4); crash(kw(9,.86)+.6,.35)
bell(kw(10,.5),523,.1); bell(kw(10,.5)+.2,659,.08); bell(kw(10,.5)+.4,784,.08)
whoosh(T-1.0,.1)
with wave.open("vo.wav") as w: vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32767; vsr=w.getframerate()
vo=np.interp(np.arange(int(len(vo)*SR/vsr))/SR,np.arange(len(vo))/vsr,vo); vox=np.zeros(N); vox[:min(N,len(vo))]=vo[:N]
env=np.convolve(np.abs(vox)>.02,np.ones(int(.3*SR))/int(.3*SR),'same'); mix=mus*(1-.4*np.clip(env*3,0,1))+sfx+vox
fade=int(1.5*SR); mix[-fade:]*=np.linspace(1,0,fade); mix=mix/np.abs(mix).max()*.9
with wave.open("mix.wav","wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([mix,mix],1)*32767).astype(np.int16).tobytes())
print("mixed",T)
