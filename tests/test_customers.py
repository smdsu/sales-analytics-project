import pytest
from httpx import AsyncClient
from faker import Faker
import random

fake = Faker()


@pytest.mark.asyncio
async def test_get_all_customers_no_auth():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get("/customers/")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_customer_by_id_no_auth(setup_database):
    test_customer_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get(f"/customers/{test_customer_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_add_customer_no_auth():
    new_customer = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_birth': fake.date_of_birth(
            minimum_age=18, maximum_age=90
        ).strftime('%Y-%m-%d'),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'gender': random.choice(['Male', 'Female']),
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/customers/add/", json=new_customer)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_customer_by_id_no_auth(setup_database):
    updated_customer = {
        "name": "Updated Customer",
        "email": "updated@example.com",
        "phone": "+0987654321"
    }
    customer_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put(
            f"/customers/update_by_id/{customer_id}",
            json=updated_customer
        )
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_customer_by_filter_no_auth():
    updated_customer = {
        "phone": "9876543210"
    }
    filter_data = {
        "email": "test@example.com"
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put(
            "/customers/update_by_filter/",
            json={
                **updated_customer,
                **filter_data
            }
        )
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_delete_customer_by_id_no_auth(setup_database):
    customer_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.delete(f"/customers/delete/{customer_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_customers(fake_super_token):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/customers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_customer(fake_super_token):
    new_customer = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'date_of_birth': fake.date_of_birth(
            minimum_age=18, maximum_age=90
        ).strftime('%Y-%m-%d'),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'gender': random.choice(['Male', 'Female']),
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.post("/customers/add/", json=new_customer)
    assert response.status_code == 200
    assert response.json()["message"] == "Покупатель успешно добавлен!"


@pytest.mark.asyncio
async def test_get_customer_by_id(fake_super_token, setup_database):
    test_customer_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get(f"/customers/{test_customer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_customer_id


@pytest.mark.asyncio
async def test_upd_customer_by_id(fake_super_token, setup_database):
    updated_customer = {
        "name": "Updated Customer",
        "email": "updated@example.com",
        "phone": "+0987654321"
    }
    customer_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put(
            f"/customers/update_by_id/{customer_id}",
            json=updated_customer
        )
    assert response.status_code == 200
    assert response.json()["message"] == f"Покупатель {customer_id} успешно обновлен!"


@pytest.mark.asyncio
async def test_upd_customer_by_filter(fake_super_token):
    updated_customer = {
        "phone_new": "9876543210"
    }
    filter_data = {
        "email": "updated@example.com"
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put(
            "/customers/update_by_filter/",
            json={
                **updated_customer,
                **filter_data
            }
        )
    assert response.status_code == 200
    assert response.json()["message"] == "Покупатели успешно обновлены!"


@pytest.mark.asyncio
async def test_delete_customer_by_id(fake_super_token, setup_database):
    customer_id = 1
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.delete(f"/customers/delete/{customer_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Покупатель с {customer_id} удалён!"
