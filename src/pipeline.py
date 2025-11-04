from src.weather_api import fetch_weather_data
from src.weather_database import insert_weather_data
from src.weather_logger import get_logger

logger = get_logger()
"""
Driver program to perform:
1) Fetch weather data
2) Insert weather data into a postgres table
"""
def run_weather_data_pipeline():
    logger.info("Starting Weather data pipeline...")
    data = fetch_weather_data()
    
    if not data:
        logger.warning("No data fetched. Weather data load aborted.")
        return
    insert_weather_data(data)
    logger.info("Weather data pipeline executed successfully.")

if __name__ == "__main__":
    run_weather_data_pipeline()
