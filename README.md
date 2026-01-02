# Search MCP Server

[![CI](https://github.com/creafly/search-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/creafly/search-mcp/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/creafly/search-mcp)](https://github.com/creafly/search-mcp/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/creafly/search-mcp/pulls)

MCP server for web search via various APIs.

## Features

- **search_web** - Web search
- **search_news** - News search
- **search_images** - Image search

## Supported Providers

### Brave Search API

- Free plan: 2000 requests/month
- Get API key: https://brave.com/search/api/

### SerpAPI

- Free plan: 100 requests/month
- Get API key: https://serpapi.com/

## Installation

```bash
# Install dependencies
make install

# Or for development
make dev
```

## Configuration

Create a `.env` file:

```env
# Brave Search (recommended)
BRAVE_API_KEY=your_brave_api_key

# Or SerpAPI
SERPAPI_API_KEY=your_serpapi_key

# Provider selection
SEARCH_PROVIDER=brave  # brave | serpapi

# Server settings
PORT=8003
HOST=0.0.0.0
LOG_LEVEL=INFO
```

## Running

```bash
make run
```

## Docker

```bash
docker build -t search-mcp .
docker run -p 8003:8003 --env-file .env search-mcp
```

## Tests

```bash
make test
```

## License

MIT
