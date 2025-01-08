from app.database import async_session_maker
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from app.sales.models import Sale
from app.saledetails.models import SaleDetails
from app.dao.base import BaseDAO


class SaleDAO(BaseDAO):
    model = Sale

    @classmethod
    async def find_all_with_total(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(Sale).filter_by(**filter_by).options(
                joinedload(Sale.saledetails).joinedload(SaleDetails.product)

            )
            result = await session.execute(query)
            sales = result.unique().scalars().all()

            if not sales:
                return None

            sales_data = []
            for sale in sales:
                total_amount = sum(
                    sd.product.unit_price * sd.quantity
                    for sd in sale.saledetails
                )
                sales_data.append({
                    "sale_id": sale.id,
                    "branch": sale.branch,
                    "city": sale.city,
                    "customer_type": sale.customer_type,
                    "customer_id": sale.customer_id,
                    "sale_date": sale.sale_date,
                    "total_amount": (
                        round(total_amount, 2)
                        if total_amount is not None
                        else total_amount
                    ),
                    "created_at": sale.created_at,
                    "updated_at": sale.updated_at
                })

            return sales_data

    @classmethod
    async def find_one_or_none_with_total(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(Sale).filter_by(id=data_id).options(
                joinedload(Sale.saledetails).joinedload(SaleDetails.product)

            )
            result = await session.execute(query)
            sale = result.unique().scalar_one_or_none()

            if not sale:
                return None

            total_amount = sum(
                sd.product.unit_price * sd.quantity
                for sd in sale.saledetails
            )

            sales_data = {
                "sale_id": sale.id,
                "branch": sale.branch,
                "city": sale.city,
                "customer_type": sale.customer_type,
                "customer_id": sale.customer_id,
                "sale_date": sale.sale_date,
                "total_amount": (
                    round(total_amount, 2)
                    if total_amount is not None
                    else total_amount
                ),
                "created_at": sale.created_at,
                "updated_at": sale.updated_at
            }

            return sales_data
