from typing import Optional

from src.core.validators import validate_count, validate_country_code, validate_query
from src.entrypoints.mcp_instance import mcp
from src.services.search_service import SearchService


@mcp.tool()
async def search_images(
    query: str,
    count: Optional[int] = None,
    country: Optional[str] = None,
    safe_search: bool = True,
) -> dict:
    """
    Поиск изображений.

    Args:
        query: Поисковый запрос
        count: Количество результатов (1-100, по умолчанию 10)
        country: Код страны (ISO 3166-1 alpha-2)
        safe_search: Безопасный поиск (по умолчанию включен)

    Returns:
        Изображения с URL, размерами и источниками
    """
    query = validate_query(query)
    if count is not None:
        count = validate_count(count)
    country = validate_country_code(country)

    service = SearchService()
    return await service.search_images(
        query,
        count=count,
        country=country,
        safe_search=safe_search,
    )
