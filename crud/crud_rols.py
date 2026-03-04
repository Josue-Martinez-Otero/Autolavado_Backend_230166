import models.modelRols
import schemas.schema_rols
from sqlalchemy.orm import Session
import models, schemas

def get_rol(db: Session, skip: int = 0, limit: int = 100):
    '''Función para obtener un rol por su ID'''
    return db.query(models.modelRols.Rols).offset(skip).limit(limit).all()

def get_rol_by_nombre(db: Session, nombre_rol: str):
    return db.query(models.modelRols.Rols).filter(models.modelRols.Rols.nombre_rol == nombre_rol).first()

def create_rol(db: Session, rol: schemas.schema_rols.RolCreate):
    '''Función para crear un nuevo rol'''
    db_rol = models.modelRols.Rols(
        nombre_rol=rol.nombre_rol,
        estado=rol.estado,
        fecha_registro=rol.fecha_registro,
        fecha_actualizacion=rol.fecha_actualizacion
    )
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def update_rol(db: Session, rol_id: int, rol: schemas.schema_rols.RolUpdate):
    '''Función para actualizar un rol existente'''
    db_rol = db.query(models.modelRols.Rols).filter(models.modelRols.Rols.Id == rol_id).first()
    if db_rol is None:
         for var, value in vars(rol).items():
            setattr(db_rol, var, value) if value else None
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

def delete_rol(db: Session, rol_id: int):
    '''Función para eliminar un rol por su ID'''
    db_rol = db.query(models.modelRols.Rols).filter(models.modelRols.Rols.Id == rol_id).first()
    if db_rol is None:
        return None
    db.delete(db_rol)
    db.commit()
    return db_rol
