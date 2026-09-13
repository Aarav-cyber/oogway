import pytest


@pytest.mark.asyncio
async def test_create_and_get_session(client):
    res = await client.post("/sessions", json={"title": "Test Growth Session"})
    assert res.status_code == 201
    data = res.json()
    session_id = data["id"]
    assert data["title"] == "Test Growth Session"

    # Get session
    get_res = await client.get(f"/sessions/{session_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == session_id


@pytest.mark.asyncio
async def test_list_sessions(client):
    await client.post("/sessions", json={"title": "Session 1"})
    await client.post("/sessions", json={"title": "Session 2"})

    res = await client.get("/sessions")
    assert res.status_code == 200
    sessions = res.json()["sessions"]
    assert len(sessions) >= 2
