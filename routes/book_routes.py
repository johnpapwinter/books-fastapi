from typing import Any

from fastapi import APIRouter, Path, HTTPException, Depends, Query
from starlette import status

from auth import filter_for_role
from enums import UserRole
from models import BookRequest, SearchRequest, PaginatedResponse, BookResponse
from service import BookService, get_book_service

router = APIRouter(prefix="/book")


@router.get("/get-all", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[BookResponse])
async def get_all(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1),
        service: BookService = Depends(get_book_service),
        payload: Any = Depends(filter_for_role(UserRole.ANY))):

    return service.get_all_books(page, page_size)


@router.get("/get/{book_id}", status_code=status.HTTP_200_OK, response_model=BookResponse)
async def get_one(service: BookService = Depends(get_book_service),
                  payload: Any = Depends(filter_for_role(UserRole.ANY)),
                  book_id: int = Path(gt=0)):

    return service.get_book(book_id)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=BookRequest)
async def create_book(book_request: BookRequest,
                      service: BookService = Depends(get_book_service),
                      payload: Any = Depends(filter_for_role(UserRole.ANY))):

    return service.create_new_book(book_request)


@router.patch("/update", status_code=status.HTTP_200_OK, response_model=BookRequest)
async def update_book(book_request: BookRequest,
                      service: BookService = Depends(get_book_service),
                      payload: Any = Depends(filter_for_role(UserRole.ANY))):

    if book_request.id is None:
        raise HTTPException(status_code=400, detail="Id should not be null")

    return service.update_book(book_request.id, book_request)


@router.delete("/delete/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0),
                      payload: Any = Depends(filter_for_role(UserRole.ADMIN))):

    return {"message": f"I deleted book with id {book_id}"}


@router.post("/search", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[BookRequest])
async def search_book(
        search_filters: SearchRequest,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1),
        service: BookService = Depends(get_book_service),
        payload: Any = Depends(filter_for_role(UserRole.ANY))):

    return service.search_books(search_filters, page, page_size)
