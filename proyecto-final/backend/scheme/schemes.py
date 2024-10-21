from typing import List, Optional
from fastapi import File, UploadFile
from pydantic import BaseModel

class ProductoSchemaGetOne(BaseModel):
    codigo: int
    nombre: str
    descripcion: str
    precio: float
    foto: str

class ProductoSchemaGetAll(BaseModel):
    productos: List[ProductoSchemaGetOne]

class ProductoSchemaDelete(BaseModel):
    pass
    
class ProductoUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None

    class Config:
        orm_mode = True  # Esto permite usar el modelo directamente con las consultas ORM
class ProductoSchemaCreate(BaseModel):
    codigo: int
    nombre: str
    descripcion: Optional[str] = ""
    precio: float
    foto: Optional[UploadFile] = File()
    
    