from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.database import Base, int_pk, str_uniq

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]

    # Связь многие-ко-многим (книги)
    books: Mapped[List["Book"]] = relationship(
        "Book", secondary="book_genre_association", back_populates="genres"
    )
