.PHONY: help up down logs build restart clean migrate

# Colors
YELLOW := \033[1;33m
GREEN := \033[1;32m
NC := \033[0m

help: ## Show this help
	@echo "$(GREEN)Flower Shop - Full Stack Commands$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

# ============ Development ============

up: ## Start all services (dev mode)
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## View all logs
	docker compose logs -f

logs-api: ## View API logs
	docker compose logs -f api

logs-frontend: ## View frontend logs
	docker compose logs -f frontend

build: ## Build all images
	docker compose build

rebuild: ## Rebuild and restart all services
	docker compose up -d --build

restart: ## Restart all services
	docker compose restart

# ============ Database ============

migrate: ## Run Django migrations
	docker compose exec api python manage.py migrate

makemigrations: ## Create Django migrations
	docker compose exec api python manage.py makemigrations

createsuperuser: ## Create Django superuser
	docker compose exec api python manage.py createsuperuser

shell: ## Open Django shell
	docker compose exec api python manage.py shell

dbshell: ## Open database shell
	docker compose exec postgres psql -U postgres -d flower_shop

# ============ Production ============

up-prod: ## Start production services
	docker compose -f docker-compose.prod.yml up -d

down-prod: ## Stop production services
	docker compose -f docker-compose.prod.yml down

build-prod: ## Build production images
	docker compose -f docker-compose.prod.yml build

# ============ Utilities ============

clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all

ps: ## Show running containers
	docker compose ps

reset-db: ## Reset database (DANGEROUS!)
	docker compose down -v
	docker compose up -d postgres
	@echo "Waiting for postgres..."
	@sleep 5
	docker compose up -d api
	@sleep 3
	docker compose exec api python manage.py migrate
