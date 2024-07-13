from sqlmodel import Session, create_engine
import csv, datetime, os

from app.db.models import User, Book, Review, Bookmark 


# Replace with your actual database URL
DATABASE_URL = "sqlite:///app/test.db"
engine = create_engine(DATABASE_URL)

def insert_from_csv(model, csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        items = []
        for row in reader:
            # Convert datetime fields to Python datetime objects
            if 'created_at' in row:
                row['created_at'] = datetime.datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
            if 'publish_date' in row:
                row['publish_date'] = datetime.datetime.strptime(row['publish_date'], '%Y-%m-%d')
            # Convert is_admin to boolean
            if 'is_admin' in row:
                row['is_admin'] = row['is_admin'].lower() == 'true'  # Convert 'True'/'False' strings to boolean
            
            item = model(**row)
            items.append(item)
        
        with Session(engine) as session:
            session.add_all(items)
            session.commit()

# Path to CSV files
fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
csv_files = {
    User: os.path.join(fixtures_dir, 'users.csv'),
    Review: os.path.join(fixtures_dir, 'reviews.csv'),
    Bookmark: os.path.join(fixtures_dir, 'bookmarks.csv'),
    Book: os.path.join(fixtures_dir, 'books.csv'),
}

# Insert data for each model
for model, csv_path in csv_files.items():
    insert_from_csv(model, csv_path)
