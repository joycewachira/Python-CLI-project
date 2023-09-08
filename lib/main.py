import click
from models import User, Book, Checkout
from database import session, initialize_database
from datetime import datetime, timedelta

# Initialize the database (create tables if they don't exist)
initialize_database()

# Define a Click command with options
@click.command()
@click.option('--username', prompt='Username')
@click.password_option()
@click.option('--full_name', prompt='Full Name')
@click.option('--email', prompt='Email')
@click.option('--phone_number', prompt='Phone Number')
def register_user(username, password, full_name, email, phone_number):
    # Register a new user.
    user = User(username=username, password=password, full_name=full_name, email=email, phone_number=phone_number)
    session.add(user)
    session.commit()
    print(f'User {username} registered successfully.')

@click.command()
@click.option('--title', prompt='Title')
@click.option('--author', prompt='Author')
@click.option('--isbn', prompt='ISBN')
@click.option('--genre', prompt='Genre')
def add_new_book(title, author, isbn, genre):
    # Add a new book to the library catalog.
    book = Book(title=title, author=author, isbn=isbn, genre=genre)
    session.add(book)
    session.commit()
    print(f'Book "{title}" added to the catalog successfully.')

@click.command()
@click.option('--user_id', prompt='User ID', type=int)
@click.option('--book_id', prompt='Book ID', type=int)
def checkout_book(user_id, book_id):
    # Check out a book for a user.
    user = session.query(User).filter_by(user_id=user_id).first()
    book = session.query(Book).filter_by(book_id=book_id).first()

    if not user:
        print('User not found.')
        return
    if not book:
        print('Book not found.')
        return

    checkout_date = datetime.now().date()
    due_date = checkout_date + timedelta(days=14)

    checkout = Checkout(user_id=user_id, book_id=book_id, checkout_date=checkout_date, due_date=due_date)
    session.add(checkout)
    session.commit()
    print(f'Book "{book.title}" checked out successfully for {user.full_name}.')

@click.command()
@click.option('--user_id', prompt='User ID', type=int)
@click.option('--book_id', prompt='Book ID', type=int)
def return_book(user_id, book_id):
    # Return a book.
    checkout = session.query(Checkout).filter_by(user_id=user_id, book_id=book_id, returned=False).first()

    if not checkout:
        print('Book not checked out by this user.')
        return

    checkout.returned = True
    session.commit()
    print(f'Book "{checkout.book.title}" returned successfully by {checkout.user.full_name}.')

if __name__ == '__main__':
    # Use these commands to register a user, add a new book, checkout, and return a book.
    register_user()
    add_new_book()
    checkout_book()
    return_book()
