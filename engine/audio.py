"""Audio for @kitzz.ai reels: Kokoro voice lines, voice polish, synthesized music beds, SFX, mix + -14 LUFS.
Kokoro runs through kokoro-onnx (model files kokoro-v1.0.onnx + voices-v1.0.bin in $KOKORO_DIR)."""
import os, re, subprocess, tempfile, numpy as np, soundfile as sf

SR = 24000
KDIR = os.environ.get("KOKORO_DIR", "/home/claude/models")
_K = None
def K():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(f"{KDIR}/kokoro-v1.0.onnx", f"{KDIR}/voices-v1.0.bin")
    return _K

# ---- pronunciation: spoken text only; captions keep the normal spelling ----
EN_FIX = [(r"\bOTPs\b", "O-T-Ps"), (r"\bOTP\b", "O-T-P"), (r"\bUPI\b", "U-P-I"), (r"\bFASTag\b", "Fast Tag"),
          (r"\bDRS\b", "D-R-S"), (r"\bSMS\b", "S-M-S"), (r"\bTRAI\b", "tray"), (r"\bDLT\b", "D-L-T"),
          (r"\bCCTV\b", "C-C-T-V"), (r"\bNPCI\b", "N-P-C-I"), (r"\bNETC\b", "N-E-T-C"), (r"\bRFID\b", "R-F-I-D"),
          (r"\bBBC\b", "B-B-C"), (r"\bRAM\b", "ram"), (r"\bNYU\b", "N-Y-U"), (r"\bNASA\b", "nasa"), (r"Chang'e", "Chahng-uh"),
          (r"(\d+) KB\b", r"\1 kilobytes"), (r"(\d+) GB\b", r"\1 gigabytes"), (r"\bAI\b", "A-I"), (r"\bkm\b", "kilometres"), (r"\bISRO\b", "is-roh"),
          (r"₹\s?([\d,]+)", lambda m: m.group(1).replace(",", "") + (" rupee" if m.group(1) == "1" else " rupees"))]
HI_PH = [("ˈeː ˈaːi", "ˌeɪˈaɪ"), ("eːˈaːi", "ˌeɪˈaɪ")]   # write AI as "ए आई" in Hindi scripts
def en_spoken(s):
    for a, b in EN_FIX: s = re.sub(a, b, s)
    return s
def phonemes(text, lang="en-us"): return K().tokenizer.phonemize(en_spoken(text) if lang.startswith("en") else text, lang)

def _ff(inp, out, af):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", inp, "-af", af, "-ar", str(SR), "-ac", "1", out], check=True)

def polish(a, pitch=0.0, tone="warm"):
    """Gentle voice chain: high-pass, presence/warmth EQ, de-esser, compression; optional ±semitone pitch shift."""
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/i.wav", a, SR)
        eq = "equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=1" if tone == "warm" else \
             "equalizer=f=180:t=q:w=1:g=-1,equalizer=f=3500:t=q:w=1:g=2.5"
        chain = f"highpass=f=75,{eq},deesser=i=0.4:m=0.5:f=0.5,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2"
        if pitch: chain = f"rubberband=pitch={2 ** (pitch / 12):.5f}:formant=preserved," + chain
        _ff(f"{d}/i.wav", f"{d}/o.wav", chain)
        b, _ = sf.read(f"{d}/o.wav", dtype="float32")
    return b

