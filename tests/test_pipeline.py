from src.pipeline import run_weather_data_pipeline

def test_pipeline(mocker):
    mock_data = [
                        {
                        "device_id": "S1",
                        "sensorlocation": "Melbourne",
                        "received_at": "2025-11-01T10:00:00",
                        "airtemperature": 22.5,
                        "relativehumidity": 55.0
                        }
                ]
                
    mocker.patch("src.pipeline.fetch_weather_data", return_value=mock_data)
    mock_insert = mocker.patch("src.pipeline.insert_weather_data")
    run_weather_data_pipeline()
    mock_insert.assert_called_once_with(mock_data)
