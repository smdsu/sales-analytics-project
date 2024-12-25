from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field

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