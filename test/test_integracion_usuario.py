import uuid
from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

@pytest.mark.integracion
def test_flujo_completo_usuario():

    # 1️⃣ Crear usuario
    unique_name = f"User_{uuid.uuid4()}"
    payload = {
        "rol_Id": 1,
        "nombre": unique_name,
        "papellido": "Test",
        "sapellido": "Test",
        "direccion": "Test",
        "correo_electronico": f"{unique_name}@test.com",
        "numero_telefono": "1234567890",
        "contrasena": "1234"
    }

    create_response = client.post("/user/", json=payload)
    assert create_response.status_code in [200, 201]

    # 2️⃣ Login
    login_data = {
        "username": unique_name,   # OAuth2 usa username
        "password": "1234"
    }

    login_response = client.post("/login", data=login_data)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3️⃣ Acceder endpoint protegido
    headers = {
        "Authorization": f"Bearer {token}"
    }

    protected_response = client.get("/user/", headers=headers)

    assert protected_response.status_code == 200
    assert isinstance(protected_response.json(), list)