import sys; sys.path.insert(0, '/home/claude/bk'); from kit import make_voice
V = 'af_heart'
LINES = [
 dict(key='hook', voice=V, say="Honey can last three thousand years.", cap="Honey can last 3,000 years.", gap=0.2),
 dict(key='tomb', voice=V, say="Archaeologists found pots of it in ancient Egyptian tombs. | Still edible."),
 dict(key='water', voice=V, say="Here's why. | Honey is only about seventeen percent water. | Germs that land in it get the water sucked right out of them.", cap="Here's why. Honey is only about 17% water. Germs that land in it get the water sucked right out of them."),
 dict(key='acid', voice=V, say="It's also acidic. | Roughly as sour as orange juice.", pre=0.05),
 dict(key='bee', voice=V, say="And bees add an enzyme that slowly makes hydrogen peroxide. | A built-in germ killer."),
 dict(key='crystal', voice=V, say="So if your honey turns hard and cloudy? | It hasn't gone bad. | It's just crystallised. | Warm the jar in hot water.", cap="So if your honey turns hard and cloudy? It hasn't gone bad. It's just crystallised. Warm the jar in hot water."),
 dict(key='cta', voice=V, say="Send this to the friend who threw theirs away. | Because remember,", cap="Send this to the friend who threw theirs away. Because remember…", gap=0.1),
]
make_voice('/home/claude/s4', LINES, lead=0.1, tail=0.5)
