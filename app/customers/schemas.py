from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

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