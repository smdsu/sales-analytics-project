class RBSaleDetail:
    def __init__(
            self,
            sale_id: int | None = None,
            product_id: str | None = None,
            quantity: int | None = None,
    ):
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity = quantity

    def to_dict(self) -> dict:
        date = {
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date
