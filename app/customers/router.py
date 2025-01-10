from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)
from app.bulk.bulk import get_bulk_dict

from app.customers.dao import CustomerDAO
from app.customers.schemas import SCustomer, SCustomerAdd, SCustomerUpd
from app.customers.rb import RBCustomer, RBCustomerTime
from app.users.dependencies import (
    is_current_user_admin,
    is_current_user_vendor,
    is_current_user_analyst,
)
from app.users.models import User

router = APIRouter(
    prefix="/customers",
    tags=["Работа с клиентской базой"]
)


@router.get(
    "/",
    response_model=list[SCustomer],
    summary="Получить список всех клиентов"
)
async def get_all_customers(
    user_data: User = Depends(is_current_user_analyst),
    request_body: RBCustomer = Depends()
) -> list[SCustomer]:
    return await CustomerDAO.find_all(**request_body.to_dict())


@router.get(
    "/{id}",
    response_model=SCustomer,
    summary="Получить данные клиента по ID"
)
async def get_customer_by_id(
    id: int,
    user_data: User = Depends(is_current_user_analyst)
) -> SCustomer | None:
    rez = await CustomerDAO.find_one_or_none_by_id(id)
    if not rez:
        raise HTTPException(status_code=404, detail=f'Клиент с id={id} не найден')
    return rez


@router.get(
    "/time_range/{param}",
    response_model=list[SCustomer],
    summary=(
        "Получить детали продаж в заданном временном диапазоне."
        "Доступные параметры: date_of_birth, created_at, updated_at"
    )
)
async def get_customers_by_time_range(
    param: str,
    user_data: User = Depends(is_current_user_analyst),
    request_body: RBCustomerTime = Depends()
) -> list[SCustomer]:
    return await CustomerDAO.find_all_in_time_range(
        **request_body.to_dict(),
        param=param
    )


@router.post("/add/")
async def add_customer(
    customer: SCustomerAdd,
    user_data: User = Depends(is_current_user_vendor)
) -> dict:
    check = await CustomerDAO.add(**customer.dict())
    if check:
        return {"message": "Покупатель успешно добавлен!", "customer": customer}
    else:
        return {"message": "Ошибка при добавлении покупателя!"}


@router.put("/update_by_id/{id}")
async def upd_customer_by_id(
    id: int,
    new_customer: SCustomerUpd = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await CustomerDAO.update(
        filter_by={"id": id},
        **new_customer.to_new_data_dict()
    )
    if check:
        return {
            "message": f"Покупатель {id} успешно обновлен!",
            "rows": new_customer.to_new_data_dict()
        }
    else:
        return {"message": "Ошибка при обновлении покупателя!"}


@router.put("/update_by_filter/")
async def upd_customer_by_filter(
    new_customer: SCustomerUpd = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await CustomerDAO.update(
        filter_by=new_customer.to_filter_dict(),
        **new_customer.to_new_data_dict()
    )
    if check:
        return {
            "message": "Покупатели успешно обновлены!",
            "rows_updated": check,
            "data": new_customer.to_new_data_dict()
        }
    else:
        return {"message": "Ошибка при обновлении покупателя!"}


@router.delete("/delete/{id}")
async def delete_customer_by_id(
    id: int,
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = CustomerDAO.delete(id=id)
    if check:
        return {"message": f"Покупатель с {id} удалён!"}
    else:
        return {"message": "Произошла ошибка при удалении покупателя!"}


@router.post("/bulk_insert/")
async def bulk_insert_products(
    user_data: User = Depends(is_current_user_admin),
    file: UploadFile = File(...)
):
    valid_records = await get_bulk_dict(file, SCustomerAdd)

    check = await CustomerDAO.bulk_insert(valid_records)
    if check:
        return {"message": "Покупатели успешно добавлены!"}
    else:
        return {"message": "Ошибка при добавлении покупателей!"}
