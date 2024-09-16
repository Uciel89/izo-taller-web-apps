from fastapi import Depends, FastAPI, Request, Response

from starlette.background import BackgroundTask

from sqlalchemy.orm import Session

import logging
from pathlib import Path

from backend.providers.database import BaseDeDatos
from backend.custom_logging import CustomizeLogger

titulo = "Refugio del Remo"
descripcion =   "Sistema para carga de clientes y kayaks de clientes, además de login de los operarios del sistema con autenticación JWT"
tags_metadata = [
    {
        "name": "Clientes",
        "description": "Endpoints relacionados a clientes.",
    },
    {
        "name": "Embarcaciones",
        "description": "Endpoints relacionados a embarcaciones.",
    },
    {
        "name": "Pagos",
        "description": "Endpoints relacionados a los pagos." 
    },
    {
        "name": "Mails",
        "description": "Endpoints relacionados a los mails." 
    },
    {
        "name": "Parametros",
        "description": "Endpoints relacionados a obtención y modificación de parámetros." 
    },
    {
        "name": "Autenticación",
        "description": "Endpoints relacionados a la autenticación y seguridad del sistema." 
    },
]

app = FastAPI(title = titulo, 
              description=descripcion , 
              openapi_tags=tags_metadata,
              )

logger = logging.getLogger(f'{__name__}')

config_path=Path(__file__).with_name("logging_config.json")
logger = CustomizeLogger.make_logger(config_path)
print(config_path)

def log_info(req_body, res_body):
    logging.info(req_body)
    logging.info(res_body)

@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    response = await call_next(request)
    logging.info(request.headers)
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    task = BackgroundTask(log_info, req_body, res_body)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)


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
        
@app.get("/")
async def ping(db: Session = Depends(get_db)):
    return 'pong'