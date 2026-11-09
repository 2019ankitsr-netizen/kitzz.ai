import soundfile as sf, numpy as np, json, sys
from kokoro import KPipeline
p=KPipeline(lang_code='h')
L=[
"दिवाली के बाद, कलम क्यों रख दी जाती है?",
"मान्यता है, ब्रह्मा जी की काया से प्रकट हुए, हाथ में कलम-दवात लिए, भगवान चित्रगुप्त।",
"यमराज के दरबार में, हर इंसान के कर्मों का लेखा-जोखा, यही रखते हैं।",
"इसीलिए कायस्थ परिवार, पूजा होने तक, कलम और बही को आराम देते हैं।",
"इस साल चित्रगुप्त पूजा है, बुधवार, ग्यारह नवंबर, भाई दूज के दिन।",
"पूजा में रखिए, नई कलम, दवात, कोरा कागज़ और बही।",
"तिलक लगाइए, फूल, अक्षत, और दीया चढ़ाइए।",
"फिर नई कलम से लिखिए, ओम् चित्रगुप्ताय नमः।",
"ये रील अपने कायस्थ दोस्त को भेजिए, और सेव कीजिए। क्योंकि पूजा के बाद ही, फिर कलम चलती है।",
]
voice=sys.argv[1]; sp=float(sys.argv[2])
durs=[]
for i,t in enumerate(L):
    a=np.concatenate([np.asarray(r[2]) for r in p(t,voice=voice,speed=sp)])
    sf.write(f'v{i}.wav',a,24000); durs.append(len(a)/24000)
json.dump(durs,open('durs.json','w')); print([round(d,2) for d in durs], round(sum(durs),1))
