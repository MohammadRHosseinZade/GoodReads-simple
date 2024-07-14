from sqlmodel import Session, create_engine
import csv, datetime, os
from app.core import security
from app.db.models import User, Book, Review, Bookmark 
from app.db.database import DATABASE_URL


engine = create_engine(DATABASE_URL)

def insert_from_csv(model, csv_file_path):
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        items = []
        for row in reader:
            if 'created_at' in row:
                row['created_at'] = datetime.datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
            if 'publish_date' in row:
                row['publish_date'] = datetime.datetime.strptime(row['publish_date'], '%Y-%m-%d')
            if 'is_admin' in row:
                row['is_admin'] = row['is_admin'].lower() == 'true'  # Convert 'True'/'False' strings to boolean
            
            item = model(**row)
            items.append(item)
        
        with Session(engine) as session:
            session.add_all(items)
            session.commit()


fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
csv_files = {
    Book: os.path.join(fixtures_dir, 'books.csv'),
    User: os.path.join(fixtures_dir, 'users.csv'),
    Review: os.path.join(fixtures_dir, 'reviews.csv'),
    Bookmark: os.path.join(fixtures_dir, 'bookmarks.csv'),
    
}




def create_admin_user():
    admin_user = User(
        name="Admin User",
        email=os.environ.get("DEFAULT_ADMIN_USER", default="admin@example.com"),
        hashed_password=security.get_password_hash(password=os.environ.get("DEFAULT_ADMIN_PASSWORD","123321456")),
        is_admin=True,
        created_at=datetime.datetime.now()
    )
    with Session(engine) as session:
        session.add(admin_user)
        session.commit()



if __name__ == "__main__":
    create_admin_user()   
    for model, csv_path in csv_files.items():
        insert_from_csv(model, csv_path)     