# ---------------- natural Indian voices: AI4Bharat Indic Parler-TTS ----------------
# voice="parler:<Speaker>:<mood>"  e.g. "parler:Rohit:calm", "parler:Divya:bright". Works for Hindi, Hinglish and Indian English.
# Slow on CPU (~10x real time) but far more natural than Kokoro. Needs torch + parler-tts (see README).
PARLER_REPO = os.environ.get("PARLER_REPO", "RXD03/indic-parler-tts")   # Apache-2.0 mirror of ai4bharat/indic-parler-tts
PARLER_MOODS = {
    "calm": "{s} speaks in a warm, expressive storytelling voice at a moderate pace, with clear audio and very little background noise.",
    "tense": "{s} speaks in a deep, dramatic and intense storytelling voice at a moderate pace, with clear audio and very little background noise.",
    "bright": "{s} speaks in a warm, joyful and expressive storytelling voice at a moderate pace, with clear audio and very little background noise.",
    "news": "{s} speaks in a clear, confident and energetic news presenter voice at a slightly fast pace, with very clear audio and no background noise.",
}
_P = {}
def _parler():
    if not _P:
        import torch
        from transformers import AutoTokenizer
        from parler_tts import ParlerTTSForConditionalGeneration
        torch.set_num_threads(max(1, os.cpu_count() or 2))
        m = ParlerTTSForConditionalGeneration.from_pretrained(PARLER_REPO)
        _P.update(m=m, tok=AutoTokenizer.from_pretrained(PARLER_REPO), dtok=AutoTokenizer.from_pretrained(m.config.text_encoder._name_or_path), torch=torch)
    return _P

def say_parler(text, speaker="Rohit", mood="calm", seed=7):
    P = _parler(); torch = P["torch"]; torch.manual_seed(seed)
    ids = P["dtok"](PARLER_MOODS.get(mood, mood).format(s=speaker), return_tensors="pt"); pids = P["tok"](text.replace("|", ","), return_tensors="pt")
    with torch.no_grad():
        a = P["m"].generate(input_ids=ids.input_ids, attention_mask=ids.attention_mask,
                            prompt_input_ids=pids.input_ids, prompt_attention_mask=pids.attention_mask).cpu().numpy().squeeze().astype(np.float32)
    sr = P["m"].config.sampling_rate
    if sr != SR:
        import librosa; a = librosa.resample(a, orig_sr=sr, target_sr=SR).astype(np.float32)
    return trim(a, 0.01)

def say(text, voice, speed=1.0, lang="en-us", pitch=0.0, tone="warm"):
    """One line. Long lines are split into short phrases (6-10 words) joined with comma pauses for a smoother read."""
    if voice.startswith("parler:"):
        _, spk, mood = (voice.split(":") + ["calm"])[:3]
        txt = en_spoken(text) if lang.startswith("en") else text.replace("ए आई", "एआई")   # Parler stretches "ए आई"; "एआई" reads as AI
        a = say_parler(txt, spk, mood)
        if abs(speed - 1.0) > .01:
            import librosa; a = librosa.effects.time_stretch(a, rate=speed).astype(np.float32)
        return polish(a, pitch, tone)
    spoken = en_spoken(text) if lang.startswith("en") else text
    # "|" = short breath (0.16 s) inside a sentence; sentence ends get 0.32 s
    parts = [p.strip() for p in re.split(r"(?<=[.!?…।|])\s+", spoken) if p.strip()]
    out = []
    for i, p in enumerate(parts):
        brk = p.endswith("|"); p = p.rstrip("|").strip()
        if not p: continue
        if lang == "hi":   # Hindi: phonemize, then fix acronyms espeak gets wrong (ए आई -> "ay-eye")
            ph = K().tokenizer.phonemize(p, "hi")
            for x, y in HI_PH: ph = ph.replace(x, y)
            a, sr = K().create(ph, voice=voice, speed=speed, lang=lang, is_phonemes=True)
        else:
            a, sr = K().create(p, voice=voice, speed=speed, lang=lang)
        a = trim(a)
        out.append(a)
        if i < len(parts) - 1: out.append(np.zeros(int(SR * (0.16 if brk else 0.32)), np.float32))
    a = np.concatenate(out).astype(np.float32)
    return polish(a, pitch, tone)

def trim(a, thr=0.008):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx): return a
    s, e = max(0, idx[0] - int(SR * 0.02)), min(len(a), idx[-1] + int(SR * 0.06))
    return a[s:e]

def silence(sec): return np.zeros(int(SR * sec), np.float32)

