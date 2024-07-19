from fastapi import APIRouter, Path, HTTPException
from starlette import status

from models import BookRequest, SearchRequest

router = APIRouter(prefix="/book")


@router.get("/get-all", status_code=status.HTTP_200_OK)
async def get_all():

    return {"message": "I return all books"}


@router.get("/get/{book_id}", status_code=status.HTTP_200_OK)
async def get_one(book_id: int = Path(gt=0)):

    return {"message": f"I return one book with id {book_id}"}


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):

    return {"message": f"I added new book with title {book_request.title}"}


@router.patch("/update", status_code=status.HTTP_200_OK)
async def update_book(book_request: BookRequest):
    if book_request.id is None:
        raise HTTPException(status_code=400, detail="Id should not be null")

    return {"message": f"I updated book with id {book_request.id}"}


@router.delete("/delete/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):

    return {"message": f"I deleted book with id {book_id}"}


@router.post("/search", status_code=status.HTTP_200_OK)
async def search_book(search_filters: SearchRequest):

    return {"message": f"I search book with title {search_filters.title} and author {search_filters.author}"}
