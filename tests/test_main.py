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

def test_weblink():
    response = client.get("/weblink", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Weblink - Omron Microscan VT-Interface Module" in response.content

def test_help():
    response = client.get("/help", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Help - Omron Microscan VT-Interface Module" in response.content

def test_settings():
    response = client.get("/settings", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"Settings - Omron Microscan VT-Interface Module" in response.content