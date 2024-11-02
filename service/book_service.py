from fastapi import Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from database import get_db
from error_messages import ErrorMessages
from models import Book, BookRequest, SearchRequest, PaginatedResponse, BookResponse, Genre
from service.generic_service import GenericService


class BookService(GenericService[Book, BookRequest]):
    def __init__(self, db: Session):
        super().__init__(db, Book, BookRequest)

    def get_book(self, book_id: int) -> BookResponse | None:
        """
        Retrieve a book by its ID.
        Args: book_id (int): The ID of the book to retrieve.
        Returns: BookResponse | None: The book response if found, otherwise None.
        """
        book = self.db.query(Book).options(joinedload(self.model.genre)).filter(Book.id == book_id).first()
        return BookResponse.model_validate(book) if book else None

    def get_all_books(self, page: int = 1, page_size: int = 10) -> PaginatedResponse[BookResponse]:
        """
        Retrieve all books with pagination.
        Args:
            page (int): The page number to retrieve. Defaults to 1.
            page_size (int): The number of books per page. Defaults to 10.
        Returns:
            PaginatedResponse[BookResponse]: A paginated response of books.
        """
        query = self.db.query(Book).options(joinedload(self.model.genre))
        return self._paginate(query, page, page_size)

    def create_new_book(self, book: BookRequest) -> BookRequest:
        """
        Create a new book.
        Args: book (BookRequest): The book request containing the book details.
        Returns: BookRequest: The created book request.
        """
        return self.create(book)

    def update_book(self, book_id: int, updated_book: BookRequest) -> BookRequest:
        """
        Update an existing book.
        Args:
            book_id (int): The ID of the book to update.
            updated_book (BookRequest): The book request containing the updated book details.
        Returns:
            BookRequest: The updated book request.
        Raises:
            HTTPException: If the book is not found.
        """
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail=ErrorMessages.BOOK_NOT_FOUND.value)

        update_data = updated_book.model_dump(exclude_unset=True)
        return self.update(book, update_data)

    def search_books(self, search_filters: SearchRequest,
                     page: int = 1,
                     page_size: int = 10) -> PaginatedResponse[BookRequest]:
        """
        Search for books based on the provided search filters.
        Args:
            search_filters (SearchRequest): The search filters containing the search criteria.
            page (int): The page number to retrieve. Defaults to 1.
            page_size (int): The number of books per page. Defaults to 10.
        Returns:
            PaginatedResponse[BookRequest]: A paginated response of books matching the search criteria.
        """
        query = self.db.query(Book)

        if search_filters.title or search_filters.author:
            filters = []
            if search_filters.title:
                filters.append(Book.title.ilike(f"%{search_filters.title}%"))
            if search_filters.author:
                filters.append(Book.author.ilike(f"%{search_filters.author}%"))
            query = query.filter(or_(*filters))

        return self._paginate(query, page, page_size)

    def add_book_to_genre(self, book_id: int, genre_id: int) -> BookResponse:
        """
        Add a book to a genre.
        Args:
            book_id (int): The ID of the book to add to the genre.
            genre_id (int): The ID of the genre to add the book to.
        Returns:
            BookResponse: The updated book response.
        Raises:
            HTTPException: If the book or genre is not found.
        """
        book = self.db.query(Book).filter(Book.id == book_id).first()
        genre = self.db.query(Genre).filter(Genre.id == genre_id).first()
        if genre is None or book is None:
            raise HTTPException(status_code=404, detail=ErrorMessages.ENTITY_NOT_FOUND.value)

        book.genre_id = genre_id
        book.genre = genre

        return self._db_operation(lambda: self._refresh(book))


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)
