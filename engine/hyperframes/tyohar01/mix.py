import numpy as np, wave, json
SR=44100; TL=json.load(open("timeline.json")); L=TL["lines"]; T=TL["total"]; N=int(T*SR); rng=np.random.default_rng(7)
tt=lambda d: np.arange(int(d*SR))/SR
def place(b,x,at):
    i=int(at*SR); j=min(N,i+len(x)); b[i:j]+=x[:j-i]
mus=np.zeros(N); sfx=np.zeros(N)
f0=130.81  # D3 drone, tanpura-like
t=np.arange(N)/SR
for h,g in [(1,.5),(1.5,.25),(2,.35),(3,.12),(4,.08)]: mus+=g*np.sin(2*np.pi*f0*h*t+np.sin(2*np.pi*.2*t*h))
mus*= (0.6+0.4*np.sin(2*np.pi*t/2.4)**2)*0.05
def bell(m,g=.06):
    f=440*2**((m-69)/12); x=tt(1.2); return (np.sin(2*np.pi*f*x)+.4*np.sin(2*np.pi*f*2.76*x))*np.exp(-x*4)*g
scale=[62,64,66,69,71,74,76]; beat=60/96
k=0; a=0.6
while a<T-1:
    if k%2==0: place(mus,bell(scale[(k*3)%7],.035),a)
    tab=tt(.25); place(mus,np.sin(2*np.pi*(90+60*np.exp(-tab*30))*tab)*np.exp(-tab*12)*(.12 if k%4==0 else .05),a)
    a+=beat; k+=1
def whoosh(at,g=.06):
    x=tt(.4); n=np.convolve(rng.standard_normal(len(x)),np.ones(10)/10,'same'); place(sfx,n*np.sin(np.linspace(0,np.pi,len(x)))**2*g,at)
def chime(at,g=.08):
    for j,m in enumerate([74,78,81]): place(sfx,bell(m,g),at+j*.07)
place(sfx, (lambda x: np.sin(2*np.pi*(120-60*x)*x)*np.exp(-x*8)*.25)(tt(.4)), .05)
for i in range(1,len(L)): whoosh(L[i]["start"]-.3)
chime(L[1]["start"]+.2); chime(L[-1]["start"]+.1,.1)
with wave.open("vo.wav") as w: vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32767; vsr=w.getframerate()
vo=np.interp(np.arange(int(len(vo)*SR/vsr))/SR,np.arange(len(vo))/vsr,vo); vox=np.zeros(N); vox[:min(N,len(vo))]=vo[:N]
env=np.convolve(np.abs(vox)>.02,np.ones(int(.25*SR))/int(.25*SR),'same'); mix=mus*(1-.45*np.clip(env*3,0,1))+sfx+vox
fade=int(1.2*SR); mix[-fade:]*=np.linspace(1,0,fade); mix=mix/np.abs(mix).max()*.9
st=np.stack([mix,mix],1)
with wave.open("mix.wav","wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
