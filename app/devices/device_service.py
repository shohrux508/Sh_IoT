from fastapi import WebSocket, HTTPException, status

from app.devices.device_adapters import DeviceCommands
from app.devices.ws_connection import device_session_manager


async def get_websocket_or_404(device_id: int) -> WebSocket:
    session = await device_session_manager.get(device_id)
    websocket = session.websocket
    if not websocket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Устройство {device_id} не подключено.'
        )
    return websocket


async def control_device(device_id: int, device_type: str, state: bool = None, start_time: str = None,
                         stop_time: str = None):
    try:
        websocket = await get_websocket_or_404(device_id)
    except Exception as e:
        print(f'Ошибка Websocket, {e}')
        return 'Не удалось найти соединений', state
    device = DeviceCommands(device_type=device_type, device_id=device_id, websocket=websocket)
    if start_time and stop_time:
        await device.set_timer(start_time=start_time, stop_time=stop_time)
        return 'Set timer', state
    elif state is not None:
        await device.set_state(state=state)
        return 'Set state', state
    else:
        await device.clear_timer()
        return 'Clear timer', 0


async def get_device_status(device_id: int, device_type: str) -> bool:
    websocket = await get_websocket_or_404(device_id)
    device = DeviceCommands(device_type=device_type, device_id=device_id, websocket=websocket)
    return await device.get_state()


async def get_active_devices() -> list[int]:
    return await device_session_manager.all_ids()
