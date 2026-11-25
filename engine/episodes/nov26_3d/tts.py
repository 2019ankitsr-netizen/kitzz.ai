import os, espeakng_loader as e
os.environ['PHONEMIZER_ESPEAK_LIBRARY']=e.get_library_path()
os.environ['ESPEAK_DATA_PATH']=e.get_data_path()
from phonemizer.backend.espeak.wrapper import EspeakWrapper
EspeakWrapper.set_library(e.get_library_path())
try: EspeakWrapper.set_data_path(e.get_data_path())
except Exception: pass
from kokoro import KPipeline
import soundfile as sf, numpy as np, sys, json
def say(text, voice='hm_omega', speed=1.0, lang='h'):
    p=KPipeline(lang_code=lang)
    return np.concatenate([a.numpy() if hasattr(a,'numpy') else a for _,_,a in p(text, voice=voice, speed=speed)])
if __name__=='__main__':
    a=say(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else 'hm_omega')
    sf.write(sys.argv[3] if len(sys.argv)>3 else 'vo/test.wav', a, 24000); print(len(a)/24000)
