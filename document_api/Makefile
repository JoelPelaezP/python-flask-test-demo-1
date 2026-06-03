DOCKER_FILES := -f docker-compose.yml
DOCKER_DEBUG_FILES := -f docker-compose.debug.yml
API_SERVICE_NAME := dotnet-document-generator
DOCKER_RUN_CMD = docker compose $(DOCKER_FILES) run --rm $(API_SERVICE_NAME)

local-setup:
	pip install -r requirements.txt

build: build-api

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