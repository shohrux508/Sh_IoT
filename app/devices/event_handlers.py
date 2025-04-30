import json


async def handle_device_event(device_id: int, message: str):
    print(message)
    if message.startswith('print'):
        print(message.replace('print', ''))

