import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_organization(client: AsyncClient):
    """Создание организации"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    activity = await client.post("/activities/", json={"name": "Тестовая деятельность", "parent_id": None})
    activity_id = activity.json()["id"]

    response = await client.post(
        "/organizations/",
        json={
            "name": "Тестовая Организация",
            "building_id": building_id,
            "phone_numbers": ["12345678"],
            "activity_ids": [activity_id],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Тестовая Организация"
    assert len(data["phone_numbers"]) == 1
    assert data["phone_numbers"][0] == "12345678"
    assert data["building"]["id"] == building_id
    assert len(data["activities"]) == 1
    assert data["activities"][0]["id"] == activity_id


@pytest.mark.asyncio
async def test_create_organization_multiple_phones(client: AsyncClient):
    """Создание организации с несколькими телефонами"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    activity = await client.post("/activities/", json={"name": "Тест", "parent_id": None})
    activity_id = activity.json()["id"]

    response = await client.post(
        "/organizations/",
        json={
            "name": "Многоканальная компания",
            "building_id": building_id,
            "phone_numbers": ["12345678", "87654321", "11223344"],
            "activity_ids": [activity_id],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["phone_numbers"]) == 3
    assert "12345678" in data["phone_numbers"]
    assert "87654321" in data["phone_numbers"]
    assert "11223344" in data["phone_numbers"]


@pytest.mark.asyncio
async def test_create_organization_without_activities(client: AsyncClient):
    """Создание организации без видов деятельности"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    response = await client.post(
        "/organizations/",
        json={
            "name": "Компания без деятельности",
            "building_id": building_id,
            "phone_numbers": ["12345678"],
            "activity_ids": [],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Компания без деятельности"
    assert data["activities"] == []


@pytest.mark.asyncio
async def test_get_organization_by_id(client: AsyncClient):
    """Получение организации по ID"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    activity = await client.post("/activities/", json={"name": "Тест", "parent_id": None})
    activity_id = activity.json()["id"]

    created = await client.post(
        "/organizations/",
        json={
            "name": "Тестовая",
            "building_id": building_id,
            "phone_numbers": ["12345678"],
            "activity_ids": [activity_id],
        },
    )
    org_id = created.json()["id"]

    response = await client.get(f"/organizations/{org_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == org_id
    assert data["name"] == "Тестовая"
    assert data["building"]["id"] == building_id
    assert data["activities"][0]["id"] == activity_id


@pytest.mark.asyncio
async def test_get_nonexistent_organization(client: AsyncClient):
    """Получение несуществующей организации"""
    fake_id = "018e3e4a-5f12-7abc-bf21-9958362b535d"
    response = await client.get(f"/organizations/{fake_id}")

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "OrganizationNotFoundError"
    assert "not found" in error["message"].lower()


@pytest.mark.asyncio
async def test_search_organization_by_name(client: AsyncClient):
    """Поиск организации по имени"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    await client.post(
        "/organizations/",
        json={"name": "Альфа Групп", "building_id": building_id, "phone_numbers": ["11111111"], "activity_ids": []},
    )
    await client.post(
        "/organizations/",
        json={"name": "Бета Софт", "building_id": building_id, "phone_numbers": ["22222222"], "activity_ids": []},
    )

    response = await client.get("/organizations/search/name", params={"name": "Альфа"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Альфа Групп"

    response = await client.get("/organizations/search/name", params={"name": "Несуществующая"})
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_search_organization_by_building(client: AsyncClient):
    """Список организаций в здании"""
    building1 = await client.post("/buildings/", json={"address": "Здание 1 тест", "latitude": 55.0, "longitude": 37.0})
    building1_id = building1.json()["id"]

    building2 = await client.post("/buildings/", json={"address": "Здание 2 тест", "latitude": 56.0, "longitude": 38.0})
    building2_id = building2.json()["id"]

    for i in range(3):
        await client.post(
            "/organizations/",
            json={
                "name": f"Компания {i}",
                "building_id": building1_id,
                "phone_numbers": [f"{i}" * 8],
                "activity_ids": [],
            },
        )

    response = await client.get(f"/organizations/building/{building1_id}")
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = await client.get(f"/organizations/building/{building2_id}")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_organization_with_multiple_activities(client: AsyncClient):
    """Организация с несколькими несвязанными активностями"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    activity1 = await client.post("/activities/", json={"name": "Цветы", "parent_id": None})
    activity2 = await client.post("/activities/", json={"name": "Кофе", "parent_id": None})
    activity1_id = activity1.json()["id"]
    activity2_id = activity2.json()["id"]

    response = await client.post(
        "/organizations/",
        json={
            "name": "Кофе и Розы",
            "building_id": building_id,
            "phone_numbers": ["12345678"],
            "activity_ids": [activity1_id, activity2_id],
        },
    )
    assert response.status_code == 201

    res = await client.get(f"/organizations/search/activity/{activity1_id}")
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Кофе и Розы"

    res = await client.get(f"/organizations/search/activity/{activity2_id}")
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Кофе и Розы"


@pytest.mark.asyncio
async def test_activity_hierarchy_search(client: AsyncClient):
    """Поиск организаций по иерархии деятельностей"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    food = await client.post("/activities/", json={"name": "Еда", "parent_id": None})
    food_id = food.json()["id"]

    meat = await client.post("/activities/", json={"name": "Мясо", "parent_id": food_id})
    meat_id = meat.json()["id"]

    lamb = await client.post("/activities/", json={"name": "Баранина", "parent_id": meat_id})
    lamb_id = lamb.json()["id"]

    await client.post(
        "/organizations/",
        json={
            "name": "Мясной Склад",
            "building_id": building_id,
            "phone_numbers": ["11111111"],
            "activity_ids": [meat_id],
        },
    )
    await client.post(
        "/organizations/",
        json={
            "name": "Мир Баранины",
            "building_id": building_id,
            "phone_numbers": ["22222222"],
            "activity_ids": [lamb_id],
        },
    )

    res = await client.get(f"/organizations/search/activity/{food_id}")
    names = [o["name"] for o in res.json()]
    assert "Мясной Склад" in names
    assert "Мир Баранины" in names
    assert len(res.json()) == 2

    res = await client.get(f"/organizations/search/activity/{meat_id}")
    assert len(res.json()) == 2

    res = await client.get(f"/organizations/search/activity/{lamb_id}")
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Мир Баранины"


@pytest.mark.asyncio
async def test_geo_search_organizations_radius(client: AsyncClient):
    """Поиск организаций в радиусе"""
    center = await client.post("/buildings/", json={"address": "Центр здание", "latitude": 55.0, "longitude": 37.0})
    center_id = center.json()["id"]

    nearby = await client.post("/buildings/", json={"address": "Рядом здание", "latitude": 55.01, "longitude": 37.01})
    nearby_id = nearby.json()["id"]

    far = await client.post("/buildings/", json={"address": "Далеко здание", "latitude": 56.0, "longitude": 38.0})
    far_id = far.json()["id"]

    activity = await client.post("/activities/", json={"name": "Тест", "parent_id": None})
    activity_id = activity.json()["id"]

    await client.post(
        "/organizations/",
        json={
            "name": "Центральная компания",
            "building_id": center_id,
            "phone_numbers": ["11111111"],
            "activity_ids": [activity_id],
        },
    )
    await client.post(
        "/organizations/",
        json={
            "name": "Близкая компания",
            "building_id": nearby_id,
            "phone_numbers": ["22222222"],
            "activity_ids": [activity_id],
        },
    )
    await client.post(
        "/organizations/",
        json={
            "name": "Дальняя компания",
            "building_id": far_id,
            "phone_numbers": ["33333333"],
            "activity_ids": [activity_id],
        },
    )

    response = await client.get("/organizations/search/radius", params={"lat": 55.0, "lon": 37.0, "radius": 2000})
    assert response.status_code == 200
    names = [o["name"] for o in response.json()]
    assert "Центральная компания" in names
    assert "Близкая компания" in names
    assert "Дальняя компания" not in names


@pytest.mark.asyncio
async def test_geo_search_organizations_bounds(client: AsyncClient):
    """Поиск организаций в прямоугольной области"""
    inside = await client.post("/buildings/", json={"address": "Внутри области", "latitude": 55.5, "longitude": 37.5})
    inside_id = inside.json()["id"]

    outside = await client.post("/buildings/", json={"address": "Снаружи области", "latitude": 56.5, "longitude": 38.5})
    outside_id = outside.json()["id"]

    activity = await client.post("/activities/", json={"name": "Тест", "parent_id": None})
    activity_id = activity.json()["id"]

    await client.post(
        "/organizations/",
        json={
            "name": "Внутренняя компания",
            "building_id": inside_id,
            "phone_numbers": ["11111111"],
            "activity_ids": [activity_id],
        },
    )
    await client.post(
        "/organizations/",
        json={
            "name": "Внешняя компания",
            "building_id": outside_id,
            "phone_numbers": ["22222222"],
            "activity_ids": [activity_id],
        },
    )

    response = await client.get(
        "/organizations/search/bounds", params={"min_lat": 55.0, "min_lon": 37.0, "max_lat": 56.0, "max_lon": 38.0}
    )
    assert response.status_code == 200
    names = [o["name"] for o in response.json()]
    assert "Внутренняя компания" in names
    assert "Внешняя компания" not in names


@pytest.mark.asyncio
async def test_create_organization_invalid_building(client: AsyncClient):
    """Создание организации с несуществующим зданием"""
    fake_id = "018e3e4a-5f12-7abc-bf21-9958362b535d"
    activity = await client.post("/activities/", json={"name": "Тест", "parent_id": None})
    activity_id = activity.json()["id"]

    response = await client.post(
        "/organizations/",
        json={"name": "Призрак", "building_id": fake_id, "phone_numbers": ["12345678"], "activity_ids": [activity_id]},
    )
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "RelatedEntityNotFound"


@pytest.mark.asyncio
async def test_create_organization_invalid_activity(client: AsyncClient):
    """Создание организации с несуществующей деятельностью"""
    building = await client.post(
        "/buildings/", json={"address": "Тестовое здание", "latitude": 55.0, "longitude": 37.0}
    )
    building_id = building.json()["id"]

    fake_id = "018e3e4a-5f12-7abc-bf21-9958362b535d"

    response = await client.post(
        "/organizations/",
        json={"name": "Призрак", "building_id": building_id, "phone_numbers": ["12345678"], "activity_ids": [fake_id]},
    )
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "RelatedEntityNotFound"