# ---------------- music + sfx (all synthesized) ----------------
def _env(n, a=0.01, r=0.3):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4)); return e.astype(np.float32)
def note(f, dur, kind="pluck", vol=0.3):
    n = int(SR * dur); t = np.arange(n) / SR
    if kind == "pluck":   w = (np.sin(2*np.pi*f*t) + .35*np.sin(4*np.pi*f*t) + .12*np.sin(6*np.pi*f*t)) * _env(n, .004, dur*.35)
    elif kind == "mallet": w = (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*f*3.99*t)*np.exp(-t*18)) * _env(n, .002, dur*.4)
    elif kind == "pad":
        w = sum(np.sin(2*np.pi*f*(1+dt)*t + p) for dt, p in ((0, 0), (.004, 1), (-.004, 2), (.5, .3))) / 3.2
        w *= np.minimum(1, t/0.6) * np.minimum(1, (dur - t)/0.6).clip(0, 1)
    elif kind == "bass":  w = np.tanh(2*np.sin(2*np.pi*f*t)) * _env(n, .005, dur*.6)
    elif kind == "bell":  w = (np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*f*2.76*t) + .25*np.sin(2*np.pi*f*5.4*t)) * _env(n, .002, dur*.5)
    return (w * vol).astype(np.float32)
def kick(vol=.6):
    n = int(SR*.35); t = np.arange(n)/SR; f = 45 + 110*np.exp(-t*30)
    return (np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9) * vol).astype(np.float32)
def hat(vol=.08):
    n = int(SR*.06); return (np.random.default_rng(1).standard_normal(n) * np.exp(-np.arange(n)/SR*70) * vol).astype(np.float32)
def snare(vol=.25):
    n = int(SR*.2); t = np.arange(n)/SR; r = np.random.default_rng(2).standard_normal(n)
    return ((r*.7 + np.sin(2*np.pi*190*t)*.5) * np.exp(-t*22) * vol).astype(np.float32)
def place(buf, clip, t):
    i = int(t*SR); j = min(len(buf), i+len(clip))
    if i < len(buf) and j > i: buf[i:j] += clip[:j-i]
def mtof(m): return 440 * 2 ** ((m - 69) / 12)

STYLES = {  # bpm, chord roots (midi), chord quality, lead kind, drums
    "xray":   dict(bpm=104, prog=[57, 53, 60, 55], q=[0, 3, 7, 10], lead="pluck", drums="pulse"),
    "story":  dict(bpm=92,  prog=[60, 55, 57, 53], q=[0, 4, 7, 11], lead="mallet", drums="soft"),
    "cctv":   dict(bpm=84,  prog=[50, 50, 46, 48], q=[0, 3, 7], lead="bell", drums="tick"),
    "swiss":  dict(bpm=120, prog=[52, 52, 48, 50], q=[0, 3, 7], lead="pluck", drums="hard"),
    "festive": dict(bpm=96, prog=[60, 65, 67, 60], q=[0, 4, 7, 11, 14], lead="bell", drums="dholak"),
    "space":  dict(bpm=76,  prog=[57, 53, 48, 55], q=[0, 7, 14, 16], lead="bell", drums="none"),
}
def music(style, dur, seed=0, drop=()):
    """Loopable synthesized bed. drop = [(t0, t1)] windows where the music falls away under key lines."""
    S = STYLES[style]; rng = np.random.default_rng(seed); beat = 60 / S["bpm"]; bar = beat * 4
    buf = np.zeros(int(SR * (dur + 2)), np.float32); t = 0.0; i = 0
    while t < dur:
        root = S["prog"][i % len(S["prog"])]
        for iv in S["q"]: place(buf, note(mtof(root + iv - 12 + (12 if style == "space" else 0)), bar + .3, "pad", .05), t)
        place(buf, note(mtof(root - 24), bar * .95, "bass", .10 if style != "space" else .05), t)
        steps = 8 if style in ("xray", "swiss") else 4
        for k in range(steps):
            if rng.random() < (.85 if style != "cctv" else .5):
                m = root + S["q"][rng.integers(len(S["q"]))] + 12 * rng.integers(0, 2)
                place(buf, note(mtof(m), beat * 4 / steps * 1.6, S["lead"], .07 if style != "space" else .05), t + k * bar / steps)
        for b in range(4):
            tb = t + b * beat; dr = S["drums"]
            if dr in ("pulse", "hard"): place(buf, kick(.5 if dr == "hard" else .35), tb)
            if dr == "hard" and b % 2: place(buf, snare(.22), tb)
            if dr in ("pulse", "hard", "soft"): place(buf, hat(.05 if dr == "soft" else .07), tb + beat / 2)
            if dr == "soft" and b == 0: place(buf, kick(.22), tb)
            if dr == "tick": place(buf, hat(.06), tb); place(buf, hat(.03), tb + beat / 2)
            if dr == "dholak":
                place(buf, kick(.30 if b % 2 == 0 else .18), tb); place(buf, snare(.08), tb + beat * .5)
                if b == 3: place(buf, snare(.07), tb + beat * .75)
        t += bar; i += 1
    buf = buf[:int(SR * dur)]
    env = np.ones_like(buf)
    for t0, t1 in drop:
        a, b = int(t0 * SR), int(t1 * SR); env[a:b] = .25
    k = int(SR * .25); env = np.convolve(env, np.ones(k) / k, mode="same")
    fade = np.minimum(1, np.arange(len(buf)) / (SR * .3)) * np.minimum(1, (len(buf) - np.arange(len(buf))) / (SR * .6))
    return (buf * env * fade).astype(np.float32)

