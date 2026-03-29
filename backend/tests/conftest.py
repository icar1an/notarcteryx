import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.mountain_db import mountain_db


@pytest.fixture(scope="session", autouse=True)
def _load_mountains():
    mountain_db.load()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
