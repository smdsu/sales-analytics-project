from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class SProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_name: str = Field(..., description="Название продукта")
    product_description: str = Field(..., description="Описание продукта")
    product_category: str = Field(..., description="Категория продукта")
    unit_price: float = Field(..., description="Цена продукта")
    created_at: datetime = Field(..., description="Время создания записи в таблице")
    updated_at: datetime = Field(..., description="Время обноввления записи в таблице")