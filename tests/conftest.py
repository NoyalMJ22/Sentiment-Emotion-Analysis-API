import pytest
from httpx import AsyncClient
from app.main import app

# Create a master fixture that passes an async Test Client everywhere
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
