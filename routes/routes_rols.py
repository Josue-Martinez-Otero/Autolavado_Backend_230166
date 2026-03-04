from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import config.db
import models.modelRols
import schemas.schema_rols
import crud.crud_rols
from config.security import get_current_user

rol_router = APIRouter()

# Crear tablas si no existen
models.modelRols.Base.metadata.create_all(bind=config.db.engine)


# Dependencia DB
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# OBTENER TODOS LOS ROLES
# ==============================
@rol_router.get(
    "/rol/",
    response_model=List[schemas.schema_rols.Rol],
    tags=["Roles"]
)
async def read_rols(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud.crud_rols.get_rol(db=db, skip=skip, limit=limit)


# ==============================
# CREAR ROL
# ==============================
@rol_router.post(
    "/rol/",
    response_model=schemas.schema_rols.Rol,
    tags=["Roles"]
)
async def create_rol(
    rol: schemas.schema_rols.RolCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Validar si ya existe
    db_rol_existente = crud.crud_rols.get_rol_by_nombre(
        db, nombre_rol=rol.nombre_rol
    )

    if db_rol_existente:
        raise HTTPException(
            status_code=400,
            detail="El rol ya existe, intenta nuevamente"
        )

    return crud.crud_rols.create_rol(db=db, rol=rol)


# ==============================
# ACTUALIZAR ROL
# ==============================
@rol_router.put(
    "/rol/{rol_id}",
    response_model=schemas.schema_rols.Rol,
    tags=["Roles"]
)
async def update_rol(
    rol_id: int,
    rol: schemas.schema_rols.RolUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_rol = crud.crud_rols.update_rol(
        db=db,
        rol_id=rol_id,
        rol=rol
    )

    if db_rol is None:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return db_rol


# ==============================
# ELIMINAR ROL
# ==============================
@rol_router.delete(
    "/rol/{rol_id}",
    response_model=schemas.schema_rols.Rol,
    tags=["Roles"]
)
async def delete_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_rol = crud.crud_rols.delete_rol(
        db=db,
        rol_id=rol_id
    )

    if db_rol is None:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return db_rol