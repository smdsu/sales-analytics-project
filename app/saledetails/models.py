from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base, int_pk
from app.products.models import Product
from app.sales.models import Sale


class SaleDetails(Base):
    sale_id: Mapped[int_pk] = mapped_column(
        ForeignKey("sales.id"),
        nullable=False
    )
    product_id: Mapped[int_pk] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(server_default=text('0'))

    sale: Mapped["Sale"] = relationship("Sale", back_populates="saledetails")
    product: Mapped["Product"] = relationship("Product", back_populates="saledetails")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.sale_id}:{self.product_id})"

    def to_dict(self) -> dict:
        date = {
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date
