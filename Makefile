.PHONY: help up down build logs migrate seed test lint

FLUTTER ?= $(HOME)/flutter/bin/flutter

help:
	@echo "My Fitness Buddy - Available commands:"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make build     - Build all Docker images"
	@echo "  make logs      - Tail backend logs"
	@echo "  make migrate   - Run Alembic migrations"
	@echo "  make seed      - Seed database with sample data"
	@echo "  make test      - Run backend tests"
	@echo "  make lint      - Run backend linters"
	@echo "  make mobile-test    - Run Flutter tests"
	@echo "  make mobile-run     - Run Flutter app (Linux)"
	@echo "  make mobile-analyze - Run Flutter analyzer"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f backend

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python scripts/seed_data.py

test:
	docker compose exec backend pytest tests/ -v

test-cov:
	docker compose exec backend pytest tests/ -v --cov=app --cov-report=term-missing

lint:
	docker compose exec backend ruff check app tests
	docker compose exec backend mypy app

shell:
	docker compose exec backend bash

admin-dev:
	cd admin && npm run dev

admin-build:
	cd admin && npm run build

admin-test:
	cd admin && npm test

mobile-test:
	@test -x "$(FLUTTER)" || (echo "Flutter not found at $(FLUTTER). Install: git clone https://github.com/flutter/flutter.git -b stable $(HOME)/flutter"; exit 1)
	cd mobile && "$(FLUTTER)" test

mobile-run:
	@test -x "$(FLUTTER)" || (echo "Flutter not found at $(FLUTTER)"; exit 1)
	cd mobile && "$(FLUTTER)" run -d chrome --dart-define=API_BASE_URL=http://localhost:8000/api/v1

mobile-analyze:
	@test -x "$(FLUTTER)" || (echo "Flutter not found at $(FLUTTER)"; exit 1)
	cd mobile && "$(FLUTTER)" analyze
