import json, random
from figs import *
TL = json.load(open("timeline.json")); L = TL["lines"]; DUR = TL["total"] + 0.6
r = random.Random(5)
SC = [(0, 1), (2, 2), (3, 3), (4, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13)]
def ground(col="#8a5a2b"): return f'<path d="M0 1180 L1080 1180 L1080 1920 L0 1920Z" fill="{col}"/><path d="M0 1180 L1080 1180" stroke="#5e3a18" stroke-width="6"/>'
def village_bg(sky="#f6d79a"):
    return f'<rect width="1080" height="1920" fill="{sky}"/><circle cx="820" cy="560" r="220" fill="#fff3c4" opacity=".55"/>' + banana(120, 1180, 1.2) + banana(960, 1180, 1.1, -1) + hut(560, 1180, 1.25)
P = lambda body, s=1.0, x=0, y=0, extra="": f'<g transform="translate({x} {y}) scale({s})" filter="url(#pp)" {extra}>{body}</g>'
scenes = {}
# 0 hook: dark stage, spotlight, sister with thorn
scenes[0] = f'''<g class="bg"><rect width="1080" height="1920" fill="#1a0d12"/><ellipse cx="540" cy="1200" rx="360" ry="70" fill="#f6c46a" opacity=".25"/></g>
<g class="mid">{P(woman(face="sad", tear=True), 1.25, 540, 1210)}</g>
<g class="fg"><g id="thorn" opacity="0" transform="translate(700 700)"><path d="M0 0 L160 -120" stroke="#5b4a2a" stroke-width="12" stroke-linecap="round"/>{''.join(f'<path d="M{20+i*28} {-15-i*21} l-8 -26 l18 14Z" fill="#7a6a3a"/>' for i in range(5))}<circle cx="164" cy="-124" r="10" fill="#c0262d"/></g>
<text id="q" x="540" y="560" text-anchor="middle" font-family="Yatra" font-size="140" fill="#ffd166" opacity="0">श्राप?</text></g>'''
# 1 Yamlok
fl = "".join(flame(x, 1180, r.uniform(.9, 1.6), "ff") for x in range(40, 1100, 120))
scenes[1] = f'''<g class="bg"><rect width="1080" height="1920" fill="url(#hell)"/>{fl}<rect y="1180" width="1080" height="740" fill="#2a0c0c"/></g>
<g class="mid">{P(buffalo(), 1.0, 600, 1240)}{P(yamraj(face="calm"), 1.05, 640, 1080)}</g>
<g class="fg">{P(woman(saree="#1f8a8a", border="#d4a017", skin="#4a72c4", blouse="#d4a017", pose="point"), .9, 170, 1300)}
<text x="540" y="520" text-anchor="middle" font-family="Yatra" font-size="96" fill="#ffd166" opacity=".95">यमलोक</text></g>'''
# 2 village, brother sitting, shadow grows
scenes[2] = f'''<g class="bg">{village_bg()}</g><g class="mid">{ground()}<path id="shadow" d="M0 0 C-40 -60 -40 -260 0 -300 C40 -260 40 -60 0 0Z M-40 -330 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 M-30 -360 L0 -420 L30 -360Z" fill="#1a0d12" opacity="0" transform="translate(820 1150) scale(1.6)"/>
{P(man(sit=True, face="calm"), 1.05, 430, 1260)}</g><g class="fg"></g>'''
# 3 sister cursing, yamraj knows
scenes[3] = f'''<g class="bg">{village_bg("#f2c98a")}</g><g class="mid">{ground()}{P(man(face="wide"), .95, 300, 1300)}
<g id="cs3a">{P(woman(face="angry", pose="point", heart=True), 1.05, 560, 1320)}</g>
<g id="ym3" opacity="0">{P(yamraj(face="closed"), 1.0, 900, 1330)}</g></g>
<g class="fg"><g id="sparks">{''.join(f'<path d="M{620+i*40} {860-i*30} l30 -20 l-10 30 l34 -16" stroke="#e03131" stroke-width="8" fill="none"/>' for i in range(4))}</g>
<g id="lipsTag" opacity="0"><rect x="120" y="450" width="380" height="90" rx="45" fill="#e03131"/><text x="310" y="510" text-anchor="middle" font-family="Hind" font-weight="700" font-size="46" fill="#fff">होंठों पर श्राप</text></g>
<g id="heartTag" opacity="0"><rect x="560" y="450" width="400" height="90" rx="45" fill="#ffd166"/><text x="760" y="510" text-anchor="middle" font-family="Hind" font-weight="700" font-size="46" fill="#3a0b1a">मन में प्यार</text></g></g>'''
# 4 wall falls
bricks = "".join(f'<rect x="{(c*80)+(40 if rr%2 else 0)}" y="{rr*46}" width="76" height="42" fill="#a2552f"/>' for rr in range(14) for c in range(-1, 4))
scenes[4] = f'''<g class="bg">{village_bg("#f2c98a")}</g><g class="mid">{ground()}{P(man(sit=True, face="wide"), 1.0, 330, 1260)}
<g id="wall"><g transform="translate(560 1180)"><g id="wallR"><rect x="0" y="-644" width="280" height="644" fill="#7a3a1e"/><g transform="translate(0 -644)">{bricks}</g></g></g></g>
<g id="sis4" opacity="0">{P(woman(pose="shield", face="angry"), 1.0, 470, 1300)}</g></g><g class="fg"><g id="dust4" opacity="0">{''.join(f'<circle cx="{r.uniform(200,900):.0f}" cy="{r.uniform(1000,1260):.0f}" r="{r.uniform(20,60):.0f}" fill="#d9b98a" opacity=".7"/>' for _ in range(16))}</g></g>'''
# 5 snake under thali, scorpions -> flowers
sc = "".join(scorpion(x, y, .9, "scp") for x, y in [(330, 1060), (520, 1040), (720, 1070)])
mg = "".join(marigold(x, y, 1.1, "mg") for x, y in [(330, 1060), (520, 1040), (720, 1070)])
scenes[5] = f'''<g class="bg"><rect width="1080" height="1920" fill="#3a2414"/><rect y="560" width="1080" height="700" fill="#5a3a20"/></g>
<g class="mid"><g id="thaliG"><rect x="200" y="760" width="680" height="40" rx="10" fill="#7a4a22"/><ellipse cx="540" cy="720" rx="220" ry="40" fill="#d6d3cc" stroke="#9c958a" stroke-width="8"/><ellipse cx="500" cy="705" rx="90" ry="22" fill="#fff"/><circle cx="610" cy="708" r="22" fill="#e9a23b"/>{snake(470, 900, 1.15, 'id="snk"')}</g>
<g id="bedG" opacity="0"><rect x="160" y="1040" width="760" height="140" rx="16" fill="#e9e1cf"/><rect x="160" y="1170" width="760" height="40" fill="#7a4a22"/>{sc}{mg}</g>
<path id="aanchal" d="M-300 400 Q100 520 560 470 Q900 430 1400 520 L1400 640 Q900 560 560 600 Q100 650 -300 540Z" fill="#f2b400" opacity="0"/><path id="aanchal2" d="M-300 400 Q100 520 560 470 Q900 430 1400 520" stroke="#c0262d" stroke-width="22" fill="none" opacity="0"/></g><g class="fg"></g>'''
# 6 sister stands against Yamraj
scenes[6] = f'''<g class="bg"><rect width="1080" height="1920" fill="url(#dusk)"/>{banana(80,1180,1.3)}{banana(1000,1180,1.2,-1)}</g>
<g class="mid">{ground("#6b4423")}<path d="M840 1180 C800 1060 800 760 860 700 a60 60 0 1 1 80 0 C1000 760 1000 1060 960 1180Z M850 640 L900 560 L950 640Z" fill="#120810" opacity=".85"/>
{P(woman(pose="stop", face="angry"), 1.55, 430, 1380)}</g><g class="fg"></g>'''
# 7 godhan + items + musal
items = [("pan", '<path d="M0 0 C-40 -30 -30 -80 0 -100 C30 -80 40 -30 0 0Z" fill="#3fa34d"/>'), ("sup", '<circle r="22" fill="#8a4f17"/><circle r="22" fill="none" stroke="#5a3010" stroke-width="5"/>'),
         ("lau", '<path d="M0 0 L0 -40 M-12 -48 L12 -48 M0 -40 L0 -58" stroke="#4a2a10" stroke-width="9" stroke-linecap="round"/>'), ("ela", '<ellipse rx="16" ry="28" fill="#8fbf4a"/>')]
