from fastapi import APIRouter, Path, HTTPException, Depends
from starlette import status

from models import BookRequest, SearchRequest
from service import BookService, get_book_service

router = APIRouter(prefix="/book")


@router.get("/get-all", status_code=status.HTTP_200_OK, response_model=list[BookRequest])
async def get_all(service: BookService = Depends(get_book_service)):

    return service.get_all_books()


@router.get("/get/{book_id}", status_code=status.HTTP_200_OK, response_model=BookRequest)
async def get_one(service: BookService = Depends(get_book_service), book_id: int = Path(gt=0)):

    return service.get_book(book_id)


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=BookRequest)
async def create_book(book_request: BookRequest, service: BookService = Depends(get_book_service)):

    return service.create_new_book(book_request)


@router.patch("/update", status_code=status.HTTP_200_OK, response_model=BookRequest)
async def update_book(book_request: BookRequest, service: BookService = Depends(get_book_service)):
    if book_request.id is None:
        raise HTTPException(status_code=400, detail="Id should not be null")

    return service.update_book(book_request.id, book_request)


@router.delete("/delete/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):

    return {"message": f"I deleted book with id {book_id}"}


@router.post("/search", status_code=status.HTTP_200_OK)
async def search_book(search_filters: SearchRequest):

    return {"message": f"I search book with title {search_filters.title} and author {search_filters.author}"}
