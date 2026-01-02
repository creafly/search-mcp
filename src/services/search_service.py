import logging
from typing import Any, Optional

import httpx

from src.core.settings import SearchProvider, Settings, get_settings


class SearchService:
    """Сервис для веб-поиска через различные API."""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.logger = logging.getLogger("mcp_search.service")

    async def search_web(
        self,
        query: str,
        count: Optional[int] = None,
        offset: Optional[int] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        freshness: Optional[str] = None,
    ) -> dict[str, Any]:
        """Поиск в интернете."""
        if self.settings.SEARCH_PROVIDER == SearchProvider.BRAVE:
            return await self._brave_web_search(query, count, offset, country, language, freshness)
        else:
            return await self._serpapi_search(query, "google", count, offset, country, language)

    async def search_news(
        self,
        query: str,
        count: Optional[int] = None,
        offset: Optional[int] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        freshness: Optional[str] = None,
    ) -> dict[str, Any]:
        """Поиск новостей."""
        if self.settings.SEARCH_PROVIDER == SearchProvider.BRAVE:
            return await self._brave_news_search(query, count, offset, country, language, freshness)
        else:
            return await self._serpapi_search(
                query, "google_news", count, offset, country, language
            )

    async def search_images(
        self,
        query: str,
        count: Optional[int] = None,
        country: Optional[str] = None,
        safe_search: bool = True,
    ) -> dict[str, Any]:
        """Поиск изображений."""
        if self.settings.SEARCH_PROVIDER == SearchProvider.BRAVE:
            return await self._brave_image_search(query, count, country, safe_search)
        else:
            return await self._serpapi_search(query, "google_images", count, None, country, None)

    async def _brave_web_search(
        self,
        query: str,
        count: Optional[int],
        offset: Optional[int],
        country: Optional[str],
        language: Optional[str],
        freshness: Optional[str],
    ) -> dict[str, Any]:
        """Brave Web Search."""
        params: dict[str, Any] = {"q": query}
        if count:
            params["count"] = count
        if offset:
            params["offset"] = offset
        if country:
            params["country"] = country
        if language:
            params["search_lang"] = language
        if freshness:
            params["freshness"] = freshness

        async with httpx.AsyncClient(
            base_url=self.settings.BRAVE_API_BASE_URL,
            headers=self.settings.brave_headers,
            timeout=self.settings.REQUEST_TIMEOUT,
        ) as client:
            response = await client.get("/web/search", params=params)
            response.raise_for_status()
            return response.json()

    async def _brave_news_search(
        self,
        query: str,
        count: Optional[int],
        offset: Optional[int],
        country: Optional[str],
        language: Optional[str],
        freshness: Optional[str],
    ) -> dict[str, Any]:
        """Brave News Search."""
        params: dict[str, Any] = {"q": query}
        if count:
            params["count"] = count
        if offset:
            params["offset"] = offset
        if country:
            params["country"] = country
        if language:
            params["search_lang"] = language
        if freshness:
            params["freshness"] = freshness

        async with httpx.AsyncClient(
            base_url=self.settings.BRAVE_API_BASE_URL,
            headers=self.settings.brave_headers,
            timeout=self.settings.REQUEST_TIMEOUT,
        ) as client:
            response = await client.get("/news/search", params=params)
            response.raise_for_status()
            return response.json()

    async def _brave_image_search(
        self,
        query: str,
        count: Optional[int],
        country: Optional[str],
        safe_search: bool,
    ) -> dict[str, Any]:
        """Brave Image Search."""
        params: dict[str, Any] = {"q": query}
        if count:
            params["count"] = count
        if country:
            params["country"] = country
        params["safesearch"] = "strict" if safe_search else "off"

        async with httpx.AsyncClient(
            base_url=self.settings.BRAVE_API_BASE_URL,
            headers=self.settings.brave_headers,
            timeout=self.settings.REQUEST_TIMEOUT,
        ) as client:
            response = await client.get("/images/search", params=params)
            response.raise_for_status()
            return response.json()

    async def _serpapi_search(
        self,
        query: str,
        engine: str,
        count: Optional[int],
        offset: Optional[int],
        country: Optional[str],
        language: Optional[str],
    ) -> dict[str, Any]:
        """SerpAPI Search."""
        params: dict[str, Any] = {
            "q": query,
            "engine": engine,
            "api_key": self.settings.SERPAPI_API_KEY,
        }
        if count:
            params["num"] = count
        if offset:
            params["start"] = offset
        if country:
            params["gl"] = country.lower()
        if language:
            params["hl"] = language

        async with httpx.AsyncClient(
            base_url=self.settings.SERPAPI_BASE_URL,
            timeout=self.settings.REQUEST_TIMEOUT,
        ) as client:
            response = await client.get("/search", params=params)
            response.raise_for_status()
            return response.json()
