from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SSale(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    branch: str = Field(..., description="Название филиала")
    city: str = Field(..., description="Город")
    customer_type: str = Field(..., description="Тип клиента")
    customer_id: float = Field(..., description="ID клиента")
    sale_date: date = Field(..., description="Дата продажи")
    created_at: datetime = Field(..., description="Время создания записи в таблице")
    updated_at: datetime = Field(..., description="Время обноввления записи в таблице")

class SSaleAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    branch: str = Field(..., description="Название филиала")
    city: str = Field(..., description="Город")
    customer_type: str = Field(..., description="Тип клиента")
    customer_id: float = Field(..., description="ID клиента")
    sale_date: date = Field(..., description="Дата продажи")

class SSaleUpd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = Field(None, description="ID продажи")
    branch: Optional[str] = Field(None, description="Название филиала")
    city: Optional[str] = Field(None, description="Город")
    customer_type: Optional[str] = Field(None, description="Тип клиента")
    customer_id: Optional[float] = Field(None, description="ID клиента")
    sale_date: Optional[date] = Field(None, description="Дата продажи")

    branch_new: Optional[str] = Field(None, description="Новое название филиала")
    city_new: Optional[str] = Field(None, description="Новый город")
    customer_type_new: Optional[str] = Field(None, description="Новый тип клиента")
    customer_id_new: Optional[float] = Field(None, description="Новый ID клиента")
    sale_date_new: Optional[date] = Field(None, description="Новая дата продажи")

    def to_filter_dict(self):
        data = {
            'id': self.id,
            'branch': self.branch,
            'city': self.city,
            'customer_type': self.customer_type,
            'customer_id': self.customer_id,
            'sale_date': self.sale_date
        }
        fultered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
    
    def to_new_data_dict(self):
        data = {
            'branch': self.branch_new,
            'city': self.city_new,
            'customer_type': self.customer_type_new,
            'customer_id': self.customer_id_new,
            'sale_date': self.sale_date_new
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data