import logging
from enum import Enum
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class SearchProvider(str, Enum):
    """Поддерживаемые провайдеры поиска."""

    BRAVE = "brave"
    SERPAPI = "serpapi"


class Settings(BaseSettings):
    """Настройки приложения для веб-поиска."""

    APP_NAME: str = Field(default="Search MCP Server", description="Название приложения")

    BRAVE_API_KEY: str = Field(default="", description="API ключ Brave Search")
    BRAVE_API_BASE_URL: str = Field(
        default="https://api.search.brave.com/res/v1",
        description="Базовый URL для Brave Search API",
    )

    SERPAPI_API_KEY: str = Field(default="", description="API ключ SerpAPI")
    SERPAPI_BASE_URL: str = Field(
        default="https://serpapi.com",
        description="Базовый URL для SerpAPI",
    )

    SEARCH_PROVIDER: SearchProvider = Field(
        default=SearchProvider.BRAVE,
        description="Провайдер поиска (brave, serpapi)",
    )

    PORT: int = Field(default=8003, ge=1024, le=65535, description="Порт для запуска MCP сервера")
    HOST: str = Field(default="0.0.0.0", description="Хост для запуска MCP сервера")
    LOG_LEVEL: str = Field(default="INFO", description="Уровень логирования")

    REQUEST_TIMEOUT: int = Field(
        default=30,
        ge=5,
        le=120,
        description="Таймаут запросов в секундах",
    )
    DEFAULT_RESULTS_COUNT: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Количество результатов по умолчанию",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    def validate_required_fields(self) -> None:
        """Проверка обязательных полей."""
        if self.SEARCH_PROVIDER == SearchProvider.BRAVE:
            if not self.BRAVE_API_KEY:
                raise ValueError("BRAVE_API_KEY is required when using Brave Search")
        elif self.SEARCH_PROVIDER == SearchProvider.SERPAPI:
            if not self.SERPAPI_API_KEY:
                raise ValueError("SERPAPI_API_KEY is required when using SerpAPI")

    @property
    def brave_headers(self) -> dict[str, str]:
        """Заголовки для Brave Search API."""
        return {
            "Accept": "application/json",
            "X-Subscription-Token": self.BRAVE_API_KEY,
        }


@lru_cache()
def get_settings() -> Settings:
    """Получить экземпляр настроек (с кешированием)."""
    return Settings()


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Настройка логирования."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    return logging.getLogger("mcp_search")
