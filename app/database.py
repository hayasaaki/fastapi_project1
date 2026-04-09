import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg.rows import dict_row
from .config import settings 
import psycopg2

SQLALCHEMY_DATABASE_URL  = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

base  = declarative_base()

def get_db():
    db = sessionlocal()
    try :
        yield db
    finally :
        db.close()


# while True:
#     try:
#         conn = psycopg.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres', password = '41321234', row_factory= dict_row)
#         cursor =  conn.cursor()
#         print ("Succes")
#         break
#     except Exception as error :
#         print ("Failed, retrying...")
#         # print ("Error", error)
#         time.sleep(2)
#     raise RuntimeError("Nu sa reusit conectarea")