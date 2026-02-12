import requests, json
from .config import PROMPTS_DIR, get_flag

DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"

def _prompt(transcript: str, lang: str) -> str:
    tpl_path = PROMPTS_DIR / "mom_v2_prompt.txt"
    tpl = tpl_path.read_text(encoding="utf-8") if tpl_path.exists() else "Return JSON MoM."
    return tpl.replace("{{LANG}}", lang or "auto").replace("{{TRANSCRIPT}}", transcript)

def generate_mom_v2(transcript: str, lang: str) -> dict:
    model = get_flag("OLLAMA_MODEL", "qwen2.5:3b-instruct")
    payload = {"model": model, "prompt": _prompt(transcript, lang), "stream": False,
               "options": {"temperature": 0.2, "num_ctx": 4096}}
    r = requests.post(DEFAULT_OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    out = r.json().get("response", "").strip()
    try:
        parsed = json.loads(out)
        if isinstance(parsed, dict):
            parsed["engine"] = "v2-ollama"
            parsed["language"] = lang
            return parsed
    except Exception:
        pass
    return {"engine":"v2-ollama","language":lang,"summary":[out[:500]],"decisions":[],"action_items":[],"risks":[],"next_steps":[]}
