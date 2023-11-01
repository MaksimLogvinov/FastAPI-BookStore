from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.core import Book
from models.filters import BooksFilter


class BookService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_books_filter(self, book_filter: BooksFilter,
                               page: int, size: int) -> list[Book]:
        offset_min = page * size
        offset_max = (page + 1) * size
        query_filter = await book_filter.filter(select(Book))
        books = await self.session.execute(query_filter)
        return books.scalars().all()[offset_min:offset_max]
