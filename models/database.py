import os

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, \
    async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, \
    Mapped, mapped_column

meta = MetaData()

SQLALCHEMY_DATABASE_URL = os.getenv('FASTAPI_DB_URL')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    except:
        await db.rollback()
    finally:
        await db.close()
