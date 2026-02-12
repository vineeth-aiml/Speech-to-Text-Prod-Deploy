from pathlib import Path
from faster_whisper import WhisperModel
from .config import get_flag

class STTEngine:
    def __init__(self):
        model_name = get_flag("WHISPER_MODEL", "small")
        models_dir = Path("models/whisper")
        local_path = models_dir / model_name
        model_ref = str(local_path) if local_path.exists() else model_name
        self.model = WhisperModel(model_ref, device="cpu", compute_type="int8")

    def transcribe_file(self, wav_path: str, language: str = "auto"):
        lang = None if (language in (None, "", "auto")) else language
        segments, info = self.model.transcribe(wav_path, vad_filter=True, language=lang)
        parts = []
        for seg in segments:
            t = (seg.text or "").strip()
            if t:
                parts.append(t)
        return " ".join(parts).strip(), {
            "language": getattr(info, "language", None),
            "duration": getattr(info, "duration", None)
        }
