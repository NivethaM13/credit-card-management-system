from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ================= HOME TEST =================

def test_home():

    response = client.get("/")

    assert response.status_code == 200


# ================= REGISTER TEST =================

def test_register():

    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "test123@gmail.com",
            "password": "12345"
        }
    )

    assert response.status_code == 200


# ================= LOGIN TEST =================

def test_login():

    response = client.post(
        "/login",
        json={
            "email": "test123@gmail.com",
            "password": "12345"
        }
    )

    assert response.status_code == 200