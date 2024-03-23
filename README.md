
# Project Overivew

---
This project encompasses two main components:

* Docker Compose Setup: Configuration for Nginx, Docker, and Django to streamline DevOps practices. This setup ensures all system components—Django, Nginx, and PostgreSQL—are launched using docker-compose, enhancing the service's DevOps aspect.

* Django API Development: Implementation of an API providing movie information, including paginated movie listings and details for individual movies by ID.

## Deployment Steps

---

* Docker Setup: Write a Dockerfile for Django and configure Nginx as the reverse proxy. Ensure Nginx version is hidden for security and static files are served through Nginx to reduce load on Django.

* Static Files: Configure Nginx to bypass try_files for admin routes, serving static files directly to optimize performance.

## Getting Started

---
Instructions to set up the project locally.

```bash
# Clone the repository
git clone https://yourproject.git

# Navigate to the project directory
cd your_project_name

# Deploy with Docker Compose
docker-compose up --build
```

## Running the Tests

---
Tests are included to verify API functionality. To run the tests:

```bash
poetry run pytest
```

Ensure your docker-compose environment is correctly configured before executing tests.

## License

---
This project is open source and available under the [MIT License](LICENSE).
