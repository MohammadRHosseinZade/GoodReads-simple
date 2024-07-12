from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from passlib.context import CryptContext
import datetime


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=False)
    email: str = Field(index=True, nullable=False, unique=True)
    # created_at: datetime.datetime = Field(default_factory=datetime.datetime.now())
    is_admin: bool = Field(default=False)
    hashed_password: str = Field(nullable=False)

    reviews: list["Review"] = Relationship(back_populates="owner")
    book_marked: list["Bookmark"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def create(cls, username: str, email: str, password: str):
        hashed_password = pwd_context.hash(password)
        return cls(username=username, email=email, hashed_password=hashed_password)
    

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, index=True)
    description: str = Field(nullable=False)
    publish_date: datetime.datetime = Field()

    reviews: list["Review"] = Relationship(back_populates="book")
    book_marks:list["Bookmark"] = Relationship(back_populates="book")


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    score: int = Field(nullable=True,ge=1,le=5)
    comment: str = Field(nullable=True)
    owner_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")

    owner: User = Relationship(back_populates="reviews")
    book: Book = Relationship(back_populates="reviews")


class Bookmark(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")

    user: User = Relationship(back_populates="book_marked")
    book: Book = Relationship(back_populates="reviews")