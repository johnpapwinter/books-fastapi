from fastapi import Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from models import Book, BookRequest, SearchRequest, PaginatedResponse
from service.generic_service import GenericService


class BookService(GenericService[Book, BookRequest]):
    def __init__(self, db: Session):
        super().__init__(db, Book, BookRequest)

    def get_book(self, book_id: int) -> BookRequest | None:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        return BookRequest.model_validate(book) if book else None

    def get_all_books(self, page: int = 1, page_size: int = 10) -> PaginatedResponse[BookRequest]:
        query = self.db.query(Book)
        return self._paginate(query, page, page_size)

    def create_new_book(self, book: BookRequest) -> BookRequest:
        return self.create(book)

    def update_book(self, book_id: int, updated_book: BookRequest) -> BookRequest:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = updated_book.model_dump(exclude_unset=True)
        return self.update(book, update_data)

    def search_books(self, search_filters: SearchRequest,
                     page: int = 1,
                     page_size: int = 10) -> PaginatedResponse[BookRequest]:
        query = self.db.query(Book)

        if search_filters.title or search_filters.author:
            filters = []
            if search_filters.title:
                filters.append(Book.title.ilike(f"%{search_filters.title}%"))
            if search_filters.author:
                filters.append(Book.author.ilike(f"%{search_filters.author}%"))
            query = query.filter(or_(*filters))

        return self._paginate(query, page, page_size)


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)
