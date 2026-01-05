.PHONY: up down logs ps rebuild api-shell worker-shell db-shell migrate

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

rebuild:
	docker compose build --no-cache

api-shell:
	docker exec -it aiapply-api sh

worker-shell:
	docker exec -it aiapply-worker sh

db-shell:
	docker exec -it aiapply-db psql -U aiapply -d ai_apply

migrate:
	docker exec -it aiapply-api alembic upgrade head
