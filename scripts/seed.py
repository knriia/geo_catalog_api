import asyncio

from src.business.organizations.domain.organization_entity import OrganizationCreateEntity
from src.business.organizations.organization_service import OrganizationService
from src.catalogs.activities.activity_service import ActivityService
from src.catalogs.activities.domain.activity_entity import ActivityCreateEntity
from src.catalogs.buildings.building_service import BuildingService
from src.catalogs.buildings.domain.building_entity import BuildingCreateEntity
from src.core.di_container import get_di_container

# Структура деятельностей с иерархией
ACTIVITIES = [
    # Уровень 1
    {"name": "Продукты питания"},
    {"name": "Автомобили и запчасти"},
    {"name": "Одежда и обувь"},
    {"name": "Электроника"},

    # Уровень 2 (Продукты питания)
    {"name": "Мясная продукция", "parent": "Продукты питания"},
    {"name": "Молочная продукция", "parent": "Продукты питания"},
    {"name": "Овощи и фрукты", "parent": "Продукты питания"},
    {"name": "Хлебобулочные изделия", "parent": "Продукты питания"},

    # Уровень 2 (Автомобили)
    {"name": "Запчасти", "parent": "Автомобили и запчасти"},
    {"name": "Шины и диски", "parent": "Автомобили и запчасти"},
    {"name": "Автомасла и жидкости", "parent": "Автомобили и запчасти"},
    {"name": "Автоаксессуары", "parent": "Автомобили и запчасти"},

    # Уровень 2 (Одежда)
    {"name": "Мужская одежда", "parent": "Одежда и обувь"},
    {"name": "Женская одежда", "parent": "Одежда и обувь"},
    {"name": "Детская одежда", "parent": "Одежда и обувь"},
    {"name": "Обувь", "parent": "Одежда и обувь"},

    # Уровень 2 (Электроника)
    {"name": "Смартфоны", "parent": "Электроника"},
    {"name": "Ноутбуки и ПК", "parent": "Электроника"},
    {"name": "Телевизоры", "parent": "Электроника"},
    {"name": "Аксессуары", "parent": "Электроника"},

    # Уровень 3 (Мясная продукция)
    {"name": "Говядина", "parent": "Мясная продукция"},
    {"name": "Свинина", "parent": "Мясная продукция"},
    {"name": "Курица", "parent": "Мясная продукция"},
    {"name": "Колбасные изделия", "parent": "Мясная продукция"},

    # Уровень 3 (Молочная продукция)
    {"name": "Молоко", "parent": "Молочная продукция"},
    {"name": "Сыры", "parent": "Молочная продукция"},
    {"name": "Йогурты", "parent": "Молочная продукция"},
    {"name": "Творог", "parent": "Молочная продукция"},

    # Уровень 3 (Овощи и фрукты)
    {"name": "Овощи", "parent": "Овощи и фрукты"},
    {"name": "Фрукты", "parent": "Овощи и фрукты"},
    {"name": "Зелень", "parent": "Овощи и фрукты"},

    # Уровень 3 (Запчасти)
    {"name": "Двигатели", "parent": "Запчасти"},
    {"name": "Трансмиссия", "parent": "Запчасти"},
    {"name": "Тормозная система", "parent": "Запчасти"},
    {"name": "Электрика", "parent": "Запчасти"},
]

# Здания Москвы
BUILDINGS = [
    {"address": "г. Москва, ул. Тверская, д. 15", "latitude": 55.7646, "longitude": 37.6056},
    {"address": "г. Москва, ул. Арбат, д. 10", "latitude": 55.7512, "longitude": 37.5924},
    {"address": "г. Москва, Ленинградский пр-т, д. 44", "latitude": 55.7965, "longitude": 37.5425},
    {"address": "г. Москва, Кутузовский пр-т, д. 32", "latitude": 55.7403, "longitude": 37.5341},
    {"address": "г. Москва, ул. Новый Арбат, д. 21", "latitude": 55.7520, "longitude": 37.5866},
    {"address": "г. Москва, пр-т Мира, д. 104", "latitude": 55.8236, "longitude": 37.6373},
    {"address": "г. Москва, ул. Пятницкая, д. 45", "latitude": 55.7407, "longitude": 37.6273},
    {"address": "г. Москва, Садовое кольцо, д. 14", "latitude": 55.7655, "longitude": 37.6061},
    {"address": "г. Москва, ул. Большая Дмитровка, д. 8", "latitude": 55.7638, "longitude": 37.6157},
    {"address": "г. Москва, ул. Мясницкая, д. 20", "latitude": 55.7625, "longitude": 37.6331},
    {"address": "г. Москва, ул. Покровка, д. 12", "latitude": 55.7593, "longitude": 37.6435},
    {"address": "г. Москва, Ленинский пр-т, д. 45", "latitude": 55.6973, "longitude": 37.5623},
    {"address": "г. Москва, ул. Профсоюзная, д. 102", "latitude": 55.6587, "longitude": 37.5539},
    {"address": "г. Москва, ул. Академика Королева, д. 12", "latitude": 55.8224, "longitude": 37.6320},
]

