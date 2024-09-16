import logging
from typing import Optional, Type, TypeVar
from fastapi import Depends, APIRouter, HTTPException, Request, Response

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

from sqlalchemy.orm import Session
from providers.database import BaseDeDatos

from models.models import Base, SessionLocal, engine
from models.models import Producto

from scheme.schemes import ProductoSchemaCreate, ProductoSchemaDelete, ProductoSchemaGetAll, ProductoSchemaGetOne, ProductoSchemaUpdate

logger = logging.getLogger(f'{__name__}')

def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as error:
        print(error.args)
    finally:
        db.close()

T = TypeVar('T', bound=BaseModel)
 

router = APIRouter(prefix="/productos")

@router.get('/', tags=["Productos"])
async def obtener_productos(producto_id: Optional[int] = None, db: Session = Depends(get_db)):
    if producto_id:
        db_producto = db.query(Producto).filter(Producto.codigo == producto_id).first()
        logger.info(db_producto)
        if not db_producto:
            return JSONResponse(status_code=404, content={"estado":"producto no encontrado"})
        return db_producto.__dict__
    db_producto = db.query(Producto).filter().all()
    if not db_producto:
        return JSONResponse(status_code=404, content={"estado":"producto no encontrado"})
    return {'lista_productos': [producto.__dict__ for producto in db_producto]}

@router.post('/', tags=["Productos"])
async def crear_producto(producto: ProductoSchemaCreate, db: Session = Depends(get_db)):
    try:
        producto_db = Producto(
            codigo = producto.codigo,
            nombre = producto.nombre,
            descripcion = producto.descripcion,
            precio = producto.precio,
            foto = producto.foto
        )
        db.add(producto_db)
        db.commit()
        db.refresh(producto_db)
        logger.info(producto_db)
        return producto_db.__dict__
    except Exception as error:
        logger.error(error.args)
        return
@router.put('/{producto_id}', tags=["Productos"])
async def modificar_producto(producto_id: Optional[int] = None, db: Session = Depends(get_db)):
    pass

@router.delete('/{producto_id}', tags=["Productos"])
async def eliminar_producto(producto_id: Optional[int] = None, db: Session = Depends(get_db)):
    pass