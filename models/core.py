from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from models.database import Base


class Author(Base):
    __tablename__ = 'authors'

    first_name: Mapped[str]
    middle_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[int]
    phone: Mapped[str] = mapped_column(unique=True)


class Book(Base):
    __tablename__ = 'books'

    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    price: Mapped[float]
    year: Mapped[int]
    count_pages: Mapped[int]
    date_created: Mapped[datetime]


class Storage(Base):
    __tablename__ = 'storages'

    title: Mapped[str]
    country: Mapped[str]
    city: Mapped[str]
    postal_code: Mapped[str]


class StorageBook(Base):
    __tablename__ = 'storage_book'

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    storage_id: Mapped[int] = mapped_column(ForeignKey('storages.id'))
    quantity_on_stock: Mapped[int] = mapped_column(default=0)
