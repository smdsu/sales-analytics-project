from sqlalchemy.orm import Mapped

from app.database import Base, str_null_true, int_pk
    
class Product(Base):
    id: Mapped[int_pk]
    product_name: Mapped[str]
    product_description: Mapped[str_null_true]
    product_category: Mapped[str]
    unit_price: Mapped[float]

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"product_name={self.product_name!r})")
    def __repr__(self):
        return str(self)