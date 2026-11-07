"""S3 CCTV Riddles voice test, round 2: new detective + CCTV-log voice pairs (speed 1.0)."""
import os, sys, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
import audio as A
from voicetest import slate
LINES = [("log", "CCTV log. Camera three. Twenty-one fourteen."),
         ("det", "Three friends paid ₹30 for a room. The real bill was ₹25."),
         ("det", "So where did one rupee go? Answer in the comments.")]
TAKES = [  # (label, detective voice, log voice, tone, pitch, speed)
    ("George · British, measured", "bm_george", "bf_isabella", "warm", 0, 1.0),
    ("Lewis · British, deep", "bm_lewis", "bf_emma", "warm", 0, 1.0),
    ("Onyx · deep US", "am_onyx", "af_sarah", "warm", 0, 1.0),
    ("Fenrir · gruff US", "am_fenrir", "bf_isabella", "warm", -0.5, 1.0),
    ("Daniel · British, calm", "bm_daniel", "af_sarah", "warm", 0, 1.0),
    ("Fable · British storyteller", "bm_fable", "bf_emma", "warm", 0, 1.0),
]
def run(out):
    os.makedirs(out, exist_ok=True); segs = []
    for i, (label, det, log, tone, pitch, sp) in enumerate(TAKES, 1):
        parts = [A.silence(.5)]
        for who, txt in LINES:
            v = det if who == "det" else log
            parts += [A.say(txt, v, sp, "en-us", pitch if who == "det" else 0, tone), A.silence(.45)]
        parts += [A.sfx("chime"), A.silence(.4)]
        wav = f"{out}/S3b_t{i}.wav"; sf.write(wav, np.concatenate(parts), A.SR)
        png = f"{out}/S3b_t{i}.png"; slate("S3 CCTV Riddles · round 2", (30, 32, 30), (255, 220, 80), i, label, sp, [det, log], png)
        seg = f"{out}/S3b_t{i}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", png, "-i", wav, "-c:v", "libx264",
                        "-tune", "stillimage", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-shortest", seg], check=True)
        segs.append(seg)
    lst = f"{out}/S3b.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "copy", "-af",
                    "loudnorm=I=-14:TP=-1.5:LRA=9", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart",
                    f"{out}/VoiceTest_S3_cctv_riddles_round2.mp4"], check=True)
if __name__ == "__main__": run(sys.argv[1])
