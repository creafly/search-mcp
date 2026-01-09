from fastmcp import FastMCP

from src.core.settings import get_settings

settings = get_settings()

mcp = FastMCP(
    name=settings.APP_NAME,
    instructions="""
    Search MCP Server - сервер для веб-поиска через различные API.

    Возможности:
    - Поиск в интернете (web search)
    - Поиск новостей (news search)
    - Поиск изображений (image search)

    Поддерживаемые провайдеры:
    - Brave Search API
    - SerpAPI (Google Search)

    Для работы требуется API ключ выбранного провайдера.
    """,
)
