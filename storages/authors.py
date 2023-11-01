from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import AuthorsAdd
from models.core import Author
from models.database import engine
from storages import exceptions

session = AsyncSession(bind=engine, expire_on_commit=False)


async def get_authors(db: AsyncSession) -> list[Author]:
    authors = await db.execute(select(Author))
    return authors.scalars().all()


async def add_author(author: AuthorsAdd, db: AsyncSession) -> Author:
    author = Author(first_name=author.first_name, middle_name=author.middle_name,
                    last_name=author.last_name, birth_date=author.last_name,
                    phone=author.phone)
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


async def get_author(author_id: int) -> Author:
    author = await session.execute(select(Author).where(Author.id == author_id))
    author = author.scalars().first()
    return author


async def update_author(author_id: int, first_name: str,
                        middle_name: str, last_name: str, phone: str) -> Author:
    author = await get_author(author_id)
    if author:
        author.first_name = first_name
        author.middle_name = middle_name
        author.last_name = last_name
        author.phone = phone
        await session.commit()
    else:
        raise exceptions.NotFoundError(
            f'Автор под номером {author_id} не найден'
        )
    return author


async def delete_author(author_id: int) -> None:
    author = get_author(author_id)
    if author:
        await session.delete(author)
        await session.commit()
    else:
        raise exceptions.NotFoundError(
            f'Автор под номером {author_id} не найден'
        )
    return None
