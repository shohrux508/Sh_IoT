import json
import time

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import create_app
from fastapi.testclient import TestClient
from app.devices.schemas import DeviceRequestControl, DeviceCreate
from tests.health import client

app = create_app()
transport = ASGITransport(app=app)
base_url = 'http://test'


@pytest.mark.asyncio
async def test_devices_all():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        response = await ac.get('/devices/all')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_devices_active():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        response = await ac.get('/devices/active')
    assert response.status_code == 200


def test_device_websocket():
    with client.websocket_connect('/devices/register/1') as ws:
        while ws.receive_text():
            assert ws.receive_text() == 'ping'


