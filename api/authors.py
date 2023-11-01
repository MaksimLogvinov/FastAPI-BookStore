from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ShowAuthors, AuthorsAdd
from models.core import Author
from models.database import get_db
from storages.authors import get_authors, add_author, update_author, \
    delete_author

router = APIRouter()


@router.get('/', response_model=list[ShowAuthors])
async def show_books(db: AsyncSession = Depends(get_db)) -> list[Author]:
    results = await get_authors(db)
    return results


@router.post('/', response_model=AuthorsAdd)
async def authors_add(author: AuthorsAdd, db: AsyncSession = Depends(get_db)) -> Author:
    return await add_author(author, db)


@router.put('/{author_id}', response_model=ShowAuthors)
async def author_update(author_id: int, first_name: str,
                        middle_name: str, last_name: str, phone: str) -> Author:
    return await update_author(author_id, first_name,
                               middle_name, last_name, phone)


@router.delete('/{author_id}')
async def author_delete(book_id: int) -> None:
    return await delete_author(book_id)
