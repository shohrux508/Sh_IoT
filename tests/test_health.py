import sys, os
# Добавляем в sys.path корень проекта (на уровень выше папки tests)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': "ok"}
