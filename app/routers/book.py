from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select, func, case
from app.schemas.schema import BookDetails, BooksRetrieve, UserReview, BookCreate
from app.db import models, database
from app.routers.auth import get_current_user

router = APIRouter(prefix='/book', tags=['book'])

@router.post("/create/", response_model=models.Book)
async def create_book(book: BookCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.is_admin != True:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/all_books", response_model=list[BooksRetrieve])
async def get_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    statement = select(
        models.Book.id,
        models.Book.title,
        models.Book.description,
        models.Book.publish_date,
        func.count(models.Bookmark.id).label("book_marked_count"),
    ).outerjoin(models.Bookmark).group_by(models.Book.id).offset(skip).limit(limit)
    
    result = db.execute(statement)
    books = result.all()
    
    return books

@router.get("/detail/{book_id}", response_model=BookDetails)
async def get_book(book_id: int, db: Session = Depends(database.get_db)):
    statement = select(
        models.Book.id,
        models.Book.title,
        models.Book.description,
        models.Book.publish_date,
        func.count(models.Bookmark.id).label("book_marked_count"),
        func.count(models.Review.comment).label("review_comments_count"),
        func.count(models.Review.score).label("review_score_count"),
        func.coalesce(func.avg(models.Review.score), 0).label("average_review_score"),
        func.count(case((models.Review.score == 1, 1))).label("score_one_count"),
        func.count(case((models.Review.score == 2, 1))).label("score_two_count"),
        func.count(case((models.Review.score == 3, 1))).label("score_three_count"),
        func.count(case((models.Review.score == 4, 1))).label("score_four_count"),
        func.count(case((models.Review.score == 5, 1))).label("score_five_count"),
        models.User.id.label("user_id"),
        models.User.name.label("user_name"),
        models.Review.comment.label("review_comment"),
        models.Review.score.label("review_score")
    ).select_from(models.Book).where(models.Book.id == book_id).outerjoin(
        models.Bookmark, models.Bookmark.book_id == models.Book.id
    ).outerjoin(
        models.Review, models.Review.book_id == models.Book.id
    ).outerjoin(
        models.User, models.User.id == models.Review.owner_id
    ).group_by(
        models.Book.id,
        models.User.id,
        models.Review.comment,
        models.Review.score
    )

    result = db.execute(statement)
    book_data = result.fetchall()

    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")

    book_details = book_data[0]
    user_reviews = [
        UserReview(
            user_id=row.user_id,
            user_name=row.user_name,
            review_comment=row.review_comment,
            review_score=row.review_score
        ) for row in book_data if row.user_id is not None
    ]

    return BookDetails(
        id=book_details.id,
        title=book_details.title,
        description=book_details.description,
        publish_date=book_details.publish_date,
        book_marked_count=book_details.book_marked_count,
        review_comments_count=book_details.review_comments_count,
        review_score_count=book_details.review_score_count,
        average_review_score=book_details.average_review_score,
        score_one_count=book_details.score_one_count,
        score_two_count=book_details.score_two_count,
        score_three_count=book_details.score_three_count,
        score_four_count=book_details.score_four_count,
        score_five_count=book_details.score_five_count,
        user_reviews=user_reviews
    )