class RBProduct:
    def __init__(
            self,
            id: int | None = None,
            product_name: str | None = None,
            product_category: str | None = None,
            unit_price: float | None = None,
    ):
        self.id = id
        self.product_name = product_name
        self.product_category = product_category
        self.unit_price = unit_price

    def to_dict(self) -> dict:
        date = {
            'id': self.id,
            'product_name': self.product_name,
            'product_category': self.product_category,
            'unit_price': self.unit_price,
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date
