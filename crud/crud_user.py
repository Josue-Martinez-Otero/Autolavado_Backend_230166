from datetime import datetime

import models.modelUser
import schemas.schema_user
from sqlalchemy.orm import Session
from config.security import hash_password, verify_password


# ==============================
# OBTENER USUARIOS
# ==============================
def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.modelUser.User).offset(skip).limit(limit).all()


# ==============================
# BUSCAR POR NOMBRE
# ==============================
def get_user_by_nombre(db: Session, nombre: str):
    return db.query(models.modelUser.User).filter(
        models.modelUser.User.nombre == nombre
    ).first()


# ==============================
# BUSCAR POR CORREO
# ==============================
def get_user_by_correo_electronico(db: Session, correo: str):
    return db.query(models.modelUser.User).filter(
        models.modelUser.User.correo_electronico == correo
    ).first()


# ==============================
# CREAR USUARIO
# ==============================
def create_user(db: Session, user: schemas.schema_user.UserCreate):

    hashed_password = hash_password(user.contrasena)

    db_user = models.modelUser.User(
        rol_Id=user.rol_Id,
        nombre=user.nombre,
        papellido=user.papellido,
        sapellido=user.sapellido,
        direccion=user.direccion,
        correo_electronico=user.correo_electronico,
        numero_telefono=user.numero_telefono,
        contrasena=hashed_password,
        estatus=True,
        fecha_registro=datetime.now(),
        fecha_modificacion=datetime.now()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ==============================
# ACTUALIZAR USUARIO
# ==============================
def update_user(db: Session, user_id: int, user: schemas.schema_user.UserUpdate):

    db_user = db.query(models.modelUser.User).filter(
        models.modelUser.User.Id == user_id
    ).first()

    if db_user is None:
        return None

    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# ==============================
# ELIMINAR USUARIO
# ==============================
def delete_user(db: Session, user_id: int):

    db_user = db.query(models.modelUser.User).filter(
        models.modelUser.User.Id == user_id
    ).first()

    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


# ==============================
# AUTENTICAR USUARIO
# ==============================
def authenticate_user(db: Session, email_o_tel: str, contrasena: str):

    usuario = db.query(models.modelUser.User).filter(
        (models.modelUser.User.nombre == email_o_tel) |
        (models.modelUser.User.correo_electronico == email_o_tel) |
        (models.modelUser.User.numero_telefono == email_o_tel)
    ).first()
    
    if not usuario:
        return None

    if not verify_password(contrasena, usuario.contrasena):
        return None

    return usuario