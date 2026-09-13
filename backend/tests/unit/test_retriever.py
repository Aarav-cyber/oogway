import pytest
from app.rag.ingest import ingest_document
from app.rag.retriever import Retriever


@pytest.mark.asyncio
async def test_retrieval_quality_and_grounding(db_session):
    # Ingest test document
    await ingest_document(
        db=db_session,
        source_id="test-doc-1",
        title="Brian Chesky Airbnb Growth",
        content="Brian Chesky emphasizes that retention is crucial before scaling user acquisition at Airbnb.",
        source_url="https://example.com/brian",
        episode_date="2023-11-02",
    )

    # Search relevant query
    results = await Retriever.retrieve_chunks(db_session, query="retrieval Airbnb user acquisition", top_k=3, min_score=0.1)
    assert len(results) > 0
    assert results[0].document_id is not None
    assert results[0].title == "Brian Chesky Airbnb Growth"
    assert "retention is crucial" in results[0].text


@pytest.mark.asyncio
async def test_unrelated_query_empty_retrieval(db_session):
    await ingest_document(
        db=db_session,
        source_id="test-doc-1",
        title="Brian Chesky Airbnb Growth",
        content="Brian Chesky emphasizes retention.",
    )

    results = await Retriever.retrieve_chunks(db_session, query="quantum mechanics particle physics relativity", min_score=2.0)
    assert len(results) == 0
