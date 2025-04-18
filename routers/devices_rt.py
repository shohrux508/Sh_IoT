from fastapi import APIRouter, Query, WebSocket

router = APIRouter(prefix='/devices')
devices = {1: 'raspberrypi5', 2: 'raspberrypi4'}

esp_connection: dict[int:WebSocket] | dict = {}  # глобальная переменная, хранящая подключение


@router.websocket("/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: int):
    global esp_connection
    await websocket.accept()
    esp_connection[device_id] = websocket
    print("ESP32 подключился")
    try:
        while True:
            data = await websocket.receive_text()
            print("От ESP32:", data)
    except:
        print("Соединение потеряно")


@router.get("/control/{device_id}")
async def control_device(device_id: int, cmd: str = Query(..., description='Команда для ESP8266')):
    global esp_connection
    connection: WebSocket = esp_connection.get(device_id)
    if connection is not None:
        await connection.send_text(cmd)
        print(connection, cmd)
        return {"status": "sent", "command": cmd}
    else:
        return {"error": f"Устройство-{device_id} не слушает"}
