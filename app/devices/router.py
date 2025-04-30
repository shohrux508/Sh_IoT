from fastapi import APIRouter, Query, WebSocket

from app.devices.device_service import control_device, get_device_status, get_active_devices
from app.devices.event_handlers import handle_device_event
from app.devices.schemas import (
    ActiveDevicesResponse,
    DeviceRequestControl,
    DeviceControlResponse,
    DeviceStatusResponse)
from app.devices.ws_connection import DeviceSession, device_session_manager

router = APIRouter(prefix='/devices')


@router.websocket('/register/{device_id}', name='Регистрация устройства')
async def websocket_endpoint(websocket: WebSocket, device_id: int):
    await websocket.accept()
    try:
        await device_session_manager.register(device_id=device_id, websocket=websocket)
        session = DeviceSession(device_id=device_id, websocket=websocket, event_handler=handle_device_event)

        await session.start()
    except Exception:
        await websocket.close()
        raise


@router.post(
    path='/control/{device_id}',
    response_model=DeviceControlResponse,
    summary='Управление устройством'
)
async def control_socket(device_id: int, request: DeviceRequestControl):
    state = request.state
    device_type = request.device_type
    start_time = request.start_time
    stop_time = request.stop_time
    action, result_state = await control_device(
        device_id=device_id,
        device_type=device_type,
        start_time=start_time,
        stop_time=stop_time,
        state=state
    )
    return DeviceControlResponse(
        action=action,
        state=result_state,
        device_id=device_id
    )


@router.get('/status/{device_id}', response_model=DeviceStatusResponse)
async def get_device_status_r(device_id: int,
                              device_type: str = Query(..., description='Получение статуса устройства')):
    state = await get_device_status(device_id=device_id, device_type=device_type)
    return DeviceStatusResponse(
        device_id=device_id,
        state=state
    )


@router.get('/active', response_model=ActiveDevicesResponse, summary='Список активных устройств')
async def active_devices():
    device_ids = await get_active_devices()
    print(device_ids)
    return ActiveDevicesResponse(active_devices=device_ids)
