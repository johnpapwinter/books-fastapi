from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import GenreRequest, Genre, PaginatedResponse, GenreResponse
from service.generic_service import GenericService


class GenreService(GenericService[Genre, GenreRequest]):
    def __init__(self, db: Session):
        super().__init__(db, Genre, GenreRequest)

    def create_genre(self, genre: GenreRequest) -> GenreRequest:
        return self.create(genre)

    def get_genre(self, genre_id: int) -> GenreResponse | None:
        genre = (self.db.query(Genre).options(joinedload(self.model.books)).filter(Genre.id == genre_id).first())
        return GenreResponse.model_validate(genre) if genre else None

    def get_genres(self, page: int = 1, page_size = 10) -> PaginatedResponse[GenreResponse]:
        query = self.db.query(Genre).options(joinedload(self.model.books))
        return self._paginate(query, page, page_size)


def get_genre_service(db: Session = Depends(get_db)):
    return GenreService(db)
