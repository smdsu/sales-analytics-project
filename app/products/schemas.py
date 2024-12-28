from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_name: str = Field(..., description="Название продукта")
    product_description: str = Field(..., description="Описание продукта")
    product_category: str = Field(..., description="Категория продукта")
    unit_price: float = Field(..., description="Цена продукта")
    created_at: datetime = Field(..., description="Время создания записи в таблице")
    updated_at: datetime = Field(..., description="Время обноввления записи в таблице")

class SProductAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_name: str = Field(..., description="Название продукта")
    product_description: str = Field(..., description="Описание продукта")
    product_category: str = Field(..., description="Категория продукта")
    unit_price: float = Field(..., description="Цена продукта")

class SProductUpd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = Field(None, description="ID продукта")
    product_name: Optional[str] = Field(None, description="Название продукта")
    product_description: Optional[str] = Field(None, description="Описание продукта")
    product_category: Optional[str] = Field(None, description="Категория продукта")
    unit_price: Optional[float] = Field(None, description="Цена продукта")

    product_name_new: Optional[str] = Field(None, description="Название продукта")
    product_description_new: Optional[str] = Field(None, description="Описание продукта")
    product_category_new: Optional[str] = Field(None, description="Категория продукта")
    unit_price_new: Optional[float] = Field(None, description="Цена продукта")

    def to_filter_dict(self) -> dict:
        data = {
            'id': self.id,
            'product_name': self.product_name,
            'product_description': self.product_description,
            'product_category': self.product_category,
            'unit_price': self.unit_price
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
    
    def to_new_data_dict(self) -> dict:
        data = {
            'product_name': self.product_name_new,
            'product_description': self.product_description_new,
            'product_category': self.product_category_new,
            'unit_price': self.unit_price_new
        }
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data