from unittest.mock import MagicMock, patch
from src.weather_database import create_weather_table,insert_weather_data

def test_create_weather_table_executes_sql_and_commits():
    with patch("src.weather_database.get_connection") as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        create_weather_table()

        # Assert the CREATE TABLE SQL was executed
        executed_sqls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        assert any("CREATE TABLE IF NOT EXISTS weather_data" in sql for sql in executed_sqls)


def test_insert_weather_data_executes_batch_insert():
    sample_records = [
        {
            "device_id": "sensor_001",
            "sensorlocation": "Melbourne",
            "received_at": "2025-11-04 08:00:00",
            "airtemperature": 22.5,
            "relativehumidity": 55.2
        },
        {
            "device_id": "sensor_002",
            "sensorlocation": "Sydney",
            "received_at": "2025-11-04 08:05:00",
            "airtemperature": 23.1,
            "relativehumidity": 58.0
        }
    ]

    with patch("src.weather_database.get_connection") as mock_get_conn, \
         patch("src.weather_database.create_weather_table") as mock_create_table:

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        insert_weather_data(sample_records)

        # Assert table creation was triggered
        mock_create_table.assert_called_once()

        # Assert executemany was called with correct SQL and values
        assert mock_cursor.executemany.call_count == 1
        args, _ = mock_cursor.executemany.call_args
        assert "INSERT INTO weather_data" in args[0]
        assert len(args[1]) == 2  # two records
        assert args[1][0][0] == "sensor_001"
        assert args[1][1][0] == "sensor_002"
