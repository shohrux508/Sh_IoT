import asyncio
from datetime import datetime, timedelta

from app.events.emitters import event_bus
from typing import Dict
from fastapi import WebSocket
import json
from app.logger_module.logger_utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


class WSConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}
        self.pending = {}

    async def connect(self, device_id: str, ws: WebSocket):
        self.active[device_id] = ws
        event_bus.emit('device_connected', device_id)

    async def disconnect(self, device_id: str) -> bool:
        try:
            self.active.pop(device_id, None)
            event_bus.emit('device_disconnected', device_id)
        except:
            return False
        return True

    async def get(self, device_id) -> WebSocket | None:
        return self.active.get(device_id)

    async def get_list(self) -> Dict:
        return self.active

    async def broadcast(self, message: dict | str):
        payload = json.dumps(message, ensure_ascii=False) if not isinstance(message, str) else message
        for ws in self.active.values():
            await ws.send_text(payload)

    async def send_personal(self, device_id: str, message: dict | str, request_id: str = None,
                            timeout: float = 5) -> dict | None:
        ws = self.active.get(device_id)
        if not ws:
            event_bus.emit('message_failed', device_id, message)
            raise RuntimeError(f'Websocket for device {device_id} not found')
        if isinstance(message, str):
            payload = message
        else:
            payload = json.dumps(message, ensure_ascii=False)

        await ws.send_text(payload)
        request_id = message.get('request_id')
        if request_id:
            future = asyncio.get_event_loop().create_future()
            self.pending.setdefault(device_id, {})[request_id] = future
            try:
                response = await asyncio.wait_for(future, timeout=timeout)
                return response
            except asyncio.TimeoutError:
                logger.warning(f"Device {device_id} did not respond in time.")
            finally:
                self.pending[device_id].pop(request_id, None)

        return None

    async def set_response(self, device_id: str, message: dict | str):
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except Exception as e:
                logger.error(f"Ошибка при разборе сообщения от {device_id}: {e}\n{message}")
                return
        if 'request_id' not in message:
            return
        request_id = message.get('request_id')
        if request_id and device_id in self.pending and request_id in self.pending[device_id]:
            future = self.pending[device_id][request_id]
            if not future.done():
                future.set_result(message)


ws_manager = WSConnectionManager()
