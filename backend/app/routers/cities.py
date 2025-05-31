from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.services.cities_service import fetch_city_suggestions
from app.schemas import CitySuggestion

router = APIRouter(tags=["cities"])

@router.get(
    "/cities",
    response_model=List[CitySuggestion],
    summary="Autocomplete city names",
    description="Возвращает до 5 вариантов городов по частичному совпадению имени."
)
async def get_cities(
    q: str = Query(
        ...,
        min_length=2,
        description="Часть названия города для автодополнения"
    )
) -> List[CitySuggestion]:
    """
    Автодополнение названий городов через Nominatim.
    """
    try:
        suggestions = await fetch_city_suggestions(q)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Геокодер недоступен: {e}")

    return suggestions
