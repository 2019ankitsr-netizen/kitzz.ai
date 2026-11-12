import sys; sys.path.insert(0, '/home/claude/bk'); from kit import make_voice
V = 'af_heart'
LINES = [
 dict(key='hook', voice=V, say="Every banana you eat is radioactive.", gap=0.2),
 dict(key='why', voice=V, say="Bananas are full of potassium. | And a tiny bit of natural potassium is radioactive. | It's called potassium forty.", cap="Bananas are full of potassium. And a tiny bit of natural potassium is radioactive. It's called potassium-40."),
 dict(key='dose', voice=V, say="One banana gives you about a tenth of a micro see-vert.", cap="One banana gives you about 0.1 microsieverts."),
 dict(key='xray', voice=V, say="A dental X-ray? | About fifty bananas.", cap="A dental X-ray? About 50 bananas.", pre=0.1),
 dict(key='safe', voice=V, say="And it doesn't build up. | Your body keeps its potassium steady, and flushes out the extra."),
 dict(key='unit', voice=V, say="Scientists even joke about it as a unit. | The banana equivalent dose.", cap="Scientists even joke about it as a unit: the Banana Equivalent Dose."),
 dict(key='cta', voice=V, say="Send this to the friend who eats three a day. | Because remember,", cap="Send this to the friend who eats three a day. Because remember…", gap=0.1),
]
make_voice('/home/claude/s4', LINES, lead=0.1, tail=0.5)
