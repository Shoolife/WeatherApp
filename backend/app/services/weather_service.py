import httpx
from fastapi import HTTPException
from typing import Tuple
from datetime import datetime
from sqlmodel import Session

from app.crud import StatsCRUD
from app.schemas import WeatherResponse, HourlyForecast

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


async def geocode_city(city: str) -> Tuple[float, float]:
    """
    Определяет координаты города по названию через Open-Meteo Geocoding API.
    """
    params = {"name": city, "count": 1}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(GEOCODING_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Geocoding service error")

    results = response.json().get("results")
    if not results:
        raise HTTPException(status_code=404, detail="City not found")

    location = results[0]
    return float(location["latitude"]), float(location["longitude"])


async def fetch_weather_data(lat: float, lon: float) -> dict:
    """
    Получает данные о погоде через Open-Meteo Forecast API.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,cloudcover",
        "forecast_days": 1,
        "timezone": "auto",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(WEATHER_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Weather service error")

    return response.json()


async def get_weather_for_city(session: Session, city: str) -> WeatherResponse:
    """
    Возвращает структурированные погодные данные по городу.
    Также записывает город в статистику.
    """
    lat, lon = await geocode_city(city)

    data = await fetch_weather_data(lat, lon)

    StatsCRUD.increment_city(session, city)

    hourly_data = data.get("hourly", {})
    times = hourly_data.get("time", [])
    temps = hourly_data.get("temperature_2m", [])
    clouds = hourly_data.get("cloudcover", [])

    hourly: list[HourlyForecast] = []
    for time_str, temp, cloud in zip(times, temps, clouds):
        dt = datetime.fromisoformat(time_str)
        hourly.append(HourlyForecast(time=dt, temperature=temp, weathercode=cloud))

    current = data.get("current_weather", {})
    temperature = current.get("temperature")
    wind_speed = current.get("windspeed")
    timestamp_str = current.get("time")
    try:
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None
    except Exception:
        timestamp = None

    return WeatherResponse(
        city=city,
        latitude=lat,
        longitude=lon,
        temperature=temperature,
        wind_speed=wind_speed,
        timestamp=timestamp,
        hourly=hourly
    )
