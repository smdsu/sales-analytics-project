from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
)
from fastapi.responses import StreamingResponse
from app.saledetails.dao import SaleDetailsDAO
from app.saledetails.rb import RBSaleDetail, RBSaleDetailTime
from app.saledetails.schemas import (
    SSaleDetail,
    SSaleDetailFull,
    SSaleDetailAdd,
    SSaleDetailUpd,
)
from app.users.dependencies import (
    is_current_user_admin,
    is_current_user_analyst,
    is_current_user_vendor,
)
from app.users.models import User
from app.bulk.bulk import get_bulk_dict

router = APIRouter(prefix="/saledetails", tags=["Работа с SaleDetails"])


@router.get(
    "/",
    response_model=list[SSaleDetail],
    description="Получить список всех SaleDetails",
)
async def get_all_saledetails(
    request_body: RBSaleDetail = Depends(),
    user_data: User = Depends(is_current_user_analyst)
) -> list[SSaleDetail]:
    return await SaleDetailsDAO.find_all(**request_body.to_dict())


@router.get(
    "/full_bill/{sale_id}",
    response_model=list[SSaleDetailFull],
    description="Получить детали одной продажи"
)
async def get_full_by_sale_id(
    sale_id: int,
    user_data: User = Depends(is_current_user_analyst)
) -> list[SSaleDetail] | None:
    result = await SaleDetailsDAO.find_with_price_one_or_none_by_id(sale_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'Детали по продаже с id={sale_id} не найдены'
        )
    return result


@router.get(
    "/time_range/{param}",
    response_model=list[SSaleDetail],
    summary=(
        "Получить детали продаж в заданном временном диапазоне."
        "Доступные параметры: created_at, updated_at"
    )
)
async def get_saledetails_by_time_range(
    param: str,
    user_data: User = Depends(is_current_user_analyst),
    request_body: RBSaleDetailTime = Depends()
) -> list[SSaleDetail]:
    return await SaleDetailsDAO.find_all_in_time_range(
        **request_body.to_dict(),
        param=param
    )


@router.get(
    "/full_bill/time_range/{param}",
    response_model=list[SSaleDetailFull],
    summary=(
        "Получить детали продаж в заданном временном диапазоне."
        "Доступные параметры: created_at, updated_at"
    )
)
async def get_full_saledetails_by_time_range(
    param: str,
    user_data: User = Depends(is_current_user_analyst),
    request_body: RBSaleDetailTime = Depends()
) -> list[SSaleDetailFull]:
    return await SaleDetailsDAO.find_all_in_time_range(
        **request_body.to_dict(),
        param=param
    )


@router.post("/add/")
async def add_saledetail(
    saledetail: SSaleDetailAdd,
    user_data: User = Depends(is_current_user_vendor)
) -> dict:
    check = await SaleDetailsDAO.add(**saledetail.dict())
    if check:
        return {
            "message": "Детали продажи успешно добавлены!",
            "saledetail": saledetail
        }
    else:
        return {"message": "Ошибка при добавлении деталей продажи!"}


@router.put("/update/")
async def update_saledetail(
    saledetail: SSaleDetailUpd,
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await SaleDetailsDAO.update(
        filter_by=saledetail.to_filter_dict(),
        **saledetail.to_new_data_dict()
    )
    if check:
        return {
            "message": "Детали продажи успешно обновлены!",
            "rows_updated": check,
            "data": saledetail.to_new_data_dict()
        }
    else:
        return {"message": "Ошибка при обновлении деталей продажи!"}


@router.delete("/delete/{id}")
async def delete_saledetail_by_id(
    id: int,
    user_data: User = Depends(is_current_user_admin)
) -> dict:
    check = await SaleDetailsDAO.delete(sale_id=id)
    if check:
        return {"message": f"Детали продажи с {id} удалены!"}
    else:
        return {"message": "Произошла ошибка при удалении деталей продажи!"}


@router.post("/bulk_insert/")
async def bulk_insert_saledetails(
    user_data: User = Depends(is_current_user_admin),
    file: UploadFile = File(...)
):
    valid_records = await get_bulk_dict(file, SSaleDetailAdd)

    check = await SaleDetailsDAO.bulk_insert(valid_records)
    if check:
        return {"message": "Детали продажи успешно добавлены!"}
    else:
        return {"message": "Ошибка при добавлении деталей продажи!"}


@router.get("/get_csv/")
async def get_csv(
    request_body: RBSaleDetail = Depends(),
    user_data: User = Depends(is_current_user_admin)
):
    return await SaleDetailsDAO.export_to_csv(**request_body.to_dict())


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
    request_body: RBSaleDetail = Depends(),
    user_data: User = Depends(is_current_user_admin)
) -> StreamingResponse:
    csv_data = await SaleDetailsDAO.export_to_csv(**request_body.to_dict())

    return StreamingResponse(
        iter([csv_data]), media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sales_details.csv"}
    )
