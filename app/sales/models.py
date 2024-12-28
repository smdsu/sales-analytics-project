from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base, int_pk

from datetime import date

class Sale(Base):
    id: Mapped[int_pk]
    branch: Mapped[str]
    city: Mapped[str]
    customer_type: Mapped[str]
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=True)
    sale_date: Mapped[date]

    saledetails: Mapped[list["SaleDetails"]] = relationship("SaleDetails", back_populates="sale")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="sales")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id})")
    
    def __repr__(self):
        return str(self)