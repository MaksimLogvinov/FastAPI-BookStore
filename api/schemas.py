from datetime import datetime, date

from pydantic import BaseModel, Field


class ShowBooks(BaseModel):
    id: int
    title: str
    author_id: int
    price: float
    year: int
    count_pages: int
    date_created: datetime


class BooksAdd(BaseModel):
    title: str
    author_id: int
    price: float = Field(gte=0)
    year: int = Field(gte=1, lte=9999)
    count_pages: int = Field(gt=2)
    date_created: datetime = Field(lte=datetime.now())


class ShowAuthors(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    birth_date: date
    phone: str


class AuthorsAdd(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    birth_date: date
    phone: str = Field(max_length=20)
