import pytest
from httpx import AsyncClient
from backend.app.main import app

"""Модуль тестов test_stats: проверка функциональности статистики."""

@pytest.mark.asyncio
async def test_stats_empty_and_after_search(monkeypatch):
    """
    Если до запросов статистика пуста — отдается пустой список.
    После одного запроса /api/weather?city=Zeta статистика содержит один элемент:
    city == "zeta", count == 1.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp_initial = await ac.get("/api/stats")
        assert resp_initial.status_code == 200
        assert resp_initial.json() == []

        import backend.app.services.weather_service as weather_mod

        async def fake_geocode(city: str):
            return 0.0, 0.0

        async def fake_fetch(lat: float, lon: float):
            return {
                "hourly": {
                    "time": [],
                    "temperature_2m": [],
                    "weathercode": []
                }
            }

        monkeypatch.setattr(weather_mod, "geocode_city", fake_geocode)
        monkeypatch.setattr(weather_mod, "fetch_weather", fake_fetch)

        resp_weather = await ac.get("/api/weather?city=Zeta")
        assert resp_weather.status_code == 200

        resp_stats = await ac.get("/api/stats")
        assert resp_stats.status_code == 200
        stats_data = resp_stats.json()
        assert len(stats_data) == 1
        assert stats_data[0]["city"] == "zeta"
        assert stats_data[0]["count"] == 1