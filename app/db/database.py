from sqlmodel import SQLModel, create_engine, Session
from os import environ
from app.db import models

DB_USER = environ.get("DB_USER", "root")
DB_PASSWORD = environ.get("DB_PASSWORD", "fgdg09843hdg34yhgt43yfdg745")
DB_HOST = environ.get("DB_HOST", "goodreads_db")
DB_PORT = environ.get("DB_PORT", "5432")
DB_DBNAME = environ.get("DB_DBNAME", "GoodReads")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DBNAME}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

if __name__=="__main__":
    create_db_and_tables()
