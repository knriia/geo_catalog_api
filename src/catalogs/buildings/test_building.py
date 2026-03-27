import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_building(client: AsyncClient):
    """Создание здания"""
    response = await client.post(
        "/buildings/", json={"address": "г. Москва, ул. Ленина 1", "latitude": 55.7558, "longitude": 37.6173}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["address"] == "г. Москва, ул. Ленина 1"
    assert data["latitude"] == 55.7558
    assert data["longitude"] == 37.6173
    assert "id" in data


@pytest.mark.asyncio
async def test_get_all_buildings(client: AsyncClient):
    """Получение всех зданий"""
    await client.post("/buildings/", json={"address": "Здание 1 тест", "latitude": 10, "longitude": 10})
    await client.post("/buildings/", json={"address": "Здание 2 тест", "latitude": 20, "longitude": 20})
    await client.post("/buildings/", json={"address": "Здание 3 тест", "latitude": 30, "longitude": 30})

    response = await client.get("/buildings/")
    assert response.status_code == 200
    buildings = response.json()
    assert len(buildings) >= 3

    addresses = [b["address"] for b in buildings]
    assert "Здание 1 тест" in addresses
    assert "Здание 2 тест" in addresses
    assert "Здание 3 тест" in addresses


@pytest.mark.asyncio
async def test_get_building_by_id(client: AsyncClient):
    """Получение здания по ID"""
    created = await client.post("/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0})
    building_id = created.json()["id"]

    response = await client.get(f"/buildings/{building_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == building_id
    assert data["address"] == "Тестовое здание"
    assert data["latitude"] == 55.0
    assert data["longitude"] == 37.0


@pytest.mark.asyncio
async def test_get_nonexistent_building(client: AsyncClient):
    """Получение несуществующего здания"""
    fake_id = "018e3e4a-5f12-7abc-bf21-9958362b535d"
    response = await client.get(f"/buildings/{fake_id}")

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "BuildingNotFoundError"
    assert "not found" in error["message"].lower()


@pytest.mark.asyncio
async def test_search_buildings_in_radius(client: AsyncClient):
    """Поиск зданий в радиусе"""
    center = await client.post("/buildings/", json={"address": "Центр здание", "latitude": 55.0, "longitude": 37.0})
    center_id = center.json()["id"]

    nearby = await client.post("/buildings/", json={"address": "Рядом здание", "latitude": 55.01, "longitude": 37.01})
    nearby_id = nearby.json()["id"]

    far = await client.post("/buildings/", json={"address": "Далеко здание", "latitude": 56.0, "longitude": 38.0})
    far_id = far.json()["id"]

    response = await client.get(
        "/buildings/search/radius", params={"latitude": 55.0, "longitude": 37.0, "radius_meters": 2000}
    )
    assert response.status_code == 200
    buildings = response.json()
    building_ids = [b["id"] for b in buildings]

    assert center_id in building_ids
    assert nearby_id in building_ids
    assert far_id not in building_ids


@pytest.mark.asyncio
async def test_search_buildings_in_radius_empty(client: AsyncClient):
    """Поиск зданий в радиусе — пустой результат"""
    await client.post("/buildings/", json={"address": "Далекое здание", "latitude": 60.0, "longitude": 60.0})

    response = await client.get(
        "/buildings/search/radius", params={"latitude": 0, "longitude": 0, "radius_meters": 1000}
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_search_buildings_in_bounds(client: AsyncClient):
    """Поиск зданий в прямоугольной области"""
    inside = await client.post("/buildings/", json={"address": "Внутри области", "latitude": 55.5, "longitude": 37.5})
    inside_id = inside.json()["id"]

    east = await client.post("/buildings/", json={"address": "Восточнее здание", "latitude": 55.5, "longitude": 38.5})
    east_id = east.json()["id"]

    north = await client.post("/buildings/", json={"address": "Севернее здание", "latitude": 56.5, "longitude": 37.5})
    north_id = north.json()["id"]

    response = await client.get(
        "/buildings/search/bounds",
        params={"min_latitude": 55.0, "min_longitude": 37.0, "max_latitude": 56.0, "max_longitude": 38.0},
    )
    assert response.status_code == 200
    buildings = response.json()
    building_ids = [b["id"] for b in buildings]

    assert inside_id in building_ids
    assert east_id not in building_ids
    assert north_id not in building_ids


@pytest.mark.asyncio
async def test_search_buildings_in_bounds_empty(client: AsyncClient):
    """Поиск зданий в прямоугольной области — пустой результат"""
    await client.post("/buildings/", json={"address": "Где-то здание", "latitude": 55.5, "longitude": 37.5})

    response = await client.get(
        "/buildings/search/bounds",
        params={"min_latitude": 0, "min_longitude": 0, "max_latitude": 1, "max_longitude": 1},
    )
    assert response.status_code == 200
    assert response.json() == []