def sfx(kind):
    if kind == "whoosh":
        n = int(SR*.45); t = np.arange(n)/SR; r = np.random.default_rng(5).standard_normal(n)
        r = np.convolve(r, np.ones(6)/6, "same"); return (r * np.sin(np.pi*t/.45)**2 * .18).astype(np.float32)
    if kind == "tick": return note(2400, .05, "bell", .12)
    if kind == "pop": return note(880, .12, "mallet", .25)
    if kind == "chime": return np.concatenate([note(mtof(76), .25, "bell", .15), note(mtof(83), .5, "bell", .15)])
    if kind == "beep": return note(1000, .18, "pluck", .15)
    if kind == "dingdong": return np.concatenate([note(mtof(76), .45, "bell", .22), note(mtof(72), .8, "bell", .22)])
    if kind == "hit":
        k = kick(.6); s_ = snare(.2); k[:len(s_)] += s_; return k
    if kind == "static":
        n = int(SR*.3); return (np.random.default_rng(9).standard_normal(n) * .05).astype(np.float32)
    raise ValueError(kind)

def mixdown(voice, music_bed, sfx_track, out_wav, music_db=-18):
    """Voice on top, music ducked under the voice (sidechain) at ~-18 dB, SFX, then two-pass loudnorm to -14 LUFS."""
    n = max(len(voice), len(music_bed), len(sfx_track))
    pad = lambda a: np.pad(a, (0, n - len(a)))
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/v.wav", pad(voice), SR); sf.write(f"{d}/m.wav", pad(music_bed), SR); sf.write(f"{d}/s.wav", pad(sfx_track), SR)
        g = 10 ** (music_db / 20) / max(1e-6, np.sqrt(np.mean(music_bed ** 2)) / 0.1)
        fc = (f"[1:a]volume={g:.4f}[m];[0:a]asplit[v1][v2];[m][v2]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=300[md];"
              f"[v1][md][2:a]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.9[o]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/v.wav", "-i", f"{d}/m.wav", "-i", f"{d}/s.wav",
                        "-filter_complex", fc, "-map", "[o]", "-ar", "48000", f"{d}/mix.wav"], check=True)
        loudnorm(f"{d}/mix.wav", out_wav)

def loudnorm(inp, out, I=-14, TP=-1.5, LRA=9):
    import json
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", inp, "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    af = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", inp, "-af", af, "-ar", "48000", out], check=True)

def lufs(path):
    import pyloudnorm as pyln
    a, sr = sf.read(path); return pyln.Meter(sr).integrated_loudness(a)
