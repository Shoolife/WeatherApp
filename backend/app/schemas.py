from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CitySuggestion(BaseModel):
    name: str = Field(..., description="Full display name of the city")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")


class HourlyForecast(BaseModel):
    time: datetime = Field(..., description="Timestamp of the forecast hour")
    temperature: float = Field(..., description="Temperature in °C")
    weathercode: int = Field(..., description="Open-Meteo weather code")


class WeatherResponse(BaseModel):
    city: str = Field(..., description="City name as requested")
    latitude: float = Field(..., description="Latitude of the city")
    longitude: float = Field(..., description="Longitude of the city")
    temperature: Optional[float] = Field(None, description="Current temperature in °C")
    wind_speed: Optional[float] = Field(None, description="Current wind speed in m/s")
    timestamp: Optional[datetime] = Field(None, description="Time of current weather measurement")
    hourly: List[HourlyForecast] = Field(..., description="Hourly forecast data")


class StatsResponse(BaseModel):
    city: str = Field(..., description="City name")
    count: int = Field(..., description="Number of times the city was requested")
