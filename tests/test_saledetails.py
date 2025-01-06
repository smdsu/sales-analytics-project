import pytest
from httpx import AsyncClient
import random


@pytest.mark.asyncio
async def test_get_all_salesdetails_no_auth():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get("/saledetails/")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_full_saledetail_by_sale_id_no_auth():
    test_sale_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get(f"/saledetails/full_bill/{test_sale_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_add_saledetail_no_auth():
    new_saledetail = {
        'sale_id': 1,
        'product_id': 1,
        'quantity': random.randint(1, 10),
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/saledetails/add/", json=new_saledetail)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_saledetail_no_auth():
    updated_sale = {
        "sale_id": 1,
        'product_id': 1,
        'quantity': 77,
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put("/saledetails/update/", json=updated_sale)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_delete_saledetail_no_auth():
    sale_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.delete(f"/saledetails/delete/{sale_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_salesdetails(fake_super_token):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/saledetails/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_full_saledetail_by_sale_id(fake_super_token):
    test_sale_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get(f"/saledetails/full_bill/{test_sale_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_saledetail(fake_super_token):
    new_saledetail = {
        'sale_id': 1,
        'product_id': 1,
        'quantity': random.randint(1, 10),
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.post("/saledetails/add/", json=new_saledetail)
    assert response.status_code == 200
    assert response.json()["message"] == "Детали продажи успешно добавлены!"


@pytest.mark.asyncio
async def test_upd_saledetail(fake_super_token):
    updated_sale = {
        "sale_id": 1,
        'product_id': 1,
        'quantity_new': 77,
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put("/saledetails/update/", json=updated_sale)
    assert response.status_code == 200
    assert response.json()["message"] == "Детали продажи успешно обновлены!"


@pytest.mark.asyncio
async def test_delete_saledetail(fake_super_token):
    sale_id = 2
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.delete(f"/saledetails/delete/{sale_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Детали продажи с {sale_id} удалены!"
