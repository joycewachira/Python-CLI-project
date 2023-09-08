import click
from database import add_user, add_book, add_checkout, get_user_by_username, get_book_by_isbn, get_checked_out_books_by_user
from datetime import datetime, timedelta

@click.group()
def cli():
    """
    Library Management System CLI.
    """
    pass

@cli.command()
@click.option('--username', prompt=True, help='Username')
@click.option('--password', prompt=True, hide_input=True, help='Password')
@click.option('--full_name', prompt=True, help='Full Name')
@click.option('--email', prompt=True, help='Email')
@click.option('--phone_number', prompt=True, help='Phone Number')
def add_user_command(username, password, full_name, email, phone_number):
    """
    Add a new user to the library system.
    """
    add_user(username, password, full_name, email, phone_number)
    click.echo(f'User {username} added successfully.')

@cli.command()
@click.option('--title', prompt=True, help='Title')
@click.option('--author', prompt=True, help='Author')
@click.option('--isbn', prompt=True, help='ISBN')
@click.option('--genre', prompt=True, help='Genre')
def add_book_command(title, author, isbn, genre):
    """
    Add a new book to the library catalog.
    """
    add_book(title, author, isbn, genre)
    click.echo(f'Book "{title}" added successfully.')

@cli.command()
@click.option('--username', prompt=True, help='Username of the user checking out the book')
@click.option('--isbn', prompt=True, help='ISBN of the book being checked out')
def check_out_command(username, isbn):
    """
    Check out a book.
    """
    user = get_user_by_username(username)
    if not user:
        click.echo(f'User {username} not found.')
        return

    book = get_book_by_isbn(isbn)
    if not book:
        click.echo(f'Book with ISBN {isbn} not found.')
        return

    # Calculate due date (e.g., 14 days from today)
    checkout_date = datetime.now().date()
    due_date = checkout_date + timedelta(days=14)

    add_checkout(user.user_id, book.book_id, checkout_date, due_date)
    click.echo(f'Book "{book.title}" checked out by {username} successfully.')

@cli.command()
@click.option('--username', prompt=True, help='Username of the user returning the book')
@click.option('--isbn', prompt=True, help='ISBN of the book being returned')
def return_book_command(username, isbn):
    """
    Return a book.
    """
    user = get_user_by_username(username)
    if not user:
        click.echo(f'User {username} not found.')
        return

    book = get_book_by_isbn(isbn)
    if not book:
        click.echo(f'Book with ISBN {isbn} not found.')
        return

    # Find the checkout entry for this book by the user
    checkout = next((c for c in user.checkouts if c.book_id == book.book_id and not c.returned), None)

    if not checkout:
        click.echo(f'User {username} has not checked out the book "{book.title}".')
        return

    # Mark the book as returned
    checkout.returned = True
    click.echo(f'Book "{book.title}" returned by {username} successfully.')

@cli.command()
@click.option('--username', prompt=True, help='Username of the user searching for books')
@click.option('--genre', help='Genre to filter by (optional)')
def search_books_command(username, genre):
    """
    Search for books.
    """
    user = get_user_by_username(username)
    if not user:
        click.echo(f'User {username} not found.')
        return

    # Retrieve checked-out books by the user
    checked_out_books = get_checked_out_books_by_user(user.user_id)

    if genre:
        # Filter by genre if specified
        checked_out_books = [book for book in checked_out_books if book.genre == genre]

    if not checked_out_books:
        click.echo(f'No books found for user {username}.')
        return

    click.echo(f'Books checked out by {username}:')
    for book in checked_out_books:
        click.echo(f'- {book.title} by {book.author} (ISBN: {book.isbn}, Genre: {book.genre})')

if __name__ == '__main__':
    cli()
