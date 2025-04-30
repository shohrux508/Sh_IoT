import asyncio
from datetime import datetime, timedelta

from fastapi import WebSocket


class DeviceSession:
    HEARTBEAT_INTERVAL = 10  # секунд
    HEARTBEAT_TIMEOUT = 30  # секунд

    def __init__(self, device_id: int, websocket: WebSocket, event_handler=None):
        self.device_id = device_id
        self.websocket = websocket
        self.event_handler = event_handler
        self.last_pong_time = datetime.now()
        self.running = True
        self.manager = device_session_manager

    async def start(self):
        try:
            await asyncio.gather(
                self.ping_loop(),
                self.listen_loop(),
            )
        except Exception as e:
            print(f"[{self.device_id}] Ошибка в работе устройства: {e}")
            self.running = False
        finally:
            if not self.running:  # только если сессия остановлена из-за сбоя
                await self.manager.unregister(self.device_id)
                print(f"[{self.device_id}] Сессия завершена и удалена.")

    async def ping_loop(self):
        while self.running:
            await asyncio.sleep(self.HEARTBEAT_INTERVAL)
            await self.websocket.send_text("ping")

            if datetime.now() - self.last_pong_time > timedelta(seconds=self.HEARTBEAT_TIMEOUT):
                print(f'Текущее время: {datetime.now()}\n'
                      f'Время последнего pong\'а: {self.last_pong_time}')
                print(f"[{self.device_id}] Таймаут heartbeat")
                self.running = False

    async def listen_loop(self):
        while self.running:
            try:
                message = await self.websocket.receive_text()
                print(message)
                self.last_pong_time = datetime.now()
            except:
                await asyncio.sleep(3)

    async def send_command(self, cmd: str):
        try:
            await self.websocket.send_text(cmd)
        except Exception as e:
            print(f"[{self.device_id}] Ошибка отправки команды: {e}")

    async def close(self):
        # Гарантируем закрытие независимо от флага running
        self.running = False
        try:
            await self.websocket.close()
        except Exception:
            pass
        print(f"[{self.device_id}] Сессия завершена")


class DeviceConnectionManager:
    def __init__(self, event_handler=None):
        self.active_devices: dict[int, DeviceSession] = {}
        self.event_handler = event_handler

    async def register(self, device_id: int, websocket: WebSocket):
        session = DeviceSession(device_id=device_id, websocket=websocket, event_handler=self.event_handler)
        self.active_devices[device_id] = session

    async def unregister(self, device_id: int):
        session = self.active_devices.pop(device_id, None)
        if session:
            await session.close()

    async def get(self, device_id: int) -> DeviceSession | None:
        return self.active_devices.get(device_id)

    async def all_ids(self) -> list[int]:
        return list(self.active_devices.keys())


device_session_manager = DeviceConnectionManager()
