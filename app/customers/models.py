from sqlalchemy.orm import Mapped, relationship
from app.database import Base, str_uniq, int_pk

from datetime import date

class Customer(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    phone_number: Mapped[str_uniq]
    gender: Mapped[str]

    sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="customer")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"