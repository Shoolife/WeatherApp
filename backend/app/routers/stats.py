from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.services.stats_service import get_stats
from app.schemas import StatsResponse

router = APIRouter(
    tags=["Stats"]
)

@router.get("/stats", response_model=List[StatsResponse])
def stats_list(session: Session = Depends(get_session)) -> List[StatsResponse]:
    """
    Возвращает статистику по городам: сколько раз был запрошен прогноз.
    """
    try:
        records = get_stats(session)
        return [
            StatsResponse(city=rec.city, count=rec.count)
            for rec in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
