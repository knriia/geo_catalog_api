import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_authorization_security(client: AsyncClient):
    """Проверка авторизации без API ключа"""
    async with AsyncClient(transport=client._transport, base_url=client.base_url) as unauthorized_client:
        response = await unauthorized_client.get("/organizations/search/name?name=test")
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_authorization_with_valid_key(client: AsyncClient):
    """Проверка авторизации с валидным API ключом"""
    response = await client.get("/organizations/search/name?name=test")
    assert response.status_code != 401


@pytest.mark.asyncio
async def test_authorization_with_invalid_key(client: AsyncClient):
    """Проверка авторизации с невалидным API ключом"""
    async with AsyncClient(transport=client._transport, base_url=client.base_url) as invalid_client:
        invalid_client.headers.update({"X-API-KEY": "invalid-key-12345"})
        response = await invalid_client.get("/organizations/search/name?name=test")
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid API Key"
