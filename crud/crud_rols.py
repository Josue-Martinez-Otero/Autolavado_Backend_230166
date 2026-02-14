import models.modelRols
import schemas.schema_rols
from sqlalchemy.orm import Session

def get_rol(db: Session, skip: int = 0, limit: int = 10):
    '''Función para obtener un rol por su ID'''
    return db.query(models.modelRols.Rols).offset(skip).limit(limit).all()