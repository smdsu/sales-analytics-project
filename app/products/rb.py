from datetime import date


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


class RBProductTime:
    def __init__(
            self,
            id: int | None = None,
            product_name: str | None = None,
            product_category: str | None = None,
            unit_price: float | None = None,
            start_time: date | None = None,
            end_time: date | None = None
    ):
        self.id = id
        self.product_name = product_name
        self.product_category = product_category
        self.unit_price = unit_price
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> dict:
        date = {
            'id': self.id,
            'product_name': self.product_name,
            'product_category': self.product_category,
            'unit_price': self.unit_price,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date
