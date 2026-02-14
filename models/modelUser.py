'''
Docstring for models.modelUser
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from config.db import Base

class User(Base):
    ''' Docstring for User'''
    __tablename__ = "tbb_users"
    Id = Column(Integer, primary_key=True, index=True)
    rol_Id = Column(Integer, ForeignKey("tbc_roles.Id"))
    nombre = Column(String(60))
    papellido = Column(String(60))
    sapellido = Column(String(60))
    direccion = Column(String(100))
    correo_electronico = Column(String(60))
    numero_telefono = Column(String(10)) 
    contrasena = Column(String(60))  
    estatus = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_modificacion = Column(DateTime)