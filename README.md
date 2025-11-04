# 🌤 Melbourne Weather data Pipeline

A modular Python pipeline that fetches weather data from an external API(https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/microclimate-sensors-data/records), stores it in a PostgreSQL database, and ensures robust logging, schema creation, and batch inserts.

---
## 🧭 Approach
The `Melbourne Weather data Pipeline` was designed as a modular, production-grade pipeline to ingest, store, and validate weather data from external sources.The approach emphasizes scalability, testability, and team onboarding.

### 🔨 Key Design Principles
- **Modular architecture**: All logic is split into reusable components (src/weather_api.py, src/weather_database.py, etc.) for clarity and maintainability.
- **Automated schema creation**: The pipeline ensures the weather_data table is created if it doesn't exist, using idempotent SQL.
- **Batch inserts with conflict handling**: Weather records are inserted using executemany() with ON CONFLICT DO NOTHING to avoid duplicates.
- **Robust logging**: A centralized logger (weather_logger.py) tracks all operations, errors, and critical events.
- **Test-first development**: Pytest-based unit tests validate both table creation and data insertion logic using mocks.
- **Docker-ready**: A docker-compose.yml file provisions a local PostgreSQL instance for development and testing.
- **Visual onboarding**: A project structure diagram and tree output are included to help new developers understand the layout quickly.
### 📈 Workflow Summary
- Weather data is fetched via API (e.g., paginated JSON using `limit` and `offset` api parameters as one API call gives 100 records maximum hence used `offset` parameter to paginate 100 records at a time to reach to 1000 records, also used `where` parameter to filter records where `senosorlocation` is null to provide quality data to Analysts).
- Records are validated and transformed into insertable tuples.
- The database table is created if missing.
- All records are batch-inserted with conflict protection.
- Logs are written for every major step.
- Tests ensure correctness and reproducibility.

---
## 📌 Assumptions
The following assumptions were made during the design and implementation of the pipeline:
- 🗃️ **Database Availability**: A PostgreSQL instance is running and accessible with credentials provided via `weather_config.py`. The database is expected to support standard SQL features like ON CONFLICT DO NOTHING.
- 📦 **Data Format**: Weather data is received as a list of dictionaries (JSON-like), each containing:
    - device_id: string
    - sensorlocation: string
    - received_at: timestamp (ISO 8601 format)
    - airtemperature: float
    - relativehumidity: float
- 🧪 **Data Integrity**: Incoming records are assumed to be pre-validated. The pipeline does not perform schema validation or type coercion beyond basic insert formatting.
- 🔁 **Idempotency**: Duplicate records (same device_id and received_at) are safely ignored using ON CONFLICT DO NOTHING.
- 🧱 **Table Schema Stability**: The schema for weather_data is fixed and not expected to change frequently. If schema evolution is needed, migrations should be handled manually or via Alembic.
- 🧪 **Testing Environment**: Unit tests use mocks for database connections and do not require a live PostgreSQL instance. Integration tests are assumed to be run separately.
- 🐳 **Local Development**: Docker is used to provision PostgreSQL locally via docker-compose.yml. Developers are expected to have Docker installed.
- 🔐 **Secrets Management**: Credentials are stored in `weather_config.py` for simplicity. In production, secrets should be managed via environment variables or secret managers.
- 📁 **Project Structure**: All source code resides in the src/ folder, and tests in tests/. This structure is assumed by test runners and documentation tools.
- 📄 **Logging**: Logging is centralized via `weather_logger.py` and assumes a console-based output. No external logging service is integrated yet.
- 🚫 **Performance Testing**: Load testing, stress testing, and benchmarking are explicitly out of scope for this version of the project. The pipeline is optimized for correctness and modularity, not throughput and it only ingests 1000 records which can be changed using RECORD_LIMIT configuration in `weather_config.py`, please refer API documentation for offset limits.


---

## 🧱 Project Structure
<pre>melb_weather_data
├── Dockerfile
├── Makefile
├── README.md
├── docker-compose.yml
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── pipeline.py
│   ├── weather_api.py
│   ├── weather_config.py
│   ├── weather_database.py
│   └── weather_logger.py
└── tests
    ├── __init__.py
    ├── test_pipeline.py
    ├── test_weather_api.py
    └── test_weather_database.py
</pre>
---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/venu-uppala/melb_weather_data.git
cd melb_weather_data
```

### 2. Setup virtual environment and Install dependencies
```bash
make setup
make activate
```

### 3. Configure database
Edit src/weather_config.py
```Python
DB_CONFIG = {
        "dbname": "your_db",
        "user": "your_user",
        "password": "your_password",
        "host": "localhost",
        "port": "5432"
}
```
🛠 Usage
### Run the weather data pipeline
```Bash
python3 -m src.pipeline
```
This will fail if postgress db is not setup and configure properly, let us run this code using docker. Here docker-compose is used to setup postgres db on the fly, creates weather_data table and loads 1000 records into the table.
```Bash
docker-compose up --build
```
Go to `Exec` tab of postgres docker container to execute below listed commands to see the ingested data or use GUI tool like Dbeaver to connect to the postgres db.
```Bash
# To connect to the postgres db created on the fly using docker-compose
psql -U postgres -d melb_weather_data
# count query
select count(1) from weather_data;
# Analyst query
SELECT sensorlocation, AVG(airtemperature) AS avg_temp, AVG(relativehumidity) AS avg_humidity
FROM weather_data
GROUP BY sensorlocation
ORDER BY avg_temp DESC;
```
Below screenshot shows the out of the above mentioned commands.

<img width="926" height="469" alt="image" src="https://github.com/user-attachments/assets/8655bbc0-256f-4844-b420-cc798b654b3f" />

🧪 Testing
Run all tests with:
```Bash
make test
```
Includes:
- ✅ test_fetch_exact_record_limit
- ✅ test_insert_weather_data_executes_batch_insert
- ✅ test_create_weather_table_executes_sql_and_commits


📋 Table Schema
```Sql
CREATE TABLE IF NOT EXISTS weather_data (
    device_id TEXT NOT NULL,
    sensorlocation TEXT NOT NULL,
    received_at TIMESTAMP NOT NULL,
    airtemperature REAL,
    relativehumidity REAL,
    PRIMARY KEY (device_id, received_at)
);
```
### Query for Analysts
```Sql
SELECT sensorlocation, AVG(airtemperature) AS avg_temp, AVG(relativehumidity) AS avg_humidity
FROM weather_data
GROUP BY sensorlocation
ORDER BY avg_temp DESC;
```

📚 Logging:
Logs are configured via weather_logger.py and include:
- logger.info() for successful operations
- logger.error() for insert failures
- logger.critical() for connection or transaction issues

🧠 Author
Built by Venu Gopal Uppala — Big Data Lead Engineer passionate about scalable data platforms, automation, and team enablement.

📄 License
MIT License — feel free to use, modify, and contribute.
