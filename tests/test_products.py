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
async def test_get_all_in_time_range_no_auth():
    params = ["created_at", "updated_at"]
    start_time_range = ["2025-01-01", "2025-01-05", "2023-01-08"]
    end_time_range = ["2025-01-03", "2025-01-05", "2023-01-01"]
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        for param in params:
            for i in range(len(start_time_range)):
                response = await async_client.get(
                    f"/products/time_range/{param}",
                    params={
                        "start_time": start_time_range[i],
                        "end_time": end_time_range[i]
                    }
                )
                print(
                    "param:", param,
                    "start_time:", start_time_range[i],
                    "end_time:", end_time_range[i]
                )
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
async def test_bulk_insert_no_auth():
    test_data = (
        b"product_name,product_description,product_category,unit_price\n"
        b"Product A,Desc A,Category X,99.99\n"
        b"Product B,Desc B,Category Y,49.50\n"
    )
    file = {"file": ("test.csv", test_data, "text/csv")}
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/products/bulk_insert/", files=file)
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
async def test_get_all_in_time_range(fake_super_token, setup_database):
    params = ["created_at", "updated_at"]
    start_time_range = ["2025-01-01", "2025-01-05", "2023-01-08"]
    end_time_range = ["2025-01-03", "2025-01-05", "2023-01-01"]
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        for param in params:
            for i in range(len(start_time_range)):
                response = await async_client.get(
                    f"/products/time_range/{param}",
                    params={
                        "start_time": start_time_range[i],
                        "end_time": end_time_range[i]
                    }
                )
                print(
                    "param:", param,
                    "start_time:", start_time_range[i],
                    "end_time:", end_time_range[i]
                )
                assert response.status_code == 200
                assert isinstance(response.json(), list)


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


@pytest.mark.asyncio
async def test_bulk_insert(fake_super_token):
    test_data = (
        b"product_name,product_description,product_category,unit_price\n"
        b"Product A,Desc A,Category X,99.99\n"
        b"Product B,Desc B,Category Y,49.50\n"
    )
    file = {"file": ("test.csv", test_data, "text/csv")}
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.post("/products/bulk_insert/", files=file)
    assert response.status_code == 200
    assert response.json()["message"] == "Продукты успешно добавлены!"
