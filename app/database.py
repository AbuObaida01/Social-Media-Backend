from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase,sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic_settings import BaseSettings
from .config import settings
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
load_dotenv()

# print("CWD:", os.getcwd())
# print("ENV EXISTS:", os.path.exists(".env"))
# print("FROM OS ENV:", os.getenv("DATABASE_URL"))
# The format of connectiong with the DB

# DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'



# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD").strip())
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# DATABASE_URL = (
#     f"postgresql://{settings.database_username}:{quote_plus(settings.database_password)}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# )

DATABASE_URL=os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL=DATABASE_URL.replace("postgres://","postgresql+psycopg2://",1)
# print("DATABASE_URL:", DATABASE_URL)
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

SessionLocal= sessionmaker(bind=engine)

def get_db():
    with SessionLocal() as db:
        yield db


# #Coonectiong to the database another method using psycopd
# while True:
#     try:
#         conn=psycopg2.connect(host='23', database='abcd',port=1234, user='POSTGRE', password='Password', cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connected")
#         break
#     except Exception as error:
#         print("failed")
#         print("Error", error)
#         time.sleep(2)