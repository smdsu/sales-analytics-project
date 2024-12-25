from app.sales.models import Sale
from app.dao.base import BaseDAO

class SaleDAO(BaseDAO):
    model = Sale