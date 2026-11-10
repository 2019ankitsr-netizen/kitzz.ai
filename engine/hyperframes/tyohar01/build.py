import json, random, math
TL = json.load(open("timeline.json")); L = TL["lines"]; DUR = TL["total"]
r = random.Random(11)
caps = "\n".join(f'<div class="cap" id="cap{i}"><span>{l["caption"]}</span></div>' for i, l in enumerate(L))
waves = "".join(f'<path d="M{x} {y} q20 -9 40 0 t40 0" />' for x in range(-200, 1400, 110) for y in (1040, 1090, 1150, 1220, 1290))
stars = "".join(f'<circle class="st" cx="{r.uniform(20,1060):.0f}" cy="{r.uniform(260,900):.0f}" r="{r.choice([2,2.5,3])}" fill="#fff"/>' for _ in range(50))
diyas = "".join(f'<g class="dy" transform="translate({x} {y})"><path d="M-22 0 Q0 22 22 0Z" fill="#c2551c"/><ellipse class="fl" cx="0" cy="-12" rx="7" ry="14" fill="#ffd166"/></g>' for x, y in [(70, 985), (150, 985), (230, 985), (110, 1045), (190, 1045)])
thekua = "".join(f'<g class="tk" transform="translate({x} {y}) rotate({r.uniform(-20,20):.0f})"><ellipse rx="70" ry="52" fill="#b8742e"/><ellipse rx="56" ry="40" fill="none" stroke="#8a4f17" stroke-width="5"/><path d="M-40 0 H40 M-28 -20 L28 20 M-28 20 L28 -20" stroke="#8a4f17" stroke-width="5"/></g>' for x, y in [(330, 640), (540, 600), (750, 640), (430, 760), (650, 760)])
html = r'''<!doctype html><html lang="hi" data-resolution="portrait"><head><meta charset="UTF-8"/><title>Tyohar 01 Chhath</title>
<script src="gsap.min.js"></script>
<style>
@font-face{font-family:"Hind";src:url("fonts/Hind-Bold.ttf");font-weight:700}
@font-face{font-family:"Hind";src:url("fonts/Hind-SemiBold.ttf");font-weight:600}
@font-face{font-family:"Yatra";src:url("fonts/YatraOne-Regular.ttf")}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#140a1e}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Hind";color:#fff}
svg.full{position:absolute;left:0;top:0}
#chrome{position:absolute;top:200px;left:50%;transform:translateX(-50%);background:#ffd166;color:#3a1a05;font-weight:700;font-size:34px;padding:8px 30px;border-radius:40px;white-space:nowrap}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}
.big{position:absolute;width:1080px;text-align:center;font-family:"Yatra";color:#fff1cf;text-shadow:0 8px 30px rgba(0,0,0,.55)}
.day{position:absolute;left:90px;top:290px;padding:16px 34px;border-radius:30px;background:rgba(255,246,228,.95);color:#3a1a05;box-shadow:0 8px 0 rgba(0,0,0,.25)}
.day .n{font-weight:700;font-size:34px;color:#b5172f;letter-spacing:1px}.day .t{font-family:"Yatra";font-size:72px;line-height:1.1}
.cap{position:absolute;left:90px;width:900px;top:1350px;text-align:center;font-weight:700;font-size:50px;line-height:1.3;opacity:0}
.cap span{background:rgba(20,8,24,.82);padding:10px 26px;border-radius:24px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.chip{position:absolute;padding:14px 34px;border-radius:50px;font-weight:700;font-size:46px;background:#fff;color:#3a1a05;box-shadow:0 8px 0 rgba(0,0,0,.25);opacity:0;white-space:nowrap}
#clock{position:absolute;left:140px;top:470px;width:800px;width:600px;text-align:center;font-family:"Yatra";font-family:"Hind";font-weight:700;font-size:170px;color:#fff1cf;text-shadow:0 10px 40px rgba(0,0,0,.7),0 0 6px #3a1a05}
#endcard{position:absolute;left:90px;top:430px;width:900px;padding:50px 40px;border-radius:40px;background:#fff6e4;color:#3a1a05;text-align:center;box-sizing:border-box}
#endcard .h{font-family:"Yatra";font-size:78px;color:#b5172f;line-height:1.15}#endcard .s{font-weight:700;font-size:44px;margin-top:22px}
.wv path{fill:none;stroke:rgba(255,255,255,.35);stroke-width:5;stroke-linecap:round}
</style></head><body>
<div id="root" data-composition-id="t1" data-width="1080" data-height="1920" data-start="0" data-duration="{{DUR}}">
<svg class="full" width="1080" height="1920">
 <defs>
  <linearGradient id="skyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b1150"/><stop offset=".55" stop-color="#c2410c"/><stop offset="1" stop-color="#fbbf24"/></linearGradient>
  <linearGradient id="skyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0a24"/><stop offset="1" stop-color="#2a1a4a"/></linearGradient>
  <linearGradient id="skyDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7dd3fc"/><stop offset=".6" stop-color="#f9a8d4"/><stop offset="1" stop-color="#fde68a"/></linearGradient>
  <linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c2d12"/><stop offset="1" stop-color="#1e1b4b"/></linearGradient>
  <radialGradient id="sunG"><stop offset="0" stop-color="#fff7d6"/><stop offset=".6" stop-color="#fbbf24"/><stop offset="1" stop-color="#f97316"/></radialGradient>
 </defs>
 <rect width="1080" height="1000" fill="url(#skyDusk)"/>
 <rect id="night" width="1080" height="1000" fill="url(#skyNight)" opacity="0"/><g id="stars" opacity="0">{{STARS}}</g>
 <rect id="dawn" width="1080" height="1000" fill="url(#skyDawn)" opacity="0"/>
 <g id="sun"><circle cx="780" cy="830" r="230" fill="#fbbf24" opacity=".18"/><circle cx="780" cy="830" r="120" fill="url(#sunG)"/></g>
 <rect y="980" width="1080" height="940" fill="url(#water)"/>
 <rect id="wnight" y="980" width="1080" height="940" fill="#0d0b26" opacity="0"/><rect id="wdawn" y="980" width="1080" height="940" fill="#3b4f8a" opacity="0"/>
 <ellipse id="sunRef" cx="760" cy="1060" rx="90" ry="22" fill="#fde68a" opacity=".55"/>
 <g class="wv" id="waves">{{WAVES}}</g>
 <path d="M0 960 L330 960 L380 1000 L0 1000Z M0 1020 L280 1020 L320 1060 L0 1060Z" fill="#5b3a29"/>
 <g id="diyas" opacity="0">{{DIYAS}}</g>
 <g transform="translate(560 1010)"><g id="vrati" opacity="0"><path d="M-40 60 Q-46 -60 -10 -110 L10 -110 Q46 -60 40 60Z" fill="#1a0b10"/><circle cx="0" cy="-140" r="34" fill="#1a0b10"/>
   <path id="arms" d="M-30 -90 L-70 -190 M30 -90 L70 -190" stroke="#1a0b10" stroke-width="22" stroke-linecap="round"/>
   <path id="soop" d="M-110 -210 Q0 -170 110 -210 L90 -250 Q0 -225 -90 -250Z" fill="#c8a165" stroke="#1a0b10" stroke-width="6"/>
   <circle cx="-40" cy="-245" r="18" fill="#f59e0b"/><circle cx="0" cy="-250" r="20" fill="#16a34a"/><circle cx="40" cy="-245" r="18" fill="#dc2626"/></g></g>
</svg>
<div id="chrome">त्योहार, 1 मिनट में · छठ</div>

<div class="sc" id="s0">
 <div id="clock">0 घंटे</div>
 <svg class="full" width="1080" height="1920"><g id="drop" transform="translate(540 370)"><path d="M0 -70 C40 -10 55 20 55 40 A55 55 0 0 1 -55 40 C-55 20 -40 -10 0 -70Z" fill="#7dd3fc"/><path id="dropX" d="M-80 -80 L80 110" stroke="#e03131" stroke-width="20" stroke-linecap="round"/></g></svg>
 <div class="chip" id="smile" style="left:330px;top:820px">+ मुस्कान</div>
</div>
<div class="sc" id="s1">
 <div class="day"><div class="n">दिन 1 · 13 नवंबर</div><div class="t">नहाय-खाय</div></div>
 <svg class="full" width="1080" height="1920"><g transform="translate(540 680)"><g id="plate"><ellipse rx="230" ry="80" fill="#e5e7eb" stroke="#9ca3af" stroke-width="8"/><ellipse cx="-60" cy="-20" rx="110" ry="50" fill="#fff"/>
   <g fill="#65a30d"><rect x="40" y="-40" width="60" height="40" rx="10"/><rect x="100" y="-20" width="55" height="38" rx="10"/><rect x="60" y="10" width="58" height="36" rx="10"/></g></g></g></svg>
 <div class="chip" id="c1a" style="left:180px;top:830px">स्नान</div><div class="chip" id="c1b" style="left:470px;top:830px;background:#ffd166">कद्दू-भात</div>
</div>
<div class="sc" id="s2">
 <div class="day"><div class="n">दिन 2 · 14 नवंबर</div><div class="t">खरना</div></div>
 <svg class="full" width="1080" height="1920">
  <g transform="translate(400 640)"><path d="M-150 -20 Q0 160 150 -20Z" fill="#a16207"/><ellipse cy="-20" rx="150" ry="36" fill="#fef3c7"/>
   <path class="steam" d="M-50 -70 q20 -30 0 -60 t0 -60" stroke="#fff" stroke-width="8" fill="none" opacity=".7"/><path class="steam" d="M20 -70 q20 -30 0 -60 t0 -60" stroke="#fff" stroke-width="8" fill="none" opacity=".7"/></g>
  <g transform="translate(720 640)"><circle r="95" fill="#e9b872"/><circle r="95" fill="none" stroke="#a16207" stroke-width="6"/><circle cx="-30" cy="-20" r="10" fill="#a16207" opacity=".5"/><circle cx="25" cy="25" r="12" fill="#a16207" opacity=".5"/></g>
  <g id="ring" opacity="0" transform="translate(540 940)"><circle r="110" fill="rgba(0,0,0,.45)" stroke="rgba(255,255,255,.25)" stroke-width="18"/><circle id="ringArc" r="110" fill="none" stroke="#7dd3fc" stroke-width="18" transform="rotate(-90)" stroke-dasharray="691" stroke-dashoffset="691"/>
   <text y="22" text-anchor="middle" font-family="Yatra" font-size="72" fill="#fff">36h</text></g>
 </svg>
 <div class="chip" id="c2a" style="left:200px;top:450px;opacity:0">गुड़ की खीर</div>
</div>
<div class="sc" id="s3">
 <div class="day"><div class="n">दिन 3 · 15 नवंबर</div><div class="t">डूबते सूरज को अर्घ्य</div></div>
 <div class="chip" id="c3" style="left:120px;top:540px;background:#ffd166">बहुत कम त्योहार: डूबते सूरज की पूजा</div>
</div>
<div class="sc" id="s4">
 <div class="day"><div class="n">दिन 4 · 16 नवंबर</div><div class="t">उगते सूरज को अर्घ्य</div></div>
 <svg class="full" width="1080" height="1920"><g id="thekua">{{THEKUA}}</g></svg>
 <div class="chip" id="c4" style="left:330px;top:1180px;background:#ffd166">पारण + ठेकुआ</div>
</div>
<div class="sc" id="s5">
 <div class="big" style="top:470px;font-size:84px">अर्घ्य का समय?</div>
 <div class="chip" id="c5" style="left:200px;top:640px">अपने शहर का पंचांग देखें</div>
</div>
<div class="sc" id="s6">
 <div id="endcard"><div class="h">उसे भेजो जो इस छठ<br/>घर से दूर है</div><div class="s">अपने घाट का नाम कमेंट में लिखो</div></div>
</div>
{{CAPS}}
<script>
(function(){
 const L={{LINES}}, D={{DUR}}; const tl=gsap.timeline({paused:true}); const s=i=>L[i].start, e=i=>L[i].end;
 L.forEach((l,i)=>{const el='#cap'+i; tl.fromTo(el,{opacity:0,y:16},{opacity:1,y:0,duration:.2},l.start-.05); if(i<L.length-1) tl.to(el,{opacity:0,duration:.15},l.end+.1);});
 tl.fromTo('#waves',{x:0},{x:-110,duration:2.6,ease:'none',repeat:Math.ceil(D/2.6)},0);
 tl.fromTo('#sunRef',{scaleX:1,transformOrigin:'50% 50%'},{scaleX:1.25,duration:1.1,yoyo:true,repeat:Math.ceil(D),ease:'sine.inOut'},0);
 document.querySelectorAll('.fl').forEach((f,i)=>tl.fromTo(f,{scaleY:1,transformOrigin:'50% 100%'},{scaleY:1.3,duration:.25+(i%3)*.07,yoyo:true,repeat:Math.ceil(D*3),ease:'sine.inOut'},i*.1));
 document.querySelectorAll('.st').forEach((c,i)=>tl.fromTo(c,{opacity:.3},{opacity:1,duration:.8+(i%4)*.3,yoyo:true,repeat:Math.ceil(D),ease:'sine.inOut'},(i%5)*.2));
 const cut=[0,e(0)+.15,e(1)+.15,e(2)+.15,e(3)+.15,e(4)+.15,e(5)+.15,D+1];
 for(let k=0;k<7;k++){ if(k>0) tl.fromTo('#s'+k,{opacity:0,y:30},{opacity:1,y:0,duration:.35,ease:'power2.out'},cut[k]-.05); tl.to('#s'+k,{opacity:0,duration:.25},cut[k+1]-.2);} tl.set('#s0',{opacity:1},0);
 // hook: clock ticks down fast, drop crossed
 const ck={v:0}; tl.to(ck,{v:36,duration:1.6,ease:'power2.out',onUpdate:()=>{document.getElementById('clock').textContent=Math.round(ck.v)+' घंटे';}},0.05);
 tl.fromTo('#clock',{scale:.4,opacity:0},{scale:1,opacity:1,duration:.4,ease:'back.out(2.2)'},0.02);
 tl.fromTo('#dropX',{strokeDasharray:260,strokeDashoffset:260},{strokeDashoffset:0,duration:.3},1.2);
 tl.fromTo('#smile',{opacity:0,scale:.6},{opacity:1,scale:1,duration:.3,ease:'back.out(2.5)'},kw(0,.55));
 function kw(i,f){return s(i)+(e(i)-s(i))*f;}
 // day1: plate slides, chips
 tl.fromTo('#plate',{x:-700},{x:0,duration:.6,ease:'power3.out'},s(1)+.6);
 tl.fromTo('#c1a',{opacity:0,y:20},{opacity:1,y:0,duration:.3},kw(1,.55)); tl.fromTo('#c1b',{opacity:0,y:20},{opacity:1,y:0,duration:.3},kw(1,.75));
 // day2: steam, kheer chip, ring fills; sky to night
 document.querySelectorAll('.steam').forEach((p,i)=>tl.fromTo(p,{y:0,opacity:.7},{y:-40,opacity:0,duration:1.2,repeat:6,ease:'none'},s(2)+i*.5));
 tl.fromTo('#c2a',{opacity:0,y:20},{opacity:1,y:0,duration:.3},kw(2,.3));
 tl.to(['#night','#wnight'],{opacity:1,duration:1.5},kw(2,.5)); tl.to('#stars',{opacity:1,duration:1.2},kw(2,.6)); tl.to(['#sun','#sunRef'],{opacity:0,duration:1},kw(2,.5));
 tl.to('#ring',{opacity:1,duration:.3},kw(2,.62)); tl.to('#ringArc',{strokeDashoffset:0,duration:e(2)-kw(2,.62),ease:'none'},kw(2,.62));
 // day3: back to dusk, sun sinks, vrati raises soop, diyas
 tl.to(['#night','#wnight','#stars'],{opacity:0,duration:1},s(3)-.3); tl.set('#sun',{y:-330},s(3)-.3); tl.to(['#sun'],{opacity:1,duration:.6},s(3)-.3); tl.to('#sunRef',{opacity:.55,duration:.6},s(3));
 tl.to('#sun',{y:130,duration:e(3)-s(3)+.3,ease:'sine.in'},s(3)); tl.to('#sunRef',{scaleX:.4,opacity:.2,duration:e(3)-s(3)},s(3));
 tl.to(['#vrati','#diyas'],{opacity:1,duration:.5},s(3)+.4); tl.fromTo('#vrati',{y:40},{y:0,duration:.8,ease:'power2.out'},s(3)+.4);
 tl.fromTo('#c3',{opacity:0,y:20},{opacity:1,y:0,duration:.3},kw(3,.55));
 // day4: dawn, sun rises from left, thekua pop
 tl.to(['#dawn','#wdawn'],{opacity:1,duration:1.2},s(4)-.3); tl.set('#sun',{x:-420,y:240},s(4)-.3); tl.to('#sun',{y:-130,opacity:1,duration:2.4,ease:'power2.out'},s(4)); tl.set('#sunRef',{attr:{cx:340},opacity:.5,scaleX:1},s(4));
 tl.set("#vrati",{x:250},s(4)-.3);
 document.querySelectorAll('.tk').forEach((t,i)=>tl.fromTo(t,{opacity:0,scale:.3,transformOrigin:'50% 50%'},{opacity:1,scale:1,duration:.3,ease:'back.out(2.5)'},kw(4,.6)+i*.12));
 tl.fromTo('#c4',{opacity:0,y:20},{opacity:1,y:0,duration:.3},kw(4,.5));
 tl.fromTo('#c5',{opacity:0,scale:.7},{opacity:1,scale:1,duration:.3,ease:'back.out(2)'},s(5)+.6);
 tl.fromTo('#endcard',{y:200,rotation:-4},{y:0,rotation:0,duration:.6,ease:'back.out(1.4)'},s(6));
 window.__timelines=window.__timelines||{}; window.__timelines['t1']=tl;
})();
</script></div></body></html>'''
for k, v in {"{{DUR}}": str(DUR), "{{CAPS}}": caps, "{{WAVES}}": waves, "{{STARS}}": stars, "{{DIYAS}}": diyas, "{{THEKUA}}": thekua,
             "{{LINES}}": json.dumps([{"start": l["start"], "end": l["end"]} for l in L])}.items():
    html = html.replace(k, v)
open("hf/index.html", "w").write(html); print("ok", DUR)
