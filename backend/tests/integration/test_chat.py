import pytest
from app.rag.ingest import ingest_document


@pytest.mark.asyncio
async def test_chat_message_flow_and_grounding(client, db_session):
    # Seed transcript
    await ingest_document(
        db=db_session,
        source_id="chesky-ep-1",
        title="Brian Chesky on Product Management",
        content="Brian Chesky discusses product retention, founder-led management, and focus at Airbnb.",
    )

    # Create session
    s_res = await client.post("/sessions", json={"title": "Chat Test"})
    session_id = s_res.json()["id"]

    # Send chat message
    c_res = await client.post(f"/sessions/{session_id}/messages", json={"content": "How does Brian Chesky handle product retention?"})
    assert c_res.status_code == 200
    data = c_res.json()

    assert data["message"]["role"] == "assistant"
    assert "retention" in data["message"]["content"].lower()
    assert data["skill"] == "grounded_qa"
    assert len(data["sources"]) > 0
    assert data["sources"][0]["title"] == "Brian Chesky on Product Management"


@pytest.mark.asyncio
async def test_session_isolation(client, db_session):
    s1_res = await client.post("/sessions", json={"title": "Session 1"})
    s1_id = s1_res.json()["id"]

    s2_res = await client.post("/sessions", json={"title": "Session 2"})
    s2_id = s2_res.json()["id"]

    await client.post(f"/sessions/{s1_id}/messages", json={"content": "My secret key is 12345"})

    # Fetch messages for s2
    m2_res = await client.get(f"/sessions/{s2_id}/messages")
    assert m2_res.status_code == 200
    messages_s2 = m2_res.json()
    assert len(messages_s2) == 0  # Guarantees session isolation
