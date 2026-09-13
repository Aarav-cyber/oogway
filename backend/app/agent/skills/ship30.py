from typing import List, Dict, Any, Tuple
from app.llm.base import BaseLLMProvider
from app.rag.sources import RetrievedChunk, SourceMetadata


SHIP30_SYSTEM_PROMPT = """You are a Ship 30 for 30 Writing Expert. Your job is to transform product/growth insights into a high-impact, skimmable 1,250-word atomic essay.

Key Output Requirements:
1. Length: Approximately 1,250 words long.
2. Hook: Start with a powerful 1-2 sentence hook that grabs the reader's attention.
3. Narrative Progression: Clear logical flow from problem statement to actionable framework.
4. Skimmability: Use bold, clear H2/H3 headings, short 1-3 sentence paragraphs.
5. Formatting: Use bullet points for steps/lists and selective **bold emphasis** on crucial keywords.
6. Takeaways: End with a specific, highly actionable takeaway summary for the reader.
7. Grounding: All core concepts must be grounded in the provided Lenny transcript insights. Do NOT invent false facts.
"""


class Ship30Skill:
    @staticmethod
    async def execute(
        llm: BaseLLMProvider,
        query: str,
        conversation_history: List[Dict[str, str]],
        chunks: List[RetrievedChunk],
    ) -> Tuple[str, List[SourceMetadata]]:
        sources: List[SourceMetadata] = []

        context_blocks = []
        for c in chunks:
            sources.append(
                SourceMetadata(
                    document_id=c.document_id,
                    chunk_id=c.chunk_id,
                    title=c.title,
                    source_url=c.source_url,
                    episode_date=c.metadata.get("episode_date"),
                    snippet=c.text[:200] + "...",
                )
            )
            context_blocks.append(f"Source: {c.title}\n{c.text}")

        context_str = "\n\n".join(context_blocks) if context_blocks else "Use previous conversation context."

        prompt = (
            f"Please write a full Ship 30 for 30 style atomic essay (~1,250 words) based on:\n\n"
            f"USER REQUEST: {query}\n\n"
            f"TRANSCRIPT GROUNDING CONTEXT:\n{context_str}"
        )

        messages = list(conversation_history)
        messages.append({"role": "user", "content": prompt})

        essay = await llm.generate(
            messages=messages,
            system_prompt=SHIP30_SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=4096,
        )

        return essay, sources
