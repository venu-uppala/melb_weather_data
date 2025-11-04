import psycopg2
from src.weather_config import DB_CONFIG
from src.weather_logger import get_logger

logger = get_logger()
"""
    Returns postgres database connection object.
"""
def get_connection():
    return psycopg2.connect(**DB_CONFIG)
"""
    Creates weather_data table if not exists in postgres
"""
def create_weather_table():
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    device_id TEXT NOT NULL,
                    sensorlocation TEXT NOT NULL,
                    received_at TIMESTAMP NOT NULL,
                    airtemperature REAL,
                    relativehumidity REAL,
                    PRIMARY KEY (device_id, received_at)
                );
            """)
            logger.info("Created weather_data table")
    except Exception as e:
        logger.critical(f"Failed to create weather_data table: {e}")
"""
    Inserts weather data records into weather_data postgres table
"""
def insert_weather_data(records):
    # Create weather table if not exists
    create_weather_table()

    query = """
        INSERT INTO weather_data (device_id, sensorlocation, received_at, airtemperature, relativehumidity)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """

    values = [
        (
            r["device_id"],
            r["sensorlocation"],
            r["received_at"],
            r["airtemperature"],
            r["relativehumidity"]
        )
        for r in records
    ]

    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.executemany(query, values)
            logger.info(f"Inserted {len(values)} records into weather_data")
    except Exception as e:
        logger.critical(f"Database insert failed: {e}")

