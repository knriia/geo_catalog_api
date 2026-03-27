# Geo Catalog API

Справочник организаций с геопоиском и иерархической структурой видов деятельности.

## 📋 О проекте

API для управления каталогом организаций, зданий и видов деятельности. Поддерживает:
- Иерархию видов деятельности (максимум 3 уровня)
- Геопоиск по радиусу и прямоугольной области
- Поиск организаций по видам деятельности с учетом иерархии
- Пагинацию для списковых эндпоинтов

## 🛠 Технологии

- **Python 3.13**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — ORM
- **PostgreSQL + PostGIS** — геоданные
- **Dishka** — dependency injection
- **Pydantic** — валидация данных
- **Alembic** — миграции
- **Docker** — контейнеризация
- **pytest** — тестирование
- **ruff** — линтер и форматтер
- **pre-commit** — хуки git

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Make (опционально)

### Запуск
```bash
# Клонировать репозиторий
git clone git@github.com:knriia/geo_catalog_api.git
cd geo_catalog_api

# Скопировать переменные окружения
cp .env.example .env
```

#### Если установлен Make можно воспользоваться командами (рекомендуется), если нет ниже приведены обычные команды

#### С Make
```bash
# Собрать образы
make build

# Запустить проект
make up

# Заполнить базу тестовыми данными
make seed

# Запустить тесты
make test

# Все доступные команды описаны в Makefile или можно выполнить команду:
make help
```

#### Без Make
```bash
# Собрать и запустить проект
docker compose up -d --build

# Заполнить базу тестовыми данными
docker compose exec app python -m scripts.seed

# Запустить тесты
docker compose exec app pytest

# Остановить проект
docker compose down

# Полная очистка (с удалением данных)
docker compose down -v
```

### Особенности запуска

При старте проекта автоматически:
- Поднимается база данных PostgreSQL с PostGIS
- Накатываются миграции через Alembic
- Запускается приложение FastAPI

Если миграции не накатились автоматически, выполните вручную:

#### С Make
```
make migrate
```
#### Без Make
```
docker compose run --rm migrator
```

### Доступ к API
После запуска API доступно:
- API: http://localhost:8000
- Документация: http://localhost:8000/docs

### Авторизация в Swagger
Для тестирования эндпоинтов через Swagger необходимо:

- Нажать кнопку Authorize
- Ввести API-ключ из .env (переменная STATIC_API_KEY)
- Нажать Authorize

## 📖 Основные эндпоинты

| Ресурс | Эндпоинт | Описание |
|--------|----------|----------|
| **Деятельности** | `POST /activities/` | Создание деятельности |
| | `GET /activities/` | Список деятельностей (пагинация) |
| | `GET /activities/tree/{id}` | Ветка дерева деятельности |
| **Здания** | `POST /buildings/` | Создание здания |
| | `GET /buildings/` | Список зданий (пагинация) |
| | `GET /buildings/{id}` | Здание по ID |
| | `GET /buildings/search/radius` | Поиск зданий в радиусе |
| | `GET /buildings/search/bounds` | Поиск зданий в прямоугольнике |
| **Организации** | `POST /organizations/` | Создание организации |
| | `GET /organizations/` | Список организаций (пагинация) |
| | `GET /organizations/{id}` | Организация по ID |
| | `GET /organizations/search/name` | Поиск по названию |
| | `GET /organizations/search/activity/{id}` | Поиск по виду деятельности |
| | `GET /organizations/search/radius` | Поиск в радиусе |
| | `GET /organizations/search/bounds` | Поиск в прямоугольнике |
| | `GET /organizations/building/{id}` | Организации в здании |

# В корне проекта лежит файл со структурой всего проекта "structure.md"
