import requests
from src.weather_config import API_URL, RECORD_LIMIT
from src.weather_logger import get_logger

logger = get_logger()

def fetch_weather_data():
    all_data = []
    page_size = 100
    offset = 0

    while len(all_data) < RECORD_LIMIT:
        response = requests.get(
            f"{API_URL}?where=sensorlocation is not null&limit={page_size}&offset={offset}"
        )
        batch = response.json()["results"]

        if not batch:
            print("No more data available from API.")
            break

        all_data.extend(batch)
        offset += page_size
        
    return all_data[:RECORD_LIMIT]
