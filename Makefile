.PHONY: dev build down logs migrate train setup-env

dev:
	docker-compose up -d

build:
	docker-compose build

down:
	docker-compose down -v

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend alembic upgrade head

train:
	docker-compose exec backend python -m app.ml.train

setup-env:
	cp .env.example .env
	@echo "Created .env file. Please edit and add your API keys."
