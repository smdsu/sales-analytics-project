from datetime import date


class RBUser:
    def __init__(
            self,
            id: int | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            phone_number: str | None = None,
            email: str | None = None,
            is_user: bool | None = None,
            is_vendor: bool | None = None,
            is_analyst: bool | None = None,
            is_admin: bool | None = None,
            is_super_admin: bool | None = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.is_user = is_user
        self.is_vendor = is_vendor
        self.is_analyst = is_analyst
        self.is_admin = is_admin
        self.is_super_admin = is_super_admin

    def to_dict(self) -> dict:
        date_dict = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'is_user': self.is_user,
            'is_vendor': self.is_vendor,
            'is_analyst': self.is_analyst,
            'is_admin': self.is_admin,
            'is_super_admin': self.is_super_admin,
        }
        filttered_date = {
            key: value
            for key, value in date_dict.items()
            if value is not None
        }
        return filttered_date


class RBUserTime:
    def __init__(
            self,
            id: int | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
            phone_number: str | None = None,
            email: str | None = None,
            is_user: bool | None = None,
            is_vendor: bool | None = None,
            is_analyst: bool | None = None,
            is_admin: bool | None = None,
            is_super_admin: bool | None = None,
            start_time: date | None = None,
            end_time: date | None = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.is_user = is_user
        self.is_vendor = is_vendor
        self.is_analyst = is_analyst
        self.is_admin = is_admin
        self.is_super_admin = is_super_admin
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> dict:
        date_dict = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'is_user': self.is_user,
            'is_vendor': self.is_vendor,
            'is_analyst': self.is_analyst,
            'is_admin': self.is_admin,
            'is_super_admin': self.is_super_admin,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        filttered_date = {
            key: value
            for key, value in date_dict.items()
            if value is not None
        }
        return filttered_date
