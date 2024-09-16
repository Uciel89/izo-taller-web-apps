from fastapi import Depends, APIRouter, File, Form, HTTPException, Request, Response, UploadFile

from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

from sqlalchemy.orm import Session
from providers.database import BaseDeDatos

from models.models import Base, SessionLocal, engine
from models.models import Producto

from scheme.schemes import ProductoSchemaCreate, ProductoSchemaDelete, ProductoSchemaGetAll, ProductoSchemaGetOne, ProductoSchemaUpdate

import os
import logging
from typing import Optional, Type, TypeVar
import aiofiles

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

@router.get('/imagen/{id_imagen}', tags=["Productos"])
async def obtener_imagen(id_imagen: int, db: Session = Depends(get_db)):
    try:
        producto_db = db.query(Producto).filter(Producto.codigo == id_imagen).first()
    except Exception as error:
        logger.exception(error.args)
        return JSONResponse(content= {'estado':'no existe registro'}, status_code= 404)
    
    if os.path.exists(f'uploads/{producto_db.foto}'):
        return FileResponse(f'uploads/{producto_db.foto}')
    return JSONResponse(content= {'estado':'foto no encontrada'}, status_code= 404)

@router.post('/', tags=["Productos"], response_model=ProductoSchemaGetOne)
async def crear_producto(   
                            codigo: int = Form(...),
                            nombre: str = Form(...),
                            descripcion: Optional[str] = Form(None),
                            precio: float = Form(...),
                            foto: UploadFile = File(...),
                            db: Session = Depends(get_db)):
    
    try:
        producto_db = Producto(
            codigo = codigo,
            nombre = nombre,
            descripcion = descripcion,
            precio = precio,
            foto = f'{codigo}.{foto.filename.split(".")[-1]}'
        )
        db.add(producto_db)
        db.commit()
        db.refresh(producto_db)
        
        out_file_path = 'uploads/' + producto_db.foto
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            content = await foto.read()
            await out_file.write(content)
        return producto_db.__dict__
    except Exception as error:
        logger.error(error.args)
        return {"estado": error.args}
    
@router.put('/{producto_id}', tags=["Productos"])
async def modificar_producto(producto_id: Optional[int] = None, db: Session = Depends(get_db)):
    pass

@router.delete('/{producto_id}', tags=["Productos"])
async def eliminar_producto(producto_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        db.query(Producto).filter(Producto.codigo == producto_id).delete()
        db.commit()
        return JSONResponse(content={"estado":"producto eliminado correctamente"})
    except Exception as error:
        logger.exception('Error durante consulta de delete')
        return JSONResponse(content={"estado":"producto no encontrado"}, status_code=404)