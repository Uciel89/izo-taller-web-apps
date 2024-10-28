from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(f'{__name__}')


load_dotenv()


class BaseDeDatos():
    def __init__(self):
        self.db_path = os.getenv("DB_PATH")  

    def iniciar_conexion(self):
        SQLALCHEMY_DATABASE_URL = f'sqlite:///{self.db_path}'
        try:
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                connect_args={"check_same_thread": False}, 
                echo=True,
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base = declarative_base()
            return Base, SessionLocal, engine
        except Exception as err:
            logger.exception('ERROR DURANTE INICIALIZACIÓN BASE DE DATOS')
