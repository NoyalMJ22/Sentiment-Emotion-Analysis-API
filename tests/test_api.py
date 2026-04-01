import pytest
from httpx import AsyncClient
from app.core.config import settings

# Important: Allows testing of Async FastAPI endpoints gracefully
pytestmark = pytest.mark.asyncio(scope="session")

class TestSentimentAPI:
    async def test_analyze_no_auth(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/analyze",
            json={"text": "I absolutely love this!"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid or missing X-API-Key header"

    async def test_analyze_success(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/analyze",
            headers={"X-API-Key": settings.API_KEY},
            json={"text": "This fast API is incredibly fast and amazing!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "positive"
        assert "emotions" in data
        assert "joy" in data["emotions"]

    async def test_batch_analyze(self, async_client: AsyncClient):
        response = await async_client.post(
            "/api/v1/analyze/batch",
            headers={"X-API-Key": settings.API_KEY},
            json={"texts": ["I am so happy today!", "This is the worst experience."]}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 2
        assert data["results"][0]["sentiment"] == "positive"
        assert data["results"][1]["sentiment"] == "negative"
