import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from config.db import Base
from models.modelUser import User


# ==========================
# BASE DE DATOS EN MEMORIA
# ==========================
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# ==========================
# FIXTURE DE BASE DE DATOS
# ==========================
@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# ==========================
# TEST DE INSERCIÓN
# ==========================
@pytest.mark.database
def test_crear_usuario_db(db):

    nuevo_usuario = User(
        nombre="Juan",
        papellido="Perez",
        sapellido="Lopez",
        direccion="Calle 123",
        correo_electronico="juan@test.com",
        numero_telefono="1234567890",
        contrasena="123456",
        estatus=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    usuario_guardado = db.query(User).filter(
        User.correo_electronico == "juan@test.com"
    ).first()

    assert usuario_guardado is not None
    assert usuario_guardado.nombre == "Juan"
    assert usuario_guardado.papellido == "Perez"