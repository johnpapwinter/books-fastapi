import pytest
from fastapi import HTTPException
from models import BookRequest, SearchRequest, PaginatedResponse, BookResponse
from error_messages import ErrorMessages


class TestBookService:
    def test_create_book_success(self, book_service):
        book_data = BookRequest(
            title="New Book",
            author="New Author",
            year=2024,
            pages=200
        )

        book = book_service.create_new_book(book_data)

        assert book.title == book_data.title
        assert book.author == book_data.author
        assert book.year == book_data.year
        assert book.pages == book_data.pages

    def test_get_book_success(self, book_service, sample_book):
        book = book_service.get_book(sample_book.id)

        assert book is not None
        assert isinstance(book, BookResponse)
        assert book.title == sample_book.title
        assert book.author == sample_book.author

    def test_get_book_not_found(self, book_service):
        book = book_service.get_book(999)  # Non-existent ID
        assert book is None

    def test_get_all_books_empty(self, book_service):
        result = book_service.get_all_books()

        assert isinstance(result, PaginatedResponse)
        assert result.total_pages == 0
        assert len(result.items) == 0

    def test_get_all_books_with_data(self, book_service):
        book_data = BookRequest(
            title="Test Book",
            author="Test Author",
            year=2024,
            pages=200
        )
        book_service.create_new_book(book_data)

        result = book_service.get_all_books()

        assert isinstance(result, PaginatedResponse)
        assert result.total_pages >= 1
        assert len(result.items) >= 1
        assert hasattr(result.items[0], 'title')
        assert hasattr(result.items[0], 'author')

    def test_get_all_books_pagination(self, book_service):
        # Create multiple books
        for i in range(15):
            book_service.create_new_book(
                BookRequest(
                    title=f"Book {i}",
                    author=f"Author {i}",
                    year=2024,
                    pages=200
                )
            )

        # Test first page
        page1 = book_service.get_all_books(page=1, page_size=10)
        assert len(page1.items) == 10

        # Test second page
        page2 = book_service.get_all_books(page=2, page_size=10)
        assert len(page2.items) == 5

    def test_update_book_success(self, book_service, sample_book):
        updated_data = BookRequest(
            title="Updated Title",
            author="Updated Author",
            year=2023,
            pages=250
        )

        updated_book = book_service.update_book(sample_book.id, updated_data)

        assert updated_book.title == updated_data.title
        assert updated_book.author == updated_data.author
        assert updated_book.year == updated_data.year
        assert updated_book.pages == updated_data.pages

    def test_update_book_not_found(self, book_service):
        updated_data = BookRequest(
            title="Updated Title",
            author="Updated Author",
            year=2023,
            pages=250
        )

        with pytest.raises(HTTPException) as exc_info:
            book_service.update_book(999, updated_data)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == ErrorMessages.BOOK_NOT_FOUND.value

    def test_search_books_by_title(self, book_service):
        # Create test books
        book_service.create_new_book(
            BookRequest(title="Python Programming", author="John Doe", year=2024, pages=200)
        )
        book_service.create_new_book(
            BookRequest(title="Java Programming", author="Jane Smith", year=2024, pages=200)
        )

        search_filters = SearchRequest(title="Python")
        result = book_service.search_books(search_filters)

        assert result.total_pages == 1
        assert "Python" in result.items[0].title

    def test_search_books_by_author(self, book_service):
        # Create test books
        book_service.create_new_book(
            BookRequest(title="Book 1", author="John Smith", year=2024, pages=200)
        )
        book_service.create_new_book(
            BookRequest(title="Book 2", author="Jane Doe", year=2024, pages=200)
        )

        search_filters = SearchRequest(author="Smith")
        result = book_service.search_books(search_filters)

        assert result.total_pages == 1
        assert "Smith" in result.items[0].author

    def test_search_books_no_results(self, book_service, sample_book):
        search_filters = SearchRequest(title="NonexistentBook")
        result = book_service.search_books(search_filters)

        assert result.total_pages == 0
        assert len(result.items) == 0

    def test_add_book_to_genre_book_not_found(self, book_service, sample_genre):
        with pytest.raises(HTTPException) as exc_info:
            book_service.add_book_to_genre(999, sample_genre.id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == ErrorMessages.ENTITY_NOT_FOUND.value

    def test_add_book_to_genre_genre_not_found(self, book_service, sample_book):
        with pytest.raises(HTTPException) as exc_info:
            book_service.add_book_to_genre(sample_book.id, 999)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == ErrorMessages.ENTITY_NOT_FOUND.value

