'''Docstring for schema.schema_user'''
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods

class RolBase(BaseModel):
    ''' Clase para modelar los campos de tabla Rols'''
    nombre: str
    estatus: bool

class RolCreate(RolBase):
    ''' Clase para crear un Rol basado en la tabla Rols'''
    pass

class RolUpdate(RolBase):
    ''' Clase para actualizar un Rol basado en la tabla Rols'''
    pass

class Rol(RolBase):
    '''Clase para realizar operaciones por ID en la tabla Rol'''
    id: int
    class Config:
        '''Utilizar el omr para ejecutar '''
        orm_mode = True