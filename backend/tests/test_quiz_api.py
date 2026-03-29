import pytest
from datetime import datetime, timedelta, timezone

from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.quiz_service import quiz_service


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_full_quiz_flow(client: AsyncClient):
    """End-to-end: start quiz, submit answers, get price."""
    # Start
    resp = await client.post(
        "/api/quiz/start", json={"product_id": "bird-head-toque"}
    )
    assert resp.status_code == 201
    data = resp.json()
    session_id = data["session_id"]
    assert data["num_answers_required"] == 5

    # Submit answers
    started = datetime.fromisoformat(data["started_at"])
    answers = []
    t = started + timedelta(seconds=3)
    for name in ["Mount Rainier", "Mount Si", "Mailbox Peak", "Granite Mountain", "Mount Pilchuck"]:
        answers.append({"mountain_name": name, "answered_at": t.isoformat()})
        t += timedelta(seconds=5)

    resp = await client.post(
        f"/api/quiz/{session_id}/submit", json={"answers": answers}
    )
    assert resp.status_code == 200
    result = resp.json()
    assert 0 <= result["truthfulness_score"] <= 1
    # Authentic hiker should pay close to base price (low surcharge)
    assert result["final_price"] >= result["base_price"]
    assert result["surcharge_pct"] <= 30  # legit hikers without frontend metadata get mild surcharge
    assert result["base_price"] == 60.0

    # Retrieve pricing
    resp = await client.get(f"/api/pricing/{session_id}")
    assert resp.status_code == 200
    assert resp.json()["final_price"] == result["final_price"]


@pytest.mark.asyncio
async def test_start_invalid_product(client: AsyncClient):
    resp = await client.post(
        "/api/quiz/start", json={"product_id": "nonexistent"}
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_submit_to_nonexistent_session(client: AsyncClient):
    resp = await client.post(
        "/api/quiz/fake-session-id/submit",
        json={
            "answers": [
                {"mountain_name": f"Mountain {i}", "answered_at": datetime.now(timezone.utc).isoformat()}
                for i in range(5)
            ]
        },
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_double_submit(client: AsyncClient):
    """Submitting twice to the same session should fail."""
    resp = await client.post(
        "/api/quiz/start", json={"product_id": "bird-head-toque"}
    )
    session_id = resp.json()["session_id"]
    started = datetime.fromisoformat(resp.json()["started_at"])

    answers = [
        {"mountain_name": f"Mount Everest", "answered_at": (started + timedelta(seconds=i + 3)).isoformat()}
        for i in range(5)
    ]

    resp1 = await client.post(f"/api/quiz/{session_id}/submit", json={"answers": answers})
    assert resp1.status_code == 200

    resp2 = await client.post(f"/api/quiz/{session_id}/submit", json={"answers": answers})
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_expired_session(client: AsyncClient):
    """Submitting to an expired session should return 410."""
    resp = await client.post(
        "/api/quiz/start", json={"product_id": "bird-head-toque"}
    )
    session_id = resp.json()["session_id"]

    # Manually expire the session
    session = quiz_service.get_session(session_id)
    session.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)

    answers = [
        {"mountain_name": "Everest", "answered_at": datetime.now(timezone.utc).isoformat()}
        for _ in range(5)
    ]

    resp = await client.post(f"/api/quiz/{session_id}/submit", json={"answers": answers})
    assert resp.status_code == 410


@pytest.mark.asyncio
async def test_products_list(client: AsyncClient):
    resp = await client.get("/api/products")
    assert resp.status_code == 200
    products = resp.json()["products"]
    assert len(products) >= 1
    assert any(p["id"] == "bird-head-toque" for p in products)
