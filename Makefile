DOCKER_FILES := -f docker-compose.yml
DOCKER_DEBUG_FILES := -f docker-compose.debug.yml
DB_SERVICE_NAME := python-flask-db
API_SERVICE_NAME := python-flask-api
ALEMBIC_CONFIG_FILE := ./database/migrations/alembic.ini
ALEMBIC_CMD := alembic --config $(ALEMBIC_CONFIG_FILE)
DOCKER_RUN_CMD = docker compose $(DOCKER_FILES) run --rm $(API_SERVICE_NAME)

local-setup:
	pip install -r requirements.txt

build: build-api build-db

build-api:
	docker compose $(DOCKER_FILES) build

build-start-force:
	docker compose $(DOCKER_FILES) up --build --force-recreate --no-deps

start:
	docker compose $(DOCKER_FILES) up -d

start-logs:
	docker compose $(DOCKER_FILES) up

start-debug:
	docker compose $(DOCKER_FILES) $(DOCKER_DEBUG_FILES) up

stop:
	docker compose down

build-db: start-db db-upgrade

start-db:
	docker compose $(DOCKER_FILES) up -d --wait $(DB_SERVICE_NAME)

db-upgrade:
	$(DOCKER_RUN_CMD) $(ALEMBIC_CMD) upgrade head

db-migrate:
	$(DOCKER_RUN_CMD) $(ALEMBIC_CMD) revision --autogenerate -m "$(MSG)"

format-check:
	$(DOCKER_RUN_CMD) isort . --check
	$(DOCKER_RUN_CMD) black . --check

format:
	$(DOCKER_RUN_CMD) isort . --atomic
	$(DOCKER_RUN_CMD) black .

test:
	$(DOCKER_RUN_CMD) pytest $(args)

task-check-weather:
	$(DOCKER_RUN_CMD) python tasks/__init__.py