from collections import defaultdict
from app.events.emitters import event_bus
from fastapi import WebSocket
import asyncio


class WSConnectionManager:
    def __init__(self):
        self.active = dict[str, WebSocket] = {}
        self.pending = dict[str, dict[str, asyncio.Future]] = defaultdict(dict)

    async def connect(self, device_id: int, ws: WebSocket):
        self.active[device_id] = ws
        event_bus.emit('device_connected', device_id)

    async def disconnect(self, device_id: int) -> bool:
        ws = self.active.pop(device_id, None)
        if not ws:
            return False
        await ws.close()
        event_bus.emit('device_disconnected', device_id)
        return True

    async def send_text(self, device_id: int, payload: str):
        ws = self.active.get(device_id)
        if not ws:
            event_bus.emit('message_failed', device_id, payload)
            return False
        await ws.send_text(payload)
        event_bus.emit('message_sent', device_id, payload)
        return True
