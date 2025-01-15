from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)
from fastapi.responses import StreamingResponse
from app.bulk.bulk import get_bulk_dict
from app.products.dao import ProductDAO
from app.products.schemas import SProduct, SProductAdd, SProductUpd
from app.products.rb import RBProduct, RBProductTime
from app.users.dependencies import is_current_user_admin, is_current_user_analyst
from app.users.models import User

router = APIRouter(prefix="/products", tags=["Работа с продуктами"])


@router.get(
    "/",
    response_model=list[SProduct],
    summary="Получить список всех продуктов"
)
async def get_all_products(
    request_body: RBProduct = Depends(),
    user_data: User = Depends(is_current_user_analyst)
) -> list[SProduct]:
    return await ProductDAO.find_all(**request_body.to_dict())


@router.get(
    "/{id}",
    response_model=SProduct,
    summary="Получить данные продукта по ID"
)
async def get_product_by_id(
    id: int,
    user_data: User = Depends(is_current_user_analyst)
) -> SProduct | None:
    rez = await ProductDAO.find_one_or_none_by_id(id)
    if not rez:
        raise HTTPException(status_code=404, detail=f'Продукт с id={id} не найден')
    return rez


@router.get(
    "/time_range/{param}",
    response_model=list[SProduct],
    summary=(
        "Получить детали продаж в заданном временном диапазоне."
        "Доступные параметры: created_at, updated_at"
    )
)
async def get_products_by_time_range(
    param: str,
    user_data: User = Depends(is_current_user_analyst),
    request_body: RBProductTime = Depends()
) -> list[SProduct]:
    return await ProductDAO.find_all_in_time_range(
        **request_body.to_dict(),
        param=param
    )


@router.post("/add/")
async def add_product(
    product: SProductAdd,
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await ProductDAO.add(**product.dict())
    if check:
        return {"message": "Продукт успешно добавлен!", "product": product}
    else:
        return {"message": "Ошибка при добавлении продукта!"}


@router.put("/update_by_id/{id}")
async def update_product_by_id(
    id: int,
    new_product: SProductUpd = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await ProductDAO.update(
        filter_by={'id': id},
        **new_product.to_new_data_dict()
    )
    if check:
        return {
            "message": f"Продукт {id} успешно обновлён!",
            "rows": new_product.to_new_data_dict()
        }
    else:
        return {"message": "Произошла ошибка при обновлении продукта!"}


@router.put("/update_by_filter/")
async def update_product_by_filter(
    new_product: SProductUpd = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await ProductDAO.update(
        filter_by=new_product.to_filter_dict(),
        **new_product.to_new_data_dict()
    )
    if check:
        return {
            "message": "Продукты успешно обновлены!",
            "rows_updated": check,
            "data": new_product.to_new_data_dict()
        }
    else:
        return {"message": "Ошибка при обновлении продукта!"}


@router.delete("/delete/{id}")
async def delete_product_by_id(
    id: int,
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await ProductDAO.delete(id=id)
    if check:
        return {"message": f"Продукт с {id} удалён!"}
    else:
        return {"message": "Произошла ошибка при удалении продукта!"}


@router.post("/bulk_insert/")
async def bulk_insert_products(
    user_data: User = Depends(is_current_user_admin),
    file: UploadFile = File(...)
):
    valid_records = await get_bulk_dict(file, SProductAdd)

    check = await ProductDAO.bulk_insert(valid_records)
    if check:
        return {"message": "Продукты успешно добавлены!"}
    else:
        return {"message": "Ошибка при добавлении продуктов!"}


@router.get("/get_csv/")
async def get_csv(
    request_body: RBProduct = Depends(),
    user_data: User = Depends(is_current_user_admin)
):
    return await ProductDAO.export_to_csv(**request_body.to_dict())


@router.get(
    "/download_csv/",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {"text/csv": {}},
            "description": "Return the CSV file."
        }
    }
)
async def download_csv(
    request_body: RBProduct = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> StreamingResponse:
    csv_data = await ProductDAO.export_to_csv(**request_body.to_dict())

    return StreamingResponse(
        iter([csv_data]), media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products.csv"}
    )
