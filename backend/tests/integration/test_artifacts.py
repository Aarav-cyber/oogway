import pytest


@pytest.mark.asyncio
async def test_artifact_generation_and_retrieval(client):
    s_res = await client.post("/sessions", json={"title": "Artifact Session"})
    session_id = s_res.json()["id"]

    c_res = await client.post(f"/sessions/{session_id}/messages", json={"content": "Create HTML artifact summarizing retention strategy"})
    assert c_res.status_code == 200
    data = c_res.json()

    assert data["artifact_id"] is not None
    artifact_id = data["artifact_id"]

    # Fetch artifact directly
    art_res = await client.get(f"/artifacts/{artifact_id}")
    assert art_res.status_code == 200
    art_data = art_res.json()
    assert art_data["type"] == "html"
    assert "Generated HTML Title" in art_data["content"]
