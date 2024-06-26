# Docker Compose commands
compose-up:
	docker compose up --build

compose-down:
	docker compose down

# Clean up Docker Compose services, images, volumes, and caches
clean:
	docker compose down -v
	docker system prune -af --volumes
	docker network rm $(docker network ls -q)
	docker rmi -f $(docker images -q)
	docker rm -f $(docker ps -a -q)


# Format Python code
fmt:
	ruff format .

lint-mp:
	mypy .
lint-rf:
	ruff check --fix .


# Help command
help:
	@echo "Makefile commands:"
	@echo "  compose-up       Start the Docker Compose services"
	@echo "  compose-down     Stop the Docker Compose services"
	@echo "  clean            Stop and remove all Docker Compose services, images, volumes, and caches"
	@echo "  fmt              Format Python code using Ruff"
	@echo "  lint-mp              Lint Python code using Mypy"
	@echo "  lint-rf             Lint Python code using Ruff"
	@echo "  help             Show this help message"

.PHONY: compose-up compose-down clean help fmt lint-rf lint-mp