from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas import ShowBooks, BooksAdd
from models.core import Book
from models.database import get_db, engine
from models.filters import BooksFilter
from models.services import BookService
from storages.books import get_books, add_book, update_book, delete_book

router = APIRouter()


@router.get('/', response_model=list[ShowBooks])
async def show_books(db: AsyncSession = Depends(get_db)) -> list[Book]:
    return await get_books(db)


@router.get('/search', response_model=list[ShowBooks])
async def filter_books(
        book_filter: BooksFilter = FilterDepends(BooksFilter),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100)) -> list[Book]:
    session = AsyncSession(bind=engine)
    service = BookService(session=session)
    return await service.get_books_filter(book_filter, page, size)


@router.post('/', response_model=BooksAdd)
async def book_add(book: BooksAdd, db: AsyncSession = Depends(get_db)) -> Book:
    return await add_book(book, db)


@router.put('/{book_id}', response_model=ShowBooks)
async def book_update(book_id: int, title: str, price: float) -> Book:
    return await update_book(book_id, title, price)


@router.delete('/{book_id}')
async def book_delete(book_id: int) -> None:
    return await delete_book(book_id)
