import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data/meetings")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_meeting(meeting: dict) -> str:
    meeting_id = meeting.get("id") or datetime.utcnow().strftime("%Y%m%d%H%M%S")
    meeting["id"] = meeting_id
    (DATA_DIR / f"{meeting_id}.json").write_text(
        json.dumps(meeting, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return meeting_id

def list_meetings():
    items = []
    for p in sorted(DATA_DIR.glob("*.json"), reverse=True):
        try:
            items.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return items

def read_meeting(meeting_id: str):
    return json.loads((DATA_DIR / f"{meeting_id}.json").read_text(encoding="utf-8"))

def update_meeting(meeting_id: str, patch: dict):
    path = DATA_DIR / f"{meeting_id}.json"
    m = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"id": meeting_id}
    m.update(patch)
    save_meeting(m)
    return m
