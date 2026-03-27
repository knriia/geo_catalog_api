import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_root_activity(client: AsyncClient):
    """Создание корневой деятельности"""
    response = await client.post("/activities/", json={"name": "Еда", "parent_id": None})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Еда"
    assert data["parent_id"] is None
    assert data["level"] == 1
    assert "id" in data


@pytest.mark.asyncio
async def test_create_child_activity(client: AsyncClient):
    """Создание дочерней деятельности"""
    parent = await client.post("/activities/", json={"name": "Еда", "parent_id": None})
    parent_id = parent.json()["id"]

    response = await client.post("/activities/", json={"name": "Мясо", "parent_id": parent_id})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Мясо"
    assert data["parent_id"] == parent_id
    assert data["level"] == 2


@pytest.mark.asyncio
async def test_activity_nesting_limit(client: AsyncClient):
    """Проверка ограничения вложенности (максимум 3 уровня)"""
    r1 = await client.post("/activities/", json={"name": "Уровень 1", "parent_id": None})
    assert r1.status_code == 201
    id1 = r1.json()["id"]

    r2 = await client.post("/activities/", json={"name": "Уровень 2", "parent_id": id1})
    assert r2.status_code == 201
    id2 = r2.json()["id"]

    r3 = await client.post("/activities/", json={"name": "Уровень 3", "parent_id": id2})
    assert r3.status_code == 201
    id3 = r3.json()["id"]

    response = await client.post("/activities/", json={"name": "Уровень 4", "parent_id": id3})

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "ActivityLimitError"
    assert "Maximum nesting level" in error["message"]


@pytest.mark.asyncio
async def test_get_activity_tree(client: AsyncClient):
    """Получение ветки дерева деятельностей"""
    food = await client.post("/activities/", json={"name": "Еда", "parent_id": None})
    food_id = food.json()["id"]

    meat = await client.post("/activities/", json={"name": "Мясо", "parent_id": food_id})
    meat_id = meat.json()["id"]

    lamb = await client.post("/activities/", json={"name": "Баранина", "parent_id": meat_id})
    lamb_id = lamb.json()["id"]

    response = await client.get(f"/activities/tree/{food_id}")
    assert response.status_code == 200
    tree = response.json()
    assert len(tree) == 3

    assert tree[0]["id"] == food_id
    assert tree[1]["id"] == meat_id
    assert tree[2]["id"] == lamb_id

    assert tree[0]["name"] == "Еда"
    assert tree[0]["level"] == 1
    assert tree[1]["name"] == "Мясо"
    assert tree[1]["level"] == 2
    assert tree[2]["name"] == "Баранина"
    assert tree[2]["level"] == 3


@pytest.mark.asyncio
async def test_get_activity_tree_from_middle(client: AsyncClient):
    """Получение ветки дерева от промежуточного узла"""
    food = await client.post("/activities/", json={"name": "Еда", "parent_id": None})
    food_id = food.json()["id"]

    meat = await client.post("/activities/", json={"name": "Мясо", "parent_id": food_id})
    meat_id = meat.json()["id"]

    await client.post("/activities/", json={"name": "Баранина", "parent_id": meat_id})

    response = await client.get(f"/activities/tree/{meat_id}")
    assert response.status_code == 200
    tree = response.json()

    assert len(tree) == 2
    assert tree[0]["name"] == "Мясо"
    assert tree[0]["level"] == 2
    assert tree[1]["name"] == "Баранина"
    assert tree[1]["level"] == 3


@pytest.mark.asyncio
async def test_get_nonexistent_activity_tree(client: AsyncClient):
    """Получение ветки несуществующей деятельности"""
    fake_id = "018e3e4a-5f12-7abc-bf21-9958362b535d"
    response = await client.get(f"/activities/tree/{fake_id}")

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "ActivityNotFoundError"
    assert "not found" in error["message"].lower()


@pytest.mark.asyncio
async def test_create_activity_with_nonexistent_parent(client: AsyncClient):
    """Создание деятельности с несуществующим родителем"""
    fake_id = "018e3e4a-5f12-7abc-bf21-9958362b535d"
    response = await client.post("/activities/", json={"name": "Дочерняя", "parent_id": fake_id})

    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "ActivityNotFoundError"


@pytest.mark.asyncio
async def test_activity_level_calculation(client: AsyncClient):
    """Проверка правильности расчета уровня вложенности"""
    r1 = await client.post("/activities/", json={"name": "Корень", "parent_id": None})
    assert r1.json()["level"] == 1

    r2 = await client.post("/activities/", json={"name": "Уровень 2", "parent_id": r1.json()["id"]})
    assert r2.json()["level"] == 2

    r3 = await client.post("/activities/", json={"name": "Уровень 3", "parent_id": r2.json()["id"]})
    assert r3.json()["level"] == 3
