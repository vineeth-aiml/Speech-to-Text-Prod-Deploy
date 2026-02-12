from fastapi import FastAPI, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .ws_stt import stt_ws_handler
from .storage import save_meeting, list_meetings, read_meeting, update_meeting
from .mom_engine import generate_mom
from .exports import to_txt, to_md
from .config import get_flag

app = FastAPI(title="Offline STT + MoM (V1/V2/V3 CPU)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoMRequest(BaseModel):
    meeting_id: str
    transcript: str
    language: str | None = None

@app.websocket("/ws/stt")
async def ws_stt(ws: WebSocket, room_id: str = Query("default"), lang: str = Query(None)):
    lang = lang or get_flag("LANG_DEFAULT", "auto")
    await stt_ws_handler(ws, room_id=room_id, lang=lang)

@app.get("/api/meetings")
def api_list():
    return list_meetings()

@app.get("/api/meetings/{meeting_id}")
def api_read(meeting_id: str):
    return read_meeting(meeting_id)

@app.post("/api/meetings/save")
def api_save(payload: dict):
    meeting_id = save_meeting(payload)
    return {"meeting_id": meeting_id}

@app.post("/api/mom")
def api_mom(req: MoMRequest):
    lang = (req.language or "auto").strip()
    mom = generate_mom(req.transcript, lang=lang)
    update_meeting(req.meeting_id, {"transcript": req.transcript, "language": lang, "mom": mom})
    return {"meeting_id": req.meeting_id, "mom": mom}

@app.get("/api/meetings/{meeting_id}/export.txt")
def export_txt(meeting_id: str):
    if not bool(get_flag("EXPORTS_ENABLED", True)):
        return {"error":"Exports disabled"}
    return to_txt(read_meeting(meeting_id))

@app.get("/api/meetings/{meeting_id}/export.md")
def export_md(meeting_id: str):
    if not bool(get_flag("EXPORTS_ENABLED", True)):
        return {"error":"Exports disabled"}
    return to_md(read_meeting(meeting_id))
