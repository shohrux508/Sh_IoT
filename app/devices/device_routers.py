from typing import List

from fastapi import APIRouter, Query, WebSocket, Depends, HTTPException

from app.devices.dependencies import get_device_service
from app.devices.device_service import DeviceService
from app.devices.schemas import *
from app.devices.ws_handlers import websocket_handler
from app.logger_module.logger_utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/devices')


@router.websocket('/ws/{device_id}/connect')
async def websocket_connection(websocket: WebSocket, device_id: int,
                               service: DeviceService = Depends(get_device_service)):
    await websocket.accept()
    logger.info('⏳Установлена временная связь.\n'
                ' Ожидание дополнительных данных...')
    await websocket_handler.handle_connection(websocket=websocket, device_id=device_id, service=service)
    # {"auth_token": "abc123"}


@router.post(
    path='/control/{device_id}',
    response_model=DeviceControl_response,
    summary='Управление устройством'
)
async def control_socket(device_id: int, request: DeviceControl_request,
                         service: DeviceService = Depends(get_device_service)):
    action, result_state = await service.control_device(
        device_id=device_id,
        **request.model_dump()
    )
    return DeviceControl_response(
        action=action,
        state=result_state,
        device_id=device_id
    )


@router.get('/{device_id}/status', response_model=DeviceStatus_response)
async def get_device_status_r(device_id: int,
                              device_type: str = Query(..., description='Получение статуса устройства'),
                              service: DeviceService = Depends(get_device_service)):
    try:
        state = await service.get_device_status(device_id=device_id, device_type=device_type)
    except:
        raise HTTPException(status_code=404, detail='Device not found')
    return DeviceStatus_response(
        device_id=device_id,
        state=state
    )


@router.get('/active', response_model=ActiveDevicesResponse, summary='Список активных устройств')
async def active_devices(service: DeviceService = Depends(get_device_service)):
    device_ids = await service.get_active_devices()
    return ActiveDevicesResponse(active_devices=device_ids)


@router.get('/all', response_model=List[DeviceInfo])
async def get_all_devices_in_short(service: DeviceService = Depends(get_device_service),
                                   name: str = Query(None), sort: str = Query(None)):
    devices = await service.list_filtered_sorted(name=name, sort=sort)
    return devices


@router.post('/create', response_model=DeviceInfo, response_model_exclude_none=True)
async def create_device(data: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    try:
        device = await service.create(data)
        logger.info(f'Новое устройство: {device.id}')
        return device
    except Exception as e:
        logger.error(f'Ошибка при создании устройства: {e}')
