from typing import Any

from fastapi import APIRouter, Path, Depends, Query
from starlette import status

from auth import filter_for_role
from enums import UserRole
from models import GenreRequest, GenreResponse, PaginatedResponse
from service import GenreService, get_genre_service

genre_router = APIRouter(prefix="/genre")


@genre_router.get("/get/{genre_id}", status_code=status.HTTP_200_OK, response_model=GenreResponse)
async def get_genre(service: GenreService = Depends(get_genre_service),
                    payload: Any = Depends(filter_for_role(UserRole.ANY)),
                    genre_id: int = Path(gt=0)):

    return service.get_genre(genre_id)


@genre_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=GenreRequest)
async def create_genre(genre_request: GenreRequest,
                       service: GenreService = Depends(get_genre_service),
                       payload: Any = Depends(filter_for_role(UserRole.ANY))):

    return service.create_genre(genre_request)


@genre_router.get("/get-all", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[GenreResponse])
async def get_all(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1),
        service: GenreService = Depends(get_genre_service),
        payload: Any = Depends(filter_for_role(UserRole.ANY)),
):

    return service.get_genres(page, page_size)
