# Paper-cut figure library (SVG strings). Feet anchored at (0,0); ~520px tall at s=1.
def _eyes(face, y=-412):
    if face in ("calm", "closed"): return f'<path d="M-20 {y} q8 6 16 0 M6 {y} q8 6 16 0" stroke="#2a1206" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if face == "angry": return f'<path d="M-26 {y-14} L-6 {y-6} M26 {y-14} L6 {y-6}" stroke="#2a1206" stroke-width="6"/><circle cx="-14" cy="{y}" r="6" fill="#2a1206"/><circle cx="14" cy="{y}" r="6" fill="#2a1206"/>'
    if face == "wide": return f'<circle cx="-15" cy="{y}" r="9" fill="#fff"/><circle cx="15" cy="{y}" r="9" fill="#fff"/><circle cx="-15" cy="{y}" r="5" fill="#2a1206"/><circle cx="15" cy="{y}" r="5" fill="#2a1206"/>'
    return f'<circle cx="-14" cy="{y}" r="6" fill="#2a1206"/><circle cx="14" cy="{y}" r="6" fill="#2a1206"/>'
def _mouth(face, y=-386):
    if face == "angry": return f'<ellipse cx="0" cy="{y}" rx="13" ry="9" fill="#5a1010"/>'
    if face in ("sad",): return f'<path d="M-12 {y+4} q12 -10 24 0" stroke="#5a1010" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if face == "wide": return f'<ellipse cx="0" cy="{y}" rx="9" ry="12" fill="#5a1010"/>'
    return f'<path d="M-12 {y-2} q12 10 24 0" stroke="#5a1010" stroke-width="5" fill="none" stroke-linecap="round"/>'
ARMS = {  # (left, right) paths relative to shoulders at (-44,-345),(44,-345)
 "down": ("M-44 -345 Q-70 -270 -62 -200", "M44 -345 Q70 -270 62 -200"),
 "stop": ("M-44 -345 Q-70 -270 -62 -200", "M44 -345 Q120 -350 190 -360"),
 "raise": ("M-44 -345 Q-90 -420 -80 -500", "M44 -345 Q90 -420 80 -500"),
 "shield": ("M-44 -345 Q-140 -330 -190 -300", "M44 -345 Q140 -330 190 -300"),
 "pray": ("M-44 -345 Q-30 -300 -4 -330", "M44 -345 Q30 -300 4 -330"),
 "point": ("M-44 -345 Q-70 -270 -62 -200", "M44 -345 Q130 -400 200 -430"),
 "bless": ("M-44 -345 Q-70 -270 -62 -200", "M44 -345 Q110 -420 150 -470"),
 "pound": ("M-44 -345 Q-10 -420 10 -470", "M44 -345 Q40 -420 20 -470"),
}
def woman(saree="#f2b400", border="#c0262d", skin="#c98b5e", pose="down", face="calm", hair="#1a0d06", blouse="#c0262d", tear=False, heart=False, sid=""):
    la, ra = ARMS[pose]
    t = f'<g class="fig" {sid}>'
    t += f'<path d="M-30 -440 Q-70 -420 -60 -330 L-50 -300 L50 -300 L60 -330 Q70 -420 30 -440Z" fill="{hair}"/>'
    t += f'<path d="M-78 0 L78 0 L52 -265 L-52 -265Z" fill="{saree}"/><path d="M-78 0 L78 0 L76 -22 L-76 -22Z" fill="{border}"/>'
    t += f'<rect x="-44" y="-355" width="88" height="95" rx="22" fill="{blouse}"/>'
    t += f'<path d="M-46 -350 L30 -350 L70 -150 L40 -140 Z" fill="{saree}"/><path d="M30 -350 L40 -350 L78 -150 L70 -148Z" fill="{border}"/>'
    t += f'<path d="{la}" stroke="{skin}" stroke-width="24" fill="none" stroke-linecap="round"/><path d="{ra}" stroke="{skin}" stroke-width="24" fill="none" stroke-linecap="round"/>'
    t += f'<rect x="-12" y="-378" width="24" height="30" fill="{skin}"/><circle cx="0" cy="-410" r="44" fill="{skin}"/>'
    t += f'<path d="M-46 -414 Q-44 -470 0 -462 Q44 -470 46 -414 Q30 -444 0 -446 Q-30 -444 -46 -414Z" fill="{hair}"/><circle cx="34" cy="-452" r="22" fill="{hair}"/>'
    t += f'<circle cx="0" cy="-432" r="6" fill="#d00000"/>' + _eyes(face) + _mouth(face)
    if tear: t += '<path class="tear" d="M-16 -402 q-6 14 0 22 q6 -8 0 -22Z" fill="#9ad7ff"/>'
    if heart: t += '<path class="heart" d="M0 -300 c-14 -18 -40 -6 -30 14 l30 28 l30 -28 c10 -20 -16 -32 -30 -14Z" fill="#ffd166"/>'
    return t + '</g>'
