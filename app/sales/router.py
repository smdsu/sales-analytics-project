from fastapi import APIRouter, Depends, HTTPException
from app.sales.dao import SaleDAO
from app.sales.schemas import SSale
from app.sales.rb import RBSale

router = APIRouter(prefix="/sales", tags=["Работа с продажами"])

@router.get("/", response_model=list[SSale], summary="Получить список всех продаж")
async def get_all_sales(request_body: RBSale = Depends()) -> list[SSale]:
    return await SaleDAO.find_all(**request_body.to_dict())

@router.get("/{id}", response_model=SSale, summary="Получить данные продажи по ID")
async def get_sale_by_id(id: int) -> SSale | None:
    rez = await SaleDAO.find_one_or_none_by_id(id)
    if not rez:
        raise HTTPException(status_code=404, detail=f'Продукт с id={id} не найден')
    return rez