from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.document import ChunkModel, DocumentModel
from app.rag.embeddings import TextVectorizer
from app.rag.sources import RetrievedChunk, SourceMetadata
import logging

logger = logging.getLogger("lenny_backend")


class Retriever:
    @staticmethod
    async def retrieve_chunks(
        db: AsyncSession,
        query: str,
        top_k: int = 5,
        min_score: float = 0.5,
    ) -> List[RetrievedChunk]:
        """Retrieves top_k relevant transcript chunks using BM25 relevance scoring against DB chunks."""
        result = await db.execute(select(ChunkModel))
        all_chunks = result.scalars().all()

        if not all_chunks:
            logger.info("No chunks found in database.")
            return []

        query_tokens = TextVectorizer.tokenize(query)
        if not query_tokens:
            return []

        docs_tokens = [TextVectorizer.tokenize(chunk.text) for chunk in all_chunks]
        total_len = sum(len(dt) for dt in docs_tokens)
        avg_doc_len = total_len / len(all_chunks) if all_chunks else 1.0
        idf_dict = TextVectorizer.calculate_idfs(docs_tokens)

        scored_chunks = []
        for chunk, tokens in zip(all_chunks, docs_tokens):
            score = TextVectorizer.compute_bm25_score(
                query_tokens=query_tokens,
                doc_tokens=tokens,
                avg_doc_len=avg_doc_len,
                idf_dict=idf_dict,
            )
            if score >= min_score:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_results = scored_chunks[:top_k]

        retrieved = []
        for score, chunk in top_results:
            retrieved.append(
                RetrievedChunk(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    title=chunk.title,
                    text=chunk.text,
                    source_url=chunk.source_url,
                    score=score,
                    metadata=chunk.chunk_metadata or {},
                )
            )

        return retrieved
