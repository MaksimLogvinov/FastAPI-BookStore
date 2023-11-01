from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from models.core import Book


class BooksFilter(Filter):
    title__ilike: str = Field(alias="title")
    price__gte: float = Field(alias="price")

    class Constants(Filter.Constants):
        model = Book

    class Config:
        populate_by_name = True
