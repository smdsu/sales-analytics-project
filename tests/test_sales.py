import pytest
from httpx import AsyncClient
from faker import Faker
import random

fake = Faker()


@pytest.mark.asyncio
async def test_get_all_sales_no_auth():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get("/sales/")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_sales_with_total_no_auth():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get("/sales/with_total")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_sales_with_total_by_id_no_auth():
    test_sale_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get(f"/sales/{test_sale_id}/with_total/")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_in_time_range_no_auth():
    params = [None, "sale_date", "created_at", "updated_at"]
    start_time_range = [None, "2025-01-01", "2025-01-05", "2023-01-08"]
    end_time_range = [None, "2025-01-03", "2025-01-05", "2023-01-01"]
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        for param in params:
            for i in range(len(start_time_range)):
                response = await async_client.get(
                    f"/sales/time_range/{param}",
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
async def test_get_sale_by_id_no_auth(setup_database):
    test_sale_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get(f"/sales/{test_sale_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_add_sale_no_auth():
    new_sale = {
        'branch': fake.city(),
        'city': fake.city(),
        'customer_type': random.choice(['Member', 'Normal']),
        'customer_id': 1,
        'sale_date': fake.date(),
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/sales/add/", json=new_sale)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_sale_by_id_no_auth(setup_database):
    updated_sale = {
        'branch': "Updated branch",
        'city': "Updated city",
        'customer_type': "Updated customer type",
        'customer_id': 1,
        'sale_date': fake.date(),
    }
    sale_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put(
            f"/sales/update_by_id/{sale_id}",
            json=updated_sale
        )
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_sale_by_filter_no_auth():
    updated_sale = {
        "customer_id": 1,
        "customer_type_new": "YoBoy"
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put("/sales/update_by_filter/", json=updated_sale)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_delete_sale_by_id_no_auth(setup_database):
    sale_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.delete(f"/sales/delete/{sale_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_sales(fake_super_token):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/sales/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_sale(fake_super_token):
    new_sale = {
        'branch': fake.city(),
        'city': fake.city(),
        'customer_type': random.choice(['Member', 'Normal']),
        'customer_id': 1,
        'sale_date': fake.date(),
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.post("/sales/add/", json=new_sale)
    assert response.status_code == 200
    assert response.json()["message"] == "Продажа успешно добавлена!"


@pytest.mark.asyncio
async def test_get_sale_by_id(fake_super_token, setup_database):
    test_sale_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get(f"/sales/{test_sale_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_sale_id


@pytest.mark.asyncio
async def test_get_all_sales_with_total(fake_super_token, setup_database):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/sales/with_total")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_all_sales_with_total_by_id(fake_super_token, setup_database):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:

        response = await async_client.get("/sales/")
        assert response.status_code == 200
        sales = response.json()

        max_sale_id = max(sale['id'] for sale in sales)

        response = await async_client.get(f"/sales/{max_sale_id}/with_total/")
    assert response.status_code == 200
    assert response.json()["sale_id"] == max_sale_id


@pytest.mark.asyncio
async def test_get_all_in_time_range(fake_super_token, setup_database):
    params = ["sale_date", "created_at", "updated_at"]
    start_time_range = ["2025-01-01", "2025-01-05", "2023-01-08"]
    end_time_range = ["2025-01-03", "2025-01-05", "2023-01-01"]
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        for param in params:
            for i in range(len(start_time_range)):
                response = await async_client.get(
                    f"/sales/time_range/{param}",
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
async def test_upd_sale_by_id(fake_super_token, setup_database):
    updated_sale = {
        'branch': "Updated branch",
        'city': "Updated city",
        'customer_type': "Updated customer type",
        'customer_id': 1,
        'sale_date': fake.date(),
    }
    sale_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put(
            f"/sales/update_by_id/{sale_id}",
            json=updated_sale
        )
    assert response.status_code == 200
    assert response.json()["message"] == f"Продажа {sale_id} успешно обновлён!"


@pytest.mark.asyncio
async def test_upd_sale_by_filter(fake_super_token):
    updated_sale = {
        "customer_id": 1,
        "customer_type_new": "YoBoy"
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put("/sales/update_by_filter/", json=updated_sale)
    assert response.status_code == 200
    assert response.json()["message"] == "Продажи успешно обновлены!"


@pytest.mark.asyncio
async def test_delete_sale_by_id(fake_super_token, setup_database):
    sale_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.delete(f"/sales/delete/{sale_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Продажа с {sale_id} удалён!"
