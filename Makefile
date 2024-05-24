# Docker Compose commands
compose-up:
	docker compose up --build

compose-down:
	docker compose down

# Clean up Docker Compose services, images, volumes, and caches
clean:
	docker compose down -v
	docker system prune -af --volumes

# Format Python code
fmt:
	poetry run ruff format

lint:
	poetry run ruff check --fix .
	poetry run mypy .

# Help command
help:
	@echo "Makefile commands:"
	@echo "  compose-up       Start the Docker Compose services"
	@echo "  compose-down     Stop the Docker Compose services"
	@echo "  clean            Stop and remove all Docker Compose services, images, volumes, and caches"
	@echo "  fmt              Format Python code using Ruff"
	@echo "  lint             Lint Python code using Ruff"
	@echo "  help             Show this help message"

.PHONY: compose-up compose-down clean help fmt lint