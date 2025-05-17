
import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import create_app

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

