from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.services.weather_service import get_weather_for_city
from app.services.stats_service import record_search
from app.schemas import WeatherResponse

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/", response_model=WeatherResponse)
async def get_weather(
    city: str = Query(..., min_length=1, description="Название города"),
    session: Session = Depends(get_session)
):
    """
    Получаем прогноз погоды и сохраняем статистику запроса.
    """
    try:
        weather = await get_weather_for_city(session, city)
        return weather

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))