import os
# Postgress database configuration details
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "melb_weather_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres")
}
# External weather data API URL
API_URL = os.getenv("API_URL", "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/microclimate-sensors-data/records")
# Number of maximum records to fetch from the external API
RECORD_LIMIT = int(os.getenv("RECORD_LIMIT", 1000))
