import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    res = await client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_readiness_endpoint(client):
    res = await client.get("/ready")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "database" in data
    assert "llm" in data
