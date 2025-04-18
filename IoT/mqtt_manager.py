# import asyncio
# from aiomqtt import Client
# import sys
# from config import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, ssl_context, logger
# 
#
# class ManageBroker:
#     @staticmethod
#     async def publish(topic: str, command: str):
#
#         try:
#             async with Client(
#                     hostname=MQTT_BROKER,
#                     port=MQTT_PORT,
#                     username=MQTT_USERNAME,
#                     password=MQTT_PASSWORD,
#                     tls_context=ssl_context,
#             ) as client:
#                 await client.publish(topic, str(command))
#                 logger.info(f'Отправлено: {command}')
#         except Exception as e:
#             logger.error(f"Ошибка при публикации команды '{command}' на тему '{topic}': {e}")
#
#     @staticmethod
#     async def subscribe(topic: str):
#         attempt = 0
#
#         while attempt < 5:
#             try:
#                 logger.info(f"[MQTT] Подключение к брокеру... Попытка {attempt + 1}")
#                 async with Client(
#                         hostname=MQTT_BROKER,
#                         port=MQTT_PORT,
#                         username=MQTT_USERNAME,
#                         password=MQTT_PASSWORD,
#                         tls_context=ssl_context,
#                 ) as client:
#                     await client.subscribe(topic)
#                     logger.info(f"[MQTT] Подписка на тему: {topic}")
#                     attempt = 0
#
#                     async for msg in client.messages:
#                         yield msg.payload.decode()
#
#             except Exception as e:
#                 attempt += 1
#                 logger.error(f"[MQTT] Ошибка при подписке: {e}")
#                 logger.info(f"[MQTT] Повторная попытка через 6 секунд...")
#                 await asyncio.sleep(6)
#
#         logger.critical("[MQTT] Превышено число попыток подключения. Завершаю.")
#         sys.exit(1)
