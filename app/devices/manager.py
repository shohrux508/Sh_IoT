from typing import Dict, Optional
from fastapi import WebSocket
from asyncio import Lock


class DeviceConnectionManager:
    def __init__(self):
        self._connections: Dict[int, WebSocket] = {}
        self._lock = Lock()

    async def register(self, device_id: int, websocket: WebSocket):
        async with self._lock:
            self._connections[device_id] = websocket

    async def unregister(self, device_id: int):
        async with self._lock:
            self._connections.pop(device_id, None)

    async def get(self, device_id: int) -> Optional[WebSocket]:
        async with self._lock:
            return self._connections.get(device_id)

    async def all_ids(self) -> list[int]:
        async with self._lock:
            return list(self._connections.keys())

    async def exists(self, device_id: int) -> bool:
        async with self._lock:
            return device_id in self._connections
