import pytest
import pytest_asyncio
import random
from httpx import AsyncClient
from fastapi.testclient import TestClient
from faker import Faker
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app  # noqa E402

fake = Faker()


@pytest_asyncio.fixture()
async def fake_super_token():
    from tests.test_auth import test_auth_login
    token = await test_auth_login()
    print("fake_super_token: Token:", token)
    return token


@pytest_asyncio.fixture(scope="session")
async def fake_session_token():
    from tests.test_auth import test_auth_login
    token = await test_auth_login()
    print("fake_session_token: Token:", token)
    return token


@pytest.fixture
def client_with_super_token(fake_super_token):
    client = TestClient(app)
    client.cookies = {"users_access_token": fake_super_token}
    return client


@pytest_asyncio.fixture(scope="session")
async def setup_database():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        # Логин для получения токена
        login_response = await async_client.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "root1"
            }
        )
        token = login_response.cookies.get("users_access_token")
        assert token is not None
        cookies = {"users_access_token": token}

        # Создание новых записей в таблицах
        user_response = await async_client.post("/users/add/", json={
            'phone_number': fake.phone_number(),
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': "root2"
        }, cookies=cookies)
        assert user_response.status_code == 200

        customer_response = await async_client.post("/customers/add/", json={
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(
                minimum_age=18, maximum_age=90
            ).strftime('%Y-%m-%d'),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'gender': random.choice(['Male', 'Female']),
        }, cookies=cookies)
        assert customer_response.status_code == 200

        product_response = await async_client.post("/products/add/", json={
            'product_name': fake.word(),
            'product_description': fake.text(),
            'product_category': random.choice(
                [
                    'Electronics',
                    'Clothing',
                    'Books',
                    'Toys',
                    'Groceries'
                ]
            ),
            'unit_price': round(random.uniform(5.0, 500.0), 2),
        }, cookies=cookies)
        assert product_response.status_code == 200

        sale_response = await async_client.post("/sales/add/", json={
            'branch': fake.city(),
            'city': fake.city(),
            'customer_type': random.choice(['Member', 'Normal']),
            'customer_id': 1,
            'sale_date': fake.date(),
        }, cookies=cookies)
        assert sale_response.status_code == 200

        saledetail_response = await async_client.post("/saledetails/add/", json={
            'sale_id': 1,
            'product_id': 1,
            'quantity': random.randint(1, 10),
        }, cookies=cookies)
        assert saledetail_response.status_code == 200

    yield
