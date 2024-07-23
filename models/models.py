from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')


class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    year: int = Field(lt=2100)
    pages: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class SearchRequest(BaseModel):
    title: Optional[str] = Field(default=None)
    author: Optional[str] = Field(default=None)


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    current_page: int
    total_pages: int
    total_items: int


class UserRequest(BaseModel):
    id: Optional[int] = Field(default=None)
    username: str = Field(min_length=3)
    email: str = Field(min_length=3)
    password: str = Field(min_length=3)
    role: str = Field(min_length=3)

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)


class LoginResponse(BaseModel):
    access_token: str = Field(min_length=3)
    token_type: str = Field(min_length=3)
    username: str = Field(min_length=3)

