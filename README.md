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

## Sprint Update
---
In this sprint, we enhanced the ETL process to handle additional models, prepared a process to populate the database with test data for further development of tests for the FastAPI service, and added the FastAPI service.

## Getting Started
---
Instructions to set up the project locally.

```bash
# Deploy with Docker Compose
make compose-up
