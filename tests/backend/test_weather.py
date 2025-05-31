import pytest
from httpx import AsyncClient
from backend.app.main import app
import backend.app.services.weather_service as weather_service

@pytest.mark.asyncio
async def test_get_weather_increments_and_returns(monkeypatch):
    """
    Тестирует, что при получении погоды:
      - вызываются geocode_city и fetch_weather,
      - данные возвращаются в ожидаемом формате,
      - статистика запросов (/api/stats) корректно подсчитывает повторные вызовы (регистр приводится к нижнему).
    """
    async def mock_geocode(city: str):
        return 10.0, 20.0

    async def mock_fetch(lat, lon):
        return {
            "hourly": {
                "time": ["2025-06-01T00:00:00", "2025-06-01T01:00:00"],
                "temperature_2m": [15.0, 16.0],
                "weathercode": [0, 1]
            }
        }

    monkeypatch.setattr(weather_service, "geocode_city", mock_geocode)
    monkeypatch.setattr(weather_service, "fetch_weather", mock_fetch)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r1 = await ac.get("/api/weather?city=CityA")
        assert r1.status_code == 200
        data1 = r1.json()
        assert data1["city"] == "CityA"
        assert isinstance(data1["latitude"], float)
        assert isinstance(data1["longitude"], float)
        assert len(data1["hourly"]) == 2
        assert data1["hourly"][0]["temperature"] == 15.0

        r2 = await ac.get("/api/weather?city=CityB")
        assert r2.status_code == 200
        data2 = r2.json()
        assert data2["city"] == "CityB"

        r3 = await ac.get("/api/weather?city=CityA")
        assert r3.status_code == 200

        stats_resp = await ac.get("/api/stats")
        assert stats_resp.status_code == 200
        stats_data = stats_resp.json()
        assert stats_data[0]["city"] == "citya" and stats_data[0]["count"] == 2
        assert stats_data[1]["city"] == "cityb" and stats_data[1]["count"] == 1