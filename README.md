
# Project Overivew
---
This ETL (Extract, Transform, Load) project is designed to automate the data handling process by extracting data from PostgreSQL databases, applying necessary transformations, and then loading the processed data into Elasticsearch for enhanced search and analysis capabilities. The system aims to facilitate real-time data integration and analytics by leveraging PostgreSQL's robust data management features along with Elasticsearch's powerful search functionalities.

Key Components:
* Extractor: Connects to PostgreSQL to retrieve data based on specified criteria.
* Transformer: Processes data to fit the target schema, which includes cleaning, normalizing, and enriching the data.
* Loader: Loads the transformed data into Elasticsearch, ensuring that the data is indexed correctly for optimal search performance.

## Getting Started

---
Instructions to set up the project locally.

```bash
# Clone the repository
git clone https://github.com/agredyaev/new_admin_panel_sprint_3.git

# Navigate to the project directory
cd new_admin_panel_sprint_3

# Deploy with Docker Compose
docker-compose up --build
```
The database is populated from a backup during initialization.

## Running the Tests

---

Tests are included to verify the database and elasticsearch integration.

```bash
poetry run pytest
```

Ensure docker-compose environment is correctly configured before executing tests.

## License

---
This project is open source and available under the [MIT License](LICENSE).
