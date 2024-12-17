from sqlalchemy import ForeignKey, text 
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base, str_uniq, str_null_true, int_pk

from datetime import date

class Sale(Base):
    sale_id: Mapped[int_pk]
    branch: Mapped[str]
    city: Mapped[str]
    customer_type: Mapped[str]
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.customer_id'), nullable=True)
    gender: Mapped[str]
    sale_date: Mapped[date]

    customer: Mapped["Customer"] = relationship("Customer")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.sale_id})")
    
    def __repr__(self):
        return str(self)
    
class Product(Base):
    product_id: Mapped[int_pk]
    product_name: Mapped[str_uniq]
    product_description: Mapped[str_null_true]
    product_category: Mapped[str]
    unit_price: Mapped[float]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.product_id}, "
                f"product_name={self.product_name!r})")
    def __repr__(self):
        return str(self)

class SaleDetails(Base):
    sale_id: Mapped[int_pk] = mapped_column(ForeignKey("sales.sale_id"), nullable=False)
    product_id: Mapped[int_pk] = mapped_column(ForeignKey("products.product_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(server_default=text('0'))

    sale: Mapped["Sale"] = relationship("Sale")
    product: Mapped["Product"] = relationship("Product")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.sale_id}, "
                f"product_id={self.product_id})")
    def __repr__(self):
        return str(self)


class Customer(Base):
    customer_id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    email: Mapped[str_uniq]
    phone_number: Mapped[str_uniq]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.customer_id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")

    def __repr__(self):
        return str(self)

