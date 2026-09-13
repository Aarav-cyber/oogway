import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.document import DocumentModel, ChunkModel
from app.rag.chunking import chunk_text
import logging

logger = logging.getLogger("lenny_backend")


async def ingest_document(
    db: AsyncSession,
    source_id: str,
    title: str,
    content: str,
    source_url: Optional[str] = None,
    episode_date: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> DocumentModel:
    """Ingests or updates a transcript document and creates searchable chunks in the database."""
    # Check if doc exists
    result = await db.execute(select(DocumentModel).where(DocumentModel.source_id == source_id))
    doc = result.scalar_one_or_none()

    if not doc:
        doc = DocumentModel(
            id=str(uuid.uuid4()),
            source_id=source_id,
            title=title,
            source_url=source_url,
            episode_date=episode_date,
            doc_metadata=metadata or {},
        )
        db.add(doc)
        await db.flush()
    else:
        doc.title = title
        doc.source_url = source_url
        doc.episode_date = episode_date
        doc.doc_metadata = metadata or {}
        # Delete old chunks
        old_chunks = await db.execute(select(ChunkModel).where(ChunkModel.document_id == doc.id))
        for old_c in old_chunks.scalars().all():
            await db.delete(old_c)
        await db.flush()

    raw_chunks = chunk_text(content)
    for idx, chunk_str in enumerate(raw_chunks):
        chunk_obj = ChunkModel(
            id=str(uuid.uuid4()),
            document_id=doc.id,
            chunk_index=idx,
            text=chunk_str,
            title=title,
            source_url=source_url,
            chunk_metadata={
                "source_id": source_id,
                "episode_date": episode_date,
                "chunk_index": idx,
            },
        )
        db.add(chunk_obj)

    await db.commit()
    logger.info(f"Ingested document '{title}' ({source_id}) with {len(raw_chunks)} chunks.")
    return doc
