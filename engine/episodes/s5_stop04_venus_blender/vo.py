import sys; sys.path.insert(0, '/home/claude/bk'); from kit import make_voice
M, E = 'am_michael', 'bf_emma'
LINES = [
 dict(key='hook', voice=E, say="Next stop! | Venus.", cap="Next stop: Venus.", speed=1.05, gap=0.25),
 dict(key='intro', voice=M, say="The brightest planet in our night sky. | And the hottest one in the solar system.", speed=1.0),
 dict(key='day', voice=M, say="Fact. | Venus spins so slowly, that one turn takes two hundred and forty three Earth days. | Longer than its whole year.", cap="FACT: Venus spins so slowly that one turn takes 243 Earth days. Longer than its whole year.", speed=1.02),
 dict(key='west', voice=M, say="Fact. | It spins backwards. | So the Sun rises in the west.", cap="FACT: It spins backwards. So the Sun rises in the west.", speed=1.0),
 dict(key='hot', voice=M, say="Fact. | Its thick air traps the heat. | The ground is around four hundred and sixty five degrees. | Hot enough to melt lead.", cap="FACT: Its thick air traps the heat. The ground is around 465°C. Hot enough to melt lead.", speed=1.02),
 dict(key='press', voice=M, say="Standing there, the air would press on you like nine hundred metres of ocean.", cap="Standing there, the air would press on you like 900 metres of ocean.", speed=1.02),
 dict(key='imagine', voice=M, say="Imagine. | A sunrise in the west, | and about two months until sunset.", cap="IMAGINE: a sunrise in the west, and about two months until sunset.", speed=1.0),
 dict(key='next', voice=E, say="Next stop! | Jupiter.", cap="Next stop: Jupiter.", speed=1.05, gap=0.2),
 dict(key='cta', voice=M, say="Save this ride. | And tag who you'd send to Venus.", tone='bright', gap=0.1),
]
make_voice('/home/claude/s5', LINES, lead=0.1, tail=0.6)
