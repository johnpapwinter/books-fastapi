from fastapi import APIRouter, Path, HTTPException, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from models import BookRequest, SearchRequest, PaginatedResponse
from service import BookService, get_book_service, UserService, get_user_service

router = APIRouter(prefix="/book")


@router.get("/get-all", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[BookRequest])
async def get_all(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1),
        service: BookService = Depends(get_book_service),
        user_service: UserService = Depends(get_user_service),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    user_service.verify_token(credentials=credentials)

    return service.get_all_books(page, page_size)


@router.get("/get/{book_id}", status_code=status.HTTP_200_OK, response_model=BookRequest)
async def get_one(service: BookService = Depends(get_book_service),
                  user_service: UserService = Depends(get_user_service),
                  credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                  book_id: int = Path(gt=0)):
    user_service.verify_token(credentials=credentials)

    return service.get_book(book_id)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=BookRequest)
async def create_book(book_request: BookRequest,
                      service: BookService = Depends(get_book_service),
                      user_service: UserService = Depends(get_user_service),
                      credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                      ):

    return service.create_new_book(book_request)


@router.patch("/update", status_code=status.HTTP_200_OK, response_model=BookRequest)
async def update_book(book_request: BookRequest,
                      service: BookService = Depends(get_book_service),
                      user_service: UserService = Depends(get_user_service),
                      credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                      ):
    user_service.verify_token(credentials=credentials)

    if book_request.id is None:
        raise HTTPException(status_code=400, detail="Id should not be null")

    return service.update_book(book_request.id, book_request)


@router.delete("/delete/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0),
                      user_service: UserService = Depends(get_user_service),
                      credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                      ):
    user_service.verify_token(credentials=credentials)

    return {"message": f"I deleted book with id {book_id}"}


@router.post("/search", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[BookRequest])
async def search_book(
        search_filters: SearchRequest,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1),
        service: BookService = Depends(get_book_service),
        user_service: UserService = Depends(get_user_service),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    user_service.verify_token(credentials=credentials)

    return service.search_books(search_filters, page, page_size)
