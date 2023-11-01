from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import BooksAdd
from models.core import Book
from models.database import engine
from storages import exceptions

session = AsyncSession(bind=engine, expire_on_commit=False)


async def get_books(db: AsyncSession) -> list[Book]:
    books = await db.execute(select(Book))
    return books.scalars().all()


async def add_book(book: BooksAdd, db: AsyncSession) -> Book:
    book = Book(title=book.title, author_id=book.author_id, year=book.year,
                count_pages=book.count_pages, date_created=book.date_created,
                price=book.price)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def get_book(book_id: int) -> Book:
    book = await session.execute(select(Book).where(Book.id == book_id))
    book = book.scalars().first()
    return book


async def update_book(book_id: int, title: str, price: float) -> Book:
    book = await get_book(book_id)
    if book:
        book.title = title
        book.price = price
        await session.commit()
    else:
        raise exceptions.NotFoundError(
            f'Книга с номером {book_id} не найдена'
        )
    return book


async def delete_book(book_id: int) -> None:
    book = get_book(book_id)
    if book:
        await session.delete(book)
        await session.commit()
    else:
        raise exceptions.NotFoundError(
            f'Книга с номером {book_id} не найдена'
        )
    return None
