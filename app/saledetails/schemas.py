from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class SSaleDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sale_id: int = Field(..., description="ID продажи")
    product_id: int = Field(..., description="ID продукта")
    quantity: int = Field(..., description="Количество продукта")
    created_at: datetime = Field(..., description="Время создания записи в таблице")
    updated_at: datetime = Field(..., description="Время обноввления записи в таблице")