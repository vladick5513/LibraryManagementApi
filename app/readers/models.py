from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database import Base, int_pk, str_uniq

class Reader(Base):

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    email: Mapped[str_uniq]
    joined_date: Mapped[date] = mapped_column(default=date.today)

    # Связь один-ко-многим (выдачи книг)
    loans: Mapped[List["Loan"]] = relationship("Loan", back_populates="reader")