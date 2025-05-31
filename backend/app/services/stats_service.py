from sqlmodel import Session
from datetime import datetime
from app.crud import StatsCRUD
from app.schemas import StatsResponse

"""
Модуль services.stats_service: бизнес-логика для обработки статистических данных.
"""

def record_search(session: Session, city: str) -> None:
    """
    Увеличивает счётчик запросов к городу (вне зависимости от регистра)
    и обновляет время последнего запроса.
    """
    record = StatsCRUD.increment_city(session, city)
    if hasattr(record, "last_searched"):
        record.last_searched = datetime.utcnow()
        session.add(record)
        session.commit()
        session.refresh(record)


def get_stats(session: Session) -> list[StatsResponse]:
    """
    Возвращает статистику по всем городам: имя города и количество запросов.
    """
    records = StatsCRUD.list_stats(session)
    return [
        StatsResponse(city=r.city, count=r.count)
        for r in records
    ]
