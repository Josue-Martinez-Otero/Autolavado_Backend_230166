import models.modelVehiculos
import schemas.schema_vehiculos
from sqlalchemy.orm import Session
import models, schemas

def get_vehiculo(db: Session, skip: int = 0, limit: int = 10):
    '''Función para obtener un vehiculo por su ID'''
    return db.query(models.modelVehiculos.Vehiculo).offset(skip).limit(limit).all()

def get_vehiculo_by_nombre(db: Session, placas: str):
    return db.query(models.modelVehiculos.Vehiculo).filter(models.modelVehiculos.Vehiculo.placas == placas).first()

def create_vehiculo(db: Session, vehiculo: schemas.schema_vehiculos.VehiculoCreate):
    '''Función para crear un nuevo vehiculo'''
    db_vehiculo = models.modelVehiculos.Vehiculo(
        usuario_Id=vehiculo.usuario_Id,
        placa=vehiculo.placa,
        marca=vehiculo.marca,
        modelo=vehiculo.modelo,
        color=vehiculo.color,
        tipo=vehiculo.tipo,
        anio=vehiculo.anio,
        numero_serie=vehiculo.numero_serie,
        estatus=vehiculo.estatus,
        fecha_registro=vehiculo.fecha_registro,
        fecha_modificacion=vehiculo.fecha_modificacion
    )
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

def update_vehiculo(db: Session, vehiculo_id: int, vehiculo: schemas.schema_vehiculos.VehiculoUpdate):
    '''Función para actualizar un vehiculo existente'''
    db_vehiculo = db.query(models.modelVehiculos.Vehiculo).filter(models.modelVehiculos.Vehiculo.Id == vehiculo_id).first()
    if db_vehiculo is None:
        return None
    for var, value in vars(vehiculo).items():
        setattr(db_vehiculo, var, value) if value else None
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo

def delete_vehiculo(db: Session, vehiculo_id: int):
    '''Función para eliminar un vehiculo por su ID'''
    db_vehiculo = db.query(models.modelVehiculos.Vehiculo).filter(models.modelVehiculos.Vehiculo.Id == vehiculo_id).first()
    if db_vehiculo is None:
        return None
    db.delete(db_vehiculo)
    db.commit()
    return db_vehiculo
