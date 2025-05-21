import asyncio

from app.devices.device_service import DeviceService
from fastapi import WebSocket, status, WebSocketDisconnect

from app.events.emitters import event_bus
from app.ws.ws_connection import ws_manager


class WebSocketHandler:
    async def handle_connection(self, websocket: WebSocket, device_id: int, service: DeviceService):
        if not await self._authenticate(websocket, device_id, service):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        event_bus.emit('device_connected', device_id)
        await ws_manager.add(device_id, websocket)
        await self._listen(websocket, device_id)

    @staticmethod
    async def _authenticate(websocket: WebSocket, device_id: int, service: DeviceService) -> bool:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            event_bus.emit('device_timeout', device_id)
            return False

        token = data.get("auth_token") if isinstance(data, dict) else None
        verified = await service.verify_auth_token(device_id, token)
        if not verified:
            event_bus.emit('websocket_wrong_auth_token', device_id)
        return verified

    @staticmethod
    async def _listen(websocket: WebSocket, device_id: int):
        try:
            while True:
                msg = await websocket.receive_text()
                event_bus.emit('message_from_device', device_id, msg)
        except WebSocketDisconnect:
            event_bus.emit('websocket_disconnected', device_id)
            await ws_manager.remove(device_id)


websocket_handler = WebSocketHandler()
