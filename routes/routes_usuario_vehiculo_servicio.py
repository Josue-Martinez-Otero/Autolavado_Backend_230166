from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

import config.db
import crud.crud_usuario_vehiculo_servicio
import schemas.schema_usuario_vehiculo_servicio
import models.model_usuario_vehiculo_servicio

usuario_vehiculo_servicio = APIRouter()

# Crear tablas
models.model_usuario_vehiculo_servicio.Base.metadata.create_all(bind=config.db.engine)


# ==============================
# DEPENDENCIA DB
# ==============================
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# OBTENER TODOS
# ==============================
@usuario_vehiculo_servicio.get(
    "/usuario_vehiculo_servicio/",
    response_model=List[schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio],
    tags=["Usuario Vehiculo Servicios"]
)
async def read_usuario_vehiculo_servicios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.crud_usuario_vehiculo_servicio.get_usuario_vehiculo_servicio(
        db=db,
        skip=skip,
        limit=limit
    )


# ==============================
# CREAR
# ==============================
@usuario_vehiculo_servicio.post(
    "/usuario_vehiculo_servicio/",
    response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuario Vehiculo Servicios"]
)
async def create_usuario_vehiculo_servicio(
    data: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioCreate,
    db: Session = Depends(get_db)
):
    # Validar si ya existe un servicio en misma fecha y hora
    existing = crud.crud_usuario_vehiculo_servicio.get_usuario_vehiculo_servicio_by_fecha_hora(
        db,
        fecha=data.fecha,
        hora=data.hora
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un servicio registrado en esa fecha y hora"
        )

    return crud.crud_usuario_vehiculo_servicio.create_usuario_vehiculo_servicio(
        db=db,
        usuario_vehiculo_servicio=data
    )


# ==============================
# ACTUALIZAR
# ==============================
@usuario_vehiculo_servicio.put(
    "/usuario_vehiculo_servicio/{usuario_vehiculo_servicio_id}",
    response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio,
    tags=["Usuario Vehiculo Servicios"]
)
async def update_usuario_vehiculo_servicio(
    usuario_vehiculo_servicio_id: int,
    data: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioUpdate,
    db: Session = Depends(get_db)
):
    db_obj = crud.crud_usuario_vehiculo_servicio.update_usuario_vehiculo_servicio(
        db=db,
        usuario_vehiculo_servicio_id=usuario_vehiculo_servicio_id,
        usuario_vehiculo_servicio=data
    )

    if db_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario Vehiculo Servicio no encontrado"
        )

    return db_obj


# ==============================
# ELIMINAR
# ==============================
@usuario_vehiculo_servicio.delete(
    "/usuario_vehiculo_servicio/{usuario_vehiculo_servicio_id}",
    response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio,
    tags=["Usuario Vehiculo Servicios"]
)
async def delete_usuario_vehiculo_servicio(
    usuario_vehiculo_servicio_id: int,
    db: Session = Depends(get_db)
):
    db_obj = crud.crud_usuario_vehiculo_servicio.delete_usuario_vehiculo_servicio(
        db=db,
        usuario_vehiculo_servicio_id=usuario_vehiculo_servicio_id
    )

    if db_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario Vehiculo Servicio no encontrado"
        )

    return db_obj