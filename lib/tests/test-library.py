# test-library.py

import pytest
from main import register_user, add_new_book, checkout_book, search_books
from models import User, Book
from database import session, initialize_database
from datetime import datetime, timedelta

# ... (Previous code for setup_database and user registration test)

def test_book_checkout(setup_database):
    # Customize the checkout data for testing
    user_id = 2023  # Replace with the actual User ID from your database.
    book_id = 57    # Replace with the actual Book ID from your database.

    # Simulate book checkout
    checkout_book(user_id, book_id)

    # Retrieve the user's checked-out books
    checked_out_books = session.query(Book).filter(Book.checkouts.any(user_id=user_id, returned=False)).all()

    # Assertions to check if the book was checked out successfully
    assert len(checked_out_books) == 1
    assert checked_out_books[0].title == 'Test Book'

def test_search_books(setup_database):
    # Customize the search query for testing
    query = 'Mystery'  # Replace with a suitable search query for your test scenario.

    # Perform book search
    search_results = search_books(query)

    # Assertions to check if search returned results
    assert len(search_results) > 0
    for book in search_results:
        assert query.lower() in book.title.lower() or query.lower() in book.author.lower()

if __name__ == '__main__':
    pytest.main()
