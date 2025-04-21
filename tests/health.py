import sys
import os
from fastapi.testclient import TestClient
from app.main import app

# Добавляем в sys.path корень проекта (на уровень выше папки tests)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': "ok"}
