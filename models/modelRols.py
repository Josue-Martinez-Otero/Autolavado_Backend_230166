from sqlalchemy import Column, Integer, String, Boolean
# pylint: disable=import-error
from config.db import Base

# pylint: disable=too-few-public-methods
class Rols(Base):
    '''En este apartado se define la clase con sus atributos'''
    __tablename__ = "tbc_roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(15))
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    
