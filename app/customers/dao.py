from app.customers.models import Customer
from app.dao.base import BaseDAO


class CustomerDAO(BaseDAO):
    model = Customer
