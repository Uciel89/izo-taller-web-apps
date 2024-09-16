from fastapi import Depends, APIRouter, Request, Response

from starlette.background import BackgroundTask

from sqlalchemy.orm import Session
from providers.database import BaseDeDatos

db = BaseDeDatos()
Base, SessionLocal, engine = db.iniciar_conexion()

try:
    Base.metadata.create_all(bind=engine)
except Exception as err:
    print(err.args)

def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as error:
        print(error.args)
    finally:
        db.close()
        
router = APIRouter(prefix="/productos")

@router.get('/productos', tags=["Productos"])
async def obtener_productos():
    pass

@router.post('/productos', tags=["Productos"])
async def obtener_productos():
    pass

@router.put('/productos', tags=["Productos"])
async def obtener_productos():
    pass

@router.delete('/productos', tags=["Productos"])
async def obtener_productos():
    pass