from sqlmodel import Session, create_engine
from db.models import Book 
import csv
import datetime

# Replace with your actual database URL
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

def insert_books_from_csv(csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        books = []
        for row in reader:
            book = Book(
                id=int(row['id']),
                title=row['title'],
                description=row['description'],
                publish_date=datetime.datetime.strptime(row['publish_date'], '%Y-%m-%d')
            )
            books.append(book)
        
        with Session(engine) as session:
            session.add_all(books)
            session.commit()


csv_file_path = '../fixtures/books.csv'
insert_books_from_csv(csv_file_path)
