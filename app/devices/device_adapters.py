from abc import ABC, abstractmethod
import json


class BaseDevice(ABC):
    def __init__(self, device_id, device_type, websocket):
        self.device_id = device_id
        self.device_type = device_type
        self.websocket = websocket

    async def send_data_ws(self, data):
        try:
            self.websocket.send_text(data=data)
        except Exception as e:
            print(f'Ошибка при отправке через Websocket: {e}')

    @abstractmethod
    async def turn_on(self):
        pass

    @abstractmethod
    async def turn_off(self):
        pass

    @abstractmethod
    async def set_state(self, state):
        pass

    @abstractmethod
    async def set_timer(self, start_time, stop_time):
        pass

    @abstractmethod
    async def get_state(self):
        pass


class DeviceCommands(BaseDevice):

    async def turn_on(self):
        data = {
            'action': 'turn_on',
            'device_id': self.device_id,
            'device_type': self.device_type
        }
        await self.send_data_ws(data=json.dumps(data))

    async def turn_off(self):
        data = {
            'action': 'turn_off',
            'device_id': self.device_id,
            'device_type': self.device_type
        }
        await self.send_data_ws(data=json.dumps(data))

    async def set_state(self, state):
        data = {
            'action': 'set_state',
            'state': state,
            'device_id': self.device_id,
            'device_type': self.device_type
        }
        await self.send_data_ws(data=json.dumps(data))

    async def set_timer(self, start_time, stop_time):
        data = {
            'action': 'set_timer',
            'start_time': start_time,
            'stop_time': stop_time,
            'device_id': self.device_id,
            'device_type': self.device_type
        }
        await self.send_data_ws(data=json.dumps(data))

    async def clear_timer(self):
        data = {
            'action': 'clear_timer',
            'device_id': self.device_id,
            'device_type': self.device_type
        }
        await self.send_data_ws(data=json.dumps(data))

    async def get_state(self):
        data = {
            'action': 'get_state',
            'device_id': self.device_id,
            'device_type': self.device_type,
        }
        await self.send_data_ws(data=json.dumps(data))
