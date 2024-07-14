from pydantic import BaseModel
from datetime import datetime



class Token(BaseModel):
    access_token: str
    token_type: str    

class BooksRetrieve(BaseModel):
    id: int
    title: str
    description: str
    publish_date: datetime
    book_marked_count: int
    


    class Config:
        orm_mode = True

class BookDetails(BooksRetrieve):
    review_comments_count: int
    review_score_count: int
    average_review_score: float
    score_one_count: int
    score_two_count: int
    score_three_count: int
    score_four_count: int
    score_five_count: int
    user_reviews: list["UserReview"] 

class UserReview(BaseModel):
    user_id: int
    user_name: str
    review_comment: str
    review_score: int

    class Config:
        orm_mode = True        

class BookCreate(BaseModel):
    title: str
    description: str
    publish_date: datetime

class BookUpdate(BookCreate):
    pass    

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    