def man(kurta="#f5efe2", dhoti="#ffffff", gam="#c0262d", skin="#b97a4f", pose="down", face="calm", sit=False, sid=""):
    la, ra = ARMS[pose]
    t = f'<g class="fig" {sid}>'
    if sit:
        t += f'<path d="M-60 -170 L60 -170 L95 -60 L130 -10 L80 0 L50 -80 L-50 -80 L-60 -170Z" fill="{dhoti}" stroke="#d8d0c0" stroke-width="3"/>'
        off = 130
    else:
        t += f'<path d="M-58 0 L-8 0 L-6 -210 L-50 -210Z M8 0 L58 0 L50 -210 L6 -210Z" fill="{dhoti}" stroke="#d8d0c0" stroke-width="3"/>'; off = 0
    t += f'<g transform="translate(0 {off})"><rect x="-50" y="-360" width="100" height="160" rx="24" fill="{kurta}"/><path d="M-50 -350 L50 -250 L50 -230 L-50 -330Z" fill="{gam}"/>'
    t += f'<path d="{la}" stroke="{skin}" stroke-width="24" fill="none" stroke-linecap="round"/><path d="{ra}" stroke="{skin}" stroke-width="24" fill="none" stroke-linecap="round"/>'
    t += f'<rect x="-13" y="-380" width="26" height="30" fill="{skin}"/><circle cx="0" cy="-410" r="44" fill="{skin}"/><path d="M-46 -416 Q-40 -468 0 -462 Q40 -468 46 -416 Q20 -440 -46 -416Z" fill="#1a0d06"/>'
    t += _eyes(face) + _mouth(face) + '</g>'
    return t + '</g>'
def yamraj(pose="down", face="calm", sid=""):
    skin = "#3a5aa8"; la, ra = ARMS[pose]
    t = f'<g class="fig" {sid}>'
    t += '<path d="M-70 0 L-10 0 L-8 -230 L-60 -230Z M10 0 L70 0 L60 -230 L8 -230Z" fill="#9b1c24"/><rect x="-66" y="-250" width="132" height="34" fill="#d4a017"/>'
    t += f'<path d="M-62 -380 L62 -380 L58 -240 L-58 -240Z" fill="{skin}"/><path d="M-50 -370 Q0 -300 50 -370" stroke="#d4a017" stroke-width="12" fill="none"/>'
    t += '<path d="M-62 -380 L-20 -380 L60 -250 L30 -240Z" fill="#9b1c24"/>'
    t += f'<path d="{la}" stroke="{skin}" stroke-width="28" fill="none" stroke-linecap="round"/><path d="{ra}" stroke="{skin}" stroke-width="28" fill="none" stroke-linecap="round"/>'
    if pose == "down": t += '<g transform="translate(70 -200)"><rect x="-6" y="-260" width="12" height="300" fill="#8a5a1c"/><circle cy="-280" r="34" fill="#d4a017"/><circle cy="-280" r="34" fill="none" stroke="#8a5a1c" stroke-width="6"/></g>'
    t += f'<rect x="-14" y="-400" width="28" height="30" fill="{skin}"/><circle cx="0" cy="-432" r="48" fill="{skin}"/>'
    t += '<path d="M-44 -462 L-34 -540 L-14 -500 L0 -560 L14 -500 L34 -540 L44 -462Z" fill="#d4a017" stroke="#8a5a1c" stroke-width="4"/><circle cx="0" cy="-490" r="10" fill="#c0262d"/>'
    t += '<path d="M-30 -406 Q-14 -394 0 -404 Q14 -394 30 -406 Q14 -386 0 -396 Q-14 -386 -30 -406Z" fill="#111"/>'
    t += _eyes(face, -440).replace("#2a1206", "#0a0a14")
    return t + '</g>'
