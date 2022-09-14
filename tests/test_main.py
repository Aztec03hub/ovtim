from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Omron Microscan VT-Interface Module" in response.content
    response = client.get("/static/css/style3.css")
    assert response.status_code == 200

def test_managescanners():
    response = client.get("/managescanners", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Manage Scanners - Omron Microscan VT-Interface Module" in response.content