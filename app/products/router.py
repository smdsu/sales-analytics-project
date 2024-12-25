from fastapi import APIRouter, Depends, HTTPException
from app.products.dao import ProductDAO
from app.products.schemas import SProduct
from app.products.rb import RBProduct

router = APIRouter(prefix="/products", tags=["Работа с продуктами"])

@router.get("/", response_model=list[SProduct], summary="Получить список всех продуктов")
async def get_all_products(request_body: RBProduct = Depends()) -> list[SProduct]:
    return await ProductDAO.find_all(**request_body.to_dict())

@router.get("/{id}", response_model=SProduct, summary="Получить данные продукта по ID")
async def get_product_by_id(id: int) -> SProduct | None:
    rez = await ProductDAO.find_one_or_none_by_id(id)
    if not rez:
        raise HTTPException(status_code=404, detail=f'Продукт с id={id} не найден')
    return rez