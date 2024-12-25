from sqlalchemy import ForeignKey, text 
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base, int_pk
from app.products.models import Product
from app.sales.models import Sale

class SaleDetails(Base):
    sale_id: Mapped[int_pk] = mapped_column(ForeignKey("sales.id"), nullable=False)
    product_id: Mapped[int_pk] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(server_default=text('0'))
    sale: Mapped["Sale"] = relationship("Sale")
    product: Mapped["Product"] = relationship("Product")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.sale_id}, "
                f"product_id={self.product_id})")
    def __repr__(self):
        return str(self)