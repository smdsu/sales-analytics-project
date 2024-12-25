from app.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.saledetails.models import SaleDetails
from app.dao.base import BaseDAO

class SaleDetailsDAO(BaseDAO):
    model = SaleDetails