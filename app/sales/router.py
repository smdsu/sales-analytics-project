from fastapi import APIRouter, Depends, HTTPException
from app.sales.dao import SaleDAO
from app.sales.schemas import SSale, SSaleAdd, SSaleUpd
from app.sales.rb import RBSale
from app.users.dependencies import (
    is_current_user_admin,
    is_current_user_analyst,
    is_current_user_vendor,
)
from app.users.models import User

router = APIRouter(prefix="/sales", tags=["Работа с продажами"])


@router.get(
    "/",
    response_model=list[SSale],
    summary="Получить список всех продаж"
)
async def get_all_sales(
    request_body: RBSale = Depends(),
    user_data: User = Depends(is_current_user_analyst)
) -> list[SSale]:
    return await SaleDAO.find_all(**request_body.to_dict())


@router.get(
    "/{id}",
    response_model=SSale,
    summary="Получить данные продажи по ID"
)
async def get_sale_by_id(
    id: int,
    user_data: User = Depends(is_current_user_analyst)
) -> SSale | None:
    rez = await SaleDAO.find_one_or_none_by_id(id)
    if not rez:
        raise HTTPException(status_code=404, detail=f'Продукт с id={id} не найден')
    return rez


@router.post("/add/")
async def add_sale(
    sale: SSaleAdd,
    user_data: User = Depends(is_current_user_vendor)
) -> dict:
    check = await SaleDAO.add(**sale.dict())
    if check:
        return {"message": "Продажа успешно добавлена!", "sale": sale}
    else:
        return {"message": "Ошибка при добавлении продажи!"}


@router.put("/update_by_id/{id}")
async def update_sale_by_id(
    id: int,
    new_sale: SSaleUpd = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await SaleDAO.update(filter_by={'id': id}, **new_sale.to_new_data_dict())
    if check:
        return {
            "message": f"Продажа {id} успешно обновлён!",
            "rows": new_sale.to_new_data_dict()
        }
    else:
        return {"message": "Произошла ошибка при обновлении продажи!"}


@router.put("/update_by_filter/")
async def update_sale_by_filter(
    new_sale: SSaleUpd = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await SaleDAO.update(
        filter_by=new_sale.to_filter_dict(),
        **new_sale.to_new_data_dict()
    )
    if check:
        return {
            "message": "Продажи успешно обновлены!",
            "rows_updated": check,
            "data": new_sale.to_new_data_dict()
        }
    else:
        return {"message": "Ошибка при обновлении продажи!"}


@router.delete("/delete/{id}")
async def delete_sale_by_id(
    id: int,
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = SaleDAO.delete(id=id)
    if check:
        return {"message": f"Продажа с {id} удалён!"}
    else:
        return {"message": "Произошла ошибка при удалении продажи!"}
