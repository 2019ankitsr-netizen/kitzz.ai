"""Voice tests: each series' test script at 3 speeds x 2 tones, with a slate card per take, as one MP4 per series."""
import os, sys, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import audio as A
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, s)

SPEEDS = [0.95, 1.0, 1.08]
# per series: (name, colours, tones[(label, tone, pitch)], lines[(voice, text, lang)])
TESTS = {
 "S1_how_things_work": ("S1 How Things Work", ((10, 18, 38), (255, 210, 60)),
   [("Warm", "warm", 0), ("Bright", "bright", 1)],
   [("am_michael", "This six-digit OTP reached you in about three seconds. Here's the route it took.", "en-us"),
    ("am_michael", "FASTag, | UPI, | ATM PINs, | DRS in cricket, | and Wi-Fi through walls. All coming up.", "en-us"),
    ("am_michael", "Save it. Send it to the friend who uses this every day.", "en-us")]),
 "S2_ai_ki_kahani": ("S2 AI Ki Kahani", ((246, 232, 205), (180, 70, 50)),
   [("Soft storyteller", "warm", -0.5), ("Lively", "bright", 1)],
   [("hf_alpha", "एक छोटे से शहर में, बबलू के फ़ोन में, एक अनजानी आवाज़ आई।", "hi"),
    ("hf_beta", "नमस्ते बबलू! मैं तारा हूँ। तुम्हारी ए आई दोस्त।", "hi"),
    ("hm_psi", "ए आई? मतलब तुम सोचती हो?", "hi"),
    ("hf_beta", "नहीं। मैं बस अंदाज़ा लगाती हूँ, कि अगला शब्द क्या होगा।", "hi")]),
 "S3_cctv_riddles": ("S3 CCTV Riddles", ((30, 32, 30), (255, 220, 80)),
   [("Low noir", "warm", -1.5), ("Crisp", "bright", 0)],
   [("bf_emma", "CCTV log. Camera three. Twenty-one fourteen.", "en-us"),
    ("am_michael", "Three friends paid ₹30 for a room. The real bill was ₹25.", "en-us"),
    ("am_michael", "So where did one rupee go? Answer in the comments.", "en-us")]),
 "S4_hook_shots": ("S4 Hook Shots", ((244, 242, 236), (225, 30, 30)),
   [("Punchy", "bright", 1), ("Confident", "warm", 0)],
   [("af_heart", "₹99. Not ₹100. Your brain fell for it.", "en-us"),
    ("af_heart", "The left digit decides, before you even finish reading.", "en-us"),
    ("af_heart", "Send this to someone. They won't believe it.", "en-us")]),
 "S5_space_transit": ("S5 Space Transit", ((4, 6, 14), (255, 180, 60)),
   [("Calm deep", "warm", -1), ("Clear", "bright", 0)],
   [("bf_emma", "Next stop. | Saturn's rings.", "en-us"),
    ("am_michael", "These rings are about 270,000 km across, yet mostly less than a hundred metres thick.", "en-us"),
    ("am_michael", "Chandrayaan, Voyager, and the Boötes Void are on this line too. Save this ride.", "en-us")]),
}

def slate(title, bg, acc, take, label, speed, voices, path):
    W, H = 1080, 1920; im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    fg = (20, 20, 20) if sum(bg) > 400 else (255, 255, 255)
    d.text((90, 330), "VOICE TEST", font=F("Inter-Bold.otf", 40), fill=acc)
    d.text((90, 390), title, font=F("InterDisplay-Black.otf", 76), fill=fg)
    d.text((90, 560), f"Take {take}", font=F("InterDisplay-Black.otf", 150), fill=acc)
    d.text((90, 760), f"{label}", font=F("InterDisplay-ExtraBold.otf", 84), fill=fg)
    d.text((90, 870), f"speed {speed:.2f}×", font=F("InterDisplay-ExtraBold.otf", 84), fill=fg)
    d.text((90, 1010), "voices: " + ", ".join(voices), font=F("Inter-Medium.otf", 40), fill=fg)
    d.text((90, 1080), "Reply with the take number you like.", font=F("Inter-Medium.otf", 40), fill=fg)
    im.save(path)

def run(out):
    os.makedirs(out, exist_ok=True)
    for key, (title, (bg, acc), tones, lines) in TESTS.items():
        segs, take = [], 0
        for label, tone, pitch in tones:
            for sp in SPEEDS:
                take += 1
                parts = [A.silence(0.5)]
                for v, txt, lang in lines:
                    parts += [A.say(txt, v, sp, lang, pitch, tone), A.silence(0.45)]
                parts += [A.sfx("chime"), A.silence(0.4)]
                a = np.concatenate(parts); wav = f"{out}/{key}_t{take}.wav"; sf.write(wav, a, A.SR)
                png = f"{out}/{key}_t{take}.png"; slate(title, bg, acc, take, label, sp, sorted({l[0] for l in lines}), png)
                seg = f"{out}/{key}_t{take}.mp4"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", png, "-i", wav,
                                "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                                "-ar", "48000", "-shortest", seg], check=True)
                segs.append(seg)
        lst = f"{out}/{key}.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
        tmp = f"{out}/{key}_raw.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", tmp], check=True)
        final = f"{out}/VoiceTest_{key}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
                        "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", final], check=True)
        print("done", final)

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "voicetests")
