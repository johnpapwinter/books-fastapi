from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    year: int = Field(lt=2100)
    pages: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class SearchRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)


