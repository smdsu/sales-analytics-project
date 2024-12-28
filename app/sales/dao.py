from sqlalchemy.orm import joinedload
from app.sales.models import Sale
from app.dao.base import BaseDAO

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session_maker

class SaleDAO(BaseDAO):
    model = Sale