from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Book, BookRequest


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_book(self, book_id: int) -> BookRequest | None:
        result = self.db.query(Book).filter(Book.id == book_id).first()
        return BookRequest.model_validate(result) if result else None

    def get_all_books(self) -> list[BookRequest]:
        result = self.db.query(Book).all()
        return [BookRequest.model_validate(book) for book in result]

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

    def update_book(self, book_id: int, book: BookRequest) -> BookRequest:
        result = self.db.query(Book).filter(Book.id == book_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = book.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(result, key, value)

        try:
            self.db.commit()
            self.db.refresh(result)
        except Exception as e:
            print(e)
            self.db.rollback()

        return BookRequest.model_validate(result)


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)

