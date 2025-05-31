from typing import List
import httpx
from fastapi import HTTPException, status
from app.schemas import CitySuggestion

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "weather-app/1.0"

async def fetch_city_suggestions(
    query: str,
    limit: int = 5
) -> List[CitySuggestion]:
    """
    Подсказки городов через Nominatim, возвращает список CitySuggestion.

    - query: строка поиска (минимум 3 символа)
    - limit: максимальное число результатов
    """
    q = query.strip()
    if len(q) < 3:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Query must be at least 3 characters long"
        )

    params = {
        "q": q,
        "format": "json",
        "limit": limit * 2  
    }
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "ru"
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(NOMINATIM_URL, params=params, headers=headers)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Geocoding service error: {exc.response.status_code}"
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to connect to geocoding service: {exc}"
            )

    raw = resp.json()
    suggestions: List[CitySuggestion] = []
    seen = set()

    for item in raw:
        full = item.get("display_name", "").strip()
        if not full:
            continue

        name = full.split(",", 1)[0]
        if name in seen:
            continue
        seen.add(name)

        lat = item.get("lat")
        lon = item.get("lon")
        if lat is None or lon is None:
            continue

        try:
            suggestions.append(
                CitySuggestion(name=name, lat=float(lat), lon=float(lon))
            )
        except (ValueError, TypeError):
            continue

        if len(suggestions) >= limit:
            break

    return suggestions