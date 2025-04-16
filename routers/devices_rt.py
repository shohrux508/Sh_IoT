import asyncio
from typing import List
from fastapi import APIRouter, HTTPException, Query

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
            await Devices(session).create(device)
        return {"message": "Устройство успешно добавлено!"}
    except:
        return {"message": "Не удалось добавить устройство!"}


@router.delete('/{device_id}/delete')
async def delete_device(device_id: int):
    try:
        async with async_session() as session:
            await Devices(session).delete(model_id=device_id)
        return {"message": f"Устройство: {device_id} удалено!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail='Не удалось удалить устройство!')


@router.get('/print-devices')
async def print_devices(ids: List[int] = Query(...)):
    try:
        for i_d in ids:
            print(i_d)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Возникла ошибка при попытки вывести устройств')
