import pytest
from fastapi.testclient import TestClient
from main import app  # ajusta si tu archivo principal tiene otro nombre

client = TestClient(app)


@pytest.mark.auth
def test_login_correcto():

    response = client.post(
        "/login",
        data={
            "username": "admin@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

    