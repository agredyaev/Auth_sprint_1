# Project Overview
---
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-3.2-blue)
![Redis](https://img.shields.io/badge/Redis-5.0.4-red)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.12-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.1-green)
![Docker](https://img.shields.io/badge/Docker-20.10-blue)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

Key Components:
* **Fake data generator**: Generates fake data for the application and loads it into the database.
* **Extractor**: Connects to PostgreSQL to retrieve data based on specified criteria.
* **Transformer**: Processes data to fit the target schema, which includes cleaning, normalizing, and enriching the data.
* **Loader**: Loads the transformed data into Elasticsearch, ensuring that the data is indexed correctly for optimal search performance.
* **API**: Provides a RESTful API for the application, allowing for data retrieval, filtering, and aggregation.
* **Tests**: Functional and performance tests to ensure the API is working as expected.

## Sprint Update
---
In this sprint, we are working on 
    * Refactoring the API implementation regarding SOLID principles.
    * Adding functional tests to ensure the API is working as expected.

## Getting Started
---
Instructions to set up the project locally.

```bash
# Install Poetry if it's not already installed
# https://python-poetry.org/docs/#installation
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository 
https://github.com/agredyaev/Async_API_sprint_2.git
 
# Navigate to the project directory
cd Async_API_sprint_2

# Create .env file
cp .env.example .env

# Deploy API service and run tests with Docker Compose
make compose-up