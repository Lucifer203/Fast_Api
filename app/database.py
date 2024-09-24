from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from .config import settings
from urllib.parse import quote_plus



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{quote_plus(settings.database_password)}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost',database='FastApi',
#                                 user='postgres',password='Adarsh@123',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successfull!!")
#         break
#     except Exception as error:
#         print("Connecting to database failed .")
#         print("Error: ",error)
#         time.sleep(2)