from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import weather, stats, cities
from app.database import init_db

"""Главный модуль приложения: создание FastAPI-инстанса и регистрация маршрутов."""

app = FastAPI(
    title="WeatherApp",
    description="Приложение для получения прогноза погоды по городу и ведения статистики запросов.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """
    Инициализация базы данных при старте приложения:
    - создаёт таблицы (если не существуют)
    - может наполнить начальными данными (если нужно)
    """
    init_db()


app.include_router(weather.router, prefix="/api", tags=["weather"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(cities.router, prefix="/api", tags=["cities"])
