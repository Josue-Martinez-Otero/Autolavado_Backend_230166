from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import config.db, models.modelRols, schemas.schema_rols, crud.crud_rols 

rol_router = APIRouter()

models.modelRols.Base.metadata.create_all(bind=config.db.engine)    

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@rol_router.get("/rol/", response_model=list[schemas.schema_rols.Rols], tags=["Rols"])        
async def read_rols(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''Función para obtener un rol por su ID'''
    db_rol = crud.crud_rols.get_rol(db, skip=skip, limit=limit)
    return db_rol