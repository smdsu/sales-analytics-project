from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.customers.models import Customer
from app.database import Base, int_pk

from datetime import date

class Sale(Base):
    id: Mapped[int_pk]
    branch: Mapped[str]
    city: Mapped[str]
    customer_type: Mapped[str]
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=True)
    sale_date: Mapped[date]

    customer: Mapped["Customer"] = relationship("Customer")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id})")
    
    def __repr__(self):
        return str(self)