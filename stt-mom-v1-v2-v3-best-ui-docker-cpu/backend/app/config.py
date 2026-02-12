from pathlib import Path
import yaml

FLAGS_PATH = Path("ops/feature_flags.yaml")
PROMPTS_DIR = Path("prompts")

def load_flags() -> dict:
    if FLAGS_PATH.exists():
        return yaml.safe_load(FLAGS_PATH.read_text(encoding="utf-8")) or {}
    return {}

def get_flag(name: str, default=None):
    return load_flags().get(name, default)
