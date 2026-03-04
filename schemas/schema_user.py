'''
Docstring for schemas.schema_user
'''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    '''Clase para modelar los campos de tabla Usuarios'''
    rol_Id: int
    nombre: str
    papellido: str             
    sapellido: str
    direccion: str
    correo_electronico: str
    numero_telefono: str
    
    
# pylint: disable=too-few-public-methods, unnecessary-pass
class UserCreate(UserBase):
    contrasena: str
    '''Clase para crear un Rol basado en la tabla Rols'''
    pass
class UserUpdate(UserBase):
    '''Clase para actualizar un Rol basado en la tabla Rols'''
    pass

class UserResponse(UserBase):
    Id: int
    estatus: bool
    fecha_registro: datetime
    fecha_modificacion: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    '''Clase para realizar login por numero de telefono o correo'''
    numero_telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    contrasena: str
