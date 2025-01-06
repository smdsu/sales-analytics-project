import pytest
from httpx import AsyncClient
from faker import Faker

fake = Faker()


@pytest.mark.asyncio
async def test_auth_register():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/auth/register",
            json={
                "phone_number": "98489465",
                "email": "user@example.com",
                "first_name": "Test",
                "last_name": "Test",
                "password": "root1"
            }
        )
        print("test_auth_register: Response status code:", response.status_code)
        assert response.status_code == 200
        assert response.json()["message"] == "Пользователь зарегестрирован"


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
        print("test_auth_login: Response status code:", response.status_code)
        token = response.cookies.get("users_access_token")
        print("test_auth_login: Token:", token)
        assert token is not None
        assert response.status_code == 200
        return token


@pytest.mark.asyncio
async def test_admin_user(fake_super_token):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.put("/users/set_me_founder")
        print("test_admin_user: Response status code:", response.status_code)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_logout():
    token = await test_auth_login()
    cookies = {"users_access_token": token}
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies=cookies
    ) as async_client:
        response = await async_client.post("/auth/logout/")
        print("test_logout: Response status code:", response.status_code)
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
        print(
            "test_register_user_with_existing_email: Response status code:",
            response.status_code
        )
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
        print("test_register_user: Response status code:", response.status_code)
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
        print("test_get_current_user: Response status code:", user_response.status_code)
        assert user_response.status_code == 200
        user_data = user_response.json()
        assert user_data.get("email") == "user@example.com"


@pytest.mark.asyncio
async def test_get_all_users_no_auth():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get("/users/")
    print("test_get_all_users_no_auth: Response status code:", response.status_code)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_user_by_id_no_auth(setup_database):
    test_user_id = 2
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.get(f"/users/{test_user_id}")
    print("test_get_user_by_id_no_auth: Response status code:", response.status_code)
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
    print("test_add_user_no_auth: Response status code:", response.status_code)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_user_by_id_no_auth(setup_database):
    updated_user = {
        "first_name": "Updated",
        "last_name": "Updated",
        "email": "updated_email@example.com",
    }
    user_id = 2
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put(
            f"/users/update_by_id/{user_id}",
            json=updated_user
        )
    print("test_upd_user_by_id_no_auth: Response status code:", response.status_code)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_upd_user_by_filter_no_auth():
    updated_user = {
        "email": "new_email@example.com",
    }
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.put("/users/update_by_filter/", json=updated_user)
    print(
        "test_upd_user_by_filter_no_auth: Response status code:", response.status_code)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_delete_user_by_id_no_auth(setup_database):
    user_id = 2
    async with AsyncClient(base_url="http://127.0.0.1:8000") as async_client:
        response = await async_client.delete(f"/users/delete/{user_id}")
    print("test_delete_user_by_id_no_auth: Response status code:", response.status_code)
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_get_all_users(fake_super_token):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/users/")
    print("test_get_all_users: Response status code:", response.status_code)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_by_id(fake_super_token, setup_database):
    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/users/")
        assert response.status_code == 200
        users = response.json()

        max_user_id = max(user['id'] for user in users)

        response = await async_client.get(f"/users/{max_user_id}")
        print("test_get_user_by_id: Response status code:", response.status_code)
        assert response.status_code == 200
        assert response.json()["id"] == max_user_id


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
    print("test_add_user: Response status code:", response.status_code)
    assert response.status_code == 200
    assert response.json()["message"] == "Пользователь успешно добавлен!"


@pytest.mark.asyncio
async def test_upd_user_by_id(fake_super_token, setup_database):
    updated_user = {
        "first_name_new": "Updated",
        "last_name_new": "Updated",
        "email_new": "updated_email@example.com",
    }

    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/users/")
        assert response.status_code == 200
        users = response.json()

        max_user_id = max(user['id'] for user in users)

        response = await async_client.put(
            f"/users/update_by_id/{max_user_id}",
            json=updated_user
        )
        print("test_upd_user_by_id: Response status code:", response.status_code)
        assert response.status_code == 200
        assert response.json()["message"] == (
            f"Пользователь {max_user_id} успешно обновлен!"
        )


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
    print("test_upd_user_by_filter: Response status code:", response.status_code)
    assert response.status_code == 200
    assert response.json()["message"] == "Пользователи успешно обновлены!"


@pytest.mark.asyncio
async def test_delete_user_by_id(fake_super_token, setup_database):

    async with AsyncClient(
        base_url="http://127.0.0.1:8000",
        cookies={"users_access_token": fake_super_token}
    ) as async_client:
        response = await async_client.get("/users/")
        assert response.status_code == 200
        users = response.json()

        max_user_id = max(user['id'] for user in users)

        response = await async_client.delete(f"/users/delete/{max_user_id}")
        print("test_delete_user_by_id: Response status code:", response.status_code)
        assert response.status_code == 200
        assert response.json()["message"] == f"Пользователь с {max_user_id} удалён!"
