import uuid

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_crear_usuario_exitoso():
    payload = {
        "rol_Id": 1,
         "nombre": f"Test_{uuid.uuid4()}",
        "papellido": "Test",
        "sapellido": "Test",
        "direccion": "Tes",
        "correo_electronico": "test@test.com",
        "numero_telefono": "0000000000",
        "contrasena": "test"
    }

    response = client.post("/user/", json=payload)

    # Debe responder 201 o 200
    print(response.status_code)
    print(response.json())
    assert response.status_code in [200, 201]

    data = response.json()

    assert data["correo_electronico"] == payload["correo_electronico"]
    assert data["nombre"] == payload["nombre"]

    # Seguridad: la contraseña NO debe regresar
    assert "contrasena" not in data


def test_crear_usuario_datos_invalidos():
    payload_invalido = {
        "rol_Id": "no-es-un-numero",  # Tipo incorrecto
        "nombre": "Error"
    }

    response = client.post("/user/", json=payload_invalido)

    # FastAPI debe validar automáticamente
    assert response.status_code == 422