from typing import List, Optional
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
    
class ProductoSchemaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    foto: Optional[str] = None
    
class ProductoSchemaCreate(BaseModel):
    codigo: int
    nombre: str
    descripcion: Optional[str] = ""
    precio: float
    foto: Optional[str] = ""
    
    