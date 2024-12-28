from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SSaleDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sale_id: int = Field(..., description="ID продажи")
    product_id: int = Field(..., description="ID продукта")
    quantity: int = Field(..., description="Количество продукта")
    created_at: datetime = Field(..., description="Время создания записи в таблице")
    updated_at: datetime = Field(..., description="Время обноввления записи в таблице")

class SSaleDetailFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sale_id: int = Field(..., description="ID продажи")
    product_id: int = Field(..., description="ID продукта")
    unit_price: float = Field(..., description="Цена продукта")
    quantity: int = Field(..., description="Количество продукта")
    total_price: float = Field(..., description="Общая стоимость товаров")
    created_at: datetime = Field(..., description="Время создания записи в таблице")
    updated_at: datetime = Field(..., description="Время обноввления записи в таблице")

class SSaleDetailAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sale_id: int = Field(..., description="ID продажи")
    product_id: int = Field(..., description="ID продукта")
    quantity: int = Field(..., description="Количество продукта")

class SSaleDetailUpd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sale_id: Optional[int] = Field(None, description="ID продажи")
    product_id: Optional[int] = Field(None, description="ID продукта")
    quantity: Optional[int] = Field(None, description="Количество продукта")

    sale_id_new: Optional[int] = Field(None, description="Новый ID продажи")
    product_id_new: Optional[int] = Field(None, description="Новый ID продукта")
    quantity_new: Optional[int] = Field(None, description="Новое количество продукта")

    def to_filter_dict(self) -> dict:
        data = {
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data

    def to_new_data_dict(self) -> dict:
        data = {
            'sale_id': self.sale_id_new,
            'product_id': self.product_id_new,
            'quantity': self.quantity_new
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data