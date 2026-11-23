# S1 ep08: How a microwave heats food (Blender)

Same S1 product-macro look as ep06/ep07 (bpy 5.1, Cycles CPU, AgX, DOF). Cup of chai on a turntable, glossy H2O molecules,
purple microwave tubes from a finned magnetron, hot/cold spots on the plate, a spoon that sparks, Percy Spencer's melting chocolate.

Beats: payoff-first hook (glowing molecules over steaming chai, "your food heats itself") → water = tiny magnet (+/−) → magnetron
→ field flips 2.45 billion times/s, molecules twist → twisting = jostling = heat → hot/cold spots, plate spins → metal sparks
→ 1945 Percy Spencer → send CTA, loops back to the hook (microwave "ding" on both ends).

Pipeline (WORK=/home/claude/mw): `vo.py` → `scene.py $WORK/frames --res 45 --spp 6 --thr 0.08` (~5 s/frame on 2 CPUs)
→ `audio.py` → `compose.py video out.mp4`. Camera holds each beat with a slow push-in, then glides to the next.
