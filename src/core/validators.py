import re
from typing import Optional


def validate_query(query: str) -> str:
    """Валидация поискового запроса."""
    if not query or not isinstance(query, str):
        raise ValueError("Search query is required and must be a string")

    query = query.strip()
    if not query:
        raise ValueError("Search query cannot be empty")

    if len(query) > 500:
        raise ValueError("Search query is too long (max 500 characters)")

    return query


def validate_count(count: int, max_count: int = 100) -> int:
    """Валидация количества результатов."""
    if count < 1:
        raise ValueError("Results count must be at least 1")
    if count > max_count:
        raise ValueError(f"Results count cannot exceed {max_count}")

    return count


def validate_offset(offset: int) -> int:
    """Валидация смещения результатов."""
    if offset < 0:
        raise ValueError("Offset cannot be negative")

    return offset


def validate_country_code(country: Optional[str]) -> Optional[str]:
    """Валидация кода страны (ISO 3166-1 alpha-2)."""
    if country is None:
        return None

    country = country.strip().upper()
    if not country:
        return None

    if not re.match(r"^[A-Z]{2}$", country):
        raise ValueError("Invalid country code format (expected ISO 3166-1 alpha-2)")

    return country


def validate_language(language: Optional[str]) -> Optional[str]:
    """Валидация кода языка."""
    if language is None:
        return None

    language = language.strip().lower()
    if not language:
        return None

    if not re.match(r"^[a-z]{2}(-[A-Za-z]{2})?$", language):
        raise ValueError("Invalid language code format")

    return language


def validate_freshness(freshness: Optional[str]) -> Optional[str]:
    """Валидация параметра свежести результатов."""
    valid_values = ["pd", "pw", "pm", "py"]

    if freshness is None:
        return None

    freshness = freshness.strip().lower()
    if not freshness:
        return None

    if freshness not in valid_values:
        raise ValueError(f"Invalid freshness value. Must be one of: {', '.join(valid_values)}")

    return freshness
