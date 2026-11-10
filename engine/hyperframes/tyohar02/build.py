import json, random
TL = json.load(open("timeline.json")); L = TL["lines"]; DUR = TL["total"]
r = random.Random(3)
bokeh = "".join(f'<circle class="bk" cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(10,46):.0f}" fill="{r.choice(["#ffb84d","#ff7a3d","#ffd98a"])}" opacity=".12"/>' for _ in range(40))
garland = "".join(f'<circle cx="{x}" cy="{150+38*__import__("math").sin(x/1080*3.14159)+0}" r="17" fill="{["#ff9f1c","#ffbf3c","#ff7b00"][i%3]}"/>' for i, x in enumerate(range(-10, 1100, 30)))
petals = "".join(f'<ellipse class="pt" cx="{r.uniform(40,1040):.0f}" cy="{r.uniform(-300,0):.0f}" rx="10" ry="18" fill="{r.choice(["#ff9f1c","#ffbf3c","#e8590c"])}" transform="rotate({r.uniform(0,180):.0f})"/>' for _ in range(36))
caps = "\n".join(f'<div class="cap" id="cap{i}"><span>{l["caption"]}</span></div>' for i, l in enumerate(L))
poem = "".join(f'<path class="pl" d="M110 {150+i*56} q{60} -14 120 0 t120 0 t120 0 t{r.choice([60,100,120])} 0" />' for i in range(8))
items = [("क्रिकेट ग्रिप किट", "हर संडे खेलता है"), ("फ़ोटो फ़्रेम", "बचपन याद आएगा"), ("हेडफ़ोन", "रोज़ का सफ़र"), ("चाय मग सेट", "चाय का शौक़"), ("डायरी + पेन", "लिखना पसंद")]
lis = "".join(f'<div class="li" id="li{i}"><b>{i+1}</b> {a} <i>क्यों? {b}</i></div>' for i, (a, b) in enumerate(items))
html = r'''<!doctype html><html lang="hi" data-resolution="portrait"><head><meta charset="UTF-8"/><title>Tyohar 02 Bhai Dooj</title>
<script src="gsap.min.js"></script>
<style>
@font-face{font-family:"Hind";src:url("fonts/Hind-Bold.ttf");font-weight:700}
@font-face{font-family:"Hind";src:url("fonts/Hind-SemiBold.ttf");font-weight:600}
@font-face{font-family:"Yatra";src:url("fonts/YatraOne-Regular.ttf")}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#2a0a14}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Hind";color:#fff}
.bg{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 35%,#7a1d2e 0%,#3a0b1a 55%,#1c0610 100%)}
svg.full{position:absolute;left:0;top:0}
#chrome{position:absolute;top:210px;left:50%;transform:translateX(-50%);background:#ffd166;color:#3a0b1a;font-weight:700;font-size:34px;padding:8px 30px;border-radius:40px;letter-spacing:1px;white-space:nowrap}
.sc{position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0}
.big{position:absolute;width:1080px;text-align:center;font-family:"Yatra";color:#ffe2a6;text-shadow:0 8px 30px rgba(0,0,0,.5)}
.badge{position:absolute;left:90px;top:300px;width:120px;height:120px;border-radius:60px;background:#ffd166;color:#3a0b1a;font-family:"Yatra";font-size:84px;text-align:center;line-height:136px;box-shadow:0 8px 0 rgba(0,0,0,.3)}
.btitle{position:absolute;left:236px;top:320px;font-weight:700;font-size:62px;color:#fff}
.cap{position:absolute;left:90px;width:900px;top:1330px;text-align:center;font-weight:700;font-size:52px;line-height:1.3;opacity:0}
.cap span{background:rgba(20,4,12,.82);padding:10px 26px;border-radius:24px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.box{position:absolute;width:300px;height:190px;left:390px;border-radius:18px;background:linear-gradient(135deg,#6b3a1f,#4a2410);border:6px solid #c9963b;box-shadow:0 12px 0 rgba(0,0,0,.35)}
.box:after{content:"";position:absolute;left:138px;top:0;width:24px;height:100%;background:#d62e4b}
.box:before{content:"";position:absolute;left:0;top:83px;width:100%;height:24px;background:#d62e4b}
.yr{position:absolute;left:720px;font-weight:700;font-size:44px;color:#ffd166;opacity:0}
.chip{position:absolute;padding:14px 34px;border-radius:50px;font-weight:700;font-size:48px;background:#fff;color:#3a0b1a;box-shadow:0 8px 0 rgba(0,0,0,.25);opacity:0;white-space:nowrap}
#photo{position:absolute;left:250px;top:500px;width:580px;height:580px;border-radius:12px;overflow:hidden;background:#d9c4a0}
#frame{position:absolute;left:220px;top:470px;width:640px;height:640px;border:24px solid #c9963b;border-radius:18px;box-sizing:border-box;box-shadow:inset 0 0 0 8px #8a5a1c,0 20px 40px rgba(0,0,0,.5);opacity:0}
#scan{position:absolute;left:250px;top:500px;width:580px;height:10px;background:linear-gradient(90deg,transparent,#7cf3ff,transparent);box-shadow:0 0 30px #7cf3ff;opacity:0}
#bubble{position:absolute;left:150px;top:470px;width:780px;padding:26px 34px;border-radius:34px 34px 34px 8px;background:#fff;color:#2a0a14;font-weight:600;font-size:44px;line-height:1.35;opacity:0}
#card{position:absolute;left:140px;top:430px;width:800px;height:620px;border-radius:26px;background:#fff6e4;box-shadow:0 18px 0 rgba(0,0,0,.3);opacity:0}
#card h3{margin:0;padding:30px 0 0;text-align:center;font-family:"Yatra";font-weight:400;font-size:62px;color:#b5172f}
.pl{fill:none;stroke:#5a2a14;stroke-width:7;stroke-linecap:round}
.li{position:absolute;left:110px;width:860px;padding:18px 30px;border-radius:26px;background:#fff;color:#2a0a14;font-weight:700;font-size:44px;opacity:0;box-sizing:border-box}
.li b{display:inline-block;width:56px;height:56px;border-radius:28px;background:#b5172f;color:#fff;text-align:center;line-height:62px;margin-right:12px}
.li i{font-style:normal;font-weight:600;font-size:34px;color:#8a5a1c;margin-left:10px}
#link{position:absolute;left:110px;top:620px;width:860px;padding:34px;border-radius:30px;background:#fff;border:6px solid #e03131;text-align:center;box-sizing:border-box}
#link .t{font-weight:700;font-size:60px;color:#e03131}#link .u{font-weight:600;font-size:40px;color:#1c7ed6;text-decoration:underline}
#cursor{position:absolute;left:900px;top:1050px;width:0;height:0;border-left:30px solid transparent;border-right:30px solid transparent;border-bottom:70px solid #fff;transform:rotate(-30deg);filter:drop-shadow(0 4px 6px rgba(0,0,0,.5))}
#endcard{position:absolute;left:90px;top:470px;width:900px;padding:50px 40px;border-radius:40px;background:#fff6e4;color:#2a0a14;text-align:center;box-sizing:border-box}
#endcard .h{font-family:"Yatra";font-size:86px;color:#b5172f;line-height:1.15}
#endcard .s{font-weight:700;font-size:46px;margin-top:20px}
#endcard .d{display:inline-block;margin-top:30px;padding:10px 30px;border-radius:40px;background:#3a0b1a;color:#ffd166;font-weight:700;font-size:38px}
</style></head><body>
<div id="root" data-composition-id="t2" data-width="1080" data-height="1920" data-start="0" data-duration="{{DUR}}">
<div class="bg"></div>
<svg class="full" width="1080" height="1920"><g id="bokeh">{{BOKEH}}</g><path d="M-20 150 Q540 230 1100 150" stroke="#2f7a3a" stroke-width="6" fill="none"/><g>{{GARLAND}}</g><g id="petals">{{PETALS}}</g></svg>
<div id="chrome">त्योहार, 1 मिनट में · भाई दूज</div>

<div class="sc" id="s0">
  <div class="big" style="top:330px;font-size:96px">फिर वही डिब्बा?</div>
  <div class="box" id="b0" style="top:1060px"></div><div class="box" id="b1" style="top:850px"></div><div class="box" id="b2" style="top:640px"></div>
  <div class="yr" id="y0" style="top:1120px">2024</div><div class="yr" id="y1" style="top:910px">2025</div><div class="yr" id="y2" style="top:700px">2026?</div>
</div>
<div class="sc" id="s1">
  <div class="big" id="n3" style="top:420px;font-size:260px;line-height:1">3</div>
  <div class="big" style="top:720px;font-size:90px">गिफ्ट</div>
  <svg class="full" width="1080" height="1920"><circle cx="540" cy="1090" r="130" fill="#fff6e4" stroke="#ffd166" stroke-width="14"/><line id="hand" x1="540" y1="1090" x2="540" y2="990" stroke="#b5172f" stroke-width="14" stroke-linecap="round"/><circle cx="540" cy="1090" r="14" fill="#3a0b1a"/></svg>
  <div class="chip" id="cAI" style="left:180px;top:930px">AI</div><div class="chip" id="cHr" style="left:700px;top:1150px">1 घंटा</div>
</div>
<div class="sc" id="s2">
  <div class="badge">1</div><div class="btitle">धुँधली फ़ोटो → साफ़</div>
  <div id="photo"><svg width="580" height="580" id="kids"><rect width="580" height="580" fill="#e9d6b0"/><rect y="400" width="580" height="180" fill="#b98d55"/>
   <circle cx="200" cy="230" r="70" fill="#8d5a3b"/><path d="M130 225 Q200 120 270 225" fill="#2a1606"/><rect x="140" y="300" width="120" height="170" rx="40" fill="#e8590c"/>
   <circle cx="380" cy="260" r="60" fill="#8d5a3b"/><path d="M320 255 Q380 170 440 255 L440 330 L320 330Z" fill="#2a1606"/><rect x="325" y="320" width="110" height="150" rx="40" fill="#c2255c"/>
   <circle cx="180" cy="230" r="7" fill="#111"/><circle cx="222" cy="230" r="7" fill="#111"/><circle cx="362" cy="258" r="6" fill="#111"/><circle cx="398" cy="258" r="6" fill="#111"/>
   <path d="M180 262 Q200 280 220 262" stroke="#111" stroke-width="5" fill="none"/><path d="M362 286 Q380 300 398 286" stroke="#111" stroke-width="5" fill="none"/>
   <circle cx="380" cy="232" r="6" fill="#e03131"/></svg></div>
  <div id="scan"></div><div id="frame"></div>
  <div class="chip" id="cRes" style="left:330px;top:1160px;background:#7cf3ff">AI फ़ोटो रिस्टोर</div>
</div>
<div class="sc" id="s3">
  <div class="badge">2</div><div class="btitle">अपनी कविता</div>
  <div id="bubble">3 किस्से + निकनेम "गोलू" बताओ, 8 लाइन की कविता लिखो</div>
  <div id="card"><h3>मेरे गोलू के लिए</h3><svg width="800" height="620" style="position:absolute;left:0;top:0">{{POEM}}</svg></div>
</div>
<div class="sc" id="s4">
  <div class="badge">3</div><div class="btitle">सही गिफ्ट लिस्ट</div>
  <div class="chip" id="k0" style="left:100px;top:470px">उम्र 24</div><div class="chip" id="k1" style="left:380px;top:470px">पसंद: क्रिकेट</div><div class="chip" id="k2" style="left:300px;top:580px;background:#ffd166">बजट ₹1000</div>
  <div style="position:absolute;top:710px;left:0">{{LIST}}</div>
</div>
<div class="sc" id="s5">
  <div id="link"><div class="t">MEGA SALE 90% OFF</div><div class="u">gift-d00j-sale.xyz</div></div>
  <div id="cursor"></div>
  <svg class="full" width="1080" height="1920"><path id="x1" d="M140 600 L940 860" stroke="#e03131" stroke-width="30" stroke-linecap="round"/><path id="x2" d="M940 600 L140 860" stroke="#e03131" stroke-width="30" stroke-linecap="round"/></svg>
  <div class="chip" id="cNo" style="left:290px;top:950px;background:#e03131;color:#fff">क्लिक नहीं!</div>
</div>
<div class="sc" id="s6">
  <div id="endcard"><div class="h">सेव करो<br/>+ भेजो</div><div class="s">इस बार किसका गिफ्ट बेहतर निकलेगा?</div><div class="d">बुधवार, 11 नवंबर</div></div>
</div>
{{CAPS}}
<script>
(function(){
 const L = {{LINES}}, D = {{DUR}}; const tl = gsap.timeline({paused:true});
 const s=i=>L[i].start, e=i=>L[i].end;
 L.forEach((l,i)=>{const el='#cap'+i; tl.fromTo(el,{opacity:0,y:16},{opacity:1,y:0,duration:.2},l.start-.05); if(i<L.length-1) tl.to(el,{opacity:0,duration:.15},l.end+.1);});
 document.querySelectorAll('.bk').forEach((c,i)=>tl.fromTo(c,{opacity:.06},{opacity:.22,duration:1.2+(i%4)*.3,yoyo:true,repeat:Math.ceil(D),ease:'sine.inOut'},(i%6)*.25));
 document.querySelectorAll('.pt').forEach((p,i)=>tl.fromTo(p,{y:0},{y:2300,x:(i%2?60:-60),duration:7+(i%5),ease:'none',repeat:Math.ceil(D/7)},(i%9)*.6));
 const show=(id,a,b)=>{tl.fromTo(id,{opacity:0,scale:.96},{opacity:1,scale:1,duration:.3,ease:'power2.out'},a); tl.to(id,{opacity:0,duration:.25},b);};
 const cut=[0,e(0)+.15,e(1)+.15,e(2)+.15,e(3)+.15,e(4)+.15,e(5)+.15,D+1];
 for(let k=0;k<7;k++) show('#s'+k,Math.max(0,cut[k]-.05),cut[k+1]-.2);
 tl.set('#s0',{opacity:1},0);
 // s0 boxes drop in quickly (fast hook)
 ['#b0','#b1','#b2'].forEach((b,k)=>{tl.fromTo(b,{y:-900,rotation:k%2?6:-6},{y:0,rotation:k%2?-3:3,duration:.45,ease:'bounce.out'},.05+k*.35); tl.to('#y'+k,{opacity:1,duration:.2},.35+k*.35);});
 tl.to('#b2',{rotation:-10,duration:.12,yoyo:true,repeat:5},1.6);
 // s1
 tl.fromTo('#n3',{scale:.3,opacity:0},{scale:1,opacity:1,duration:.5,ease:'back.out(2.5)'},cut[1]);
 tl.fromTo('#hand',{rotation:0,svgOrigin:'540 1090'},{rotation:360,duration:e(1)-s(1),ease:'none'},s(1));
 tl.fromTo('#cAI',{opacity:0,x:-80},{opacity:1,x:0,duration:.35,ease:'back.out(2)'},s(1)+1.4);
 tl.fromTo('#cHr',{opacity:0,x:80},{opacity:1,x:0,duration:.35,ease:'back.out(2)'},s(1)+2.6);
 // s2 blur -> restore
 tl.set('#photo',{filter:'blur(16px) sepia(.8) contrast(.7) brightness(1.1)'},0);
 const r0=s(2)+1.8; tl.set('#scan',{opacity:1},r0); tl.fromTo('#scan',{y:0},{y:570,duration:1.6,ease:'power1.inOut'},r0); tl.set('#scan',{opacity:0},r0+1.6);
 tl.to('#photo',{filter:'blur(0px) sepia(0) contrast(1) brightness(1)',duration:1.6,ease:'power1.inOut'},r0);
 tl.fromTo('#cRes',{opacity:0,y:30},{opacity:1,y:0,duration:.3},r0);
 tl.fromTo('#frame',{opacity:0,scale:1.25},{opacity:1,scale:1,duration:.5,ease:'back.out(1.6)'},e(2)-1.6);
 // s3 prompt then self-drawing poem
 tl.fromTo('#bubble',{opacity:0,y:30},{opacity:1,y:0,duration:.35},s(3)+.8); tl.to('#bubble',{opacity:0,y:-40,duration:.3},s(3)+3.4);
 tl.fromTo('#card',{opacity:0,rotationX:80,transformPerspective:900,transformOrigin:'50% 0%'},{opacity:1,rotationX:0,duration:.6,ease:'power3.out'},s(3)+3.5);
 document.querySelectorAll('.pl').forEach((p,i)=>{const n=p.getTotalLength(); p.style.strokeDasharray=n; tl.fromTo(p,{strokeDashoffset:n},{strokeDashoffset:0,duration:.35,ease:'none'},s(3)+4.0+i*.38);});
 // s4 chips + list with reasons
 ['#k0','#k1','#k2'].forEach((k,i)=>tl.fromTo(k,{opacity:0,scale:.5},{opacity:1,scale:1,duration:.3,ease:'back.out(2.5)'},s(4)+1.5+i*.55));
 for(let i=0;i<5;i++){tl.set('#li'+i,{top:i*112},0); tl.fromTo('#li'+i,{opacity:0,x:200},{opacity:1,x:0,duration:.3,ease:'power2.out'},s(4)+3.5+i*.42);}
 // s5 cursor approaches, cross draws
 tl.fromTo('#cursor',{x:0,y:0},{x:-330,y:-280,duration:1.1,ease:'power2.inOut'},s(5)+.2);
 ['#x1','#x2'].forEach((x,i)=>{tl.fromTo(x,{drawSVG:0,strokeDasharray:900,strokeDashoffset:900},{strokeDashoffset:0,duration:.3,ease:'power2.in'},s(5)+1.3+i*.25);});
 tl.to('#cursor',{x:-200,y:200,opacity:0,duration:.4},s(5)+1.9);
 tl.fromTo('#cNo',{opacity:0,y:30},{opacity:1,y:0,duration:.3,ease:'back.out(2)'},s(5)+1.9);
 // s6
 tl.fromTo('#endcard',{y:200,rotation:-4},{y:0,rotation:0,duration:.6,ease:'back.out(1.4)'},s(6));
 window.__timelines=window.__timelines||{}; window.__timelines['t2']=tl;
})();
</script></div></body></html>'''
for k, v in {"{{DUR}}": str(DUR), "{{BOKEH}}": bokeh, "{{GARLAND}}": garland, "{{PETALS}}": petals, "{{CAPS}}": caps, "{{POEM}}": poem,
             "{{LIST}}": lis, "{{LINES}}": json.dumps([{"start": l["start"], "end": l["end"]} for l in L])}.items():
    html = html.replace(k, v)
open("hf/index.html", "w").write(html); print("ok", DUR)
