from fastapi import Depends, FastAPI, Request, Response

from starlette.background import BackgroundTask

from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

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
    req_body = await request.body()
    response = await call_next(request)
    logging.info(request.headers)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    if len(req_body) > 1000 and len(res_body) > 1000:
        task = BackgroundTask(log_info, 'REQUEST MUY LARGO', 'RESPONSE MUY LARGA')
    elif len(res_body) > 1000:
        task = BackgroundTask(log_info, req_body, 'RESPONSE MUY LARGA')
    elif len(req_body) > 1000:
        task = BackgroundTask(log_info, 'REQUEST MUY LARGO', res_body)
    else:
        task = BackgroundTask(log_info, req_body, res_body)

    return Response(
        content=res_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
        background=task
    )


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
        
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

# Agregar middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def ping():
    return 'pong'

app.include_router(producto_router, prefix="/v1")