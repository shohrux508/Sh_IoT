from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import async_session
from database.requests import Users, Devices
from schemas import DeviceOut, DeviceCreate, UserOut

router = APIRouter(prefix='/devices')
devices = {1: 'raspberrypi5', 2: 'raspberrypi4'}


@router.get('/', tags=['Устройства'], summary='Получить одно устройство')
async def get_devices():
    return devices


@router.get('/{id}', tags=['Устройства'], summary='Получить все устройства')
async def get_device(id: int):
    return {'message': devices.get(id)}

esp32_connection: dict[int:WebSocket] | dict = {}  # глобальная переменная, хранящая подключение


@router.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: int):
    global esp32_connection
    await websocket.accept()
    esp32_connection[device_id] = websocket
    print("ESP32 подключился")

    try:
        while True:
            data = await websocket.receive_text()
            print("От ESP32:", data)
    except:
        print("Соединение потеряно")
        esp32_connection = None


@router.get("/control/{device_id}")
async def control_device(cmd: str, device_id: int):
    global esp32_connection
    connection: WebSocket = esp32_connection.get(device_id)
    if connection is None:
        await connection.send_text(cmd)
        print(connection, cmd)
        return {"status": "sent", "command": cmd}
    else:
        return {"error": "ESP32 не подключен"}
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
async def delete_device(device_id: int, session: AsyncSession = Depends(async_session)):
    try:
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
