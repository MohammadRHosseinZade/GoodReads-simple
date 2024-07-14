from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from app.schemas.schema import ReviewCreate
from app.db import models, database
from app.routers.auth import get_current_user


router = APIRouter(prefix='/review', tags=['review'])

@router.post("/create/", response_model=models.Review)
async def review_book(review: ReviewCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    statement = select(models.Bookmark).where(models.Bookmark.book_id == review.book_id, models.Bookmark.user_id == current_user.id)
    existing_bookmark = db.execute(statement).scalar_one_or_none()
    if existing_bookmark:
        db.delete(existing_bookmark)
        db.commit()
    new_review = models.Review(
        owner_id=current_user.id,
        book_id=review.book_id,
        score=review.score,
        comment=review.comment)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review