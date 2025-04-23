import asyncio

from datetime import UTC, datetime, timedelta
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse

from app.config import logger
from app.devices.schemas import CommandResponse, ErrorResponse, ActiveDevicesResponse, DeviceCreate
from app.devices.manager import DeviceConnectionManager

router = APIRouter(prefix='/devices')

HEARTBEAT_INTERVAL = 10  # каждое N секунд пингуем
HEARTBEAT_TIMEOUT = 30   # если нет ответа за N секунд — отключаем

manager = DeviceConnectionManager()


@router.websocket('/register/{device_id}', name='Регистрация устройства')
async def websocket_endpoint(websocket: WebSocket, device_id: int):
    await websocket.accept()
    raw_data = await websocket.receive_text()
    creds = DeviceCreate.model_validate_json(raw_data)
    if not creds.token == '2645':
        logger.info(f'Устройство {device_id} не смогло подключиться, из-за неправильного токена')
        await websocket.send_text("❌ Неверный токен")
        await websocket.close()

        return

    await manager.register(device_id, websocket)
    logger.info(f'Устройство {device_id} подключено.')

    last_pong_time = datetime.now(UTC)

    async def ping_loop():
        nonlocal last_pong_time
        try:
            while True:
                await asyncio.sleep(HEARTBEAT_INTERVAL)
                try:
                    await websocket.send_text('ping')
                    logger.debug(f'Ping отправлен устройству {device_id}')
                except Exception as e:
                    logger.warning(f'Ошибка при отправке ping устройству {device_id}: {e}')
                    break

                if datetime.now(UTC) - last_pong_time > timedelta(seconds=HEARTBEAT_TIMEOUT):
                    logger.warning(f'Таймаут heartbeat для устройства {device_id}')
                    break
        finally:
            # Закрытие соединения инициируется снаружи
            pass

    async def listen_loop():
        nonlocal last_pong_time
        while True:
            try:
                message = await websocket.receive_text()
                if message.lower() == 'pong':
                    last_pong_time = datetime.now(UTC)
                    logger.debug(f'Pong получен от {device_id}')
                else:
                    logger.info(f'Получено от {device_id}: {message}')
            except WebSocketDisconnect:
                logger.warning(f'WebSocketDisconnect от устройства {device_id}')
                break
            except Exception as e:
                logger.error(f'Ошибка получения данных от устройства {device_id}: {e}')
                break

    # Запускаем оба процесса параллельно
    try:
        await asyncio.gather(ping_loop(), listen_loop())
    finally:
        print('here')
        if await manager.get(device_id) is websocket:
            await manager.unregister(device_id)
            logger.info(f'Устройство {device_id} удалено из хранилища')

        try:
            await websocket.close()
        except Exception as e:
            logger.debug(f'Ошибка при закрытии WebSocket {device_id}: {e}')

@router.get(
    path='/control/{device_id}',
    response_model=CommandResponse,
    responses={
        404: {'model': ErrorResponse, 'description': 'Устройство не подключено'}
    },
    summary='Управление устройством'
)
async def control_device(device_id: int, cmd: str = Query(..., description='Команда для ESP8266')):
    connection: WebSocket = await manager.get(device_id)

    if connection is not None:
        await connection.send_text(cmd)
        logger.info(f'Команда \'{cmd}\' отправлена на устройство {device_id}')
        return CommandResponse(success=True, device_id=device_id, command=cmd)
    else:
        logger.warning(f'Попытка отправить команду на неактивное устройство {device_id}')
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(error=f'Устройство {device_id} не подключено').model_dump()
        )

@router.get('/active', response_model=ActiveDevicesResponse, summary='Активные устройства')
async def active_devices():
    return ActiveDevicesResponse(active_devices=await manager.all_ids())
