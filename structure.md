geo_catalog_api/
├── migrations/
│   ├── versions/
│   │   └── aa443a1da333_init.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── scripts/
│   ├── init-test-db.sh    # !/bin/bash
│   └── seed.py
├── src/
│   ├── business/
│   │   ├── organizations/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── organization_dto.py
│   │   │   │   └── organization_routers.py
│   │   │   ├── domain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── iorganization_repository.py
│   │   │   │   ├── organization_entity.py
│   │   │   │   └── organization_exceptions.py
│   │   │   ├── infrastructure/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── organization_mapper.py
│   │   │   │   ├── organization_model.py
│   │   │   │   ├── organization_provider.py
│   │   │   │   └── organization_repository.py
│   │   │   ├── __init__.py
│   │   │   ├── organization_service.py
│   │   │   └── test_organizations.py
│   │   └── __init__.py
│   ├── catalogs/
│   │   ├── activities/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── activity_dto.py
│   │   │   │   └── activity_routers.py
│   │   │   ├── domain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── activity_entity.py
│   │   │   │   ├── activity_exceptions.py
│   │   │   │   └── iactivity_repository.py
│   │   │   ├── infrastructure/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── activity_mapper.py
│   │   │   │   ├── activity_model.py
│   │   │   │   ├── activity_provider.py
│   │   │   │   └── activity_repository.py
│   │   │   ├── __init__.py
│   │   │   ├── activity_service.py
│   │   │   └── test_activity.py
│   │   ├── buildings/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── building_dto.py
│   │   │   │   └── building_routers.py
│   │   │   ├── domain/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── building_entity.py
│   │   │   │   ├── building_exceptions.py
│   │   │   │   └── ibuilding_repository.py
│   │   │   ├── infrastructure/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── building_mapper.py
│   │   │   │   ├── building_model.py
│   │   │   │   ├── building_provider.py
│   │   │   │   └── building_repository.py
│   │   │   ├── __init__.py
│   │   │   ├── building_service.py
│   │   │   └── test_building.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── db_provider.py
│   │   │   ├── models.py
│   │   │   └── session_manager.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── handlers.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── di_container.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   ├── test_security.py
│   │   └── types.py
│   ├── __init__.py
│   └── main.py
├── alembic.ini
├── conftest.py
├── docker-compose.yaml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
└── structure.md
