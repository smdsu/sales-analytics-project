from sqlalchemy.orm import Mapped, relationship

from app.database import Base, str_null_true, int_pk
    
class Product(Base):
    id: Mapped[int_pk]
    product_name: Mapped[str]
    product_description: Mapped[str_null_true]
    product_category: Mapped[str]
    unit_price: Mapped[float]

    saledetails: Mapped[list["SaleDetails"]] = relationship("SaleDetails", back_populates="product")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"