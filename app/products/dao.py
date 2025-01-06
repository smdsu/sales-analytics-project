from app.products.models import Product
from app.dao.base import BaseDAO


class ProductDAO(BaseDAO):
    model = Product
