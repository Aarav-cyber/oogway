import pytest


@pytest.mark.asyncio
async def test_persistence_of_session_and_messages(client):
    s_res = await client.post("/sessions", json={"title": "Persistent Session"})
    session_id = s_res.json()["id"]

    await client.post(f"/sessions/{session_id}/messages", json={"content": "First user message"})

    msg_res = await client.get(f"/sessions/{session_id}/messages")
    assert msg_res.status_code == 200
    messages = msg_res.json()
    assert len(messages) == 2  # 1 user message + 1 assistant message
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "First user message"
    assert messages[1]["role"] == "assistant"
