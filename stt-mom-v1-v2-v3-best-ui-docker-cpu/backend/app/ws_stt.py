import os, wave, tempfile
from fastapi import WebSocket
from .stt_engine import STTEngine
from .config import get_flag
from .rooms import hub

engine = STTEngine()

class WavAssembler:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        self.path = self.tmp.name
        self.tmp.close()
        wf = wave.open(self.path, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.sample_rate)
        wf.writeframes(b"")
        wf.close()

    def append_pcm16(self, pcm_bytes: bytes):
        wf = wave.open(self.path, "rb")
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())
        wf.close()
        wf = wave.open(self.path, "wb")
        wf.setparams(params)
        wf.writeframes(frames + pcm_bytes)
        wf.close()

    def cleanup(self):
        try: os.remove(self.path)
        except Exception: pass

async def stt_ws_handler(ws: WebSocket, room_id: str, lang: str):
    await ws.accept()
    await hub.join(room_id, ws)

    assembler = WavAssembler(sample_rate=16000)
    chunk_count = 0
    last_sent = ""
    partial_every = int(get_flag("PARTIAL_EVERY_N_CHUNKS", 10))
    do_broadcast = bool(get_flag("ROOM_BROADCAST", True))

    try:
        while True:
            pcm = await ws.receive_bytes()
            assembler.append_pcm16(pcm)
            chunk_count += 1
            if chunk_count % partial_every == 0:
                text, meta = engine.transcribe_file(assembler.path, language=lang)
                if text and text != last_sent:
                    last_sent = text
                    msg = {"type":"partial","room_id":room_id,"text":text,"meta":meta}
                    await ws.send_json(msg)
                    if do_broadcast:
                        await hub.broadcast(room_id, msg)
    except Exception:
        pass
    finally:
        assembler.cleanup()
        await hub.leave(room_id, ws)
        try: await ws.close()
        except Exception: pass
