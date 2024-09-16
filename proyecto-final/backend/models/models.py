from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

from providers.database import BaseDeDatos
import uuid

bbdd = BaseDeDatos()
Base, SessionLocal, engine = bbdd.iniciar_conexion()

class Producto(Base):
    __tablename__ = 'productos'

    codigo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
    foto = Column(String, nullable=True)