# S1 ep09: How a touchscreen feels your finger (Blender)

Same S1 product-macro look. A tilted glossy phone with its capacitive sensing grid lifted out above the glass (exploded view):
cyan rows, purple columns, 91 glowing crossing nodes (one shared Object-Info emission material; brightness = stored charge).
A stylised finger pulls charge (nodes dim to ember, sparks stream into the tip); a scan bar finds the dip; swipe and pinch;
a glove does nothing, a sausage works; a 1965 radar scope for the origin.

Pipeline (WORK=/home/claude/ts): `vo.py` → `scene.py $WORK/frames --res 45 --spp 6 --thr 0.08` → `audio.py` → `compose.py video out.mp4`.
