from typing import Dict, Set
from fastapi import WebSocket
import asyncio

class RoomHub:
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def join(self, room_id: str, ws: WebSocket):
        async with self.lock:
            self.rooms.setdefault(room_id, set()).add(ws)

    async def leave(self, room_id: str, ws: WebSocket):
        async with self.lock:
            if room_id in self.rooms and ws in self.rooms[room_id]:
                self.rooms[room_id].remove(ws)
            if room_id in self.rooms and not self.rooms[room_id]:
                self.rooms.pop(room_id, None)

    async def broadcast(self, room_id: str, message: dict):
        async with self.lock:
            targets = list(self.rooms.get(room_id, set()))
        for ws in targets:
            try:
                await ws.send_json(message)
            except Exception:
                pass

hub = RoomHub()
