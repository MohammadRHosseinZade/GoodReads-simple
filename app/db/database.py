from sqlmodel import SQLModel, create_engine, Session
from app.db import models

DATABASE_URL = "sqlite:///app/test.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

if __name__=="__main__":
    create_db_and_tables()
