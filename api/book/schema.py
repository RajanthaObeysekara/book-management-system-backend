from typing import List
from pydantic import BaseModel, model_validator
from fastapi import Request

class Book(BaseModel):
    title:str
    author: str
    publication_date:str
    ISBN: str
    cover_image:str
    category: str


class BooksCreate(Book):
    pass

class BookResponse(Book):
    id:int
    class Config:
            from_attributes = True  # Similar to 'from_orm' in Pydantic v1
