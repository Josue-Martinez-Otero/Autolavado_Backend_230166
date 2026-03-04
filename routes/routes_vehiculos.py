from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

import config.db
import crud.crud_vehiculos
import schemas.schema_vehiculos
import models.modelVehiculos

vehiculo = APIRouter()

# Crear tablas
models.modelVehiculos.Base.metadata.create_all(bind=config.db.engine)


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
# OBTENER TODOS LOS VEHICULOS
# ==============================
@vehiculo.get(
    "/vehiculo/",
    response_model=List[schemas.schema_vehiculos.Vehiculo],
    tags=["Vehiculos"]
)
async def read_vehiculo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.crud_vehiculos.get_vehiculo(
        db=db,
        skip=skip,
        limit=limit
    )


# ==============================
# CREAR VEHICULO
# ==============================
@vehiculo.post(
    "/vehiculo/",
    response_model=schemas.schema_vehiculos.Vehiculo,
    status_code=status.HTTP_201_CREATED,
    tags=["Vehiculos"]
)
async def create_vehiculo(
    vehiculo_data: schemas.schema_vehiculos.VehiculoCreate,
    db: Session = Depends(get_db)
):
    # Validar placas duplicadas
    existing_vehiculo = crud.crud_vehiculos.get_vehiculo_by_placas(
        db,
        placas=vehiculo_data.placas
    )

    if existing_vehiculo:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un vehículo con esas placas"
        )

    return crud.crud_vehiculos.create_vehiculo(
        db=db,
        vehiculo=vehiculo_data
    )


# ==============================
# ACTUALIZAR VEHICULO
# ==============================
@vehiculo.put(
    "/vehiculo/{vehiculo_id}",
    response_model=schemas.schema_vehiculos.Vehiculo,
    tags=["Vehiculos"]
)
async def update_vehiculo(
    vehiculo_id: int,
    vehiculo_data: schemas.schema_vehiculos.VehiculoUpdate,
    db: Session = Depends(get_db)
):
    db_vehiculo = crud.crud_vehiculos.update_vehiculo(
        db=db,
        vehiculo_id=vehiculo_id,
        vehiculo=vehiculo_data
    )

    if db_vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return db_vehiculo


# ==============================
# ELIMINAR VEHICULO
# ==============================
@vehiculo.delete(
    "/vehiculo/{vehiculo_id}",
    response_model=schemas.schema_vehiculos.Vehiculo,
    tags=["Vehiculos"]
)
async def delete_vehiculo(
    vehiculo_id: int,
    db: Session = Depends(get_db)
):
    db_vehiculo = crud.crud_vehiculos.delete_vehiculo(
        db=db,
        vehiculo_id=vehiculo_id
    )

    if db_vehiculo is None:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return db_vehiculo