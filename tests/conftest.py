import pytest


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    from unittest.mock import MagicMock

    from src.core.settings import SearchProvider

    settings = MagicMock()
    settings.BRAVE_API_KEY = "test_key"
    settings.BRAVE_API_BASE_URL = "https://api.search.brave.com/res/v1"
    settings.SERPAPI_API_KEY = "test_key"
    settings.SERPAPI_BASE_URL = "https://serpapi.com"
    settings.SEARCH_PROVIDER = SearchProvider.BRAVE
    settings.REQUEST_TIMEOUT = 30
    settings.brave_headers = {
        "Accept": "application/json",
        "X-Subscription-Token": "test_key",
    }
    return settings


@pytest.fixture
def mock_search_service(mock_settings):
    """Mock search service for testing."""
    from unittest.mock import AsyncMock, MagicMock

    service = MagicMock()
    service.settings = mock_settings
    service.search_web = AsyncMock(return_value={"web": {"results": []}})
    service.search_news = AsyncMock(return_value={"news": {"results": []}})
    service.search_images = AsyncMock(return_value={"images": {"results": []}})
    return service