def buffalo(sid=""):
    return f'''<g class="fig" {sid}><ellipse cx="0" cy="-130" rx="230" ry="110" fill="#26232e"/><rect x="-170" y="-80" width="36" height="90" fill="#26232e"/><rect x="-80" y="-70" width="36" height="80" fill="#26232e"/><rect x="60" y="-70" width="36" height="80" fill="#26232e"/><rect x="140" y="-80" width="36" height="90" fill="#26232e"/>
    <ellipse cx="-250" cy="-150" rx="70" ry="56" fill="#26232e"/><path d="M-280 -190 Q-370 -230 -330 -290 Q-320 -230 -260 -205Z M-220 -190 Q-150 -240 -190 -300 Q-190 -240 -240 -205Z" fill="#cfc6b0"/><circle cx="-270" cy="-160" r="6" fill="#ffd166"/>
    <path d="M-160 -230 Q0 -260 160 -230 L150 -170 L-150 -170Z" fill="#9b1c24"/><path d="M-160 -230 Q0 -260 160 -230" stroke="#d4a017" stroke-width="10" fill="none"/></g>'''
def hut(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><rect x="-200" y="-240" width="400" height="240" fill="#b88552"/><rect x="-200" y="-240" width="400" height="240" fill="url(#mud)" opacity=".35"/>
    <path d="M-250 -230 L0 -400 L250 -230Z" fill="#c9a24a"/>{''.join(f'<path d="M{-230+i*40} -238 L{-120+i*20} -330" stroke="#9c7a2f" stroke-width="4"/>' for i in range(12))}
    <rect x="-50" y="-150" width="100" height="150" rx="8" fill="#3a2414"/></g>'''
def banana(x, y, s=1.0, flip=1):
    leaves = "".join(f'<path d="M0 -300 Q{flip*a*1.2} {-380+abs(a)*0.3} {flip*a*2} {-300+abs(a)*0.6}" stroke="#3f7d2c" stroke-width="34" fill="none" stroke-linecap="round"/>' for a in (-140, -80, 90, 150))
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-14 0 L14 0 L10 -310 L-10 -310Z" fill="#6b8f3a"/>{leaves}</g>'
def flame(x, y, s=1.0, cls="fl"):
    return f'<g transform="translate({x} {y}) scale({s})"><path class="{cls}" d="M0 0 C-50 -40 -40 -120 0 -200 C40 -120 50 -40 0 0Z" fill="#ff7b00"/><path class="{cls}" d="M0 0 C-26 -26 -20 -80 0 -120 C20 -80 26 -26 0 0Z" fill="#ffd166"/></g>'
def scorpion(x, y, s=1.0, cls=""):
    return f'''<g class="{cls}" transform="translate({x} {y}) scale({s})"><ellipse rx="34" ry="20" fill="#2a1a10"/><path d="M30 0 Q80 -10 80 -50 Q76 -80 56 -76" stroke="#2a1a10" stroke-width="12" fill="none"/>
    <path d="M-30 -8 L-60 -30 M-30 8 L-60 30 M-10 18 L-20 40 M10 18 L16 40 M-10 -18 L-20 -40 M10 -18 L16 -40" stroke="#2a1a10" stroke-width="7"/></g>'''
def marigold(x, y, s=1.0, cls=""):
    p = "".join(f'<ellipse cx="0" cy="-26" rx="14" ry="24" fill="{"#ff9f1c" if i%2 else "#ffbf3c"}" transform="rotate({i*30})"/>' for i in range(12))
    return f'<g class="{cls}" transform="translate({x} {y}) scale({s})">{p}<circle r="14" fill="#e8590c"/></g>'
def snake(x, y, s=1.0, sid=""):
    return f'''<g {sid} transform="translate({x} {y}) scale({s})"><path d="M-160 0 Q-110 -40 -60 0 T40 0 Q80 -10 90 -80" stroke="#1d2a1d" stroke-width="34" fill="none" stroke-linecap="round"/>
    <ellipse cx="96" cy="-118" rx="44" ry="52" fill="#1d2a1d"/><circle cx="84" cy="-124" r="6" fill="#ffd166"/><circle cx="108" cy="-124" r="6" fill="#ffd166"/><path d="M96 -70 l-6 22 m6 -22 l6 22" stroke="#d00" stroke-width="4"/></g>'''
