from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Book, Checkout  # Make sure you have these imports

# Replace 'sqlite:///library.db' with your database URL
DATABASE_URL = 'sqlite:///library.db'

# Create a SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def initialize_database():
    """
    Initialize the database by creating tables.
    """
    Base.metadata.create_all(engine)  # Fix the indentation here

def add_user(username, password, full_name, email, phone_number):
    """
    Add a new user to the 'users' table.
    """

    user = User(username=username, password=password, full_name=full_name, email=email, phone_number=phone_number)
    session.add(user)
    session.commit()

def add_book(title, author, isbn, genre):
    """
    Add a new book to the 'books' table.
    """

    book = Book(title=title, author=author, isbn=isbn, genre=genre)
    session.add(book)
    session.commit()

def add_checkout(user_id, book_id, checkout_date, due_date):
    """
    Add a new checkout entry to the 'checkouts' table.
    """

    checkout = Checkout(user_id=user_id, book_id=book_id, checkout_date=checkout_date, due_date=due_date)
    session.add(checkout)
    session.commit()

def get_user_by_username(username):
    """
    Retrieve a user by their username.
    """

    return session.query(User).filter_by(username=username).first()

def get_book_by_isbn(isbn):
    """
    Retrieve a book by its ISBN.
    """

    return session.query(Book).filter_by(isbn=isbn).first()

def get_checked_out_books_by_user(user_id):
    """
    Retrieve books checked out by a user.
    """

    return session.query(Book).join(Checkout).filter(Checkout.user_id == user_id, Checkout.returned == False).all()
