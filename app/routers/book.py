from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.db import models, database


router = APIRouter(prefix='/books', tags=['book'])

class BookRetrieve(BaseModel):
    id: int
    title: str
    description: str
    publish_date: datetime

    class Config:
        orm_mode = True

@router.get("/get_books", response_model=list[BookRetrieve])
async def get_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    statement = select(models.Book).offset(skip).limit(limit)
    result = db.execute(statement)
    books = result.scalars().all()
    return books

@router.get("/book/{book_id}", response_model=BookRetrieve)
async def get_book(book_id: int, db: Session = Depends(database.get_db)):
    statement = select(models.Book).where(models.Book.id == book_id)
    result = db.execute(statement)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book