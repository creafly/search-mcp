from typing import Optional

from src.core.validators import (
    validate_count,
    validate_country_code,
    validate_freshness,
    validate_language,
    validate_offset,
    validate_query,
)
from src.entrypoints.mcp_instance import mcp
from src.services.search_service import SearchService


@mcp.tool()
async def search_web(
    query: str,
    count: Optional[int] = None,
    offset: Optional[int] = None,
    country: Optional[str] = None,
    language: Optional[str] = None,
    freshness: Optional[str] = None,
) -> dict:
    """
    Поиск в интернете.

    Args:
        query: Поисковый запрос
        count: Количество результатов (1-100, по умолчанию 10)
        offset: Смещение для пагинации
        country: Код страны (ISO 3166-1 alpha-2, например "US", "RU")
        language: Код языка (например "en", "ru")
        freshness: Свежесть результатов (pd=день, pw=неделя, pm=месяц, py=год)

    Returns:
        Результаты поиска с заголовками, описаниями и URL
    """
    query = validate_query(query)
    if count is not None:
        count = validate_count(count)
    if offset is not None:
        offset = validate_offset(offset)
    country = validate_country_code(country)
    language = validate_language(language)
    freshness = validate_freshness(freshness)

    service = SearchService()
    return await service.search_web(
        query,
        count=count,
        offset=offset,
        country=country,
        language=language,
        freshness=freshness,
    )
