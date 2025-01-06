from datetime import date


class RBCustomer:
    def __init__(
            self,
            id: int | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            date_of_birth: date | None = None,
            email: str | None = None,
            phone_number: str | None = None,
            gender: str | None = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone_number = phone_number
        self.gender = gender

    def to_dict(self) -> dict:
        date = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'email': self.email,
            'phone_number': self.phone_number,
            'gender': self.gender,
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date
