from fastapi import APIRouter, Depends, HTTPException
from app.saledetails.dao import SaleDetailsDAO
from app.saledetails.rb import RBSaleDetail
from app.saledetails.schemas import SSaleDetail

router = APIRouter(prefix="/saledetails", tags=["Работа с SaleDetails"])

@router.get("/", response_model=list[SSaleDetail], description="Получить список всех SaleDetails")
async def get_all_saledetails(request_body: RBSaleDetail = Depends()) -> list[SSaleDetail]:
    return await SaleDetailsDAO.find_all(**request_body.to_dict())