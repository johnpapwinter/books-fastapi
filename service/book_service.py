from math import ceil

from fastapi import Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from models import Book, BookRequest, SearchRequest, PaginatedResponse


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_book(self, book_id: int) -> BookRequest | None:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        return BookRequest.model_validate(book) if book else None

    def get_all_books(self, page: int = 1, page_size: int = 10) -> PaginatedResponse[BookRequest]:
        # books = self.db.query(Book).all()
        # return [BookRequest.model_validate(book) for book in books]
        query = self.db.query(Book)
        return self._paginate(query, page, page_size)

    def create_new_book(self, book: BookRequest) -> BookRequest:
        new_book = Book(title=book.title, author=book.author, year=book.year, pages=book.pages)
        try:
            self.db.add(new_book)
            self.db.commit()
            self.db.refresh(new_book)
        except Exception as e:
            print(e)
            self.db.rollback()

        return BookRequest.model_validate(new_book)

    def update_book(self, book_id: int, updated_book: BookRequest) -> BookRequest:
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = updated_book.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)

        try:
            self.db.commit()
            self.db.refresh(book)
        except Exception as e:
            print(e)
            self.db.rollback()

        return BookRequest.model_validate(book)

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

    def _paginate(self, query, page: int, page_size: int) -> PaginatedResponse[BookRequest]:
        total_items = query.count()
        total_pages = ceil(total_items / page_size)

        items = query.offset(page - 1).limit(page_size).all()
        book_requests = [BookRequest.model_validate(book) for book in items]

        return PaginatedResponse(
            items=book_requests,
            current_page=page,
            total_pages=total_pages,
            total_items=total_items,
        )


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)
