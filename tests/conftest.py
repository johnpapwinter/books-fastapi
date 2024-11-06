import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.test import TestSettings
from database import Base, get_db
from main import app
from models import GenreRequest, Book, BookRequest
from service.book_service import BookService
from service.genre_service import GenreService
from initialization import initialize_db

import config


@pytest.fixture(scope="session")
def test_settings():
    return TestSettings()


@pytest.fixture
def test_db(test_settings: TestSettings) -> Session:
    # Use a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    database_url = f"sqlite:///{db_path}"

    # Create test database
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Initialize database
    initialize_db()

    # Get database session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def book_service(test_db):
    return BookService(test_db)


@pytest.fixture
def genre_service(test_db):
    return GenreService(test_db)


@pytest.fixture
def sample_genre(genre_service):
    genre_data = GenreRequest(name="Epic Fantasy")
    return genre_service.create_genre(genre_data)


@pytest.fixture
def sample_book(book_service):
    book_data = BookRequest(
        title="Test Book",
        author="Test Author",
        year=2010,
        pages=300
    )
    return book_service.create_new_book(book_data)