import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.cache import CacheManager
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_chat_endpoint_with_mocked_cache():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/chat", params={"query": "test"})
        assert response.status_code == 200

@pytest.fixture(scope="module")
def client():
    """Creates a test client for FastAPI app."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_chat_endpoint_with_mocked_cache(client):
    """Tests the /chat endpoint with mocked cache, search, and model responses."""

    query = "What is FastAPI?"
    mock_cache_get = AsyncMock(return_value=None)
    mock_cache_set = AsyncMock()

    with patch.object(cache, "get", mock_cache_get):
        with patch.object(cache, "set", mock_cache_set):
            with patch("app.search.search_web", AsyncMock(return_value=["https://example.com"])):
                with patch("app.parser.parse_content", AsyncMock(return_value={"url": "https://example.com", "content": "Example content"})):
                    with patch("app.main.generate_with_ollama", AsyncMock(return_value="FastAPI is a modern web framework")):

                        response = client.post("/chat", params={"query": query})
                        
                        assert response.status_code == 200
                        assert "response" in response.json()
                        assert response.json()["response"] == "FastAPI is a modern web framework"

    mock_cache_get.assert_called_once_with(query)
    mock_cache_set.assert_called_once()


@pytest.mark.asyncio
async def test_chat_endpoint_with_cached_response(client):
    """Tests if the /chat endpoint returns cached results."""

    query = "What is FastAPI?"
    mock_cache_get = AsyncMock(return_value="Cached FastAPI response")

    with patch.object(cache, "get", mock_cache_get):
        response = client.post("/chat", params={"query": query})

        assert response.status_code == 200
        assert response.json()["response"] == "Cached FastAPI response"

    mock_cache_get.assert_called_once_with(query)


@pytest.mark.asyncio
async def test_chat_endpoint_search_error(client):
    """Tests handling of search failure."""

    query = "What is FastAPI?"
    
    with patch.object(cache, "get", AsyncMock(return_value=None)):
        with patch("app.search.search_web", AsyncMock(side_effect=Exception("Search error"))):

            response = client.post("/chat", params={"query": query})

            assert response.status_code == 500
            assert "Search error" in response.json()["detail"]


