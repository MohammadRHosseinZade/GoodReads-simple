from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select, func, case
from sqlalchemy.exc import NoResultFound
from app.schemas.schema import BookmarkCreate
from app.db import models, database
from app.routers.auth import get_current_user


router = APIRouter(prefix='/bookmark', tags=['bookmark'])

@router.post("/create/", response_model=models.Bookmark)
async def bookmark_book(bookmark: BookmarkCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Review).where(models.Review.book_id == bookmark.book_id, models.Review.owner_id == current_user.id)
    existing_review = db.execute(statement).scalar_one_or_none()
    if existing_review:
        raise HTTPException(status_code=400, detail="User has already reviewed this book and cannot bookmark it")
    new_bookmark = models.Bookmark(
        user_id=current_user.id,
        book_id=bookmark.book_id
    )
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    return new_bookmark

@router.delete("/delete/{bookmark_id}", response_model=dict)
async def delete_bookmark(bookmark_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    bookmark = db.get(models.Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    if bookmark.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db.delete(bookmark)
    db.commit()
    return {"detail": "Bookmark deleted successfully"}
