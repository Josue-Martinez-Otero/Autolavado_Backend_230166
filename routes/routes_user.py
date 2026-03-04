from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

import config.db
import crud.crud_user
import schemas.schema_user
import models.modelUser
from config.security import create_access_token, get_current_user

user = APIRouter()

# Crear tablas si no existen
models.modelUser.Base.metadata.create_all(bind=config.db.engine)


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
# OBTENER USUARIOS (PROTEGIDO)
# ==============================
@user.get(
    "/user/",
    response_model=List[schemas.schema_user.UserResponse],
    tags=["Users"]
)
async def read_user(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return crud.crud_user.get_user(db=db, skip=skip, limit=limit)


# ==============================
# CREAR USUARIO
# ==============================
@user.post(
    "/user/",
    response_model=schemas.schema_user.UserResponse,
    tags=["Users"]
)
async def create_user(
    user_data: schemas.schema_user.UserCreate,
    db: Session = Depends(get_db)
):
    # Validar duplicado por nombre
    existing_user = crud.crud_user.get_user_by_nombre(
        db,
        user_data.nombre
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    return crud.crud_user.create_user(db=db, user=user_data)


# ==============================
# ACTUALIZAR USUARIO (PROTEGIDO)
# ==============================
@user.put(
    "/user/{user_id}",
    response_model=schemas.schema_user.UserResponse,
    tags=["Users"]
)
async def update_user(
    user_id: int,
    user_data: schemas.schema_user.UserUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_user = crud.crud_user.update_user(
        db=db,
        user_id=user_id,
        user=user_data
    )

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return db_user


# ==============================
# ELIMINAR USUARIO (PROTEGIDO)
# ==============================
@user.delete(
    "/user/{user_id}",
    response_model=schemas.schema_user.UserResponse,
    tags=["Users"]
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_user = crud.crud_user.delete_user(
        db=db,
        user_id=user_id
    )

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return db_user


# ==============================
# LOGIN
# ==============================
@user.post("/login", tags=["Login"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2 usa "username" por defecto
    user = crud.crud_user.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    access_token = create_access_token(
        data={"sub": str(user.nombre), "rol_id": user.rol_Id}
    )   

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }