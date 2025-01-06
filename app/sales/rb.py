from datetime import date


class RBSale:
    def __init__(
            self,
            id: int | None = None,
            branch: str | None = None,
            city: str | None = None,
            customer_type: str | None = None,
            customer_id: int | None = None,
            sale_date: date | None = None,
            total_amount: float | None = None,
    ):
        self.id = id
        self.branch = branch
        self.city = city
        self.customer_type = customer_type
        self.customer_id = customer_id
        self.sale_date = sale_date
        self.total_amount = total_amount

    def to_dict(self) -> dict:
        date = {
            'id': self.id,
            'branch': self.branch,
            'city': self.city,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'sale_date': self.sale_date,
            'total_amount': self.total_amount,
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date
