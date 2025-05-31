from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import validator

class CityStats(SQLModel, table=True):
    """
    ORM-модель для хранения статистики по городам.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    city: str = Field(
        ..., 
        index=True, 
        unique=True, 
        nullable=False, 
        description="Normalized lowercase city name"
    )
    count: int = Field(
        default=0, 
        nullable=False, 
        description="Number of times this city was searched"
    )
    last_searched: datetime = Field(
        default_factory=datetime.utcnow, 
        nullable=False,
        description="Timestamp of the last search"
    )

    @validator("city", pre=True, always=True)
    def normalize_city(cls, v: str) -> str:
        """
        Приводим название города к нижнему регистру и убираем лишние пробелы,
        чтобы при сравнении не было дубликатов в разных регистрах.
        """
        return v.strip().lower()