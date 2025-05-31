from sqlmodel import select, Session
from sqlalchemy import func
from datetime import datetime
from app.models import CityStats  


class StatsCRUD:
    """Класс для выполнения CRUD-операций над статистикой поисков городов."""

    @staticmethod
    def increment_city(session: Session, city: str) -> CityStats:
        """
        Увеличивает счётчик статистики для указанного города (регистр не учитывается),
        обновляет время последнего поиска и возвращает запись.
        """
        city_norm = city.strip().lower()

        stmt = select(CityStats).where(func.lower(CityStats.city) == city_norm)
        record = session.exec(stmt).first()

        if record:
            record.count += 1
            record.last_searched = datetime.utcnow()
        else:
            record = CityStats(
                city=city_norm,
                count=1,
                last_searched=datetime.utcnow()
            )
            session.add(record)

        session.commit()
        session.refresh(record)
        return record

    @staticmethod
    def list_stats(session: Session) -> list[CityStats]:
        """
        Возвращает все записи статистики, отсортированные по убыванию количества и дате последнего запроса.
        """
        stmt = (
            select(CityStats)
            .order_by(CityStats.count.desc(), CityStats.last_searched.desc())
        )
        return session.exec(stmt).all()
