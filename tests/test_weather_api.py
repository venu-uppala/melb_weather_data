import pytest
from unittest.mock import patch, MagicMock
from src.weather_api import fetch_weather_data

# Constants to patch
API_URL = "https://example.com/api"
RECORD_LIMIT = 300

@pytest.fixture(autouse=True)
def patch_constants(monkeypatch):
    monkeypatch.setattr("src.weather_api.API_URL", API_URL)
    monkeypatch.setattr("src.weather_api.RECORD_LIMIT", RECORD_LIMIT)

def generate_batch(start, size):
    return [{"device_id": i, "airtemperature": 20 + i} for i in range(start, start + size)]

@patch("src.weather_api.requests.get")
def test_fetch_exact_record_limit(mock_get):
    # Simulate 3 pages of 100 records
    mock_get.side_effect = [
        MagicMock(json=lambda: {"results": generate_batch(0, 100)}),
        MagicMock(json=lambda: {"results": generate_batch(100, 100)}),
        MagicMock(json=lambda: {"results": generate_batch(200, 100)})
    ]
    data = fetch_weather_data()
    print(data)
    assert len(data) == 300
    assert data[0]["device_id"] == 0
    assert data[-1]["device_id"] == 299


@patch("src.weather_api.requests.get")
def test_fetch_less_than_record_limit(mock_get):
    # Simulate 2 full pages and one empty
    mock_get.side_effect = [
        MagicMock(json=lambda: {"results": generate_batch(0, 100)}),
        MagicMock(json=lambda: {"results": generate_batch(100, 100)}),
        MagicMock(json=lambda: {"results": []}),
    ]

    data = fetch_weather_data()
    assert len(data) == 200

@patch("src.weather_api.requests.get")
def test_fetch_empty_first_batch(mock_get):
    mock_get.return_value = MagicMock(json=lambda: {"results": []})

    data = fetch_weather_data()
    assert data == []

@patch("src.weather_api.requests.get")
def test_fetch_partial_final_batch(mock_get):
    # Simulate 2 full pages and one partial
    mock_get.side_effect = [
        MagicMock(json=lambda: {"results": generate_batch(0, 100)}),
        MagicMock(json=lambda: {"results": generate_batch(100, 100)}),
        MagicMock(json=lambda: {"results": generate_batch(200, 50)}),
        MagicMock(json=lambda: {"results": []}),
    ]

    data = fetch_weather_data()
    assert len(data) == 250
