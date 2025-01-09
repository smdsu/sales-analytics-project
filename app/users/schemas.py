from datetime import datetime
from pydantic import Field, EmailStr, BaseModel
from typing import Optional
from pydantic import ConfigDict
from app.users.auth import get_password_hash


class SUserRegister(BaseModel):
    phone_number: str = Field(..., description="Номер телефона, начинающийся с +")
    email: EmailStr = Field(..., description="Электронная почта")
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Пароль от 5 до 50 знаков"
    )  # Сделать проверку пароля на стойкость


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Пароль от 5 до 50 знаков"
    )


class SUserData(BaseModel):
    id: int = Field(..., description="ID пользователя")
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")

    phone_number: str = Field(..., description="Номер телефона, начинающийся с +")
    email: EmailStr = Field(..., description="Электронная почта")


class SUserFullData(BaseModel):
    id: int = Field(..., description="ID пользователя")
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")

    phone_number: str = Field(..., description="Номер телефона, начинающийся с +")
    email: EmailStr = Field(..., description="Электронная почта")

    password: str = Field(..., description="Хэш пароля")

    is_user: bool
    is_vendor: bool
    is_analyst: bool
    is_admin: bool
    is_super_admin: bool

    created_at: datetime
    updated_at: datetime


class SUserUpd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = Field(None, description="ID пользователя")
    first_name: Optional[str] = Field(None, description="Имя")
    last_name: Optional[str] = Field(None, description="Фамилия")
    phone_number: Optional[str] = Field(
        None,
        description="Номер телефона, начинающийся с +"
    )
    email: Optional[EmailStr] = Field(None, description="Электронная почта")
    # password: str = Field(..., description="Хэш пароля")

    is_user: Optional[bool] = Field(None)
    is_vendor: Optional[bool] = Field(None)
    is_analyst: Optional[bool] = Field(None)
    is_admin: Optional[bool] = Field(None)
    is_super_admin: Optional[bool] = Field(None)

    id_new: Optional[int] = Field(None, description="ID пользователя")
    first_name_new: Optional[str] = Field(None, description="Имя")
    last_name_new: Optional[str] = Field(None, description="Фамилия")
    phone_number_new: Optional[str] = Field(
        None,
        description="Номер телефона, начинающийся с +"
    )
    email_new: Optional[EmailStr] = Field(None, description="Электронная почта")
    password_new: Optional[str] = Field(None, description="Пароль")

    is_user_new: Optional[bool] = Field(None)
    is_vendor_new: Optional[bool] = Field(None)
    is_analyst_new: Optional[bool] = Field(None)
    is_admin_new: Optional[bool] = Field(None)
    is_super_admin_new: Optional[bool] = Field(None)

    def to_filter_dict(self) -> dict:
        date = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'is_user': self.is_user,
            'is_vendor': self.is_vendor,
            'is_analyst': self.is_analyst,
            'is_admin': self.is_admin,
            'is_super_admin': self.is_super_admin
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date

    def to_new_data_dict(self) -> dict:
        password = None
        if self.password_new is not None:
            password = get_password_hash(self.password_new)
        date = {
            'id': self.id_new,
            'first_name': self.first_name_new,
            'last_name': self.last_name_new,
            'phone_number': self.phone_number_new,
            'email': self.email_new,
            'password': password,
            'is_user': self.is_user_new,
            'is_vendor': self.is_vendor_new,
            'is_analyst': self.is_analyst_new,
            'is_admin': self.is_admin_new,
            'is_super_admin': self.is_super_admin_new
        }
        filttered_date = {
            key: value
            for key, value in date.items()
            if value is not None
        }
        return filttered_date
