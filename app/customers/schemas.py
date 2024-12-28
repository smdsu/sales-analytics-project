from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from typing import Optional

class SCustomer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str = Field(..., description="Имя клиента")
    last_name: str = Field(..., description="Фамилия клиента")
    date_of_birth: date = Field(..., description="Дата рождения клиента в формате ГГГГ-ММ-ДД")
    email: EmailStr = Field(..., description="Электронная почта клиента")
    phone_number: str = Field(..., description="Номер телефона клиента")
    gender: str = Field(..., description="Пол")
    created_at: datetime = Field(..., description="Время создания записи в таблице")
    updated_at: datetime = Field(..., description="Время обноввления записи в таблице")

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value

class SCustomerAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str = Field(..., description="Имя клиента")
    last_name: str = Field(..., description="Фамилия клиента")
    date_of_birth: date = Field(..., description="Дата рождения клиента в формате ГГГГ-ММ-ДД")
    email: EmailStr = Field(..., description="Электронная почта клиента")
    phone_number: str = Field(..., description="Номер телефона клиента")
    gender: str = Field(..., description="Пол")

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value

class SCustomerUpd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = Field(None, description="ID клиента")
    first_name: Optional[str] = Field(None, description="Имя клиента")
    last_name: Optional[str] = Field(None, description="Фамилия клиента")
    date_of_birth: Optional[date] = Field(None, description="Дата рождения клиента в формате ГГГГ-ММ-ДД")
    email: Optional[EmailStr] = Field(None, description="Электронная почта клиента")
    phone_number: Optional[str] = Field(None, description="Номер телефона клиента")
    gender: Optional[str] = Field(None, description="Пол")

    first_name_new: Optional[str] = Field(None, description="Новое емя клиента")
    last_name_new: Optional[str] = Field(None, description="Новая фамилия клиента")
    date_of_birth_new: Optional[date] = Field(None, description="Новая дата рождения клиента в формате ГГГГ-ММ-ДД")
    email_new: Optional[EmailStr] = Field(None, description="Новая электронная почта клиента")
    phone_number_new: Optional[str] = Field(None, description="Новый номер телефона клиента")
    gender_new: Optional[str] = Field(None, description="Новый пол")

    @field_validator("date_of_birth", "date_of_birth_new")
    def validate_date_of_birth(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value
    
    def to_filter_dict(self) -> dict:
        date =  {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'email': self.email,
            'phone_number': self.phone_number,
            'gender': self.gender,
        }
        filttered_date = {key: value for key, value in date.items() if value is not None}
        return filttered_date
    
    def to_new_data_dict(self) -> dict:
        date =  {
            'first_name': self.first_name_new,
            'last_name': self.last_name_new,
            'date_of_birth': self.date_of_birth_new,
            'email': self.email_new,
            'phone_number': self.phone_number_new,
            'gender': self.gender_new,
        }
        filttered_date = {key: value for key, value in date.items() if value is not None}
        return filttered_date