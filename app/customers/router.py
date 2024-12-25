from fastapi import APIRouter, Depends, HTTPException
from app.customers.dao import CustomerDAO
from app.customers.schemas import SCustomer
from app.customers.rb import RBCustomer

router = APIRouter(prefix="/customers", tags=["Работа с клиентской базой"])

@router.get("/", response_model=list[SCustomer], summary="Получить список всех клиентов")
async def get_all_customers(request_body: RBCustomer = Depends()) -> list[SCustomer]:
    return await CustomerDAO.find_all(**request_body.to_dict())

@router.get("/{id}", response_model=SCustomer, summary="Получить данные клиента по ID")
async def get_customer_by_id(id: int) -> SCustomer | None:
    rez = await CustomerDAO.find_one_or_none_by_id(id)
    if not rez:
        raise HTTPException(status_code=404, detail=f'Клиент с id={id} не найден')
    return rez