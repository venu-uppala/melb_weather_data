# 🌤 Melbourne Weather data Pipeline

A modular Python pipeline that fetches weather data from an external API, stores it in a PostgreSQL database, and ensures robust logging, schema creation, and batch inserts.

---

## 🚀 Features

- ✅ Fetches paginated weather data from external APIs
- ✅ Filters weather data where location is null to provide quality data to analysts
- ✅ Creates `weather_data` table on the fly (idempotent)
- ✅ Inserts records using efficient batch inserts (`executemany`)
- ✅ Skips duplicates with `ON CONFLICT DO NOTHING`
- ✅ Modular logging and configuration
- ✅ Pytest coverage for table creation and data insertion

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
Go to `exec` tab of postgres docker container to execute below listed commands to see the ingested data or use GUI tool like Dbeaver to connect to the postgres db.
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
