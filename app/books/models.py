from datetime import date
from typing import List

from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, str_uniq, int_pk, str_null_true

book_genre_association = Table(
    "book_genre_association",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    title: Mapped[str_uniq]
    description: Mapped[str_null_true]
    publication_date: Mapped[date]

    # Связь многие-к-одному (автор)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship("Author", back_populates="books")

    # Связь многие-ко-многим (жанры)
    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary=book_genre_association, back_populates="books"
    )

    # Доступные экземпляры книги
    available_copies: Mapped[int] = mapped_column(default=1)
