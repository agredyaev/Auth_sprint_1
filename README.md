# Project Overview
---
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-3.2-blue)
![Redis](https://img.shields.io/badge/Redis-5.0.4-red)
![Pytest](https://img.shields.io/badge/pytest-7.7.7-blue)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.12-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.1-green)
![Docker](https://img.shields.io/badge/Docker-20.10-blue)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

This project involves the development of an authentication service. The implementation includes business logic and endpoints for user management, such as registration, role assignment/verification, and password changes. Below is a structured and concise overview of the key features:

## User Management
- **Registration**: Endpoints for new user registration.
- **Role Assignment/Verification**: Assign roles to users and verify their roles.
- **Password Change**: Allow users to change their passwords.

## Authentication
- **Login**: Users can log in and receive tokens for access.
- **Logout**: Users can log out, and their tokens will be added to a blacklist to prevent further use.
- **Token Refresh**: Refresh access tokens using refresh tokens.
- **Login/Logout History**: View the login and logout history of users.

## Role Management
- **Create Roles**: Endpoints to create new roles.
- **Update Roles**: Endpoints to update existing roles.
- **Delete Roles**: Endpoints to delete roles.

## Authorization
- **Access Control**: A system to check user permissions for accessing specific endpoints.

## Getting Started
---
Instructions to set up the project locally.

```bash
# Install Poetry if it's not already installed
# https://python-poetry.org/docs/#installation
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository 
https://github.com/agredyaev/Auth_sprint_1.git
 
# Navigate to the project directory
cd Auth_sprint_1

# Create .env file
cp .env.example .env

# Deploy API service and run tests with Docker Compose
make compose-up