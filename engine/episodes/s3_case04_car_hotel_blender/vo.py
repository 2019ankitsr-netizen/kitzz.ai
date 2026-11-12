import sys; sys.path.insert(0, '/home/claude/bk'); from kit import make_voice
D, E = 'am_fenrir', 'bf_emma'
def DL(key, say, cap=None, **k): return dict(key=key, voice=D, say=say, cap=cap, speed=k.pop('speed', 1.0), pitch=k.pop('pitch', -0.5), **k)
def EL(key, say, cap=None, **k): return dict(key=key, voice=E, say=say, cap=cap, speed=1.0, **k)
LINES = [
 DL('hook', "He pushed his car to a hotel. | And instantly, he was bankrupt.", "He pushed his car to a hotel. And instantly, he was bankrupt.", speed=1.05, gap=0.25),
 EL('solved', "Case three, solved.", gap=0.2),
 DL('ans', "The surgeon was the boy's mother. | Most people picture a man. | That's the trap."),
 EL('log', "C C T V log. | Camera two. | Hotel car park. | Twenty-three ten.", "CCTV log · Cam 02 · Hotel car park · 23:10", gap=0.3),
 DL('setup', "A man pushes his car, by hand, all the way to the front of a hotel."),
 DL('stop', "He stops. | Looks at the owner. | And says: | I'm bankrupt."),
 DL('ask', "No crash. No theft. No one else touched the car. | So what happened?", speed=0.97, pitch=-0.8),
 DL('clue', "Clue. | The hotel is red. | And the whole town fits on a table.", pre=0.3, pitch=0.5),
 DL('cta', "Answer in the comments. | And send it to the friend who always wins at Business.", gap=0.25),
 DL('loop', "He pushed his car to a hotel. | Why?", gap=0.1),
]
make_voice('/home/claude/s3', LINES, lead=0.1, tail=0.5)
