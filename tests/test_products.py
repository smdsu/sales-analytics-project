import pytest
from httpx import AsyncClient
from faker import Faker
import random

fake = Faker()


@pytest.mark.asyncio
async def test_get_all_products_no_auth():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get("/products/")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_product_by_id_no_auth(setup_database):
    test_product_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get(f"/products/{test_product_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_add_product_no_auth():
    categories = ['Electronics', 'Clothing', 'Books', 'Toys', 'Groceries']
    new_product = {
        'product_name': fake.word(),
        'product_description': fake.text(),
        'product_category': random.choice(categories),
        'unit_price': round(random.uniform(5.0, 500.0), 2),
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/products/add/", json=new_product)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_product_by_id_no_auth(setup_database):
    updated_product = {
        "product_name": "Updated Product",
        "product_description": "Updated Product Desc",
        "product_category": "Updated Product Category",
        "unit_price": 777,
    }
    product_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put(
            f"/products/update_by_id/{product_id}",
            json=updated_product
        )
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_product_by_filter_no_auth():
    updated_product = {
        "unit_price": 666.0,
        "unit_price_new": 308.08,
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put(
            "/products/update_by_filter/",
            json=updated_product
        )
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_delete_product_by_id_no_auth(setup_database):
    product_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.delete(f"/products/delete/{product_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_products(fake_super_token):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_product(fake_super_token):
    categories = ['Electronics', 'Clothing', 'Books', 'Toys', 'Groceries']
    new_product = {
        'product_name': fake.word(),
        'product_description': fake.text(),
        'product_category': random.choice(categories),
        'unit_price': round(random.uniform(5.0, 500.0), 2),
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.post("/products/add/", json=new_product)
    assert response.status_code == 200
    assert response.json()["message"] == "Продукт успешно добавлен!"


@pytest.mark.asyncio
async def test_get_product_by_id(fake_super_token, setup_database):
    test_product_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get(f"/products/{test_product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_product_id


@pytest.mark.asyncio
async def test_upd_product_by_id(fake_super_token, setup_database):
    updated_product = {
        "product_name": "Updated Product",
        "product_description": "Updated Product Desc",
        "product_category": "Updated Product Category",
        "unit_price": 777,
    }
    product_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put(
            f"/products/update_by_id/{product_id}",
            json=updated_product
        )
    assert response.status_code == 200
    assert response.json()["message"] == f"Продукт {product_id} успешно обновлён!"


@pytest.mark.asyncio
async def test_upd_product_by_filter(fake_super_token):
    updated_product = {
        "unit_price": 777.00,
        "unit_price_new": 308.08,
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put(
            "/products/update_by_filter/",
            json=updated_product
        )
    assert response.status_code == 200
    assert response.json()["message"] == "Продукты успешно обновлены!"


@pytest.mark.asyncio
async def test_delete_product_by_id(fake_super_token, setup_database):

    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/products/")
        assert response.status_code == 200
        products = response.json()

        max_product_id = max(product['id'] for product in products)

        response = await async_client.delete(f"/products/delete/{max_product_id}")
        print("test_delete_product_by_id: Response status code:", response.status_code)
        assert response.status_code == 200
        assert response.json()["message"] == f"Продукт с {max_product_id} удалён!"
