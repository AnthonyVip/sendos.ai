import pytest
from fastapi import status as http_status
from httpx import AsyncClient
from main import app


JWT_TOKEN = None
ITEM_ID = None


@pytest.fixture
def mock_user_request():
    class UserRequest:
        email = "user3@example.com"
        password = "string"
    return UserRequest()


@pytest.fixture
def mock_inventory_request():
    class InventoryRequest:
        name = "test"
        description = "other test description"
        quantity = 1
        price = 25
    return InventoryRequest()


@pytest.fixture
def mock_headers():
    return {"Authorization": f"Bearer {JWT_TOKEN}"}


@pytest.mark.asyncio
async def test_create_user(mock_user_request):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "email": mock_user_request.email,
            "password": mock_user_request.password
        }
        response = await ac.post("/api/users/create", json=payload)
        assert response.status_code == http_status.HTTP_201_CREATED
        assert response.json()["jwt_token"]


@pytest.mark.asyncio
async def test_login_user(mock_user_request):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "email": mock_user_request.email,
            "password": mock_user_request.password
        }
        response = await ac.post("/api/users/login", json=payload)
        assert response.status_code == http_status.HTTP_200_OK
        assert response.json()["jwt_token"]
        global JWT_TOKEN
        JWT_TOKEN = response.json()["jwt_token"]


@pytest.mark.asyncio
async def test_create_item(mock_inventory_request, mock_headers):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = mock_headers
        payload = {
            "name": mock_inventory_request.name,
            "description": mock_inventory_request.description,
            "quantity": mock_inventory_request.quantity,
            "price": mock_inventory_request.price
        }
        response = await ac.post(
            "/api/items",
            json=payload,
            headers=headers
        )
        assert response.status_code == http_status.HTTP_201_CREATED
        global ITEM_ID
        ITEM_ID = response.json()["id"]


@pytest.mark.asyncio
async def test_get_item(mock_headers):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = mock_headers
        response = await ac.get(
            f"/api/items/{ITEM_ID}",
            headers=headers
        )
        assert response.status_code == http_status.HTTP_200_OK
        assert response.json()["id"] == ITEM_ID


@pytest.mark.asyncio
async def test_list_items(mock_headers):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = mock_headers
        response = await ac.get(
            "/api/items",
            headers=headers
        )
        assert response.status_code == http_status.HTTP_200_OK


@pytest.mark.asyncio
async def test_delete_item(mock_headers):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = mock_headers
        response = await ac.delete(
            f"/api/items/{ITEM_ID}",
            headers=headers
        )
        assert response.status_code == http_status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_item(mock_headers):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = mock_headers
        payload = {
            "name": "update test",
        }
        response = await ac.put(
            f"/api/items/{ITEM_ID}",
            json=payload,
            headers=headers
        )
        assert response.status_code == http_status.HTTP_200_OK
        assert response.json()["name"] == "update test"
