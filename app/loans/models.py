from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, int_pk


class Loan(Base):


    id: Mapped[int_pk]

    # Связь с читателем
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    reader: Mapped["Reader"] = relationship("Reader", back_populates="loans")

    # Связь с книгой
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship("Book")

    # Дата выдачи и возврата
    issue_date: Mapped[date] = mapped_column(default=date.today)
    return_date: Mapped[date] = mapped_column(nullable=True)
