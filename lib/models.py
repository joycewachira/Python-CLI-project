from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLAlchemy engine and session
engine = create_engine('sqlite:///library.db') 
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Define the Users table
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String)
    phone_number = Column(String)
    
    # Define a one-to-many relationship with Checkouts
    checkouts = relationship('Checkout', back_populates='user')

# Define the Books table
class Book(Base):
    __tablename__ = 'books'
    
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    genre = Column(String)
    availability = Column(Boolean, default=True)
    
    # Define a one-to-many relationship with Checkouts
    checkouts = relationship('Checkout', back_populates='book')

# Define the Checkouts table
class Checkout(Base):
    __tablename__ = 'checkouts'
    
    checkout_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.book_id'), nullable=False)
    checkout_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    returned = Column(Boolean, default=False)
    
    # Define many-to-one relationships with Users and Books
    user = relationship('User', back_populates='checkouts')
    book = relationship('Book', back_populates='checkouts')

# Create the tables in the database
Base.metadata.create_all(engine)
