from app.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from app.saledetails.models import SaleDetails
from app.dao.base import BaseDAO

class SaleDetailsDAO(BaseDAO):
    model = SaleDetails

    @classmethod
    async def find_with_price_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).options(
                joinedload(cls.model.product)
            ).filter_by(sale_id=data_id)
            result = await session.execute(query)
            sd_info_list = result.scalars().all()

            if not sd_info_list:
                return None
            
            sd_data_list = []
            for sd_info in sd_info_list:
                sd_data = sd_info.to_dict()
                sd_data["unit_price"] = sd_info.product.unit_price
                sd_data["total_price"] = sd_info.product.unit_price * sd_info.quantity
                sd_data_list.append(sd_data)
            
            return sd_data_list