
from app.config import logger
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

router = APIRouter(prefix='/devices')

esp_connections: dict[int, WebSocket] = {}  # глобальная переменная, хранящая подключение


@router.websocket('/register/{device_id}', name='Регистрация устройства')
async def websocket_endpoint(websocket: WebSocket, device_id: int):
    await websocket.accept()
    esp_connections[device_id] = websocket
    logger.info(f'Устройство {device_id} подключено.')

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f'Получено от устройства {device_id}]: {data}')
    except WebSocketDisconnect:
        esp_connections.pop(device_id, None)
        logger.warning(f'Устройство {device_id} отключено.')
    except Exception as e:
        esp_connections.pop(device_id, None)
        logger.error(f'Неожиданная ошибка с устройством {device_id}: {e}')
    finally:
        if esp_connections.get(device_id) is websocket:
            esp_connections.pop(device_id, None)
            logger.info(f'Подключение с {device_id} удалено из хранилища.')

        try:
            await websocket.close()
        except Exception as e:
            logger.debug(f'Ошибка при закрытии соединения {device_id}: {e}')

@router.get(
    '/control/{device_id}',
    # response_model=CommandResponse,
    # responses={
    #     404: {'model': ErrorResponse, 'description': 'Устройство не подключено'}
    # },
    summary='Управление устройством'
)
async def control_device(device_id: int, cmd: str = Query(..., description='Команда для ESP8266')):
    connection: WebSocket = esp_connections.get(device_id)

    if connection is not None:
        await connection.send_text(cmd)
        logger.info(f'Команда \'{cmd}\' отправлена на устройство {device_id}')
        return {'status': 'sent', 'command': cmd}
    else:
        logger.warning(f'Попытка отправить команду на неактивное устройство {device_id}')
        return {'error': f'Устройство-{device_id} не слушает'}

@router.get('/active', summary='Активные устройства')
async def active_devices():
    return {'active_devices': esp_connections}