itg = "".join(f'<g transform="translate({x} {y})"><g id="it{i}" opacity="0">{svg}</g></g>' for i, ((n, svg), (x, y)) in enumerate(zip(items, [(470, 1010), (560, 980), (630, 1020), (520, 1070)])))
scenes[7] = f'''<g class="bg">{village_bg("#f0c27e")}</g><g class="mid">{ground()}
<g id="gob" filter="url(#pp)"><ellipse cx="545" cy="1150" rx="210" ry="40" fill="#5a3a1c"/><path d="M545 1140 C470 1140 450 1080 470 1040 C430 1020 440 960 500 970 C500 920 590 920 590 970 C650 960 660 1020 620 1040 C640 1080 620 1140 545 1140Z" fill="#6b4a2a"/>{itg}</g>
<g id="musal"><g transform="translate(560 470)"><rect x="-22" y="-60" width="44" height="560" rx="20" fill="#9a6a34"/><rect x="-26" y="380" width="52" height="40" fill="#5a3a1c"/></g></g>
{P(woman(pose="pound", face="angry"), 1.0, 640, 1330)}</g><g class="fg"><g id="dust7" opacity="0">{''.join(f'<circle cx="{r.uniform(380,720):.0f}" cy="{r.uniform(1000,1160):.0f}" r="{r.uniform(16,46):.0f}" fill="#c9a77a" opacity=".75"/>' for _ in range(14))}</g></g>'''
# 8 power breaks, blessing
threads = "".join(f'<path class="thr" d="M{540-180+i*60} 560 Q{540+r.uniform(-60,60):.0f} {800+i*30} {540-150+i*50} 1180" stroke="#ffd166" stroke-width="6" fill="none"/>' for i in range(7))
scenes[8] = f'''<g class="bg"><rect width="1080" height="1920" fill="url(#dusk)"/></g><g class="mid">{ground("#6b4423")}
{P(yamraj(pose="bless", face="closed"), 1.15, 700, 1300)}<g id="thrG">{threads}</g>
{P(man(pose="pray"), .95, 260, 1320)}{P(woman(pose="pray"), .95, 420, 1330)}</g><g class="fg"><g id="halo" opacity="0"><circle cx="340" cy="900" r="260" fill="#fff3c4" opacity=".35"/></g></g>'''
# 9 thorn, regret
scenes[9] = f'''<g class="bg"><rect width="1080" height="1920" fill="#24121a"/><circle cx="540" cy="760" r="420" fill="#f6c46a" opacity=".12"/></g>
<g class="mid">{P(woman(face="sad", tear=True, pose="pray"), 1.7, 540, 1500)}</g>
<g class="fg"><g id="thorn9" opacity="0" transform="translate(620 830)"><path d="M0 0 L190 -40" stroke="#5b4a2a" stroke-width="12" stroke-linecap="round"/>{''.join(f'<path d="M{30+i*34} {-6-i*7} l-4 -26 l16 16Z" fill="#7a6a3a"/>' for i in range(5))}</g>
<circle id="spk9" cx="625" cy="828" r="10" fill="#fff6d0" opacity="0"/></g>'''
# 10 ritual today
women = "".join(P(woman(saree=c, border=b, pose="pound", face="calm"), .78, x, 1330) for x, c, b in [(170, "#e8590c", "#ffd166"), (390, "#c2255c", "#ffd166"), (690, "#2f9e44", "#ffd166"), (910, "#f2b400", "#c0262d")])
garl = "".join(f'<circle cx="{x}" cy="{430+30*((x//40)%2)}" r="18" fill="{["#ff9f1c","#ffbf3c","#e8590c"][(x//40)%3]}"/>' for x in range(0, 1100, 40))
scenes[10] = f'''<g class="bg"><rect width="1080" height="1920" fill="#f0c27e"/>{hut(540,1180,1.1)}</g><g class="mid">{ground()}<ellipse cx="545" cy="1220" rx="150" ry="30" fill="#5a3a1c"/>{women}</g>
<g class="fg">{garl}<g id="map" opacity="0"><rect x="160" y="560" width="760" height="96" rx="48" fill="#3a0b1a"/><text x="540" y="625" text-anchor="middle" font-family="Hind" font-weight="700" font-size="48" fill="#ffd166">बिहार · झारखंड · पूर्वांचल</text></g></g>'''
# 11 end card
scenes[11] = f'''<g class="bg"><rect width="1080" height="1920" fill="#24121a"/></g><g class="mid">{P(man(pose="down"), .9, 420, 1250)}{P(woman(pose="shield", face="angry"), .95, 640, 1260)}</g>
<g class="fg"><g id="endc" opacity="0"><rect x="90" y="380" width="900" height="300" rx="40" fill="#fff6e4"/><text x="540" y="500" text-anchor="middle" font-family="Yatra" font-size="70" fill="#b5172f">उस बहन को भेजो</text>
<text x="540" y="600" text-anchor="middle" font-family="Hind" font-weight="700" font-size="46" fill="#3a0b1a">जो तुम्हारे लिए यमराज से भी लड़ जाए</text></g></g>'''
caps = "\n".join(f'<div class="cap" id="cap{i}"><span>{l["caption"]}</span></div>' for i, l in enumerate(L))
clouds = "".join(f'<g class="cl" style="transform-origin:{x}px 0px"><line x1="{x}" y1="0" x2="{x}" y2="{y-30}" stroke="#d9c7a0" stroke-width="2"/><g transform="translate({x} {y}) scale({s})" filter="url(#pp)"><path d="M-90 0 Q-100 -50 -50 -55 Q-40 -100 10 -90 Q50 -120 80 -70 Q120 -70 110 -20 Q120 10 80 10 L-80 10 Q-110 10 -90 0Z" fill="#f4ead2"/></g></g>' for x, y, s in [(180, 300, .9), (420, 360, .7), (760, 290, 1.0), (960, 380, .6)])
bokeh = "".join(f'<circle class="bk" cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(200,1700):.0f}" r="{r.uniform(18,60):.0f}" fill="{r.choice(["#ffd27a","#ffb347","#fff0c0"])}"/>' for _ in range(22))
dust = "".join(f'<circle class="du" cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(300,1500):.0f}" r="{r.uniform(2,4.5):.1f}" fill="#fff6d0"/>' for _ in range(60))
rays = "".join(f'<polygon points="{x},0 {x+70},0 {x+420},1920 {x+200},1920" fill="#fff4cc"/>' for x in (80, 300, 520))
scene_html = "".join(f'<div class="sc" id="s{k}"><svg class="full" width="1080" height="1920" viewBox="0 0 1080 1920"><g class="cam">{v}</g></svg></div>' for k, v in scenes.items())
html = open("tpl.html").read()
for k, v in {"{{DUR}}": f"{DUR:.3f}", "{{SCENES}}": scene_html, "{{CAPS}}": caps, "{{CLOUDS}}": clouds, "{{BOKEH}}": bokeh, "{{DUST}}": dust, "{{RAYS}}": rays,
             "{{LINES}}": json.dumps([{"start": l["start"], "end": l["end"]} for l in L]), "{{SC}}": json.dumps(SC)}.items():
    html = html.replace(k, v)
open("hf/index.html", "w").write(html); print("ok", DUR)
