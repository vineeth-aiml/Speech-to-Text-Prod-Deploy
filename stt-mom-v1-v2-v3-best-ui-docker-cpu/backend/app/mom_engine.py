from .config import get_flag
from .mom_engine_v1 import generate_mom_v1
from .mom_engine_v2_ollama import generate_mom_v2

def generate_mom(transcript: str, lang: str):
    mode = str(get_flag("MOM_ENGINE", "v2")).lower().strip()
    if mode == "v1":
        return generate_mom_v1(transcript, lang)
    try:
        return generate_mom_v2(transcript, lang)
    except Exception:
        return generate_mom_v1(transcript, lang)
