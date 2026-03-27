DC = docker compose
APP_CONTAINER = app
MIGRATOR_CONTAINER = migrator

ARGS = $(filter-out $@,$(MAKECMDGOALS))
%:
	@:

.PHONY: help build up down restart logs migrate revision shell ps

help:
	@echo "Команды для управления проектом:"
	@echo "  make build       - Собрать образы"
	@echo "  make up          - Запустить проект (в фоне)"
	@echo "  make down        - Остановить и удалить контейнеры"
	@echo "  make down-v      - Остановить и удалить контейнеры и volume"
	@echo "  make restart     - Перезапустить проект"
	@echo "  make logs        - Просмотр логов"
	@echo "  make ps          - Статус контейнеров"
	@echo "  make revision    - Создать новую миграцию (usage: make revision 'name')"
	@echo "  make migrate     - Накатить миграции вручную"
	@echo "  make seed        - Запуск скрипта для наполнения базы данными"
	@echo "  make test        - Запустить все тесты"
	@echo "  make test-v      - Запустить тесты с подробным выводом (verbose)"

build:
	$(DC) build $(ARGS)

up:
	$(DC) up -d $(ARGS)

down:
	$(DC) down $(ARGS)

down-v:
	$(DC) down -v $(ARGS)

restart:
	$(DC) restart $(ARGS)

logs:
	$(DC) logs -f $(ARGS)

ps:
	$(DC) ps

revision:
	$(DC) run --rm $(APP_CONTAINER) alembic revision --autogenerate -m "$(ARGS)"

migrate:
	$(DC) run --rm $(MIGRATOR_CONTAINER)

seed:
	$(DC) exec $(APP_CONTAINER) python -m scripts.seed

test:
	$(DC) exec $(APP_CONTAINER) pytest

test-v:
	$(DC) exec $(APP_CONTAINER) pytest -vv -s
