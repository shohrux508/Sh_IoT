from fastapi import APIRouter

from database.engine import async_session
from database.requests import Users, Devices
from schemas import DeviceOut, DeviceCreate, UserOut

router = APIRouter(prefix='/devices')
devices = {1: 'raspberrypi5', 2: 'raspberrypi4'}


@router.get('/', tags=['Устройства'], summary='Получить одно устройство')
async def get_devices():
    return devices


@router.get('/{device_id}', tags=['Устройства'], summary='Получить все устройства')
async def get_device(device_id: int):
    return {'message': devices.get(device_id)}


@router.post('/')
async def add_device(device: DeviceCreate):
    print(f"Новое устройство: {device.name}")
    try:
        async with async_session() as session:
            await Devices(session).create(device_name=device.name, device_id=device.id)
        return {"message": "Устройство успешно добавлено!"}
    except:
        return {"message": "Не удалось добавить устройство!"}