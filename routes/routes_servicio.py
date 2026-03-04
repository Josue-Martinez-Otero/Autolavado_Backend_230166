from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import config.db
import crud.crud_servicio
import schemas.schema_servicio
import models.modelServicio
from config.security import get_current_user

servicio = APIRouter()

# Crear tablas si no existen
models.modelServicio.Base.metadata.create_all(bind=config.db.engine)


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
# OBTENER SERVICIOS
# ==============================
@servicio.get(
    "/servicio/",
    response_model=List[schemas.schema_servicio.Servicio],
    tags=["Servicios"]
)
async def read_servicio(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud.crud_servicio.get_servicio(db=db, skip=skip, limit=limit)


# ==============================
# CREAR SERVICIO
# ==============================
@servicio.post(
    "/servicio/",
    response_model=schemas.schema_servicio.Servicio,
    tags=["Servicios"]
)
async def create_servicio(
    servicio_data: schemas.schema_servicio.ServicioCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Validar duplicado
    db_servicio_existente = crud.crud_servicio.get_servicio_by_nombre(
        db,
        nombre_servicio=servicio_data.nombre_servicio
    )

    if db_servicio_existente:
        raise HTTPException(
            status_code=400,
            detail="El servicio ya existe"
        )

    return crud.crud_servicio.create_servicio(
        db=db,
        servicio=servicio_data
    )


# ==============================
# ACTUALIZAR SERVICIO
# ==============================
@servicio.put(
    "/servicio/{servicio_id}",
    response_model=schemas.schema_servicio.Servicio,
    tags=["Servicios"]
)
async def update_servicio(
    servicio_id: int,
    servicio_data: schemas.schema_servicio.ServicioUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_servicio = crud.crud_servicio.update_servicio(
        db=db,
        servicio_id=servicio_id,
        servicio=servicio_data
    )

    if db_servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    return db_servicio


# ==============================
# ELIMINAR SERVICIO
# ==============================
@servicio.delete(
    "/servicio/{servicio_id}",
    response_model=schemas.schema_servicio.Servicio,
    tags=["Servicios"]
)
async def delete_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_servicio = crud.crud_servicio.delete_servicio(
        db=db,
        servicio_id=servicio_id
    )

    if db_servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    return db_servicio
