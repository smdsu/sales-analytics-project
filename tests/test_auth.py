import pytest
from httpx import AsyncClient
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
async def test_auth_login():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "root1"
            }
        )
        token = response.cookies.get("users_access_token")
        assert token is not None
        assert response.status_code == 200
        return token


@pytest.mark.asyncio
async def test_logout():
    token = await test_auth_login()
    cookies = {"users_access_token": token}
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies=cookies
    ) as async_client:
        response = await async_client.post("/auth/logout/")
        assert response.status_code == 200
        assert response.cookies.get("users_access_token") is None


@pytest.mark.asyncio
async def test_register_user_with_existing_email():
    reg_data = {
        "phone_number": "98489465",
        "email": "user@example.com",
        "first_name": "Test",
        "last_name": "Test",
        "password": "root2"
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/auth/register", json=reg_data)
        assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_user():
    reg_data = {
        "phone_number": "98489465",
        "email": fake.email(),
        "first_name": "Test",
        "last_name": "Test",
        "password": "root2"
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/auth/register", json=reg_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Пользователь зарегестрирован"


@pytest.mark.asyncio
async def test_get_current_user():
    token = await test_auth_login()
    cookies = {"users_access_token": token}

    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies=cookies
    ) as async_client:
        user_response = await async_client.get("/users/me")
        assert user_response.status_code == 200
        user_data = user_response.json()
        assert user_data.get("email") == "user@example.com"


@pytest.mark.asyncio
async def test_get_all_users_no_auth():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get("/users/")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_user_by_id_no_auth():
    test_user_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get(f"/users/{test_user_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_add_user_no_auth():
    new_user = {
        'phone_number': fake.phone_number(),
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': "root2"
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.post("/users/add/", json=new_user)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_user_by_id_no_auth():
    updated_user = {
        "first_name": "Updated",
        "last_name": "Updated",
        "email": "updated_email@example.com",
    }
    user_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put(
            f"/users/update_by_id/{user_id}",
            json=updated_user
        )
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_user_by_filter_no_auth():
    updated_user = {
        "email": "new_email@example.com",
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put("/users/update_by_filter/", json=updated_user)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_delete_user_by_id_no_auth():
    user_id = 1
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.delete(f"/users/delete/{user_id}")
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_users(fake_super_token):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_by_id(fake_super_token):
    test_user_id = 16
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get(f"/users/{test_user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user_id


@pytest.mark.asyncio
async def test_add_user(fake_super_token):
    new_user = {
        'phone_number': fake.phone_number(),
        'email': fake.email(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'password': "root2"
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.post("/users/add/", json=new_user)
    assert response.status_code == 200
    assert response.json()["message"] == "Пользователь успешно добавлен!"


@pytest.mark.asyncio
async def test_upd_user_by_id(fake_super_token):
    updated_user = {
        "first_name_new": "Updated",
        "last_name_new": "Updated",
        "email_new": "updated_email@example.com",
    }
    user_id = 15
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put(
            f"/users/update_by_id/{user_id}",
            json=updated_user
        )
    assert response.status_code == 200
    assert response.json()["message"] == f"Пользователь {user_id} успешно обновлен!"


@pytest.mark.asyncio
async def test_upd_user_by_filter(fake_super_token):
    updated_user = {
        "email": "updated_email@example.com",
        "email_new": "new_email@example.com",
    }
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put("/users/update_by_filter/", json=updated_user)
    assert response.status_code == 200
    assert response.json()["message"] == "Пользователи успешно обновлены!"


@pytest.mark.asyncio
async def test_delete_user_by_id(fake_super_token):
    user_id = 15
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.delete(f"/users/delete/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Пользователь с {user_id} удалён!"
