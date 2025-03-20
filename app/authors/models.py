from typing import List

from sqlalchemy.orm import Mapped, relationship
from datetime import date
from app.database import Base, int_pk, str_uniq, str_null_true


class Author(Base):

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    biography: Mapped[str_null_true]
    birth_date: Mapped[date]

    # Связь один-ко-многим (книги)
    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")