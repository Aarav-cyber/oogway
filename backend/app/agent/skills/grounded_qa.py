from typing import List, Dict, Any, Tuple
from app.llm.base import BaseLLMProvider
from app.rag.sources import RetrievedChunk, SourceMetadata


GROUNDED_QA_SYSTEM_PROMPT = """You are the Lenny Growth Assistant, an expert AI advisor trained on Lenny's Podcast and Newsletter material.

Your task is to answer product and growth questions based ONLY on the provided Lenny transcript context.

Rules:
1. Ground every claim directly in the provided transcript context.
2. Cite or mention the episode/source when providing insights.
3. If the provided transcript context does NOT contain enough relevant information to answer the question, state explicitly: "I don't have enough information in the available Lenny transcript material to answer that confidently."
4. Do NOT invent or hallucinate transcript claims or guests.
5. Use a friendly, structured, professional tone suitable for product managers and founders.
"""


class GroundedQASkill:
    @staticmethod
    async def execute(
        llm: BaseLLMProvider,
        query: str,
        conversation_history: List[Dict[str, str]],
        chunks: List[RetrievedChunk],
    ) -> Tuple[str, List[SourceMetadata]]:
        sources: List[SourceMetadata] = []

        if not chunks:
            answer = "I don't have enough information in the available Lenny transcript material to answer that confidently."
            return answer, []

        context_blocks = []
        for c in chunks:
            source_meta = SourceMetadata(
                document_id=c.document_id,
                chunk_id=c.chunk_id,
                title=c.title,
                source_url=c.source_url,
                episode_date=c.metadata.get("episode_date"),
                snippet=c.text[:200] + "...",
            )
            sources.append(source_meta)
            context_blocks.append(
                f"Source Title: {c.title}\nSource URL: {c.source_url or 'N/A'}\nContext:\n{c.text}\n---"
            )

        context_str = "\n\n".join(context_blocks)
        user_content = f"TRANSCRIPT CONTEXT:\n{context_str}\n\nUSER QUESTION: {query}"

        messages = list(conversation_history)
        messages.append({"role": "user", "content": user_content})

        answer = await llm.generate(
            messages=messages,
            system_prompt=GROUNDED_QA_SYSTEM_PROMPT,
            temperature=0.3,
        )

        return answer, sources
