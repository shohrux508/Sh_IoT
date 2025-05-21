from app.ws.ws_connection import event_bus, ws_manager

from app.logger_module.logger_utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()


@event_bus.on("device_connected")
async def handle_connect(device_id):
    await ws_manager.send_personal(device_id, 'Вы подключились')


@event_bus.on("device_disconnected")
async def handle_disconnect(device_id):
    pass


@event_bus.on('websocket_wrong_auth_token')
async def handle_auth_token_wrong(device_id):
    logger.info(f"Неверный auth_token, {device_id}")
    await ws_manager.send_personal(device_id, message='Неверный auth_token')
    await ws_manager.disconnect(device_id=device_id)


@event_bus.on("message_from_device")
async def handle_message(device_id, message):
    await ws_manager.send_personal(device_id, f"Вы сказали: {message}")
    await ws_manager.set_response(device_id=int(device_id), message=message)


@event_bus.on('got_reply')
async def handle_reply_message(device_id, data, response):
    logger.info(f'[{device_id}], Ответ от устройства. Запрос: {data}\nОтвет: {response}')


@event_bus.on('message_to_device')
async def handle_message_to_device(device_id, message):
    pass

@event_bus.on('new_device')
async def handle_new_device(device_id):
    logger.info(f'Новое устройство: {device_id}')


@event_bus.on('device_timeout')
async def handle_timeout(device_id, last_pong_time):
    pass


@event_bus.on('device_send_error')
async def handle_send_error(device_id, error):
    pass


@event_bus.on('device_error')
async def handle_error(device_id, error):
    pass


@event_bus.on('device_session_end')
async def handle_session_end(device_id):
    pass
