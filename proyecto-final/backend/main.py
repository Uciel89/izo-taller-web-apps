from fastapi import Depends, FastAPI, Request, Response

from starlette.background import BackgroundTask

from sqlalchemy.orm import Session

import logging
from pathlib import Path

from models.models import Base, SessionLocal, engine
from custom_logging import CustomizeLogger
from routes.productos import router as producto_router

titulo = "Seminario"
descripcion =   "CRUD de productos para seminario."
tags_metadata = [
    {
        "name": "Productos",
        "description": "Endpoints relacionados a operaciones con productos.",
    }
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
    if 'multipart/form-data' in request.headers.get('Content-Type', '') or 'x-www-form-urlencoded' in request.headers.get('Content-Type', ''):
        response = await call_next(request)
        return response

    req_body = await request.body()
    response = await call_next(request)
    
    logging.info(request.headers)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk

    if dict(response.headers).get('content-type') != 'image/png':
        task = BackgroundTask(log_info, req_body, res_body)
        return Response(content=res_body, status_code=response.status_code, 
                        headers=dict(response.headers), 
                        media_type=response.media_type, 
                        background=task)
    return Response(content=res_body, status_code=response.status_code, 
                        headers=dict(response.headers), 
                        media_type=response.media_type)
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
async def ping():
    return 'pong'

app.include_router(producto_router, prefix="/v1")