from fastapi import FastAPI
from app.routers import auth, book, bookmark, review
from app.db.database import create_db_and_tables

create_db_and_tables()
app = FastAPI()


app.include_router(auth.router)
app.include_router(book.router)
app.include_router(bookmark.router)
app.include_router(review.router)