# Организации
ORGANIZATIONS = [
    {
        "name": "Мясной Гастроном",
        "building": "г. Москва, ул. Тверская, д. 15",
        "phone_numbers": ["+7-495-123-45-67", "+7-916-123-45-67"],
        "activities": ["Говядина", "Свинина", "Курица"]
    },
    {
        "name": "Молочная Лавка",
        "building": "г. Москва, ул. Арбат, д. 10",
        "phone_numbers": ["+7-495-987-65-43"],
        "activities": ["Молоко", "Сыры", "Йогурты"]
    },
    {
        "name": "Овощной Рай",
        "building": "г. Москва, ул. Новый Арбат, д. 21",
        "phone_numbers": ["+7-495-555-12-34"],
        "activities": ["Овощи", "Фрукты", "Зелень"]
    },
    {
        "name": "Автозапчасти",
        "building": "г. Москва, Ленинградский пр-т, д. 44",
        "phone_numbers": ["+7-495-777-88-99", "+7-915-777-88-99"],
        "activities": ["Двигатели", "Трансмиссия", "Тормозная система"]
    },
    {
        "name": "Шиномонтаж",
        "building": "г. Москва, Кутузовский пр-т, д. 32",
        "phone_numbers": ["+7-495-111-22-33"],
        "activities": ["Шины и диски"]
    },
    {
        "name": "Автомасла",
        "building": "г. Москва, ул. Мясницкая, д. 20",
        "phone_numbers": ["+7-495-444-55-66"],
        "activities": ["Автомасла и жидкости"]
    },
    {
        "name": "Хлебный Дом",
        "building": "г. Москва, ул. Пятницкая, д. 45",
        "phone_numbers": ["+7-495-888-99-00"],
        "activities": ["Хлебобулочные изделия"]
    },
    {
        "name": "Мужской Стиль",
        "building": "г. Москва, ул. Большая Дмитровка, д. 8",
        "phone_numbers": ["+7-495-222-33-44"],
        "activities": ["Мужская одежда", "Обувь"]
    },
    {
        "name": "Женская Мода",
        "building": "г. Москва, ул. Покровка, д. 12",
        "phone_numbers": ["+7-495-666-77-88"],
        "activities": ["Женская одежда", "Обувь"]
    },
    {
        "name": "Детский Мир",
        "building": "г. Москва, пр-т Мира, д. 104",
        "phone_numbers": ["+7-495-999-00-11"],
        "activities": ["Детская одежда", "Обувь"]
    },
    {
        "name": "Цифровой Рай",
        "building": "г. Москва, ул. Тверская, д. 15",
        "phone_numbers": ["+7-495-123-45-67"],
        "activities": ["Смартфоны", "Ноутбуки и ПК", "Аксессуары"]
    },
    {
        "name": "ТехноМир",
        "building": "г. Москва, ул. Профсоюзная, д. 102",
        "phone_numbers": ["+7-495-777-88-99"],
        "activities": ["Телевизоры", "Аксессуары"]
    },
    {
        "name": "Колбасный Цех",
        "building": "г. Москва, ул. Арбат, д. 10",
        "phone_numbers": ["+7-495-444-55-66"],
        "activities": ["Колбасные изделия", "Мясная продукция"]
    },
    {
        "name": "Сырная История",
        "building": "г. Москва, ул. Мясницкая, д. 20",
        "phone_numbers": ["+7-495-888-99-00"],
        "activities": ["Сыры", "Молочная продукция"]
    },
    {
        "name": "Автоэлектрика",
        "building": "г. Москва, Ленинградский пр-т, д. 44",
        "phone_numbers": ["+7-495-111-22-33"],
        "activities": ["Электрика", "Автоаксессуары"]
    },
]


async def seed():
    container = get_di_container()

    async with container() as request_container:
        activity_service = await request_container.get(ActivityService)
        building_service = await request_container.get(BuildingService)
        org_service = await request_container.get(OrganizationService)

        print("🌱 Начинаем заполнение базы данными...")
        print("=" * 50)

        print("\n📁 Создание активностей...")
        activity_ids = {}

        for activity in ACTIVITIES:
            parent_id = None
            if "parent" in activity:
                parent_name = activity["parent"]
                parent_id = activity_ids.get(parent_name)
                if not parent_id:
                    print(f"  ⚠️ Родительская активность не найдена: {parent_name} для {activity['name']}")
                    continue

            created = await activity_service.create_activity(
                ActivityCreateEntity(name=activity["name"], parent_id=parent_id)
            )
            activity_ids[activity["name"]] = created.id
            level = "  " * (created.level - 1) + "└─"
            print(f"  {level} {activity['name']} (уровень {created.level})")

        print(f"  ✅ Создано {len(activity_ids)} активностей")

        print("\n🏢 Создание зданий...")
        building_ids = {}
        for building in BUILDINGS:
            created = await building_service.create_building(
                BuildingCreateEntity(
                    address=building["address"],
                    latitude=building["latitude"],
                    longitude=building["longitude"]
                )
            )
            building_ids[building["address"]] = created.id
            print(f"  ✅ {building['address']}")

        print(f"  ✅ Создано {len(building_ids)} зданий")

        print("\n🏢 Создание организаций...")
        count = 0
        for org in ORGANIZATIONS:
            building_id = building_ids.get(org["building"])
            if not building_id:
                print(f"  ⚠️ Здание не найдено: {org['building']}")
                continue

            org_activity_ids = []
            for act_name in org["activities"]:
                act_id = activity_ids.get(act_name)
                if act_id:
                    org_activity_ids.append(act_id)
                else:
                    print(f"  ⚠️ Активность не найдена: {act_name}")

            try:
                await org_service.create_organization(
                    OrganizationCreateEntity(
                        name=org["name"],
                        building_id=building_id,
                        phone_numbers=org["phone_numbers"],
                        activity_ids=org_activity_ids
                    )
                )
                count += 1
                print(f"  ✅ {org['name']}")
            except Exception as e:
                print(f"  ❌ Ошибка при создании {org['name']}: {e}")

        print("\n" + "=" * 50)
        print(f"🎉 Заполнение завершено!")
        print(f"  📊 Активностей: {len(activity_ids)}")
        print(f"  🏢 Зданий: {len(building_ids)}")
        print(f"  🏢 Организаций: {count}")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(seed())